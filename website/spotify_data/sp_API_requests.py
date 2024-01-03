import requests
import urllib.parse



def spotify_request(base_url, offset, access_token):

    params = {'limit': 50, 'offset': offset}
    url = base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_response = (requests.get(url, headers=headers)).json()
    return spotify_response


def spotify_req_get_users_saved_tracks(access_token, offset):
    '''retrieving 50 saved songs from spotify at a time'''

    base_url = 'https://api.spotify.com/v1/me/tracks'
    spotify_saved_tracks_response = spotify_request(base_url, offset, access_token)
    return spotify_saved_tracks_response


def spotify_req_get_users_playlists(access_token, offset):
    '''retrieving info about 50 playlists from spotify at a time'''

    base_url = 'https://api.spotify.com/v1/me/playlists'
    spotify_playlists_response = spotify_request(base_url, offset, access_token)
    return spotify_playlists_response


def spotify_req_get_playlist_items(access_token, offset, playlist_id):
    '''retrieving 50 songs from spotify's particular playlist at a time'''

    base_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    spotify_playlist_items_response = spotify_request(base_url, offset, access_token)
    return spotify_playlist_items_response


def spotify_req_get_current_user_profile(access_token):
    get_user_base_url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    current_user_profile_data_response = (requests.get(get_user_base_url, headers=headers)).json()
    return current_user_profile_data_response
