from csv_file import *
from find import Find
from settings import *
from picture import Picture
from repertory import Repertory
class Engine:

    def __init__(self):
        self.find = Find()
        self.csv = Make_csv()
        self.list_category = {}
        self.list_article = []
        self.picture = Picture()
        self.repertory = Repertory()
      
    def lunch_article_CSV_picture(self, article_name):                                                                   
        url_article = self.find.find_url_article(article_name)                                                                                                                                                                
        self.list_article = self.find.find_val_article(url_article)
        self.repertory.repertory("Articles")
        self.csv.article_csv(self.list_article)  
        self.repertory.repertory("Articles/Pictures")
        self.picture.picture(self.list_article[2],self.list_article[9])

    def lunch_category_CSV_picture(self, category_name):
        list_url_category = {}
        list_url_category = self.find.find_all_category()
        for name in list_url_category.keys():
            if category_name == name or category_name == 'all': 
                links_article_category = self.find.find_all_urls_articles_category(list_url_category[name])
                self.list_category[name] = []
                for url in links_article_category:
                    self.list_category[name].append(self.find.find_val_article(url))  
                self.repertory.repertory("Categories")
                self.csv.category_csv(self.list_category)  
                self.repertory.repertory("Categories/Pictures/"+ name)
                for val in self.list_category[name]:
                    self.picture.picture(val[2], val[9])                    