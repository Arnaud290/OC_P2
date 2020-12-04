"""Launch module for creating csv and image files"""
from csv_file import MakeCsv
from find import Find
from picture import Picture
from repertory import Repertory
class Engine:
    """Launch class for creating csv and image files"""
    def __init__(self):
        self.find = Find()
        self.csv = MakeCsv()
        self.picture = Picture()
        self.repertory = Repertory()
    def lunch_article_csv_picture(self, article_name):
        """Csv and image file creation attribute for an article"""
        url_article = self.find.find_url_article(article_name)
        list_article = self.find.find_val_article(url_article)
        self.repertory.repertory("Articles")
        self.csv.article_csv(list_article)
        self.repertory.repertory("Articles/Pictures")
        self.picture.picture(list_article[2], list_article[9])
    def lunch_category_csv_picture(self, category_name):
        """Csv and image file creation attribute for an categories"""
        list_articles_category = {}
        list_url_category = {}
        list_url_category = self.find.find_all_category()
        for key in list_url_category:
            if category_name in (key, 'all'):
                links_article_category = self.find.find_all_urls_art_cat(list_url_category[key])
                list_articles_category[key] = []
                for url in links_article_category:
                    list_articles_category[key].append(self.find.find_val_article(url))
                self.repertory.repertory("Categories")
                self.csv.category_csv(list_articles_category)
                self.repertory.repertory("Categories/Pictures/"+ key)
                for val in list_articles_category[key]:
                    self.picture.picture(val[2], val[9])
