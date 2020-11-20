import requests
from bs4 import BeautifulSoup
import csv
import os


def recup_liste_urls_categories():

    """
    Récupération des catégories et leurs liens dans un dictionnaire
    """
    listCategory=dict()
    url = 'https://books.toscrape.com/'
    reponse = requests.get(url)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text,'lxml')
        lis = soup.find('ul', {'class':'nav nav-list'}).find('li').find('ul').findAll('li')
        for li in lis:
            categorie = li.text.strip()
            a = li.find('a')                                                                              
            link = 'https://books.toscrape.com/'+a['href']  
            listCategory[li.text.strip()] = link
        return listCategory

def recup_toutes_urls_articles_categorie(url_categorie):  
    """
    Module permettant de recuperer les liens des articles sur une ou plusieurs pages
    """                                                                                 
    links = []                                                                                                                                                                                                                                                                                  
    reponse = requests.get(url_categorie)                                                                                     
    if reponse.ok:                                                                                                  
        soup = BeautifulSoup(reponse.text,'lxml')                                                                
        articles = soup.findAll("article") 
        for article in articles:                                                                               
            a = article.find('a')                                                                              
            link = a['href']    
            links.append("https://books.toscrape.com/catalogue/"+ str(link)[9:])                                                
        try:
            nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                     
        except:
            return links                                                                                                                                                                                                     
        else:
            nb_pages = int((str(nb_pages)[10:]))
            for i in range(2, nb_pages + 1):
                urlpage = str(url_categorie)[:-10] + 'page-' + str(i) + '.html'
                reponse = requests.get(urlpage)
                if reponse.ok:  
                    soup = BeautifulSoup(reponse.text,'lxml') 
                    articles = soup.findAll("article")  
                    for article in articles:                                                                               
                        a = article.find('a')                                                                              
                        link = a['href']    
                        links.append("https://books.toscrape.com/catalogue/"+ str(link)[9:])  
                else:                                                                                                           
                    print("Veuillez entrer une adresse valide.") 
        return links                                                                                                                                                                 
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")   

def valeurs_articles_catégorie(url):
    """
    module qui retourne la liste des informations d'une page
    """
    reponse = requests.get(url)                                                                                     
    if reponse.ok:                                                                                                      
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text                                         
        product_description= soup.find('article').find('p').find_next('p').find_next('p').find_next('p').text  
        categorie = soup.find('ul', {'class':'breadcrumb'}).find('a').find_next('a').find_next('a').text              
        tds = soup.findAll('td')                                                                                    
        product_list=[]                                                                                                                                       
        for td in tds:                                                                                                       
            product_list.append(td.text)                                                                                    
        image = soup.find('div',{'class':'item active'}).find('img')['src']                                         
        lien_image = 'http://books.toscrape.com/' + (str(image)[6:])                                                                     
        list_valeurs = [url, product_list[0], title, product_list[3].strip('Â'), product_list[2].strip('Â'),        
        product_list[5], product_description, categorie, product_list[6], lien_image]  
        return list_valeurs
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.") 

if not os.path.exists('Categories_info'):                                                                                                  
    os.makedirs('Categories_info')
os.chdir('Categories_info')                                                                                                     # création et accés au répertoire 'Categories_info'
listeCategories = recup_liste_urls_categories()
list_entete = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',         
                'price_excluding_tax', 'number_available', 'product_description','category' , 'review_rating', 'image_url']     # Création de la liste d'entêtes
for categorie in listeCategories:
    listUrl = recup_toutes_urls_articles_categorie(listeCategories[categorie])                                                  # récupération des liens d'articles de chaques catégories
    file_csv = (str(categorie) + '.csv')  
    with open(file_csv,'w',encoding='latin1') as file: 
        csvfile = csv.writer(file, delimiter=',')                                                                                                                           
        csvfile.writerow(list_entete)    
        for url in listUrl:
            list_valeurs = valeurs_articles_catégorie(url)                                                                
            csvfile.writerow(list_valeurs)                                                                                      # inscription des valeurs de chaques articles dans le fichier CSV
print("Récupération des informations en fonction des catégories effecutée. Les fichiers CSV sont dans le répertoire Categories_info.")