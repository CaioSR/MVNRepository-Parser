import csv
import os

def string2list(string):
    li = []
    done = False
    while not done:
        start = string.find('\'') + 1
        end = string[start:].find('\'')+start
        li.append(string[start:end])
        string = string[end+1:]
        if string == ']':
            done = True

    return li

path = 'E:/1. Caio Shimada/TCC/Parser/parser/files-to-merge/'
path1 = path + 'spring' #diretório do projeto 1
proj1 = 'spring'
path2 = path + 'shiro' #diretório do projeto 2
proj2 = 'shiro'

projects = [path1, path2]

for i in range(len(projects)):
    if i == 0:
        with open(projects[i]+'/Nodes.csv', 'r') as p1, open(path+'/merged/Nodes.csv', 'w', newline='') as wf:
            rp1 = csv.reader(p1)
            writer = csv.writer(wf)
            for line in rp1:
                writer.writerow([line[0],[projects[i]]])

        p1.close()
        wf.close()

        with open(projects[i]+'/Links.csv', 'r') as p1, open(path+'/merged/Links_temp.csv', 'w', newline='') as wf:
            rP1 = csv.reader(p1)
            writer = csv.writer(wf)

            for line in rP1:
                for j in range(len(line)):
                    if j != 0:
                        writer.writerow([line[0],line[j]])

        p1.close()
        wf.close()

    else:

        with open(path+'/merged/Nodes.csv', 'r') as rf, open(projects[i]+'/Nodes.csv', 'r') as p2, open(path+'/merged/Nodes_temp.csv', 'w', newline='') as wf:
            reader = csv.reader(rf)
            rp2 = csv.reader(p2)
            writer = csv.writer(wf)

            listed_reader = list(reader)
            listed_rp2 = list(rp2)

            for line in listed_reader:
                if [line[0]] in listed_rp2:
                    l_common = string2list(line[1])
                    l_common.append(projects[i])
                    writer.writerow([line[0],l_common])
                else:
                    writer.writerow(line)

            for j in range(len(listed_reader)):
                listed_reader[j] = listed_reader[j][0]

            for line in listed_rp2:
                if line[0] not in listed_reader:
                    writer.writerow([line[0],[projects[i]]])

        rf.close()
        p2.close()
        wf.close()

        os.remove(path+'/merged/Nodes.csv')
        os.rename(path+'/merged/Nodes_temp.csv', path+'/merged/Nodes.csv')

        with open(projects[i]+'/Links.csv', 'r') as p2, open(path+'/merged/Links_temp.csv', 'r') as rTemp, open(path+'/merged/Links.csv', 'w', newline='') as wf:
            rP2 = csv.reader(p2)
            rTe = csv.reader(rTemp)
            listed_rTe = list(rTe)
            writer = csv.writer(wf)

            for line in listed_rTe:
                for j in range(len(line)):
                    if j != 0:
                        writer.writerow([line[0],line[j]])

            for line in rP2:
                for j in range(len(line)):
                    if j != 0:
                        if [line[0],line[j]] not in listed_rTe:
                            writer.writerow([line[0],line[j]])

        p2.close()
        rTemp.close()
        wf.close()

       
nodes_dict = {}
with open(path+'/merged/Nodes.csv', 'r') as rf, open (path+'/merged/Nodes_temp.csv', 'w', newline='') as wf:
    reader = csv.reader(rf)
    writer = csv.writer(wf)

    writer.writerow(['id', 'label', 'project'])
    
    id=0
    for line in reader:
        writer.writerow([id,line[0],line[1]])
        nodes_dict[line[0]] = id
        id+=1

rf.close()
wf.close()

os.remove(path+'/merged/Nodes.csv')
os.rename(path+'/merged/Nodes_temp.csv', path+'/merged/Nodes.csv')
    
with open(path+'/merged/Nodes.csv', 'r') as rNodes, open(path+'/merged/Links.csv', 'r') as rLinks, open(path+'/merged/Links_temp.csv', 'w', newline='') as wF:
    rNo = csv.reader(rNodes)
    rLi = csv.reader(rLinks)
    list_rLi = list(rLi)
    writer = csv.writer(wF)

    writer.writerow(['source','target'])
    for link in list_rLi:
        source, target = None, None
        source = nodes_dict[link[0]]
        target = nodes_dict[link[1]]
        # for node in nodes:
        #     if node[1] == link[0]:
        #         source = node[0]
        #     if node[1] == link[1]:
        #         target = node[0]
        #     if source != None and target != None:
        #         break
        writer.writerow([source,target])

rNodes.close()
rLinks.close()
wF.close()

os.remove(path+'/merged/Links.csv')
os.rename(path+'/merged/Links_temp.csv', path+'/merged/Links.csv')


# with open(proj1+'/Nodes.csv', 'r') as p1, open(proj2+'/Nodes.csv', 'r') as p2, open('merged/commonNodes.csv', 'w', newline='') as wF:
#     rP1 = csv.reader(p1)
#     rP2 = csv.reader(p2)
#     nodesproj2 = list(rP2)
#     writer = csv.writer(wF)

#     for nP1 in rP1:
#         if nP1 in nodesproj2:
#             writer.writerow(nP1)

# del nodesproj2
# p1.close()
# p2.close()
# wF.close()

# with open(proj1+'/Nodes.csv', 'r') as p1, open('merged/commonNodes.csv', 'r') as rCommon, open('merged/Nodes.csv', 'w', newline='') as wF:
#     rP1 = csv.reader(p1)
#     rCo = csv.reader(rCommon)
#     common = list(rCo)
#     writer = csv.writer(wF)

#     for nP1 in rP1:
#         if nP1 not in common:
#             writer.writerow([nP1[0],[proj1]]) #tratar pra pegar só o modulo

# del common
# p1.close()
# rCommon.close()
# wF.close()

# with open(proj2+'/Nodes.csv', 'r') as p2, open('merged/commonNodes.csv', 'r') as rCommon, open('merged/Nodes.csv', 'a', newline='') as wF:
#     rP2 = csv.reader(p2)
#     rCo = csv.reader(rCommon)
#     common = list(rCo)
#     writer = csv.writer(wF)

#     for nP2 in rP2:
#         if nP2 not in common:
#             writer.writerow([nP2[0],[proj2]]) #tratar pra pegar só o modulo

# del common
# p2.close()
# rCommon.close()
# wF.close()

# with open('merged/commonNodes.csv', 'r') as rCommon, open('merged/Nodes.csv', 'a', newline='') as wF:
#     rCo = csv.reader(rCommon)
#     writer = csv.writer(wF)

#     for node in rCo:
#         writer.writerow([node[0],[proj1,proj2]])

# rCommon.close()
# wF.close()

# i=0
# with open('merged/Nodes.csv', 'r') as rF, open('merged/Nodes_temp.csv', 'w', newline='') as wF:
#     reader = csv.reader(rF)
#     writer = csv.writer(wF)

#     writer.writerow(['id', 'label', 'project'])
#     for node in reader:
#         node.insert(0,i)
#         writer.writerow(node)
#         i+=1

# # os.remove('merged/commonNodes.csv')
# os.remove('merged/Nodes.csv')
# os.rename('merged/Nodes_temp.csv', 'merged/Nodes.csv')

# with open('spring/Links.csv', 'r') as p1, open('merged/Links_temp.csv', 'w', newline='') as wF:
#     rP1 = csv.reader(p1)
#     writer = csv.writer(wF)

#     for line in rP1:
#         for i in range(len(line)):
#             if i != 0:
#                 writer.writerow([line[0],line[i]])
# p1.close()
# wF.close()

# with open('shiro/Links.csv', 'r') as p2, open('merged/Links_temp.csv', 'r') as rTemp, open('merged/Links.csv', 'w', newline='') as wF:
#     rP2 = csv.reader(p2)
#     rTe = csv.reader(rTemp)
#     writer = csv.writer(wF)

#     for line in rTe:
#         for i in range(len(line)):
#             if i != 0:
#                 writer.writerow([line[0],line[i]])

#     for line in rP2:
#         for i in range(len(line)):
#             if i != 0:
#                 if [line[0],line[i]] not in rTe:
#                     writer.writerow([line[0],line[i]])

# p2.close()
# rTemp.close()
# wF.close()

# with open('merged/Nodes.csv', 'r') as rNodes, open('merged/Links.csv', 'r') as rLinks, open('merged/Links_temp.csv', 'w', newline='') as wF:
#     rNo = csv.reader(rNodes)
#     nodes = list(rNo)
#     rLi = csv.reader(rLinks)
#     writer = csv.writer(wF)

#     writer.writerow(['source','target'])
#     for link in rLi:
#         source, target = None, None
#         for node in nodes:
#             if node[1] == link[0]:
#                 source = node[0]
#             if node[1] == link[1]:
#                 target = node[0]
#             if source != None and target != None:
#                 break
#         writer.writerow([source,target])

# rNodes.close()
# rLinks.close()
# wF.close()

# os.remove('merged/Links.csv')
# os.rename('merged/Links_temp.csv', 'merged/Links.csv')
