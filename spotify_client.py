import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

def get_saved_tracks(limit=50):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

    results = sp.current_user_saved_tracks(limit=50)
    all_saved_tracks = results['items']

    payload = []
    for idx, item in enumerate(all_saved_tracks):
        track = item['track']
        artist_name = track['artists'][0]['name']
        track_name = track['name']

        payload.append({"artist": artist_name, "track": track_name})
    return payload