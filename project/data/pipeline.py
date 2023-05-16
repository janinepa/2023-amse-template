import pandas as pd

import os
import dotenv

import http.client
import requests

import gzip
import shutil

from sqlalchemy import create_engine

# Data engineering script to pull, massage, and store data
# Output: local datasets in /data directory (as raw csv or raw json and processed SQLite databases)

engine = create_engine('sqlite:///amse.db', echo=False)


def get_data_from_db(table):
    engine = create_engine('sqlite:///amse.db', echo=False)

    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_table(table, conn)

    return data

###################################
### Datasource 1: DB timetables ###
###################################


# get API key
dotenv.load_dotenv()

APIKey = os.getenv('APIKey')
ClientID = os.getenv('ClientID')

# connect to API
conn = http.client.HTTPSConnection("apis.deutschebahn.com")

headers = {
    'DB-Client-Id': ClientID,
    'DB-Api-Key': APIKey,
    'accept': "application/xml"
}

# get all Stations
conn.request(
    "GET", "/db-api-marketplace/apis/timetables/v1/station/*", headers=headers)

res = conn.getresponse()

if (res.status != 200):
    print("HTTP Error", res.status, res.reason)

data = res.read()
train_stations = pd.read_xml(data)

train_stations.to_sql('train_stations', 'sqlite:///amse.sqlite',
                      if_exists='replace', index=False)

# get timetable data from stations (currently only one station)
conn.request(
    "GET", "/db-api-marketplace/apis/timetables/v1/fchg/8000036", headers=headers)

res = conn.getresponse()

if (res.status != 200):
    print("HTTP Error", res.status, res.reason)

data = res.read()
timetables = pd.read_xml(data.decode())

timetables.to_sql('timetables', 'sqlite:///amse.sqlite',
                  if_exists='replace', index=False)


#################################
##### Datasource 2: Weather #####
#################################

# get all stations
url = "https://bulk.meteostat.net/v2/stations/lite.json.gz"
name = "weather_stations"

res = requests.get(url)

if (res.status_code != 200):
    print("HTTP Error", res.status_code, res.reason)

with open(name+".json.gz", "wb") as file:
    file.write(res.content)

with gzip.open(name+".json.gz", 'rb') as f_in:
    with open(name+".json", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

data = pd.read_json(name+".json")
data.to_csv(name+".csv")
weather_stations = pd.read_csv(name+".csv")

weather_stations.to_sql(
    'weather_stations', 'sqlite:///amse.sqlite', if_exists='replace', index=False)


# get weather data for stations (currently only one station)
url = "https://bulk.meteostat.net/v2/hourly/10326.csv.gz"
name = "10326"

res = requests.get(url)

if (res.status_code != 200):
    print("HTTP Error", res.status_code, res.reason)

with open(name+".csv.gz", "wb") as file:
    file.write(res.content)

with gzip.open(name+".csv.gz", 'rb') as f_in:
    with open(name+".csv", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

colnames = ['date', 'hour', 'temp', 'dwpt', 'rhum', 'prcp',
            'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco']
weather = pd.read_csv(name+".csv", names=colnames, header=None)

weather.to_sql('weather', 'sqlite:///amse.sqlite',
               if_exists='replace', index=False)
