from flask import Blueprint, render_template, request, url_for, redirect
from dotenv import load_dotenv
import os
import requests
import urllib.parse
import base64
from flask_login import login_required, current_user
from website.spotify.spotify_data import *
from website.spotify.parse import *
from website.spotify.save_to_database import *
from website.database.models import db, UserMusicPlatform

spotify_bp = Blueprint('spotify_bp', __name__, template_folder="templates")

load_dotenv()

@spotify_bp.route('/authorization')
@login_required
def authorization():
    '''requesting authorization from Spotify to access data
    using client id from app registration on spotify dev'''
    spotify_login_page_url = request_authorization()
    return redirect(spotify_login_page_url)


@spotify_bp.route('/callback')
@login_required
def callback():
    '''in case user accepted app's request and logged in:
    retrieving query parameters (code and state) from spotify callback'''

    state_received = request.args.get("state")
    #TODO compare received state with the one which was sent before
    
    try:
        code = request.args.get("code")
    except:
        error = request.args.get("error")

    access_token, refresh_token = get_token(code)
    save_token(access_token, refresh_token)
    return redirect(url_for("spotify_bp.successfully_logged_in_to_spotify"))


@spotify_bp.route('/create_library', methods=["POST", "GET"])
@login_required
def successfully_logged_in_to_spotify():
    if request.method == "POST":
        create_library_response = eval(request.form["create_library"])
        if not create_library_response:
            #TODO delete user's music platform row
            return redirect(url_for("home_bp.home"))
        else:
            create_library()
    return render_template("spotify/create_library.html")


def request_authorization():
    client_id = os.getenv("CLIENT_ID")
    response_type = 'code'
    redirect_uri = 'http://127.0.0.1:5000/spotify/callback'
    scope = 'user-library-read playlist-read-private user-follow-read user-read-private user-read-email'
    state = 'fgfrgwgawgwwe' #TODO store it somewhere
    params = {'client_id': client_id, 'response_type': response_type, 'redirect_uri': redirect_uri, 'scope': scope, 'state': state}
    authorize_url = 'https://accounts.spotify.com/authorize'
    spotify_login_page_url = authorize_url + '?' + urllib.parse.urlencode(params)
    #TODO add a behaviour for response status other than 200
    return spotify_login_page_url


def get_token(code):
    '''exchanging authorization code for an access token - post request to the token endpoint'''
    redirect_uri = 'http://127.0.0.1:5000/spotify/callback'
    grant_type = 'authorization_code'
    params = {'grant_type': grant_type, 'code': code, 'redirect_uri': redirect_uri}
    access_token_response_dict = token_request(params)
    access_token = access_token_response_dict['access_token']
    refresh_token = access_token_response_dict['refresh_token']
    return access_token, refresh_token


def do_refresh_token(refresh_token):
    grant_type = 'refresh_token'
    params = {'grant_type': grant_type, 'refresh_token': refresh_token}
    access_token_response_dict = token_request(params)
    access_token = access_token_response_dict['access_token']
    save_token(access_token, refresh_token)
    return access_token


def token_request(params):
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    get_token_base_url = 'https://accounts.spotify.com/api/token'
    get_token_url = get_token_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + convert_to_base64_str(client_id + ':' + client_secret)
    }
    access_token_response = requests.post(get_token_url, headers=headers)
    access_token_response_dict = access_token_response.json()
    return access_token_response_dict


def save_token(access_token, refresh_token):
    music_platform_id = get_music_platform_id(access_token)
    user = UserMusicPlatform.query.filter_by(user_id = current_user.id).first()
    if not user:
        new_user = UserMusicPlatform("Spotify", music_platform_id, access_token, refresh_token, current_user.id)
        db.session.add(new_user)
        db.session.commit()
    else:
        user.access_token = access_token
        db.session.add(user)
        db.session.commit()
        return access_token


def create_library():
    user = UserMusicPlatform.query.filter_by(user_id = current_user.id).first()
    access_token = user.access_token
    refresh_token = user.refresh_token
    is_valid = check_token_validity(access_token)
    if is_valid == False:
        access_token = do_refresh_token(refresh_token)

    spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks = get_spotify_data(access_token)
    music_platform_id = user.music_platform_id
    playlists_info_library, saved_tracks_library, all_playlists_tracks_library = parse(spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks, music_platform_id)
    save_to_dabatase(playlists_info_library, saved_tracks_library, all_playlists_tracks_library)


def check_token_validity(access_token):
    '''making an API request to check the type of response'''
    response = spotify_req_get_current_user_profile(access_token)
    if response.status_code == 401:
        return False
    else:
        return True


def convert_to_base64_str(data):
    data_bytes = data.encode('ascii')
    data_base64_str = base64.b64encode(data_bytes).decode()
    return data_base64_str

