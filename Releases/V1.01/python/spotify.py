import re
import base64
import os
import sys
import run

try:
    import spotipy
    import spotipy.oauth2 as oauth2
    import wget
except ImportError:
    run.install('spotipy')
    import spotipy
    import spotipy.oauth2 as oauth2
    run.install('wget')





# Generates Credentials
credentials = oauth2.SpotifyClientCredentials(
        client_id=run.client_id, client_secret=run.secret_id)
token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)
    



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

# Unused function - Why do i still have this?
def clean_up_file(file, text):
    with open(file, 'a', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            clean = re.sub("^https", "", line)
            file.write(clean + "/n")
            return clean

# Fairly Obvious
def get_playlist_image(playlist_id,path,track_name):
    image = spotify.playlist_cover_image(playlist_id)
    url = image[0]["url"]
    path_full = os.path.join(path, track_name + str(".png"))
    filename = wget.download(url, path_full)
    return filename

#Beatsaber encodes all playlist images in base64. So we need to encode the spotify image
def base64_encode(path):
    with open(path, "rb") as f:
        encoded=base64.b64encode(f.read())
        return encoded.decode('utf-8')
