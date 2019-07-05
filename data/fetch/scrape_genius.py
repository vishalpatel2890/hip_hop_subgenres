import requests
import re
import pandas as pd
import csv
import dateutil.parser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def get_artist_page(artist):
    '''
    Open artists page on Genius.com with Selenium

    Parameters
    ----------
    artist : string
        artist name

    Returns
    --------
    driver :  Selenium Driver Object
        Driver object with artists page open
    '''
    artist = artist.replace(" ", "-")
    artist = artist.replace(".", "")
    print(artist)
    try:
        driver = webdriver.Chrome()
        driver.get(f"http://www.genius.com/artists/{artist}")
        # driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        driver.find_element_by_xpath("/html/body/routable-page/ng-outlet/routable-profile-page/ng-outlet/routed-page/profile-page/div[3]/div[2]/artist-songs-and-albums/album-grid/div[2]").click()
    except NoSuchElementException as e:
        driver.close()
        print ('Artist not found', e)
        return
    except Exception as e:
        driver.close()
        return (e)

    return driver

def get_albums(driver):
        '''
        Scrape urls of artist's albums pages from Genius

        Parameters
        ----------
        driver :  Selenium Driver Object
            Driver object with artists page open

        Returns
        --------
        album_urls :  list
            list of album urls associated with artist
        '''
        try:
            selenium_html = driver.find_element_by_xpath('/html/body/div[5]/div[1]/ng-transclude/scrollable-data/div')
            html = selenium_html.get_attribute("innerHTML")
            soup = BeautifulSoup(html, features="html.parser")
            album_tags = soup.findAll('div', {'class':'mini_card-title'})
            album_url_tag = soup.findAll('a')
            album_list = [album.text for album in album_tags]
            album_urls =  [album['href'] for album in album_url_tag]
            driver.close()
        except Exception as e:
            driver.close()
            print('Error occured during scrape')
            return (e)
        if len(album_urls) > 0:
            return album_urls
        else:
            print('No Albums Scraped')
            return

def scrape_artists_albums(artist):
    '''
    Controller function to get all urls of artist's album pages

    Parameters
    ----------
    artist : string
        artists name

    Returns
    --------
    album_urls :  list
        list of album urls associated with artist
    '''
    album_urls = get_albums(get_artist_page(artist))
    return album_urls

def scrape_album_data(album_url):
    '''
    Scrape album name and release date

    Parameters
    ----------
    album_url : string
        genius album url

    Returns
    --------
    album_feat :  dict
        dictionary with keys 'album_name', 'release_date'
    '''
    try:
        req = requests.get(album_url)
        html = BeautifulSoup(req.content, 'html.parser')
        release_date = html.find('div', {'class': 'metadata_unit'})
        release_text = (release_date.text)[9:]
        release_date_obj = dateutil.parser.parse(release_text)
        album_name = html.find('h1', {'class': 'header_with_cover_art-primary_info-title header_with_cover_art-primary_info-title--white'}).text
        album_feat = {'album_name': album_name, 'release_date': release_date_obj}
    except Exception as e:
        print(f"Failed to get album data for {album_url}")
        return
    return album_feat

#function to scrape song names, artists featured on song, song url
def scrape_album_songs(artist, album_url):
    '''
    Scrape and clean all song lyrics for each album

    Parameters
    ----------
    artist : string
        artist name
    album_url : String
        genius album url

    Returns
    --------
    songs :  list
        list of dictionaries - each dictionary is one song with keys 'artist',
        'name', 'all_lyrics', 'artist_lyrics',
    '''
    try:
        #request, parse html
        req = requests.get(album_url)
        html = BeautifulSoup(req.content, 'html.parser')
        #find all song names
        song_names = html.findAll('h3', {'class': "chart_row-content-title"})
        #find all song urls (for scraping lyrics)
        song_urls = html.findAll('a', {'class': 'u-display_block'})
        #list of song urls
        song_urls = [song['href'] for song in song_urls]
        #list of song names from HTML - includes featured artists
        song_names = [song.text for song in song_names]
        #cleanup song text - separate title and artists featured on track - returns (song_name, list of features)
        song_names = [(clean_song_name(song)) for song in song_names]
        #zip together (song_name, features) with song_url
        lyrics = [scrape_lyrics(url, artist) for url in song_urls]
        songs = list(zip(song_names, lyrics))
    except Exception as e:
        print(f'failed to scrape album : {album_url}', e)
        return

    #final list of artist, song_name, features, song_url
    songs = [{'artist': artist, 'name': song[0], 'all_lyrics': song[1]['all_lyrics'], 'artist_lyrics': song[1]['artist_lyrics']} for song in songs]

    return songs

def clean_song_name(song):
    '''
    Clean up song name string

    Parameters
    ----------
    song : string
        song name as scrape from genius

    Returns
    --------
    song :  string
        song name without extraneous text
    '''
    features = None
    #clean new lines characters, Lyrics text, and Ft. text
    regex_first = re.compile('^(\n)( )*')
    regex_second = re.compile('(\n)( )*(Lyrics)(\n)*')
    regex_third = re.compile('(\(Ft.*)')

    #replace matching patterns from above with nothing
    song = re.sub(regex_first, '', song)
    song = re.sub(regex_second, '', song)
    song = re.sub(regex_third, '', song)
    #strip right whitespace
    song = song.rstrip()
    #search to find song containing (Ft. ...)
    feature_match = re.search(regex_third, song)

    return song

#function to scrape lyrics from song page
def scrape_lyrics(url, artist):
    '''
    Scrape and clean song lyrics for song. Also, separate artists lyrics from
    featured artists lyrics

    Parameters
    ----------
    url : string
        song url
    artist : String
        artist name

    Returns
    --------
    lyrics :  dict
        dictionary with cleaned lyrics with keys 'all_lyrics', 'artist_lyrics'
    '''
    #request lyric page url
    req = requests.get(url)
    html = BeautifulSoup(req.content, 'html.parser')
    #get lyrics
    all_text = html.find('div', {'class': 'lyrics'}).text
    #split lyrics on new line


    verses = [line + '\n' for line in all_text.split('\n') if line]
    #regex to find lines containing [] indicating unncessary information
    regex = re.compile('([\][])')
    #keep lines that do match regex and have len > 0
    all_verses = [verse for verse in verses if len(verse)>0 and not regex.search(verse)]
    artist_lyrics = just_artist_lyrics(verses, artist)
    #join lyrics into str
    all_verses_str = ' '.join(all_verses)
    lyrics = {'all_lyrics':all_verses_str, 'artist_lyrics': artist_lyrics}
    return lyrics

def just_artist_lyrics(lines, artist):
    '''
    Isolate artist lyrics from other lyrics

    Parameters
    ----------
    lines : list
        list of song lyrics, each element is a verse
    artist: string
        artist name


    Returns
    --------
    artist_lines_str :  string
        song lyrics sung by passed in artist
    '''
    #script to run to get just main artist lines
    artist_pattern = r"(\[)+(.*)" + re.escape(artist) + r"(.*)(\])+"
    #find index of attributions just to artist
    regex_artist = re.compile(artist_pattern, re.IGNORECASE)
    idx_art = []
    for idx, line in enumerate(lines):
        if regex_artist.search(line):
            idx_art.append(idx)

    if len(idx_art)>0:
        #find index of all lyrics attributions
        regex_all = re.compile('(\[)+(.*)(\])+')
        idx_all = []
        for idx, line in enumerate(lines):
            if regex_all.search(line):
                idx_all.append(idx)

        #get list of just artists lyrics
        artist_lines = []
        for idx, line in enumerate(idx_art):
            try:
                artist_lines.append(lines[line+1: idx_all[idx_all.index(line)+1]])
            except:
                artist_lines.append(lines[line+1:])

        artist_lines = [line for sublist in artist_lines for line in sublist]
        artist_lines_str = ' '.join(artist_lines)

    else:
        regex = re.compile('([\][])')
        artist_lyrics = [line  for line in lines if len(line)> 0 and not regex.search(line)]
        artist_lines_str = ' '.join(artist_lyrics)

    return artist_lines_str
