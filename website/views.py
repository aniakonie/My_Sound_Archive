from flask import Flask, url_for, redirect, render_template, request
from flask import Blueprint
import mysql.connector

views = Blueprint('views', '__name__')


@views.route('/', methods=["POST", "GET"])
def library():

    folders = ["All artists", "Rock", "Others"]

    if request.method == "POST":
        selected_folder = request.form["selected_folder"]
        return redirect(url_for("views.library_folders", selected_folder = selected_folder))

    return render_template("artists.html", folders = folders)


@views.route('/<selected_folder>', methods=["POST", "GET"])
def library_folders(selected_folder):

    folders = ["All artists", "Rock", "Others"]

    vml = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "virtual_music_library"
    )

    cursor = vml.cursor()

    query_artists = (
    '''
    SELECT track_artist_main
    FROM tracks
    GROUP BY track_artist_main
    HAVING COUNT(track_artist_main) > 2
    ORDER BY track_artist_main ASC
    '''
    )

    cursor.execute(query_artists)

    artists_folders = []
    for track_artist_main in cursor:
        artists_folders.append(track_artist_main[0])

    #IMPROVE THIS!!!!!!!!!!!!
    if request.method == "POST":
        try:
            selected_artist = request.form["selected_artist"]
            return redirect(url_for("views.library_tracks", selected_folder=selected_folder, selected_artist = selected_artist))

        except:
            selected_folder = request.form["selected_folder"]
            return redirect(url_for("views.library_folders", selected_folder = selected_folder))

    return render_template("artists.html", artists_folders = artists_folders, folders=folders)


@views.route('/<selected_folder>/<selected_artist>', methods=["POST", "GET"])
def library_tracks(selected_folder, selected_artist):

    folders = ["All artists", "Rock", "Others"]
    
    vml = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "virtual_music_library"
    )

    cursor = vml.cursor()

    query_artists = (
    '''
    SELECT track_artist_main
    FROM tracks
    GROUP BY track_artist_main
    HAVING COUNT(track_artist_main) > 2
    ORDER BY track_artist_main ASC
    '''
    )

    cursor.execute(query_artists)

    artists_folders = []
    for track_artist_main in cursor:
        artists_folders.append(track_artist_main[0])

    cursor = vml.cursor(dictionary=True)

    query_tracks = (
    '''
    SELECT *
    FROM tracks
    WHERE track_artist_main = %s
    ORDER BY track_title ASC
    '''
    )

    cursor.execute(query_tracks, (selected_artist,))

    tracklist = []
    for row in cursor:
        tracklist.append(row)

    if request.method == "POST":
        try:
            selected_artist = request.form["selected_artist"]
            return redirect(url_for("views.library_tracks", selected_folder=selected_folder, selected_artist = selected_artist))

        except:
            selected_folder = request.form["selected_folder"]
            return redirect(url_for("views.library_folders", selected_folder = selected_folder))

    return render_template("artists.html", tracklist = tracklist, folders=folders, artists_folders = artists_folders)

