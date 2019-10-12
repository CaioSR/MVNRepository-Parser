from urllib.request import urlopen #biblioteca para abrir e ler um url
from bs4 import BeautifulSoup #biblioteca para realizar o parse
import time
import save as sv
import os

class MVNrepo():

    def __init__(self, project, max_depth, f_dir, p_dir):
        p = self.separateV(project)
        self.project = p[0]
        self.version = p[1]
        self.max_depth = max_depth
        self.save = sv.Save(f_dir, p_dir, self.version)
        self.parser(self.project, self.max_depth, 0, target_version = self.version)
        self.save.copyToFinal()

    def getSoup(self, link):
        page = urlopen(link)
        time.sleep(2)
        html = page.read()

        soup = BeautifulSoup(html,'html.parser')

        return soup

    def separateV(self, project):
        aux1 = project[project.find('/artifact'):][10:] #return project/module/version
        aux2 = aux1[aux1.find('/'):][1:] #return module/version
        version = aux2[aux2.find('/'):] #return version
        root = project[:project.find(version)]

        return [root, aux1]

    def getVersions(self, soup):
        versions = []

        for link in soup.find_all('a'):
            if 'repos/' in link.get('href'):
                versions.append(previous)

            previous = link.get('href')

        return versions

    def searchDependency(self, module, dependency):
        link = "https://mvnrepository.com/artifact/"+module
        soup = self.getSoup(link)
        for link in soup.find_all('a'):
            if link.get('href')[10:] == dependency:
                return True
        return False

    #essa função verifica se o atual link é de uma versão ou não
    def isVersion(self, href):
        #return re.compile(r"[+-]?\d+(?:\.\d+)?").search(href) #procura por números no link
        if href.count('/') == 4:
            return True
        else:
            return False

    def getDependencies(self, module, soup):

        self.save.setState(module, 'Getting dependencies')

        dependency = [] #lista para salvar vários links de uma mesma dependencia (página principal, de versão específica, etc
        dependencies = [] #lista com todas as listas de dependencias
        scope = 0 #variavel para definir o inicio da leitura das dependencias
        previous = 'non-version' #armazena se o link anterior foi de uma versão de uma dependencia
        for link in soup.find_all('a'): #procura por tags 'a'

            if scope == 1:
                if 'artifact' in link.get('href'):
                    #verifica se o link anterior foi uma versão
                    if previous == 'version':
                        #verifica se o atual link é de uma versão
                        if self.isVersion(link.get('href')):
                            #acrescenta o link na lista da dependência
                            dependency.append(link.get('href')[10:])
                            #acrescenta a lista da dependência na lista de dependências
                            if dependency not in dependencies:
                                dependencies.append(dependency)

                                self.save.setDependency(module, dependency)

                            #zera a lista da dependência
                            dependency = []

                        else:
                            #verifica se a lista não está vazia.
                            #(Sempre que o link passa nos dois ifs anteriores, ao chegar nesse
                            #a lista ainda estará vazia. Caso ela esteja vazia, ele não poderá
                            #passar por aqui.
                            if dependency != []:
                                #acrescenta a lista da dependência na lista de dependências
                                if dependency not in dependencies:
                                    dependencies.append(dependency)

                                    self.save.setDependency(module, dependency)
                                #zera a lista da dependência
                                dependency = []
                                #acrescenta o link na lista da dependência
                                dependency.append(link.get('href')[10:])
                            else:
                                dependency.append(link.get('href')[10:])
                    else:
                        #acrescenta o link na lista da dependência
                        dependency.append(link.get('href')[10:])

                    #se o link for uma versão, define previous como version
                    if self.isVersion(link.get('href')): previous = 'version'
                    #senão define como non-version
                    else: previous = 'non-version'

                else:
                    if 'twitter' in link.get('href'):
                        if dependency not in dependencies and dependency != []:
                            dependencies.append(dependency)

                            self.save.setDependency(module, dependency)

                        scope = 0
                        break

            #se o link lido conter #buildr o escopo é ativado pois
            #ele é o último link antes das dependências
            if '#buildr' in link.get('href'):
                scope = 1

        return dependencies

    def getUsages(self, module, root_usages, soup, page=None):

        aux = module[module.find('/'):][1:]
        version = aux[aux.find('/'):][1:]
        module_link = module[:module.find(version)-1]

        self.save.setState(module, 'Getting usages')
        if not page:
            print('Page 1')

        usages = []
        previous = ''
        scope = 0
        next_page = 0
        current_page = 0
        end = 0

        while not end:

            for link in soup.find_all('a'):

                if page:
                    usages_page_link = root_usages + '?p=' + page
                    print("Continued on page " + page)
                    soup = self.getSoup(usages_page_link)
                    current_page = int(page)
                    self.save.setCurrentPage(module, page)
                    page = None

                if scope == 1:

                    if 'artifact' in link.get('href'):
                        if link.get('href') == previous:
                            if link.get('href') not in usages:
                                usages.append(link.get('href')[10:])
                                self.save.setUsage(module,link.get('href')[10:])

                        previous = link.get('href')

                    elif '?p=' in link.get('href'):
                        next_page = int(link.get('href')[3:])

                        if next_page > current_page:
                            scope = 0
                            usages_page_link = root_usages + link.get('href')
                            soup = self.getSoup(usages_page_link)
                            current_page = int(link.get('href')[3:])
                            print('Page',current_page)
                            self.save.setCurrentPage(module, current_page)
                            break

                    elif '/tags' in link.get('href'):
                        end = 1
                        scope = 0

                        break

                if module_link in link.get('href'):
                    scope = 1

        self.save.setState(module, 'Done usages')
        return usages

    def parser(self, root_link, max_depth, depth, target_version = None, lookForDependency = None):

        root_html = self.getSoup(root_link)
        module_root = root_link[root_link.find('/artifact'):][10:]

        if not target_version:
            print("Looking for correct usage version")

            try:
                version = None
                versions = self.getVersions(root_html)
                for v in versions:
                    v = v[v.find('/'):]
                    print("Currently on {}" .format(v))
                    module = module_root + v
                    result = self.searchDependency(module, lookForDependency)
                    if result:
                        print("Correct version is {}" .format(v))
                        version = v
                        break
                if not version:
                    return

            except Exception as e:
                self.save.initialize(module_root,depth)
                print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module_root))
                self.save.setState(module_root, 'Error')
                return

        else:
            version = target_version[target_version.find('/'):][1:]
            version = version[version.find('/'):]

        print(version)

        module = module_root+version
        print("Current module:", module)

        nodes = self.save.getAllProgress()

        if module not in nodes:

            self.save.initialize(module,depth) #Status Initialized !! MUDAR !!!

            try:
                module_html = self.getSoup(root_link+version)
                dependencies = self.getDependencies(module, module_html) #status getting dependencies
                print('There are {} dependencies in the module {}' .format(len(dependencies), module))
            except Exception as e:
                print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module))
                self.save.setState(module, 'Error')
                return

            self.save.addModule(module)
            for dependency in dependencies:
                self.save.addModule(dependency[2])
            self.save.addLinks(module, dependencies)
            print('Updated nodes ans links')
            self.save.setState(module, 'Done Dependencies')

            depth+=1
            if depth < max_depth:

                usages_link = root_link+version+'/usages'
                usages_html = self.getSoup(usages_link)
                usages = self.getUsages(module, usages_link, usages_html) #status getting usages

                print('There are {} usages in the module {}' .format(len(usages), module))
                #if len(usages) >= 50: usages = usages[:50]

                for dependency in dependencies: #status verifying dependency
                    print('Opening', dependency[1])
                    self.save.setCurrent(module, 'd', dependency[2])
                    self.parser("https://mvnrepository.com/artifact/"+dependency[1],max_depth,depth,target_version = dependency[2])
                    print('Returned to', module)

                for usage in usages: #status verifying usage
                    print('Opening', usage)
                    self.save.setCurrent(module, 'u', usage)
                    self.parser("https://mvnrepository.com/artifact/"+usage,max_depth,depth,lookForDependency = module)
                    print('Returned to', module)

            else:
                print("Depth too high")

            self.save.setState(module, 'Complete')
            return

        elif module in nodes:

            mod = self.save.getProgress(module)
            progress = mod[2]
            depth = int(mod[0])
            status = mod[4]

            if progress != 'Complete' and progress != 'Error':
                if status == 'closed':

                    self.save.switchStatus(module)

                    if progress == 'Getting dependencies' or progress == 'Initialized':
                        print('Returned to get dependencies')

                        module_html = self.getSoup(root_link+version)
                        dependencies = self.getDependencies(module, module_html) #status getting dependencies

                        print('There are {} dependencies in the module {}' .format(len(dependencies), module))

                        self.save.addModule(module)
                        for dependency in dependencies:
                            self.save.addModule(dependency[2])
                        self.save.addLinks(module, dependencies)
                        print('Updated nodes ans links')
                        self.save.setState(module, 'Done dependencies')

                        depth+=1
                        if depth < max_depth:

                            usages_link = root_link+version+'/usages'
                            usages_html = self.getSoup(usages_link)
                            usages = self.getUsages(module, usages_link, usages_html) #status getting usages

                            print('There are {} usages in the module {}' .format(len(usages), module))
                            #if len(usages) >= 50: usages = usages[:50]

                            for dependency in dependencies: #status verifying dependency
                                print('Opening', dependency[1])
                                self.save.setCurrent(module, 'd', dependency[2])
                                self.parser("https://mvnrepository.com/artifact/"+dependency[1],max_depth,depth,target_version = dependency[2])
                                print('Returned to', module)

                            for usage in usages: #status verifying usage
                                print('Opening', usage)
                                self.save.setCurrent(module, 'u', usage)
                                self.parser("https://mvnrepository.com/artifact"+usage,max_depth,depth,lookForDependency = module)
                                print('Returned to', module)

                        else:
                            print("Depth too high")

                        self.save.setState(module, 'Complete')
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

                            usages_link = root_link+version+'/usages'
                            usages_html = self.getSoup(usages_link)
                            usages = self.getUsages(module, usages_link, usages_html, page=currentPage) #status getting usages

                            print('There are {} usages in the module {}' .format(len(usages), module))
                            #if len(usages) >= 50: usages = usages[:50]

                            dependencies = self.save.getDependencies(module)

                            for dependency in dependencies: #status verifying dependency
                                print('Opening', dependency[0])
                                self.save.setCurrent(module, 'd', dependency[1])
                                self.parser("https://mvnrepository.com/artifact/"+dependency[0],max_depth,depth,target_version = dependency[1])
                                print('Returned to', module)

                            usages = self.save.getUsages(module)

                            for usage in usages: #status verifying usage
                                usage = usage[0]
                                print('Opening', usage)
                                self.save.setCurrent(module, 'u', usage)
                                self.parser("https://mvnrepository.com/artifact/"+usage,max_depth,depth,lookForDependency = module)
                                print('Returned to', module)

                        else:
                            print("Depth too high")

                        self.save.setState(module, 'Complete')
                        return

                    if progress == 'Verifying dependency' or progress == 'Done usages':
                        depth+=1
                        if depth < max_depth:

                            print('Returned to verifying dependencies')
                            currentDependency = mod[3]
                            print('Current dependency: {}' .format(currentDependency))

                            dependencies = self.save.getDependencies(module)
                            for dep in dependencies:
                                if dep[1] == currentDependency:
                                    currentIndex = dependencies.index(dep)
                                    break
                            remainingDependencies = dependencies[currentIndex:]

                            for dependency in remainingDependencies: #status verifying dependencies
                                print('Opening', dependency[0])
                                self.save.setCurrent(module, 'd', dependency[1])
                                self.parser("https://mvnrepository.com/artifact/"+dependency[0],max_depth,depth,target_version = dependency[1])
                                print('Returned to', module)

                            usages = self.save.getUsages(module)

                            for usage in usages: #status verifying usage
                                usage = usage[0]
                                print('Opening', usage)
                                self.save.setCurrent(module, 'u', usage)
                                self.parser("https://mvnrepository.com/artifact/"+usage,max_depth,depth,lookForDependency = module)
                                print('Returned to', module)

                        else:
                            print("Depth too high")

                        self.save.setState(module, 'Complete')
                        return

                    if progress == 'Verifying usage':
                        depth+=1
                        if depth < max_depth:

                            print('Returned to verifying usages')
                            currentUsage = mod[3]
                            print('Current usage: {}' .format(currentUsage))

                            usages = self.save.getUsages(module)
                            currentIndex = usages.index([currentUsage])
                            remainingUsages = usages[currentIndex:]

                            for usage in remainingUsages: #status verifying usage
                                usage = usage[0]

                                print('Opening', usage)
                                self.save.setCurrent(module, 'u', usage)
                                self.parser("https://mvnrepository.com/artifact/"+usage,max_depth,depth,lookForDependency = module)
                                print('Returned to', module)

                        else:
                            print("Depth too high")

                        self.save.setState(module, 'Complete')
                        return

                else:
                    print(module, ' already open')

            else:
                print(module,'Already Veryfied')
