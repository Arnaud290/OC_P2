"""Module for creating csv files"""
import csv
import re
from classes.settings import CSV_HEADERS


class MakeCsv:
    """Class for creating csv files"""
    def __init__(self, list_val, article_title=None):
        self.list_val = list_val
        self.pattern = re.compile('[^A-Za-z0-9]')
        self.article_title = article_title
        self.csv()

    def csv(self):
        """Attribute for creating a csv file for an article or  an category """
        if isinstance(self.list_val, list):
            file_csv = self.article_title + '.csv'
            with open(file_csv, 'w', encoding='latin1') as file:
                csvfile = csv.writer(file, delimiter=',')
                csvfile.writerow(CSV_HEADERS)
                csvfile.writerow(self.list_val)
        else:
            for key in self.list_val:
                title = self.pattern.sub('_', key)
                file_csv = title[0:32] + '.csv'
                with open(file_csv, 'w', encoding='latin1') as file:
                    csvfile = csv.writer(file, delimiter=',')
                    csvfile.writerow(CSV_HEADERS)
                    for val in self.list_val[key]:
                        csvfile.writerow(val)
