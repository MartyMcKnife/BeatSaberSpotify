import os
from zipfile import ZipFile
import io
import sys
import subprocess
import pkg_resources

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
    from fuzzywuzzy import fuzz
    import wget
except ImportError:
    install('requests')
    install('fuzzywuzzy')
    install('wget')
    import requests
    from fuzzywuzzy import fuzz
    import wget

got_songs = 0

class BeatSaver:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.invalid = '<>"|?*\/'
    def get_song_info(self, track):
        trackParsed = track.replace(" ", "%20")
        # get the url
        url = "https://beatsaver.com/api/search/text/page:?q=" + str(trackParsed)
        # say hi to beatsaver, and see if he has the song
        resp = requests.get(url, headers=self.headers)
        info = resp.json()
        # refine result
        
        # return the first key, hash and name
        try:
            content = info["docs"]
            for i in range(4):
                songID = content[i]["key"]
                songName = content[i]["name"]
                username = content[i]['uploader']['username']
                if self.check_correct(songName, track, 60) == True:
                    stats = content[i]["stats"]
                    upvotes = stats["upVotes"]
                    downvotes = stats["downVotes"]
                    if int(upvotes) > int(downvotes):
                        return songID, songName, username
                    else:
                        print("Song: {0} has low upvotes. Falling back to BeatSage".format(track), flush=True)
                print("Song: {0} not found. Falling back to BeatSage".format(track).encode('utf-8'), flush=True)
            return None, None, None
        except (KeyError, IndexError):
            print("Song: {0} does not exist. Falling back to BeatSage".format(track).encode('utf-8'), flush=True)
            return None, None, None


    def download_song_from_id(self, id,song_name,username,root_path, unzip):
        
        # get the url
        url = 'https://beatsaver.com/api/download/key/' + str(id)
        resp = requests.get(url, headers=self.headers, stream=True)
        for char in self.invalid:
            song_name = song_name.replace(char, '')

        folder_path = os.path.join(root_path, '{0} ({1} - {2})'.format(id, song_name, username))
        # stolen from stack overflow - gets the song download id, downloads, and copies it into a zip file with the correct name
        if not os.path.isdir(folder_path):
            if unzip == True:
                z = ZipFile(io.BytesIO(resp.content))
                z.extractall(folder_path)
            elif unzip == False:
                with open(folder_path + ".zip", 'wb') as f:
                    f.write(resp.content) 
            print("Downloaded {0}".format(song_name).encode('utf-8'), flush=True)
        else:
            print("Song: {0} already downloaded. Skipping".format(song_name).encode('utf-8'), flush=True)


    def check_correct(self,returned_song_name, required_song_name, threshold):
        # use complicated maf to check the ratio of how accurate the song is
        check = fuzz.token_sort_ratio(returned_song_name, required_song_name)
        # if it is above the threshold, then we have found it. otherwise DENIED
        if check > threshold:
            return True

