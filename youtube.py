import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


class YouTube:
    def __init__(self) -> None:
        self.api_service_name = 'youtube'
        self.api_version = 'v3'
        self.client_secrets_file = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')
        self.scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

    def youtube_authenticate(self):
        # Initialize the flow using the client secrets file and scopes
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes
        )
        # Use run_local_server instead of run_console
        credentials = flow.run_local_server(port=0)  # This starts a local server for OAuth

        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=credentials
        )
        return youtube

    # Search for a video on YouTube
    def search_youtube_video(self, youtube, query):
        request = youtube.search().list(part='snippet', q=query, type='video', maxResults=1)
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        return video_id

    # Create a playlist on YouTube
    def create_youtube_playlist(self, youtube, title, description):
        request = youtube.playlists().insert(part='snippet,status', body={
            'snippet': {
                'title': title,
                'description': description
            },
            'status': {
                'privacyStatus': 'public'
            }
        })
        response = request.execute()
        return response['id']

    # Add a video to a playlist
    def add_video_to_playlist(self, youtube, playlist_id, video_id):
        request = youtube.playlistItems().insert(part='snippet', body={
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        })
        response = request.execute()
        return response
