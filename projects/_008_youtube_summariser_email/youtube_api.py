from googleapiclient.discovery import build
import streamlit as st


def get_channel_id_from_username(username="timferriss"):
    youtube_api_key = st.secrets["youtube"]["youtube_api_key"]
    youtube_client = build('youtube', 'v3', developerKey=youtube_api_key)

    search_response = youtube_client.search().list(
        q=username,
        part='snippet',
        type='channel',
        maxResults=1
    ).execute()

    channel_id = search_response['items'][0]['id']['channelId']
    return channel_id


def get_channel_details(channel_id):
    youtube_api_key = st.secrets["youtube"]["youtube_api_key"]
    youtube_client = build('youtube', 'v3', developerKey=youtube_api_key)

    channel_response = youtube_client.channels().list(
        id=channel_id,
        part='snippet,contentDetails,statistics'
    ).execute()

    return channel_response['items'][0]
