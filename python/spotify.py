import base64
import os
import sys
import subprocess
import pkg_resources

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



# Generates Credentials
credentials = oauth2.SpotifyClientCredentials(
        client_id="0ae28390d808489dae0689e77389de23", client_secret="6d3cbce3d4b7426897c65301972509a9")
token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)
    



# Below is credit of ritiek - https://github.com/plamere/spotipy/issues/246#issuecomment-358546616
# Gets all songs and artists in playlist, and writes them to a text file
# Also gets all covers of the albums for Beat Sage, to make indexing easier
def write_tracks(text_file, tracks, pathForCovers):
    with open(text_file, 'w+', encoding='utf-8') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                
                try:
                    if "Tracks" in text_file:
                        track_url = track['name']
                        file_out.write(track_url + '\n')
                    # Write Artists to Text File
                    elif "Artists" in text_file:
                        artists = track['artists']
                        artistsName = artists[0]['name']
                        file_out.write(artistsName + '\n')
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']), flush=True)
                #Download Album Cover
                if pathForCovers != False:
                    images = track["album"]["images"]
                    url = images[0]["url"]
                    path_full = os.path.join(pathForCovers, track['name'] + str(".png"))
                    wget.download(url, path_full)

            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


def write_playlist(username, playlist_id, pathForCovers):
    results = spotify.user_playlist(username, playlist_id, fields='tracks,next,name')
    attributesToGet = ["Tracks", "Artists"]


    for item in attributesToGet:
        text_file = u'{0} - {1}.txt'.format(results['name'],item, ok='-_()[]{}')
        print(u'Writing {0} {1} to {2}'.format(
            results['tracks']['total'], item, text_file).encode("utf-8"), flush=True)
        tracks = results['tracks']
        if item == "Tracks":
            write_tracks(text_file, tracks, pathForCovers)
        else:
            write_tracks(text_file, tracks, False)
    return text_file
    



# Gets Playlist Image
def get_playlist_image(playlist_id,path,playlist_name):
    image = spotify.playlist_cover_image(playlist_id)
    url = image[0]["url"]
    path_full = os.path.join(path, playlist_name + str(".png"))
    filename = wget.download(url, path_full)
    return filename

#Beatsaber encodes all playlist images in base64. So we need to encode the spotify image
def base64_encode(path):
    with open(path, "rb") as f:
        encoded=base64.b64encode(f.read())
        return encoded.decode('utf-8')


