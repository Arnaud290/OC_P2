from csv_file import *
from scrap import Scrap
from settings import *
import os
class Engine:

    def __init__(self):
        self.article_name = ''
        self.url_article = ''
        self.list_val_article = []
        self.scrap = Scrap()
        self.csv = Make_csv()

    def title(self):
        print("Bonjour, bienvenue sur le programme de scraping du site https://books.toscrape.com,\n")
        print("        - Pour une recupération des informations sur un article, faites le 1\n\
        - Pour une recupération des informations sur une catégorie, faites le 2\n\
        - Pour une recupération des informations sur toutes les catégories faites le 3\n\
        - Pour quitter le programme, faites 0\n\n\nPour Chaque choix, les images des articles \
recherchés seront disponible dans le répertoire Images")

    def lunch_article_CSV_picture(self):
        self.article_name = input("Veuillez entrer le nom de l'article: ")                                                                     
        self.url_article = self.scrap.find_url_article(self.article_name)                                                                                                                                                                      
        self.list_val_article  = self.scrap.find_val_article(self.url_article)
        self.csv.article_csv(self.list_val_article)  
        self.scrap.picture(self.list_val_article)