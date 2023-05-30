import pandas as pd

import os
import dotenv

import http.client
import requests

import gzip
import shutil

import sqlite3
from sqlalchemy import create_engine

from datetime import datetime

# Data engineering script to pull, massage, and store data
# Output: local datasets in /data directory (as raw csv or raw json and processed SQLite databases)

engine = create_engine('sqlite:///amse.db', echo=False)


def parse_date(date_str, raw=False):
    if date_str == 'nan':
        return float('nan')
    date = date_str[:6]
    time = date_str[6:10]

    year = int(date[:2]) + 2000
    month = int(date[2:4])
    day = int(date[4:6])
    hour = int(time[:2])
    minute = int(time[2:4])

    d = datetime(year, month, day, hour, minute, second=0)

    if raw:
        return d.timestamp()
    else:
        return d.strftime("%d.%m.%Y, %H:%M")


def get_data_from_db(table):
    engine = create_engine('sqlite:///amse.db', echo=False)

    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_table(table, conn)

    return data

###################################
### Datasource 1: DB timetables ###
###################################


def get_trainstations(headers):
    # connect to API
    conn = http.client.HTTPSConnection("apis.deutschebahn.com")

    # get all Stations
    conn.request(
        "GET", "/db-api-marketplace/apis/timetables/v1/station/*", headers=headers)

    res = conn.getresponse()

    if (res.status != 200):
        print("HTTP Error", res.status, res.reason)
    else:
        data = res.read()
        train_stations = pd.read_xml(data)

        # Filter for main stations
        substrings = ["Hbf"]
        mask = train_stations["name"].str.contains("|".join(substrings))
        train_stations = train_stations[mask]

        return train_stations


def get_timetables(headers, train_stations):
    train_stations_list = list(train_stations.eva)

    conn = http.client.HTTPSConnection("apis.deutschebahn.com")
    timetable_table = pd.DataFrame()

    # get timetable data from stations
    for i in train_stations_list:
        conn.request(
            "GET", "/db-api-marketplace/apis/timetables/v1/fchg/{}".format(i), headers=headers)

        res = conn.getresponse()

        if (res.status != 200):
            print("HTTP Error", res.status, res.reason)
        else:
            data = res.read()
            # filter for departure data
            if 'dp' not in data.decode("utf-8"):
                print('dp not in data')
            else:
                timetables = pd.read_xml(
                    data.decode("utf-8"), xpath=".//s//dp")

                # filter for changed time and planned time
                if 'ct' in timetables.columns:
                    timetables[['ct']] = timetables[['ct']].astype(str)
                    timetables['ct'] = timetables['ct'].apply(parse_date)
                else:
                    timetables['ct'] = float('nan')

                if 'pt' in timetables.columns:
                    timetables[['pt']] = timetables[['pt']].astype(str)
                    timetables['pt'] = timetables['pt'].apply(parse_date)
                else:
                    timetables['pt'] = float('nan')

                # timetables.to_csv('timetables.csv')
                timetables['eva'] = i

                timetable = pd.DataFrame(timetables[['eva', 'ct', 'pt']])

                # TODO drop nan or just where planned is nan
                timetable = timetable.dropna()

                timetable_table = timetable_table.append(timetable)

    # TODO update taballe mit neunen daten wenn eva und pt gleich dann nicht append sonst schon

    return timetable_table

#################################
##### Datasource 2: Weather #####
#################################


def get_weather_station():
    # get all stations
    url = "https://bulk.meteostat.net/v2/stations/lite.json.gz"
    name = "weather_stations"

    res = requests.get(url)

    if (res.status_code != 200):
        print("HTTP Error", res.status_code, res.reason)
    else:
        with open("./temp/"+name+".json.gz", "wb") as file:
            file.write(res.content)

        with gzip.open("./temp/"+name+".json.gz", 'rb') as f_in:
            with open("./temp/"+name+".json", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        data = pd.read_json("./temp/"+name+".json")
        data.to_csv("./temp/"+name+".csv")
        weather_stations = pd.read_csv("./temp/"+name+".csv")
        weather_stations = weather_stations[weather_stations['country'] == 'DE']

    return weather_stations


def get_match_table(weather_stations, train_stations):

    w = weather_stations[['id', 'name']]
    t = train_stations[['eva', 'name']]

    train_stations_list = list(train_stations['name'])
    train_stations_list
    weather = []
    for i in train_stations_list:
        x = i.split('Hbf', 1)
        weather.append(x[0].strip())

    t['common'] = weather
    t['join'] = 1
    w['join'] = 1

    dataFrameFull = t.merge(
        w, on='join').drop('join', axis=1)

    t.drop('join', axis=1, inplace=True)
    # print(dataFrameFull)
    dataFrameFull['match'] = dataFrameFull.apply(
        lambda x: x.name_y.find(x.common), axis=1).ge(0)

    match_table = dataFrameFull[dataFrameFull['match']]

    match_table.drop_duplicates(subset=['name_x'])

    return match_table


def get_weather_data(match_table):
    # get weather data for stations (currently only one station)
    weather_dataframe = pd.DataFrame()
    for i in list(match_table.id):
        print(i)

        url = "https://bulk.meteostat.net/v2/hourly/{}.csv.gz".format(i)
        name = i

        res = requests.get(url)

        if (res.status_code != 200):
            print("HTTP Error", res.status_code, res.reason)
        else:
            with open("./temp/"+name+".csv.gz", "wb") as file:
                file.write(res.content)

            with gzip.open("./temp/"+name+".csv.gz", 'rb') as f_in:
                with open("./temp/"+name+".csv", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            colnames = ['date', 'hour', 'temp', 'dwpt', 'rhum', 'prcp',
                        'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco']
            weather = pd.read_csv("./temp/"+name+".csv",
                                  names=colnames, header=None)
            weather['station'] = i
            weather = weather[weather.date > '2023-01-01']
            weather_dataframe = weather_dataframe.append(weather)
            # weather.to_sql('weather', 'sqlite:///amse.sqlite',
            #   if_exists='append', index=False)
    return weather_dataframe


def load(data, table, db):
    conn = sqlite3.connect(db)
    data.to_sql(table, conn, if_exists='replace', index=False)
    conn.close()


if __name__ == "__main__":
    # get DB API key
    dotenv.load_dotenv()
    APIKey = os.getenv('APIKey')
    ClientID = os.getenv('ClientID')
    headers = {
        'DB-Client-Id': ClientID,
        'DB-Api-Key': APIKey,
        'accept': "application/xml"
    }

    train_stations = get_trainstations(headers)
    load(train_stations, 'train_stations', 'amse.sqlite')

    time_tables = get_timetables(headers, train_stations)
    load(time_tables, 'timetables3005', 'amse.sqlite')

    weather_stations = get_weather_station()
    load(weather_stations, 'weather_stations', 'amse.sqlite')

    match_table = get_match_table(weather_stations, train_stations)
    load(match_table, 'match_table', 'amse.sqlite')

    weather_data = get_weather_data(match_table)
    load(weather_data, 'weather', 'amse.sqlite')
