import requests
from time import sleep
from random import randrange
from bs4 import BeautifulSoup, SoupStrainer

class UrlHandler:

    @staticmethod
    def getSoup(url):
        # Set headers  
        headers = requests.utils.default_headers()
        
        headers.update({ 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'})
        try:
            while True:
                req = requests.get(url, headers)
                break

            req.raise_for_status()
        
        except requests.exceptions.ConnectionError:
            print('\n\nCONNECTION ERROR. Retrying in 30 seconds.\n\n')
            sleep(30)

        except requests.exceptions.HTTPError as HTTPError:
            if HTTPError.response.status_code == 403: 
                print('\n\nFORBIDDEN.\n\n')
                exit()

        soup = BeautifulSoup(req.content, 'html.parser', parse_only=SoupStrainer('a'))

        timeout = randrange(5,10)
        sleep(timeout)

        return soup