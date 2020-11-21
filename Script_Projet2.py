import requests
from bs4 import BeautifulSoup
import csv
import os
from threading import Thread

repertoire_parent = os.getcwd()                                                                                             # Repertoire actuel

list_entete = ['product_page_url',
                'universal_ product_code (upc)',
                'title',
                'price_including_tax',         
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url'] 

def recup_url_article(article_recherche): 
    """
    Module permettant de récuperer l'adresse URL de l'article demandé
    """
    class Th_recup_url(Thread): 
        """
        Class de recherche d'une adresse URL d'un article par page
        cette classe s'execute en Threading
        """  
        def __init__(self, article_recherche, i):
            Thread.__init__(self)
            self.article_recherche = article_recherche
            self.i = i
        def run(self):
            url = 'http://books.toscrape.com/catalogue/page-' + str(self.i) + '.html'                                       # recherche sur le numéro de page demandé                                    
            reponse = requests.get(url)                                                                                                                                                             
            if reponse.ok:                                                                                              
                soup = BeautifulSoup(reponse.text,'lxml')                                                                             
                articles = soup.findAll("article")                                                                          # récupération des donnees des articles de la page                                                                        
                for article in articles:                                                                        
                    a = article.find('a')                                                                                                                                                                
                    link = ('http://books.toscrape.com/catalogue/'+ a['href'])                                                                                     
                    reponse = requests.get(link)
                    if reponse.ok:
                        soup = BeautifulSoup(reponse.text,'lxml')
                        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text
                        if title == self.article_recherche:                                                                 # si le nom de l'article verifié correspond à l'article demandé
                            retour_url.append(link)                                                                         # retour du lien de l'article                                                                                               
            else:                                                                                                          
                print("Veuillez entrer une adresse valide.")                                                                                                                                                            
    url = 'https://books.toscrape.com/index.html'                                                                   
    reponse = requests.get(url)                                                                                                                                                                      
    if reponse.ok:                                                                                                 
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                        # récupéraion du nombre de pages à parcourir                                                                                                                                                            
        nb_pages = int(nb_pages[10:])                                                                            
    else:                                                                                                          
        print("Veuillez entrer une adresse valide.")   
    retour_url = []
    t=dict()                                                       
    for i in range(0, nb_pages):
        t[i] = Th_recup_url(article_recherche, i+1)                                                                         # lancement de la class "Th_recup_url" pour chaques pages en simultanée
        t[i].start()    
    for i in t:
        t[i].join()                                                                                                         # fin de tout les lancements de la class "Th_recup_url"
    return retour_url[0]                                                                                                    # retour de l'adresse URL de l'article demandé                                                                                                                                                                                                       
                                            
def valeurs_articles(url_article_recherche):
    """
    module qui retourne la liste des informations d'un article
    """
    reponse = requests.get(url_article_recherche)                                                                                     
    if reponse.ok:                                                                                                      
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text                                         # récupération du titre                                     
        product_description= soup.find('article').find('p').find_next('p').find_next('p').find_next('p').text               # récupération du résumé
        categorie = soup.find('ul', {'class':'breadcrumb'}).find('a').find_next('a').find_next('a').text                    # récupération de la categorie           
        tds = soup.findAll('td')                                                                                    
        product_list=[]                                                                                                                                       
        for td in tds:                                                                                                       
            product_list.append(td.text)                                                                                    # mis dans la liste "product_list" les informations dans un tableau (prix...)                                                                                 
        image = soup.find('div',{'class':'item active'}).find('img')['src']                                         
        lien_image = 'http://books.toscrape.com/' + (image[6:])                                                             # récupération du lien de l'image de l'article                                                                    
        list_valeurs = [url_article_recherche, product_list[0], title, product_list[3].strip('Â'), product_list[2].strip('Â'),        
        product_list[5], product_description, categorie, product_list[6], lien_image]                                       # création de la liste contenant toutes les informations
        return list_valeurs                                                                                                 # retour de la liste
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.") 

def creation_repertoire(repertoire):
    """
    Module permettant de créer et de rentrer dans un repertoire
    """
    if not os.path.exists(repertoire):                                                                                      
        os.makedirs(repertoire)                                                                                             # création d'un répartoire si il n'existe pas    
    os.chdir(repertoire)                                                                                                    # accès au repertoire

def recup_url_categorie(categorie_recherche):                                                                                               
    """                                             
    Module permettant de recuperer le lien d'une categorie
    """
    reponse = requests.get("https://books.toscrape.com/index.html")                                                         # récupération du texte sur l'index
    if reponse.ok: 
        soup = BeautifulSoup(reponse.text,'lxml')
        lis = soup.find('ul', {'class':'nav nav-list'}).find('li').find('ul').findAll('li')                                 # récupération des catégories
        for li in lis:
            if li.text.strip() == categorie_recherche:
                a = li.find('a')                                                                              
                link = 'https://books.toscrape.com/'+a['href']                                                              
                return link                                                                                                 # retour du lien de la catégorie
        print("Cette catégorie n'existe pas")
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")   

def recup_toutes_urls_articles_categorie(url_categorie):  
    """
    Module permettant de recuperer les liens des articles sur 
    une ou plusieurs pages d'une catégorie
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
            return links                                                                                                    # si il n'y a qu'une seule page, retour de la liste                                                                                                 
        else:
            nb_pages = int(nb_pages[10:])
            for i in range(2, nb_pages + 1):
                urlpage = url_categorie[:-10] + 'page-' + str(i) + '.html'
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

def images(nom, lien_image):
    """
    Module permettant le téléchargement des images
    """
    response = requests.get(lien_image)                                                                                     # récupération des données du lien de l'image
    fichier_image = nom + '.jpg'                                                                                            # création du nom du fichier image
    file = open(fichier_image, 'wb')
    file.write(response.content)                                                                                            # recopie de l'image en local                         
    file.close()                                                                                                            # fermeture du fichier image

def info_article_CSV():
    """
    Module de lancement " récupération des informations
    d'un article demandé et mis dans un fichier CSV
    """
    article = input("Veuillez entrer le nom de l'article: ")                                                                # demande à l'utilisateur d'inscrire le nom d'un article                                                              
    url = recup_url_article(article)                                                                                        # récupération de l'adresse URL de l'article demandé                                                                                     
    creation_repertoire('Articles')                                                                                         # création d'un répertoire "Article" et accès au repertoire                                                                                                 
    list_valeurs = valeurs_articles(url) 
    file_csv = list_valeurs[2].replace('/','|') + '.csv'                                                                    # création du nom du fichier CSV
    with open(file_csv,'w',encoding='latin1') as file:                                                           
        csvfile = csv.writer(file, delimiter=',')                                                                                                                  
        csvfile.writerow(list_entete)                                                                                       # inscription de l'entête dans le fichier CSV                                                                             
        csvfile.writerow(list_valeurs)                                                                                      # inscription des valeurs dans le fichier CSV
    creation_repertoire('Images')                                                                                           # création d'un répertoire "Article" et accès au repertoire             
    images(list_valeurs[2].replace('/','|'), list_valeurs[9])                                                               # téléchargement de l'image de l'article 
    print("\n\n\nLes données de l'article {} sont dans le fichier CSV dans le repertoire Articles".format(article))
        
def info_categorie_CSV():
    """
    Module de lancement " récupération des informations
    d'une catégorie demandée et inscription des données de
    chaques articles dans un fichier CSV
    """
    categorie = input("Veuillez entrer le nom de la catégorie : ")                                                      # demande à l'utilisateur le nom d'une catégorie
    url = recup_url_categorie(categorie)                                                                                # récupération du lien de la catégorie
    urls = recup_toutes_urls_articles_categorie(url)                                                                    # récupération des liens des articles de la catégore
    repertoire = 'Catégories'+'/'+ categorie                                        
    creation_repertoire(repertoire)                                                                                     # création d'un répertoire "Catégorie" et d'un sous répertoire avec le nom de la catégorie
    for url in urls :
        list_valeurs = valeurs_articles(url)                                                                            # récupération des informatiosn de s chaques articles 
        file_csv = list_valeurs[2].replace('/','|') + '.csv'
        with open(file_csv,'w',encoding='latin1') as file:                                                              # création d'un fichier CSV par article                                                         
            csvfile = csv.writer(file, delimiter=',')                                                                                                                  
            csvfile.writerow(list_entete)                                                                                
            csvfile.writerow(list_valeurs)
    creation_repertoire('Images')                                                                                       # création d'un repertoire Image 
    for url in urls : 
        list_valeurs = valeurs_articles(url)
        images(list_valeurs[2].replace('/','|'), list_valeurs[9])                                                       # téléchargement des images de chaques articles
    print("\n\n\nLes données des articles de la catégorie {} sont dans les fichiers CSV dans le repertoire {}.".format(categorie,repertoire))
    
def info_toutes_catgories_CSV():
    """
    Module de lancement " récupération des informations
    de toutes les catégories du site et inscription des données de
    chaques articles dans un fichier CSV par catégorie
    """ 
    creation_repertoire('Toutes_Categories')                                                                                # création d'un répertoire "Toutes_catégories"                                    
    listCategory=dict()                                                                                                     # Dictionnaire qui va stocker le nom des catégories et les adresses URLs
    url = 'https://books.toscrape.com/'
    reponse = requests.get(url)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text,'lxml')
        lis = soup.find('ul', {'class':'nav nav-list'}).find('li').find('ul').findAll('li')                                 # récupération des informations des catégories
        for li in lis:
            categorie = li.text.strip()
            a = li.find('a')                                                                              
            link = 'https://books.toscrape.com/'+a['href']  
            listCategory[li.text.strip()] = link                                                                            # inscription du (nom = lien) pour chaques catégories 
    for categorie in listCategory:                                                                                          # création d'un fichiers CVS pour les informations des articles
        file_csv = categorie + '.csv'
        with open(file_csv,'w',encoding='latin1') as file:                                                                                                                           
            csvfile = csv.writer(file, delimiter=',')                                                                                                                  
            csvfile.writerow(list_entete)
            listUrl = recup_toutes_urls_articles_categorie(listCategory[categorie])                                         # récupération des liens des articles pour chaques catégories     
            for url in listUrl:
                list_valeurs = valeurs_articles(url)                                                                        # récupération des informations des articles
                csvfile.writerow(list_valeurs)                                                                              # inscription des informations dans le fichier CSV
        repertoire_Images = 'Images/' + categorie                                                                           # création d'un repertoire Image et d'un sous répertoire du nom de chaque catégories          
        creation_repertoire(repertoire_Images)
        for url in listUrl:
            list_valeurs = valeurs_articles(url)
            images(list_valeurs[2].replace('/','|'), (list_valeurs[9]))                                                     # téléchargement des images
        repertoire = repertoire_parent + '/Toutes_Categories'
        os.chdir(repertoire)                                                                                                # retour au répertoire "Toutes_catégories"
    print("\n\n\nLes données des articles de toutes les catégories sont le repertoire Toutes_Categories.")

print("Bonjour, bienvenue sur le programme de scraping du site https://books.toscrape.com,\n")
print("    - Pour une recupération des informations sur un article, faites le 1\n\
    - Pour une recupération des informations sur une catégorie, faites le 2\n\
    - Pour une recupération des informations sur toutes les catégorie faites le 3\n\
    - Pour quitter le programme, faites 0\n\n\nPour Chaques choix, les images des articles\
recherchés seront disponble dans le repertoire Images")

while True:
    """
    Boucle de lancement des modules
    """
    os.chdir(repertoire_parent)
    choix = (input("\n\n\nChoix : "))
    if choix not in ('0','1','2','3'):
        continue
    if choix == '1':
        info_article_CSV()                                                                                                  # Module récupération article
    if choix == '2':
        info_categorie_CSV()                                                                                                # Module récupération catégorie
    if choix == '3':
        info_toutes_catgories_CSV()                                                                                         # module réupération de toutes les catégories
    if choix == '0':
        break                                                                                                               # arret du programme