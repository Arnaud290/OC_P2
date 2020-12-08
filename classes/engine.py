"""Launch module for creating csv and image files"""
import os
from classes.make_csv import MakeCsv
from classes.find import Find
from classes.picture import Picture
from classes.repertory import Repertory
from classes.settings import TITLE


class Engine:
    """Launch class for creating csv and image files"""
    def __init__(self):
        self.find = Find()
        self.parent_directory = os.getcwd()
        self.launch_menu()

    def launch_article_csv_picture(self, article_name):
        """Csv and image file creation attribute for an article"""
        url_article = self.find.find_url_article(article_name)
        list_article = self.find.find_val_article(url_article)
        Repertory("Articles")
        MakeCsv(list_article)
        Repertory("Pictures")
        title = list_article[2].replace('/', '_')
        title = title.replace(':', '_').replace(".", '_')
        Picture(title, list_article[9])

    def launch_category_csv_picture(self, category_name):
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
                os.chdir(self.parent_directory)
                Repertory("Categories")
                MakeCsv(list_art_cat)
                Repertory("Pictures/" + key)
                for val in list_art_cat[key]:
                    title = val[2].replace('/', '_')
                    title = title.replace(':', '_').replace(".", '_')
                    Picture(title, val[9])

    def launch_menu(self):
        """Sequencer attribute"""
        print(TITLE)
        while True:
            os.chdir(self.parent_directory)
            choice = (input("\n\n\nChoix : "))
            if choice not in ('0', '1', '2', '3'):
                continue
            if choice == '1':
                article_name = input("Please enter the article name: ")
                self.launch_article_csv_picture(article_name)
            if choice == '2':
                category_name = input("Please enter the category name: ")
                self.launch_category_csv_picture(category_name)
            if choice == '3':
                self.launch_category_csv_picture('all')
            if choice == '0':
                break
