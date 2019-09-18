import csv
import os

def addLinks(module, dependencies):

    modules = [module]
    for dependency in dependencies:
        modules.append(dependency[2])

    with open('files/Links.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(modules)

    writeFile.close()

def addModule(module):

    try:
        with open('files/Nodes.csv', 'r', newline='') as readFile:
            reader = csv.reader(readFile)
            nodes = list(reader)

        readFile.close()

        if [module] not in nodes:
            with open('files/Nodes.csv', 'a', newline='') as writeFile:
                writer  = csv.writer(writeFile)
                writer.writerow([module])

            writeFile.close()
    except:

        with open('files/Nodes.csv', 'w', newline='') as writeFile:
            writer  = csv.writer(writeFile)
            writer.writerow([module])

        writeFile.close()


def initialize(module,depth):

    with open('files/Progress.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([depth,module,'Initialized','Null','open'])

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

    file = module.replace('/','+')
    file = 'files/modules/['+file+']Usages.csv'

    try:
        with open(file, 'r') as readFile:
            reader = csv.reader(readFile)
            us = list(reader)

        readFile.close()

        if [usage] not in us:
            with open(file, 'a', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow([usage])

            writeFile.close()

    except:
        with open(file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([usage])

        writeFile.close()

def setDependency(module, dependency):

    dependency = [dependency[1],dependency[2]]

    file = module.replace('/','+')
    file = 'files/modules/['+file+']Dependencies.csv'

    try:
        with open(file, 'r') as readFile:
            reader = csv.reader(readFile)
            dep = list(reader)
        readFile.close()

        if dependency not in dep:
            with open(file, 'a', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(dependency)

            writeFile.close()

    except:
        with open(file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(dependency)

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

def getAllProgress():

    try:
        with open('files/Progress.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            allProgress = list(reader)

        readFile.close()

        nodes = []
        for mod in allProgress:
            nodes.append(mod[1])

        return nodes

    except:
        return []

def getProgress(module):
    with open('files/Progress.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        modules = list(reader)

    readFile.close()

    for mod in modules:
        if mod[1] == module:
            return mod

def getDependencies(module):
    file = module.replace('/','+')
    file = 'files/modules/['+file+']Dependencies.csv'

    with open(file, 'r') as readFile:
        reader = csv.reader(readFile)
        dependencies = list(reader)

    readFile.close()

    return dependencies

def getUsages(module):

    file = module.replace('/','+')
    file = 'files/modules/['+file+']Usages.csv'

    with open(file, 'r') as readFile:
        reader = csv.reader(readFile)
        usages = list(reader)

    readFile.close()

    return usages

def switchStatus(module):

    with open('files/Progress.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        modules = list(reader)

    readFile.close()

    for mod in modules:
        if mod[1] == module:
            if mod[4] == 'closed':
                mod[4] = 'open'
            else:
                mod[4] = 'closed'

    with open('files/Progress.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(modules)

    writeFile.close()

def defaultStatus():

    with open('files/Progress.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        modules = list(reader)

    readFile.close()

    for mod in modules:
        mod[4] = 'closed'

    with open('files/Progress.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(modules)

    writeFile.close()
