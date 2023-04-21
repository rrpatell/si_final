import json
import sqlite3
import os
import csv
import matplotlib
import matplotlib.pyplot as plt
import random
import numpy as np

def create_output(cur):
    cur.execute('''SELECT Cities.id, state FROM Cities JOIN States ON States.id = Cities.id''')
    output = []
    for row in cur:
        output.append(row)
    return output

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/Final.db')
    cur = conn.cursor()
    output = create_output(cur)
    state_count = {}
    for i in output:
        if i[1] in state_count:
            state_count[i[1]] = state_count[i[1]] + 1
        else:
            state_count[i[1]] = 1

    header = ["State", "Zipcode_Count"]
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

    cur.execute('SELECT state, ROUND(AVG(ozone_levels),2) FROM Ozone JOIN StatesForAir on state_id = StatesForAir.id GROUP BY state')
    collected_data = cur.fetchall()
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, 'calcByState.csv'), 'w')
    csv_writer = csv.writer(outFile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    title = ['State', 'Avg Ozone Levels']
    csv_writer.writerow(title)
    for row in collected_data:
        csv_writer.writerow([row[0], row[1]])
    outFile.close()

    i=np.argsort(state_list[:10])
    collected_data = np.asarray(collected_data)
    count_list = np.asarray(count_list[:10])
    state_list = sorted(state_list[:10])

    weather_list = []
    for i in collected_data:
        weather_list.append(float((i[1])))

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('States')
    ax1.set_ylabel('Number of Zip Codes', color=color)
    ax1.plot(state_list, count_list, 'go', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 

    color = 'tab:blue'
    ax2.set(ylim=(0, 150))
    ax2.set_ylabel('Ozone Concentration (in μg/m^3)', color=color) 
    ax2.plot(state_list, weather_list, 'go', color=color)
    ax2.tick_params(axis='y', labelcolor=color, bottom=False)
    ax1.set_xticklabels(state_list, rotation=90)

    plt.title("Ten Most Common States with Zip Codes between 20588-98300 and their Average Ozone Concentration")
    fig.savefig('visual1.png', bbox_inches="tight")

if __name__ == "__main__":
    main()