from flask import Blueprint, url_for, redirect, render_template, request, abort
from flask_login import login_required, current_user
from website.database.models import *


library_bp = Blueprint('library_bp', __name__, template_folder='templates')


@library_bp.route('/', methods=["POST", "GET"])
@login_required
def library():
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

    no_of_songs = 2 #TODO retrieve from user's settings table
    artists_folders = get_artists_of_selected_genre(selected_genre, current_user.id, no_of_songs)

    #IMPROVE THIS!!!!!!!!!!!!
    if request.method == "POST":
        try:
            selected_artist = request.form["selected_artist"]
            return redirect(url_for("library_bp.library_tracks", selected_folder=selected_folder, selected_artist = selected_artist, current = "library"))

        except:
            selected_folder = request.form["selected_folder"]
            return redirect(url_for("library_bp.library_folders", selected_folder = selected_folder, current = "library"))

    return render_template("library/library.html", artists_folders = artists_folders, genres = genres, current = "library")



# @library_bp.route('/<selected_genre>/<selected_subgenre>', methods=["POST", "GET"])
# @login_required
# def library_genres(selected_genre, selected_subgenre):

#     genres = get_genres()
#     subgenres = get_subgenres()
#     if selected_genre not in genres:
#         abort(404)





# @library_bp.route('/<selected_folder>/<selected_artist>', methods=["POST", "GET"])
# def library_tracks(selected_folder, selected_artist):

#     tracklist_featured = ''

#     folders = ["rock", "metal", "jazz", "pop", "reggae", "electronic", "funk", "others"]
    
#     vml, cursor = db_connect()
#     cursor = vml.cursor()

#     query_artists = (
#     '''
#     SELECT track_artist_main
#     FROM tracks
#     LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
#     WHERE artist_genre = %s
#     GROUP BY track_artist_main
#     HAVING COUNT(track_artist_main) > 2
#     ORDER BY track_artist_main ASC;
#     '''
#     )

#     cursor.execute(query_artists, (selected_folder,))

#     artists_folders = ["Loose tracks"]
#     for track_artist_main in cursor:
#         artists_folders.append(track_artist_main[0])

#     cursor = vml.cursor(dictionary=True)


#     if selected_artist != "Loose tracks":

#         query_tracks = (
#         '''
#         SELECT *
#         FROM tracks
#         WHERE track_artist_main = %s
#         ORDER BY track_title ASC
#         '''
#         )

#         cursor.execute(query_tracks, (selected_artist,))

#     elif selected_artist == "Loose tracks":

#         query_tracks = (
#         '''
#         SELECT *
#         FROM tracks
#         LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
#         WHERE artist_genre = %s AND track_artist_main IN (
#         SELECT track_artist_main
#         FROM tracks
#         LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
#         GROUP BY track_artist_main
#         HAVING COUNT(track_artist_main) < 3
#         )
#         ORDER BY track_artist_main ASC
#         '''
#         )

#         cursor.execute(query_tracks, (selected_folder,))

#     tracklist = []
#     for row in cursor:
#         tracklist.append(row)


#     if selected_artist != "Loose tracks":

#         query_featured_tracks = (
#         '''    
#         SELECT *
#         FROM tracks
#         WHERE track_artist_add1 = %s OR track_artist_add2 = %s
#         OR track_artist_main != %s AND album_artist_main = %s
#         ORDER BY track_title ASC;
#         '''
#         )
        
#         cursor.execute(query_featured_tracks, (selected_artist,)*4)

#         tracklist_featured = []
#         for row in cursor:
#             tracklist_featured.append(row)


#     if request.method == "POST":
#         try:
#             selected_artist = request.form["selected_artist"]
#             return redirect(url_for("library_bp.library_tracks", selected_folder=selected_folder, selected_artist = selected_artist, current = "library"))

#         except:
#             selected_folder = request.form["selected_folder"]
#             return redirect(url_for("library_bp.library_folders", selected_folder = selected_folder, current = "library"))

#     return render_template("library/library.html", tracklist = tracklist, folders=folders, artists_folders = artists_folders, tracklist_featured = tracklist_featured, selected_artist = selected_artist, current = "library")


def get_genres():
    artists_main_genres = Genre.query.with_entities(Genre.genre).distinct().order_by(Genre.genre.asc())
    genres = [genre.genre for genre in artists_main_genres] + ['others']
    return genres





def get_subgenres():
    pass





def get_artists_of_selected_genre(genre, user_id, no_of_songs):
    '''Select all artists which play particular genre and user owns in his library at least 3 songs of this artist'''

    query_sql = (f'''
    SELECT artist_name
    FROM artists_genres
    WHERE artist_main_genre = '{genre}' AND artist_uri IN
    (SELECT tracks.main_artist_uri
    FROM users_tracks
    INNER JOIN tracks ON users_tracks.track_uri = tracks.track_uri
    WHERE user_id = '{user_id}' AND display_in_library = 'True'
    GROUP BY tracks.main_artist_uri
    HAVING COUNT(tracks.main_artist_uri) > {no_of_songs})
    ORDER BY artist_name ASC;
    '''
    )

    query_result = db.session.execute(query_sql)
    artists_folders = ["Loose tracks"]
    artists = [artist.artist_name for artist in query_result]
    for artist in artists:
        artists_folders.append(artist)
    return artists_folders
