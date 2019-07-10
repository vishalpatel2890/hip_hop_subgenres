from db_model import *



# fuzz is used to compare TWO strings
from fuzzywuzzy import fuzz

# process is used to compare a string to MULTIPLE other strings
from fuzzywuzzy import process


def delete_non_songs(session):
    '''
    Delete "non-songs" : artifacts scraped that do not contain lyrics

    Parameters
    ----------
    session : SQLAlchemy Session Object
        SQLAlchemy session object containing current session with  connection to
        database
    '''

    songs_art = session.query(Song).filter(Song.name.contains('Album Art')).all()
    songs_credit = session.query(Song).filter(Song.name.contains('Credits')).all()
    songs_book = session.query(Song).filter(Song.name.contains('Booklet')).all()
    songs_intro = session.query(Song).filter(Song.name.contains('Intro')).all()
    songs_outro = session.query(Song).filter(Song.name.contains('Outro')).all()
    songs_live = session.query(Song).filter(Song.name.contains('(Live)')).all()
    songs_skit = session.query(Song).filter(Song.name.contains('Skit')).all()
    songs_mix = session.query(Song).filter(Song.name.contains('Mix')).all()
    songs_remix = session.query(Song).filter(Song.name.contains('mix')).all()
    songs_snippet = session.query(Song).filter(Song.name.contains('Snippet')).all()
    songs_to_delete = [songs_art, songs_credit, songs_book, songs_intro, songs_outro, songs_live, songs_skit, songs_snippet, songs_mix, songs_remix]

    for list_songs in songs_to_delete:
        for song in list_songs:
            session.delete(song)
            session.commit()


def get_duplicates(session, artist_id):
    '''
    Generate list of duplicated songs (filtered by song name and artist name).
    List does not contain first instance of that song only following duplicates

    Parameters
    ----------
    session : SQLAlchemy Session Object
        SQLAlchemy session object containing current session with  connection to
        database
    artist_id : integer
        artist unique id in database

    Returns
    --------
    all_duplicates : list
        list of song objects (SQLAlchemy) that are duplicates and need to be
        deleted
    '''
    all_duplicates = []
    artist_object = session.query(Artist).filter(Artist.id == artist_id).all()[0]
    artist_songs = [song for album in artist_object.albums for song in album.songs]
    artist_song_names = [song.name for song in artist_songs]
    for name in artist_song_names:
        duplicate_prob = process.extract(name, artist_song_names, scorer=fuzz.ratio)
        likely_duplicate = [dup[0] for dup in duplicate_prob[1:] if dup[1] > 80]
        if len(likely_duplicate) > 0:
            duplicated_songs = []

            for duplicate in likely_duplicate:
                song_object = session.query(Song).filter(and_(
                Song.name == duplicate,
                Song.album.has(artist = artist_object)))[0]

                artist_song_names.remove(duplicate)

                all_duplicates.append(song_object)
    return all_duplicates

def remove_duplicates(list_duplicates):
    for i in all_duplicates:
        for song in i[1:]:
            try:
                delete = session.query(Song).filter(Song.id == song[2])[0]
                session.delete(delete)
                session.commit()
            except:
                'not deleted'

#
# drop_songs_with_no_lyrics_0 = df_songs_merged[df_songs_merged['all_lyrics'].str.contains('Lyrics for this song')]
# drop_songs_with_no_lyrics_1 = df_songs_merged[df_songs_merged['all_lyrics'].str.contains('Lyrics will be')]
# drop_songs_with_no_lyrics_2 = df_songs_merged[df_songs_merged['all_lyrics'].str.contains('Lyrics from Snippet')]
# drop_songs_with_no_lyrics_3 = df_songs_merged[df_songs_merged.all_lyrics =='']
#df_songs[df_songs.all_lyrics.str.len() < 100]
# # for idx, song in drop_songs_with_no_lyrics_2.iterrows():
#     delete = session.query(Song).filter(Song.id == song['id_x'])[0]
#     session.delete(delete)
#     session.commit()
