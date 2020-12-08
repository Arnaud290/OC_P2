"""Element search module"""
from classes.thread_find_url_article import ThreadFindUrlArticle
from classes.settings import URL
from classes.scrap import Scrap


class Find:
    """Element search class"""
    def __init__(self):
        self.list_val_article = []
        self.result_url_article = []
        self.list_url_category = {}
        self.scrap = Scrap()

    def find_url_article(self, article_name):
        """Attribute to find a url of an article"""
        soup = self.scrap.scrap(URL)
        nb_pages = soup.find('li', {'class': 'current'}).text.strip()
        nb_pages = int(nb_pages[10:])
        return_th = dict()
        for i in range(nb_pages):
            return_th[i] = ThreadFindUrlArticle(article_name, i + 1)
            return_th[i].start()
        for i in return_th:
            return_th[i].join()
            if return_th[i].result():
                url_article = return_th[i].result()
        return url_article

    def find_val_article(self, article_url):
        """Attribute to find article information"""
        soup = self.scrap.scrap(article_url)
        title = soup.find('div', {'class': 'col-sm-6 product_main'})
        title = title.find('h1').text
        description = soup.find('article', {'class': 'product_page'})
        description = description.findChildren('p', recursive=False)
        try:
            description = description[0].text
        except IndexError:
            description = ''
        categorie = soup.find('ul', {'class': 'breadcrumb'})
        categorie = categorie.findChildren('a')[2].text
        table = soup.findAll('td')
        product_list = []
        for cell in table:
            product_list.append(cell.text)
        image = soup.find('div', {'class': 'item active'}).find('img')['src']
        lien_image = URL + (image[6:])
        self.list_val_article = [
                                article_url,
                                product_list[0],
                                title,
                                product_list[3].strip('Â'),
                                product_list[2].strip('Â'),
                                product_list[5],
                                description,
                                categorie,
                                product_list[6],
                                lien_image
                                ]
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
                links.append(URL + "catalogue/" + str(link)[9:])
        soup = self.scrap.scrap(url_category)
        try:
            nb_pages = soup.find('li', {'class': 'current'}).text.strip()
        except AttributeError:
            find_links_articles(url_category)
            return links
        else:
            nb_pages = int(nb_pages[10:])
            for i in range(1, nb_pages + 1):
                more_pages = url_category[:-10] + 'page-' + str(i) + '.html'
                find_links_articles(more_pages)
            return links

    def find_all_category(self):
        """Attribute to find url addresses of all categories"""
        soup = soup = self.scrap.scrap(URL)
        categories = soup.find('ul', {'class': 'nav nav-list'})
        categories = categories.find('li')
        categories = categories.find('ul')
        categories = categories.findAll('li')
        for category in categories:
            categorie_name = category.text.strip()
            categorie_link = category.find('a')
            categorie_link = URL + categorie_link['href']
            self.list_url_category[categorie_name] = categorie_link
        return self.list_url_category
