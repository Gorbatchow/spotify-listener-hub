import os
import requests
import pandas as pd
from spotify_client import get_saved_tracks

freqblog_key = os.getenv("FREQBLOG_API_KEY")

csv_file_path = "data/saved_tracks_features.csv"

def get_tracks_features():
    if os.path.exists(csv_file_path):
        print("Using local csv file with saved tracks features")
        df = pd.read_csv(csv_file_path)
        return df
    else:
        print("No CSV file found. Fetching data from Spotify and FreqBlog API")

        payload = get_saved_tracks()

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
            return df
        else:
            print(f"\nStatus: {response.status_code} - {response.text}")

if __name__ == "__main__":
    df = get_tracks_features()
    print(df.head(5))  