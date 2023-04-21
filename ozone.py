import requests
import json
import sqlite3
import datetime
import os
import matplotlib.pyplot as plt
import csv

def getWeather(city, state):
    api_key = "2b81fdc1b4e124c402aa53a931bf8b08"
    start = "1680325200"
    end = "1681963200"
    lat = getCoord(city, state)[0]
    lon = getCoord(city, state)[1]
    base_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api_key}"
    raw_response = requests.get(base_url)
    response = raw_response.json()
    data = response['list']
    city = city.replace("+"," ")
    dt_list = []
    date_list = []
    o3_list = []
    for i in data:
        dt = str(datetime.datetime.fromtimestamp(i['dt']))
        date = dt[:10]
        o3 = i['components']['o3']
        if date not in date_list:
            date_list.append(date)
        dt_list.append(dt)
        o3_list.append(o3)
    subdict = {}
    for i in range(len(dt_list)):
        subdict[dt_list[i]] = o3_list[i]
    results = {}
    for date_key in date_list:
        o3_on_date = []
        for dt_key in subdict.keys():
            if dt_key[:10]==date_key:
                o3_on_date.append(subdict[dt_key])
        results[date_key] = max(o3_on_date)
    return results

def getCoord(city, state):
    api_key = "2b81fdc1b4e124c402aa53a931bf8b08"
    country = "US"
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={api_key}"
    raw_response = requests.get(url)
    response = raw_response.json()
    return (response[0]['lat'], response[0]['lon'])

def reorg_dict(results):
    new_dict = {}
    subdict = {}
    dates = list(list(results.values())[0].keys())
    for date in dates:
        this_date_subdict = {}
        for state in results:
            for d in results[state]:
                if d == date:
                    this_date_subdict[state] = results[state][d]
        new_dict[date] = this_date_subdict
    return new_dict

def make_ozone_id(ozone_dict):
    ozone_records = {}
    count = 0
    for date in list(ozone_dict.keys()):
        for state in ozone_dict[date]:
            internal_dict = {}
            internal_dict['ozone'] = ozone_dict[date][state]
            internal_dict['state'] = state
            internal_dict['date'] = date
            ozone_records[count] = internal_dict
            count += 1
    return ozone_records

def make_state_id(cities):
    states = {}
    count = 1
    for i in cities:
        if i[1] in states:
            continue
        else:
            states[i[1]] = count
            count += 1
    return states

def make_states_db(cur, conn, states):
    cur.execute("CREATE TABLE IF NOT EXISTS StatesForAir (id INTEGER PRIMARY KEY, state TEXT)")
    cur.execute("select count(*) from StatesForAir")
    results = cur.fetchone()
    states_entries = results[0]
    stateList = list(states.items())
    for i in range(states_entries, min(states_entries+25, len(stateList))):
        id = stateList[i][1]
        state = stateList[i][0]
        if state == "":
            state = "Unknown"
        cur.execute("INSERT OR IGNORE INTO StatesForAir (id, state) VALUES (?,?)",(id, state))
    conn.commit()

def make_air_db(cur, conn, air, states):
    cur.execute("CREATE TABLE IF NOT EXISTS Ozone (id INTEGER PRIMARY KEY, date DATE, state_id INTEGER, ozone_levels DOUBLE)")
    cur.execute("select count(*) from Ozone")
    results = cur.fetchone()
    air_entries = results[0]
    for i in range(air_entries, min(air_entries+25, len(air))):
        id = i
        date = air[i]['date']
        state = states[air[i]['state']]
        ozone = air[i]['ozone']
        cur.execute("INSERT OR IGNORE INTO Ozone (id, date, state_id, ozone_levels) VALUES (?,?,?,?)",(id, date, state, ozone))
    conn.commit()

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
    cities = [("Sacramento", "CA"), ("Austin", "TX"), ("Saint+Paul", "MN"), ("Nashville", "TN"), ("Charleston", "WV"), ("Springfield", "IL"), ("Lansing", "MI"), ("Tallahassee", "FL"), ("Richmond", "VA"), ("Jefferson+City", "MO")]
    results = {}
    for city in cities:
        results[city[1]] = getWeather(city[0], city[1])
    results_dict = results
    dates_dict = reorg_dict(results_dict)
    ozone_dict = make_ozone_id(dates_dict)

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/Final.db')
    cur = conn.cursor()

    states_id = make_state_id(cities)
    make_states_db(cur, conn, states_id)
    make_air_db(cur, conn, ozone_dict, states_id)

    calculation1(cur, conn)
    visualization(calculation1(cur, conn), calculation2(cur, conn))

if __name__ == "__main__":
    main()
