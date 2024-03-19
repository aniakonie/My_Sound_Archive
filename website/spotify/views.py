from flask import Blueprint, render_template, request, url_for, redirect, abort, session, flash
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
from website.library.genres_classification.genres_classification import classify_artists_genres

spotify_bp = Blueprint('spotify_bp', __name__, template_folder="templates")

load_dotenv()

@spotify_bp.route('/authorization')
@login_required
def authorization():
    '''requesting authorization from Spotify to access data
    using client id from app registration on spotify dev'''
    if current_user.is_library_created:
        abort(404)
    spotify_login_page_url = request_authorization()
    return redirect(spotify_login_page_url)


@spotify_bp.route('/callback')
@login_required
def callback():
    '''in case user accepted app's request and logged in:
    retrieving query parameters (code and state) from spotify callback'''

    state_received = request.args.get("state")
    # user tried to access this url by typing it in the browser
    if state_received == None:
        abort(401)
    else:
        pass #TODO compare received state with the one which was sent before
    # spotify sent back an error - something went wrong or user refused access to his/her spotify account
    error = request.args.get("error")
    if error != None:
        if error == "access_denied":
            flash('''Did you mean to refuse access to your Spotify account? If not, please click 'Log in to Spotify' again.
                  If you did mean it and you are not sure whether to accept it, please head over to 'How it works' page and find out more about the app.''', category="info")
            return redirect(url_for("library_bp.library"))
        else:
            flash("Oops, something went wrong. Spotify refused to cooperate. Please try again by clicking 'Log in to Spotify", category="error")
            return redirect(url_for("library_bp.library"))
    else:
        code = request.args.get("code")
        access_token, refresh_token = get_token_initial(code)
        save_token(access_token, refresh_token)
    return redirect(url_for("spotify_bp.successfully_logged_in_to_spotify"))


@spotify_bp.route('/create_library', methods=["POST", "GET"])
@login_required
def successfully_logged_in_to_spotify():
    user = UserMusicPlatform.query.filter_by(user_id = current_user.id).first()
    if not user:
        return redirect(url_for("home_bp.log_in_to_spotify"))
    if current_user.is_library_created:
        abort(401)

    if request.method == "POST":
        if request.form["create_library"] == "Changed my mind":
            return redirect(url_for("library_bp.library"))
        else:
            create_library()
            return redirect(url_for("library_bp.library"))
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


def get_token_initial(code):
    '''exchanging authorization code for an access token - post request to the token endpoint'''
    redirect_uri = 'http://127.0.0.1:5000/spotify/callback'
    grant_type = 'authorization_code'
    params = {'grant_type': grant_type, 'code': code, 'redirect_uri': redirect_uri}
    access_token_response_dict = token_request(params)
    access_token = access_token_response_dict['access_token']
    refresh_token = access_token_response_dict['refresh_token']
    return access_token, refresh_token


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


def get_access_token():
    user = UserMusicPlatform.query.filter_by(user_id = current_user.id).first()
    access_token = user.access_token
    refresh_token = user.refresh_token
    is_valid = check_token_validity(access_token)
    if is_valid == False:
        access_token = do_refresh_token(refresh_token)
    return access_token


def check_token_validity(access_token):
    '''making an API request to check the type of response'''
    response = spotify_req_get_current_user_profile(access_token)
    return response.status_code == 401


def do_refresh_token(refresh_token):
    grant_type = 'refresh_token'
    params = {'grant_type': grant_type, 'refresh_token': refresh_token}
    access_token_response_dict = token_request(params)
    access_token = access_token_response_dict['access_token']
    save_token(access_token, refresh_token)
    return access_token


def create_library():
    user = UserMusicPlatform.query.filter_by(user_id = current_user.id).first()
    access_token = get_access_token()
    spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks = get_spotify_data(access_token)
    music_platform_id = user.music_platform_id
    playlists_info_library, saved_tracks_library, all_playlists_tracks_library = parse(spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks, music_platform_id)
    save_to_dabatase(playlists_info_library, saved_tracks_library, all_playlists_tracks_library)
    print('music saved, now genres...')
    save_default_user_settings()
    classify_artists_genres()
    print('done')
    current_user.is_library_created = True
    db.session.add(current_user)
    db.session.commit()


def save_default_user_settings():
    user_settings = UserSettings(current_user.id)
    db.session.add(user_settings)
    db.session.commit()


def convert_to_base64_str(data):
    data_bytes = data.encode('ascii')
    data_base64_str = base64.b64encode(data_bytes).decode()
    return data_base64_str

