"""Program launch module"""
import os
from engine import Engine
import settings
class Menu:
    """Class launch module"""
    @classmethod
    def lunch_menu(cls):
        """Sequencer attribute"""
        print(settings.TITLE)
        while True:
            os.chdir(settings.parent_directory)
            class_engine = Engine()
            choix = (input("\n\n\nChoix : "))
            if choix not in ('0','1','2','3'):
                continue
            if choix == '1':
                article_name = input("Please enter the article name: ")
                class_engine.lunch_article_csv_picture(article_name)
            if choix == '2':
                category_name = input("Please enter the category name: ")
                class_engine.lunch_category_csv_picture(category_name)
            if choix == '3':
                class_engine.lunch_category_csv_picture('all')
            if choix == '0':
                break
