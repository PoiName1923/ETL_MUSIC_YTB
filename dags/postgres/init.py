from postgres.Postgres_Operation import *
from dataprocess.cleaningdata import *


def load_artist_id_daily_postgres(Execution_date: str):
    artist_id = return_artists_id_cleaned(Execution_date=Execution_date)
    with connect_postgres(username='ndtien2004',password='ndtien2004') as conn:
        conn_op = Postgres_Operation(conn=conn)

        conn_op.insert_data(table_name='ARTIST',df='MUSIC_DATABASE')
def load_artist_song_daily_postgres(Execution_date: str):
    artist_id = return_artists_song_cleaned(Execution_date=Execution_date)
    with connect_postgres(username='ndtien2004',password='ndtien2004') as conn:
        conn_op = Postgres_Operation(conn=conn)

        conn_op.insert_data(table_name='ARTIST_SONG',df='MUSIC_DATABASE')

def loading_daily_postgres(Execution_date:str):
    load_artist_id_daily_postgres(Execution_date=Execution_date)
    load_artist_song_daily_postgres(Execution_date=Execution_date)