import mysql.connector


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

    vml = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "virtual_music_library"
    )

    cursor = vml.cursor()

    cursor.execute('''
    CREATE TABLE main_genres (
    main_genre VARCHAR(20) PRIMARY KEY,
    subgenres VARCHAR(300))
    '''
    )

    for item in main_genres:
        add_item = "INSERT INTO main_genres(main_genre) VALUES(%s)" 
        item_value = (item,)
        cursor.execute(add_item, item_value)
        vml.commit()


def genres_artists_classification():


    string = "contemporary vocal jazz, jazz, pop, vocal jazz"
    genres_string = string.lower()

    main_genres_dict = dict()

    for item in main_genres:
        main_genres_dict[item] = genres_string.count(item)
    print(main_genres_dict)

    genre_classification = [name for (name, num_of_occur) in main_genres_dict.items() if num_of_occur == max(main_genres_dict.values())]

    print(genre_classification)

    if len(genre_classification) == 1:
        artist_genre = genre_classification[0]







genres_artists_classification()


    




#electronica
#metalcore, post-metal, post-rock
#co jeśli tyle samo razy występują jakieś gatunki