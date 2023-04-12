import json
import sqlite3
import os

full_path = os.path.join(os.path.dirname(__file__), 'zip_api.json')
f = open(full_path)
file_data = f.read()
f.close()
json_data = json.loads(file_data)
cities = json_data['0']

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/Final.db')
cur = conn.cursor()

states = {}
count = 0
for i in cities:
    if i['state'] in states:
        continue
    else:
        states[i['state']] = count
        count = count + 1

cur.execute("CREATE TABLE IF NOT EXISTS States (id INTEGER PRIMARY KEY, state TEXT)")
cur.execute("select count(*) from States")
results = cur.fetchone()
states_entries = results[0]
stateList = list(states.items())
for i in range(states_entries, min(states_entries+25, len(stateList))):
    id = stateList[i][1]
    state = stateList[i][0]
    cur.execute("INSERT OR IGNORE INTO States (id, state) VALUES (?,?)",(id, state))
conn.commit()

cur.execute("CREATE TABLE IF NOT EXISTS Cities (zip INTEGER PRIMARY KEY, id INTEGER, city TEXT)")
cur.execute("select count(*) from Cities")
results = cur.fetchone()
cities_entries = results[0]
for i in range(cities_entries, min(cities_entries+25, len(cities))):
    id = states[cities[i]['state']]
    zip = cities[i]['zip']
    city = cities[i]['city']
    cur.execute("INSERT OR IGNORE INTO Cities (zip, id, city) VALUES (?,?,?)",(zip, id, city))
conn.commit()