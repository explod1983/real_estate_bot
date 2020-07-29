import os
import json

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

with open('static_data_site_info.json', 'r') as file:
    data_base = json.load(file)

web_sites = data_base['web_sites']

