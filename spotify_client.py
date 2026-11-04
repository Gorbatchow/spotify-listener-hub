import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import requests
import pandas as pd

load_dotenv()
freqblog_key = os.getenv("FREQBLOG_API_KEY")

# Ścieżka do naszego lokalnego pliku z bazą
csv_file_path = "data/saved_tracks_features.csv"

if os.path.exists(csv_file_path):
    print("Using local csv file with saved tracks features")
    df = pd.read_csv(csv_file_path)
    print(df.head(10))
else:
    print("No CSV file found. Fetching data from Spotify and FreqBlog API")
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
        df = pd.DataFrame(tracks_features)
        df.to_csv(csv_file_path, index=False)
        print(df.head(10)) 
    else:
        print(f"\nStatus: {response.status_code} - {response.text}")  