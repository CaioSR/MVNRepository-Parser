import csv
import os

def addLinks(module, dependencies):

    modules = [module]
    for dependency in dependencies:
        modules.append(dependency[2][10:])

    with open('files/Links.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(modules)

    writeFile.close()

def addModule(module,depth):

    with open('files/Nodes.csv', 'a', newline='') as writeFile:
        writer  = csv.writer(writeFile)
        writer.writerow([module])

    writeFile.close()

    with open('files/Progress.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([depth,module,'Initialized','Null'])

    writeFile.close()

def setState(module, state):

    with open('files/Progress.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        modules = list(reader)

    readFile.close()

    for mod in modules:
        if mod[1] == module:
            mod[2] = state
            mod[3] = 'Null'

    with open('files/Progress.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(modules)

    writeFile.close()
"""
    if state == 'Complete':
        delFile(module)
"""
def setCurrentPage(module, page):

    with open('files/Progress.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        modules = list(reader)

    readFile.close()

    for mod in modules:
        if mod[1] == module:
            mod[3] = page

    with open('files/Progress.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(modules)

    writeFile.close()

def setCurrent(module, relation, current):

    with open('files/Progress.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        modules = list(reader)

    readFile.close()

    for mod in modules:
        if mod[1] == module:
            if relation == 'd':
                mod[2] = 'Verifying dependency'
            elif relation == 'u':
                mod[2] = 'Verifying usage'
            mod[3] = current

    with open('files/Progress.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(modules)

    writeFile.close()

def setUsage(module, usage):

    usage = usage[10:]

    file = module.replace('/','+')
    file = 'files/modules/['+file+']Usages.csv'

    with open(file, 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([usage])

    writeFile.close()

def setDependency(module, dependency):

    dependency = dependency[2][10:]

    file = module.replace('/','+')
    file = 'files/modules/['+file+']Dependencies.csv'

    with open(file, 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([dependency])

    writeFile.close()
"""
def delFile(module):

    module = module.replace('/','+')
    os.remove('['+module+']Dependencies.csv')
    try:
        os.remove('['+module+']Usages.csv')
    except:
        pass
"""
def checkUsages(module):
    pass

def getLastPage():
    pass

def getModules():

    with open('files/Nodes.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        nodes = list(reader)

    readFile.close()

    return nodes

def getDependencies():
    pass

def getUsages():
    pass
