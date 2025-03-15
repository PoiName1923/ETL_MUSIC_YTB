# Library
import requests
from bs4 import BeautifulSoup
import pandas as pd
from ytmusicapi import YTMusic, OAuthCredentials
from datetime import datetime, timezone

from mongodb.mongodb_operation import *

Execution_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ytmusic = YTMusic()

# Lấy danh sách ID video của nghệ sĩ
def get_id_videos(channel_id: str):
    search_results = ytmusic.get_artist(channel_id).get('songs', {}).get('results', [])
    return [song['videoId'] for song in search_results if 'videoId' in song]

def get_data_song(artists_df: pd.DataFrame, Execution_date: str):
    print("Loading Artist Song...")
    attr_col = ['Video Id', 'Channel Id', 'Title', 'Author', 'Durations', 'Views', 'Upload Date', 
                'Thumbnail', 'URL']

    video_data_list = []

    for _, row in artists_df.iterrows():  # Lặp qua từng nghệ sĩ
        channel_id = row['Channel ID']
        list_song = [ytmusic.get_song(song_id) for song_id in get_id_videos(channel_id)]

        for song in list_song:
            video_data_list.append({
                "Execution": Execution_date,
                "Video Id": song["videoDetails"].get("videoId"),
                "Channel Id": channel_id,
                "Title": song["videoDetails"].get("title"),
                "Author": song["videoDetails"].get("author"),
                "Durations": int(song["videoDetails"].get("lengthSeconds", 0)),
                "Views": int(song["videoDetails"].get("viewCount", 0)),
                "Upload Date": song.get("microformat", {}).get("microformatDataRenderer", {}).get("uploadDate"),
                "Thumbnail": song.get("microformat", {}).get("microformatDataRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url"),
                "URL": song.get("microformat", {}).get("microformatDataRenderer", {}).get("urlCanonical"),
            })

    # Chuyển danh sách thành DataFrame
    video_data_df = pd.DataFrame(video_data_list, columns=attr_col)
    print("Done...")
    return video_data_df

def loading_song_data(Execution : str):
    with connect_mongodb(username='ndtien2004',password='ndtien2004',host='localhost',port='27017') as client:
        client_op = MongoDB_Operation(client = client)

        data_id = client_op.find_data(db_name='ytb_db', collection_name='artists_id',query={"Execution Date":Execution})

        data_song = get_data_song(artists_df = data_id, Execution_date=Execution)
        print("Loading Song Data...")
        client_op.insert_many(db_name='ytb_db',collection_name='artists_song', data=data_song)

