import spotipy

def sp_get_library(sp):

	#this will be a list of dictionaries, one dictionary = parameters for one song
	saved_tracks = []

	offset = 0
	while True:
		saved_tracks.extend(sp.current_user_saved_tracks(limit=50, offset=offset, market=None)['items'])
		if len(sp.current_user_saved_tracks(limit=50, offset=offset, market=None)['items']) == 0:
			break
		offset += 50

	#iterating through list with saved tracks
	#GETTING DATA FOR USER_SAVED_TRACKS DATABASE WITH A STRUCTURE: track_uri, track_artists, track_title, album_artists, album_title, album_uri
	
	saved_tracks_library = []
	artists_uris = {}

	for i in saved_tracks:

		#link for playing the track (works in the desktop app only)
		track_uri = i["track"]["uri"]

		track_title = i["track"]["name"]

		#album artists
		album_artists_dict = i["track"]["album"]["artists"]
		album_artists = []
		for k in album_artists_dict:
			album_artist = k["name"]
			album_artists.append(album_artist)

		#track artists and artists_uris
		track_artists_list = i["track"]["artists"]
		track_artists = []
		for k in track_artists_list:
			track_artist = k["name"]
			track_artists.append(track_artist)

			if track_artist not in artists_uris:
				artists_uris[track_artist] = k["uri"]

		album_title = i["track"]["album"]["name"]
		album_uri = i["track"]["album"]["uri"]

		saved_track = {"track_uri": track_uri, "track_artists": track_artists, "track_title": track_title, "album_artists": album_artists, "album_title": album_title, "album_uri": album_uri}
        
		saved_tracks_library.append(saved_track)

	return artists_uris

	# #iterating through list with playlists
	# #GETTING DATA FOR USER_SAVED_TRACKS DATABASE WITH A STRUCTURE: track_uri, track_artists, track_title, album_artists, album_title, album_uri

	# playlists = []

	# offset = 0
	# while True:
	# 	playlists.extend(sp.current_user_playlists(limit=50, offset=offset)['items'])
	# 	if len(sp.current_user_playlists(limit=50, offset=offset)['items']) == 0:
	# 		break
	# 	offset += 50

	# playlists_ids = []
	# for i in playlists:
	# 	playlists_ids.append(i["id"])
	
	# #list of tracks from all playlists combined; some songs may have repeats
	# all_playlists_tracks = []

	# for playlist_id in playlists_ids:
	# 	offset = 0
	# 	while True:
	# 		all_playlists_tracks.extend(sp.playlist_tracks(playlist_id, limit=50, offset=offset, market=None, fields="items(id)", additional_types=('track', )))
	# 		if len(sp.playlist_tracks(playlist_id, limit=50, offset=offset, market=None, fields="items(id)", additional_types=('track', ))) == 0:
	# 			break
	# 		offset += 50
	
	# spotify_track_ids_fromplaylists = []
	# for i in all_playlists_tracks:
	# 	spotify_track_ids_fromplaylists.append(i["id"])

	# print(playlists_ids)
	# print(len(all_playlists_tracks))


