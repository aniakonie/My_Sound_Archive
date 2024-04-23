import requests
import urllib.parse


def get_music_platform_id(access_token):
    current_user_profile_data_response = spotify_req_get_current_user_profile(access_token)
    status_code = current_user_profile_data_response.status_code
    if status_code == 403:
        music_platform_id = None
        return music_platform_id, status_code
    else:
        current_user_profile_data = current_user_profile_data_response.json() 
        music_platform_id = current_user_profile_data["id"]
        return music_platform_id, status_code


def get_spotify_data(access_token):

    spotify_playlists = get_spotify_playlists(access_token)
    print("playlists retrieved")
    spotify_saved_tracks = get_spotify_saved_tracks(access_token)
    print("saved tracks retrieved")
    spotify_all_playlists_tracks = get_spotify_all_playlists_tracks(access_token)
    print("playlists tracks retrieved")
    return spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks

    
def get_spotify_saved_tracks(access_token):
    '''adding batches of retrieved 50 songs to make a whole list of songs'''

    spotify_saved_tracks = get_spotify_response_all_items(spotify_req_get_users_saved_tracks, access_token)
    return spotify_saved_tracks


def get_spotify_all_playlists_tracks(access_token):
    '''adding songs from all playlists'''

    spotify_playlists = get_spotify_playlists(access_token)
    music_platform_id, status_code = get_music_platform_id(access_token)
    spotify_playlists_ids = get_spotify_playlists_ids(spotify_playlists, music_platform_id)
    spotify_all_playlists_tracks = {}

    # adding songs of each playlist to a dictionary: key = playlist_id, value: list of songs
    for playlist_id in spotify_playlists_ids:
        spotify_playlist_tracks = get_spotify_playlist_songs_one_playlist(access_token, playlist_id)
        spotify_all_playlists_tracks[playlist_id] = spotify_playlist_tracks
    return spotify_all_playlists_tracks


def get_spotify_playlists(access_token):
    '''adding batches of retrieved 50 playlists data to make a whole list of playlists data'''

    spotify_playlists = get_spotify_response_all_items(spotify_req_get_users_playlists, access_token)
    return spotify_playlists


def get_spotify_playlist_songs_one_playlist(access_token, playlist_id):
    '''adding batches of retrieved 50 songs from spotify's particular playlist to make a whole list of one playlist's songs'''

    spotify_playlist_tracks = []
    offset = 0

    while True:
        spotify_playlist_items_response, status_code = spotify_req_get_playlist_items(access_token, offset, playlist_id)
        print(status_code)

        spotify_playlist_items_50items = spotify_playlist_items_response['items']
        if len(spotify_playlist_items_50items) == 0:
            break
        spotify_playlist_tracks.extend(spotify_playlist_items_50items)
        offset += 50
    return spotify_playlist_tracks


def get_spotify_playlists_ids(spotify_playlists, music_platform_id):

    spotify_playlists_ids = set()
    for playlist in spotify_playlists:
        if playlist["owner"]["id"] == music_platform_id:
            spotify_playlists_ids.add(playlist["id"])
    return spotify_playlists_ids


# REQUESTS OFFSET

def get_spotify_response_all_items(spotify_req_function, access_token):

    offset = 0
    spotify_response_all_items = []

    while True:
        spotify_response, status_code = spotify_req_function(access_token, offset)
        print(status_code)
        spotify_50items = spotify_response['items']
        if len(spotify_50items) == 0:
            break
        spotify_response_all_items.extend(spotify_50items)
        offset += 50
    return spotify_response_all_items


# SPOTIFY API REQUESTS

def spotify_request(base_url, offset, access_token):

    params = {'limit': 50, 'offset': offset}
    url = base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_response_json = requests.get(url, headers=headers)
    status_code = spotify_response_json.status_code
    spotify_response = spotify_response_json.json()
    return spotify_response, status_code


def spotify_req_get_users_saved_tracks(access_token, offset):
    '''retrieving 50 saved songs from spotify at a time'''

    base_url = 'https://api.spotify.com/v1/me/tracks'
    spotify_saved_tracks_response, status_code = spotify_request(base_url, offset, access_token)
    return spotify_saved_tracks_response, status_code


def spotify_req_get_users_playlists(access_token, offset):
    '''retrieving info about 50 playlists from spotify at a time'''

    base_url = 'https://api.spotify.com/v1/me/playlists'
    spotify_playlists_response, status_code = spotify_request(base_url, offset, access_token)
    return spotify_playlists_response, status_code


def spotify_req_get_playlist_items(access_token, offset, playlist_id):
    '''retrieving 50 songs from spotify's particular playlist at a time'''
    base_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    spotify_playlist_items_response, status_code = spotify_request(base_url, offset, access_token)
    return spotify_playlist_items_response, status_code


def spotify_req_get_current_user_profile(access_token):
    get_user_base_url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    current_user_profile_data_response = requests.get(get_user_base_url, headers=headers)
    return current_user_profile_data_response
