
def parse(spotify_playlists, spotify_saved_tracks, spotify_all_playlists_tracks, music_platform_id):

    saved_tracks_library = parse_spotify_saved_tracks(spotify_saved_tracks)
    all_playlists_tracks_library, playlists_to_discard = parse_spotify_all_playlists_tracks(spotify_all_playlists_tracks)
    playlists_info_library = parse_playlists_info(spotify_playlists, playlists_to_discard, music_platform_id)

    return playlists_info_library, saved_tracks_library, all_playlists_tracks_library


def parse_playlists_info(spotify_playlists, playlists_to_discard, music_platform_id):
    '''extracting playlist info from spotify playlists for library - "playlist_info" table'''
    playlists_info_library = set()
    for playlist in spotify_playlists:
            playlist_id = playlist["id"]
            playlist_name = playlist["name"]
            if playlist_name == '':
                playlist_name = '[no name]'
            is_owner = True if playlist["owner"]["id"] == music_platform_id else False
            playlist_info = (playlist_id, playlist_name, is_owner)
            if playlist_id not in playlists_to_discard:
                playlists_info_library.add(playlist_info)
    return playlists_info_library


def parse_spotify_all_playlists_tracks(spotify_all_playlists_tracks):

    all_playlists_tracks_library = {}
    playlists_to_discard = set()

    playlists_ids = list(spotify_all_playlists_tracks.keys())
    for playlist in playlists_ids:
        all_playlists_tracks_library[playlist] = []
        playlist_tracks = spotify_all_playlists_tracks[playlist]
        for track_info in playlist_tracks:
            if track_info["track"] == None:
                continue
            elif track_info["track"]["is_local"] == True:
                continue
            elif 'episode' in track_info["track"]["uri"]:
                continue
            else:
                track = parse_track_info(track_info)
                all_playlists_tracks_library[playlist].append(track)
        #discard playlist if no tracks were added
        if all_playlists_tracks_library[playlist] == []:
            all_playlists_tracks_library.pop(playlist)
            playlists_to_discard.add(playlist)
    print(all_playlists_tracks_library)
    return all_playlists_tracks_library, playlists_to_discard


def parse_spotify_saved_tracks(spotify_saved_tracks):

    saved_tracks_library = []

    for track_info in spotify_saved_tracks:
        if track_info["track"] == None:
            continue
        elif track_info["track"]["is_local"] == True:
            continue
        else:
            track = parse_track_info(track_info)
            saved_tracks_library.append(track)
    return saved_tracks_library


def parse_track_info(track_info):

    track_uri = track_info["track"]["uri"]
    track_artist_main, main_artist_uri, track_artist_add1, track_artist_add2 = parse_track_artists_main_artist_uri(track_info)
    track_title = track_info["track"]["name"]
    album_artist_main, album_artist_add1, album_artist_add2 = parse_album_artists(track_info)
    album_title = track_info["track"]["album"]["name"]
    album_uri = track_info["track"]["album"]["uri"]

    #TODO consider using named tuples instead of dictionaries (order of the songs is not required)
    track = {
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
    return track


def parse_album_artists(track_info):
    '''extracting album artists from spotify songs for library'''

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
    '''extracting album artists from spotify songs for library'''

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