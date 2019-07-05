from data.db_model import *

from data.fetch.scrape_genius import *
from data.fetch.spotify_api import *

#function to add all albums and all songs to database
def add_albums_song_to_db(session, artist):
    done = False
    while not done:
        try:
            album_urls = scrape_artists_albums(artist)
            if len(album_urls) > 0 :
                done = True
        except Exception as e:
            print ('Selenium Failed... Restarting')
            print (f'Error : {e}')
    print(album_urls)

    for album in album_urls:
        try:
            album_data = scrape_album_data(album)
            artist_id = session.query(Artist).filter(func.lower(Artist.name) == artist.lower())[0].id
            print(artist_id)
            album_obj = Album(artist_id=artist_id, name=album_data['album_name'], release_date = album_data['release_date'])
        except Exception as e:
            # list_of_missed.append({'type': 'album_data', 'album': album, 'artist': artist})
            print ('failed to add album:', album)
            print(f'Error: {e}')


        try:
            songs = scrape_album_songs(artist, album)
            for song in songs:
                song_row = Song(name = song['name'], all_lyrics=song['all_lyrics'], artist_lyrics=song['artist_lyrics'])
                song_row.album = album_obj
        except:
            # list_of_missed.append({'type': 'album_songs', 'artist': artist, 'album': album})
            print('failed to add album_songs:', album_data['album_name'])

        try:
            session.add(album_obj)
            session.commit()
            print(f'Sucessfully added {album}')
        except:
            # list_of_missed.append({'type': 'object', 'artist' : artist, 'album' :album})
            print('failed to commit session:', artist, album)

def add_spotify_songs_to_db(session, list_of_missed):
    songs = session.query(Song).filter(Song.id >= 24548).all()
    for song in songs:
        artist = song.album.artist
        # print(artist.name, song.name)
        try:
            spotify_id = get_spotify_track_id(artist.name, song.name)
            song_data = get_spotify_track_info(spotify_id)
            spotify_data = Spotify(danceability = song_data['danceability'],
                                   energy = song_data['energy'],
                                   loudness = song_data['loudness'],
                                   speechiness = song_data['speechiness'],
                                   acousticness = song_data['acousticness'],
                                   instrumentalness = song_data['instrumentalness'],
                                   liveness = song_data['liveness'],
                                   valence = song_data['valence'],
                                   tempo = song_data['tempo']
                                  )
            spotify_data.song = song
            session.add(spotify_data)
            session.commit()
        except:
            list_of_missed.append({'type': 'spotify', 'artist': artist.name, 'song' :song.name, 'song_id': song.id})
            print(artist.name, song.name, song.id)

def delete_album(i):
    album_to_delete = session.query(Album).filter(Album.id == i)[0]
    session.delete(album_to_delete)
    session.commit()
