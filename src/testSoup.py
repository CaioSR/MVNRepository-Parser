import requests
from urllib.request import urlopen
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import time

def separateV(project, getRoot = False, getVersion = False, getModule = False):
    aux1 = project[project.find('/artifact'):][10:] #return project/module/version
    aux2 = aux1[aux1.find('/'):][1:] #return module/version
    version = aux2[aux2.find('/'):] #return /version
    root = project[:project.find(version)]

    response = []

    if getRoot:
        response.append(root)
    if getVersion:
        response.append(version)
    if getModule:
        response.append(aux1)

    return response

# Set headers  
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
req = requests.get('https://mvnrepository.com/artifact/org.apache.jclouds/jclouds-core', headers)
soup = BeautifulSoup(req.content, 'html.parser', parse_only=SoupStrainer('a'))

#print(soup.prettify())

versions = []
multiple_versions = False
for tag in soup.find_all('a'):
    if tag.get('class') and tag.get('class')[0] == 'vsc':
        multiple_versions = True
        break

if multiple_versions:
    for tag in soup.find_all('a', class_='vsc'):
        versions.append(tag.get('href'))
else:
    for tag in soup.find_all('a', class_='vbtn'):
        versions.append(tag.get('href'))

return versions



mod = '/artifact/org.apache.jclouds/jclouds-core/1.2'
mod = mod[10:]
mod = mod[mod.find('/'):]
print(mod)







