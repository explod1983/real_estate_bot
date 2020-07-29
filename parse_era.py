import requests
from bs4 import BeautifulSoup
import sys
import os


URL = 'https://www.erasweden.com'
URL_ale = f'{URL}/hitta-din-bostad?query=Commune%3A%22Ale%22'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_FILE_PATH = f'{DIR_PATH}/base/era_base.txt'


def latest_result():
    r = requests.get(URL_ale)
    soup = BeautifulSoup(r.content, "html.parser")

    filter_results = soup.find("ul", {"class": "extended items"})
    houses = filter_results.find_all("a")

    return [URL + str(house['href'] + '\n') for house in houses]


def update_era_db():
    try:
        with open(DB_FILE_PATH, 'w') as file:
            for link in latest_result():
                file.write(link)
    except:
        e = sys.exc_info()[0]
        print('Error, cannot write to DB file: ', e)


def read_db():
    try:
        with open(DB_FILE_PATH, 'r') as file:
            return file.readlines()
    except:
        e = sys.exc_info()[0]
        print('Error, cannot read to DB file: ', e)


def compare_ERA_latest_with_db():
    return list(set(latest_result()) - set(read_db()))
