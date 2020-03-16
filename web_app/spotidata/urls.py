from django.urls import path

from . import views

urlpatterns = [
    path('',               views.index,         name='index'),
    path('auth/',          views.auth,          name='auth'),
    path('auth_callback/', views.auth_callback, name='auth_callback'),
    path('login_failed/',  views.auth_fail,     name='auth_fail'),
    path('you/',           views.auth_success,  name='auth_success'),

    path('get_saved_albums/',   views.get_saved_albums,   name='get_saved_albums'),
    path('get_playlists/',      views.get_playlists,      name='get_playlists'),
    path('get_tracks/',         views.get_tracks,         name='get_tracks'),
]