from flask import request

def create_library_request():

    if request.method == "POST":
        create_library_response = eval(request.form["create_library"])
        if not create_library_response:
            return False
        else:
            create_library()


def create_library():

    #POBIERA Z KLASY SpotifyLibrary
    #spotify_saved_tracks
    #spotify_all_playlists_tracks
    #spotify_playlists

    #PRZEKAZUJE JAKO ARGUMENTY DO METOD KLASY SpotifyLibraryExtract

    #otrzymane dane zapisuje w bazie danych
    #przekierowuje do strony z biblioteką i z flash messagem, że biblioteka została utworzona

    pass