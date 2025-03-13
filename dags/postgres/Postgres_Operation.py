import psycopg2
import pandas as pd
from psycopg2.extras import execute_batch
from contextlib import contextmanager

@contextmanager
def connect_postgres(username:str = 'ndtien2004', password:str = 'ndtien2004', host:str =  'localhost', port:str = "5432", db:str = 'MUSIC_DB'):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname = db,
            user = username,
            password = password,
            host = host,
            port = port
        )
        print("Connect to Postgres Successfully")
        yield conn
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("Stop Connect to Postgres")

class Postgres_Operation:
    '''Initialize the Postgres operation class'''
    def __init__(self, conn):
        if not isinstance(conn, psycopg2.extensions.connection):
            raise TypeError("Conn must be a psycopg2 connection object")
        self.conn = conn

    '''Execute a query'''
    def execute_query(self, query, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()

    '''Create database if not exists'''
    def create_database(self, database_name):
        query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
        self.execute_query(query)

    '''Create schema if not exists'''
    def create_schema(self, schema_name):
        query = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
        self.execute_query(query)

    '''Create table if not exists'''
    def create_table(self, create_table_query):
        self.execute_query(create_table_query)

    '''Insert data'''
    def insert_data(self, table_name, df : pd.DataFrame, batch_size=1000):

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        with self.conn.cursor() as cursor:
            execute_batch(cursor, query, df.itertuples(index=False, name=None), page_size=batch_size)
            self.conn.commit()

    '''Read data'''
    def read_data(self, table_name, columns="*", conditions=None):
        query = f"SELECT {columns} FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
