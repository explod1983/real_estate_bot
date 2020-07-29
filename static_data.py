import os
import json

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
db_file_path = DIR_PATH + '/static_data_site_info.json'
with open(db_file_path, 'r') as file:
    data_base = json.load(file)

web_sites = data_base['web_sites']

