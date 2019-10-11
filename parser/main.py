import MVNparser
import csv
import save
import os

#root = "https://mvnrepository.com/artifact/org.springframework.security/spring-security-web"
#version = "/5.1.6.RELEASE"
root = "https://mvnrepository.com/artifact/org.apache.shiro/shiro-web"
version = "/1.4.1"
max_depth = 3

MVNp = MVNparser.MVNrepo()

def verifyFiles():
    try:
        save.defaultStatus()
        print('All status to closed')
    except:
        print('First Run')
        os.mkdir('files')
        os.mkdir('files/modules')

def getUsageVersion(MVNp, root_link, target_version, lookForDependency):
    root_html = MVNp.getHtml(root_link)
    module_root = root_link[root_link.find('/artifact'):][10:]

    version = None
    versions = MVNp.getVersions(root_html)
    del root_html
    for vers in versions:

        vers = vers[vers.find('/'):]
        print("Currently on {}" .format(vers))
        module = module_root + vers
        result = MVNp.searchDependency("https://mvnrepository.com/artifact/"+module, lookForDependency)

        if result:
            print("Correct version is {}" .format(vers))
            return vers

    return None

def saveDependencies(module, dependencies):
        save.addModule(module)
        for dependency in dependencies:
            save.addModule(dependency[2])
        save.addLinks(module, dependencies)
        save.setState(module, 'Done Dependencies')

        print('Updated nodes ans links')

def getDependencies(MVNp, module, link):
    dependencies = MVNp.getDependencies(module, link)

    if len(dependencies) == 0:
        save.setDependency(module, 'None')

    print('There are {} dependencies in the module {}' .format(len(dependencies), module))

    saveDependencies(module, dependencies)

def getUsages(MVNp, module, link, page = None):

    usages = MVNp.getUsages(module, link)

    if len(usages) == 0:
        save.setUsage(module, 'None')

    print('There are {} usages in the module {}' .format(len(usages), module))

def verifyDependencies(MVNp, module, max_depth, depth, current = None):

    if not current:
        for dependency in save.getDependencies(module):
            if dependency != 'None':
                print('Opening dependency:', dependency)
                save.setCurrent(module, 'd', dependency)
                dep_link = 'https://mvnrepository.com/artifact/' + dependency
                dep_root, dep_version = MVNp.separateV(dep_link)
                parser(MVNp, dep_root,max_depth,depth,target_version = dep_version)
                print('Returned to', module)
    else:
        toDo = False
        for dependency in save.getDependencies(module):
            if dependency != 'None':
                if dependency == current:
                    toDo = True
                if toDo:
                    print('Opening dependency:', dependency)
                    save.setCurrent(module, 'd', dependency)
                    dep_link = 'https://mvnrepository.com/artifact/' + dependency
                    dep_root, dep_version = MVNp.separateV(dep_link)
                    parser(MVNp,dep_root,max_depth,depth,target_version = dep_version)
                    print('Returned to', module)


def verifyUsages(MVNp, module, max_depth, depth, current = None):

    if not current:
        for usage in save.getUsages(module):
            if usage != 'None':
                print('Opening usage:', usage)
                save.setCurrent(module, 'u', usage)
                parser(MVNp,'https://mvnrepository.com/artifact/' + usage,max_depth,depth,lookForDependency = module)
                print('Returned to', module)
    else:
        toDo = False
        for usage in save.getUsages(module):
            if usage != 'None':
                if usage == current:
                    toDo = True
                if toDo:
                    print('Opening usage:', usage)
                    save.setCurrent(module, 'u', usage)
                    parser(MVNp, 'https://mvnrepository.com/artifact/' + usage,max_depth,depth,lookForDependency = module)
                    print('Returned to', module)

def parser(MVNp, root_link,max_depth,depth, target_version = None, lookForDependency = None):

    if target_version:
        version = target_version

    module_root = root_link[root_link.find('/artifact'):][10:]

    if not target_version:
        print("Looking for correct usage version")

        try:
            version = getUsageVersion(MVNp, root_link, target_version, lookForDependency)
        except Exception as e:
            save.initialize(module_root,depth)
            print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module_root))
            save.setState(module_root, 'Error')
            return

        if not version:
            return

    module = module_root+version
    print("Current module:", module)

    inProgress = save.checkProgress(module)

    if not inProgress:
        print('New module')

        save.initialize(module,depth) #Status Initialized !! MUDAR !!!

        try:
            getDependencies(MVNp, module, root_link+version)
        except Exception as e:
            print("---------ERRO--------\n",e,"\n---------------------\nSetting {} to Error Status" .format(module))
            save.setState(module, 'Error')
            return

        depth+=1
        if depth < max_depth:

            getUsages(MVNp, module,  root_link+version+'/usages')
            verifyDependencies(MVNp, module, max_depth, depth)
            verifyUsages(MVNp, module, max_depth, depth)

        else:
            print("Depth too high")

        save.setState(module, 'Complete')
        return

    elif inProgress:
        print('Module in progress')

        mod = save.getProgress(module)
        progress = mod[2]
        depth = int(mod[0])
        status = mod[4]

        if progress != 'Complete' and progress != 'Error':
            if status == 'closed':

                save.switchStatus(module)

                if progress == 'Getting dependencies' or progress == 'Initialized':
                    print('Returned to get dependencies')

                    getDependencies(MVNp, module, root_link+version)

                    depth+=1
                    if depth < max_depth:

                        getUsages(MVNp, module,  root_link+version+'/usages')
                        verifyDependencies(MVNp, module, max_depth, depth)
                        verifyUsages(MVNp, module, max_depth, depth)

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

                        getUsages(MVNp, module, root_link+version+'/usages', page = currentPage)
                        verifyDependencies(MVNp, module, max_depth, depth)
                        verifyUsages(MVNp, module, max_depth, depth)

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

                        verifyDependencies(MVNp, module, max_depth, depth, current = currentDependency)
                        verifyUsages(MVNp, module, max_depth, depth)

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

                        verifyUsages(MVNp, module, max_depth, depth, current = currentUsage)

                    else:
                        print("Depth too high")

                    save.setState(module, 'Complete')
                    return
            else:
                print(module, ' already open')
        else:
            print(module,'Already Veryfied')


verifyFiles()
parser(MVNp, root,max_depth,0,target_version=version)
input()
