import os

parent_directory = os.getcwd()  

url = 'http://books.toscrape.com/'

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

TITLE = "\n\n\nHello, welcome to the site's scraping program https://books.toscrape.com,\n\n\n\
- To retrieve information on an article, press 1\n\
- To retrieve information on a category, press 2\n\
- To retrieve information on all categories, press 3\n\
- To exit the program, press 0\n\n\nFor Each choice, the item pictures \
searched will be available in the Images directory"