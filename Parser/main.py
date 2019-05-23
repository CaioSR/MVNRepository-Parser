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

    if module_link not in graph:

        soup_version = MVNparser.getSoup(root_link+version)
        dependencies_full = MVNparser.getDependencies(soup_version)
        dependencies_names = []

        for dependency in dependencies_full:
            try:
                dependencies_names.append(dependency[1][10:])
            except:
                dependencies_full.remove(dependency)

        print('There are {} dependencies in the module {}' .format(len(dependencies_full), module_link))

        graph.update({module_link : dependencies_names})

        depth+=1
        if depth < max_depth:

            usages_link = root_link+version+'/usages'
            usages_soup = MVNparser.getSoup(usages_link)
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
