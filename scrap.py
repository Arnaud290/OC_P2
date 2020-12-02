import requests
from bs4 import BeautifulSoup
import csv
import os
from threading import Thread
from settings import *

class Th_find_url_article(Thread): 
    
        def __init__(self, article_name, i):
            Thread.__init__(self)
            self.article_name = article_name
            self.i = i
            self.article_link = None

        def run(self):

            url = 'http://books.toscrape.com/catalogue/page-' + str(self.i) + '.html'              
            reponse = requests.get(url)                                                                                                                                                             
            if reponse.ok:                                                                                              
                soup = BeautifulSoup(reponse.text,'lxml')                                                                             
                articles = soup.findAll("article")                                                                         
                for article in articles:                                                                        
                    a = article.find('a')                                                                                                                                                                
                    url = ('http://books.toscrape.com/catalogue/'+ a['href'])                                                                                     
                    reponse = requests.get(url)
                    if reponse.ok:
                        soup = BeautifulSoup(reponse.text,'lxml')
                        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
                        if title == self.article_name: 
                            self.article_link = url
        def result(self):
            return self.article_link

class Scrap():

    def __init__(self):
        self.list_val_article = []
        self.article_name = ''
        self.result_url_article = []

    def find_picture(self,list_val_article):
        if not os.path.exists("Pictures"):                                                                                      
            os.makedirs("Pictures")                                                                                            
        os.chdir("Pictures")
        response = requests.get(list_val_article[9])                                                                                     
        fichier_image = list_val_article[2] + '.jpg'                                                                                          
        file = open(fichier_image, 'wb')
        file.write(response.content)                                                                                                               
        file.close()                                    

    def find_url_article(self, article_name):
        url = 'https://books.toscrape.com/index.html'                                                                   
        reponse = requests.get(url)                                                                                                                                                                      
        if reponse.ok:                                                                                                 
            soup = BeautifulSoup(reponse.text,'lxml')                                                                   
            nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                       
            nb_pages = int(nb_pages[10:])  
        t=dict()       
        for i in range(nb_pages):  
            t[i] = Th_find_url_article(article_name, i + 1)
            t[i].start() 
        for i in t:
            t[i].join()
            if (t[i].result()) != None:
                return (t[i].result())
        
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
            self.list_val_article = [article_url,
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