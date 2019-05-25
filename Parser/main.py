import MVNparser
import csv
import save

graph = dict()

def parser(root_link,max_depth,depth, target_version = None):

    soup = MVNparser.getSoup(root_link)
    print('Current module:', root_link)

    module_link = root_link[root_link.find('/artifact'):][10:]
    module_name = module_link[module_link.find('/'):][1:]

    if not target_version:
        version = MVNparser.getVersion(soup)
    else:
        version = target_version[target_version.find(module_name):]

    version = version[version.find('/'):]
    print(version)

    try:
        with open('nodes.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            nodes = list(reader)

        readFile.close()
    except:
        nodes = []

    if [module_name] not in nodes:

        with open('nodes.csv', 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow([module_name])

        writeFile.close()

        soup_version = MVNparser.getSoup(root_link+version)
        dependencies_full = MVNparser.getDependencies(soup_version)
        dependencies_names = []

        for dependency in dependencies_full:
            try:
                dependencies_names.append(dependency[1][10:])
            except:
                dependencies_full.remove(dependency)

        print('There are {} dependencies in the module {}' .format(len(dependencies_full), module_link))

        link = [module_link]
        for dependency in dependencies_names:
            link.append(dependency)

        with open('links.csv', 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(link)

        writeFile.close()

        depth+=1
        if depth < max_depth:

            usages_link = root_link+version+'/usages'
            usages_soup = MVNparser.getSoup(usages_link)
            save.saveCurrentPage(module_name, 1)
            usages = MVNparser.getUsages(module_name, usages_link, usages_soup)

            print('There are {} usages in the module {}' .format(len(usages),module_link))
            if len(usages) >= 50: usages = usages[:50]

            for dependency in dependencies_full:
                print('Opening', dependency[1])
                parser("https://mvnrepository.com"+dependency[1],max_depth,depth,target_version = dependency[2])

            for usage in usages:
                print('Opening', usage)
                parser("https://mvnrepository.com"+usage,max_depth,depth)

        else:
            print("Depth too high")

    if [module_name] in nodes:

        try:
            with open('inProgress.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                node = list(reader)

            page = node[0][1]

            usages_link = root_link+version+'/usages'
            usages_soup = MVNparser.getSoup(usages_link)
            usages = MVNparser.getUsages(module_name, usages_link, usages_soup, page=page)

            print('Found {} more usages for the module {}' .format(len(usages), module_link))

            for usage in usages:
                print('Opening', usage)
                parser("https://mvnrepository.com"+usage,max_depth,depth)
        except:
            pass

root = "https://mvnrepository.com/artifact/org.apache.jclouds/jclouds-compute"

parser(root,3,0)

for key in graph:
    print(key)

root = "https://mvnrepository.com/artifact/org.dasein/dasein-cloud-core"

"""
parser(root,3,0)

MVNparser.writeJson(graph)

for key in graph:
    print(key)
"""
