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
        genres = get_genres()
        if request.method == "POST":
            selected_genre = request.form["selected_genre"]
            return redirect(url_for("library_bp.library_genres", selected_genre = selected_genre))
    return render_template("library/library.html", genres = genres, current = "library", user = current_user.username)



@library_bp.route('/<selected_genre>', methods=["POST", "GET"])
@login_required
def library_genres(selected_genre):

    genres = get_genres()
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre)

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")
        selected_subgenre = request.form.get("selected_subgenre")
        if new_selected_genre != None:
            return redirect(url_for("library_bp.library_genres", selected_genre = new_selected_genre, current = "library"))
        elif selected_subgenre != None:
            print(selected_genre)
            return redirect(url_for("library_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = selected_subgenre, current = "library"))
    return render_template("library/library.html", genres = genres, subgenres = subgenres, current = "library")



@library_bp.route('/<selected_genre>/<selected_subgenre>', methods=["POST", "GET"])
@login_required
def library_subgenres(selected_genre, selected_subgenre):

    genres = get_genres()
    subgenres = get_subgenres(selected_genre)

    if selected_genre not in genres or selected_subgenre not in subgenres:
        abort(404)

    artists = get_artists_of_selected_subgenre(selected_genre, selected_subgenre)
    print(artists)

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")       
        new_selected_subgenre = request.form.get("selected_subgenre")
        selected_artist = request.form.get("selected_artist")

        if new_selected_genre != None:
            return redirect(url_for("library_bp.library_genres", selected_genre = new_selected_genre, current = "library"))
        elif new_selected_subgenre != None:
            return redirect(url_for("library_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre, current = "library"))
        elif selected_artist != None:
            return redirect(url_for("library_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist = selected_artist, current = "library"))        

    return render_template("library/library.html", genres = genres, subgenres = subgenres, artists = artists, current = "library")




@library_bp.route('/<selected_genre>/<selected_subgenre>/<selected_artist>', methods=["POST", "GET"])
def library_tracks(selected_genre, selected_subgenre, selected_artist):









    # if selected_artist != "Loose tracks":

    #     query_tracks = (
    #     '''
    #     SELECT *
    #     FROM tracks
    #     WHERE track_artist_main = %s
    #     ORDER BY track_title ASC
    #     '''
    #     )

    #     cursor.execute(query_tracks, (selected_artist,))

    # elif selected_artist == "Loose tracks":

    #     query_tracks = (
    #     '''
    #     SELECT *
    #     FROM tracks
    #     LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
    #     WHERE artist_genre = %s AND track_artist_main IN (
    #     SELECT track_artist_main
    #     FROM tracks
    #     LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
    #     GROUP BY track_artist_main
    #     HAVING COUNT(track_artist_main) < 3
    #     )
    #     ORDER BY track_artist_main ASC
    #     '''
    #     )

    #     cursor.execute(query_tracks, (selected_folder,))

    # tracklist = []
    # for row in cursor:
    #     tracklist.append(row)


    # if selected_artist != "Loose tracks":

    #     query_featured_tracks = (
    #     '''    
    #     SELECT *
    #     FROM tracks
    #     WHERE track_artist_add1 = %s OR track_artist_add2 = %s
    #     OR track_artist_main != %s AND album_artist_main = %s
    #     ORDER BY track_title ASC;
    #     '''
    #     )
        
    #     cursor.execute(query_featured_tracks, (selected_artist,)*4)

    #     tracklist_featured = []
    #     for row in cursor:
    #         tracklist_featured.append(row)


    # if request.method == "POST":
    #     try:
    #         selected_artist = request.form["selected_artist"]
    #         return redirect(url_for("library_bp.library_tracks", selected_folder=selected_folder, selected_artist = selected_artist, current = "library"))

    #     except:
    #         selected_folder = request.form["selected_folder"]
    #         return redirect(url_for("library_bp.library_folders", selected_folder = selected_folder, current = "library"))

    # return render_template("library/library.html", tracklist = tracklist, genre=genre, artists_folders = artists_folders, tracklist_featured = tracklist_featured, selected_artist = selected_artist, current = "library")

    return render_template("library/library.html", tracklist = tracklist, genre=genre, artists_folders = artists_folders, tracklist_featured = tracklist_featured, selected_artist = selected_artist, current = "library")






def get_genres():
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
    WHERE user_id = {current_user.id} AND display_in_library = 'True')
    ORDER BY artist_main_genre ASC
    '''
    )

    query_result = db.session.execute(query_sql)
    genres = [genre.artist_main_genre for genre in query_result]
    genres.remove("others")
    genres.append("others")
    return genres




def get_subgenres(selected_genre):
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
    WHERE user_id = {current_user.id} AND display_in_library = 'True')
    ORDER BY artist_subgenre ASC
    '''
    )

    query_result = db.session.execute(query_sql)
    subgenres = [subgenre.artist_subgenre for subgenre in query_result]
    subgenres.remove("others")
    subgenres.append("others")
    return subgenres




def get_artists_of_selected_subgenre(selected_genre, selected_subgenre):
    '''Select all artists which play particular subgenre and user owns in his library at least 3 songs of this artist'''

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
    WHERE user_id = {current_user.id} AND display_in_library = 'True'
    GROUP BY tracks.main_artist_uri
    HAVING COUNT(tracks.main_artist_uri) > {no_of_songs})
    ORDER BY artist_subgenre ASC
    '''
    )

    query_result = db.session.execute(query_sql)
    artists = [artist.artist_name for artist in query_result]
    artists.append("Loose tracks")
    return artists







def get_loose_tracks_for_subgenre(selected_subgenre):
    pass







def get_tracks_of_artist(selected_artist_uri):
    '''Select all tracks of selected artist along with featured tracks'''


    query_sql = (f'''
    SELECT track_uri, track_artist_main, track_artist_add1, track_artist_add2, track_title, album_uri
    FROM tracks
    WHERE track_artist_main = '{selected_artist_uri}' AND track_uri IN
    (SELECT DISTINCT track_uri
    FROM users_tracks
    WHERE user_id = {current_user.user_id} AND display_in_library = 'True')
    '''
    )






def get_featured_tracks_of_artist(selected_artist_uri):
    '''Select all tracks of selected artist along with featured tracks'''


    query_sql = (f'''
    SELECT track_uri, track_artist_main, track_artist_add1, track_artist_add2, track_title, album_uri
    FROM tracks
    WHERE track_uri = '{selected_artist_uri}' OR track_uri = '{selected_artist_uri}' AND track_uri IN
    (SELECT DISTINCT track_uri
    FROM users_tracks
    WHERE user_id = {current_user.user_id} AND display_in_library = 'True')
    '''
    )













# def get_artists_of_selected_genre(genre, user_id, no_of_songs):
#     '''Select all artists which play particular genre and user owns in his library at least 3 songs of this artist'''

#     query_sql = (f'''
#     SELECT artist_name
#     FROM artists_genres
#     WHERE artist_main_genre = '{genre}' AND artist_uri IN
#     (SELECT tracks.main_artist_uri
#     FROM users_tracks
#     INNER JOIN tracks ON users_tracks.track_uri = tracks.track_uri
#     WHERE user_id = '{user_id}' AND display_in_library = 'True'
#     GROUP BY tracks.main_artist_uri
#     HAVING COUNT(tracks.main_artist_uri) > {no_of_songs})
#     ORDER BY artist_name ASC;
#     '''
#     )

#     query_result = db.session.execute(query_sql)
#     artists_folders = ["Loose tracks"]
#     artists = [artist.artist_name for artist in query_result]
#     for artist in artists:
#         artists_folders.append(artist)
#     return artists_folders














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