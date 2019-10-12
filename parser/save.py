import csv
import os
import shutil

class Save:

    f_dir = None
    p_dir = None

    def __init__(self, f_dir, p_dir, proj):
        proj = proj.replace('/','+')

        if f_dir[-1] == '/':
            self.f_dir = f_dir
        else:
            self.f_dir = f_dir + '/'

        if p_dir[-1] == '/':
            self.p_dir = p_dir
        else:
            self.p_dir = p_dir + '/'

        self.verifyDirectories(proj)


    def verifyDirectories(self, proj):
        try:
            self.defaultStatus()
            print('All status to closed')
        except:
            print('First Run')

            os.mkdir(self.p_dir)
            os.mkdir(self.p_dir + proj)
            os.mkdir(self.p_dir + proj + '/modules')
            os.mkdir(self.f_dir)
            os.mkdir(self.f_dir + proj)

        self.p_dir = self.p_dir + proj
        self.f_dir = self.f_dir + proj


    def addLinks(self, module, dependencies):

        modules = [module]
        for dependency in dependencies:
            modules.append(dependency[2])

        with open(self.p_dir + '/Links.csv', 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(modules)

        writeFile.close()

    def addModule(self, module):

        try:
            with open(self.p_dir + '/Nodes.csv', 'r', newline='') as readFile:
                reader = csv.reader(readFile)
                nodes = list(reader)

            readFile.close()

            if [module] not in nodes:
                with open(self.p_dir + '/Nodes.csv', 'a', newline='') as writeFile:
                    writer  = csv.writer(writeFile)
                    writer.writerow([module])

                writeFile.close()
        except:

            with open(self.p_dir + '/Nodes.csv', 'w', newline='') as writeFile:
                writer  = csv.writer(writeFile)
                writer.writerow([module])

            writeFile.close()


    def initialize(self, module,depth):

        with open(self.p_dir + '/Progress.csv', 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([depth,module,'Initialized','Null','open'])

        writeFile.close()

    def setState(self, module, state):

        with open(self.p_dir + '/Progress.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            modules = list(reader)

        readFile.close()

        for mod in modules:
            if mod[1] == module:
                mod[2] = state
                mod[3] = 'Null'

        with open(self.p_dir + '/Progress.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(modules)

        writeFile.close()
    """
        if state == 'Complete':
            delFile(module)
    """
    def setCurrentPage(self, module, page):

        with open(self.p_dir + '/Progress.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            modules = list(reader)

        readFile.close()

        for mod in modules:
            if mod[1] == module:
                mod[3] = page

        with open(self.p_dir + '/Progress.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(modules)

        writeFile.close()

    def setCurrent(self, module, relation, current):

        with open(self.p_dir + '/Progress.csv', 'r') as readFile:
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

        with open(self.p_dir + '/Progress.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(modules)

        writeFile.close()

    def setUsage(self, module, usage):

        file = module.replace('/','+')
        file = self.p_dir + '/modules/['+file+']Usages.csv'

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

    def setDependency(self, module, dependency):

        dependency = [dependency[1],dependency[2]]

        file = module.replace('/','+')
        file = self.p_dir + '/modules/['+file+']Dependencies.csv'

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

    def checkUsages(self, module):
        pass

    def getLastPage():
        pass

    def getAllProgress(self):

        try:
            with open(self.p_dir + '/Progress.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                allProgress = list(reader)

            readFile.close()

            nodes = []
            for mod in allProgress:
                nodes.append(mod[1])

            return nodes

        except:
            return []

    def getProgress(self, module):
        with open(self.p_dir + '/Progress.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            modules = list(reader)

        readFile.close()

        for mod in modules:
            if mod[1] == module:
                return mod

    def getDependencies(self, module):
        file = module.replace('/','+')
        file = self.p_dir + '/modules/['+file+']Dependencies.csv'

        with open(file, 'r') as readFile:
            reader = csv.reader(readFile)
            dependencies = list(reader)

        readFile.close()

        return dependencies

    def getUsages(self, module):

        file = module.replace('/','+')
        file = self.p_dir + '/modules/['+file+']Usages.csv'

        with open(file, 'r') as readFile:
            reader = csv.reader(readFile)
            usages = list(reader)

        readFile.close()

        return usages

    def switchStatus(self, module):

        with open(self.p_dir + '/Progress.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            modules = list(reader)

        readFile.close()

        for mod in modules:
            if mod[1] == module:
                if mod[4] == 'closed':
                    mod[4] = 'open'
                else:
                    mod[4] = 'closed'

        with open(self.p_dir + '/Progress.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(modules)

        writeFile.close()

    def defaultStatus(self):

        with open(self.p_dir + '/Progress.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            modules = list(reader)

        readFile.close()

        for mod in modules:
            mod[4] = 'closed'

        with open(self.p_dir + '/Progress.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(modules)

        writeFile.close()

    def copyToFinal(self):
        shutil.copy(self.p_dir + '/Nodes.csv', self.f_dir)
        shutil.copy(self.p_dir + '/Links.csv', self.f_dir)
