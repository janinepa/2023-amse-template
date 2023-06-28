import urllib.request
import zipfile
import os
import pandas as pd
from sqlalchemy import create_engine

# Download and unzip data
zip_filename, headers = urllib.request.urlretrieve('https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip')

with zipfile.ZipFile(zip_filename, "r") as zip_ref:
    target_dir = "data"
    zip_ref.extractall(target_dir)

csv_filename = os.path.join(target_dir, os.listdir(target_dir)[0])

#Reshape data
#Only use the columns "Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"
df = pd.read_csv(csv_filename, sep=';', decimal=',', index_col=False, usecols=["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"])

#Rename "Temperatur in °C (DWD)" to "Temperatur"
#Rename "Batterietemperatur in °C" to "Batterietemperatur"
df = df.rename(columns={'Temperatur in °C (DWD)': 'Temperatur','Batterietemperatur in °C': 'Batterietemperatur'})

#Transform data
#Transform temperatures in Celsius to Fahrenheit (formula is (TemperatureInCelsius * 9/5) + 32) in place (keep the same column names)
#Columns Temperatur and Batterietemperatur
def celsius_to_fahrenheit(temp):
    return (temp * 9/5) + 32

df['Temperatur'] = df['Temperatur'].apply(celsius_to_fahrenheit)
df['Batterietemperatur'] = df['Batterietemperatur'].apply(celsius_to_fahrenheit)


#Validate data
#Use validations as you see fit, e.g., for Geraet to be an id over 0
df = df[ (df['Monat'] >= 1) & (df['Monat'] <= 12)]
df = df[ (df['Geraet'] >= 0)]


#Use fitting SQLite types (e.g., BIGINT, TEXT or FLOAT) for all columns
#Write data into a SQLite database called “temperatures.sqlite”, in the table “temperatures”
engine = create_engine("sqlite:///temperatures.sqlite", echo=True)

df.to_sql('temperatures', engine, if_exists='replace', index=False)
