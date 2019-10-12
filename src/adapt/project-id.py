import csv

with open('spring/aNodes.csv', 'r') as rF, open('spring/aNodes_new.csv', 'w', newline='') as wF:
    reader = csv.reader(rF)
    for node in reader:
        node.append([1])
        writer = csv.writer(wF)
        writer.writerow(node)

    rF.close()
    wF.close()

with open('shiro/aNodes.csv', 'r') as rF, open('shiro/aNodes_new.csv', 'w', newline='') as wF:
    reader = csv.reader(rF)
    for node in reader:
        node.append([2])
        writer = csv.writer(wF)
        writer.writerow(node)

    rF.close()
    wF.close()
