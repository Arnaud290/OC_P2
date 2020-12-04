"""Text recovery module on HTML pages"""
import requests
from bs4 import BeautifulSoup
class Scrap:
    """Text recovery class on HTML pages"""
    def __init__(self):
        self.soup = ''
    def scrap(self, search_url):
        """Attribute allowing to retrieve the HTML
        text in function of the URL link"""
        reponse = requests.get(search_url)
        self.soup = BeautifulSoup(reponse.text,'lxml')
        return self.soup
