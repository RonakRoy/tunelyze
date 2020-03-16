import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json
import yaml
import os
import sys

def get_oauth(config_file_path):
    if os.path.isfile(config_file_path):
        with open(config_file_path, 'r') as config_stream:
            try:
                config = yaml.safe_load(config_stream)
            except yaml.YAMLError as e:
                print(e)

        client_id = config['client_id']
        client_secret = config['client_secret']
        redirect_uri = config['redirect_uri']
    else:
        client_id = os.environ['SPOTIPY_CLIENT_ID']
        client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']

    scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

    sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri,
                            scope=scope, cache_path=".cache-spotipy")

    return sp_oauth, redirect_uri