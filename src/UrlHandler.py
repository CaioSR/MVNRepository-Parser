import requests
from time import sleep
from random import randrange
from bs4 import BeautifulSoup, SoupStrainer

class UrlHandler:
    """
    This class handles the urls calls
    """
    @staticmethod
    def getSoup(url):
        """
        Tries to connect to the given url and returns the Soup object for scrapping
        """
        # Set headers  
        headers = requests.utils.default_headers()
        
        headers.update({ 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15'})
        while True:
            try:
                req = requests.get(url, headers)
                req.raise_for_status()
                break

            except requests.exceptions.HTTPError as HTTPError:
                if HTTPError.response.status_code == 403: 
                    print('\n\nFORBIDDEN.\n\n')
                    exit()

            except requests.exceptions.ConnectionError:
                print('\n\nCONNECTION ERROR. Retrying in 30 seconds.\n\n')
                sleep(30)
                
        soup = BeautifulSoup(req.content, 'html.parser', parse_only=SoupStrainer('a'))

        timeout = randrange(7,10)
        sleep(timeout)

        return soup