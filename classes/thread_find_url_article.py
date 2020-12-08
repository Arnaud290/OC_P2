"""Article url search class module"""

from threading import Thread
from classes.scrap import Scrap
from classes.settings import URL


class ThreadFindUrlArticle(Thread):
    """Class in threading allowing the search
    for an article on several pages simultaneously"""
    def __init__(self, article_name, i):
        Thread.__init__(self)
        self.article_name = article_name
        self.i = i
        self.article_link = False
        self.scrap = Scrap()

    def run(self):
        url = URL + 'catalogue/page-' + str(self.i) + '.html'
        soup = self.scrap.scrap(url)
        articles = soup.findAll("article")
        for article in articles:
            url_article = article.find('a')
            url_article = (URL + 'catalogue/' + url_article['href'])
            soup = self.scrap.scrap(url_article)
            title = soup.find('div', {'class': 'col-sm-6 product_main'})
            title = title.find('h1').text
            if title == self.article_name:
                self.article_link = url_article

    def result(self):
        """Attribute for article link return"""
        return self.article_link
