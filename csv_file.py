"""Module for creating csv files"""
import csv
from settings import CSV_HEADERS
class MakeCsv:
    """Class for creating csv files"""
    @classmethod
    def article_csv(cls, list_val_article):
        """Attribute for creating a csv file for an article"""
        file_csv = list_val_article[2].replace('/','|') + '.csv'
        with open(file_csv,'w',encoding='latin1') as file:
            csvfile = csv.writer(file, delimiter=',')
            csvfile.writerow(CSV_HEADERS)
            csvfile.writerow(list_val_article)
    @classmethod
    def category_csv(cls, list_val):
        """Attribute for creating a csv file for one or more categories"""
        for title in list_val.keys():
            file_csv = title.replace('/','|') + '.csv'
            with open(file_csv,'w',encoding='latin1') as file:
                csvfile = csv.writer(file, delimiter=',')
                csvfile.writerow(CSV_HEADERS)
                for val in list_val[title]:
                    csvfile.writerow(val)
