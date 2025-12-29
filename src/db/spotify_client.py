import os
import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECTED_URI")

def get_sp():
    sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(
        client_id = SPOTIFY_CLIENT_ID,
        client_secret = SPOTIFY_CLIENT_SECRET,
        # redirect_uri = REDIRECT_URI,
        # scope = "user-library-read"
    ))
    return sp


# def search_song_on_spotify(track_ID):
#     try:
#         result = sp.search(q=f"track_id: {track_ID}", type='track', limit=1)
#         return result['tracks']['items']
    
#     except SpotifyException as e:
#         if e.http_status == 429:
#             retry_after = int(e.headers.get("Retry-After", 5))  # spotify tells us how long to wait
#             print(f"Rate limit hit. Retrying after {retry_after}seconds.")
#             time.sleep(retry_after)
#             return search_song_on_spotify(track_ID)
#         else:
#             print(f"Spotify API Error: {e}")
#             return None
        
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
    
# def get_audio_features(track_ID):
#     try:
#         features =sp.audio_features([track_ID])[0]
#         return features
#     except Exception as e:
#         print(f"Error retrieving audio features: {e}")
#         return None
    