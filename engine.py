from csv_file import *
from scrap import Scrap
from settings import *
import os
class Engine:

    def __init__(self):
        self.scrap = Scrap()
        self.csv = Make_csv()
        self.list_category = {}
        self.list_article = []

    def repertory(repertory_name):
        if not os.path.exists(repertory_name):                                                                                      
            os.makedirs(repertory_name)                                                                                                
        os.chdir(repertory_name)        

    def lunch_article_CSV_picture(self):
        article_name = input("Veuillez entrer le nom de l'article: ")                                                                     
        url_article = self.scrap.find_url_article(article_name)                                                                                                                                                                
        self.list_article = self.scrap.find_val_article(url_article)
        Engine.repertory("Articles")
        self.csv.article_csv(self.list_article)  
        Engine.repertory("Pictures")
        self.scrap.find_picture(self.list_article[2],self.list_article[9])

    def lunch_category_CSV_picture(self):
        links_article_category = []
        category_name = input("Veuillez entrer le nom de la catégorie: ") 
        url_category = self.scrap.find_url_category(category_name)
        links_article_category = self.scrap.find_all_urls_articles_category(url_category)
        self.list_category[category_name] = []
        for url in links_article_category:
            self.list_category[category_name].append(self.scrap.find_val_article(url))
        Engine.repertory("Categories")
        self.csv.category_csv(self.list_category)  
        Engine.repertory("Pictures/"+ category_name)
        for val in self.list_category[category_name]:
             self.scrap.find_picture(val[2], val[9])

                        