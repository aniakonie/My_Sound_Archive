from flask import url_for, redirect, render_template, request
from flask import Blueprint
from website.database.database_connect import db_connect
import mysql.connector


library_views_bp = Blueprint('library_views_bp', __name__, template_folder='templates')


@library_views_bp.route('/', methods=["POST", "GET"])
def library():

    folders = ["rock", "metal", "jazz", "pop", "reggae", "electronic", "funk", "others"]

    if request.method == "POST":
        selected_folder = request.form["selected_folder"]
        return redirect(url_for("library_views_bp.library_folders", selected_folder = selected_folder))

    return render_template("library_views/library_views.html", folders = folders, current = "library")


@library_views_bp.route('/<selected_folder>', methods=["POST", "GET"])
def library_folders(selected_folder):

    folders = ["rock", "metal", "jazz", "pop", "reggae", "electronic", "funk", "others"]

    vml, cursor = db_connect()
    cursor = vml.cursor()

    query_artists = (
    '''
    SELECT track_artist_main
    FROM tracks
    LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
    WHERE artist_genre = %s
    GROUP BY track_artist_main
    HAVING COUNT(track_artist_main) > 2
    ORDER BY track_artist_main ASC;
    '''
    )

    cursor.execute(query_artists, (selected_folder,))

    artists_folders = ["Loose tracks"]
    for track_artist_main in cursor:
        artists_folders.append(track_artist_main[0])

    #IMPROVE THIS!!!!!!!!!!!!
    if request.method == "POST":
        try:
            selected_artist = request.form["selected_artist"]
            return redirect(url_for("library_views_bp.library_tracks", selected_folder=selected_folder, selected_artist = selected_artist, current = "library"))

        except:
            selected_folder = request.form["selected_folder"]
            return redirect(url_for("library_views_bp.library_folders", selected_folder = selected_folder, current = "library"))

    return render_template("library_views/library_views.html", artists_folders = artists_folders, folders=folders, current = "library")


@library_views_bp.route('/<selected_folder>/<selected_artist>', methods=["POST", "GET"])
def library_tracks(selected_folder, selected_artist):

    tracklist_featured = ''

    folders = ["rock", "metal", "jazz", "pop", "reggae", "electronic", "funk", "others"]
    
    vml, cursor = db_connect()
    cursor = vml.cursor()

    query_artists = (
    '''
    SELECT track_artist_main
    FROM tracks
    LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
    WHERE artist_genre = %s
    GROUP BY track_artist_main
    HAVING COUNT(track_artist_main) > 2
    ORDER BY track_artist_main ASC;
    '''
    )

    cursor.execute(query_artists, (selected_folder,))

    artists_folders = ["Loose tracks"]
    for track_artist_main in cursor:
        artists_folders.append(track_artist_main[0])

    cursor = vml.cursor(dictionary=True)


    if selected_artist != "Loose tracks":

        query_tracks = (
        '''
        SELECT *
        FROM tracks
        WHERE track_artist_main = %s
        ORDER BY track_title ASC
        '''
        )

        cursor.execute(query_tracks, (selected_artist,))

    elif selected_artist == "Loose tracks":

        query_tracks = (
        '''
        SELECT *
        FROM tracks
        LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
        WHERE artist_genre = %s AND track_artist_main IN (
        SELECT track_artist_main
        FROM tracks
        LEFT JOIN artists_uris_genres ON main_artist_uri = artist_uri
        GROUP BY track_artist_main
        HAVING COUNT(track_artist_main) < 3
        )
        ORDER BY track_artist_main ASC
        '''
        )

        cursor.execute(query_tracks, (selected_folder,))

    tracklist = []
    for row in cursor:
        tracklist.append(row)


    if selected_artist != "Loose tracks":

        query_featured_tracks = (
        '''    
        SELECT *
        FROM tracks
        WHERE track_artist_add1 = %s OR track_artist_add2 = %s
        OR track_artist_main != %s AND album_artist_main = %s
        ORDER BY track_title ASC;
        '''
        )
        
        cursor.execute(query_featured_tracks, (selected_artist,)*4)

        tracklist_featured = []
        for row in cursor:
            tracklist_featured.append(row)


    if request.method == "POST":
        try:
            selected_artist = request.form["selected_artist"]
            return redirect(url_for("library_views_bp.library_tracks", selected_folder=selected_folder, selected_artist = selected_artist, current = "library"))

        except:
            selected_folder = request.form["selected_folder"]
            return redirect(url_for("library_views_bp.library_folders", selected_folder = selected_folder, current = "library"))

    return render_template("library_views/library_views.html", tracklist = tracklist, folders=folders, artists_folders = artists_folders, tracklist_featured = tracklist_featured, selected_artist = selected_artist, current = "library")