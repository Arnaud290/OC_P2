import requests
from bs4 import BeautifulSoup
import csv
import os
from threading import Thread

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
    class Th_recup_url(Thread):   
        def __init__(self, art, i):
            Thread.__init__(self)
            self.art = art
            self.i = i
        def run(self):
            url = 'http://books.toscrape.com/catalogue/page-' + str(self.i) + '.html'                                       
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
                        if title == self.art: 
                            retour_url.append(link)                                                                                              
            else:                                                                                                          
                print("Veuillez entrer une adresse valide.")                                                                                                                                                            
    url = 'https://books.toscrape.com/index.html'                                                                   
    reponse = requests.get(url)                                                                                                                                                                      
    if reponse.ok:                                                                                                 
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        nb_pages = soup.find('li',{'class':'current'}).text.strip()                                                                                                          
        nb_pages = int((str(nb_pages)[10:]))                                                                            
    else:                                                                                                          
        print("Veuillez entrer une adresse valide.")   
    retour_url=[]
    t=dict()                                                       
    for i in range(0, nb_pages):
        t[i] = Th_recup_url(art,i+1)
        t[i].start()    
    for i in t:
        t[i].join()
    return retour_url[0]
                                            

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
    file_csv = str(list_valeurs[2]).replace('/','|') + '.csv' 
    with open(file_csv,'w',encoding='latin1') as file:                                                           
        csvfile = csv.writer(file, delimiter=',')                                                                                                                  
        csvfile.writerow(list_entete)                                                                                
        csvfile.writerow(list_valeurs)
    creation_repertoire('Images')
    images(str(list_valeurs[2]).replace('/','|'), list_valeurs[9])  
    print("Les données de l'article {} sont dans le fichier CSV dans le repertoire Articles".format(article))
        
def info_categorie_CSV():
    categorie = input("Veuillez entrer le nom de la catégorie : ") 
    url = recup_url_categorie(categorie)
    urls = recup_toutes_urls_articles_categorie(url)
    repertoire = 'Catégories'+'/'+ categorie
    creation_repertoire(repertoire)
    for url in urls :
        list_valeurs = valeurs_articles(url)
        file_csv = str(list_valeurs[2]).replace('/','|') + '.csv'
        with open(file_csv,'w',encoding='latin1') as file:                                                           
            csvfile = csv.writer(file, delimiter=',')                                                                                                                  
            csvfile.writerow(list_entete)                                                                                
            csvfile.writerow(list_valeurs)
    creation_repertoire('Images')
    for url in urls : 
        list_valeurs = valeurs_articles(url)
        images(str(list_valeurs[2]).replace('/','|'), list_valeurs[9])
    print("Les données des articles de la catégorie {} sont dans les fichiers CSV dans le repertoire {}.".format(categorie,repertoire))
    
def info_toutes_catgories_CSV():
    creation_repertoire('Toutes_Categories')
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
    for categorie in listCategory:
        file_csv = (str(categorie) + '.csv')
        with open(file_csv,'w',encoding='latin1') as file:                                                           
            csvfile = csv.writer(file, delimiter=',')                                                                                                                  
            csvfile.writerow(list_entete)
            listUrl = recup_toutes_urls_articles_categorie(listCategory[categorie])       
            for url in listUrl:
                list_valeurs = valeurs_articles(url)
                csvfile.writerow(list_valeurs)
        repertoire_Images =  'Images/' + categorie          
        creation_repertoire(repertoire_Images)
        for url in listUrl:
            list_valeurs = valeurs_articles(url)
            images(str(list_valeurs[2]).replace('/','|'), (list_valeurs[9]))
        repertoire = repertoire_parent + '/Toutes_Categories'
        os.chdir(repertoire)
    print("Les données des articles de toutes les catégories sont le repertoire Toutes_Categories.")

print("Bonjour, bienvenue sur le programme de scraping du site https://books.toscrape.com,\n")
print("    - Pour une recupération des informations sur un article, faites le 1\n\
    - Pour une recupération des informations sur une catégorie, faites le 2\n\
    - Pour une recupération des informations sur toutes les catégorie faites le 3\n\
    - Pour quitter le programme, faites 0\n\n\nPour Chaques choix, les images des articles\
recherchés seront disponble dans le repertoire Images")

while True:
    os.chdir(repertoire_parent)
    choix = (input("\n\n\nChoix : "))
    if choix not in ('0','1','2','3'):
        continue
    if choix == '1':
        info_article_CSV() 
    if choix == '2':
        info_categorie_CSV()  
    if choix == '3':
        info_toutes_catgories_CSV()
    if choix == '0':
        break