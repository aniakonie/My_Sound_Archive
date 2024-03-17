from website.database.models import *
from flask_login import current_user
from sqlalchemy.dialects.postgresql import insert


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

    for track in saved_tracks_library:
        data = UserTracks(track["track_uri"], 'saved song', True, current_user.id)
        db.session.add(data)
        db.session.commit()   

        add_track_to_tracks(track)
        add_artist_to_artists(track)
        add_artist_to_user_artists(track)

def save_all_playlists_tracks(all_playlists_tracks_library):

    playlists_ids = list(all_playlists_tracks_library.keys())
    for playlist in playlists_ids:

        query = UserPlaylists.query.filter_by(playlist_id = playlist).first()
        display_in_library = query.is_owner
        
        playlist_tracks = all_playlists_tracks_library[playlist]
        for track in playlist_tracks:
            data = UserTracks(track["track_uri"], playlist, display_in_library, current_user.id)
            db.session.add(data)
            db.session.commit()   
            add_track_to_tracks(track)
            add_artist_to_artists(track)
            add_artist_to_user_artists(track)

def add_track_to_tracks(track):

    values = {
                "track_uri": track["track_uri"],
                "track_artist_main": track["track_artist_main"][:100],
                "main_artist_uri": track["main_artist_uri"],
                "track_artist_add1": track["track_artist_add1"][:100] if track["track_artist_add1"] is not None else None,
                "track_artist_add2": track["track_artist_add2"][:100] if track["track_artist_add2"] is not None else None,
                "track_title": track["track_title"][:100],
                "album_artist_main": track["album_artist_main"][:100],
                "album_artist_add1": track["album_artist_add1"][:100] if track["album_artist_add1"] is not None else None,
                "album_artist_add2": track["album_artist_add2"][:100] if track["album_artist_add2"] is not None else None,
                "album_title": track["album_title"][:100],
                "album_uri": track["album_uri"]
                }
    
    statement = insert(Tracks).values(values).on_conflict_do_nothing(index_elements = ["track_uri"])
    db.session.execute(statement)
    db.session.commit()


def add_artist_to_artists(track):

    statement = insert(Artists).values(
        {'artist_uri':track["main_artist_uri"],
         'artist_name':track["track_artist_main"][0:50],
         'artist_genres':None, 'artist_main_genre':None}
         ).on_conflict_do_nothing()
    db.session.execute(statement)
    db.session.commit()


def add_artist_to_user_artists(track):

    statement = insert(UserArtists).values(
        {'artist_uri':track["main_artist_uri"],
         'artist_name':track["track_artist_main"][0:50],
         'artist_main_genre_custom':None,
         'artist_subgenre_custom':None,
         'user_id': current_user.id}
         ).on_conflict_do_nothing()
    db.session.execute(statement)
    db.session.commit()