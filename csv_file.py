import csv
import os
from settings import *

class Make_csv:

    def article_csv(self, list_val_article): 

        file_csv = list_val_article[2].replace('/','|') + '.csv'
        with open(file_csv,'w',encoding='latin1') as file:                                                           
                csvfile = csv.writer(file, delimiter=',')                                                                                                                  
                csvfile.writerow(CSV_HEADERS)
                csvfile.writerow(list_val_article)

    def category_csv(self, list_val): 
        
        for title in list_val.keys(): 
            file_csv = title.replace('/','|') + '.csv'
            with open(file_csv,'w',encoding='latin1') as file:                                                           
                    csvfile = csv.writer(file, delimiter=',')                                                                                                                  
                    csvfile.writerow(CSV_HEADERS)
                    for val in list_val[title]:
                        csvfile.writerow(val)