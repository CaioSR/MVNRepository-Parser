import os
import csv
import shutil
from datetime import datetime

class Addons:
    """
    This class implements 2 methods to manipulate the Nodes and Links files
    """
    @staticmethod
    def merge(path, projects):
        """
        Merges the folders with their results present in the given folder
        """
        directories = []
        for dir in projects:
            directories.append(path+'/'+dir)

        #create a new folder to save the merged result
        creationTime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        final = '/merged_'+ creationTime
        os.mkdir(path+final)

        for i in range(len(directories)):
            #setup iteration.
            if i == 0:

                #rewrite nodes with project identification
                with open(directories[i]+'/Nodes.csv', 'r') as p1, open(path+final+'/Nodes.csv', 'w', newline='') as wf:
                    rp1 = csv.reader(p1)
                    writer = csv.writer(wf)

                    for line in rp1:
                        writer.writerow([line[0],[projects[i]]])

                p1.close()
                wf.close()

                #copy links
                shutil.copy2(directories[i]+'/Links.csv', path+final+'/Links.csv')

            #this is the actual merge process
            else:

                #nodes merge
                with open(directories[i]+'/Nodes.csv', 'r') as p2, open(path+final+'/Nodes.csv', 'r') as rTemp, open(path+final+'/Nodes_temp.csv', 'w', newline='') as wf:
                    rTe = csv.reader(rTemp)
                    rp2 = csv.reader(p2)
                    writer = csv.writer(wf)

                    listed_rTe = list(rTe)
                    listed_rp2 = list(rp2)

                    #iterate through previous file
                    for line in listed_rTe:
                        #if the node is in the current file, write with the current project id added
                        if [line[0]] in listed_rp2:
                            l_common = Addons._string2list(line[1])
                            l_common.append(projects[i])
                            writer.writerow([line[0],l_common])
                        #if not, write as it is
                        else:
                            writer.writerow(line)

                    #remove identification from the previous file
                    for j in range(len(listed_rTe)):
                        listed_rTe[j] = listed_rTe[j][0]

                    #iterate through current file
                    for line in listed_rp2:
                        #write with the id of current project if the node is not on the previous file
                        if line[0] not in listed_rTe:
                            writer.writerow([line[0],[projects[i]]])

                rTemp.close()
                p2.close()
                wf.close()

                os.remove(path+final+'/Nodes.csv')
                os.rename(path+final+'/Nodes_temp.csv', path+final+'/Nodes.csv')

                #links merge
                with open(directories[i]+'/Links.csv', 'r') as p2, open(path+final+'/Links.csv', 'r') as rTemp, open(path+final+'/Links_temp.csv', 'w', newline='') as wf:
                    rp2 = csv.reader(p2)
                    rTe = csv.reader(rTemp)
                    listed_rTe = list(rTe)
                    writer = csv.writer(wf)

                    #write links from previous file
                    for line in listed_rTe:
                        writer.writerow(line)

                    #write links from the current file not in the previous file
                    for line in rp2:
                        if line not in listed_rTe:
                            writer.writerow(line)

                p2.close()
                rTemp.close()
                wf.close()

                os.remove(path+final+'/Links.csv')
                os.rename(path+final+'/Links_temp.csv', path+final+'/Links.csv')
        
        print('Merged')

    @staticmethod
    def addId(path):
        """
        Adds a header line in the Nodes and Links files
        """
        nodes_dict = {}
        with open(path+'/Nodes.csv', 'r') as rf, open(path+'/idNodes.csv', 'w', newline='') as wf:
            reader = csv.reader(rf)
            writer = csv.writer(wf)

            if 'merged_' in path:
                writer.writerow(['id', 'label', 'projects'])
            else:
                writer.writerow(['id', 'label'])
            
            id=0
            for line in reader:
                if 'merged_' in path:
                    writer.writerow([id,line[0],line[1]])
                else:
                    writer.writerow([id,line[0]])
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

        print('Added ids')

    @staticmethod
    def _string2list(string):
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

