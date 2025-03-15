from mongodb.get_id_artist import *
from mongodb.get_song_artist import *
from datetime import datetime

def get_daily_data_mongo(Execution_date : str):
    loading_artist_id(Execution=Execution_date)
    loading_song_data(Execution=Execution_date)