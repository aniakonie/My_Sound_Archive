from website.database.database_connect import db_connect

def initialize_spotify_database():

    vml, cursor = db_connect()
    cursor = vml.cursor()

    cursor.execute('''
    CREATE TABLE artists_uris_genres (
    artist_uri VARCHAR(37) PRIMARY KEY,
    artist VARCHAR(50),
    artist_genres VARCHAR(300),
    artist_genre VARCHAR(20),
    artist_subgenre VARCHAR(20)
    )
    '''
    )

    cursor.execute('''
    CREATE TABLE tracks (
    track_uri VARCHAR(36) PRIMARY KEY,
    track_artist_main VARCHAR(100),
    main_artist_uri VARCHAR(37), FOREIGN KEY (main_artist_uri) REFERENCES artists_uris_genres(artist_uri),
    track_artist_add1 VARCHAR(100),
    track_artist_add2 VARCHAR(100),
    track_title VARCHAR(100),
    album_artist_main VARCHAR(100),
    album_artist_add1 VARCHAR(100),
    album_artist_add2 VARCHAR(100),
    album_title VARCHAR(100),
    album_uri VARCHAR(36)
    )
    '''
    )