import MVNparser
import csv
import save
import os

def parser(root_link,max_depth,depth, target_version = None):

    soup = MVNparser.getSoup(root_link)

    module_link = root_link[root_link.find('/artifact'):][10:]
    module_name = module_link[module_link.find('/'):][1:]

    if not target_version:
        version = MVNparser.getVersion(soup)
    else:
        target_version = target_version[target_version.find(module_link):]
        version = target_version[target_version.find('/'):][1:]

    version = version[version.find('/'):]
    print(version)

    module = module_link+version
    print("Current module: ", module)

    try:
        nodes = save.getModules()
    except:
        nodes = []

    if [module] not in nodes:

        save.addModule(module,depth)

        soup_version = MVNparser.getSoup(root_link+version)
        dependencies_full = MVNparser.getDependencies(module, soup_version)
        dependencies_names = []

        for dependency in dependencies_full:
            try:
                dependencies_names.append(dependency[1][10:])
            except:
                dependencies_full.remove(dependency)

        print('There are {} dependencies in the module {}' .format(len(dependencies_full), module))

        save.addLinks(module, dependencies_full)

        depth+=1
        if depth < max_depth:

            usages_link = root_link+version+'/usages'
            usages_soup = MVNparser.getSoup(usages_link)
            usages = MVNparser.getUsages(module, usages_link, usages_soup)

            print('There are {} usages in the module {}' .format(len(usages),module_link))
            if len(usages) >= 50: usages = usages[:50]

            for dependency in dependencies_full:
                print('Opening', dependency[1])
                save.setCurrent(module, 'd', dependency[2][10:])
                try:
                    parser("https://mvnrepository.com"+dependency[1],max_depth,depth,target_version = dependency[2])
                except Exception as e:
                    print("---------ERRO--------\n",e,"\n---------------------")
                    save.setState(module, 'Error')
                print('Returned to', module)

            for usage in usages:
                print('Opening', usage)
                save.setCurrent(module, 'u', usage[10:])
                try:
                    parser("https://mvnrepository.com"+usage,max_depth,depth)
                except Exception as e:
                    print("---------ERRO--------\n",e,"\n---------------------")
                    save.setState(module, 'Error')
                print('Returned to', module)

            save.setState(module, 'Complete')

        else:
            print("Depth too high")
            save.setState(module, 'Complete')
            return

    elif [module] in nodes:

        progress = save.getProgress(module)

        if progress != 'Complete' and progress != 'Error':
            if progress == 'Getting Dependencies':
                pass
            if progress == 'Getting Usages':
                pass
            if progress == 'Verifying Dependency':
                pass
            if progress == 'Verifying Usage':
                pass
        else:
            print(module,'Already Veryfied')


            """
            usages = []

            lastPage = save.getLastPage()
            existentUsages = save.getUsages(module_link)
            usage = existentUsages

            usages_link = root_link+version+'/usages'
            usages_soup = MVNparser.getSoup(usages_link)

            newUsages = MVNparser.getUsages(module_link, usages_link, usages_soup, page=lastPage)

            for usage in newUsages:
                if usage not in existentUsages:
                    usages.append(usage)
            """


root = "https://mvnrepository.com/artifact/org.apache.jclouds/jclouds-compute"

parser(root,3,0)
