"""Element search module"""
from threading import Thread
from settings import URL
from scrap import Scrap
class ThFindUrlArticle(Thread):
    """Class in threading allowing the search for an article on several pages simultaneously"""
    def __init__(self, article_name, i):
        Thread.__init__(self)
        self.article_name = article_name
        self.i = i
        self.article_link = False
        self.scrap = Scrap()
    def run(self):
        soup = self.scrap.scrap(URL + 'catalogue/page-' + str(self.i) + '.html')
        articles = soup.findAll("article")
        for article in articles:
            url_article = article.find('a')
            url_article = (URL + 'catalogue/'+ url_article['href'])
            soup = self.scrap.scrap(url_article)
            title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
            if title == self.article_name:
                self.article_link = url_article
    def result(self):
        """Attribute for article link return"""
        return self.article_link
class Find:
    """Element search class"""
    def __init__(self):
        self.list_val_article = []
        self.result_url_article = []
        self.list_url_category  = {}
        self.scrap = Scrap()
    def find_url_article(self, article_name):
        """Attribute to find a url of an article"""
        soup = self.scrap.scrap(URL)
        nb_pages = soup.find('li',{'class':'current'}).text.strip()
        nb_pages = int(nb_pages[10:])
        return_th = dict()
        for i in range(nb_pages):
            return_th[i] = ThFindUrlArticle(article_name, i + 1)
            return_th[i].start()
        for i in return_th:
            return_th[i].join()
            if return_th[i].result():
                url_article = return_th[i].result()
        return url_article
    def find_val_article(self, article_url):
        """Attribute to find article information"""
        soup = self.scrap.scrap(article_url)
        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
        product_description = soup.find('article')
        product_description = product_description.find('p')
        product_description = product_description.find_next('p')
        product_description = product_description.find_next('p')
        product_description = product_description.find_next('p').text
        categorie = soup.find('ul', {'class':'breadcrumb'})
        categorie = categorie.find('a')
        categorie = categorie.find_next('a')
        categorie = categorie.find_next('a').text
        table = soup.findAll('td')
        product_list=[]
        for cell in table:
            product_list.append(cell.text)
        image = soup.find('div',{'class':'item active'}).find('img')['src']
        lien_image = URL + (image[6:])
        self.list_val_article = [article_url,
        product_list[0],
        title.replace('/','|'),
        product_list[3].strip('Â'),
        product_list[2].strip('Â'),
        product_list[5],
        product_description,
        categorie,
        product_list[6],
        lien_image]
        return self.list_val_article
    def find_all_urls_art_cat(self, url_category):
        """Attribute to find url addresses of all articles in all categories"""
        links = []
        def find_links_articles(url_category):
            soup = self.scrap.scrap(url_category)
            articles = soup.findAll("article")
            for article in articles:
                article = article.find('a')
                link = article['href']
                links.append(URL +"catalogue/"+ str(link)[9:])
        soup = self.scrap.scrap(url_category)
        try:
            nb_pages = soup.find('li',{'class':'current'}).text.strip()
        except AttributeError:
            find_links_articles(url_category)
            return links
        else:
            nb_pages = int(nb_pages[10:])
            for i in range(1, nb_pages + 1):
                url_category_more_pages = url_category[:-10] + 'page-' + str(i) + '.html'
                find_links_articles(url_category_more_pages)
            return links
    def find_all_category(self):
        """Attribute to find url addresses of all categories"""
        soup = soup = self.scrap.scrap(URL)
        categories = soup.find('ul', {'class':'nav nav-list'}).find('li').find('ul').findAll('li')
        for category in categories:
            categorie_name = category.text.strip()
            categorie_link = category.find('a')
            categorie_link = URL + categorie_link['href']
            self.list_url_category[categorie_name] = categorie_link
        return self.list_url_category
