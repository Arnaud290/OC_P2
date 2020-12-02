import os

parent_directory = os.getcwd()  

CSV_HEADERS = ['product_page_url',
                'universal_ product_code (upc)',
                'title',
                'price_including_tax',         
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url'] 

TITLE = "\n\n\nBonjour, bienvenue sur le programme de scraping du site https://books.toscrape.com,\n\n\n\
- Pour une recupération des informations sur un article, faites le 1\n\
- Pour une recupération des informations sur une catégorie, faites le 2\n\
- Pour une recupération des informations sur toutes les catégories faites le 3\n\
- Pour quitter le programme, faites 0\n\n\nPour Chaque choix, les images des articles \
recherchés seront disponible dans le répertoire Images)"