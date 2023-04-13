import requests
import json
import random
import sqlite3
import os

# get the data
def get_data(base_url):
    cities = []
    for i in (range(20588, 98300, 190)):
        url = base_url + str(i)
        response = requests.get(url)
        data = response.text
        d = json.loads(data)
        if (len(d) != 0):
            new_d = {}
            new_d['zip'] = d['post code']
            new_d['state'] = d['places'][0]['state']
            new_d['city'] = d['places'][0]['place name']
            cities.append(new_d)
    return cities

def output_json(cities):
    output_dict = {}
    output_dict[0] = cities
    with open("zip_api.json", "w") as fp:
        json.dump(output_dict,fp) 

def main():
    cities = get_data('https://api.zippopotam.us/us/')
    output_json(cities)

if __name__ == "__main__":
    main()