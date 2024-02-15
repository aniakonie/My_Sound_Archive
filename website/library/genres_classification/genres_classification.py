import random
from website.database.models import ArtistsGenres
from website.spotify.spotify_genres import spotify_get_artists_genres
from website.database.models import *

def classify_artists_genres():
    #retrieving all artists without corresponding genres from database
    artists = ArtistsGenres.query.filter_by(artist_genres = None).all()
    artists_list = [artist for artist in artists]
    artists_uris_genres = spotify_get_artists_genres(artists_list)

    artists_uris_genres_main_genre = []
    for artist in artists_uris_genres:
        genres_string = ", ".join(artist[1])
        main_genre = assign_main_genre(genres_string)
        artists_uris_genres_main_genre.append((artist + (main_genre,)))
    save_artists_genres(artists_uris_genres_main_genre)


def save_artists_genres(artists_uris_genres_main_genre):

    for artist in artists_uris_genres_main_genre:
        artist_uri_genre = ArtistsGenres.query.filter_by(artist_uri = artist[0]).first()
        print(artist_uri_genre)
        artist_uri_genre.artist_genres = ', '.join(artist[1])
        print(artist_uri_genre.artist_genres)
        artist_uri_genre.artist_main_genre = artist[2]
        print(artist_uri_genre.artist_main_genre)
        db.session.add(artist_uri_genre)
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
    "dub"
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






#liquid funk is an electronic subgenre (=liquid drum and bass)!
#electronica
#metalcore, post-metal, post-rock
#co jeśli tyle samo razy występują jakieś gatunki (na razie algorytm wybiera randomly)