import mysql.connector

def genres_folders_suggestions():

    vml = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "virtual_music_library"
    )

    cursor = vml.cursor()

    query_genres = (
    '''
    SELECT DISTINCT tracks.track_artist_main, tracks.main_artist_uri, artists_uris_genres.artist_genres
    FROM tracks
    JOIN artists_uris_genres
    ON tracks.main_artist_uri = artists_uris_genres.artist_uri
    ORDER BY tracks.track_artist_main ASC
    '''
    )

    cursor.execute(query_genres)


    #subgenres list (merged subgenres of all artists)
    subgenres_names_list = []
    for track_artist_main, main_artist_uri, artist_genres in cursor:
        subgenres_names = artist_genres.split(", ")
        subgenres_names_list.extend(subgenres_names)


    #genres list (merged genres of all artists)
    genres_names_list = []
    for name in subgenres_names_list:
        if name == "":
            continue
        genres_names = name.split(" ")
        genres_names_list.extend(genres_names)

    #subgenres popularity
    subgenres_names_popularity = dict()
    for name in subgenres_names_list:
        if name not in subgenres_names_popularity:
            subgenres_names_popularity[name] = 1
        else:
            subgenres_names_popularity[name] += 1

    print("SUBGENRES POPULARITY")
    for name, popularity in subgenres_names_popularity.items():
        if ((popularity >= 20) and (name != "")):
            print("Popularity: more than 20:", name, popularity)

    #genres popularity
    genres_names_popularity = dict()
    for name in genres_names_list:
        if name not in genres_names_popularity:
            genres_names_popularity[name] = 1
        else:
            genres_names_popularity[name] += 1


    #retrieving main_genres names from DB
    query_main_genres = (
    '''
    SELECT main_genre
    FROM main_genres
    '''
    )
    cursor.execute(query_main_genres)
    main_genres = []
    for item in cursor:
        main_genres.append(item[0])

    folders_suggestions = []
    for name, popularity in genres_names_popularity.items():
        if (popularity >= 20) and (name in main_genres):
            folders_suggestions.append(name)

    print(folders_suggestions)

    return folders_suggestions
