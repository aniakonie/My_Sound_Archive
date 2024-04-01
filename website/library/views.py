from flask import Blueprint, url_for, redirect, render_template, request, abort, session
from flask_login import login_required, current_user
from website.database.models import *
from sqlalchemy import func, select, and_, or_, distinct
from werkzeug.routing import BaseConverter
import urllib.parse


library_bp = Blueprint('library_bp', __name__, template_folder='templates')


class PathConverter(BaseConverter):
    regex = '.*?'


@library_bp.route('/', methods=["POST", "GET"])
@login_required
def library():
    if not current_user.is_library_created:
        genres = None
        if request.method == "POST":
            return redirect(url_for("spotify_bp.authorization"))
    else:
        genres = get_genres(current_user.id)
        if request.method == "POST":
            selected_genre = request.form["selected_genre"]
            return redirect(url_for("library_bp.library_genres", selected_genre = selected_genre))
    return render_template("library/library.html", genres = genres, current = "library", user = current_user.username)


@library_bp.route('/<path:selected_genre>', methods=["POST", "GET"])
@login_required
def library_genres(selected_genre):

    if not current_user.is_library_created:
        return redirect(url_for("library_bp.library"))

    genres = get_genres(current_user.id)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, current_user.id)

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")
        selected_subgenre = request.form.get("selected_subgenre")
        if new_selected_genre:
            return redirect(url_for("library_bp.library_genres", selected_genre = new_selected_genre))
        elif selected_subgenre:
            return redirect(url_for("library_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = selected_subgenre))
    return render_template("library/library.html", genres = genres, subgenres = subgenres, current = "library", selected_genre = selected_genre)


@library_bp.route('/<path:selected_genre>/<path:selected_subgenre>', methods=["POST", "GET"])
@login_required
def library_subgenres(selected_genre, selected_subgenre):

    if not current_user.is_library_created:
        return redirect(url_for("library_bp.library"))

    genres = get_genres(current_user.id)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, current_user.id)
    if selected_subgenre not in subgenres:
        abort(404)

    artists = get_artists_of_selected_subgenre(selected_genre, selected_subgenre, current_user.id)

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")       
        new_selected_subgenre = request.form.get("selected_subgenre")
        selected_artist_uri = request.form.get("selected_artist_uri")

        if new_selected_genre:
            return redirect(url_for("library_bp.library_genres", selected_genre = new_selected_genre))
        elif new_selected_subgenre:
            return redirect(url_for("library_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre))
        elif selected_artist_uri:
            session["selected_artist_uri"] = selected_artist_uri
            selected_artist_name = request.form.get("selected_artist_name")
            session["selected_artist_name"] = selected_artist_name
            selected_artist_name = encode_characters(selected_artist_name)
            return redirect(url_for("library_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_name = selected_artist_name))   

    return render_template("library/library.html", genres = genres, subgenres = subgenres, artists = artists, current = "library", selected_genre = selected_genre, selected_subgenre = selected_subgenre)


@library_bp.route('/<path:selected_genre>/<path:selected_subgenre>/<path:selected_artist_name>', methods=["POST", "GET"])
@login_required
def library_tracks(selected_genre, selected_subgenre, selected_artist_name):

    if not current_user.is_library_created:
        return redirect(url_for("library_bp.library"))
    
    genres = get_genres(current_user.id)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, current_user.id)
    if selected_subgenre not in subgenres:
        abort(404)

    selected_artist_name = session["selected_artist_name"]

    artists = get_artists_of_selected_subgenre(selected_genre, selected_subgenre, current_user.id)
    selected_artist_uri = session["selected_artist_uri"]
    if (selected_artist_uri, selected_artist_name) not in artists:
        abort(404)

    if (selected_artist_uri, selected_artist_name) != ("Loose tracks", "Loose tracks"):
        tracklist = get_tracks_of_artist(selected_artist_uri, current_user.id)
        tracklist_featured = get_featured_tracks_of_artist(selected_artist_name, current_user.id)
    else:
        tracklist = get_loose_tracks_for_subgenre(selected_genre, selected_subgenre, current_user.id)
        tracklist_featured = []

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")
        new_selected_subgenre = request.form.get("selected_subgenre")
        new_selected_artist_uri = request.form.get("selected_artist_uri")

        session.pop("selected_artist_uri", default=None)
        session.pop("selected_artist_name", default=None)

        if new_selected_genre:
            return redirect(url_for("library_bp.library_genres", selected_genre = new_selected_genre))
        elif new_selected_subgenre:
            return redirect(url_for("library_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre))
        elif new_selected_artist_uri:
            session["selected_artist_uri"] = new_selected_artist_uri
            selected_artist_name = request.form.get("selected_artist_name")
            session["selected_artist_name"] = selected_artist_name
            new_selected_artist_name = encode_characters(selected_artist_name)
            return redirect(url_for("library_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_name = new_selected_artist_name))        

    return render_template("library/library.html", genres = genres, subgenres = subgenres, artists = artists, tracklist = tracklist,
                           tracklist_featured = tracklist_featured, current ="library", selected_genre=selected_genre,
                           selected_subgenre=selected_subgenre, selected_artist_uri=selected_artist_uri, selected_artist_name=selected_artist_name)


def encode_characters(param):
    param = param.replace(' ', "-")
    param = param.replace('&', "and")
    return param


def get_genres(user_id):
    subquery = (
        select([Tracks.main_artist_uri])
        .join(UserTracks, UserTracks.track_uri == Tracks.track_uri)
        .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
    )
    query = (
        select([UserArtists.artist_main_genre_custom]).distinct()
        .filter(UserArtists.user_id == user_id) 
        .filter(UserArtists.artist_uri.in_(subquery))
        .order_by('artist_main_genre_custom')
    )
    result = db.session.execute(query)
    genres = [genre.artist_main_genre_custom for genre in result]
    genres.remove("others")
    genres.append("others")
    return genres


def get_subgenres(selected_genre, user_id):
    '''Select all subgenres for selected genre'''

    subquery = (
        select([Tracks.main_artist_uri])
        .join(UserTracks, UserTracks.track_uri == Tracks.track_uri)
        .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
    )
    query = (
        select([UserArtists.artist_subgenre_custom]).distinct()
        .filter(UserArtists.user_id == user_id) 
        .filter(UserArtists.artist_main_genre_custom == selected_genre)        
        .filter(UserArtists.artist_uri.in_(subquery))
        .order_by('artist_subgenre_custom')
    )
    query_result = db.session.execute(query)
    subgenres = [subgenre.artist_subgenre_custom for subgenre in query_result]
    subgenres.remove("others")
    subgenres.append("others")
    return subgenres


def get_artists_of_selected_subgenre(selected_genre, selected_subgenre, user_id):
    '''Select all artists which play particular subgenre and user owns in his library at least 3 songs of this artist'''

    user_settings = UserSettings.query.filter_by(user_id=user_id).first()
    no_of_songs = user_settings.no_of_songs_into_folder
    subquery = (
        select([Tracks.main_artist_uri])
        .join(UserTracks, UserTracks.track_uri == Tracks.track_uri)
        .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
        .group_by(Tracks.main_artist_uri)
        .having(func.count(distinct(Tracks.track_uri)) >= no_of_songs)
    )
    query = (
        select([UserArtists.artist_uri, UserArtists.artist_name]).distinct()
        .filter(UserArtists.user_id == user_id) 
        .filter(UserArtists.artist_main_genre_custom == selected_genre)
        .filter(UserArtists.artist_subgenre_custom == selected_subgenre)               
        .filter(UserArtists.artist_uri.in_(subquery))
        .order_by('artist_name')
    )
    query_result = db.session.execute(query)
    artists = [(artist.artist_uri, artist.artist_name) for artist in query_result]
    artists.append(("Loose tracks", "Loose tracks"))
    return artists


def get_tracks_of_artist(selected_artist_uri, user_id):
    '''Select all tracks of an artist'''
    subquery = (
        select([UserTracks.track_uri]).distinct()
        .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
    )
    query = (
        select([func.min(Tracks.track_uri).label('track_uri'), func.min(Tracks.album_uri).label('album_uri'), Tracks.track_title])
        .filter(and_(Tracks.main_artist_uri == selected_artist_uri, Tracks.track_uri.in_(subquery)))
        .group_by(Tracks.track_title)
        .order_by(Tracks.track_title.asc())
    )
    query_result = db.session.execute(query)
    tracklist = []
    for track in query_result:
        track_dict = {
            "track_title": track.track_title,
            "track_uri": track.track_uri,
            "album_uri": track.album_uri
        }
        tracklist.append(track_dict)
    return tracklist


def get_featured_tracks_of_artist(selected_artist_name, user_id):
    '''Select all featured tracks of an artist'''

    subquery = (
        select([UserTracks.track_uri]).distinct()
        .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
    )
    query = (
        select([Tracks.track_uri, Tracks.track_artist_main, Tracks.track_artist_add1, Tracks.track_artist_add2, Tracks.track_title, Tracks.album_uri])
        .filter(or_(Tracks.track_artist_add1 == selected_artist_name, Tracks.track_artist_add2 == selected_artist_name))
        .filter(Tracks.track_uri.in_(subquery))
        .order_by(Tracks.track_title.asc())
    )
    query_result = db.session.execute(query)
    tracklist_featured = []
    for track in query_result:
        track_dict = {
            "track_title": track.track_title,
            "track_uri": track.track_uri,
            "album_uri": track.album_uri,
            "track_artist_main": track.track_artist_main,
            "track_artist_add1": track.track_artist_add1,
            "track_artist_add2": track.track_artist_add2
        }
        tracklist_featured.append(track_dict)
    return tracklist_featured


def get_loose_tracks_for_subgenre(selected_genre, selected_subgenre, user_id):

    user_settings = UserSettings.query.filter_by(user_id=user_id).first()
    no_of_songs = user_settings.no_of_songs_into_folder

    artist_subquery = (
    select([UserArtists.artist_uri])
    .filter(UserArtists.user_id == user_id)
    .filter(UserArtists.artist_main_genre_custom == selected_genre)
    .filter(UserArtists.artist_subgenre_custom == selected_subgenre)
    )

    track_artist_main_subquery = (
        select([Tracks.main_artist_uri])
        .join(UserTracks, UserTracks.track_uri == Tracks.track_uri)
        .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
        .group_by(Tracks.main_artist_uri)
        .having(func.count(distinct(Tracks.track_uri)) < no_of_songs)
    )

    query = (
        select([Tracks.track_artist_main, Tracks.track_uri, Tracks.track_artist_add1, Tracks.track_artist_add2,
        Tracks.track_title, Tracks.album_uri, Tracks.main_artist_uri]).distinct()
        .join(UserTracks, UserTracks.track_uri == Tracks.track_uri)
        .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
        .filter(Tracks.main_artist_uri.in_(artist_subquery))
        .filter(Tracks.main_artist_uri.in_(track_artist_main_subquery))
        .order_by(Tracks.track_artist_main.asc())
    )

    query_result = db.session.execute(query)
    tracklist = []
    for track in query_result:
        track_dict = {
            "track_title": track.track_title,
            "track_uri": track.track_uri,
            "album_uri": track.album_uri,
            "track_artist_main": track.track_artist_main,
            "track_artist_add1": track.track_artist_add1,
            "track_artist_add2": track.track_artist_add2
        }
        tracklist.append(track_dict)
    return tracklist






