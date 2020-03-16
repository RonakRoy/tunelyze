from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import time

import sys
sys.path.append('../')

import web_utils
import api.spotify as spotify
import api.utils
from api.spotify import SpotifyClient

# Create your views here.
def index(request):
    return render(request, 'spotidata/index.html', {'message': 'Please connect to Spotify.'})

def auth(request):
    sp_oauth, redirect_uri = web_utils.get_oauth('config.yml')

    auth_url = sp_oauth.get_authorize_url()
    return HttpResponseRedirect(auth_url)

def auth_callback(request):
    sp_oauth, redirect_uri = web_utils.get_oauth('config.yml')
    token = "{}?{}".format(redirect_uri, request.GET.urlencode())
    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)

    if token_info:
        request.session['access_token'] = token_info['access_token']
        request.session['token_expries_at'] = token_info['expires_at']

        return HttpResponseRedirect('/spotidata/you/')
    else:
        return HttpResponseRedirect('/spotidata/login_failed/')

def auth_success(request):
    token_expries_at = request.session['token_expries_at']

    if token_expries_at > time.time():
        sp = SpotifyClient(request.session['access_token'])
        return render(request, 'spotidata/auth_success.html', {'name': sp.sp.current_user()['display_name'], 'id': sp.sp.current_user()['id']})
    else:
        return HttpResponseRedirect('/spotidata/auth/')

def auth_fail(request):
    return render(request, 'spotidata/auth_fail.html', {})

def get_saved_albums(request):
    sp = SpotifyClient(request.session['access_token'])

    albums = sp.get_saved_albums()

    return JsonResponse({
        'albums': api.utils.get_dict_list(albums)
    })

def get_playlists(request):
    sp = SpotifyClient(request.session['access_token'])

    albums = sp.get_playlists()

    return JsonResponse({
        'playlists': api.utils.get_dict_list(albums)
    })

def get_tracks(request):
    sp = SpotifyClient(request.session['access_token'])

    saved_tracks = request.GET.get('saved') == "true"

    albums = request.GET.get('albums')
    album_ids = [] if albums == "" else albums[0:-1].split(',')

    playlists = request.GET.get('playlists')
    playlists_ids = [] if playlists == "" else playlists[0:-1].split(',')

    tracks = sp.get_tracks(saved_tracks, album_ids, playlists_ids)

    return JsonResponse({
        'tracks': api.utils.get_dict_list(tracks)
    })
