import requests
import urllib.parse



def spotify_req_get_users_saved_tracks(access_token, offset):
    '''retrieving 50 saved songs from spotify at a time'''

    get_tracks_base_url = 'https://api.spotify.com/v1/me/tracks'
    params = {'limit': 50, 'offset': offset}
    get_tracks_url = get_tracks_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_saved_tracks_response = (requests.get(get_tracks_url, headers=headers)).json()
    return spotify_saved_tracks_response



def spotify_req_get_users_playlists(access_token, offset):
    '''retrieving info about 50 playlists from spotify at a time'''

    get_playlists_base_url = 'https://api.spotify.com/v1/me/playlists'
    params = {'limit': 50, 'offset': offset}
    get_playlists_url = get_playlists_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_playlists_response = (requests.get(get_playlists_url, headers=headers)).json()
    return spotify_playlists_response



def spotify_req_get_playlist_items(access_token, offset, playlist_id):
    '''retrieving 50 songs from spotify's particular playlist at a time'''
    get_playlist_items_base_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    params = {'limit': 50, 'offset': offset}
    get_playlist_items_url = get_playlist_items_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_playlist_items_response = (requests.get(get_playlist_items_url, headers=headers)).json()
    return spotify_playlist_items_response



def spotify_req_get_current_user_profile(access_token):
    get_user_base_url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    current_user_profile_data_response = (requests.get(get_user_base_url, headers=headers)).json()
    return current_user_profile_data_response

