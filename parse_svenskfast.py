import requests
from bs4 import BeautifulSoup
import sys

URL = 'https://www.svenskfast.se'
URL_svenska = f'{URL}/hus/vastra-gotaland/ale/'


def latest_result():
    r = requests.get(URL_svenska)
    soup = BeautifulSoup(r.content, "html.parser")

    filter_results = soup.find("div", {"class": "grid flex__grid"})
    houses = filter_results.find_all("a", {"class": "search-hit__link"})
    return [URL + str(house['href'] + '\n') for house in houses if str(house['href'])[-1].isdigit()]


def update_SVENSKAFAST_db():
    try:
        with open('base/svenskfast_base.txt', 'w') as file:
            for link in latest_result():
                file.write(link)
    except:
        e = sys.exc_info()[0]
        print('Error, cannot write to DB file: ', e)


def read_db():
    try:
        with open('base/svenskfast_base.txt', 'r') as file:
            return file.readlines()
    except:
        e = sys.exc_info()[0]
        print('Error, cannot write to DB file: ', e)


def compare_SVENSKAFAST_latest_with_db():
    return list(set(latest_result()) - set(read_db()))
