import csv
import os

def saveCurrentPage(module_name, page):

    with open('inProgress.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([module_name, page])

    writeFile.close()

def doneUsage():

    os.remove('inProgress.csv')
