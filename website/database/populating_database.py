from website.database.database_connect import db_connect
from  website.spotify_data.extracting_tracks_for_database import extract_playlists_info, extract_user_profile_data
# from website.genres_classification import genres_artists_classification


def populate_users(access_token, refresh_token):

    user_id, user_name = extract_user_profile_data(access_token)

    vml, cursor = db_connect()
    cursor = vml.cursor()

    sql_statement = "INSERT INTO users VALUES(%s, %s, CURRENT_TIMESTAMP, %s, %s)"
    row = (user_id, user_name, access_token, refresh_token)
    cursor.execute(sql_statement, row)

    vml.commit()


def populate_users_playlists_info(access_token, current_user_id):

    vml, cursor = db_connect()
    cursor = vml.cursor()

    playlists_info_library = extract_playlists_info(access_token, current_user_id)

    for (current_user_id, playlist_id, playlist_name, is_owner) in playlists_info_library:

        sql_statement = "INSERT INTO users_playlists_info VALUES(%s, %s, %s, %s)"
        row = (current_user_id, playlist_id, playlist_name, is_owner)
        cursor.execute(sql_statement, row)

        vml.commit()






















# def create_spotify_database(saved_tracks_library, artists_uris_genres):

#     vml, cursor = db_connect()
#     cursor = vml.cursor()

#     for (artist_uri, artist, artist_genres) in artists_uris_genres:

#         artist_genres_string = ", ".join(artist_genres)
#         artist_genre_chosen = genres_artists_classification(artist_genres_string)
#         artist_subgenre_chosen = " "

#         add_artist = "INSERT INTO artists_uris_genres VALUES(%s, %s, %s, %s, %s)"
#         data_artist = (artist_uri, artist, artist_genres_string, artist_genre_chosen, artist_subgenre_chosen)
#         cursor.execute(add_artist, data_artist)

#         vml.commit()


#     for item in saved_tracks_library:

#         #extracting first three artists from artists list (it may contain more than 3 artists)
#         track_artists = item["track_artists"]
#         track_artist_main = track_artists[0]
#         main_artist_uri = item["main_artist_uri"]
#         try:
#             track_artist_add1 = track_artists[1]
#         except:
#             track_artist_add1 = None
#         try:
#             track_artist_add2 = track_artists[2]
#         except:
#             track_artist_add2 = None

#         album_artists = item["album_artists"]
#         album_artist_main = album_artists[0]
#         try:
#             album_artist_add1 = album_artists[1]
#         except:
#             album_artist_add1 = None
#         try:
#             album_artist_add2 = album_artists[2]
#         except:
#             album_artist_add2 = None   

#         track_uri = item["track_uri"]
#         track_title = item["track_title"]
#         album_title = item["album_title"]
#         album_uri = item["album_uri"]
        
#         add_track = "INSERT INTO tracks VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"       

#         data_track = (track_uri, track_artist_main, main_artist_uri, track_artist_add1, track_artist_add2, track_title, album_artist_main, album_artist_add1, album_artist_add2, album_title, album_uri)
#         cursor.execute(add_track, data_track)

#         vml.commit()


