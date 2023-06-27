from data.pipeline import load
import pytest
import os
import pandas as pd
import sqlite3
from pandas.testing import assert_frame_equal


def test_weather_load():
    data = pd.DataFrame([],columns=['date', 'hour', 'temp', 'dwpt', 'rhum', 'prcp',
            'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco','station'])
    load(data, 'weather','test.sqlite')
    
    conn = sqlite3.connect('test.sqlite')
    result = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()
    
    assert_frame_equal(result, data)
    
def test_train_load():
    data = pd.DataFrame([],columns=['name', 'eva', 'ds100', 'db', 'creationts', 'meta',
            'updatets'])
    load(data, 'train_stations','test.sqlite')
    
    conn = sqlite3.connect('test.sqlite')
    result = pd.read_sql_query("SELECT * FROM train_stations", conn)
    conn.close()
    
    assert_frame_equal(result, data)