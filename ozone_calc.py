import requests
import json
import sqlite3
import datetime
import os
import matplotlib.pyplot as plt
import csv

def calculation1(cur, conn):
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

    return collected_data

def calculation2(cur, conn):
    cur.execute('SELECT date, ROUND(AVG(ozone_levels),2) FROM Ozone JOIN StatesForAir on state_id = StatesForAir.id GROUP BY date')
    collected_data = cur.fetchall()

    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, 'calcByDate.csv'), 'w')
    csv_writer = csv.writer(outFile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    title = ['Date', 'Avg Ozone Levels']
    csv_writer.writerow(title)
    for row in collected_data:
        csv_writer.writerow([row[0], row[1]])
    outFile.close()

    return collected_data

def visualization(state_list, date_list):
    states = []
    for state in state_list:
        states.append(state[0])
    values = []
    for state in state_list:
        values.append(state[1])

    plt.figure(figsize=(10,10)).tight_layout()
    plt.subplot(2,1,1)
    plt.bar(states, values)
    plt.xlabel("States")
    plt.ylabel("Ozone Concentration (in μg/m^3)")
    plt.title('Average Ozone Concentration since April 1st by State (Based on State Capital)')
    plt.ylim([0, 150])
    plt.axhline(y = 60, color = 'g', linestyle = '-', label = "'Good' category upper limit")
    plt.axhline(y = 100, color = 'y', linestyle = '-', label = "'Fair' category upper limit")
    plt.axhline(y = 140, color = 'r', linestyle = '-', label = "'Moderate' category upper limit")
    plt.tight_layout()
    plt.legend()

    dates = []
    for date in date_list:
        dates.append(date[0])
    values2 = []
    for date in date_list:
        values2.append(date[1])

    plt.subplot(2,1,2)
    plt.plot(dates, values2)
    plt.xlabel("Dates")
    plt.xticks(rotation=45)
    plt.ylabel("Ozone Concentration (in μg/m^3)")
    plt.title('Average Ozone Concentration since April 1st in 10 States by Date')
    plt.ylim([0, 150])
    plt.axhline(y = 60, color = 'g', linestyle = '-', label = "'Good' category upper limit")
    plt.axhline(y = 100, color = 'y', linestyle = '-', label = "'Fair' category upper limit")
    plt.axhline(y = 140, color = 'r', linestyle = '-', label = "'Moderate' category upper limit")
    plt.tight_layout()
    plt.legend()

    plt.savefig("Ozone.png")
    plt.show()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/Final.db')
    cur = conn.cursor()
    visualization(calculation1(cur, conn), calculation2(cur, conn))

if __name__ == "__main__":
    main()
