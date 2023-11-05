import spotipy

def sp_get_artists_genres(sp, artists_uris):

    artists_uris_list = list(artists_uris.keys())

    artists_uris_genres = set()

    n = len(artists_uris_list)//50
    a = 0
    b = 50
    for i in range(n):
        artists_50items = artists_uris_list[a:b]
        artists = sp.artists(artists = artists_50items)["artists"]
        for k in artists:
            artists_uris_genres.add((k["uri"], k["name"], tuple(k["genres"])))
        a += 50
        b += 50

    artists_therest = artists_uris_list[n*50:]
    artists = sp.artists(artists = artists_therest)["artists"]
    for k in artists:
        artists_uris_genres.add((k["uri"], k["name"], tuple(k["genres"])))

    return artists_uris_genres

