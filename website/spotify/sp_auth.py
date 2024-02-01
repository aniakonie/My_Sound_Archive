from flask import Blueprint, render_template, request, url_for, redirect
from dotenv import load_dotenv
import os
import requests
import urllib.parse
import base64
from website.database.populating_database import psql_test
from website.database.models import db

from website.spotify.sp_controller import *

sp_auth = Blueprint('sp_auth', __name__, template_folder="templates")

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

    access_token_response_dict = access_token_response.json()

    access_token = access_token_response_dict['access_token']
    refresh_token = access_token_response_dict['refresh_token']
    expires_in = access_token_response_dict['expires_in']
    token_type = access_token_response_dict['token_type']

    # current_user_id = '1182179835'

    # at this point add this data to the database?

    psql_test(db)

    return redirect(url_for("sp_auth.successfully_logged_in_to_spotify"))



@sp_auth.route('/create_library', methods=["POST", "GET"])
def successfully_logged_in_to_spotify():

    create_library = create_library_request()

    if create_library == False:
        return redirect(url_for("general_views_bp.home"))
    if create_library == True:
        pass

    return render_template("spotify/sp_create_library.html")


def refresh_token():
    pass


