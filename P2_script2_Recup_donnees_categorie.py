import requests
from bs4 import BeautifulSoup
import csv
import os


def recup_url_categorie(cat):                                                                                               
    """                                             
    Module permettant de recuperer le lien d'une categorie
    """
    reponse = requests.get("https://books.toscrape.com/index.html")                                                         # récupération du texte sur l'index
    if reponse.ok: 
        soup = BeautifulSoup(reponse.text,'lxml')
        lis = soup.find('ul', {'class':'nav nav-list'}).find('li').find('ul').findAll('li')                                 # récupération des catégories
        for li in lis:
            if li.text.strip() == cat:
                a = li.find('a')                                                                              
                link = 'https://books.toscrape.com/'+a['href']                                                              
                return link                                                                                                 # retour du lien de la catégorie
        print("Cette catégorie n'existe pas")
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")     

def recup_toutes_urls_articles_categorie(url_categorie):  
    """
    Module permettant de recuperer les liens des articles sur une ou plusieurs pages
    """                                                                                 
    links = []                                                                                                              # variable liste des liens des articles de la catégorie                                                                                                                                                                    
    reponse = requests.get(url_categorie)                                                                                     
    if reponse.ok:                                                                                                  
        soup = BeautifulSoup(reponse.text,'lxml')                                                                
        articles = soup.findAll("article") 
        for article in articles:                                                                               
            a = article.find('a')                                                                              
            link = a['href']    
            links.append("https://books.toscrape.com/catalogue/"+ str(link)[9:])                                                
        try:
            nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                     # verification du nombre de pages 
        except:
            return links                                                                                                    # si il n'y a qu'une seul page, retour de la liste                                                                                                 
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
        return links                                                                                                        # retour de la liste de toutes les pages                                                          
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")   

def recup_donnees_url(url):
    """
    Module perméttant de récupérer les données sur la page d'un article et de les inscrires 
    dans un fichier CSV
    """
    reponse = requests.get(url)                                                                                     
    if reponse.ok:                                                                                                      
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text                                         # récupération du titre de l'article   
        product_description= soup.find('article').find('p').find_next('p').find_next('p').find_next('p').text               # récupération du résumé        
        tds = soup.findAll('td')                                                                                    
        product_list=[]                                                                                                                                       
        for td in tds:                                                                                                      # mis dans une liste les informations provenant  
            product_list.append(td.text)                                                                                    # d'un tableau contenant le prix, les disponibilités...    
        image = soup.find('div',{'class':'item active'}).find('img')['src']                                         
        lien_image = 'http://books.toscrape.com/' + (str(image)[6:])                                                
        categorie = soup.find('ul', {'class':'breadcrumb'}).find('a').find_next('a').find_next('a').text                      
        list_entete = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',         
        'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']      
        list_valeurs = [url, product_list[0], title, product_list[3].strip('Â'), product_list[2].strip('Â'),        
        product_list[5], product_description, categorie, product_list[6], lien_image]                               
        file_csv = (str(title).replace('/','|') + '.csv')                                                           
        with open(file_csv,'w',encoding='latin1') as file:                                                          
            csvfile = csv.writer(file, delimiter=',')                                                                       # création du fichier CSV contenant un entête                                                           
            csvfile.writerow(list_entete)                                                                                   # et les informations 
            csvfile.writerow(list_valeurs)                                                                             
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")                                                                

categorie = input(str("Veuillez entrer une catégorie : "))                                                                  # demande à l'utilisateur le nom d'une catégorie 
url_categorie = recup_url_categorie(categorie)                                                                              # lancement du module permettant d'obtenir le lien de la catégorie        
url_articles_categories = recup_toutes_urls_articles_categorie(url_categorie)                                               # lancement du module permettant la récupération des liens de articles    
path = 'Categories' + "/" + categorie                                                                                                   
if not os.path.exists(path):                                                                                                  
    os.makedirs(path)
os.chdir(path)                                                                                                              # création et accès au dossier "catégories"

for url in url_articles_categories:
    recup_donnees_url(url)                                                                                                  # création des fichiers CSV de chaques articles

print("Les informations consernant les articles de la categorie {} sont disponibles dans le repertoire {}.".format(categorie,path))