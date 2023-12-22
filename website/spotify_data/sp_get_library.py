import requests
import urllib.parse


def get_spotify_saved_tracks(access_token):

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

    get_tracks_base_url = 'https://api.spotify.com/v1/me/tracks'
    params = {'limit': 50, 'offset': offset}
    get_tracks_url = get_tracks_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_saved_tracks_dict = (requests.get(get_tracks_url, headers=headers)).json()
    spotify_saved_tracks_50items = spotify_saved_tracks_dict['items']
    return spotify_saved_tracks_50items


def extract_track_data(spotify_saved_tracks):

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

    album_artists_dict = track_info["track"]["album"]["artists"]
    album_artists = []
    for album_artist_info in album_artists_dict:
        album_artists.append(album_artist_info["name"])   
    return album_artists


def extract_track_artists_main_artist_uri(track_info):

    track_artists_list = track_info["track"]["artists"]
    track_artists = []
    for track_artist_info in track_artists_list:
        track_artists.append(track_artist_info["name"])

    main_artist_uri = track_artists_list[0]["uri"]
    return track_artists, main_artist_uri


def get_spotify_playlists_ids(access_token, current_user_id):

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

    get_playlists_base_url = 'https://api.spotify.com/v1/me/playlists'
    params = {'limit': 50, 'offset': offset}
    get_playlists_url = get_playlists_base_url + '?' + urllib.parse.urlencode(params)
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    spotify_playlists_dict = (requests.get(get_playlists_url, headers=headers)).json()
    spotify_playlists_50items = spotify_playlists_dict['items']
    return spotify_playlists_50items



# def spotify_req_get_playlist_items(access_token, offset, playlist_id):

#     get_playlist_items_base_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
#     params = {'limit': 50, 'offset': offset}
#     get_playlist_items_url = get_playlist_items_base_url + '?' + urllib.parse.urlencode(params)
#     headers = {
#         'Authorization': 'Bearer ' + access_token
#     }
#     spotify_playlist_items_dict = (requests.get(get_playlist_items_url, headers=headers)).json()
#     spotify_playlist_items_50items = spotify_playlist_items_dict['items']
#     return spotify_playlist_items_50items






# #list of tracks from all playlists combined; some songs may have repeats
# all_playlists_tracks = []

# for playlist_id in playlists_ids:
#     offset = 0
#     while True:
#         all_playlists_tracks.extend(sp.playlist_tracks(playlist_id, limit=50, offset=offset, market=None, fields="items(id)", additional_types=('track', )))
#         if len(sp.playlist_tracks(playlist_id, limit=50, offset=offset, market=None, fields="items(id)", additional_types=('track', ))) == 0:
#             break
#         offset += 50

# spotify_track_ids_fromplaylists = []
# for i in all_playlists_tracks:
#     spotify_track_ids_fromplaylists.append(i["id"])

# print(playlists_ids)
# print(len(all_playlists_tracks))