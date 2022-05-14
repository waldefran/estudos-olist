import os 
import pandas as pd
import sqlalchemy
import argparse




BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'sql')

str_connection = 'sqlite:///{path}'
str_connection = str_connection.format( path=os.path.join(DATA_DIR, 'olist.db' ))
connection =sqlalchemy.create_engine(str_connection)

