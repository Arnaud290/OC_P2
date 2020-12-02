from csv_file import *
from scrap import Scrap
from settings import *
import os
class Engine:

    def __init__(self):
        self.list_val_article = []
        self.scrap = Scrap()
        self.csv = Make_csv()



    def lunch_article_CSV_picture(self):
        article_name = input("Veuillez entrer le nom de l'article: ")                                                                     
        url_article = self.scrap.find_url_article(article_name)                                                                                                                                                                
        self.list_val_article  = self.scrap.find_val_article(url_article)
        self.csv.article_csv(self.list_val_article)  
        self.scrap.find_picture(self.list_val_article)