import os
import sqlalchemy
import argparse

## Endereços do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

with open(os.path.join(SQL_DIR, 'segmentos.sql')) as query_file:
    query = query_file.read()

print(query)



