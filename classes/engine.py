"""Launch module for creating csv and image files"""
import os
import re
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
        self.pattern = re.compile('[^A-Za-z0-9]')
        self.launch_menu()

    def launch_article_csv_picture(self, article_name):
        """Csv and image file creation attribute for an article"""
        url_article = []
        url_article = self.find.find_url_article(article_name)
        for i in range(len(url_article)):
            os.chdir(self.parent_directory)
            Repertory("Articles")
            list_article = self.find.find_val_article(url_article[i])
            title = list_article[2][0:32]
            title = self.pattern.sub('_', title)
            if i > 0:
                title = title + '-' + str(i)
            MakeCsv(list_article, title)
            Repertory("Pictures")
            Picture(title, list_article[9])

    def launch_category_csv_picture(self, category_name):
        """Csv and image file creation attribute for an categories"""
        list_art_cat = {}
        list_url_cat = {}
        list_url_cat = self.find.find_all_category()
        for key in list_url_cat:
            picture_title_list = []
            name = self.pattern.sub('', key).lower()
            if category_name in (name, 'all'):
                links = self.find.find_all_urls_art_cat(list_url_cat[key])
                list_art_cat[key] = []
                for url in links:
                    list_art_cat[key].append(self.find.find_val_article(url))
                os.chdir(self.parent_directory)
                Repertory("Categories")
                MakeCsv(list_art_cat)
                title = self.pattern.sub('_', key)
                Repertory("Pictures/" + title[0:32])
                for val in list_art_cat[key]:
                    title = val[2]
                    title = self.pattern.sub('_', title)[0:32]
                    if title in picture_title_list:
                        title = title + '-1'
                    Picture(title, val[9])
                    picture_title_list.append(title)

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
                article_name = self.pattern.sub('', article_name).lower()
                self.launch_article_csv_picture(article_name)
            if choice == '2':
                category_name = input("Please enter the category name: ")
                category_name = self.pattern.sub('', category_name).lower()
                self.launch_category_csv_picture(category_name)
            if choice == '3':
                self.launch_category_csv_picture('all')
            if choice == '0':
                break
