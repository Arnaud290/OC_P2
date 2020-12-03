import csv
import os
from settings import *
from scrap import *
from threading import Thread

class Th_find_url_article(Thread): 
    
        def __init__(self, article_name, i):
            Thread.__init__(self)
            self.article_name = article_name
            self.i = i
            self.article_link = None
            self.scrap = Scrap()

        def run(self):
            soup = self.scrap.scrap(url + 'catalogue/page-' + str(self.i) + '.html')                                                                            
            articles = soup.findAll("article")                                                                         
            for article in articles:                                                                        
                a = article.find('a')                                                                                                                                                                
                url_article = ('http://books.toscrape.com/catalogue/'+ a['href'])
                soup = self.scrap.scrap(url_article)
                title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
                if title == self.article_name: 
                    self.article_link = url_article
                    
        def result(self):
            return self.article_link

class Find:

    def __init__(self):
        self.list_val_article = []
        self.result_url_article = []
        self.list_url_category  = {}
        self.scrap = Scrap()

    def find_url_article(self, article_name):                                                                  
        soup = self.scrap.scrap(url)                                                                                                                                                                    
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
            soup = self.scrap.scrap(article_url)                                                                
            title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text                                                                            
            product_description= soup.find('article').find('p').find_next('p').find_next('p').find_next('p').text               
            categorie = soup.find('ul', {'class':'breadcrumb'}).find('a').find_next('a').find_next('a').text                          
            tds = soup.findAll('td')                                                                                    
            product_list=[]                                                                                                                                       
            for td in tds:                                                                                                       
                product_list.append(td.text)                                                                                            
            image = soup.find('div',{'class':'item active'}).find('img')['src']                                         
            lien_image = url + (image[6:])                                                                                                                             
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

    def find_all_urls_articles_category(self, url_category):
        links = []   
        def find_links_articles(url_category):    
            soup = self.scrap.scrap(url_category)                                                              
            articles = soup.findAll("article") 
            for article in articles:                                                                               
                a = article.find('a')                                                                              
                link = a['href']    
                links.append(url +"catalogue/"+ str(link)[9:])     
        soup = self.scrap.scrap(url_category)    
        try:
            nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                     
        except: 
            find_links_articles(url_category)
            return links    
        else:
            nb_pages = int(nb_pages[10:])
            for i in range(1, nb_pages + 1):
                url_category_more_pages = url_category[:-10] + 'page-' + str(i) + '.html' 
                find_links_articles(url_category_more_pages)       
            return links                                                       

    def find_all_category(self):     
        soup = soup = self.scrap.scrap(url)  
        lis = soup.find('ul', {'class':'nav nav-list'}).find('li').find('ul').findAll('li')                                 # récupération des informations des catégories
        for li in lis:
            categorie = li.text.strip()
            a = li.find('a')                                                                              
            link = url + a['href']  
            self.list_url_category[li.text.strip()] = link                     
        return self.list_url_category