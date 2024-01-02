import requests
import urllib.parse



def get_spotify_saved_tracks(access_token):
    '''adding batches of retrieved 50 songs to make a whole list of songs''' 
    spotify_saved_tracks = []
    offset = 0

    while True:
        spotify_saved_tracks_50items = spotify_req_get_users_saved_tracks(access_token, offset)
        if len(spotify_saved_tracks_50items) == 0:
            break
        spotify_saved_tracks.extend(spotify_saved_tracks_50items)
        offset += 50
    return spotify_saved_tracks


def spotify_req_get_users_saved_tracks(access_token, offset):
    '''retrieving 50 saved songs from spotify at a time'''

    get_tracks_base_url = 'https://api.spotify.com/v1/me/tracks'
    params = {'limit': 50, 'offset': offset}
    get_tracks_url = get_tracks_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_saved_tracks_dict = (requests.get(get_tracks_url, headers=headers)).json()
    spotify_saved_tracks_50items = spotify_saved_tracks_dict['items']
    return spotify_saved_tracks_50items



def get_spotify_playlists_songs_all_playlists_together(access_token, current_user_id):
    '''adding songs from all playlists'''

    spotify_playlists_ids = get_spotify_playlists_ids(access_token, current_user_id)
    spotify_all_playlists_tracks_track_uris = set()
    spotify_all_playlists_tracks = []
    count = 0
    # retrieving songs for each playlist
    for playlist_id in spotify_playlists_ids:
        spotify_playlist_tracks = get_spotify_playlist_songs_one_playlist(access_token, playlist_id)
        print(len(spotify_playlist_tracks))
        count += (len(spotify_playlist_tracks))

        # adding songs from each playlist to the global list (excluding duplicates)
        for playlist_track in spotify_playlist_tracks:
            if playlist_track['track']['uri'] not in spotify_all_playlists_tracks_track_uris:
                spotify_all_playlists_tracks_track_uris.add(playlist_track['track']['uri'])
                spotify_all_playlists_tracks.append(playlist_track)
    print(len(spotify_all_playlists_tracks))
    print(count)
    return spotify_all_playlists_tracks



def get_spotify_playlist_songs_one_playlist(access_token, playlist_id):
    '''adding batches of retrieved 50 songs from spotify's particular playlist to make a whole list of playlist's songs'''

    spotify_playlist_tracks = []
    offset = 0

    while True:
        spotify_playlist_tracks_50items = spotify_req_get_playlist_items(access_token, offset, playlist_id)
        if len(spotify_playlist_tracks_50items) == 0:
            break
        spotify_playlist_tracks.extend(spotify_playlist_tracks_50items)
        offset += 50
    return spotify_playlist_tracks



def spotify_req_get_playlist_items(access_token, offset, playlist_id):
    '''retrieving 50 songs from spotify's particular playlist at a time'''
    get_playlist_items_base_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    params = {'limit': 50, 'offset': offset}
    get_playlist_items_url = get_playlist_items_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_playlist_items_dict = (requests.get(get_playlist_items_url, headers=headers)).json()
    spotify_playlist_items_50items = spotify_playlist_items_dict['items']
    return spotify_playlist_items_50items



def get_spotify_playlists_ids(access_token, current_user_id):
    '''adding batches of retrieved 50 playlists ids to make a whole list of playlists ids'''

    spotify_playlists = []
    offset = 0

    while True:
        spotify_playlists_50items = spotify_req_get_users_playlists(access_token, offset)
        if len(spotify_playlists_50items) == 0:
            break
        spotify_playlists.extend(spotify_playlists_50items)
        offset += 50

    spotify_playlists_ids = []
    for playlist in spotify_playlists:
        if playlist['owner']['id'] != current_user_id:
            continue
        spotify_playlists_ids.append(playlist["id"])

    return spotify_playlists_ids



def spotify_req_get_users_playlists(access_token, offset):
    '''retrieving info about 50 playlists from spotify at a time'''

    get_playlists_base_url = 'https://api.spotify.com/v1/me/playlists'
    params = {'limit': 50, 'offset': offset}
    get_playlists_url = get_playlists_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_playlists_dict = (requests.get(get_playlists_url, headers=headers)).json()
    spotify_playlists_50items = spotify_playlists_dict['items']
    return spotify_playlists_50items

















def extract_track_data(spotify_saved_tracks):
    '''extracting track data from spotify songs for VML library'''

    saved_tracks_library = []
    artists_uris = {}

    for track_info in spotify_saved_tracks:

        track_uri = track_info["track"]["uri"]
        track_artists, main_artist_uri = extract_track_artists_main_artist_uri(track_info)
        track_title = track_info["track"]["name"]
        album_artists = extract_album_artists(track_info)
        album_title = track_info["track"]["album"]["name"]
        album_uri = track_info["track"]["album"]["uri"]

        if track_artists[0] not in artists_uris:
            artists_uris[track_artists[0]] = main_artist_uri

        saved_track = {
            "track_uri": track_uri,
            "track_artists": track_artists,
            "main_artist_uri": main_artist_uri,
            "track_title": track_title,
            "album_artists": album_artists,
            "album_title": album_title,
            "album_uri": album_uri
            }

        saved_tracks_library.append(saved_track)

    return(saved_tracks_library, artists_uris)


def extract_album_artists(track_info):
    '''extracting album artists from spotify songs for VML library'''

    album_artists_dict = track_info["track"]["album"]["artists"]
    album_artists = []
    for album_artist_info in album_artists_dict:
        album_artists.append(album_artist_info["name"])   
    return album_artists



def extract_track_artists_main_artist_uri(track_info):
    '''extracting album artists from spotify songs for VML library'''

    track_artists_list = track_info["track"]["artists"]
    track_artists = []
    for track_artist_info in track_artists_list:
        track_artists.append(track_artist_info["name"])

    main_artist_uri = track_artists_list[0]["uri"]
    return track_artists, main_artist_uri