import pandas as pd
import sqlite3
from housing_utils import read_housing

def write_to_sqlite(data, sqlite_file, drop_existing=True):
    conn = sqlite3.Open(sqlite_file)
    data.to_sql()