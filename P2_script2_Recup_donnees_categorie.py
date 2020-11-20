import requests
from bs4 import BeautifulSoup
import csv
import os


def recup_url_categorie(cat):
    reponse = requests.get("https://books.toscrape.com/index.html") 
    if reponse.ok: 
        soup = BeautifulSoup(reponse.text,'lxml')
        lis = soup.find('ul', {'class':'nav nav-list'}).find('li').find('ul').findAll('li')
        for li in lis:
            if li.text.strip() == cat:
                a = li.find('a')                                                                              
                link = 'https://books.toscrape.com/'+a['href'] 
                return link 
        print("Cette catégorie n'existe pas")
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")     

def recup_toutes_urls_articles_categorie(url_categorie):                                                                                   
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

def recup_donnees_url(url):
    reponse = requests.get(url)                                                                                     
    if reponse.ok:                                                                                                      
        soup = BeautifulSoup(reponse.text,'lxml')                                                                   
        title = soup.find('div', {'class':'col-sm-6 product_main'}).find('h1').text                                 
        product_description= soup.find('article').find('p').find_next('p').find_next('p').find_next('p').text       
        tds = soup.findAll('td')                                                                                    
        product_list=[]                                                                                            
        for td in tds:                                                                                              
            product_list.append(td.text)                                                                            
        image = soup.find('div',{'class':'item active'}).find('img')['src']                                         
        lien_image = 'http://books.toscrape.com/' + (str(image)[6:])                                                
        categorie = soup.find('ul', {'class':'breadcrumb'}).find('a').find_next('a').find_next('a').text                      
        list_entete = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',         
        'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'] 
        list_valeurs = [url, product_list[0], title, product_list[3].strip('Â'), product_list[2].strip('Â'),        
        product_list[5], product_description, categorie, product_list[6], lien_image]                               
        file_csv = (str(title).replace('/','|') + '.csv')                                                           
        with open(file_csv,'w',encoding='latin1') as file:                                                          
            csvfile = csv.writer(file, delimiter=',')                                                               
            csvfile.writerow(list_entete)                                                                               
            csvfile.writerow(list_valeurs)                                                                             
    else:                                                                                                           
        print("Veuillez entrer une adresse valide.")                                                                

categorie = input(str("Veuillez entrer une catégorie : "))
url_categorie = recup_url_categorie(categorie)
url_articles_categories = recup_toutes_urls_articles_categorie(url_categorie)
path = 'Categories' + "/" + categorie
if not os.path.exists(path):
    os.makedirs(path)
os.chdir(path)

for url in url_articles_categories:
    recup_donnees_url(url)

print("Les informations consernant les articles de la categorie {} sont disponibles dans le repertoire {}.".format(categorie,path))