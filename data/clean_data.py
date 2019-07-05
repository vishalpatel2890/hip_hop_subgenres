from data.db_model import *

# fuzz is used to compare TWO strings
from fuzzywuzzy import fuzz

# process is used to compare a string to MULTIPLE other strings
from fuzzywuzzy import process

def delete_non_songs(session):
    '''
    Delete non songs (mixes, skits, etc.) from database

    Parameters
    ----------
    session : SQLAlchemy session object

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

def get_duplcates(session, artist_id):
    all_duplicates = []
    artist_songs = [(y.name, y.id) for x in session.query(Artist).filter(Artist.id == 67).all()[0].albums for y in x.songs]
    df=df_songs_merged[df_songs_merged['artist_id']== row['artist_id']]

def get_duplicates_old(session, df_songs_merged):
    all_duplicates = []
    for idx, row in df_songs_merged.iterrows():
        df=df_songs_merged[df_songs_merged['artist_id']== row['artist_id']]
        duplicate_prob = process.extract(row['name_x'], df['name_x'], scorer=fuzz.ratio)
        search = [dup[0] for dup in duplicate_prob if dup[1] > 80]
    if len(search) > 1:
        songs = []
        for song in search:
            songs.append(session.query(Song).filter(Song.name == song)[0].id)
        if len(set(songs))==1:
            duplicates = []
            for idx, song in enumerate(songs):
                song_name = session.query(Song).filter(Song.id == song)[0].name
                query = session.query(Song).filter(Song.name == song_name)[idx]
                id = query.id
                name = query.name
                artist = query.album.artist.name
                duplicates.append((name, artist, id))
            all_duplicates.append(duplicates)
        else:
            duplicates = []
            for song in songs:
                query = session.query(Song).filter(Song.id == song)[0]
                artist = query.album.artist.name
                name = query.name
                duplicates.append((name, artist, song))
            all_duplicates.append(duplicates)
        return all_duplicates

def remove_duplicates(list_duplicates):
    for i in list_duplicates:
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
