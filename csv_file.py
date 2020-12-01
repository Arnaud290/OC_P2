import csv
import os
from settings import *

class Make_csv:

    def article_csv(self, list_val_article):
        if not os.path.exists("Articles"):                                                                                      
            os.makedirs("Articles")                                                                                             # création d'un répertoire si il n'existe pas    
        os.chdir("Articles")    
        file_csv = list_val_article[2] + '.csv' 
        with open(file_csv,'w',encoding='latin1') as file:                                                           
            csvfile = csv.writer(file, delimiter=',')                                                                                                                  
            csvfile.writerow(CSV_HEADERS)                                                                                       # inscription de l'entête dans le fichier CSV                                                                             
            csvfile.writerow(list_val_article)    
                     