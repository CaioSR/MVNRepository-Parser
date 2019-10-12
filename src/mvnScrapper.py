from urllib.request import urlopen #biblioteca para abrir e ler um url
from html.parser import HTMLParser
# from bs4 import BeautifulSoup #biblioteca para realizar o parse
import time
from fileManager import FileManager

class MyHTMLParser(HTMLParser):
    links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for inAttr in attrs:
                if inAttr[0] == 'href':
                    self.links.append(inAttr[1])

class MVNscrapper():

    parser = MyHTMLParser()

    def __init__(self, project, max_depth, f_dir, p_dir):
        p = self.separateV(project, getModule = True)
        self.project = p[0]
        self.version = p[1]
        self.max_depth = max_depth
        self.f_manager = FileManager(f_dir, p_dir, self.project[2])
        self.scrap(self.project, self.max_depth, 0, target_version = self.version)
        

    def getHtml(self, link):
        self.parser.links.clear()
        page = urlopen(link)
        time.sleep(2)
        html = page.read()
        page.close()
        html = html.decode('utf-8')
        self.parser.feed(html)

        return self.parser.links

    def separateV(self, project, getModule = False):
        aux1 = project[project.find('/artifact'):][10:] #return project/module/version
        aux2 = aux1[aux1.find('/'):][1:] #return module/version
        version = aux2[aux2.find('/'):] #return /version
        root = project[:project.find(version)]

        if getModule:
            return [root, version, aux1]
        else:
            return [root, version]
       

    def fetchVersions(self, html):

        versions = []
        for link in html:
            if 'repos/' in link:
                versions.append(previous)

            previous = link

        del html
        return versions

    def searchDependency(self, link, dependency):
        html = self.getHtml(link)

        for link in html:
            if link[10:] == dependency:
                del html
                return True
        del html
        return False

    #essa função verifica se o atual link é de uma versão ou não
    def isVersion(self, href):
        #return re.compile(r"[+-]?\d+(?:\.\d+)?").search(href) #procura por números no link
        if href.count('/') == 4:
            return True
        else:
            return False

    def fetchDependencies(self, module, link):
        html = self.getHtml(link)

        self.f_manager.setState(module, 'Getting dependencies')

        dependency = [] #lista para salvar vários links de uma mesma dependencia (página principal, de versão específica, etc
        dependencies = [] #lista com todas as listas de dependencias
        scope = 0 #variavel para definir o inicio da leitura das dependencias
        previous = 'non-version' #armazena se o link anterior foi de uma versão de uma dependencia
        count = 0
        for link in html: #procura por tags 'a'

            if scope == 1:
                if 'artifact' in link:
                    #verifica se o link anterior foi uma versão
                    if previous == 'version':
                        #verifica se o atual link é de uma versão
                        if self.isVersion(link):
                            #acrescenta o link na lista da dependência
                            dependency.append(link[10:])
                            #acrescenta a lista da dependência na lista de dependências
                            if dependency not in dependencies:
                                dependencies.append(dependency)


                                self.f_manager.setDependency(module, dependency)

                            #zera a lista da dependência
                            dependency = []
                            count=0

                        else:
                            #verifica se a lista não está vazia.
                            #(Sempre que o link passa nos dois ifs anteriores, ao chegar nesse
                            #a lista ainda estará vazia. Caso ela esteja vazia, ele não poderá
                            #passar por aqui.
                            if dependency != []:
                                #acrescenta a lista da dependência na lista de dependências
                                if dependency not in dependencies:
                                    dependencies.append(dependency)


                                    self.f_manager.setDependency(module, dependency)
                                #zera a lista da dependência
                                dependency = []
                                count=0
                                #acrescenta o link na lista da dependência
                                dependency.append(link[10:])
                            else:
                                dependency.append(link[10:])
                    else:
                        #acrescenta o link na lista da dependência
                        dependency.append(link[10:])

                    #se o link for uma versão, define previous como version
                    if self.isVersion(link): previous = 'version'
                    #senão define como non-version
                    else:
                        count += 1
                        if count == 3:
                            if len(dependency) == 3:
                                dependency = [dependency[2]] #não salva dependencia sem versão
                            else:
                                dependency = []
                            count = 1
                        previous = 'non-version'

                else:
                    if 'twitter' in link:
                        if dependency not in dependencies and dependency != []:
                            if len(dependency) > 2:
                                dependencies.append(dependency)

                                self.f_manager.setDependency(module, dependency)

                        scope = 0
                        break


            #se o link lido conter #buildr o escopo é ativado pois
            #ele é o último link antes das dependências
            if '#buildr' in link:
                scope = 1

        del html
        return dependencies

    def fetchUsages(self, module, root_usages, page=None):
        html = self.getHtml(root_usages)

        aux = module[module.find('/'):][1:]
        version = aux[aux.find('/'):][1:]
        module_link = module[:module.find(version)-1]

        self.f_manager.setState(module, 'Getting usages')
        if not page:
            print('Page 1')

        usages = []
        previous = ''
        scope = 0
        next_page = 0
        current_page = 0
        end = 0

        while not end:

            for link in html:

                if page:
                    usages_page_link = root_usages + '?p=' + page
                    print("Continued on page " + page)
                    soup = self.getHtml(usages_page_link)
                    current_page = int(page)
                    self.f_manager.setCurrentPage(module, page)
                    page = None

                if scope == 1:

                    if 'artifact' in link:
                        if link == previous:
                            if link not in usages:
                                usages.append(link[10:])
                                self.f_manager.setUsage(module,link[10:])

                        previous = link

                    elif '?p=' in link:
                        next_page = int(link[3:])

                        if next_page > current_page:
                            scope = 0
                            usages_page_link = root_usages + link
                            soup = self.getHtml(usages_page_link)
                            current_page = int(link[3:])
                            print('Page',current_page)
                            self.f_manager.setCurrentPage(module, current_page)
                            break

                    elif '/tags' in link:
                        end = 1
                        scope = 0

                        break

                if module_link in link:
                    scope = 1

        self.f_manager.setState(module, 'Done usages')
        del html
        return usages

    def getUsageVersion(self, root_link, target_version, lookForDependency):
        root_html = self.getHtml(root_link)
        module_root = root_link[root_link.find('/artifact'):][10:]

        version = None
        versions = self.fetchVersions(root_html)
        del root_html
        for vers in versions:

            vers = vers[vers.find('/'):]
            print("Currently on {}" .format(vers))
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
                    dep_root, dep_version = self.separateV(dep_link)
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
                        dep_root, dep_version = self.separateV(dep_link)
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
        
        self.f_manager.copyToFinal()

       