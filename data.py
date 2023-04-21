import json
import sqlite3
import os
import csv
import matplotlib
import matplotlib.pyplot as plt
import random

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

    plt.bar(state_list[:10], count_list[:10], color ='maroon', width = 0.4)
    plt.xlabel("States")
    plt.ylabel("Number of Zip Codes")
    plt.xticks(rotation=90)
    plt.title("Ten Most Common States with Zip Codes between 20588-98300")
    plt.savefig('visual1.png', bbox_inches="tight")

if __name__ == "__main__":
    main()