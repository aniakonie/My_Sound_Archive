from website.database.database_connect import db_connect

def create_new_users_tables():

    vml, cursor = db_connect()
    cursor = vml.cursor()
    current_user_id = "blah"

    create_user_id_tracks_uris(current_user_id, cursor)
    create_user_id_playlists_info(current_user_id, cursor)
    create_user_id_artists_folders(current_user_id, cursor)
    create_user_id_settings(current_user_id, cursor)


def create_user_id_tracks_uris(current_user_id, cursor):

    cursor.execute(f'''
    CREATE TABLE {current_user_id}_tracks_uris (
    track_uri VARCHAR(36) PRIMARY KEY,
    playlist_id_or_saved_song VARCHAR(25),
    display_in_library BOOL
    )
    '''
    )


def create_user_id_playlists_info(current_user_id, cursor):

    cursor.execute(f'''
    CREATE TABLE {current_user_id}_playlists_info (
    playlist_id VARCHAR(25) PRIMARY KEY,
    playlist_name VARCHAR(100),
    owner BOOL
    )
    '''
    )


def create_user_id_artists_folders(current_user_id, cursor):

    cursor.execute(f'''
    CREATE TABLE {current_user_id}_artists_folders (
    artist_uri VARCHAR(37) PRIMARY KEY,
    artist_main_genre_custom VARCHAR(20),
    artist_subgenre_custom VARCHAR(20)
    )
    '''
    )


def create_user_id_settings(current_user_id, cursor):
    pass


