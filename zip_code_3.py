import json
import sqlite3
import os
import csv
import matplotlib
import matplotlib.pyplot as plt
import random

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/Final.db')
cur = conn.cursor()

cur.execute('''SELECT Cities.id, state FROM Cities JOIN States ON States.id = Cities.id''')
output = []
for row in cur:
    output.append(row)

state_count = {}
for i in output:
    if i[1] in state_count:
        state_count[i[1]] = state_count[i[1]] + 1
    else:
        state_count[i[1]] = 1

header = ["State", "Zip Code Count"]
with open("data_out.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    sorted_states = sorted(state_count)
    for i in sorted_states:
        writer.writerow([i, state_count[i]])

pieList = list(state_count.items())
pieList = sorted(pieList, key = lambda x: x[1], reverse=True)
count_list = []
state_list = []
for i in pieList:
    state_list.append(i[0])
    count_list.append(i[1])

plt.pie(count_list[:10], labels = state_list[:10], autopct='%1.1f%%')
plt.savefig('visual1.png')