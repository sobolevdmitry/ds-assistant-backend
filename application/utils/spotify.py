import spotipy
from spotipy.oauth2 import SpotifyOAuth
from assistant.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope="user-read-playback-state"))

def get_current_song():
    try:
        playback = sp.current_playback()
        if playback:
            return dict(id=playback['item']['id'], name=playback['item']['name'], artists=playback['item']['artists'])
        else:
            return False
    except:
        pass
    return None
