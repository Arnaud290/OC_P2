from engine import Engine
from settings import *
import os

cl = Engine()
print(TITLE)
while True:
    os.chdir(parent_directory)
    choix = (input("\n\n\nChoix : "))
    if choix not in ('0','1','2','3'):
        continue
    if choix == '1':
        cl.lunch_article_CSV_picture()

                                                                                                          
    #if choix == '2':
                                                                                                    
    #if choix == '3':
                                                                                                
    if choix == '0':
       break       