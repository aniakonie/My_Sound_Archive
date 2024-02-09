
def parse(spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks, music_platform_id):

    playlists_info_library = parse_playlists_info(spotify_playlists, music_platform_id)

    saved_tracks_library, tracks_uris = parse_spotify_saved_tracks(spotify_saved_tracks)

    print(saved_tracks_library[2000])
    print(len(spotify_saved_tracks))
    print(len(tracks_uris))







def parse_playlists_info(spotify_playlists, music_platform_id):
    '''extracting playlist info from spotify playlists for VML library - "playlist_info" table'''
    playlists_info_library = set()

    for playlist in spotify_playlists:
        playlist_id = playlist["id"]
        playlist_name = playlist["name"]
        is_owner = True if playlist["owner"]["id"] == music_platform_id else False
        playlist_info = (playlist_id, playlist_name, is_owner)
        playlists_info_library.add(playlist_info)
    return playlists_info_library






















# def func(access_token):

#     spotify_saved_tracks = get_spotify_saved_tracks(access_token)

#     tracks_uris = set()

#     for track_info in spotify_saved_tracks:

#         track_uri = track_info["track"]["uri"]
#         tracks_uris.add(track_uri)

#         track_artists, main_artist_uri = extract_track_artists_main_artist_uri(track_info)

#         is_artist_uri_in_artists_uris_genres_db(main_artist_uri)


#         if main_artist_uri not in artists_uris_genres_DATABASE:
#             DODAJ TO DO BAZY DANYCH;
#             DOBIERZ GENRE I GENRES DO ARTYSTY;

#         if track_uri not in tracks_DATABASE:
#             DODAJ TRACKURI DO BAZY DANYCH

#     return tracks_uris










#works for tracks from playlists as well
    
def parse_spotify_saved_tracks(spotify_saved_tracks):

    saved_tracks_library = []
    tracks_uris = set()

    for track_info in spotify_saved_tracks:
        track_uri = track_info["track"]["uri"]
        track_artist_main, main_artist_uri, track_artist_add1, track_artist_add2 = parse_track_artists_main_artist_uri(track_info)
        track_title = track_info["track"]["name"]
        album_artist_main, album_artist_add1, album_artist_add2 = parse_album_artists(track_info)
        album_title = track_info["track"]["album"]["name"]
        album_uri = track_info["track"]["album"]["uri"]

        saved_track = {
            "track_uri": track_uri,
            "track_artist_main": track_artist_main,
            "main_artist_uri": main_artist_uri,
            "track_artist_add1": track_artist_add1,
            "track_artist_add2": track_artist_add2,
            "track_title": track_title,
            "album_artist_main": album_artist_main,
            "album_artist_add1": album_artist_add1,
            "album_artist_add2": album_artist_add2,
            "album_title": album_title,
            "album_uri": album_uri
            }

        saved_tracks_library.append(saved_track)
        tracks_uris.add(track_uri)

    return(saved_tracks_library, tracks_uris)


def parse_album_artists(track_info):
    '''extracting album artists from spotify songs for VML library'''

    album_artist_main = track_info["track"]["album"]["artists"][0]["name"]
    album_artist_add1 = None
    album_artist_add2 = None
    if len(track_info["track"]["album"]["artists"]) > 2:
        album_artist_add1 = track_info["track"]["album"]["artists"][1]["name"]
        album_artist_add2 = track_info["track"]["album"]["artists"][2]["name"]
    elif len(track_info["track"]["album"]["artists"]) > 1:
        album_artist_add1 = track_info["track"]["album"]["artists"][1]["name"]
    return album_artist_main, album_artist_add1, album_artist_add2


def parse_track_artists_main_artist_uri(track_info):
    '''extracting album artists from spotify songs for VML library'''

    track_artist_main = track_info["track"]["artists"][0]["name"]
    main_artist_uri = track_info["track"]["artists"][0]["uri"]
    track_artist_add1 = None
    track_artist_add2 = None
    if len(track_info["track"]["artists"]) > 2:
        track_artist_add1 = track_info["track"]["artists"][1]["name"]
        track_artist_add2 = track_info["track"]["artists"][2]["name"]
    elif len(track_info["track"]["artists"]) > 1:
        track_artist_add1 = track_info["track"]["artists"][1]["name"]

    return track_artist_main, main_artist_uri, track_artist_add1, track_artist_add2
