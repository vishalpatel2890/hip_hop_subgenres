from zopfli.zlib import compress


#function calculates how much a song is compressed - 0 - least compressed 1 - most compreseed
def zopfli_compress(lyrics):
    return 1-len(compress(lyrics))/len(lyrics)

def add_repetiveness_to_db(session, query):
    '''
    Pass sqlalchemy session and list of songs (sqlalchemy model)
    '''
    for song in query:
        lyrics = song.all_lyrics.replace('\n', '')
        print(lyrics[:30], song.id)
        song.repetitiveness = zopfli_compress(lyrics)
        session.commit()
