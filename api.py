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
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "{} by {}".format(self.name, utils.get_english_list(self.artists))

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