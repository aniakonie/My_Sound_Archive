from website.database.models import *
from flask_login import current_user


def save_to_dabatase(playlists_info_library, saved_tracks_library, all_playlists_tracks_library):

    save_playlists_info(playlists_info_library)
    save_saved_tracks(saved_tracks_library)
    save_all_playlists_tracks(all_playlists_tracks_library)


def save_playlists_info(playlists_info_library):

    for playlist_id, playlist_name, is_owner in playlists_info_library:
        data = UserPlaylists(playlist_id, playlist_name, is_owner, current_user.id)
        db.session.add(data)
        db.session.commit()


def save_saved_tracks(saved_tracks_library):

    tracks_uris_db = get_tracks_uris_db()
    artists_uris_db = get_artists_uris_db()

    for track in saved_tracks_library:
        data = UserTracks(track["track_uri"], 'saved song', True, current_user.id)
        db.session.add(data)
        db.session.commit()   

        #if user's track is not in global table of tracks then it is added
        if track["track_uri"] not in tracks_uris_db:
            add_track_to_tracks(track)

        #if user's track's artist is not in global table of artists then it is added
        if track["main_artist_uri"] not in artists_uris_db:
            add_artist_to_artists(track)


def save_all_playlists_tracks(all_playlists_tracks_library):

    tracks_uris_db = get_tracks_uris_db()
    artists_uris_db = get_artists_uris_db()

    playlists_ids = list(all_playlists_tracks_library.keys())
    for playlist in playlists_ids:

        query = UserPlaylists.query.filter_by(playlist_id = playlist).first()
        display_in_library = query.is_owner
        
        playlist_tracks = all_playlists_tracks_library[playlist]
        for track in playlist_tracks:
            data = UserTracks(track["track_uri"], playlist, display_in_library, current_user.id)
            db.session.add(data)
            db.session.commit()   

            if track["track_uri"] not in tracks_uris_db:
                add_track_to_tracks(track)


def add_track_to_tracks(track):

    data = Tracks(
                track["track_uri"],
                track["track_artist_main"],
                track["main_artist_uri"],
                track["track_artist_add1"],
                track["track_artist_add2"],
                track["track_title"],
                track["album_artist_main"],
                track["album_artist_add1"],
                track["album_artist_add2"],
                track["album_title"],
                track["album_uri"])
    db.session.add(data)
    db.session.commit()


def add_artist_to_artists(track):
    #TODO change genres and main genre to null on default
    data = ArtistsGenres(track["main_artist_uri"], track["track_artist_main"], "genre", "main_genres")
    db.session.add(data)
    db.session.commit()


def get_artists_uris_db():
    artists = ArtistsGenres.query.all()
    artists_uris_db = set([artists.artist_uri for artist in artists])
    return artists_uris_db


def get_tracks_uris_db():
    tracks = Tracks.query.all()
    tracks_uris_db = set([tracks.track_uri for track in tracks])
    return tracks_uris_db



