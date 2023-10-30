import spotipy

def sp_get_library(sp):

	#getting list of saved tracks ids
	saved_tracks_ids = []

	offset = 0
	while True:
		if len(sp.current_user_saved_tracks(limit=50, offset=offset, market=None)['items']) == 0:
			break
		saved_tracks = sp.current_user_saved_tracks(limit=50, offset=offset, market=None)['items']	
		for i in saved_tracks:
			saved_tracks_ids.append(i['track']['id'])
		offset += 50

	#getting list of all playlists ids
	playlists_ids = []

	offset = 0
	while True:	
		playlists = sp.current_user_playlists(limit=50, offset=offset)['items']
		if len(playlists) == 0:
			break
		for i in playlists:
			playlists_ids.append(i["id"])
		offset += 50


	#getting list of track ids from all playlists combined; some songs may have repeats
	all_playlists_tracks_ids = []

	for playlist_id in playlists_ids:
		offset = 0
		while True:
			if len(sp.playlist_tracks(playlist_id, limit=50, offset=offset, market=None)['items']) == 0:
				break
			playlists_tracks = sp.playlist_tracks(playlist_id, limit=50, offset=offset, market=None)['items']
			for i in playlists_tracks:
				all_playlists_tracks_ids.append(i['track']['id'])
			offset += 50

	#getting list of saved albums ids
	saved_albums_ids = []

	offset = 0
	while True:
		if len(sp.current_user_saved_albums(limit=50, offset=offset, market=None)['items']) == 0:
			break
		saved_albums = sp.current_user_saved_albums(limit=50, offset=offset, market=None)['items']	
		for i in saved_albums:
			saved_albums_ids.append(i['album']['id'])
		offset += 50
	

	saved_tracks_ids_set = set(saved_tracks_ids)
	print(len(saved_tracks_ids))

	all_playlists_tracks_ids_set = set(all_playlists_tracks_ids)
	print(len(all_playlists_tracks_ids))

	all_track_ids = saved_tracks_ids_set.union(all_playlists_tracks_ids_set)
	print(len(all_track_ids))

	return(saved_tracks_ids)