import requests
from bs4 import BeautifulSoup
import csv
import os

repertoire_parent = os.getcwd()

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

def valeurs_articles(url):
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

def creation_repertoire(repertoire):
        if not os.path.exists(repertoire):                                                                                      
            os.makedirs(repertoire)                                                                                             # création d'un répartoire "Article" si il n'existe pas    
        os.chdir(repertoire)

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

def images(nom, lien_image):
    response = requests.get(lien_image)
    fichier_image = nom + '.jpg'
    file = open(fichier_image, 'wb')
    file.write(response.content)
    file.close()

def info_article_CSV():
    article = input("Veuillez entrer le nom de l'article: ")                                                               
    url = recup_url_article(article)                                                                                        
    creation_repertoire('Articles')                                                                                                
    list_valeurs = valeurs_articles(url) 
    file_csv = (str(article) + '.csv')
    with open(file_csv,'w',encoding='latin1') as file:                                                           
        csvfile = csv.writer(file, delimiter=',')                                                                                                                  
        csvfile.writerow(list_entete)                                                                                
        csvfile.writerow(list_valeurs)
    creation_repertoire('Images')
    images(article, list_valeurs[9])   
    print("Les données de l'article '{}' sont dans le fichier CSV dans le repertoire Articles".format(article))
        

def info_categorie_CSV():
    categorie = input("Veuillez entrer le nom de la catégorie : ") 
    url = recup_url_categorie(categorie)
    urls = recup_toutes_urls_articles_categorie(url)
    repertoire = 'Catégories'+'/'+ categorie
    creation_repertoire(repertoire)
    for url in urls :
        list_valeurs = valeurs_articles(url)
        file_csv = list_valeurs[2] + '.csv'
        with open(file_csv,'w',encoding='latin1') as file:                                                           
            csvfile = csv.writer(file, delimiter=',')                                                                                                                  
            csvfile.writerow(list_entete)                                                                                
            csvfile.writerow(list_valeurs)
    creation_repertoire('Images')
    for url in urls : 
        list_valeurs = valeurs_articles(url)
        images(list_valeurs[2], list_valeurs[9])


print("Bonjour, bienvenue sur le programme de scraping du site https://books.toscrape.com,\n")
print("    - Pour une recupération des informations sur un article, faite le 1\n\
    - Pour une recupération des informations sur une catégorie, faite le 2\n\
    - Pour quitter le programme, faites 0\n\n\n")




while True:
    os.chdir(repertoire_parent)
    choix = int(input("\n\n\nChoix : "))
    if choix == 1 :
        info_article_CSV() 
    if choix == 2 :
        info_categorie_CSV()  
    if choix == 0 :
        break 
        
    



