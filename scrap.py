import requests
from bs4 import BeautifulSoup

class Scrap:

    def __init__(self):
         self.soup = ''
    
    def scrap(self, search_url): 
        reponse = requests.get(search_url)
        self.soup = BeautifulSoup(reponse.text,'lxml') 
        return self.soup