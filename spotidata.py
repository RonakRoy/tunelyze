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

scope = 'user-library-read playlist-read-private playlist-read-collaborative'

print("="*25)
print("{:^25s}".format("spotidata"))
print("="*25)

print("Welcome to spotidata! Let's learn some more about your music taste.")
print()
print("Before we get started, you'll need to grant me access to your Spotify account.")

username = input("Enter your Spotify username to get connected (or just hit enter to use the one in config.yml): ")
if username == "":
    username = config['username']

with api.login(username, scope) as sp:
    print()
    print("Now that I have access to your deepest, darkest music secrets, let's begin. First, you'll need to choose what music you want me to analyze.")
    use_saved_tracks = utils.input_boolean("Do you want me to analyze your saved songs?")
    
    print()
    print("Cool. Now let's look at your saved albums. I've taken initiative and listed them out here:")
    queried_albums = utils.input_sublist("Which albums would you like to include in the analysis?", sp.get_saved_albums())

    print()
    print("One last thing: your playlists.")
    queried_playlists = utils.input_sublist("Which playlists would you like to include in the analysis?", sp.get_playlists())

    print()
    print()
    print("Alright, that's all I need. I'm going to give you everything you could possibly want to know about soungs from:")
    if use_saved_tracks:
        print("  - your Saved Music library")
    if len(queried_albums) != 0:
        print("  - the following albums: {}".format(utils.get_english_list(queried_albums)))
    if len(queried_playlists) != 0:
        print("  - the following playlists: {}".format(utils.get_english_list(queried_playlists)))

    print("="*25)

    delim = "---"

    print("Song Title{d}Artists{d}Energy{d}Danceability{d}Key{d}Loudness{d}Mode{d}Speechiness{d}Acousticness{d}Instrumentalness{d}Liveness{d}Valence{d}Tempo".format(d=delim))
    for track in sp.get_tracks(use_saved_tracks, queried_albums, queried_playlists):
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