import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
from time import sleep
from fileManager import FileManager


class MVNscrapper():

    def __init__(self, project, max_depth, f_dir, p_dir):
        p = self.separateV(project, getRoot = True, getVersion = True, getModule = True)
        self.project = p[0]
        self.version = p[1]
        self.max_depth = max_depth
        self.f_manager = FileManager(f_dir, p_dir, p[2])

        done = False
        while not done:
            try:
                self.scrap(self.project, self.max_depth, 0, target_version = self.version)
                self.f_manager.copyToFinal()
                done = True
            except:
                done = False

        

    def getSoup(self, url):
        # Set headers  
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser', parse_only=SoupStrainer('a'))
        sleep(2)

        return soup

    def separateV(self, project, getRoot = True, getVersion = True, getModule = False):
        aux1 = project[project.find('/artifact'):][10:] #return project/module/version
        aux2 = aux1[aux1.find('/'):][1:] #return module/version
        version = aux2[aux2.find('/'):] #return /version
        root = project[:project.find(version)]

        response = []

        if getRoot:
            response.append(root)
        if getVersion:
            response.append(version)
        if getModule:
            response.append(aux1)

        return response

    def fetchVersions(self, soup):

        versions = []
        multiple_versions = False
        for tag in soup.find_all('a'):
            if tag.get('class') and tag.get('class')[0] == 'vsc':
                multiple_versions = True
                break

        if multiple_versions:
            for tag in soup.find_all('a', class_='vsc'):
                versions.append(tag.get('href'))
        else:
            for tag in soup.find_all('a', class_='vbtn'):
                versions.append(tag.get('href'))

        return versions

    def searchDependency(self, url, dependency):
        soup = self.getSoup(url)

        for tag in soup.find_all('a'):
            link = tag.get('href')
            if link[10:] == dependency:
                return True

        return False

    def fetchDependencies(self, module, url):
        soup = self.getSoup(url)

        self.f_manager.setState(module, 'Getting dependencies')

        found = False
        scope = False
        dependencies = []

        for tag in soup.find_all('a'):
            link = tag.get('href')
            
            if scope:
                if 'twitter' in link:
                    scope = False
                if '/artifact' in link:
                    if not tag.get('class'):
                        found = False
                    if not found and tag.get('class') and len(tag.get('class')) > 1 and tag.get('class')[0] == 'vbtn':
                        dependencies.append(link[10:])
                        self.f_manager.setDependency(module, link[10:])
                        found = True

            if '#buildr' in link:
                scope = True

        return dependencies

    def fetchUsages(self, module, url, page=None):
        soup = self.getSoup(url)

        module_root = self.separateV(module, getModule = True)[0]

        self.f_manager.setState(module, 'Getting usages')

        if not page:
            print('Page 1')

        usages = []
        previous = ''
        scope = False
        end = False
        next_page = 0
        current_page = 0
        
        while not end:

            for tag in soup.find_all('a'):
                link = tag.get('href')

                if page:
                    usages_page_link = url + '?p=' + page
                    print("Continued on page " + page)
                    soup = self.getSoup(usages_page_link)
                    current_page = int(page)
                    self.f_manager.setCurrentPage(module, page)
                    page = None

                if scope:

                    if 'artifact' in link:
                        if link == previous:
                            if link not in usages:
                                usages.append(link[10:])
                                self.f_manager.setUsage(module,link[10:])

                        previous = link

                    elif '?p=' in link:
                        next_page = int(link[3:])

                        if next_page > current_page:
                            scope = False
                            usages_page_link = url + link
                            soup = self.getSoup(usages_page_link)
                            current_page = int(link[3:])
                            print('Page',current_page)
                            self.f_manager.setCurrentPage(module, current_page)
                            break

                    elif '/tags' in link:
                        end = True
                        scope = False

                        break

                if module_root in link:
                    scope = True

        self.f_manager.setState(module, 'Done usages')

        return usages

    def getUsageVersion(self, root_link, target_version, lookForDependency):
        root_soup = self.getSoup(root_link)
        module_root = root_link[root_link.find('/artifact'):][10:]

        versions = self.fetchVersions(root_soup)

        multiple_versions = False
        if '/artifact' in versions[0]:
            multiple_versions = True
        
        for vers in versions:
            #if multiple /artifact/abc/xyz/123
            #if not xyz/123

            if multiple_versions:
                vers = vers[10:]
                module = vers
            
            vers = vers[vers.find('/'):] 
            print("Currently on {}" .format(vers))

            if not multiple_versions:
                module = module_root + vers

            result = self.searchDependency("https://mvnrepository.com/artifact/"+module, lookForDependency)

            if result:
                print("Correct version is {}" .format(vers))
                return vers

        return None

    def saveDependencies(self, module, dependencies):
            self.f_manager.addModule(module)
            for dependency in dependencies:
                self.f_manager.addModule(dependency[2])
            self.f_manager.addLinks(module, dependencies)
            self.f_manager.setState(module, 'Done Dependencies')

            print('Updated nodes ans links')

    def getDependencies(self, module, link):
        dependencies = self.fetchDependencies(module, link)

        if len(dependencies) == 0:
            self.f_manager.setDependency(module, 'None')

        print('There are {} dependencies in the module {}' .format(len(dependencies), module))

        self.saveDependencies(module, dependencies)

    def getUsages(self, module, link, page = None):

        usages = self.fetchUsages(module, link)

        if len(usages) == 0:
            self.f_manager.setUsage(module, 'None')

        print('There are {} usages in the module {}' .format(len(usages), module))

    def verifyDependencies(self, module, max_depth, depth, current = None):

        if not current:
            for dependency in self.f_manager.getDependencies(module):
                if dependency != 'None':
                    print('Opening dependency:', dependency)
                    self.f_manager.setCurrent(module, 'd', dependency)
                    dep_link = 'https://mvnrepository.com/artifact/' + dependency
                    dep_root, dep_version = self.separateV(dep_link, getRoot = True, getVersion = True)
                    self.scrap(dep_root,max_depth,depth,target_version = dep_version)
                    print('Returned to', module)
        else:
            toDo = False
            for dependency in self.f_manager.getDependencies(module):
                if dependency != 'None':
                    if dependency == current:
                        toDo = True
                    if toDo:
                        print('Opening dependency:', dependency)
                        self.f_manager.setCurrent(module, 'd', dependency)
                        dep_link = 'https://mvnrepository.com/artifact/' + dependency
                        dep_root, dep_version = self.separateV(dep_link, getRoot = True, getVersion = True)
                        self.scrap(dep_root,max_depth,depth,target_version = dep_version)
                        print('Returned to', module)


    def verifyUsages(self, module, max_depth, depth, current = None):

        if not current:
            for usage in self.f_manager.getUsages(module):
                if usage != 'None':
                    print('Opening usage:', usage)
                    self.f_manager.setCurrent(module, 'u', usage)
                    self.scrap('https://mvnrepository.com/artifact/' + usage,max_depth,depth,lookForDependency = module)
                    print('Returned to', module)
        else:
            toDo = False
            for usage in self.f_manager.getUsages(module):
                if usage != 'None':
                    if usage == current:
                        toDo = True
                    if toDo:
                        print('Opening usage:', usage)
                        self.f_manager.setCurrent(module, 'u', usage)
                        self.scrap('https://mvnrepository.com/artifact/' + usage,max_depth,depth,lookForDependency = module)
                        print('Returned to', module)

    def scrap(self, root_link, max_depth,depth, target_version = None, lookForDependency = None):

        if target_version:
            version = target_version

        module_root = root_link[root_link.find('/artifact'):][10:]

        if not target_version:
            print("Looking for correct usage version")

            try:
                version = self.getUsageVersion(root_link, target_version, lookForDependency)
            except Exception as e:
                self.f_manager.initialize(module_root,depth)
                print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module_root))
                self.f_manager.setState(module_root, 'Error')
                return

            if not version:
                return

        module = module_root+version
        print("Current module:", module)

        inProgress = self.f_manager.checkProgress(module)

        if not inProgress:
            print('New module')

            self.f_manager.initialize(module,depth) #Status Initialized !! MUDAR !!!

            try:
                self.getDependencies(module, root_link+version)
            except Exception as e:
                print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module))
                self.f_manager.setState(module, 'Error')
                return

            depth+=1
            if depth < max_depth:

                self.getUsages(module,  root_link+version+'/usages')
                self.verifyDependencies(module, max_depth, depth)
                self.verifyUsages(module, max_depth, depth)

            else:
                print("Depth too high")

            self.f_manager.setState(module, 'Complete')
            return

        elif inProgress:
            print('Module in progress')

            mod = self.f_manager.getProgress(module)
            progress = mod[2]
            depth = int(mod[0])
            status = mod[4]

            if progress != 'Complete' and progress != 'Error':
                if status == 'closed':

                    self.f_manager.switchStatus(module)

                    if progress == 'Getting dependencies' or progress == 'Initialized':
                        print('Returned to get dependencies')

                        self.getDependencies(module, root_link+version)

                        depth+=1
                        if depth < max_depth:

                            self.getUsages(module,  root_link+version+'/usages')
                            self.verifyDependencies(module, max_depth, depth)
                            self.verifyUsages(module, max_depth, depth)

                        else:
                            print("Depth too high")

                        self.f_manager.setState(module, 'Complete')
                        return

                    if progress == 'Getting usages' or progress == 'Done dependencies':
                        depth+=1
                        if depth < max_depth:

                            print('Returned to getting usages')
                            currentPage = mod[3]
                            if currentPage == 'Null':
                                print('Page count error. Returning to first page')
                                currentPage = '1'
                            else:
                                print('Current usage page: {}' .format(currentPage))

                            self.getUsages(module, root_link+version+'/usages', page = currentPage)
                            self.verifyDependencies(module, max_depth, depth)
                            self.verifyUsages(module, max_depth, depth)

                        else:
                            print("Depth too high")

                        self.f_manager.setState(module, 'Complete')
                        return

                    if progress == 'Verifying dependency' or progress == 'Done usages':
                        depth+=1
                        if depth < max_depth:

                            print('Returned to verifying dependencies')
                            currentDependency = mod[3]
                            print('Current dependency: {}' .format(currentDependency))

                            self.verifyDependencies(module, max_depth, depth, current = currentDependency)
                            self.verifyUsages(module, max_depth, depth)

                        else:
                            print("Depth too high")

                        self.f_manager.setState(module, 'Complete')
                        return

                    if progress == 'Verifying usage':
                        depth+=1
                        if depth < max_depth:

                            print('Returned to verifying usages')
                            currentUsage = mod[3]
                            print('Current usage: {}' .format(currentUsage))

                            self.verifyUsages(module, max_depth, depth, current = currentUsage)

                        else:
                            print("Depth too high")

                        self.f_manager.setState(module, 'Complete')
                        return
                else:
                    print(module, ' already open')
                    return
            else:
                print(module,'Already Veryfied')
                return