
import requests
import pandas as pd

 # songs = pd.read_csv('lyrics.csv')

 # spotifyapi = config.spotify_api - update spotify api before running (expires)
spotifyapi = 'Bearer BQD8R8_7UchMhtXMmntAov_WGoRDufisnSEQ7YsOHG-F3g2hUOvnq_R2snqCSVe2UoshhlgghD6b00BLdU5WHbpBWRhlhLrZjCA-wmi-8PdPvHcZ5d9htNklxlXIJz-L0pipBs3k8FN5-3SHC_EM'

def get_spotify_track_id(artist, song):
     artist = artist.lower()
     artist = artist.replace(' ', '%20')
     song = song.lower()
     song = song.replace("'", "")
     song = song.replace(' ', '%20')
     url = f'https://api.spotify.com/v1/search?q=track:{song}%20artist:{artist}%20&type=track&limit=1'
     headers = {"Authorization": f'{spotifyapi}',
                 "Accept": "application/json", "Content-Type": "application/json"}

     req = requests.get(url, headers=headers)
     id = req.json()['tracks']['items'][0]['id']
     return id

def get_spotify_track_info(id):
     url = f'https://api.spotify.com/v1/audio-features/{id}'

     headers = {"Authorization": f'{spotifyapi}',
                 "Accept": "application/json", "Content-Type": "application/json"}
     req = requests.get(url, headers=headers)
     json = req.json()

     return(json)
