import csv
import os
from datetime import datetime

class Addons:
    def __init__(self):
        pass

    def merge(self, path, directories):
        projects = []
        for dir in directories:
            projects.append(path+dir)
        final = '/merged_'+datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

        for i in range(len(projects)):
            if i == 0:
                with open(projects[i]+'/Nodes.csv', 'r') as p1, open(path+final+'/Nodes.csv', 'w', newline='') as wf:
                    rp1 = csv.reader(p1)
                    writer = csv.writer(wf)
                    for line in rp1:
                        writer.writerow([line[0],[projects[i]]])

                p1.close()
                wf.close()

                with open(projects[i]+'/Links.csv', 'r') as p1, open(path+final+'/Links_temp.csv', 'w', newline='') as wf:
                    rP1 = csv.reader(p1)
                    writer = csv.writer(wf)

                    for line in rP1:
                        writer.writerow(line)

                p1.close()
                wf.close()

            else:

                with open(path+final+'/Nodes.csv', 'r') as rf, open(projects[i]+'/Nodes.csv', 'r') as p2, open(path+final+'/Nodes_temp.csv', 'w', newline='') as wf:
                    reader = csv.reader(rf)
                    rp2 = csv.reader(p2)
                    writer = csv.writer(wf)

                    listed_reader = list(reader)
                    listed_rp2 = list(rp2)

                    for line in listed_reader:
                        if [line[0]] in listed_rp2:
                            l_common = self._string2list(line[1])
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

                os.remove(path+final+'/Nodes.csv')
                os.rename(path+final+'/Nodes_temp.csv', path+final+'/Nodes.csv')

                with open(projects[i]+'/Links.csv', 'r') as p2, open(path+final+'/Links_temp.csv', 'r') as rTemp, open(path+final+'/Links.csv', 'w', newline='') as wf:
                    rP2 = csv.reader(p2)
                    rTe = csv.reader(rTemp)
                    listed_rTe = list(rTe)
                    writer = csv.writer(wf)

                    for line in rP2:
                        if line not in listed_rTe:
                            writer.writerow(line)

                p2.close()
                rTemp.close()
                wf.close()

    def addId(self, path):
        nodes_dict = {}
        with open(path+'/Nodes.csv', 'r') as rf, open (path+'/idNodes.csv', 'w', newline='') as wf:
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
            
        with open(path+'/Links.csv', 'r') as rLinks, open(path+'/idLinks.csv', 'w', newline='') as wF:
            rLi = csv.reader(rLinks)
            list_rLi = list(rLi)
            writer = csv.writer(wF)

            writer.writerow(['source','target'])
            for link in list_rLi:
                source, target = None, None
                source = nodes_dict[link[0]]
                target = nodes_dict[link[1]]
                writer.writerow([source,target])

        rLinks.close()
        wF.close()


    def _string2list(self, string):
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
