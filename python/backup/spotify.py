from dotenv import load_dotenv
load_dotenv()

import spotipy
import spotipy.oauth2 as oauth2
import re
import wget
import base64
import os

current_dir = os.curdir
client_id = os.getenv("SPOTIPY-CLIENT-ID")
secret_id = os.getenv("SPOTIPY-SECRET-ID")
print("Got Env Files. Setting them")
os.environ['SPOTIPY-CLIENT-ID'] = client_id
os.environ['SPOTIPY-SECRET-ID'] = secret_id

for filenames in os.listdir(current_dir):
    if filenames.endswith(".env"):
        os.remove(".env")
        print("Removed Environment File")

# Generates Credentials - Please do not copy these
try:
    credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id, client_secret=secret_id)
    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)
except Exception as e:
    print(e, flush=True)
    print("ERROR CONNECTING TO SPOTIFY. See above", flush=True)
    



# Below is credit of ritiek - https://github.com/plamere/spotipy/issues/246#issuecomment-358546616
def write_tracks(text_file, tracks):
    with open(text_file, 'w+', encoding='utf-8') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_url = track['name']
                    file_out.write(track_url + '\n')
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']), flush=True)
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


def write_playlist(username, playlist_id):
    results = spotify.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
    text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}'.format(
            results['tracks']['total'], text_file), flush=True)
    tracks = results['tracks']
    write_tracks(text_file, tracks)
    return text_file


def clean_up_file(file, text):
    with open(file, 'a', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            clean = re.sub("^https", "", line)
            file.write(clean + "/n")
            return clean


def get_playlist_image(playlist_id,path):
    image = spotify.playlist_cover_image(playlist_id)
    url = image[0]["url"]
    path_full = os.path.join(path, "cover.png")
    filename = wget.download(url, path_full)
    return filename


def base64_encode(path):
    with open(path, "rb") as f:
        encoded=base64.b64encode(f.read())
        return encoded.decode('utf-8')
