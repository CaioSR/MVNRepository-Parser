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
        found = False
        with open('files/Nodes.csv', 'r', newline='') as readFile:
            for line in readFile:
                if line == module:
                    found = True
                    break

        readFile.close()

        if not found:
            with open('files/Nodes.csv', 'a', newline='') as writeFile:
                writer  = csv.writer(writeFile)
                writer.writerow([module])

            writeFile.close()
    except:
        with open('files/Nodes.csv', 'w', newline='') as writeFile:
            writer  = csv.writer(writeFile)
            writer.writerow([module])

        writeFile.close()

    #
    # try:
    #     with open('files/Nodes.csv', 'r', newline='') as readFile:
    #         reader = csv.reader(readFile)
    #         nodes = list(reader)
    #
    #     readFile.close()
    #
    #     if [module] not in nodes:
    #         with open('files/Nodes.csv', 'a', newline='') as writeFile:
    #             writer  = csv.writer(writeFile)
    #             writer.writerow([module])
    #
    #         writeFile.close()
    # except:
    #
    #     with open('files/Nodes.csv', 'w', newline='') as writeFile:
    #         writer  = csv.writer(writeFile)
    #         writer.writerow([module])
    #
    #     writeFile.close()


def initialize(module,depth):

    with open('files/Progress.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([depth,module,'Initialized','Null','open'])

    writeFile.close()

def setState(module, state):

    with open('files/Progress.csv', 'r') as readFile, open('files/Progress_temp.csv', 'w', newline='') as writeFile:
        reader = csv.reader(readFile)
        writer = csv.writer(writeFile)
        for line in reader:
            if module == line[1]:
                line[2] = state
                line[3] = 'Null'
                writer.writerow(line)
            else:
                writer.writerow(line)

    readFile.close()
    writeFile.close()
    os.remove('files/Progress.csv')
    os.rename('files/Progress_temp.csv', 'files/Progress.csv')

    # with open('files/Progress.csv', 'r') as readFile:
    #     reader = csv.reader(readFile)
    #     modules = list(reader)
    #
    # readFile.close()
    #
    # for mod in modules:
    #     if mod[1] == module:
    #         mod[2] = state
    #         mod[3] = 'Null'
    #
    # with open('files/Progress.csv', 'w', newline='') as writeFile:
    #     writer = csv.writer(writeFile)
    #     writer.writerows(modules)
    #
    # writeFile.close()

    # if state == 'Complete':
    #     delFile(module)

def setCurrentPage(module, page):

    with open('files/Progress.csv', 'r') as readFile, open('files/Progress_temp.csv', 'w', newline='') as writeFile:
        reader = csv.reader(readFile)
        writer = csv.writer(writeFile)
        for line in reader:
            if module == line[1]:
                line[3] = page
                writer.writerow(line)
            else:
                writer.writerow(line)

    readFile.close()
    writeFile.close()
    os.remove('files/Progress.csv')
    os.rename('files/Progress_temp.csv', 'files/Progress.csv')

    # with open('files/Progress.csv', 'r') as readFile:
    #     reader = csv.reader(readFile)
    #     modules = list(reader)
    #
    # readFile.close()
    #
    # for mod in modules:
    #     if mod[1] == module:
    #         mod[3] = page
    #
    # with open('files/Progress.csv', 'w', newline='') as writeFile:
    #     writer = csv.writer(writeFile)
    #     writer.writerows(modules)
    #
    # writeFile.close()

def setCurrent(module, relation, current):

    with open('files/Progress.csv', 'r') as readFile, open('files/Progress_temp.csv', 'w', newline='') as writeFile:
        reader = csv.reader(readFile)
        writer = csv.writer(writeFile)
        for line in reader:
            if module == line[1]:
                if relation == 'd':
                    line[2] = 'Verifying dependency'
                elif relation == 'u':
                    line[2] = 'Verifying usage'
                line[3] = current
                writer.writerow(line)
            else:
                writer.writerow(line)

    readFile.close()
    writeFile.close()
    os.remove('files/Progress.csv')
    os.rename('files/Progress_temp.csv', 'files/Progress.csv')
    #
    # with open('files/Progress.csv', 'r') as readFile:
    #     reader = csv.reader(readFile)
    #     modules = list(reader)
    #
    # readFile.close()
    #
    # for mod in modules:
    #     if mod[1] == module:
    #         if relation == 'd':
    #             mod[2] = 'Verifying dependency'
    #         elif relation == 'u':
    #             mod[2] = 'Verifying usage'
    #         mod[3] = current
    #
    # with open('files/Progress.csv', 'w', newline='') as writeFile:
    #     writer = csv.writer(writeFile)
    #     writer.writerows(modules)
    #
    # writeFile.close()

def setUsage(module, usage):

    file = module.replace('/','+')
    file = 'files/modules/['+file+']Usages.csv'

    try:
        found = False
        with open(file, 'r') as readFile:
            for line in readFile:
                if usage == line:
                    found = True
                    break

        readFile.close()

        if not found:
            with open(file, 'a', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow([usage])

            writeFile.close()

    except:
        with open(file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([usage])

        writeFile.close()

    # try:
    #     with open(file, 'r') as readFile:
    #         reader = csv.reader(readFile)
    #         us = list(reader)
    #
    #     readFile.close()
    #
    #     if [usage] not in us:
    #         with open(file, 'a', newline='') as writeFile:
    #             writer = csv.writer(writeFile)
    #             writer.writerow([usage])
    #
    #         writeFile.close()
    #
    # except:
    #     with open(file, 'w', newline='') as writeFile:
    #         writer = csv.writer(writeFile)
    #         writer.writerow([usage])
    #
    #     writeFile.close()

def setDependency(module, dependency):

    if dependency != 'None':
        dependency = dependency[2]

    file = module.replace('/','+')
    file = 'files/modules/['+file+']Dependencies.csv'

    try:
        found = False
        with open(file, 'r') as readFile:
            for line in readFile:
                if dependency == line:
                    found = True
                    break

        readFile.close()

        if not found:
            with open(file, 'a', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow([dependency])

            writeFile.close()

    except:
        with open(file, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([dependency])

        writeFile.close()


    # try:
    #     with open(file, 'r') as readFile:
    #         reader = csv.reader(readFile)
    #         dep = list(reader)
    #     readFile.close()
    #
    #     if dependency not in dep:
    #         with open(file, 'a', newline='') as writeFile:
    #             writer = csv.writer(writeFile)
    #             writer.writerow(dependency)
    #
    #         writeFile.close()
    #
    # except:
    #     with open(file, 'w', newline='') as writeFile:
    #         writer = csv.writer(writeFile)
    #         writer.writerow(dependency)
    #
    #     writeFile.close()




# def delFile(module):
#
#     module = module.replace('/','+')
#     os.remove('['+module+']Dependencies.csv')
#     try:
#         os.remove('['+module+']Usages.csv')
#     except:
#         pass

# def checkUsages(module):
#     pass
#
# def getLastPage():
#     pass

def checkProgress(module):

    try:
        with open('files/Progress.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for line in reader:
                if module == line[1]:
                    return True
            return False
    except:
        return False


    # try:
    #     with open('files/Progress.csv', 'r') as readFile:
    #         reader = csv.reader(readFile)
    #         allProgress = list(reader)
    #
    #     readFile.close()
    #
    #     nodes = []
    #     for mod in allProgress:
    #         nodes.append(mod[1])
    #
    #     return nodes
    #
    # except:
    #     return []

def getProgress(module):

    with open('files/Progress.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for line in reader:
            if module == line[1]:
                return line

    readFile.close()

    # with open('files/Progress.csv', 'r') as readFile:
    #     reader = csv.reader(readFile)
    #     modules = list(reader)
    #
    # readFile.close()
    #
    # for mod in modules:
    #     if mod[1] == module:
    #         return mod

def getDependencies(module):
    file = module.replace('/','+')
    file = 'files/modules/['+file+']Dependencies.csv'

    with open(file, 'r') as readFile:
        for line in readFile:
            yield line.strip('\n')

    return

    # with open(file, 'r') as readFile:
    #     reader = csv.reader(readFile)
    #     dependencies = list(reader)
    #
    # readFile.close()
    #
    # return dependencies

def getUsages(module):

    file = module.replace('/','+')
    file = 'files/modules/['+file+']Usages.csv'

    with open(file, 'r') as readFile:
        for line in readFile:
            yield line.strip('\n')

    return

    # with open(file, 'r') as readFile:
    #     reader = csv.reader(readFile)
    #     usages = list(reader)
    #
    # readFile.close()
    #
    # return usages

def switchStatus(module):

    with open('files/Progress.csv', 'r') as readFile, open('files/Progress_temp.csv', 'w', newline='') as writeFile:
        reader = csv.reader(readFile)
        writer = csv.writer(writeFile)
        for line in reader:
            if module == line[1]:
                if line[4] == 'closed':
                    line[4] = 'open'
                else:
                    line[4] = 'closed'
                writer.writerow(line)
            else:
                writer.writerow(line)

    readFile.close()
    writeFile.close()
    os.remove('files/Progress.csv')
    os.rename('files/Progress_temp.csv', 'files/Progress.csv')

    # with open('files/Progress.csv', 'r') as readFile:
    #     reader = csv.reader(readFile)
    #     modules = list(reader)
    #
    # readFile.close()
    #
    # for mod in modules:
    #     if mod[1] == module:
    #         if mod[4] == 'closed':
    #             mod[4] = 'open'
    #         else:
    #             mod[4] = 'closed'
    #
    # with open('files/Progress.csv', 'w', newline='') as writeFile:
    #     writer = csv.writer(writeFile)
    #     writer.writerows(modules)
    #
    # writeFile.close()

def defaultStatus():

    with open('files/Progress.csv', 'r') as readFile, open('files/Progress_temp.csv', 'w', newline='') as writeFile:
        reader = csv.reader(readFile)
        writer = csv.writer(writeFile)
        for line in reader:
            line[4] = 'closed'
            writer.writerow(line)

    readFile.close()
    writeFile.close()
    os.remove('files/Progress.csv')
    os.rename('files/Progress_temp.csv', 'files/Progress.csv')

    # with open('files/Progress.csv', 'r') as readFile:
    #     reader = csv.reader(readFile)
    #     modules = list(reader)
    #
    # readFile.close()
    #
    # for mod in modules:
    #     mod[4] = 'closed'
    #
    # with open('files/Progress.csv', 'w', newline='') as writeFile:
    #     writer = csv.writer(writeFile)
    #     writer.writerows(modules)
    #
    # writeFile.close()
