import requests
from bs4 import BeautifulSoup
import sys

URL = 'https://www.erasweden.com'
URL_ale = f'{URL}/hitta-din-bostad?query=Commune%3A%22Ale%22'


def latest_result():
    r = requests.get(URL_ale)
    soup = BeautifulSoup(r.content, "html.parser")

    filter_results = soup.find("ul", {"class": "extended items"})
    houses = filter_results.find_all("a")

    return [URL + str(house['href'] + '\n') for house in houses]


def update_era_db():
    try:
        with open('base/era_base.txt', 'w') as file:
            for link in latest_result():
                file.write(link)
    except:
        e = sys.exc_info()[0]
        print('Error, cannot write to DB file: ', e)


def read_db():
    try:
        with open('base/era_base.txt', 'r') as file:
            return file.readlines()
    except:
        e = sys.exc_info()[0]
        print('Error, cannot write to DB file: ', e)


def compare_ERA_latest_with_db():
    return list(set(latest_result()) - set(read_db()))
