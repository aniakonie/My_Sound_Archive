from website.spotify.sp_get_library import get_spotify_saved_tracks, get_spotify_playlists_songs_all_playlists_together, get_spotify_playlists, get_current_user_profile_data
from website.database.database_connect import db_connect

def extract_user_profile_data(access_token):

    current_user_profile_data = get_current_user_profile_data(access_token)
    user_id = current_user_profile_data["id"]
    user_name = current_user_profile_data["display_name"]
    return user_id, user_name


def extract_playlists_info(access_token, current_user_id):
    '''extracting playlist info from spotify playlists for VML library - "playlist_info" table'''

    spotify_playlists = get_spotify_playlists(access_token)
    playlists_info_library = set()

    for playlist in spotify_playlists:

        playlist_id = playlist["id"]
        playlist_name = playlist["name"]
        is_owner = True if playlist["owner"]["id"] == current_user_id else False

        playlist_info = (current_user_id, playlist_id, playlist_name, is_owner)
        playlists_info_library.add(playlist_info)

    return playlists_info_library




# def func(access_token):

#     spotify_saved_tracks = get_spotify_saved_tracks(access_token)

#     tracks_uris = set()

#     for track_info in spotify_saved_tracks:

#         track_uri = track_info["track"]["uri"]
#         tracks_uris.add(track_uri)

#         track_artists, main_artist_uri = extract_track_artists_main_artist_uri(track_info)

#         is_artist_uri_in_artists_uris_genres_db(main_artist_uri)


#         if main_artist_uri not in artists_uris_genres_DATABASE:
#             DODAJ TO DO BAZY DANYCH;
#             DOBIERZ GENRE I GENRES DO ARTYSTY;

#         if track_uri not in tracks_DATABASE:
#             DODAJ TRACKURI DO BAZY DANYCH

#     return tracks_uris












def is_artist_uri_in_artists_uris_genres_db(main_artist_uri):

    vml, cursor = db_connect()
    cursor = vml.cursor()
    query = (
    '''
    SELECT artist_uri
    FROM artists_uris_genres
    '''
    )
    cursor.execute(query)   

    artists_uris_db = set()

    for artist_uri_in_artists_uris_genres in cursor:
        artists_uris_db.add(artist_uri_in_artists_uris_genres)

    if main_artist_uri in artists_uris_db:
        return True
    else:
        return False



def is_track_uri_in_tracks_db(track_uri):

    vml, cursor = db_connect()
    cursor = vml.cursor()
    query = (
    '''
    SELECT track_uri
    FROM tracks
    '''
    )
    cursor.execute(query)   

    tracks_uris_db = set()

    for track_uri_in_tracks in cursor:
        tracks_uris_db.add(track_uri_in_tracks)

    if track_uri in tracks_uris_db:
        return True
    else:
        return False







# spotify_saved_tracks = get_spotify_saved_tracks(access_token)
# spotify_all_playlists_tracks = get_spotify_playlists_songs_all_playlists_together(access_token)



# def extract_playlists_tracks_data_for_db(spotify_all_playlists_tracks):
#     '''extracting playlist tracks data from spotify songs for VML library'''

#     pass











# #works for tracks from playlists as well
# def extract_track_data_for_db(spotify_saved_tracks):
#     '''extracting track data from spotify songs for VML library'''

#     saved_tracks_library = []
#     artists_uris = {}

#     for track_info in spotify_saved_tracks:

#         track_uri = track_info["track"]["uri"]
#         track_artists, main_artist_uri = extract_track_artists_main_artist_uri(track_info)
#         track_title = track_info["track"]["name"]
#         album_artists = extract_album_artists(track_info)
#         album_title = track_info["track"]["album"]["name"]
#         album_uri = track_info["track"]["album"]["uri"]

#         if track_artists[0] not in artists_uris:
#             artists_uris[track_artists[0]] = main_artist_uri

#         saved_track = {
#             "track_uri": track_uri,
#             "track_artists": track_artists,
#             "main_artist_uri": main_artist_uri,
#             "track_title": track_title,
#             "album_artists": album_artists,
#             "album_title": album_title,
#             "album_uri": album_uri
#             }

#         saved_tracks_library.append(saved_track)

#     return(saved_tracks_library, artists_uris)


# def extract_album_artists(track_info):
#     '''extracting album artists from spotify songs for VML library'''

#     album_artists_dict = track_info["track"]["album"]["artists"]
#     album_artists = []
#     for album_artist_info in album_artists_dict:
#         album_artists.append(album_artist_info["name"])   
#     return album_artists



def extract_track_artists_main_artist_uri(track_info):
    '''extracting album artists from spotify songs for VML library'''

    track_artists_list = track_info["track"]["artists"]
    track_artists = []
    for track_artist_info in track_artists_list:
        track_artists.append(track_artist_info["name"])

    main_artist_uri = track_artists_list[0]["uri"]
    return track_artists, main_artist_uri
