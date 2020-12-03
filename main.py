from engine import Engine
from settings import *
import os


print(TITLE)
while True:
    os.chdir(parent_directory)
    cl = Engine()
    choix = (input("\n\n\nChoix : "))
    if choix not in ('0','1','2','3'):
        continue

    if choix == '1':
        cl.lunch_article_CSV_picture()

    if choix == '2':
        category_name = input("Veuillez entrer le nom de la catégorie: ") 
        cl.lunch_category_CSV_picture(category_name)
                                                                                                    
    if choix == '3':
         cl.lunch_category_CSV_picture('all')
                                                                                                
    if choix == '0':
       break       