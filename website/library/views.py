from flask import Blueprint, url_for, redirect, render_template, request, abort, session
from flask_login import login_required, current_user
from website.database.models import *
from sqlalchemy import func, select, and_, distinct


library_bp = Blueprint('library_bp', __name__, template_folder='templates')


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


@library_bp.route('/<selected_genre>', methods=["POST", "GET"])
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
        if new_selected_genre != None:
            return redirect(url_for("library_bp.library_genres", selected_genre = new_selected_genre))
        elif selected_subgenre != None:
            return redirect(url_for("library_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = selected_subgenre))
    return render_template("library/library.html", genres = genres, subgenres = subgenres, current = "library", selected_genre = selected_genre)


@library_bp.route('/<selected_genre>/<selected_subgenre>', methods=["POST", "GET"])
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

        if new_selected_genre != None:
            return redirect(url_for("library_bp.library_genres", selected_genre = new_selected_genre))
        elif new_selected_subgenre != None:
            return redirect(url_for("library_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre))
        elif selected_artist_uri != None:
            selected_artist_name = request.form.get("selected_artist_name")
            session["selected_artist_uri"] = selected_artist_uri
            return redirect(url_for("library_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_name = selected_artist_name))   

    return render_template("library/library.html", genres = genres, subgenres = subgenres, artists = artists, current = "library", selected_genre = selected_genre, selected_subgenre = selected_subgenre)


@library_bp.route('/<selected_genre>/<selected_subgenre>/<selected_artist_name>', methods=["POST", "GET"])
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

    artists = get_artists_of_selected_subgenre(selected_genre, selected_subgenre, current_user.id)
    selected_artist_uri = session["selected_artist_uri"]
    if (selected_artist_uri, selected_artist_name) not in artists:
        abort(404)

    if (selected_artist_uri, selected_artist_name) != ("Loose tracks", "Loose tracks"):
        tracklist = get_tracks_of_artist(selected_artist_uri, current_user.id)
        tracklist_featured = get_featured_tracks_of_artist(selected_artist_name, current_user.id)

    else:

        pass


    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")
        new_selected_subgenre = request.form.get("selected_subgenre")
        new_selected_artist_uri = request.form.get("selected_artist_uri")

        if new_selected_genre != None:
            return redirect(url_for("library_bp.library_genres", selected_genre = new_selected_genre))
        elif new_selected_subgenre != None:
            return redirect(url_for("library_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre))
        elif new_selected_artist_uri != None:
            new_selected_artist_name = request.form.get("selected_artist_name")
            session.pop("selected_artist_uri", default=None)
            session["selected_artist_uri"] = new_selected_artist_uri
            return redirect(url_for("library_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_name = new_selected_artist_name))        

    return render_template("library/library.html", genres = genres, subgenres = subgenres, artists = artists, tracklist = tracklist, tracklist_featured = tracklist_featured,
                           current = "library", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_uri = selected_artist_uri)



def get_genres(user_id):

    subquery = (
        select([Tracks.main_artist_uri])
        .join(UserTracks, UserTracks.track_uri == Tracks.track_uri)
        .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
    )

    query = (
        select([func.coalesce(UserArtistsGenres.artist_main_genre_custom, ArtistsGenres.artist_main_genre).label('artist_main_genre')])
        .distinct()
        .select_from(ArtistsGenres)
        .outerjoin(UserArtistsGenres, and_(ArtistsGenres.artist_uri == UserArtistsGenres.artist_uri, UserArtistsGenres.user_id == user_id))
        .filter(ArtistsGenres.artist_uri.in_(subquery))
        .order_by('artist_main_genre')
    )

    result = db.session.execute(query)
    genres = [genre.artist_main_genre for genre in result]
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
        select([
            func.coalesce(UserArtistsGenres.artist_subgenre_custom, ArtistsGenres.artist_subgenre).label('artist_subgenre'),
            func.coalesce(UserArtistsGenres.artist_main_genre_custom, ArtistsGenres.artist_main_genre).label('artist_main_genre')
        ])
        .distinct()
        .select_from(ArtistsGenres)
        .outerjoin(UserArtistsGenres, and_(ArtistsGenres.artist_uri == UserArtistsGenres.artist_uri, UserArtistsGenres.user_id == user_id))
        .filter(and_(func.coalesce(UserArtistsGenres.artist_main_genre_custom, ArtistsGenres.artist_main_genre) == selected_genre,
                     ArtistsGenres.artist_uri.in_(subquery)))
        .order_by('artist_subgenre')
    )

    query_result = db.session.execute(query)
    subgenres = [subgenre.artist_subgenre for subgenre in query_result]
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
        .having(func.count(distinct(Tracks.track_uri)) > no_of_songs)
    )

    query = (
        select([
            ArtistsGenres.artist_uri,
            ArtistsGenres.artist_name,
            func.coalesce(UserArtistsGenres.artist_subgenre_custom, ArtistsGenres.artist_subgenre).label('artist_subgenre'),
            func.coalesce(UserArtistsGenres.artist_main_genre_custom, ArtistsGenres.artist_main_genre).label('artist_main_genre')
        ])
        .distinct()
        .select_from(ArtistsGenres)
        .outerjoin(UserArtistsGenres, and_(ArtistsGenres.artist_uri == UserArtistsGenres.artist_uri, UserArtistsGenres.user_id == user_id))
        .filter(and_(
            func.coalesce(UserArtistsGenres.artist_main_genre_custom, ArtistsGenres.artist_main_genre) == selected_genre,
            func.coalesce(UserArtistsGenres.artist_subgenre_custom, ArtistsGenres.artist_subgenre) == selected_subgenre,
            ArtistsGenres.artist_uri.in_(subquery)
        ))
        .order_by('artist_name')
    )

    query_result = db.session.execute(query)
    artists = [(artist.artist_uri, artist.artist_name) for artist in query_result]
    artists.append(("Loose tracks", "Loose tracks"))
    return artists




def get_tracks_of_artist(selected_artist_uri, user_id):
    '''Select all tracks of an artist'''

    query_sql = (f'''
    SELECT MIN(track_uri) AS track_uri, MIN(album_uri) AS album_uri, track_title
    FROM tracks
    WHERE main_artist_uri = '{selected_artist_uri}' AND track_uri IN
    (SELECT DISTINCT track_uri
    FROM users_tracks
    WHERE user_id = {user_id} AND display_in_library = 'True')
    GROUP BY track_title
    ORDER BY track_title ASC
    '''
    )

    query_result = db.session.execute(query_sql)
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

    tracklist_featured_query = db.session.query(Tracks.track_uri, Tracks.track_artist_main, Tracks.track_artist_add1, Tracks.track_artist_add2, Tracks.track_title, Tracks.album_uri)\
        .filter((Tracks.track_artist_add1 == selected_artist_name) | (Tracks.track_artist_add2 == selected_artist_name))\
        .filter(Tracks.track_uri.in_(db.session.query(UserTracks.track_uri)\
                                     .filter_by(user_id=user_id, display_in_library=True).distinct()))\
        .all()

    tracklist_featured = []
    for track in tracklist_featured_query:
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


#TODO
def get_loose_tracks_for_subgenre(selected_genre, selected_subgenre, user_id):

    query_sql = (f'''
    SELECT track_uri, track_artist_main, track_artist_add1, track_artist_add2, track_title, album_uri
    FROM tracks
    
    WHERE track_uri IN
    (SELECT DISTINCT track_uri
    FROM users_tracks
    WHERE user_id = {user_id} AND display_in_library = 'True')
    AND track_artist_main IN
    '''
    )

    query_result = db.session.execute(query_sql)
    loose_tracks = []
    for track in query_result:
        track_dict = {
            "track_title": track.track_title,
            "track_uri": track.track_uri,
            "album_uri": track.album_uri,
            "track_artist_main": track.track_artist_main,
            "track_artist_add1": track.track_artist_add1,
            "track_artist_add2": track.track_artist_add2
        }
        loose_tracks.append(track_dict)
    return loose_tracks






