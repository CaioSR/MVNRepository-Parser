import csv
import os

proj1 = 'spring' #diretório do projeto 1
proj2 = 'shiro' #diretório do projeto 2

with open(proj1+'/Nodes.csv', 'r') as p1, open(proj2+'/Nodes.csv', 'r') as p2, open('merged/commonNodes.csv', 'w', newline='') as wF:
    rP1 = csv.reader(p1)
    rP2 = csv.reader(p2)
    nodesproj2 = list(rP2)
    writer = csv.writer(wF)

    for nP1 in rP1:
        if nP1 in nodesproj2:
            writer.writerow(nP1)

del nodesproj2
p1.close()
p2.close()
wF.close()

with open(proj1+'/Nodes.csv', 'r') as p1, open('merged/commonNodes.csv', 'r') as rCommon, open('merged/Nodes.csv', 'w', newline='') as wF:
    rP1 = csv.reader(p1)
    rCo = csv.reader(rCommon)
    common = list(rCo)
    writer = csv.writer(wF)

    for nP1 in rP1:
        if nP1 not in common:
            writer.writerow([nP1[0],[proj1]]) #tratar pra pegar só o modulo

del common
p1.close()
rCommon.close()
wF.close()

with open(proj2+'/Nodes.csv', 'r') as p2, open('merged/commonNodes.csv', 'r') as rCommon, open('merged/Nodes.csv', 'a', newline='') as wF:
    rP2 = csv.reader(p2)
    rCo = csv.reader(rCommon)
    common = list(rCo)
    writer = csv.writer(wF)

    for nP2 in rP2:
        if nP2 not in common:
            writer.writerow([nP2[0],[proj2]]) #tratar pra pegar só o modulo

del common
p2.close()
rCommon.close()
wF.close()

with open('merged/commonNodes.csv', 'r') as rCommon, open('merged/Nodes.csv', 'a', newline='') as wF:
    rCo = csv.reader(rCommon)
    writer = csv.writer(wF)

    for node in rCo:
        writer.writerow([node[0],[proj1,proj2]])

rCommon.close()
wF.close()

i=0
with open('merged/Nodes.csv', 'r') as rF, open('merged/Nodes_temp.csv', 'w', newline='') as wF:
    reader = csv.reader(rF)
    writer = csv.writer(wF)

    writer.writerow(['id', 'label', 'project'])
    for node in reader:
        node.insert(0,i)
        writer.writerow(node)
        i+=1

# os.remove('merged/commonNodes.csv')
os.remove('merged/Nodes.csv')
os.rename('merged/Nodes_temp.csv', 'merged/Nodes.csv')

with open('spring/Links.csv', 'r') as p1, open('merged/Links_temp.csv', 'w', newline='') as wF:
    rP1 = csv.reader(p1)
    writer = csv.writer(wF)

    for line in rP1:
        for i in range(len(line)):
            if i != 0:
                writer.writerow([line[0],line[i]])
p1.close()
wF.close()

with open('shiro/Links.csv', 'r') as p2, open('merged/Links_temp.csv', 'r') as rTemp, open('merged/Links.csv', 'w', newline='') as wF:
    rP2 = csv.reader(p2)
    rTe = csv.reader(rTemp)
    writer = csv.writer(wF)

    for line in rTe:
        for i in range(len(line)):
            if i != 0:
                writer.writerow([line[0],line[i]])

    for line in rP2:
        for i in range(len(line)):
            if i != 0:
                if [line[0],line[i]] not in rTe:
                    writer.writerow([line[0],line[i]])

p2.close()
rTemp.close()
wF.close()

with open('merged/Nodes.csv', 'r') as rNodes, open('merged/Links.csv', 'r') as rLinks, open('merged/Links_temp.csv', 'w', newline='') as wF:
    rNo = csv.reader(rNodes)
    nodes = list(rNo)
    rLi = csv.reader(rLinks)
    writer = csv.writer(wF)

    writer.writerow(['source','target'])
    for link in rLi:
        source, target = None, None
        for node in nodes:
            if node[1] == link[0]:
                source = node[0]
            if node[1] == link[1]:
                target = node[0]
            if source != None and target != None:
                break
        writer.writerow([source,target])

rNodes.close()
rLinks.close()
wF.close()

os.remove('merged/Links.csv')
os.rename('merged/Links_temp.csv', 'merged/Links.csv')
