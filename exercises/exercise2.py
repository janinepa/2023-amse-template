# Automated data pipeline for https://mobilithek.info/offers/-8739430008147831066

from sqlalchemy import create_engine
import pandas as pd

# Read data
url = 'https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV'
df = pd.read_csv(url, sep=';',decimal=',')

# First, drop the "Status" column
df=df.drop(['Status'],axis=1)

# Then, drop all rows with invalid values:
# Valid "Verkehr" values are "FV", "RV", "nur DPN"
valid_Verkehr=["FV", "RV", "nur DPN"]
df = df[df['Verkehr'].isin(valid_Verkehr)]

# Valid "Laenge", "Breite" values are geographic coordinate system values between -90 and 90
df = df[ (df['Laenge'] >= -90) & (df['Breite'] >= -90) & (df['Laenge'] <= 90) & (df['Breite'] <= 90)]

# Valid "IFOPT" values follow this pattern:
# <exactly two characters>:<any amount of numbers>:<any amount of numbers><optionally another colon followed by any amount of numbers>
df = df[df['IFOPT'].str.contains(r'^[A-Za-z]{2}:\d*:\d*(?::\d*)?$',na=False)]

# Empty cells are considered invalid
df = df.dropna()

# Write data into a SQLite database called “trainstops.sqlite”, in the table “trainstops”
# Use fitting SQLite types (e.g., BIGINT, TEXT or FLOAT) for all columns
df["Betreiber_Nr"] = df["Betreiber_Nr"].astype(int)

engine = create_engine("sqlite:///trainstops.sqlite", echo=True)

df.to_sql('trainstops', engine, if_exists='replace', index=False)
