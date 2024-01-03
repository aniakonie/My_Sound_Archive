
def playlists_info_library_into_db():
    pass

def playlists_tracks_data_into_db():
    pass

def saved_tracks_library_into_db():
    pass




def extract_playlists_tracks_data_for_db(spotify_all_playlists_tracks):
    '''extracting playlist tracks data from spotify songs for VML library'''

    pass



def extract_playlists_info(spotify_playlists, current_user_id):
    '''extracting playlist info from spotify playlists for VML library - "playlist_info" table'''

    playlists_info_library = []
    for playlist in spotify_playlists:

        playlist_id = playlist["id"]
        playlist_name = playlist["name"]
        is_owner = True if playlist["owner"]["id"] == current_user_id else False

        playlist_info = {
            "playlist_id": playlist_id,
            "playlist_name": playlist_name,
            "is_owner": is_owner
            }
        playlists_info_library.append(playlist_info)

    return playlists_info_library



def extract_track_data_for_db(spotify_saved_tracks):
    '''extracting track data from spotify songs for VML library'''

    saved_tracks_library = []
    artists_uris = {}

    for track_info in spotify_saved_tracks:

        track_uri = track_info["track"]["uri"]
        track_artists, main_artist_uri = extract_track_artists_main_artist_uri(track_info)
        track_title = track_info["track"]["name"]
        album_artists = extract_album_artists(track_info)
        album_title = track_info["track"]["album"]["name"]
        album_uri = track_info["track"]["album"]["uri"]

        if track_artists[0] not in artists_uris:
            artists_uris[track_artists[0]] = main_artist_uri

        saved_track = {
            "track_uri": track_uri,
            "track_artists": track_artists,
            "main_artist_uri": main_artist_uri,
            "track_title": track_title,
            "album_artists": album_artists,
            "album_title": album_title,
            "album_uri": album_uri
            }

        saved_tracks_library.append(saved_track)

    return(saved_tracks_library, artists_uris)


def extract_album_artists(track_info):
    '''extracting album artists from spotify songs for VML library'''

    album_artists_dict = track_info["track"]["album"]["artists"]
    album_artists = []
    for album_artist_info in album_artists_dict:
        album_artists.append(album_artist_info["name"])   
    return album_artists



def extract_track_artists_main_artist_uri(track_info):
    '''extracting album artists from spotify songs for VML library'''

    track_artists_list = track_info["track"]["artists"]
    track_artists = []
    for track_artist_info in track_artists_list:
        track_artists.append(track_artist_info["name"])

    main_artist_uri = track_artists_list[0]["uri"]
    return track_artists, main_artist_uri
