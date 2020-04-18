from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseServerError

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import time

import sys
sys.path.append('../')

import api.web as web_utils
import api.spotify as spotify
import api.utils as utils
from api.spotify import SpotifyClient

# Create your views here.
def index(request):
    return render(request, 'tunelyze/index.html', {'message': 'Please connect to Spotify.'})

def auth(request):
    sp_oauth, redirect_uri = web_utils.get_oauth(request, 'config.yml')

    auth_url = sp_oauth.get_authorize_url()
    return HttpResponseRedirect(auth_url)

def auth_callback(request):
    sp_oauth, redirect_uri = web_utils.get_oauth(request, 'config.yml')
    token = "{}?{}".format(redirect_uri, request.GET.urlencode())
    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)

    if token_info:
        request.session['access_token'] = token_info['access_token']
        request.session['token_expries_at'] = token_info['expires_at']

        return HttpResponseRedirect('/tunelyze/you/')
    else:
        return HttpResponseRedirect('/tunelyze/login_failed/')

def auth_success(request):
    valid, ret_val = check_validity(request)
    if not valid:
        return HttpResponseRedirect('/tunelyze/auth/')
    sp = ret_val

    current_user = sp.get_current_user()
    return render(request, 'tunelyze/auth_success.html', {'name': current_user.name, 'icon_url': current_user.icon_url})

def auth_fail(request):
    return render(request, 'tunelyze/auth_fail.html', {})

def get_saved_albums(request):
    valid, ret_val = check_validity(request)
    if not valid:
        return ret_val
    sp = ret_val

    albums = sp.get_saved_albums()

    return JsonResponse({
        'albums': utils.get_dict_list(albums)
    })

def get_playlists(request):
    valid, ret_val = check_validity(request)
    if not valid:
        return ret_val
    sp = ret_val

    playlists = sp.get_playlists()

    return JsonResponse({
        'playlists': utils.get_dict_list(playlists)
    })

def get_tracks(request):
    valid, ret_val = check_validity(request)
    if not valid:
        return ret_val
    sp = ret_val

    saved_tracks = request.GET.get('saved') == "true"

    albums = request.GET.get('albums')
    album_ids = [] if albums == "" else albums[0:-1].split(',')

    playlists = request.GET.get('playlists')
    playlists_ids = [] if playlists == "" else playlists[0:-1].split(',')

    tracks = sp.get_tracks(saved_tracks, album_ids, playlists_ids)
    sp.load_features(tracks)

    return JsonResponse({
        'tracks': utils.get_dict_list(tracks)
    })

def make_playlist(request):
    valid, ret_val = check_validity(request)
    if not valid:
        return ret_val
    sp = ret_val

    name = request.GET.get('name')

    tracks = request.GET.get('tracks')
    track_ids = [] if tracks == "" else tracks[0:-1].split(',')

    plist_id = sp.create_playlist(name, track_ids)

    return JsonResponse({
        'id': str(plist_id)
    })

def check_validity(request):
    try:
        token_expries_at = request.session['token_expries_at']
        if token_expries_at < time.time():
            raise Exception("Token expired. User needs to renew token or log in again.")
        sp = SpotifyClient(request.session['access_token'])
        return True, sp
    except:
        return False, HttpResponseServerError('Spotify authorization failed.')