from get_id_artist import *
from get_song_artist import *
from datetime import datetime

def get_daily_data(Execution_date : str):
    loading_artist_id(Execution=Execution_date)
    loading_song_data(Execution=Execution_date)