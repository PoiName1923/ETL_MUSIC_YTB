# Library
import requests
from bs4 import BeautifulSoup
import pandas as pd
from ytmusicapi import YTMusic, OAuthCredentials
from datetime import datetime, timezone

from mongodb_operation import *

Execution_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ytmusic = YTMusic()

# Hàm lấy danh sách nghệ sĩ từ Viberate
def get_id_top_artist(execution_date: str): 
    print("Loading Artist ID...")

    # Getting soup
    ytmusic = YTMusic()
    url = "https://www.viberate.com/music-charts/top-artists-from-vietnam/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    list_art_soup = soup.find_all('div', {"class": "chart-module-article-table-wrapper"})[0].find_all('tr')

    # Get Name
    list_art = []
    for a in list_art_soup:
        artist_name = a.find_all('td')[1].get_text(strip=True).split("VNM")[0].strip()
        if artist_name:
            list_art.append(artist_name)

    # Get Id - Name for YTB
    list_id_art = []
    for art in list_art:
        search_result = ytmusic.search(art, filter='artists', limit=1)
        if search_result and 'browseId' in search_result[0]:
            list_id_art.append({
                "Execution Date" : execution_date,
                "Artists Name" : art,
                "Channel ID" : search_result[0]['browseId']
            }) # Lưu ID của nghệ sĩ
            
    if list_id_art:
        print("Done...")
        return pd.DataFrame(list_id_art)
    else:
        print("Done...")
        return pd.DataFrame(columns=['Execution Date','Artists Name','Channel ID']) 
    
def loading_artist_id(Execution : str):
    with connect_mongodb(username='ndtien2004',password='ndtien2004',host = 'localhost', port='27017') as client:

        client_op = MongoDB_Operation(client=client)
        data_id = get_id_top_artist(execution_date=Execution)

        if client_op.check_database_exists(db_name='ytb_db') and client_op.check_collection_exists(db_name='ytb_db',collection_name='artists_id'):
            old_id = client_op.find_data(db_name='ytb_db',collection_name='artists_id',query={"Execution Date":Execution})[['Channel ID']]
            old_id.rename(columns={'Channel ID': 'Old ID'}, inplace=True)

            if data_id.empty:
                print("Không có nghệ sĩ mới từ Viberate!")
                return

            daily_data = pd.merge(old_id, data_id, left_on='Old ID', right_on="Channel ID", how='right') if not old_id.empty else data_id
            daily_data = daily_data[daily_data['Old ID'].isnull()][['Execution Date','Artists Name','Channel ID']]

            client_op.insert_many(db_name='ytb_db',collection_name='artists_id',data=daily_data)
        else:
            client_op.insert_many(db_name='ytb_db',collection_name='artists_id',data=data_id)