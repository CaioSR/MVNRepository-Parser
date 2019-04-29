"""
        for usage in usages:
            if usage != []:
                if usage[10:] in graph:
                    graph[usage[10:]].append(module_link)
                else:
                    graph.update({usage[10:] : [module_link]})
                    """


import MVNparser

graph = dict()

def parser(root_link,max_depth,depth):
    if depth >= max_depth:
        print('Depth too high', depth)
        return

    soup = MVNparser.getSoup(root_link)
    print('Current module:',root_link)

    latest_version = MVNparser.getLatestVersion(soup)
    module_name = MVNparser.getModuleName(soup)
    module_link = root_link[root_link.find('/artifact'):][10:]

    if module_link not in graph:

        latestVersionUsages=MVNparser.getLatestVersionUsages(soup)
        if latestVersionUsages != 0:
            usages_link = root_link+latestVersionUsages
            usages_soup = MVNparser.getSoup(usages_link)
            usages = MVNparser.getUsages(module_name, usages_link, usages_soup)
        else:
            usages = []

        print('There are {} usages in the module {}' .format(len(usages),module_link))
        if len(usages) >= 50: usages = usages[:50]

        print(root_link+latest_version[latest_version.find('/'):])
        soup_latest_version = MVNparser.getSoup(root_link+latest_version[latest_version.find('/'):])
        dependencies_full = MVNparser.getDependencies(soup_latest_version)
        dependencies_names = []

        for dependency in dependencies_full:
            try:
                dependencies_names.append(dependency[1][10:])
            except:
                dependencies_full.remove(dependency)

        print('There are {} dependencies in the module {}' .format(len(dependencies_full), module_link))

        graph.update({module_link : dependencies_names})

        for dependency in dependencies_full:
            print('Opening', dependency[1])
            parser("https://mvnrepository.com"+dependency[1],max_depth,depth+1)

        for usage in usages:
            print('Opening', usage)
            parser("https://mvnrepository.com"+usage,max_depth,depth+1)

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
