from flask import Blueprint

import spotipy
from website.spotify_data.sp_get_library import sp_get_library
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time

from flask import Flask, request, url_for, session, redirect

sp_auth = Blueprint('sp_auth', '__name__')

load_dotenv()

TOKEN_INFO = "token_info"

@sp_auth.route('/')
def login():
	auth_url = create_spotify_oauth().get_authorize_url()
	return redirect(auth_url)

@sp_auth.route('/redirect')
def redirect_page():
	session.clear()
	code = request.args.get('code')
	token_info = create_spotify_oauth().get_access_token(code)
	session[TOKEN_INFO] = token_info
	return redirect(url_for('sp_auth.library_main', external = True))


@sp_auth.route('/Library_Main')
def library_main():
	try:
		token_info = get_token()
	except:
		print("User not logged in")
		return redirect('/')

	sp = spotipy.Spotify(auth=token_info['access_token'])

	artists_uris = sp_get_library(sp)

	return artists_uris

def get_token():
	token_info = session.get(TOKEN_INFO, None)
	if not token_info:
		redirect(url_for('login', external = False))

	now = int(time.time())

	is_expired = token_info['expires_at'] - now < 60
	if(is_expired):
		spotify_oauth = create_spotify_oauth()
		token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
	return token_info


def create_spotify_oauth():
	return SpotifyOAuth(
		client_id = os.getenv("CLIENT_ID"),
		client_secret = os.getenv("CLIENT_SECRET"),
		redirect_uri = url_for('sp_auth.redirect_page', _external = True),
		scope = 'user-library-read playlist-read-private user-follow-read'
		)
