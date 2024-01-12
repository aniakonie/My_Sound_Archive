from website.database.database_connect import db_connect

def create_users_tables():

    vml, cursor = db_connect()
    cursor = vml.cursor()

    create_users(cursor)
    create_users_playlists_info(cursor)
    create_users_tracks_uris(cursor)
    create_users_artists_folders(cursor)
    # create_users_settings(cursor)


def create_users(cursor):

    cursor.execute('''
    CREATE TABLE users (
    user_id VARCHAR(15) PRIMARY KEY,
    user_name VARCHAR(25),
    account_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_token VARCHAR(220),
    refresh_token VARCHAR(131)
    )
    '''
    )

def create_users_playlists_info(cursor):

    cursor.execute('''
    CREATE TABLE users_playlists_info (
    user_id VARCHAR(15), FOREIGN KEY (user_id) REFERENCES users(user_id),
    playlist_id VARCHAR(25),
    playlist_name VARCHAR(100),
    owner BOOL
    )
    '''
    )


def create_users_tracks_uris(cursor):

    cursor.execute('''
    CREATE TABLE users_tracks_uris (
    user_id VARCHAR(15), FOREIGN KEY (user_id) REFERENCES users(user_id),
    track_uri VARCHAR(36), FOREIGN KEY (track_uri) REFERENCES tracks(track_uri),
    playlist_id_or_saved_song VARCHAR(25),
    display_in_library BOOL
    )
    '''
    )


def create_users_artists_folders(cursor):

    cursor.execute('''
    CREATE TABLE users_artists_folders (
    user_id VARCHAR(15), FOREIGN KEY (user_id) REFERENCES users(user_id),
    artist_uri VARCHAR(37), FOREIGN KEY (artist_uri) REFERENCES artists_uris_genres(artist_uri),
    artist_main_genre_custom VARCHAR(20),
    artist_subgenre_custom VARCHAR(20)
    )
    '''
    )


def create_users_settings(cursor):
    pass


