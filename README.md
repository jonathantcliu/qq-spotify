# qq-spotify
Scraper that updates a Spotify playlist with QQ Music's most played songs  
1. Register your app at [My Applications](https://developer.spotify.com/my-applications/#!/applications)
2. Create a .env file that contains:  
SPOTIPY_CLIENT_ID = CLIENT ID from [Dashboard](https://developer.spotify.com/dashboard/applications)  
SPOTIPY_CLIENT_SECRET = CLIENT SECRET from [Dashboard](https://developer.spotify.com/dashboard/applications)  
SPOTIPY_REDIRECT_URI = [Redirect URI](https://spotipy.readthedocs.io/en/2.19.0/#redirect-uri)  
SPOTIPY_USER = Spotify ID of the owner of the playlist you would like to edit  
SPOTIPY_PLAYLIST = Spotify ID of the playlist you would like to edit  
URL_FIRST = Link created by sharing 热歌 from 排行榜 on the QQ Music app before '&no='
3. Run qq_spotify.py!
