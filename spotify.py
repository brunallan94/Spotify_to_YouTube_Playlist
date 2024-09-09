import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


class Spotify:
    def __init__(self) -> None:
        self.SP_Client_ID = os.getenv('SPOTIFY_CLIENT_ID')
        self.SP_Client_Secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.SP_Redirect_URI = os.getenv('SPOTIFY_REDIRECT_URI')
        self.playlist_id = None  # Will be set later
        self.scope = 'user-library-read playlist-read-private'
        self.sp = None
        self.user_id = None

    def authenticate(self) -> None:
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SP_Client_ID,
                                                            client_secret=self.SP_Client_Secret,
                                                            redirect_uri=self.SP_Redirect_URI,
                                                            scope=self.scope))
        self.user_id = self.sp.me()['id']

    def get_spotify_playlist_tracks(self):
        self.authenticate()

        # Set the initial limit and offset
        limit = 50  # Maximum allowed limit
        offset = 0
        tracks: List = []

        while True:
            # Omitting the market parameter by explicitly setting it to an empty string
            if self.playlist_id == 'Liked Songs':
                results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
            else:
                results = self.sp.playlist_tracks(self.playlist_id, limit=limit, offset=offset)

            # Add each track's name and artist to the tracks list
            for item in results['items']:
                track = item['track']
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                tracks.append(f'{track_name} by {artist_name}')

            # Check if we've retrieved all tracks
            if len(results['items']) < limit:
                break  # If fewer than limit tracks are returned, we're done

            # Update the offset to get the next batch of tracks
            offset += limit

        return tracks


if __name__ == '__main__':
    call = Spotify()