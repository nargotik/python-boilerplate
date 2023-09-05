import pandas as pd
import numpy as np
from database import my_read, my_close
import time
import psutil
import os
from cachetools import cached, TTLCache

cache_sampleFunction = TTLCache(maxsize=200, ttl=20)


from flask import Flask, jsonify

def convert_to_iso(element):
    if isinstance(element, pd.Timestamp):
        return element.isoformat()
    return element

@cached(cache_sampleFunction)
def sampleFunction():
    sql = """SELECT 1 as id, now() as date"""
    df = my_read(sql, 'id')
    df = df.applymap(convert_to_iso)
    my_close()
    return df


# utils.py
def SampleGenerate(arg1, ret_data = None):
    sample = sampleFunction()
    my_close()
    return {
        "status": 200,
        "arg1": arg1,
        "result": sample.to_dict(orient='index') if ret_data else None,
    }

def SampleGenerate2(arg1, arg2, ret_data = None):
    col_a = np.random.randint(1, 100, 20)
    col_b = np.random.randint(1, 100, 20)

    unique_index = set()
    while len(unique_index) < 20:
        new_index = f'ID_{int(np.random.rand() * 1000)}'
        unique_index.add(new_index)

    df = pd.DataFrame({
        'A': col_a,
        'B': col_b
    }, index=list(unique_index))

    df['AxARG2'] = df['A'] * arg2
    df['AxARG1'] = df['A'] * arg1
    df['B+ARG1'] = df['B'] + arg1
    df['A+ARG1'] = df['A'] + arg1

    return {
        "status": 200,
        "arg1": arg1,
        "result": df.to_dict(orient='index') if ret_data else None,
    }