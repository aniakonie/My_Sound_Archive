from flask import Flask, url_for, redirect, render_template, request
from flask import Blueprint
import mysql.connector

views = Blueprint('views', '__name__')

@views.route('/artists', methods=["POST", "GET"])
def library_all_artists():

    vml = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "virtual_music_library"
    )

    cursor = vml.cursor()

    query = (
    '''
    SELECT track_artist_main
    FROM tracks
    GROUP BY track_artist_main
    HAVING COUNT(track_artist_main) > 2
    ORDER BY track_artist_main ASC
    '''
    )

    cursor.execute(query)

    artists = []
    for track_artist_main in cursor:
        artists.append(track_artist_main[0])

    if request.method == "POST":
        artist = request.form["artist"]
        print(artist)
        return redirect(url_for("views.library_artist", artist = artist))

    return render_template("artists.html", artists = artists)

@views.route('/artists/<artist>')
def library_artist(artist):

    vml = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "virtual_music_library"
    )

    cursor = vml.cursor()

    query = (
    '''
    SELECT track_uri, track_artist_main, track_artist_add1, track_artist_add2, track_title, album_uri
    FROM tracks
    WHERE track_artist_main = %s
    ORDER BY track_title ASC
    '''
    )

    cursor.execute(query, (artist,))

    for (track_uri, track_artist_main, track_artist_add1, track_artist_add2, track_title, album_uri) in cursor:
        print(f"{track_artist_main}, {track_artist_add1}, {track_artist_add2} - {track_title}")

    return artist