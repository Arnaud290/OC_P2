from engine import Engine
from settings import *
import os

class Menu:

    def lunch_menu(self):
        print(TITLE)
        while True:
            os.chdir(parent_directory)
            cl = Engine()
            choix = (input("\n\n\nChoix : "))
            if choix not in ('0','1','2','3'):
                continue
            if choix == '1':
                article_name = input("Please enter the article name: ")  
                cl.lunch_article_CSV_picture(article_name)
            if choix == '2':
                category_name = input("Please enter the category name: ") 
                cl.lunch_category_CSV_picture(category_name)                                                                                                  
            if choix == '3':
                cl.lunch_category_CSV_picture('all')                                                                                          
            if choix == '0':
                break       