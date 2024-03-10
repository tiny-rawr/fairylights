from googleapiclient.discovery import build
from datetime import datetime, timedelta
import isodate


class YouTubeClient:
    def __init__(self):
        api_key = "AIzaSyD9Gm0r16NzQ_CN6mxqhwrijCNK8w72VVs"
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_id(self, username):
        search_response = self.youtube.search().list(
            q=username,
            part='snippet',
            type='channel',
            maxResults=1
        ).execute()

        channel_id = search_response['items'][0]['id']['channelId']
        return channel_id

    def get_recent_videos(self, channel_id, max_results=50):
        """Fetch recent full videos for a given YouTube channel ID."""
        last_month = datetime.now() - timedelta(days=30)
        last_month_iso = last_month.isoformat("T") + "Z"

        videos = []
        page_token = None

        while True:
            search_response = self.youtube.search().list(
                channelId=channel_id,
                part='snippet',
                order='date',
                maxResults=max_results,
                publishedAfter=last_month_iso,
                pageToken=page_token,
                type='video'
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response['items'] if
                         item['id']['kind'] == 'youtube#video']

            # Get content details for videos to filter out Shorts
            if video_ids:
                videos_response = self.youtube.videos().list(
                    id=','.join(video_ids),
                    part='contentDetails'
                ).execute()

                for item in videos_response['items']:
                    duration = isodate.parse_duration(item['contentDetails']['duration'])
                    if duration.total_seconds() > 60:  # Filter out YouTube shorts
                        video_id = item['id']
                        snippet = next(
                            (s['snippet'] for s in search_response['items'] if s['id']['videoId'] == video_id), None)
                        if snippet:
                            video = {
                                'title': snippet['title'],
                                'description': snippet['description'],
                                'thumbnail': snippet['thumbnails']['high']['url']
                            }
                            videos.append(video)

            page_token = search_response.get('nextPageToken')
            if not page_token:
                break

        return videos

    def print_video_details(self, videos):
        """Print details of the videos."""
        for video in videos:
            print(f"Title: {video['title']}, Video ID: {video['video_id']}")


# Usage
if __name__ == "__main__":
    username = 'timferriss'

    client = YouTubeClient()

    channel_id = client.get_channel_id(username)

    recent_videos = client.get_recent_videos(channel_id)
    #client.print_video_details(recent_videos)
    print(recent_videos)
