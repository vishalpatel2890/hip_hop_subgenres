import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

engine = create_engine('sqlite:///hiphop_rec.db')
engine2 = create_engine('sqlite:///hiphop_rec1.db')

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    decade = Column(String)
    albums = relationship('Album', back_populates='artist', cascade="all, delete-orphan")

class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship('Artist', back_populates='albums')
    release_date = Column(DateTime)
    songs = relationship('Song', back_populates='album', cascade="all, delete-orphan")

class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship('Album', back_populates='songs')
    all_lyrics = Column(String)
    artist_lyrics = Column(String)
    spotify_data = relationship('Spotify', back_populates='song', cascade="all, delete-orphan")
    repetitiveness = Column(Float)
    rhyme = Column(Float)
    topic = Column(Integer)

class Spotify(Base):
    __tablename__ = 'spotify_song_data'
    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'))
    song = relationship('Song', back_populates='spotify_data')
    danceability=Column(Float)
    energy =Column(Float)
    loudness =Column(Float)
    speechiness =Column(Float)
    acousticness =Column(Float)
    instrumentalness =Column(Float)
    liveness =Column(Float)
    valence =Column(Float)
    tempo =Column(Float)

Session = sessionmaker(bind=engine)
session = Session()
Session2 = sessionmaker(bind=engine2)
session2 = Session2()

#uncomment to create new database (will overwrite existing)
# Base.metadata.create_all(engine)
