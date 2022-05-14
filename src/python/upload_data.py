import os 
import pandas as pd
import sqlalchemy

str_connection = 'sqlite:///{path}'

#Define BASEDIR como diretorio pai da pasta de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__))))

#Define DATA_DIR como diretorio das bases.
DATA_DIR = os.path.join(BASE_DIR, 'data')

files_names = [i for i in os.listdir(DATA_DIR) if i.endswith('.csv')]

str_connection = str_connection.format( path=os.path.join(DATA_DIR, 'olist.db' ))

connection =sqlalchemy.create_engine(str_connection)

for i in files_names:
    df_tmp = pd.read_csv(os.path.join(DATA_DIR, i))
    table_name = i.strip('.csv').replace('olist_','').replace('_dataset','')
    df_tmp.to_sql( table_name, connection )
