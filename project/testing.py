#from numpy import NaN
from data.pipeline import load
import pytest
import os
import pandas as pd
import sqlite3
from pandas.testing import assert_frame_equal

def test_sql():
    assert os.path.exists("./data/amse.sqlite") == True
       
#def test_transform():
#    data= pd.DataFrame([[''], [], []])
#    transformed = transfrom(data)  
#    assert transformed.shaped ==(2, 3)

def test_load():
    data = pd.DataFrame([],columns=['date', 'hour', 'temp', 'dwpt', 'rhum', 'prcp',
            'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco','station'])
    load(data, 'weather','test.sqlite')
    
    conn = sqlite3.connect('test.sqlite')
    result = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()
    
    assert_frame_equal(result, data)