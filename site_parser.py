import sys

import requests
from bs4 import BeautifulSoup


class Parser:

    def __init__(self, url):
        try:
            self.url = url
            self.r = requests.get(self.url)
            self.page = BeautifulSoup(self.r.content, "html.parser")
        except:
            e = sys.exc_info()[0]
            print('Error, while HTTP request: \n', e)

    def main_filter(self):
        try:
            if 'svenskfast' in self.url:
                return self.svenska_filter()
            elif 'erasweden' in self.url:
                return self.era_filter()
            elif 'lansfast' in self.url:
                return self.lansfast_filter()
            elif 'fastighet' in self.url:
                return self.fastighet_filter()
        except:
            e = sys.exc_info()[0]
            print('Error, in filter: \n', e)

    def lansfast_filter(self):
        try:
            soup = BeautifulSoup(self.r.json()['View'], "html.parser")
            filter_results = soup.find("div", {"class": "boxViewContainer residenceContainer"})
            houses = filter_results.find_all("a")
            return [self.url[:23] + str(house['href'] + '\n') for house in houses]
        except:
            e = sys.exc_info()[0]
            print('Error, in Svenska filter: \n', e)

    def fastighet_filter(self):
        try:
            object_url = 'https://www.fastighetsbyran.com/sv/sverige/objekt/?objektid='
            headers = {
                'Content-Type': 'application/json',
            }

            data = '{"valdaMaeklarObjektTyper":[0],' \
                   '"valdaNyckelord":[],' \
                   '"valdaLaen":[],' \
                   '"valdaKontor":[],' \
                   '"valdaKommuner":["435"],' \
                   '"valdaNaeromraaden":[],' \
                   '"valdaPostorter":[],' \
                   '"inkluderaNyproduktion":true,' \
                   '"inkluderaPaaGaang":true}'

            r = requests.post('https://www.fastighetsbyran.com/HemsidanAPI/api/v1/soek/objekt/1/false/',
                                     headers=headers, data=data)
            return ['{}{}\n'.format(object_url, obj_id['maeklarObjektId']) for obj_id in r.json()['results']]
        except:
            e = sys.exc_info()[0]
            print('Error, in Svenska filter: \n', e)

    def svenska_filter(self):
        try:
            filter_results = self.page.find("div", {"class": "grid flex__grid"})
            houses = filter_results.find_all("a", {"class": "search-hit__link"})
            return [self.url[:25] + str(house['href'] + '\n') for house in houses if str(house['href'])[-1].isdigit()]
        except:
            e = sys.exc_info()[0]
            print('Error, in Svenska filter: \n', e)

    def era_filter(self):
        try:
            filter_results = self.page.find("ul", {"class": "extended items"})
            houses = filter_results.find_all("a")
            return [self.url[:25] + str(house['href'] + '\n') for house in houses]
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
