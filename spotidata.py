import json
import yaml
import os

import api
import utils

with open('config.yml', 'r') as config_stream:
    try:
        config = yaml.safe_load(config_stream)
    except yaml.YAMLError as e:
        print(e)

os.environ['SPOTIPY_CLIENT_ID'] = config['client_id']
os.environ['SPOTIPY_CLIENT_SECRET'] = config['client_secret']
os.environ['SPOTIPY_REDIRECT_URI'] = config['redirect_uri']

username = config['username']
scope = 'user-library-read playlist-read-private'

with api.login(username, scope) as sp:
    delim = "---"

    saved_tracks = sp.get_saved_tracks()

    print("Saved tracks")
    print("="*12)
    print("Song Title{d}Artists{d}Energy{d}Danceability{d}Key{d}Loudness{d}Mode{d}Speechiness{d}Acousticness{d}Instrumentalness{d}Liveness{d}Valence{d}Tempo".format(d=delim))

    for track in saved_tracks:
        features = sp.get_features(track)
        print("{name}{d}{artists}{d}{features}".format(
            d = delim,
            name = track.name,
            artists = utils.get_english_list(track.artists),
            features = utils.get_delimited_list(
                [features.danceability, features.energy, features.key, features.loudness, features.mode, features.speechiness, features.acousticness, features.instrumentalness, features.liveness, features.valence, features.tempo],
                delim
            )
        ))

    print("You have saved a total of {} tracks.".format(len(saved_tracks)))