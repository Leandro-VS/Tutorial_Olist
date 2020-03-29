import os
import sqlalchemy
import argparse
import pandas as pd
import datetime
import utils

## Endereços do projeto
DATA_PREP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(DATA_PREP_DIR))
DATA_DIR = os.path.join(BASE_DIR, 'data')

#Parser de data para fazer a "foto"
parser = argparse.ArgumentParser()
parser.add_argument('--date_end', '-e', help='Data de fim da extração', default='2018-06-01')
args = parser.parse_args()

date_end = args.date_end
ano = int(date_end.split("-")[0]) - 1
mes = int(date_end.split("-")[1])
date_init = f"{ano}-{mes}-01"

#Importando a query
query = utils.import_query(os.path.join(DATA_PREP_DIR, 'segmentos.sql'))
query = query.format(date_init = date_init, 
                     date_end = date_end ) 

#Abrindo conexão com o banco...
conn = utils.connect_db()

create_query = f'''
            CREATE TABLE tb_seller_sgmt AS {query}
;'''

insert_query = f'''
            DELETE FROM tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
            INSERT INTO tb_seller_sgmt {query}
;'''

try:
    utils.execute_many_sql(create_query, conn)
except:
    utils.execute_many_sql(insert_query, conn, verbose=True)
