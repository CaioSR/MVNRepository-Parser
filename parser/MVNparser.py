from urllib.request import urlopen #biblioteca para abrir e ler um url
from html.parser import HTMLParser
# from bs4 import BeautifulSoup #biblioteca para realizar o parse
import time
import save

class MyHTMLParser(HTMLParser):
    links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for inAttr in attrs:
                if inAttr[0] == 'href':
                    self.links.append(inAttr[1])
class MVNrepo():

    parser = MyHTMLParser()

    def getHtml(self, link):
        self.parser.links.clear()
        page = urlopen(link)
        time.sleep(2)
        html = page.read()
        page.close()
        html = html.decode('utf-8')
        self.parser.feed(html)

        return self.parser.links

    def separateV(self, project):
        aux1 = project[project.find('/artifact'):][10:] #return project/module/version
        aux2 = aux1[aux1.find('/'):][1:] #return module/version
        version = aux2[aux2.find('/'):] #return /version
        root = project[:project.find(version)]

        return [root, version]

    def getVersions(self, html):

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

    def getDependencies(self, module, link):
        html = self.getHtml(link)

        save.setState(module, 'Getting dependencies')

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


                                save.setDependency(module, dependency)

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


                                    save.setDependency(module, dependency)
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

                                save.setDependency(module, dependency)

                        scope = 0
                        break


            #se o link lido conter #buildr o escopo é ativado pois
            #ele é o último link antes das dependências
            if '#buildr' in link:
                scope = 1

        del html
        return dependencies

    def getUsages(self, module, root_usages, page=None):
        html = self.getHtml(root_usages)

        aux = module[module.find('/'):][1:]
        version = aux[aux.find('/'):][1:]
        module_link = module[:module.find(version)-1]

        save.setState(module, 'Getting usages')
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
                    save.setCurrentPage(module, page)
                    page = None

                if scope == 1:

                    if 'artifact' in link:
                        if link == previous:
                            if link not in usages:
                                usages.append(link[10:])
                                save.setUsage(module,link[10:])

                        previous = link

                    elif '?p=' in link:
                        next_page = int(link[3:])

                        if next_page > current_page:
                            scope = 0
                            usages_page_link = root_usages + link
                            soup = self.getHtml(usages_page_link)
                            current_page = int(link[3:])
                            print('Page',current_page)
                            save.setCurrentPage(module, current_page)
                            break

                    elif '/tags' in link:
                        end = 1
                        scope = 0

                        break

                if module_link in link:
                    scope = 1

        save.setState(module, 'Done usages')
        del html
        return usages
