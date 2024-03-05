from flask import Blueprint, url_for, redirect, render_template, request, abort, session
from flask_login import login_required, current_user
from website.database.models import *


library_bp = Blueprint('library_bp', __name__, template_folder='templates')


@library_bp.route('/', methods=["POST", "GET"])
@login_required
def library():
    if not current_user.is_library_created:
        genres = None
        if request.method == "POST":
            session["allowed"] = True
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

    # else:
    #     pass

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


#FIX THIS
def get_genres(user_id):
    '''Select all genres'''

    query_sql = (f'''
    SELECT DISTINCT
    COALESCE(users_artists_genres.artist_main_genre_custom, artists_genres.artist_main_genre) AS artist_main_genre
    FROM artists_genres
    LEFT JOIN users_artists_genres ON artists_genres.artist_uri = users_artists_genres.artist_uri
    WHERE artists_genres.artist_uri IN
    (SELECT tracks.main_artist_uri
    FROM users_tracks
    INNER JOIN tracks ON users_tracks.track_uri = tracks.track_uri
    WHERE user_id = {user_id} AND display_in_library = 'True')
    ORDER BY artist_main_genre ASC
    '''
    )

    query_result = db.session.execute(query_sql)
    genres = [genre.artist_main_genre for genre in query_result]
    genres.remove("others")
    genres.append("others")
    return genres



#FIX THIS
def get_subgenres(selected_genre, user_id):
    '''Select all subgenres for selected genre'''

    query_sql = (f'''
    SELECT DISTINCT
    COALESCE(users_artists_genres.artist_subgenre_custom, artists_genres.artist_subgenre) AS artist_subgenre,
    COALESCE(users_artists_genres.artist_main_genre_custom, artists_genres.artist_main_genre) AS artist_main_genre
    FROM artists_genres
    LEFT JOIN users_artists_genres ON artists_genres.artist_uri = users_artists_genres.artist_uri
    WHERE artist_main_genre = '{selected_genre}' AND artists_genres.artist_uri IN
    (SELECT tracks.main_artist_uri
    FROM users_tracks
    INNER JOIN tracks ON users_tracks.track_uri = tracks.track_uri
    WHERE user_id = {user_id} AND display_in_library = 'True')
    ORDER BY artist_subgenre ASC
    '''
    )

    query_result = db.session.execute(query_sql)
    subgenres = [subgenre.artist_subgenre for subgenre in query_result]
    subgenres.remove("others")
    subgenres.append("others")
    return subgenres


#FIX THIS
def get_artists_of_selected_subgenre(selected_genre, selected_subgenre, user_id):
    '''Select all artists which play particular subgenre and user owns in his library at least 3 songs of this artist'''
    #TODO RETRIEVE THIS FROM USER'S SETTINGS
    no_of_songs = 2

    query_sql = (f'''
    SELECT DISTINCT artists_genres.artist_uri,
    artists_genres.artist_name,
    COALESCE(users_artists_genres.artist_subgenre_custom, artists_genres.artist_subgenre) AS artist_subgenre,
    COALESCE(users_artists_genres.artist_main_genre_custom, artists_genres.artist_main_genre) AS artist_main_genre
    FROM artists_genres
    LEFT JOIN users_artists_genres ON artists_genres.artist_uri = users_artists_genres.artist_uri
    WHERE artist_main_genre = '{selected_genre}' AND artist_subgenre = '{selected_subgenre}' AND artists_genres.artist_uri IN
    (SELECT tracks.main_artist_uri
    FROM users_tracks
    INNER JOIN tracks ON users_tracks.track_uri = tracks.track_uri
    WHERE user_id = {user_id} AND display_in_library = 'True'
    GROUP BY tracks.main_artist_uri
    HAVING COUNT(tracks.main_artist_uri) > {no_of_songs})
    ORDER BY artists_genres.artist_name ASC
    '''
    )

    query_result = db.session.execute(query_sql)
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

    query_sql = (f'''
    SELECT track_uri, track_artist_main, track_artist_add1, track_artist_add2, track_title, album_uri
    FROM tracks
    WHERE track_artist_add1 = '{selected_artist_name}' OR track_artist_add2 = '{selected_artist_name}' AND track_uri IN
    (SELECT DISTINCT track_uri
    FROM users_tracks
    WHERE user_id = {user_id} AND display_in_library = 'True')
    '''
    )

    query_result = db.session.execute(query_sql)
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




# select track_artist_main from tracks
# where track_uri in(
# select track_uri from users_tracks
# where users_tracks.user_id = 3 and users_tracks.display_in_library = 'True')
# group by track_artist_main
# having count(track_artist_main) < 3






# entire artists_genres table + custom genres and subgenres for a particular user

# SELECT artists_genres.artist_uri,
# COALESCE(users_artists_genres.artist_main_genre_custom, artists_genres.artist_main_genre) AS artist_main_genre,
# COALESCE(users_artists_genres.artist_subgenre_custom, artists_genres.artist_subgenre) AS artist_subgenre
# FROM artists_genres
# LEFT JOIN users_artists_genres ON artists_genres.artist_uri = users_artists_genres.artist_uri
# AND users_artists_genres.user_id = 3



# table with artist name, genre and subgenre for one user (custom genres and subgenres included)

# SELECT
# artists_genres.artist_name,
# COALESCE(users_artists_genres.artist_main_genre_custom, artists_genres.artist_main_genre) AS artist_main_genre,
# COALESCE(users_artists_genres.artist_subgenre_custom, artists_genres.artist_subgenre) AS artist_subgenre
# FROM artists_genres
# LEFT JOIN users_artists_genres ON artists_genres.artist_uri = users_artists_genres.artist_uri
# WHERE artists_genres.artist_uri IN
# (SELECT tracks.main_artist_uri
# FROM users_tracks
# INNER JOIN tracks ON users_tracks.track_uri = tracks.track_uri
# WHERE user_id = {current_user.id} AND display_in_library = 'True')



# tables users_artists_genres and artist_genres combined, artists for one user only

# SELECT *
# FROM artists_genres
# LEFT JOIN users_artists_genres ON artists_genres.artist_uri = users_artists_genres.artist_uri
# WHERE artists_genres.artist_uri IN
# (SELECT tracks.main_artist_uri
# FROM users_tracks
# INNER JOIN tracks ON users_tracks.track_uri = tracks.track_uri
# WHERE user_id = 3 AND display_in_library = 'True')
    


# SELECT artists_genres.artist_uri,
# COALESCE(users_artists_genres.artist_main_genre_custom, artists_genres.artist_main_genre) AS artist_main_genre,
# COALESCE(users_artists_genres.artist_subgenre_custom, artists_genres.artist_subgenre) AS artist_subgenre
# FROM artists_genres
# LEFT JOIN users_artists_genres ON artists_genres.artist_uri = users_artists_genres.artist_uri
# WHERE user_id = 3 AND artist_main_genre = 'electronic' AND artist_subgenre = 'liquid funk'