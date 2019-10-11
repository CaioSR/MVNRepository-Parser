import csv
import json

with open('files/Nodes.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    nodesCsv = list(reader)

    readFile.close()

with open('files/Links.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    linksCsv = list(reader)

    readFile.close()

nodes = []
links = []

for node in nodesCsv:
    nodes.append({"name" : '', "id" : node[0]})

for link in linksCsv:
    for i in range(len(link)):
        if i != 0:
            links.append({"source" : link[0], "target" : link[i]})

data = {'nodes' : nodes, 'links' : links}

with open('files/grafo.json', 'w') as fp:
    json.dump(data, fp)
