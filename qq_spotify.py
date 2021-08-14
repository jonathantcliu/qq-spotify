import os
import re
import requests
from bs4 import BeautifulSoup
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIPY_CLIENT_ID'], client_secret=os.environ['SPOTIPY_CLIENT_SECRET'], redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'], scope=scope))

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}

url_first = os.environ['URL_FIRST']
url_week = '&no='
url_third = '&openinqqmusic=1&type=0'
today = datetime.date.today()
year = today.year
week = today.isocalendar()[1]
url_week += '{}_{}'.format(year, week)

url = url_first + url_week + url_third
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.content, 'html5lib')

titles = soup.findAll('span', attrs={'class': 'song_list__txt'})
artists = soup.findAll('p', attrs={'class': 'song_list__desc'})

assert len(titles) == len(artists)

for i in range(len(titles)):
    titles[i] = titles[i].text
    artists[i] = artists[i].text.split('·')[0]

playlist_results = sp.user_playlist_tracks(os.environ['SPOTIPY_USER'], os.environ['SPOTIPY_PLAYLIST'])
tracks = playlist_results['items']
while playlist_results['next']:
    playlist_results = sp.next(playlist_results)
    tracks.extend(playlist_results['items'])

for i in range(len(tracks)):
    tracks[i] = tracks[i]['track']['id']

for i in range(len(titles)):
    print('Title: {}, Artist: {}'.format(titles[i], artists[i]))
    # could replace '/' with ',' to comply with Spotify's standards
    queries = [titles[i] + ' ' + artists[i]]
    stripped_title = re.sub("[\(\[].*?[\)\]]", "", titles[i])
    if '/' in artists:
        for artist in artists[i].split('/'):
            queries.append(titles[i] + ' ' + artist)
        for artist in artists[i].split('/'):
            queries.append(stripped_title + ' ' + artist)
    # last resort query
    queries.append(stripped_title)

    song = ""
    song_title = ""
    for query in queries:
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            song = results['tracks']['items'][0]['uri']
            song_title = results['tracks']['items'][0]['name']
            print("Spotify song title:", song_title)
            break
    if not song:
        print("{} not available".format(query))
        continue

    if song.split('track:')[1] in tracks:
        print("duplicate:", query)
    else:
        print("added song:", query)
        results = sp.user_playlist_add_tracks(os.environ['SPOTIPY_USER'], os.environ['SPOTIPY_PLAYLIST'], [song])
