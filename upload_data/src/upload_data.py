import os
import pandas as pd
import sqlalchemy

## Endereços do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

#Lendo os arquivos de dados .csv
files_names = [i for i in os.listdir(DATA_DIR) if i.endswith('.csv')] 

#Conexão com sqlite
str_conn = 'sqlite:///{path}'
#Abrindo conexão com o db
str_conn = str_conn.format(path = os.path.join(DATA_DIR, 'olist.db'))
conn = sqlalchemy.create_engine(str_conn)

#Inserindo cada arquivo no db
for i in files_names:
    print(i)
    #dataframe temporario
    df_tmp = pd.read_csv(os.path.join(DATA_DIR, i))
    #Enviar o df para o DB
    table_name = "tb_" + i.strip(".csv").replace("olist_", "").replace("_dataset", "")
    df_tmp.to_sql(table_name, conn, if_exists='replace', index=False)














































