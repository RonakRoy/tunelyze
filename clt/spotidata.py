import sys

sys.path.append('../')

import api.spotify as spotify
import api.utils as utils
from api.spotify import FeatureType, FeatureFilter
import clt.input_tools as clinput

def boot(config_file_path):
    import os
    import sys

    import json
    import yaml

    with open(config_file_path, 'r') as config_stream:
        try:
            config = yaml.safe_load(config_stream)
        except yaml.YAMLError as e:
            print(e)

    os.environ['SPOTIPY_CLIENT_ID'] = config['client_id']
    os.environ['SPOTIPY_CLIENT_SECRET'] = config['client_secret']
    os.environ['SPOTIPY_REDIRECT_URI'] = config['redirect_uri']

    username = config['username']
    scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

    return username, scope

def get_delimited_spreadsheet(sp, use_saved_tracks, queried_albums, queried_playlists, delim):
    yield "Song Title{d}Artists{d}Energy{d}Danceability{d}Key{d}Loudness{d}Mode{d}Speechiness{d}Acousticness{d}Instrumentalness{d}Liveness{d}Valence{d}Tempo".format(d=delim)
    
    for track in sp.get_tracks(use_saved_tracks, queried_albums, queried_playlists):
        features = track.load_features(sp)
        yield ("{name}{d}{artists}{d}{features}".format(
            d = delim,
            name = track.name,
            artists = utils.get_english_list(track.artists),
            features = utils.get_delimited_list(
                [features.danceability, features.energy, features.key, features.loudness, features.mode, features.speechiness, features.acousticness, features.instrumentalness, features.liveness, features.valence, features.tempo],
                delim
            )
        ))

def get_delimited_spreadsheet(tracks, delim):
    yield "Song Title{d}Artists{d}Energy{d}Danceability{d}Key{d}Loudness{d}Mode{d}Speechiness{d}Acousticness{d}Instrumentalness{d}Liveness{d}Valence{d}Tempo".format(d=delim)
    
    for track in tracks:
        features = track.features
        yield ("{name}{d}{artists}{d}{features}".format(
            d = delim,
            name = track.name,
            artists = utils.get_english_list(track.artists),
            features = utils.get_delimited_list(
                [features.danceability, features.energy, features.key, features.loudness, features.mode, features.speechiness, features.acousticness, features.instrumentalness, features.liveness, features.valence, features.tempo],
                delim
            )
        ))