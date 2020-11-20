
"""
links = []
for i in range(1, 51): 

    url = 'http://books.toscrape.com/catalogue/page-' + str(i) + '.html'
    reponse = requests.get(url)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text,'lxml')
        articles = soup.findAll("article")
        for article in articles:
            a = article.find('a')
            link = a['href']
            links.append('http://books.toscrape.com/catalogue/'+ link)        

print("il y a {} liens.".format(len(links)))

with open('urls.csv','w') as file:
    for link in links:
        file.write( link + '\n')

with open('urls.csv','r') as file:
    for row in file:
        print(row)

"""

"""
url = 'http://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html'
reponse = requests.get(url)
if reponse.ok:
    soup = BeautifulSoup(reponse.text,'lxml')
    ths = soup.findAll('th')
    tds = soup.findAll('td')
    with open('product.csv','w') as file:
        for th in ths:
            file.write(th.text + ',')
        file.write('\n')     
        for td in tds:
           file.write(td.text.strip('Â') + ',')

"""

"""
Categories 

listCategory=[]
url = 'https://books.toscrape.com/'
reponse = requests.get(url)
if reponse.ok:
    soup = BeautifulSoup(reponse.text,'lxml')
    lis = soup.find('ul', {'class':'nav nav-list'}).find('li').find('ul').findAll('li')
    with open('Category.csv','w') as file:
        for li in lis:
            listCategory.append(li.text.strip())
    print(listCategory)

"""


"""
Récupération des informations (product_page_url, universal_ product_code (upc),
title, price_including_tax, price_excluding_tax, number_available, product_description,
category, review_rating, image_url) dans un fichier CSV """


import requests
from bs4 import BeautifulSoup
import csv
import os

def recup_donnees_url(url):
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



def recup_toutes_urls_articles():                                                                                   
    links = []                                                                                                      # création de la variable liste "liens"
    url = 'https://books.toscrape.com/index.html'                                                                   
    reponse = requests.get(url)                                                                                     # récupération des données de la page principale    
    if reponse.ok:                                                                                                  # si le lien fonctionne...
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                 # récupération du nombres de pages            
        nb_pages=int((str(nb_pages)[10:]))                                                                          # modification de la variable pour obtenir un int     
    for i in range(1, nb_pages + 1):                                                                                # boucle pour recuperer les liens des articles sur toutes les pages           
        url = 'http://books.toscrape.com/catalogue/page-' + str(i) + '.html'                                        # créaction de la variable url en fonction de chaques pages    
        reponse = requests.get(url)                                                                                 # récupération des données
        if reponse.ok:                                                                                              # si le lien fonctionne....
            soup = BeautifulSoup(reponse.text,'lxml')                                                               # Récupération du texte de la page               
            articles = soup.findAll("article")                                                                      # récupération des liens des articles par page
            for article in articles:                                                                                # pour chaques lien...    
                a = article.find('a')                                                                               # """ inscription du lien 
                link = a['href']                                                                                    # dans la variable   
                links.append('http://books.toscrape.com/catalogue/'+ link)                                          # links """   
        else:                                                                                                           
            print("Veuillez entrer une adresse valide.")                                                            # retour si le lien n'est pas valide
    return links                                                                                                    # retour de la liste de liens     


def recup_toutes_urls_articles_categories(url_categorie):                                                                                   
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
                urlpage = str(url)[:-10]+'page-' + str(i) + '.html'
                print(urlpage) 
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



if not os.path.exists('Articles'):
    os.makedirs('Articles')
os.chdir('Articles')
liens = recup_toutes_urls_articles()
for lien in liens:
    recup_donnees_url(lien)







