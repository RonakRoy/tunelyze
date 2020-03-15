import sys
sys.path.append('../')

import api.spotify as spotify
import api.utils as utils
from api.spotify import FeatureType, FeatureFilter
import clt.input_tools as clinput

import clt.spotidata as spotidata

username, scope = spotidata.boot('../config.yml')

print("="*25)
print("{:^25s}".format("spotidata"))
print("="*25)

print("Welcome to spotidata! Let's learn some more about your music taste.")
print()
print("Before we get started, you'll need to grant me access to your Spotify account. I'm attempting to login to Spotify user {}.".format(username))

with spotify.login(username, scope) as sp:
    print()
    print("Now that I have access to your deepest, darkest music secrets, let's begin. First, you'll need to choose what music you want me to analyze.")
    use_saved_tracks = clinput.input_boolean("Do you want me to analyze your saved songs?")
    
    print()
    print("Cool. Now let's look at your saved albums. I've taken initiative and listed them out here:")
    queried_albums = clinput.input_sublist("Which albums would you like to include in the analysis?", sp.get_saved_albums())

    print()
    print("One last thing: your playlists.")
    queried_playlists = clinput.input_sublist("Which playlists would you like to include in the analysis?", sp.get_playlists())

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

    for line in spotidata.get_delimited_spreadsheet(sp, use_saved_tracks, queried_albums, queried_playlists, '---'):
        print(line)

    print()
    print()

    # filters = {
    #     FeatureType.DANCEABILITY: None,
    #     FeatureType.ENERGY: None,
    #     FeatureType.KEY: FeatureFilter(FeatureType.KEY, values=['A', 'C', 'E']),
    #     FeatureType.MODE: None,
    #     FeatureType.SPEECHINESS: FeatureFilter(FeatureType.SPEECHINESS, min_val=0.25, max_val=0.5),
    #     FeatureType.ACOUSTICNESS: None,
    #     FeatureType.INSTRUMENTALNESS: None,
    #     FeatureType.LIVENESS: None,
    #     FeatureType.VALENCE: None,
    #     FeatureType.TEMPO: None
    # }