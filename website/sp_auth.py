from flask import Blueprint
from website.spotify_data.sp_get_library import get_spotify_saved_tracks, extract_track_data, get_spotify_playlists_ids
from dotenv import load_dotenv
import os
import time
import requests
import urllib.parse
import base64
from flask import Flask, request, url_for, session, redirect
from website.spotify_data.spotify_database import initialize_spotify_database, create_spotify_database
from website.spotify_data.sp_get_artists_genres import sp_get_artists_genres

sp_auth = Blueprint('sp_auth', '__name__')

load_dotenv()



@sp_auth.route('/')
def request_authorization():
	
    #requesting authorization from Spotify to access data (get request to the authorize endpoint)
    #using client id from app registration on spotify dev

    client_id = os.getenv("CLIENT_ID")
    response_type = 'code'
    redirect_uri = 'http://127.0.0.1:5000/sp_auth/redirect'
    scope = 'user-library-read playlist-read-private user-follow-read user-read-private user-read-email'
    state = 'fgfrgwgawgwwe' #ZAMIENIĆ NA RANDOM STRING

    params = {'client_id': client_id, 'response_type': response_type, 'redirect_uri': redirect_uri, 'scope': scope, 'state': state}
    authorize_url = 'https://accounts.spotify.com/authorize'
    spotify_login_page_url = authorize_url + '?' + urllib.parse.urlencode(params)

    # dodać, że jeśli status jest inny niż 200, to przekierować gdzieś tam?

    return redirect(spotify_login_page_url)

#our endpoint to which spotify sends back code and state
@sp_auth.route('/redirect')
def redirect_page():

    #user accepted app's request and logged in
    #retrieving query parameters (code and state) from spotify callback

    state_received = request.args.get("state")

    # if state_received != state:
    #     pass #jakoś zakończyć proces autoryzacji
    # else:
    #     print('Go on')
    
    try:
        code = request.args.get("code")

    except:
        error = request.args.get("error")


    #exchanging authorization code for an access token - post request to the api/token endpoint

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = 'http://127.0.0.1:5000/sp_auth/redirect'
    grant_type = 'authorization_code'

    params = {'grant_type': grant_type, 'code': code, 'redirect_uri': redirect_uri}
    get_token_base_url = 'https://accounts.spotify.com/api/token'
    get_token_url = get_token_base_url + '?' + urllib.parse.urlencode(params)


    def convert_to_base64_str(data):

        data_bytes = data.encode('ascii')
        data_base64 = base64.b64encode(data_bytes)
        data_base64_str = data_base64.decode()
        return data_base64_str

    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + convert_to_base64_str(client_id + ':' + client_secret)
    }

    access_token_response = requests.post(get_token_url, headers=headers)

    access_token_response_json = access_token_response.json()

    access_token = access_token_response_json['access_token']
    refresh_token = access_token_response_json['refresh_token']
    expires_in = access_token_response_json['expires_in']
    token_type = access_token_response_json['token_type']

    # current_user_profile_data = get_current_user_profile(access_token)

    # spotify_saved_tracks = get_spotify_saved_tracks(access_token)
    # saved_tracks_library, artists_uris = extract_track_data(spotify_saved_tracks)

    spotify_playlists = get_spotify_playlists_ids(access_token, '1182179835')

    return spotify_playlists


def refresh_token():
    pass


def get_current_user_profile(access_token):
    get_user_base_url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    current_user_profile_data = (requests.get(get_user_base_url, headers=headers)).json()
    return current_user_profile_data

