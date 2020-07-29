import sys

import requests
from bs4 import BeautifulSoup


class Parser:

    def __init__(self, url):
        try:
            r = requests.get(url)
            self.page = BeautifulSoup(r.content, "html.parser")
        except:
            e = sys.exc_info()[0]
            print('Error, while HTTP request: \n', e)

    def svenska_filter(self, url):
        try:
            filter_results = self.page.find("div", {"class": "grid flex__grid"})
            houses = filter_results.find_all("a", {"class": "search-hit__link"})
            return [url + str(house['href'] + '\n') for house in houses if str(house['href'])[-1].isdigit()]
        except:
            e = sys.exc_info()[0]
            print('Error, in Svenska filter: \n', e)

    def era_filter(self, url):
        try:
            filter_results = self.page.find("ul", {"class": "extended items"})
            houses = filter_results.find_all("a")
            return [url + str(house['href'] + '\n') for house in houses]
        except:
            e = sys.exc_info()[0]
            print('Error, in Svenska filter: \n', e)

    @staticmethod
    def update_db(results, file_path):
        try:
            with open(file_path, 'w') as file:
                for link in results:
                    file.write(link)
        except:
            e = sys.exc_info()[0]
            print('Error, cannot write to DB file:\n', e)

    @staticmethod
    def read_db(file_path):
        try:
            with open(file_path, 'r') as file:
                return file.readlines()
        except:
            e = sys.exc_info()[0]
            print('Error, cannot read to DB file:\n', e)


def compare_results_with_db(site_filter, db_read):
    return list(set(site_filter) - set(db_read))
