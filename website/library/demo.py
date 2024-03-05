from flask import Blueprint, url_for, redirect, render_template, request, abort, session
from website.database.models import *
from website.library.views import *

demo_bp = Blueprint('demo_bp', __name__, template_folder='templates')


@demo_bp.route('/', methods=["POST", "GET"])
def library():
    genres = get_genres(3)
    if request.method == "POST":
        selected_genre = request.form["selected_genre"]
        return redirect(url_for("demo_bp.library_genres", selected_genre = selected_genre))
    return render_template("library/demo.html", genres = genres, current = "library")


@demo_bp.route('/<selected_genre>', methods=["POST", "GET"])
def library_genres(selected_genre):

    genres = get_genres(3)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, 3)

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")
        selected_subgenre = request.form.get("selected_subgenre")
        if new_selected_genre != None:
            return redirect(url_for("demo_bp.library_genres", selected_genre = new_selected_genre))
        elif selected_subgenre != None:
            return redirect(url_for("demo_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = selected_subgenre))
    return render_template("library/demo.html", genres = genres, subgenres = subgenres, current = "library", selected_genre = selected_genre)


@demo_bp.route('/<selected_genre>/<selected_subgenre>', methods=["POST", "GET"])
def library_subgenres(selected_genre, selected_subgenre):

    genres = get_genres(3)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, 3)
    if selected_subgenre not in subgenres:
        abort(404)

    artists = get_artists_of_selected_subgenre(selected_genre, selected_subgenre, 3)

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")       
        new_selected_subgenre = request.form.get("selected_subgenre")
        selected_artist_uri = request.form.get("selected_artist_uri")

        if new_selected_genre != None:
            return redirect(url_for("demo_bp.library_genres", selected_genre = new_selected_genre))
        elif new_selected_subgenre != None:
            return redirect(url_for("demo_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre))
        elif selected_artist_uri != None:
            selected_artist_name = request.form.get("selected_artist_name")
            session["selected_artist_uri"] = selected_artist_uri
            return redirect(url_for("demo_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_name = selected_artist_name))   

    return render_template("library/demo.html", genres = genres, subgenres = subgenres, artists = artists, current = "library", selected_genre = selected_genre, selected_subgenre = selected_subgenre)


@demo_bp.route('/<selected_genre>/<selected_subgenre>/<selected_artist_name>', methods=["POST", "GET"])
def library_tracks(selected_genre, selected_subgenre, selected_artist_name):

    genres = get_genres(3)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, 3)
    if selected_subgenre not in subgenres:
        abort(404)

    artists = get_artists_of_selected_subgenre(selected_genre, selected_subgenre, 3)
    selected_artist_uri = session["selected_artist_uri"]
    if (selected_artist_uri, selected_artist_name) not in artists:
        abort(404)

    if (selected_artist_uri, selected_artist_name) != ("Loose tracks", "Loose tracks"):
        tracklist = get_tracks_of_artist(selected_artist_uri, 3)
        tracklist_featured = get_featured_tracks_of_artist(selected_artist_name, 3)

    # else:
    #     pass

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")
        new_selected_subgenre = request.form.get("selected_subgenre")
        new_selected_artist_uri = request.form.get("selected_artist_uri")

        if new_selected_genre != None:
            return redirect(url_for("demo_bp.library_genres", selected_genre = new_selected_genre))
        elif new_selected_subgenre != None:
            return redirect(url_for("demo_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre))
        elif new_selected_artist_uri != None:
            new_selected_artist_name = request.form.get("selected_artist_name")
            session.pop("selected_artist_uri", default=None)
            session["selected_artist_uri"] = new_selected_artist_uri
            return redirect(url_for("demo_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_name = new_selected_artist_name))        

    return render_template("library/demo.html", genres = genres, subgenres = subgenres, artists = artists, tracklist = tracklist, tracklist_featured = tracklist_featured,
                           current = "library", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_uri = selected_artist_uri)

