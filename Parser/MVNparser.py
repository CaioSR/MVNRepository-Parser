from urllib.request import urlopen #biblioteca para abrir e ler um url
from bs4 import BeautifulSoup #biblioteca para realizar o parse
import re #biblioteca para processar expressões regulares
import time
import json
import save

def getSoup(link):
    page = urlopen(link)
    time.sleep(2)
    html = page.read()

    soup = BeautifulSoup(html,'html.parser')

    return soup

def getVersions(soup):

    versions = []

    for link in soup.find_all('a'):
        if 'repos/' in link.get('href'):
            versions.append(previous)

        previous = link.get('href')

    return versions

def searchDependency(module, dependency):
    link = "https://mvnrepository.com/artifact/"+module
    soup = getSoup(link)
    for link in soup.find_all('a'):
        if link.get('href')[10:] == dependency:
            return True
    return False

#essa função verifica se o atual link é de uma versão ou não
def isVersion(href):
    #return re.compile(r"[+-]?\d+(?:\.\d+)?").search(href) #procura por números no link
    if href.count('/') == 4:
        return True
    else:
        return False

def getDependencies(module, soup):

    save.setState(module, 'Getting dependencies')

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
                    if isVersion(link.get('href')):
                        #acrescenta o link na lista da dependência
                        dependency.append(link.get('href')[10:])
                        #acrescenta a lista da dependência na lista de dependências
                        if dependency not in dependencies:
                            dependencies.append(dependency)

                            save.setDependency(module, dependency)

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

                                save.setDependency(module, dependency)
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
                if isVersion(link.get('href')): previous = 'version'
                #senão define como non-version
                else: previous = 'non-version'

            else:
                if 'twitter' in link.get('href'):
                    if dependency not in dependencies and dependency != []:
                        dependencies.append(dependency)

                        save.setDependency(module, dependency)

                    scope = 0
                    break

        #se o link lido conter #buildr o escopo é ativado pois
        #ele é o último link antes das dependências
        if '#buildr' in link.get('href'):
            scope = 1

    return dependencies

def getUsages(module, root_usages, soup, page=None):

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

        for link in soup.find_all('a'):

            if page:
                usages_page_link = root_usages + '?p=' + page
                print("Continued on page " + page)
                soup = getSoup(usages_page_link)
                current_page = int(page)
                save.setCurrentPage(module, page)
                page = None

            if scope == 1:

                if 'artifact' in link.get('href'):
                    if link.get('href') == previous:
                        if link.get('href') not in usages:
                            usages.append(link.get('href')[10:])
                            save.setUsage(module,link.get('href')[10:])

                    previous = link.get('href')

                elif '?p=' in link.get('href'):
                    next_page = int(link.get('href')[3:])

                    if next_page > current_page:
                        scope = 0
                        usages_page_link = root_usages + link.get('href')
                        soup = getSoup(usages_page_link)
                        current_page = int(link.get('href')[3:])
                        print('Page',current_page)
                        save.setCurrentPage(module, current_page)
                        break

                elif '/tags' in link.get('href'):
                    end = 1
                    scope = 0

                    break

            if module_link in link.get('href'):
                scope = 1

    save.setState(module, 'Done usages')
    return usages
