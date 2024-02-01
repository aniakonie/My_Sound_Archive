from website.spotify.sp_API_requests import spotify_req_get_users_saved_tracks, spotify_req_get_users_playlists, spotify_req_get_playlist_items, spotify_req_get_current_user_profile

# passes: current_user_profile_data, spotify_saved_tracks, spotify_all_playlists_tracks, spotify_playlists to "extracting_tracks_for_database.py"


def get_current_user_profile_data(access_token):

    current_user_profile_data = spotify_req_get_current_user_profile(access_token)
    return current_user_profile_data
    

def get_spotify_saved_tracks(access_token):
    '''adding batches of retrieved 50 songs to make a whole list of songs'''

    spotify_saved_tracks = get_spotify_response_all_items(spotify_req_get_users_saved_tracks, access_token)
    return spotify_saved_tracks


def get_spotify_playlists_songs_all_playlists_together(access_token):
    '''adding songs from all playlists'''

    spotify_playlists = get_spotify_playlists(access_token)
    spotify_playlists_ids = get_spotify_playlists_ids(spotify_playlists)

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
        spotify_playlist_items_response = spotify_req_get_playlist_items(access_token, offset, playlist_id)
        spotify_playlist_items_50items = spotify_playlist_items_response['items']
        if len(spotify_playlist_items_50items) == 0:
            break
        spotify_playlist_tracks.extend(spotify_playlist_items_50items)
        offset += 50
    return spotify_playlist_tracks


def get_spotify_playlists_ids(spotify_playlists):

    spotify_playlists_ids = set()
    for playlist in spotify_playlists:
        spotify_playlists_ids.add(playlist["id"])

    return spotify_playlists_ids


def get_spotify_response_all_items(spotify_req, access_token):

    offset = 0
    spotify_response_all_items = []

    while True:
        spotify_response = spotify_req(access_token, offset)
        spotify_50items = spotify_response['items']
        if len(spotify_50items) == 0:
            break
        spotify_response_all_items.extend(spotify_50items)
        offset += 50
    return spotify_response_all_items

