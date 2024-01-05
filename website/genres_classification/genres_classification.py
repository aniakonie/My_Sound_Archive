from website.database.database_connect import db_connect
import random

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
    "blues",
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






#liquid funk is an electronic subgenre (=liquid drum and bass)!




def initialize_genres_database():

    vml, cursor = db_connect()

    cursor = vml.cursor()

    cursor.execute('''
    CREATE TABLE main_genres (
    main_genre VARCHAR(20) PRIMARY KEY,
    subgenres VARCHAR(300)
    )
    '''
    )

    for item in main_genres:
        add_item = "INSERT INTO main_genres(main_genre) VALUES(%s)" 
        item_value = (item,)
        cursor.execute(add_item, item_value)
        vml.commit()


def genres_artists_classification(artist_genres_string):

    genres_string = artist_genres_string.lower()
    main_genres_dict = dict()
    #counting how many times names of the main genres occur in the artist_genres retrieved from spotify (exclude 0 times)
    for item in main_genres:
        if genres_string.count(item) > 0:
            main_genres_dict[item] = genres_string.count(item)
            
    #list of the biggest occurences
    genre_classification = [name for (name, num_of_occur) in main_genres_dict.items() if num_of_occur == max(main_genres_dict.values())]

    if len(genre_classification) == 1:
        artist_genre_chosen = genre_classification[0]
    elif len(genre_classification) > 1:
        artist_genre_chosen = random.choice(genre_classification)
    elif len(genre_classification) == 0:
        artist_genre_chosen = "others"

    return artist_genre_chosen


    




#electronica
#metalcore, post-metal, post-rock
#co jeśli tyle samo razy występują jakieś gatunki