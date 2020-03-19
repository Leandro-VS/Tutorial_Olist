import os
import sqlalchemy
import argparse
import pandas as pd
import datetime

## Endereços do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

#Parser de data para fazer a "foto"
parser = argparse.ArgumentParser()
parser.add_argument('--date_end', '-e', help='Data de fim da extração', default='2018-06-01')
args = parser.parse_args()

date_end = args.date_end
ano = int(date_end.split("-")[0]) - 1
mes = int(date_end.split("-")[1])
date_init = f"{ano}-{mes}-01"

#Importando a query
with open(os.path.join(SQL_DIR, 'segmentos.sql')) as query_file:
    query = query_file.read()

#print(query)

query = query.format(date_init = date_init, 
                     date_end = date_end ) 

#print(query)
"""
    #Conexão com sqlite
    str_conn = 'sqlite:///{path}'
    #Abrindo conexão com o db
    str_conn = str_conn.format(path = os.path.join(DATA_DIR, 'olist.db'))
    conn = sqlalchemy.create_engine(str_conn)

    df = pd.read_sql_query(query, conn)
    #O processo acima é valido porem leva problemas quando o banco é muito grande, pois estamos trazendo
    #dados para o python, e isso não é recomendado.(a menos quando entrarmos na etapa de modelagem ML)
"""
#Forma alternativa

str_conn = 'sqlite:///{path}'
#Abrindo conexão com o db
str_conn = str_conn.format(path = os.path.join(DATA_DIR, 'olist.db'))
conn = sqlalchemy.create_engine(str_conn)


create_query = f'''
            CREATE TABLE tb_seller_sgmt AS {query}
;'''

insert_query = f'''
            DELETE FROM tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
            INSERT INTO tb_seller_sgmt {query}
;'''

try:
    conn.execute(create_query)
except:
    for q in insert_query.split(";")[:-1]:
        conn.execute(q)
