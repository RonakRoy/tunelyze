from enum import Enum

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import api.utils as utils

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

    def _get(self, batch_size, spotipy_get_function, process):
        offset = 0
        total = None

        while True:
            if total == None or offset <= total:
                results = spotipy_get_function(limit=batch_size, offset=offset)
                for result_item in results['items']:
                    yield process(result_item) 
                offset += batch_size
            else:
                break

            if total == None:
                total = results['total']

    def get_playlists(self):
        playlists = []
        for playlist in self._get(50, self.sp.current_user_playlists, lambda result_item : Playlist(result_item)):
            playlists.append(playlist)

        return playlists

    def get_saved_albums(self):
        albums = []
        for album in self._get(50, self.sp.current_user_saved_albums, lambda result_item : Album(result_item['album'])):
            albums.append(album)

        return albums 

    def get_tracks(self, saved=True, albums=[], playlists=[]):
        tracks = set()

        if saved:
            for track in self.get_saved_tracks():
                tracks.add(track)

        for album in albums:
            for track in self.get_album_tracks(album):
                tracks.add(track)

        for playlist in playlists:
            for track in self.get_playlist_tracks(playlist):
                tracks.add(track)
                
        return tracks
    
    def get_saved_tracks(self):
        return self._get(50, self.sp.current_user_saved_tracks, lambda result_item : Track(result_item['track']))

    def get_album_tracks(self, album):
        return self._get(50, lambda limit, offset : self.sp.album_tracks(album.id, limit=limit, offset=offset), lambda result_item : Track(result_item))

    def get_playlist_tracks(self, playlist):
        return self._get(50, lambda limit, offset : self.sp.playlist_tracks(playlist.id, limit=limit, offset=offset), lambda result_item : Track(result_item['track']))

    def get_features(self, track):
        return Features(self.sp.audio_features(track.id)[0])

    def get_tracks_that_satisfy_predicate(self, tracks, predicate):
        for track in tracks:
            if predicate(track):
                yield track

    def create_playlist(self, name, tracks):
        pl = self.sp.user_playlist_create(self.sp.current_user()['id'], name)

        batch_size = 80
        
        track_ids = []
        for track in tracks:
            track_ids.append(track.id)

            if len(track_ids) >= batch_size:
                self.sp.user_playlist_add_tracks(self.sp.current_user()['id'], pl['id'], track_ids)
                track_ids = []

        if len(track_ids) != 0:
            self.sp.user_playlist_add_tracks(self.sp.current_user()['id'], pl['id'], track_ids)

class Artist(object):
    def __init__(self, spotipy_artist):
        self.name = spotipy_artist['name']
        self.id = spotipy_artist['id']
    
    def __str__(self):
        return self.name

class Album(object):
    def __init__(self, spotipy_album):
        self.name = spotipy_album['name']
        self.artists = [Artist(spotipy_artist) for spotipy_artist in spotipy_album['artists']]
        self.id = spotipy_album['id']
    
    def __str__(self):
        return "{} by {}".format(self.name, utils.get_english_list(self.artists))

class Playlist(object):
    def __init__(self, spotipy_playlist):
        self.name = spotipy_playlist['name']
        self.id = spotipy_playlist['id']
        self.collab = spotipy_playlist

    def __str__(self):
        return self.name

class Track(object):
    def __init__(self, spotipy_track):
        self.name = spotipy_track['name']
        self.artists = [Artist(spotipy_artist) for spotipy_artist in spotipy_track['artists']]
        self.id = spotipy_track['id']

    def load_features(self, spotify_client):
        self.features = spotify_client.get_features(self)

        return self.features

    def get_feature(self, feature_type):
        if self.features == None:
            raise

        if   feature_type == FeatureType.DANCEABILITY:
            return self.features.danceability
        elif feature_type == FeatureType.ENERGY:
            return self.features.energy
        elif feature_type == FeatureType.KEY:
            return self.features.key
        elif feature_type == FeatureType.LOUDNESS:
            return self.features.loudness
        elif feature_type == FeatureType.MODE:
            return self.features.mode
        elif feature_type == FeatureType.SPEECHINESS:
            return self.features.speechiness
        elif feature_type == FeatureType.ACOUTSTICNESS:
            return self.features.acousticness
        elif feature_type == FeatureType.INSTRUMENTALNESS:
            return self.features.instrumentalness
        elif feature_type == FeatureType.LIVENESS:
            return self.features.liveness
        elif feature_type == FeatureType.VALENCE:
            return self.features.valence
        elif feature_type == FeatureType.TEMPO:
            return self.features.tempo
    
    def satisfies_all(self, feature_filters):
        for feature_filter in feature_filters:
            if not feature_filter.is_satisfied_by(self):
                return False
        return True

    def satisfies_any(self, feature_filters):
        for feature_filter in feature_filters:
            if feature_filter.is_satisfied_by(self):
                return True
        return False

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "{} by {}".format(self.name, utils.get_english_list(self.artists))

class FeatureType(Enum):
    DANCEABILITY = (0, (0.0, 1.0))
    ENERGY = (1, (0.0, 1.0))
    KEY = (2, ['C', 'C#/D♭', 'D', 'D#/E♭', 'E', 'F', 'F#/G♭', 'G', 'G#/A♭', 'A', 'A#/B♭', 'B'])
    LOUDNESS = (3, (-120.0, 0.0))
    MODE = (3, ['minor', 'major'])
    SPEECHINESS = (4, (0.0, 1.0))
    ACOUTSTICNESS = (5, (0.0, 1.0))
    INSTRUMENTALNESS = (6, (0.0, 1.0))
    LIVENESS = (7, (0.0, 1.0))
    VALENCE = (8, (0.0, 1.0))
    TEMPO = (9, (0.0, 300.0))

class FeatureFilter(object):
    def __init__(self, feature_type, values=None, min_val=None, max_val=None):
        self.feature_type = feature_type
        if isinstance(feature_type.value[1], tuple):
            if min_val > max_val or min_val < feature_type.value[1][0] or max_val > feature_type.value[1][1]:
                raise
            self.min_val = min_val
            self.max_val = max_val
        else:
            for value in values:
                if not value in feature_type.value[1]:
                    raise
            self.values = values
    
    def is_satisfied_by(self, track):
        feature_val = track.get_feature(self.feature_type)
        if isinstance(self.feature_type.value[1], tuple):
            return feature_val >= self.min_val and feature_val <= self.max_val
        else:
            return feature_val in self.values

    def __str__(self):
        if isinstance(self.feature_type.value[1], tuple):
            return "between {} and {}".format(self.min_val, self.max_val)
        else:
            return "one of {}".format(utils.get_english_list(self.values))

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