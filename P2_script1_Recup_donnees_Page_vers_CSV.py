import requests
from bs4 import BeautifulSoup
import csv
import os

def recup_url_article(art):                                                                                                                                                                                      
    url = 'https://books.toscrape.com/index.html'                                                                   
    reponse = requests.get(url)                                                                                    
    if reponse.ok:                                                                                                 
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                            
        nb_pages = int((str(nb_pages)[10:]))                                                                         
    for i in range(1, nb_pages + 1):                                                                                
        url = 'http://books.toscrape.com/catalogue/page-' + str(i) + '.html'                                       
        reponse = requests.get(url)                                                                                 
        if reponse.ok:                                                                                              
            soup = BeautifulSoup(reponse.text,'lxml')                                                                             
            articles = soup.findAll("article")                                                                     
            for article in articles:                                                                               
                a = article.find('a')                                                                               
                link = ('http://books.toscrape.com/catalogue/'+ a['href'])                                                                                     
                reponse = requests.get(link)
                if reponse.ok:
                    soup = BeautifulSoup(reponse.text,'lxml')
                    title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
                    if str(title) == art:
                        return link
        else:                                                                                                          
            print("Veuillez entrer une adresse valide.")  
    print("Cette article n'est pas sur le site.")                                           
    
def recup_donnees_article_vers_csv(url):
    reponse = requests.get(url)                                                                                     # Récupération des données de la page
    if reponse.ok:                                                                                                  # Si la page est joignable    
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   # Récupération du texte de la page
        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text                                 # récupération du titre
        product_description= soup.find('article').find('p').find_next('p').find_next('p').find_next('p').text       # """récupération de la description
        tds = soup.findAll('td')                                                                                    # Création
        product_list=[]                                                                                             # d'une
        for td in tds:                                                                                              # liste
            product_list.append(td.text)                                                                            # d'informations"""
        image = soup.find('div',{'class':'item active'}).find('img')['src']                                         # """ récupération du 
        lien_image = 'http://books.toscrape.com/' + (str(image)[6:])                                                # lien de l'image"""
        categorie = soup.find('ul', {'class':'breadcrumb'}).find('a').find_next('a').find_next('a').text            # récupération de la catégorie          
        list_entete = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',         # """liste d'entetes 
        'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'] # du fichier csv"""
        list_valeurs = [url, product_list[0], title, product_list[3].strip('Â'), product_list[2].strip('Â'),        # """liste des valeurs
        product_list[5], product_description, categorie, product_list[6], lien_image]                               # du fichier csv"""
        file_csv = (str(title).replace('/','|') + '.csv')                                                           # Création du nom du fichier csv
        with open(file_csv,'w',encoding='latin1') as file:                                                          # Ouverture pour ecriture du fichier csv
            csvfile = csv.writer(file, delimiter=',')                                                               # Ajout du fichier csv dans une variable
            csvfile.writerow(list_entete)                                                                           # ecriture des entetes     
            csvfile.writerow(list_valeurs)                                                                          # ecriture des valeurs     
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")                                                                # message si le lien n'est pas valide


article = input("Veuillez entrer le nom de l'article: ")
url = recup_url_article(article)
if not os.path.exists('Articles'):
    os.makedirs('Articles')
os.chdir('Articles')
recup_donnees_article_vers_csv(url) 
print("Les données de l'article '{}' sont dans le fichier CSV dans le repertoire Articles".format(article))
