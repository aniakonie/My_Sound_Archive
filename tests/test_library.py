import pytest
from website.__init__ import create_app

from website.database.models import *
from website.library.views import *
from sqlalchemy import func, select, and_, distinct


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })

    yield app



def test_library(app, user_id=28):
    '''
    checks if all user's tracks are displayed on the website and no track is omitted;
    compares the number of displayed tracks with the number of tracks in database
    '''
    with app.app_context():

        #number of tracks in database
        subquery = (
            select([UserTracks.track_uri]).distinct()
            .filter(and_(UserTracks.user_id == user_id, UserTracks.display_in_library == 'True'))
        )
        query = (
            select([func.min(Tracks.track_uri).label('track_uri'), Tracks.track_title, Tracks.main_artist_uri])
            .filter(Tracks.track_uri.in_(subquery))
            .group_by(Tracks.track_title, Tracks.main_artist_uri)
        )
        query_result = db.session.execute(query)
        result = []
        for track in query_result:
            result.append(track.track_uri)
        no_of_tracks_in_database = len(result)


        #number of tracks displayed on website
        track_count = 0
        genres = get_genres(user_id)
        print(genres)
        for genre in genres:
            subgenres = get_subgenres(genre, user_id)
            print(subgenres)
            for subgenre in subgenres:
                artists = get_artists_of_selected_subgenre(genre, subgenre, user_id)
                for artist in artists:
                    artist_uri = artist[0]
                    if artist_uri != "Loose tracks":
                        tracklist = get_tracks_of_artist(artist_uri, user_id)
                        track_count += len(tracklist)
                    else:
                        tracklist = get_loose_tracks_for_subgenre(genre, subgenre, user_id)
                        track_count += len(tracklist)

        no_of_tracks_displayed = track_count

    assert no_of_tracks_displayed == no_of_tracks_in_database


