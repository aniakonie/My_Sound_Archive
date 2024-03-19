import random
from website.spotify.spotify_genres import spotify_get_artists_genres
from website.database.models import *
from flask_login import current_user

def classify_artists_genres():
    '''retrieving all artists without corresponding genres from database'''
    artists = Artists.query.filter_by(artist_genres = None).all()
    artists_list = [artist for artist in artists]
    artists_uris_genres = spotify_get_artists_genres(artists_list)

    artists_uris_genres_main_genre = []
    for artist in artists_uris_genres:
        genres_string = ", ".join(artist[1])
        main_genre = assign_main_genre(genres_string)
        artists_uris_genres_main_genre.append((artist + (main_genre,)))
    save_artists_genres(artists_uris_genres_main_genre)
    save_user_artists_genres()


def save_artists_genres(artists_uris_genres_main_genre):
    '''saving genres and subgenres to global table artists'''
    for artist in artists_uris_genres_main_genre:
        artist_uri_genre = Artists.query.filter_by(artist_uri = artist[0]).first()
        artist_uri_genre.artist_genres = ', '.join(artist[1])
        artist_uri_genre.artist_main_genre = artist[2]
        #TODO assign subgenres
        artist_uri_genre.artist_subgenre = 'others'
        db.session.add(artist_uri_genre)
        db.session.commit()


#TODO add subgenres classification


def save_user_artists_genres():
    '''saving genres and subgenres to table user_artists'''
    user_artists = UserArtists.query.filter_by(user_id = current_user.id).all()
    user_artists_uris = [artist.artist_uri for artist in user_artists]
    for user_artist_uri in user_artists_uris:
        artist = Artists.query.filter_by(artist_uri = user_artist_uri).first()
        artist_main_genre = artist.artist_main_genre
        artist_subgenre = artist.artist_subgenre
        user_artist = UserArtists.query.filter_by(artist_uri = user_artist_uri).filter_by(user_id = current_user.id).first()
        user_artist.artist_main_genre_custom = artist_main_genre
        user_artist.artist_subgenre_custom = artist_subgenre
        db.session.add(user_artist)
        db.session.commit()


main_genres ={
    "metal",
    "rock",
    "jazz", 
    "pop",
    "rap",
    "reggae",
    "electronic",
    "classical music",
    "country",
    "funk",
    "blues"
    }

electronic = {
    "dubstep",
    "techno",
    "house",
    "drum and bass",
    "liquid funk"
}

reggae = {
    "polish reggae",
    "dub",
    "roots reggae"
}

rock = {
    "punk"
}


rap = {
    "hip hop"
}


def assign_main_genre(genres_string):

    genres_string = genres_string.lower()
    main_genres_dict = dict()
    #counting how many times names of the main genres occur in the artist_genres retrieved from spotify (exclude 0 times)
    for item in main_genres:
        if genres_string.count(item) > 0:
            main_genres_dict[item] = genres_string.count(item)
            
    #list of the biggest occurences
    genre_classification = [name for (name, num_of_occur) in main_genres_dict.items() if num_of_occur == max(main_genres_dict.values())]

    if len(genre_classification) == 1:
        main_genre = genre_classification[0]
    elif len(genre_classification) > 1:
        main_genre = random.choice(genre_classification)
    elif len(genre_classification) == 0:
        main_genre = "others"
    return main_genre



#dnb
#liquid funk is an electronic subgenre (=liquid drum and bass)!
#electronica
#metalcore, post-metal, post-rock
