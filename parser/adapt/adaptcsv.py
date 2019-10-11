import csv

with open('files/Nodes.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    nodes = list(reader)
readFile.close()

i=1
for node in nodes:
    node.insert(0,i)
    i+=1

with open('files/aNodes.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['id', 'label'])
    writer.writerows(nodes)
writeFile.close()

with open('files/Links.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    links = list(reader)
readFile.close()

eachLink = []
source, target = '', ''
for link in links:
    for l in range(len(link)):
        if l == 0:
            for node in nodes:
                if node[1] == link[l]:
                    source = node[0]
                    break
        if l != 0:
            for node in nodes:
                if node[1] == link[l]:
                    target = node[0]
                    break
            eachLink.append([source, target])

with open('files/aLinks.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['source', 'target'])
    writer.writerows(eachLink)
writeFile.close()
