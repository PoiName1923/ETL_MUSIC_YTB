from mongodb.mongodb_operation import *
import pandas as pd
from datetime import datetime, timezone

Execution_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

def return_artists_id_cleaned(Execution_date : str):
    def cleaning_id_data(data:pd.DataFrame):
        data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
        data = data.drop_duplicates()
        data = data.dropna()
        data = data['execution_date'] = pd.to_datetime(data['execution_date'], errors='coerce').dt.strftime('%Y-%m-%d')
        return data
    with connect_mongodb(username='ndtien2004',password='ndtien2004') as client:
        client_op = MongoDB_Operation(client=client)
        data = client_op.find_data(db_name='ytb_db',collection_name='artists_id',query={"Execution Date":Execution_date})
        return cleaning_id_data(data)
    
def return_artists_song_cleaned(Execution_date : str):
    def cleaning_song_data(data:pd.DataFrame):
        data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
        data = data.drop_duplicates()
        data = data.dropna()
        data[['execution_date','upload_date']] = pd.to_datetime(data[['execution_date','upload_date']], errors='coerce').dt.strftime('%Y-%m-%d')
        return data
    with connect_mongodb(username='ndtien2004',password='ndtien2004') as client:
        client_op = MongoDB_Operation(client=client)
        data = client_op.find_data(db_name='ytb_db',collection_name='artists_song',query={"Execution Date":Execution_date})
        return cleaning_song_data(data)