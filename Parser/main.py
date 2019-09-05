import MVNparser
import csv
import save
import os

def parser(root_link,max_depth,depth, target_version = None):

    root_html = MVNparser.getSoup(root_link)

    module_link = root_link[root_link.find('/artifact'):][10:]
    #module_name = module_link[module_link.find('/'):][1:]

    if not target_version:
        version = MVNparser.getVersion(root_html)
    else:
        target_version = target_version[target_version.find(module_link):]
        version = target_version[target_version.find('/'):][1:]

    version = version[version.find('/'):]
    print(version)

    module = module_link+version
    print("Current module:", module)

    nodes = save.getAllProgress()

    if module not in nodes:

        save.initialize(module,depth) #Status Initialized !! MUDAR !!!

        try:
            module_html = MVNparser.getSoup(root_link+version)
            dependencies = MVNparser.getDependencies(module, module_html) #status getting dependencies
            print('There are {} dependencies in the module {}' .format(len(dependencies), module))
        except Exception as e:
            print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module))
            save.setState(module, 'Error')
            return

        save.addModule(module)
        for dependency in dependencies:
            save.addModule(dependency[2])
        save.addLinks(module, dependencies)
        print('Updated nodes ans links')
        save.setState(module, 'Done Dependencies')

        depth+=1
        if depth < max_depth:

            usages_link = root_link+version+'/usages'
            usages_html = MVNparser.getSoup(usages_link)
            usages = MVNparser.getUsages(module, usages_link, usages_html) #status getting usages

            print('There are {} usages in the module {}' .format(len(usages), module))
            #if len(usages) >= 50: usages = usages[:50]

            for dependency in dependencies: #status verifying dependency
                print('Opening', dependency[1])
                save.setCurrent(module, 'd', dependency[2])
                parser("https://mvnrepository.com/artifact/"+dependency[1],max_depth,depth,target_version = dependency[2])
                print('Returned to', module)
                if dependency[2] == "com.raybritton.inspector/inspector_lib/1.2.0":
                    exit()

            for usage in usages: #status verifying usage
                print('Opening', usage)
                save.setCurrent(module, 'u', usage)
                parser("https://mvnrepository.com/artifact/"+usage,max_depth,depth)
                print('Returned to', module)
                if usage == "com.raybritton.inspector/inspector_lib":
                    exit()

        else:
            print("Depth too high")

        save.setState(module, 'Complete')
        return

    elif module in nodes:

        mod = save.getProgress(module)
        progress = mod[2]
        depth = int(mod[0])
        status = mod[4]

        if progress != 'Complete' and progress != 'Error':
            if status == 'closed':

                save.switchStatus(module)

                if progress == 'Getting dependencies' or progress == 'Initialized':
                    print('Returned to get dependencies')

                    module_html = MVNparser.getSoup(root_link+version)
                    dependencies = MVNparser.getDependencies(module, module_html) #status getting dependencies

                    print('There are {} dependencies in the module {}' .format(len(dependencies), module))

                    save.addModule(module)
                    for dependency in dependencies:
                        save.addModule(dependency[2])
                    save.addLinks(module, dependencies)
                    print('Updated nodes ans links')
                    save.setState(module, 'Done dependencies')

                    depth+=1
                    if depth < max_depth:

                        usages_link = root_link+version+'/usages'
                        usages_html = MVNparser.getSoup(usages_link)
                        usages = MVNparser.getUsages(module, usages_link, usages_html) #status getting usages

                        print('There are {} usages in the module {}' .format(len(usages), module))
                        #if len(usages) >= 50: usages = usages[:50]

                        for dependency in dependencies: #status verifying dependency
                            print('Opening', dependency[1])
                            save.setCurrent(module, 'd', dependency[2])
                            parser("https://mvnrepository.com/artifact/"+dependency[1],max_depth,depth,target_version = dependency[2])
                            print('Returned to', module)

                        for usage in usages: #status verifying usage
                            print('Opening', usage)
                            save.setCurrent(module, 'u', usage)
                            parser("https://mvnrepository.com/artifact"+usage,max_depth,depth)
                            print('Returned to', module)

                    else:
                        print("Depth too high")

                    save.setState(module, 'Complete')
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
                        usages_html = MVNparser.getSoup(usages_link)
                        usages = MVNparser.getUsages(module, usages_link, usages_html, page=currentPage) #status getting usages

                        print('There are {} usages in the module {}' .format(len(usages), module))
                        #if len(usages) >= 50: usages = usages[:50]

                        dependencies = save.getDependencies(module)

                        for dependency in dependencies: #status verifying dependency
                            print('Opening', dependency[0])
                            save.setCurrent(module, 'd', dependency[1])
                            parser("https://mvnrepository.com/artifact/"+dependency[0],max_depth,depth,target_version = dependency[1])
                            print('Returned to', module)

                        usages = save.getUsages(module)

                        for usage in usages: #status verifying usage
                            usage = usage[0]
                            print('Opening', usage)
                            save.setCurrent(module, 'u', usage)
                            parser("https://mvnrepository.com/artifact/"+usage,max_depth,depth)
                            print('Returned to', module)

                    else:
                        print("Depth too high")

                    save.setState(module, 'Complete')
                    return

                if progress == 'Verifying dependency' or progress == 'Done usages':
                    depth+=1
                    if depth < max_depth:

                        print('Returned to verifying dependencies')
                        currentDependency = mod[3]
                        print('Current dependency: {}' .format(currentDependency))

                        dependencies = save.getDependencies(module)
                        for dep in dependencies:
                            if dep[1] == currentDependency:
                                currentIndex = dependencies.index(dep)
                                break
                        remainingDependencies = dependencies[currentIndex:]

                        for dependency in remainingDependencies: #status verifying dependencies
                            print('Opening', dependency[0])
                            save.setCurrent(module, 'd', dependency[1])
                            parser("https://mvnrepository.com/artifact/"+dependency[0],max_depth,depth,target_version = dependency[1])
                            print('Returned to', module)

                        usages = save.getUsages(module)

                        for usage in usages: #status verifying usage
                            usage = usage[0]
                            print('Opening', usage)
                            save.setCurrent(module, 'u', usage)
                            parser("https://mvnrepository.com/artifact/"+usage,max_depth,depth)
                            print('Returned to', module)

                    else:
                        print("Depth too high")

                    save.setState(module, 'Complete')
                    return

                if progress == 'Verifying usage':
                    depth+=1
                    if depth < max_depth:

                        print('Returned to verifying usages')
                        currentUsage = mod[3]
                        print('Current usage: {}' .format(currentUsage))

                        usages = save.getUsages(module)
                        currentIndex = usages.index([currentUsage])
                        remainingUsages = usages[currentIndex:]

                        for usage in remainingUsages: #status verifying usage
                            usage = usage[0]

                            print('Opening', usage)
                            save.setCurrent(module, 'u', usage)
                            parser("https://mvnrepository.com/artifact/"+usage,max_depth,depth)
                            print('Returned to', module)

                    else:
                        print("Depth too high")

                    save.setState(module, 'Complete')
                    return

            else:
                print(module, ' already open')

        else:
            print(module,'Already Veryfied')


            """
            usages = []

            lastPage = save.getLastPage()
            existentUsages = save.getUsages(module_link)
            usage = existentUsages

            usages_link = root_link+version+'/usages'
            usages_html = MVNparser.getSoup(usages_link)

            newUsages = MVNparser.getUsages(module_link, usages_link, usages_html, page=lastPage)

            for usage in newUsages:
                if usage not in existentUsages:
                    usages.append(usage)
            """
try:
    save.defaultStatus()
    print('All status to closed')
except:
    print('First Run')
    os.mkdir('files')
    os.mkdir('files/modules')

root = "https://mvnrepository.com/artifact/org.apache.jclouds/jclouds-compute"
parser(root,3,0)
