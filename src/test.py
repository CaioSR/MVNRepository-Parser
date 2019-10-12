from html.parser import HTMLParser
from html.entities import name2codepoint
from urllib.request import urlopen #biblioteca para abrir e ler um url

class MyHTMLParser(HTMLParser):
    link = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for inAttr in attrs:
                if inAttr[0] == 'href':
                    self.link.append(inAttr[1])


parser = MyHTMLParser()
page = urlopen("https://mvnrepository.com/artifact/com.google.auto.service/auto-service/1.0-rc3")
html = page.read()
html = html.decode('utf-8')
parser.feed(html)
print(parser.link)
