import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from config import *

def find_track_id(track, artist):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = spotify.search(q="artist:" + artist + " " + "track:" + track, type='track', limit=1)
    uri = results['tracks']['items'][0]['uri']
    return uri


def add_to_playlist(track_uri):
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public'))
    spotify.playlist_add_items(playlist_id=playlist_id, items=track_uri, position=0)