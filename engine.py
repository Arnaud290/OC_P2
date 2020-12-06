"""Launch module for creating csv and image files"""
import os
from csv_file import MakeCsv
from find import Find
from picture import Picture
from repertory import Repertory
from settings import TITLE, parent_directory


class Engine:
    """Launch class for creating csv and image files"""
    def __init__(self):
        self.find = Find()
        self.lunch_menu()

    def lunch_article_csv_picture(self, article_name):
        """Csv and image file creation attribute for an article"""
        url_article = self.find.find_url_article(article_name)
        list_article = self.find.find_val_article(url_article)
        Repertory("Articles")
        MakeCsv(list_article)
        Repertory("Articles/Pictures")
        Picture(list_article[2], list_article[9])

    def lunch_category_csv_picture(self, category_name):
        """Csv and image file creation attribute for an categories"""
        list_art_cat = {}
        list_url_cat = {}
        list_url_cat = self.find.find_all_category()
        for key in list_url_cat:
            if category_name in (key, 'all'):
                links = self.find.find_all_urls_art_cat(list_url_cat[key])
                list_art_cat[key] = []
                for url in links:
                    list_art_cat[key].append(self.find.find_val_article(url))
                Repertory("Categories")
                MakeCsv(list_art_cat)
                Repertory("Categories/Pictures/" + key)
                for val in list_art_cat[key]:
                    Picture(val[2], val[9])

    def lunch_menu(self):
        """Sequencer attribute"""
        print(TITLE)
        while True:
            os.chdir(parent_directory)
            choice = (input("\n\n\nChoix : "))
            if choice not in ('0', '1', '2', '3'):
                continue
            if choice == '1':
                article_name = input("Please enter the article name: ")
                self.lunch_article_csv_picture(article_name)
            if choice == '2':
                category_name = input("Please enter the category name: ")
                self.lunch_category_csv_picture(category_name)
            if choice == '3':
                self.lunch_category_csv_picture('all')
            if choice == '0':
                break
