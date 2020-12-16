import os
from zipfile import ZipFile
import io
import sys
import subprocess
import pkg_resources
import logging
import logger as l
from json.decoder import JSONDecodeError

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
    from fuzzywuzzy import fuzz
    import wget
except ImportError:
    install('requests')
    install('fuzzywuzzy')
    install('python-Levenshtein')
    install('wget')
    import requests
    from fuzzywuzzy import fuzz
    import wget


class BeatSaver:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36'}
        self.invalid = '<>"|?*\/'
        self.logger = l.create_logger()
    def get_song_info(self, track, artist):
        trackParsed = track.replace(" ", "%20")
        # get the url
        url = "https://beatsaver.com/api/search/text/page:?q=" + str(trackParsed)
        # say hi to beatsaver, and see if he has the song
        
        # refine result
        
        # return the first key, hash and name
        try:
            resp = requests.get(url, headers=self.headers, auth=('user', 'pass'))
            info = resp.json()
            self.logger.debug(f'Response back from BeatSaver is {info}'.encode('utf-8'))
            content = info["docs"]
            for i in range(4):
                songID = content[i]["key"]
                songName = content[i]["name"]
                username = content[i]['uploader']['username']
                correct = fuzz.partial_ratio(songName.lower(), track.lower())
                self.logger.debug(f'Certainty for {track}: {correct} (Returned song is {songName})'.encode('utf-8'))
                
                if correct > 70:
                    songSubName = content[i]["metadata"]['songSubName']
                    songAuthorName = content[i]["metadata"]['songAuthorName']
                    self.logger.debug(f'SongSubName is {songSubName}, SongAuthorName is {songAuthorName}')
                    if songSubName.lower() == artist.lower() or songAuthorName.lower() == artist.lower():
                        stats = content[i]["stats"]
                        rating = stats['rating']
                        if rating >= 0.7:
                            return songID, songName, username
                        else:
                            print("Song: {0} has low rating. Skipping".format(track), flush=True)
                    else:
                        print(f"Song {songName}'s author on BeatSaver is not the same. Skipping", flush=True)
                
            print("Song: {0} not found. Falling back to BeatSage".format(track).encode('utf-8'), flush=True)
            return None, None, None
        except (KeyError, IndexError):
            print("Song: {0} does not exist. Falling back to BeatSage".format(track).encode('utf-8'), flush=True)
            logging.exception(f'Song: {track} exited with Exception:')
            return None, None, None


    def download_song_from_id(self, id,song_name,username,root_path, unzip):
        
        # get the url
        url = 'https://beatsaver.com/api/download/key/' + str(id)
        resp = requests.get(url, headers=self.headers, stream=True)
        for char in self.invalid:
            song_name = song_name.replace(char, '')

        folder_path = os.path.join(root_path, '{0} ({1} - {2})'.format(id, song_name, username))
        self.logger.debug(f'Folder path is {folder_path}'.encode('utf-8'))
        # stolen from stack overflow - gets the song download id, downloads, and copies it into a zip file with the correct name
        if not os.path.isdir(folder_path) and not os.path.isfile(folder_path + ".zip"):
            if unzip == True:
                z = ZipFile(io.BytesIO(resp.content))
                z.extractall(folder_path)
            elif unzip == False:
                with open(folder_path + ".zip", 'wb') as f:
                    f.write(resp.content) 
            print("Downloaded {0}".format(song_name).encode('utf-8'), flush=True)
            self.logger.info("Downloaded {0}".format(song_name).encode('utf-8'))
        else:
            print("Song: {0} already downloaded. Skipping".format(song_name).encode('utf-8'), flush=True)
            self.logger.info("Song: {0} already downloaded. Skipping".format(song_name).encode('utf-8'))




print(BeatSaver().get_song_info('Tank!', 'SEATBELTS'))