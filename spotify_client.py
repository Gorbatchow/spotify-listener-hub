import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import requests
import pandas as pd

load_dotenv()
freqblog_key = os.getenv("FREQBLOG_API_KEY")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

results = sp.current_user_saved_tracks(limit=50)
all_saved_tracks = results['items']

payload = []
for idx, item in enumerate(all_saved_tracks):
    track = item['track']
    artist_name = track['artists'][0]['name']
    track_name = track['name']

    payload.append({"artist": artist_name, "track": track_name})

response = requests.post(
    "https://api.freqblog.com/bulk",
    headers={"X-Api-Key": freqblog_key},
    json=payload
)

if response.status_code == 200:
    data = response.json()

    tracks_features = []
    for item in data.get("results", []):
        artist = item.get("artist")
        track_name = item.get("track")

        stats = item.get("result", {})

        tracks_features.append(
            {
                "artist": artist,
                "track": track_name,
                "bpm": stats.get("bpm"),
                "energy": stats.get("energy"),
                "danceability": stats.get("danceability")
            }
        )
        if stats:
            print(f"{idx + 1}.{artist} - {track_name} | BPM: {stats.get('bpm')}, Energy: {stats.get('energy')}, Danceability: {stats.get('danceability')}")
        else:
            print(f"{idx + 1}.{artist} - {track_name} | Brak statystyk")
    df = pd.DataFrame(tracks_features)
    print(df.head(10)) 
else:
    print(f"\nStatus: {response.status_code} - {response.text}")  