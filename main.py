import requests
from bs4 import BeautifulSoup
from pprint import pprint
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
billboard_url = 'https://www.billboard.com/charts/hot-100'
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri="https://example.com/", scope='playlist-modify-private', show_dialog=True, cache_path="token.txt", username='laedwards2'))
user_id = sp.current_user()["id"]

user_date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")
# user_date = '2002-08-27'
user_date_year = user_date[:4]

response = requests.get(url=f"{billboard_url}/{user_date}")

billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")

song_titles = soup.select(".o-chart-results-list__item #title-of-a-story")
song_titles_strings = [title.getText() for title in song_titles]
split_song_titles = [song_titles_strings[_].split('\n\n\t\n\t\n\t\t\n\t\t\t\t\t')[1].split('\t\t\n\t\n')[0] for _ in range(len(song_titles_strings))]
test = song_titles_strings[0].split('\n\n\t\n\t\n\t\t\n\t\t\t\t\t')[1].split('\t\t\n\t\n')

URI_spotify_list = [f'track:{title} year:{user_date_year}' for title in split_song_titles]

song_uris = []
for song in split_song_titles:
    result = sp.search(q=f'track:{song} year:{user_date_year}', type="track")
    try: 
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

new_playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False, collaborative=False, description=f"Top 100 Songs from {user_date}")


sp.playlist_add_items(new_playlist["id"], song_uris)










## Title
## c-title

## Name
## c-label

