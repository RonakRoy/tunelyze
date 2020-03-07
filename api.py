import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import utils

class login(object):
    def __init__(self, username, scope):
        self.username = username
        self.scope = scope
        
    def __enter__(self): 
        self.token = spotipy.util.prompt_for_user_token(self.username, self.scope)

        if self.token:
            self.sp = SpotifyClient(self.token)
            return self.sp
        else:
            raise
            print("Can't get token for", username)
  
    def __exit__(self, a, b, c):
        pass

class SpotifyClient(object):
    def __init__(self, token):
        self.sp = spotipy.Spotify(auth=token)
        self.sp.max_get_retries = 5

    def get_saved_tracks(self):
        saved_tracks = []

        offset = 0
        batch_size = 50

        total = None

        while True:
            if total == None or offset <= total:
                results = self.sp.current_user_saved_tracks(limit=batch_size, offset=offset)
                saved_tracks += [Track(result['track']) for result in results['items']]
                offset += batch_size
            else:
                break

            if total == None:
                total = results['total']

        return saved_tracks

    def get_features(self, track):
        results = self.sp.audio_features(track.id)

        return Features(results[0])

class Track(object):
    def __init__(self, spotipy_track):
        self.name = spotipy_track['name']
        self.artists = [artist['name'] for artist in spotipy_track['artists']]
        self.id = spotipy_track['id']

class Features(object):
    def __init__(self, spotipy_features):
        self.danceability = spotipy_features['danceability']
        self.energy = spotipy_features['energy']
        self.key = utils.get_alpha_key(spotipy_features['key'])
        self.loudness = spotipy_features['loudness']
        self.mode = 'major' if spotipy_features['mode'] == 1 else 'minor'
        self.speechiness = spotipy_features['speechiness']
        self.acousticness = spotipy_features['acousticness']
        self.instrumentalness = spotipy_features['instrumentalness']
        self.liveness = spotipy_features['liveness']
        self.valence = spotipy_features['valence']
        self.tempo = spotipy_features['tempo']