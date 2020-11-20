import requests
from bs4 import BeautifulSoup
import csv
import os

def recup_url_article(art):         
    """
    Module de récupération du lien URL de l'article demandé
    """                                                                                                                                                                             
    url = 'https://books.toscrape.com/index.html'                                                                   
    reponse = requests.get(url)                                                                                         # récuprération du test sur l'index du site                                                                               
    if reponse.ok:                                                                                                 
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                     # récupération du nombre de pages                                                       
        nb_pages = int((str(nb_pages)[10:]))                                                                            # création d'un entier du nombre de pages
    else:                                                                                                          
        print("Veuillez entrer une adresse valide.")                                                                            
    for i in range(1, nb_pages + 1):                                                                                
        url = 'http://books.toscrape.com/catalogue/page-' + str(i) + '.html'                                       
        reponse = requests.get(url)                                                                                     # récupération du texte page par page                                                                          
        if reponse.ok:                                                                                              
            soup = BeautifulSoup(reponse.text,'lxml')                                                                             
            articles = soup.findAll("article")                                                                     
            for article in articles:                                                                               
                a = article.find('a')                                                                                   # récupération du nom de chaque articles                                                                             
                link = ('http://books.toscrape.com/catalogue/'+ a['href'])                                                                                     
                reponse = requests.get(link)
                if reponse.ok:
                    soup = BeautifulSoup(reponse.text,'lxml')
                    title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
                    if title == art:                                                                                    # si le nom de l'article correspond a l'article demandé
                        return link                                                                                     # le module retourne le lien correspondant à l'article
        else:                                                                                                          
            print("Veuillez entrer une adresse valide.")  
    print("Cette article n'est pas sur le site.")                                           
    
def recup_donnees_article_vers_csv(url):
    """
    Module perméttant de récupérer les données sur la page d'un article et de les inscrires 
    dans un fichier CSV
    """
    reponse = requests.get(url)                                                                                     
    if reponse.ok:                                                                                                     
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text                                     # récupération du titre de l'article                                
        product_description= soup.find('article').find('p').find_next('p').find_next('p').find_next('p').text           # récupération du résumé  
        tds = soup.findAll('td')                                                                                    
        product_list=[]                                                                                             
        for td in tds:                                                                                                  # mis dans une liste les informations provenant                                                                                        
            product_list.append(td.text)                                                                                # d'un tableau contenant le prix, les disponibilités...                                                                                                                                                        
        image = soup.find('div',{'class':'item active'}).find('img')['src']                                          
        lien_image = 'http://books.toscrape.com/' + (str(image)[6:])                                                
        categorie = soup.find('ul', {'class':'breadcrumb'}).find('a').find_next('a').find_next('a').text                      
        list_entete = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',         
        'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'] 
        list_valeurs = [url, product_list[0], title, product_list[3].strip('Â'), product_list[2].strip('Â'),        
        product_list[5], product_description, categorie, product_list[6], lien_image]                               
        file_csv = (str(title).replace('/','|') + '.csv')                                                           
        with open(file_csv,'w',encoding='latin1') as file:                                                          
            csvfile = csv.writer(file, delimiter=',')                                                                   # création du fichier CSV contenant un entête                                                
            csvfile.writerow(list_entete)                                                                               # et les informations 
            csvfile.writerow(list_valeurs)                                                                               
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")                                                               


article = input("Veuillez entrer le nom de l'article: ")                                                                # Demande à l'utilisateur d'entrer le nom d'un article
url = recup_url_article(article)                                                                                        # récupération du lien url de l'article
if not os.path.exists('Articles'):                                                                                      
    os.makedirs('Articles')                                                                                             # création d'un répartoire "Article" si il n'existe pas    
os.chdir('Articles')                                                                                                    # changement du repertoire pour l'execution du module
recup_donnees_article_vers_csv(url) 
print("Les données de l'article '{}' sont dans le fichier CSV dans le repertoire Articles".format(article))