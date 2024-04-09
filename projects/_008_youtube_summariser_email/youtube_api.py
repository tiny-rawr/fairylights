from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from isodate import parse_duration
import streamlit as st
import requests

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

def get_video_transcript(video_id):
    transcript_with_timestamps = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([t['text'] for t in transcript_with_timestamps])
    return transcript

def get_videos_from_playlist(playlist_id, days=30):
    youtube_api_key = st.secrets["youtube"]["youtube_api_key"]

    # Get the uploads playlist items
    response = requests.get(f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key={youtube_api_key}')
    videos = response.json()['items']

    # Filter videos from the last 'x' days and get video IDs
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_videos = []
    video_ids = []
    for video in videos:
        if datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ') > cutoff_date:
            recent_videos.append(video)
            video_ids.append(video['snippet']['resourceId']['videoId'])

    # Get video durations
    response = requests.get(
        f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={",".join(video_ids)}&key={youtube_api_key}'
    )
    video_durations = {video['id']: parse_duration(video['contentDetails']['duration']).total_seconds() for video in response.json()['items']}

    videos = [
        {
            'video_id': video['snippet']['resourceId']['videoId'],
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'thumbnail': video['snippet']['thumbnails']['high']['url'],
            'publishedAt': video['snippet']['publishedAt'],
            'transcript': get_video_transcript(video['snippet']['resourceId']['videoId']),
            # Filter out YouTube Shorts (60 seconds or less)
            'duration': f"{int(video_durations[video['snippet']['resourceId']['videoId']] // 60)}m {int(video_durations[video['snippet']['resourceId']['videoId']] % 60)}s"
        }
        for video in recent_videos
        if video_durations[video['snippet']['resourceId']['videoId']] > 60
    ]

    return videos
