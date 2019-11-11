import requests
from bs4 import BeautifulSoup, SoupStrainer
from time import sleep
import random
from FileManager import FileManager


class MVNScrapper():

    def __init__(self, project, max_depth, f_dir, p_dir):
        p = self.separateV(project, getRoot = True, getVersion = True, getModule = True)
        self.project_url = p[0]
        self.version = p[1]
        self.module = p[2]
        self.max_depth = max_depth
        self.f_manager = FileManager(f_dir, p_dir, self.module)
        self.f_manager.verifyConfig('MVNRepository', self.project_url+self.version, self.max_depth, f_dir)

    def scrapper(self):
        while True:
            try:
                self.scrap(self.project_url, 0, target_version = self.version)
                self.f_manager.copyToFinal()
                break
            except requests.exceptions.ConnectionError:
                print('Essa internet eh top')
                sleep(30)
                self.f_manager.verifyDirectories(self.module)

    def getSoup(self, url):
        # Set headers  
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'})
        try:
            req = requests.get(url, headers)
            req.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403: 
                print('\n\nFORBIDDEN\n\n')
                exit()
        soup = BeautifulSoup(req.content, 'html.parser', parse_only=SoupStrainer('a'))

        timeout = random.randrange(5,10)
        sleep(timeout)

        return soup

    #mudar para string de tres bits, "001" retorna só o modulo, por exemplo.
    def separateV(self, project, getRoot = False, getVersion = False, getModule = False):
        if project.find('/artifact/') == -1:
            aux1 = project
        else:
            aux1 = project[project.find('/artifact/'):][10:] #return project/module/version
        aux2 = aux1[aux1.find('/'):][1:] #return module/version
        version = aux2[aux2.find('/'):] #return /version
        root_url = project[:project.find(version)] #return all before /artifact/

        response = []

        if getRoot:
            response.append(root_url)
        if getVersion:
            response.append(version)
        if getModule:
            response.append(aux1)

        return response

    def fetchVersions(self, url):
        soup = self.getSoup(url)

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

    def fetchDependencies(self, url, module):
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
                if '/artifact/' in link:
                    if not tag.get('class'):
                        found = False
                    if not found and tag.get('class') and len(tag.get('class')) > 1 and tag.get('class')[0] == 'vbtn':
                        dependencies.append(link[10:])
                        self.f_manager.writeDependency(module, link[10:])
                        found = True

            if '#buildr' in link:
                scope = True

        return dependencies

    def fetchUsages(self, url, module, page=None):
        soup = self.getSoup(url)

        module_root = self.separateV(module, getRoot = True)[0]

        self.f_manager.setState(module, 'Getting usages')

        usages = []
        previous = ''
        scope = False
        end = False
        next_page = 0
        current_page = 0

        if not page:
            print('Page 1')
        else:
            usages_page_link = url + '?p=' + page
            print("Continued on page " + page)
            soup = self.getSoup(usages_page_link)
            current_page = int(page)
            self.f_manager.setCurrentPage(module, page)
            page = None

        while not end:

            for tag in soup.find_all('a'):
                link = tag.get('href')

                if scope:

                    if '?p=' in link:
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

                    elif '/artifact/' in link:
                        if link == previous:
                            if link not in usages:
                                usages.append(link[10:])
                                self.f_manager.writeUsage(module,link[10:])

                        previous = link

                if module_root in link:
                    scope = True

        return usages

    def getUsageVersion(self, url, lookForDependency):
        module_root = url[url.find('/artifact/'):][10:]

        #passar só o  link
        versions = self.fetchVersions(url)
        
        if len(versions) == 0:
            return None

        multiple_versions = False
        if '/artifact/' in versions[0]:
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
                self.f_manager.addModule(dependency)
            self.f_manager.addLinks(module, dependencies)
            self.f_manager.setState(module, 'Done Dependencies')

            print('Updated nodes ans links')

    def getDependencies(self, url, module):
        dependencies = self.fetchDependencies(url, module)

        if len(dependencies) == 0:
            self.f_manager.writeDependency(module, 'None')

        self.saveDependencies(module, dependencies)
        print('There are {} dependencies in the module {}' .format(len(dependencies), module))

    def getUsages(self, url, module, page = None):
        usages = self.fetchUsages(url, module, page = page)

        if len(usages) == 0:
            self.f_manager.writeUsage(module, 'None')

        self.f_manager.setState(module, 'Done usages')
        print('There are {} usages in the module {}' .format(len(usages), module))

    def verifyDependencies(self, module, depth, current = None):

        if not current:
            for dependency in self.f_manager.readDependencies(module):
                if dependency != 'None':
                    print('Opening dependency:', dependency)
                    self.f_manager.setCurrentModule(module, 'd', dependency)
                    dep_url = 'https://mvnrepository.com/artifact/' + dependency
                    urlNversion = self.separateV(dep_url, getRoot = True, getVersion = True)
                    dep_root, dep_version = urlNversion[0], urlNversion[1]
                    self.scrap(dep_root,depth,target_version = dep_version)
                    print('Returned to', module)
                else: 
                    break
        else:
            toDo = False
            for dependency in self.f_manager.readDependencies(module):
                if dependency != 'None':
                    if dependency == current:
                        toDo = True
                    if toDo:
                        print('Opening dependency:', dependency)
                        self.f_manager.setCurrentModule(module, 'd', dependency)
                        dep_url = 'https://mvnrepository.com/artifact/' + dependency
                        urlNversion = self.separateV(dep_url, getRoot = True, getVersion = True)
                        dep_root, dep_version = urlNversion[0], urlNversion[1]
                        self.scrap(dep_root,depth,target_version = dep_version)
                        print('Returned to', module)
                else:
                    break


    def verifyUsages(self, module, depth, current = None):

        if not current:
            for usage in self.f_manager.readUsages(module):
                if usage != 'None':
                    print('Opening usage:', usage)
                    self.f_manager.setCurrentModule(module, 'u', usage)
                    self.scrap('https://mvnrepository.com/artifact/' + usage,depth,lookForDependency = module)
                    print('Returned to', module)
                else:
                    break
        else:
            toDo = False
            for usage in self.f_manager.readUsages(module):
                if usage != 'None':
                    if usage == current:
                        toDo = True
                    if toDo:
                        print('Opening usage:', usage)
                        self.f_manager.setCurrentModule(module, 'u', usage)
                        self.scrap('https://mvnrepository.com/artifact/' + usage,depth,lookForDependency = module)
                        print('Returned to', module)
                else:
                    break

    def scrap(self, root_url, depth, target_version = None, lookForDependency = None):

        if target_version:
            version = target_version

        module_root = root_url[root_url.find('/artifact'):][10:]

        if not target_version:
            print("Looking for correct usage version")

            try:
                version = self.getUsageVersion(root_url, lookForDependency)

            except requests.exceptions.HTTPError as e:
                self.f_manager.initialize(module_root,depth)
                print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module_root))
                self.f_manager.setState(module_root, 'Error')
                return

            if not version:
                return
            elif version.count('/') == 2:
                root_url = root_url.split('/')
                root_url = '/'.join(root_url[:-1])
                module_root = module_root[:module_root.find('/')]

        module = module_root+version
        print("Current module:", module)

        inProgress = self.f_manager.checkProgress(module)

        if not inProgress:
            print('New module')

            self.f_manager.initialize(module,depth) #Status Initialized !! MUDAR !!!

            try:
                self.getDependencies(root_url+version, module)
            except requests.exceptions.HTTPError as e:
                print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module))
                self.f_manager.setState(module, 'Error')
                return

            depth+=1
            if depth < self.max_depth:

                self.getUsages(root_url+version+'/usages', module)
                self.verifyDependencies(module, depth)
                self.verifyUsages(module, depth)

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

                        self.getDependencies(root_url+version, module)

                        depth+=1
                        if depth < self.max_depth:

                            self.getUsages(root_url+version+'/usages', module)
                            self.verifyDependencies(module, depth)
                            self.verifyUsages(module, depth)

                        else:
                            print("Depth too high")

                        self.f_manager.setState(module, 'Complete')
                        return

                    if progress == 'Getting usages' or progress == 'Done dependencies':
                        depth+=1
                        if depth < self.max_depth:

                            print('Returned to getting usages')
                            currentPage = mod[3]
                            if currentPage == 'Null':
                                print('Page count error. Returning to first page')
                                currentPage = '1'
                            else:
                                print('Current usage page: {}' .format(currentPage))

                            self.getUsages(root_url+version+'/usages', module, page = currentPage)
                            self.verifyDependencies(module, depth)
                            self.verifyUsages(module, depth)

                        else:
                            print("Depth too high")

                        self.f_manager.setState(module, 'Complete')
                        return

                    if progress == 'Verifying dependency' or progress == 'Done usages':
                        depth+=1
                        if depth < self.max_depth:

                            print('Returned to verifying dependencies')
                            currentDependency = mod[3]
                            print('Current dependency: {}' .format(currentDependency))

                            self.verifyDependencies(module, depth, current = currentDependency)
                            self.verifyUsages(module, depth)

                        else:
                            print("Depth too high")

                        self.f_manager.setState(module, 'Complete')
                        return

                    if progress == 'Verifying usage':
                        depth+=1
                        if depth < self.max_depth:

                            print('Returned to verifying usages')
                            currentUsage = mod[3]
                            print('Current usage: {}' .format(currentUsage))

                            self.verifyUsages(module, depth, current = currentUsage)

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