import os
import pandas as pd

def get_recommendations():
    df_user = pd.read_csv("data/saved_tracks_features.csv")
    df_db = pd.read_csv("data/Spotify-2000.csv")

    df_db = df_db.rename(columns={"Title" : "track",
                            "Artist" : "artist", 
                            "Beats Per Minute (BPM)" : "bpm", 
                            "Energy" : "energy", 
                            "Danceability" : "danceability"})

    df_db = df_db[['artist', 'track', 'bpm', 'energy', 'danceability']]
    df_db = df_db.drop_duplicates(subset=['artist', 'track'])

    user_bpm = df_user['bpm'].mean()
    user_energy = df_user['energy'].mean()
    user_dance = df_user['danceability'].mean()

    df_db['diff_bpm'] = abs(df_db['bpm'] - user_bpm) / user_bpm
    df_db['diff_energy'] = abs(df_db['energy'] - user_energy) / user_energy
    df_db['diff_dance'] = abs(df_db['danceability'] - user_dance) / user_dance

    df_db['similarity_score'] = df_db['diff_bpm'] + df_db['diff_energy'] + df_db['diff_dance']

    df_db = df_db[~df_db['track'].str.lower().isin(df_user['track'].str.lower())]
    recommendations = df_db.sort_values(by='similarity_score', ascending=True).head(10)

    return recommendations.to_dict('records')