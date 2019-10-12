import csv
import os

with open('shiro/Nodes.csv', 'r') as readFile, open('shiro/Nodes_temp.csv', 'w', newline='') as writeFile:
    reader = csv.reader(readFile)
    writer = csv.writer(writeFile)

    added = []
    for node in reader:
        if node not in added:
            writer.writerow(node)
            added.append(node)

readFile.close()
writeFile.close()

os.remove('shiro/Nodes.csv')
os.rename('shiro/Nodes_temp.csv', 'shiro/Nodes.csv')
