from spotify_client import *
import pandas as pd

sp = get_sp()

def get_tracks_by_year(year, total=1000):
    tracks = []
    pages = total // 50
    
    for i in range(pages):
        offset = i*50
        track_result = sp.search(q=f"year:{year}", type="track", limit=50, offset= offset)
        
        for j, item in enumerate(track_result['tracks']['items']):
            track_name = item['name']
            track_id = item['id']
            track_uri = item['uri']
            
            artist_name = item['artists'][0]['name']
            artist_id = item['artists'][0]['id']
            artist_uri = item['artists'][0]['uri']
            
            # features = sp.audio_features(tracks=track_id)
            # acousticness = features[0]["acousticness"]
            # danceability = features[0]["danceability"]
            # energy = features[0]["energy"]
            # liveness = features[0]["liveness"]
            # loudness = features[0]["loudness"]
            # valence = features[0]["valence"]
            # mode = features[0]["mode"]
            
            duration_ms = item['duration_ms']
            popularity = item['popularity']
            release_date = item['album']['release_date']

            tracks.append({
            "track_name": track_name,
            "track_id": track_id,
            "track_uri": track_uri,
            
            "artist_name": artist_name,
            "artist_id": artist_id,
            "artist_uri": artist_uri,
            
            # "acousticness": acousticness,
            # "danceability": danceability,
            # "energy": energy,
            # "liveness": liveness,
            # "loudness": loudness,
            # "valence": valence,
            # "mode": mode
            
            "duration_ms": duration_ms,
            "popularity": popularity,
            "release_date": release_date
            })
            
    return pd.DataFrame(tracks)