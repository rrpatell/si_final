import requests
import json
import random
import sqlite3
import os

# get the data
cities = []
for i in (range(20588, 98300, 190)):
    url = 'https://api.zippopotam.us/us/' + str(i)
    response = requests.get(url)
    data = response.text
    d = json.loads(data)
    if (len(d) != 0):
        new_d = {}
        new_d['zip'] = d['post code']
        new_d['state'] = d['places'][0]['state']
        new_d['city'] = d['places'][0]['place name']
        cities.append(new_d)

output_dict = {}
output_dict[0] = cities
with open("zip_api.json", "w") as fp:
    json.dump(output_dict,fp) 