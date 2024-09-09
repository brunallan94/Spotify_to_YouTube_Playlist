from spotify import Spotify
from youtube import YouTube
from check_internet import check_internet_connection
from googleapiclient.errors import HttpError
import time


class PlaylistExporter:
    def __init__(self):
        self.spotify = Spotify()
        self.youtube = YouTube()
        self.max_requests_per_day = 9000  # Set the max requests per day to avoid exceeding the quota
        self.requests_made = 0

    def export_playlist(self):
        # Check for an internet connection before proceeding
        if not check_internet_connection():
            print("No internet connection available. Please check your connection and try again.")
            return

        # Set your Spotify playlist ID here (or leave it as 'Liked Songs')
        self.spotify.playlist_id = 'Liked Songs'

        # Fetch Spotify playlist tracks
        tracks = self.spotify.get_spotify_playlist_tracks()

        # Authenticate YouTube
        youtube = self.youtube.youtube_authenticate()

        # Create a new YouTube playlist
        youtube_playlist_id = self.youtube.create_youtube_playlist(youtube, "My YouTube Playlist", "Playlist from Spotify")

        # Add each track to YouTube playlist
        for track in tracks:
            try:
                if self.requests_made >= self.max_requests_per_day:
                    print("Reached daily request limit. Pausing until quota resets.")
                    break

                # Search for the video and add it to the playlist
                video_id = self.youtube.search_youtube_video(youtube, track)
                self.youtube.add_video_to_playlist(youtube, youtube_playlist_id, video_id)
                print(f"Added {track} to YouTube playlist")

                # Increment the request count
                self.requests_made += 1

                # Pause to prevent hitting the quota limit too quickly
                time.sleep(1)

            except HttpError as e:
                if 'quotaExceeded' in str(e):
                    print("Quota exceeded. Halting the script until the quota resets.")
                    break
                else:
                    print(f"Failed to add {track}: {e}")
                    continue


if __name__ == '__main__':
    exporter = PlaylistExporter()
    exporter.export_playlist()
