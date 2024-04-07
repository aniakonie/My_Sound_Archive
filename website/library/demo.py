from flask import Blueprint, url_for, redirect, render_template, request, abort, session
from website.database.models import *
from website.library.views import *

demo_bp = Blueprint('demo_bp', __name__, template_folder='templates')

example_id = 1

@demo_bp.route('/', methods=["POST", "GET"])
def library():

    genres = get_genres(example_id)
    if request.method == "POST":
        selected_genre = request.form["selected_genre"]
        return redirect(url_for("demo_bp.library_genres", selected_genre = selected_genre))
    return render_template("library/demo.html", genres = genres)


@demo_bp.route('/<path:selected_genre>', methods=["POST", "GET"])
def library_genres(selected_genre):

    genres = get_genres(example_id)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, example_id)

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")
        selected_subgenre = request.form.get("selected_subgenre")
        if new_selected_genre:
            return redirect(url_for("demo_bp.library_genres", selected_genre = new_selected_genre))
        elif selected_subgenre:
            return redirect(url_for("demo_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = selected_subgenre))
    return render_template("library/demo.html", genres = genres, subgenres = subgenres, selected_genre = selected_genre)


@demo_bp.route('/<path:selected_genre>/<path:selected_subgenre>', methods=["POST", "GET"])
def library_subgenres(selected_genre, selected_subgenre):

    genres = get_genres(example_id)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, example_id)
    if selected_subgenre not in subgenres:
        abort(404)

    artists = get_artists_of_selected_subgenre(selected_genre, selected_subgenre, example_id)

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")       
        new_selected_subgenre = request.form.get("selected_subgenre")
        selected_artist_uri = request.form.get("selected_artist_uri")

        if new_selected_genre:
            return redirect(url_for("demo_bp.library_genres", selected_genre = new_selected_genre))
        elif new_selected_subgenre:
            return redirect(url_for("demo_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre))
        elif selected_artist_uri:
            session["selected_artist_uri"] = selected_artist_uri
            selected_artist_name = request.form.get("selected_artist_name")
            session["selected_artist_name"] = selected_artist_name
            selected_artist_name = encode_characters(selected_artist_name)
            return redirect(url_for("demo_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_name = selected_artist_name))   

    return render_template("library/demo.html", genres = genres, subgenres = subgenres, artists = artists, selected_genre = selected_genre, selected_subgenre = selected_subgenre)


@demo_bp.route('/<path:selected_genre>/<path:selected_subgenre>/<path:selected_artist_name>', methods=["POST", "GET"])
def library_tracks(selected_genre, selected_subgenre, selected_artist_name):

    genres = get_genres(example_id)
    if selected_genre not in genres:
        abort(404)
    subgenres = get_subgenres(selected_genre, example_id)
    if selected_subgenre not in subgenres:
        abort(404)

    selected_artist_name = session["selected_artist_name"]

    artists = get_artists_of_selected_subgenre(selected_genre, selected_subgenre, example_id)
    selected_artist_uri = session["selected_artist_uri"]
    if (selected_artist_uri, selected_artist_name) not in artists:
        abort(404)

    if (selected_artist_uri, selected_artist_name) != ("Loose tracks", "Loose tracks"):
        tracklist = get_tracks_of_artist(selected_artist_uri, example_id)
        tracklist_featured = get_featured_tracks_of_artist(selected_artist_name, example_id)
    else:
        tracklist = get_loose_tracks_for_subgenre(selected_genre, selected_subgenre, example_id)
        tracklist_featured = []

    if request.method == "POST":
        new_selected_genre = request.form.get("selected_genre")
        new_selected_subgenre = request.form.get("selected_subgenre")
        new_selected_artist_uri = request.form.get("selected_artist_uri")

        session.pop("selected_artist_uri", default=None)
        session.pop("selected_artist_name", default=None)

        if new_selected_genre:
            return redirect(url_for("demo_bp.library_genres", selected_genre = new_selected_genre))
        elif new_selected_subgenre:
            return redirect(url_for("demo_bp.library_subgenres", selected_genre = selected_genre, selected_subgenre = new_selected_subgenre))
        elif new_selected_artist_uri:
            session["selected_artist_uri"] = new_selected_artist_uri
            selected_artist_name = request.form.get("selected_artist_name")
            session["selected_artist_name"] = selected_artist_name
            new_selected_artist_name = encode_characters(selected_artist_name)
            return redirect(url_for("demo_bp.library_tracks", selected_genre = selected_genre, selected_subgenre = selected_subgenre, selected_artist_name = new_selected_artist_name))        

    return render_template("library/demo.html", genres = genres, subgenres = subgenres, artists = artists, tracklist = tracklist,
                           tracklist_featured = tracklist_featured, selected_genre=selected_genre,
                           selected_subgenre=selected_subgenre, selected_artist_uri=selected_artist_uri, selected_artist_name=selected_artist_name)

