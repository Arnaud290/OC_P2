import requests
from bs4 import BeautifulSoup
import csv
import os
from threading import Thread
from settings import *


class Scrap:

    def __init__(self):
        self.article_link = ''
        self.list_val_article = []
    
    def picture(self,list_val_article):
        if not os.path.exists("Pictures"):                                                                                      
            os.makedirs("Pictures")                                                                                             # création d'un répertoire si il n'existe pas    
        os.chdir("Pictures")
        response = requests.get(list_val_article[9])                                                                                     # récupération des données du lien de l'image
        fichier_image = list_val_article[2] + '.jpg'                                                                                            # création du nom du fichier image
        file = open(fichier_image, 'wb')
        file.write(response.content)                                                                                            # copie de l'image en local                         
        file.close()  

    def find_url_article(self, article_name):
        url = 'https://books.toscrape.com/index.html'                                                                   
        reponse = requests.get(url)                                                                                                                                                                      
        if reponse.ok:                                                                                                 
            soup = BeautifulSoup(reponse.text,'lxml')                                                                   
            nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                       
            nb_pages = int(nb_pages[10:])           
        for i in range(1,nb_pages + 1):  
            url = 'http://books.toscrape.com/catalogue/page-' + str(i) + '.html'                                                                    
            reponse = requests.get(url)                                                                                                                                                             
            if reponse.ok:                                                                                              
                soup = BeautifulSoup(reponse.text,'lxml')                                                                             
                articles = soup.findAll("article")                                                                          
                for article in articles:                                                                        
                    a = article.find('a')                                                                                                                                                                
                    self.article_link = ('http://books.toscrape.com/catalogue/'+ a['href'])                                                                                     
                    reponse = requests.get(self.article_link)
                    if reponse.ok:
                        soup = BeautifulSoup(reponse.text,'lxml')
                        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
                        if title == article_name: 
                            return self.article_link

    def find_val_article(self, article_url):
        reponse = requests.get(article_url)                                                                                     
        if reponse.ok:                                                                                                      
            soup = BeautifulSoup(reponse.text,'lxml')                                                                   
            title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text                                                                            
            product_description= soup.find('article').find('p').find_next('p').find_next('p').find_next('p').text               
            categorie = soup.find('ul', {'class':'breadcrumb'}).find('a').find_next('a').find_next('a').text                          
            tds = soup.findAll('td')                                                                                    
            product_list=[]                                                                                                                                       
            for td in tds:                                                                                                       
                product_list.append(td.text)                                                                                            
            image = soup.find('div',{'class':'item active'}).find('img')['src']                                         
            lien_image = 'http://books.toscrape.com/' + (image[6:])                                                                                                                             
            self.list_val_article = [self.article_link,
            product_list[0],
            title.replace('/','|'),
            product_list[3].strip('Â'),
            product_list[2].strip('Â'),        
            product_list[5],
            product_description,
            categorie,
            product_list[6],
            lien_image]                                      
            return self.list_val_article                                                               
                            
          