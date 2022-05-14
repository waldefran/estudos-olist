import os
import pandas as pd
import sqlalchemy
import argparse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'src','sql')

parser = argparse.ArgumentParser()
parser.add_argument( '--date_init', '-i', help='Data inicio extração', default='2017-06-01')
parser.add_argument( '--date_end', '-e', help='Data fim extração', default='2018-06-01')
args = parser.parse_args()

#Importa a Query
with open(os.path.join(SQL_DIR, 'segmentos.sql')) as query_file:
    query = query_file.read()
query = query.format(date_init = args.date_init,
                     date_end = args.date_end)
#Abre Conexão com o Banco
str_connection = 'sqlite:///{path}'
str_connection = str_connection.format( path = os.path.join(DATA_DIR, 'olist.db') ) 
connection = sqlalchemy.create_engine(str_connection)

create_query = f'''
CREATE TABLE seller_sgmt 
{query}
;'''

insert_query = f'''
DELETE FROM seller_sgmt WHERE DtSegmento = '{args.date_end}';
INSERT INTO seller_sgmt 
{query}
;'''

try:
    connection.execute(create_query)
except: 
    for q in insert_query.split(";")[:-1]:
        connection.execute(q)

