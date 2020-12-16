import base64
import os
import sys
import subprocess
import pkg_resources
import json


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import spotipy
    import spotipy.oauth2 as oauth2
    import wget
except ImportError:
    install('spotipy')
    import spotipy
    import spotipy.oauth2 as oauth2
    install('wget')
    import wget

client_id = "0ae28390d808489dae0689e77389de23"
client_secret = "6d3cbce3d4b7426897c65301972509a9"

class SpotifyAPI:
    def __init__(self):
        
        # Generates Credentials
        credentials = oauth2.SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret)
        token = credentials.get_access_token()
        self.spotify = spotipy.Spotify(auth=token)
        self.invalid = '<>:"/\|?*'

# Below is credit of ritiek - https://github.com/plamere/spotipy/issues/246#issuecomment-358546616
# Gets all songs and artists in playlist, and writes them to a text file
# Also gets all covers of the albums for Beat Sage, to make indexing easier
    def write_tracks(self, text_file, tracks, pathForCovers):
        with open(text_file, 'w+', encoding='utf-16') as file_out:
            i = 0
            while True:
                for item in tracks['items']:
                    i+=1
                    if 'track' in item:
                        track = item['track']
                    else:
                        track = item
                    
                    try:
                        if "Tracks" in text_file:
                            track_url = track['name']
                            for char in self.invalid:
                                track_url = track_url.replace(char, '')
                            file_out.write(track_url + '\n')
                        # Write Artists to Text File
                        elif "Artists" in text_file:
                            artists = track['artists']
                            artistsName = artists[0]['name']
                            for char in self.invalid:
                                artistsName = artistsName.replace(char, '')
                            file_out.write(artistsName + '\n')
                        #Download Album Cover
                        if pathForCovers != False:
                            if i == 1:
                                print('Downloading Album covers', flush=True)
                            images = track["album"]["images"]
                            url = images[0]["url"]
                            filename = track["name"]

                            for char in self.invalid:
                                filename = filename.replace(char, '')
                            path_full = os.path.join(pathForCovers, filename + str(".png"))
                            if not os.path.isfile(path_full):
                                wget.download(url, path_full)
                    except (KeyError, IndexError):
                        print(u'Skipping track {0} by {1} (local only?)'.format(
                                track['name'], track['artists'][0]['name']), flush=True)
                    

                # 1 page = 50 results
                # check if there are more pages
                if tracks['next']:
                    tracks = self.spotify.next(tracks)
                else:
                    break


    def write_playlist(self, username, playlist_id, pathForCovers):
        results = self.spotify.user_playlist(username, playlist_id, fields='tracks,next,name')
        attributesToGet = ["Tracks", "Artists"]

        for item in attributesToGet:
            text_file = u'{0} - {1}.txt'.format(results['name'],item, ok='-_()[]{}')
            print(u'Writing {0} {1} to {2}'.format(
                results['tracks']['total'], item, text_file).encode("utf-8"), flush=True)
            tracks = results['tracks']
            if item == "Tracks":
                self.write_tracks(text_file, tracks, pathForCovers)
            else:
                self.write_tracks(text_file, tracks, False)
        return text_file
        



    # Gets Playlist Image
    def get_playlist_image(self, playlist_id,path,playlist_name):
        image = self.spotify.playlist_cover_image(playlist_id)
        url = image[0]["url"]
        path_full = os.path.join(path, playlist_name + str(".png"))
        filename = wget.download(url, path_full)
        return filename

    #Beatsaber encodes all playlist images in base64. So we need to encode the spotify image
    def base64_encode(self, path):
        with open(path, "rb") as f:
            encoded=base64.b64encode(f.read())
            return encoded.decode('utf-8')

