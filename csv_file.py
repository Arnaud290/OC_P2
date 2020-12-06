"""Module for creating csv files"""
import csv
from settings import CSV_HEADERS


class MakeCsv:
    """Class for creating csv files"""
    def __init__(self, list_val):
        self.list_val = list_val
        self.csv()

    def csv(self):
        """Attribute for creating a csv file for an article or  an category """
        if isinstance(self.list_val, list):
            file_csv = self.list_val[2].replace('/', '|') + '.csv'
            with open(file_csv, 'w', encoding='latin1') as file:
                csvfile = csv.writer(file, delimiter=',')
                csvfile.writerow(CSV_HEADERS)
                csvfile.writerow(self.list_val)
        else:
            for key in self.list_val:
                file_csv = key.replace('/', '|') + '.csv'
                with open(file_csv, 'w', encoding='latin1') as file:
                    csvfile = csv.writer(file, delimiter=',')
                    csvfile.writerow(CSV_HEADERS)
                    for val in self.list_val[key]:
                        csvfile.writerow(val)
