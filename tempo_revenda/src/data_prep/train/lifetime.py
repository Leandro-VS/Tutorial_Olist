import os
import pandas as pd
import utils

BASE_DIR = os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname(__file__) ) ) )
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')
DB_PATH = os.path.join(DATA_DIR, 'olist.db')
 

conn = utils.connect_db() #Abre a conexão com o banco
query = utils.import_query(os.path.join(SQL_DIR, 'lifetime.sql')) #importa a nossa query

df = pd.read_sql_query(query, conn) #Executa a query dentro do banco
df.to_csv(os.path.join(DATA_DIR, 'lifetimes.csv'), sep=",", index=False) #Salvando em um .csv