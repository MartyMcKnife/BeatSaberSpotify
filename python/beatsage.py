from zipfile import ZipFile
import os
import json
import time
import base64
import subprocess
import pkg_resources
import sys
import shutil
import youtube_scrape as yt
import tempfile
import logger as l

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
except ImportError:
    install("requests")
    import requests

class BeatSage:
    def __init__(self,songTitle, songArtist, path):
        invalid = '<>:"/\|?*'
        for char in invalid:
            songTitle = songTitle.replace(char, '')
            songArtist = songArtist.replace(char, '')
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        self.createUrl = "https://beatsage.com/beatsaber_custom_level_create"
        self.heartBeatUrl = "https://beatsage.com/beatsaber_custom_level_heartbeat/"
        self.downloadUrl = "https://beatsage.com/beatsaber_custom_level_download/"
        self.folder_path = os.path.join(path, 'BeatSage ({0} - {1})'.format(songTitle, songArtist))
        self.zipPath = self.folder_path + ".zip"
        self.logger = l.create_logger()
        self.logger.debug(f'Folder Path: {self.folder_path}'.encode('utf-8'))
    def remove_from_zip(self, zipfname, *filenames):
            tempdir = tempfile.mkdtemp()
            try:
                tempname = os.path.join(tempdir, 'new.zip')
                with ZipFile(zipfname, 'r') as zipread:
                    with ZipFile(tempname, 'w') as zipwrite:
                        for item in zipread.infolist():
                            if item.filename not in filenames:
                                data = zipread.read(item.filename)
                                zipwrite.writestr(item, data)
                shutil.move(tempname, zipfname)
            finally:
                shutil.rmtree(tempdir)

        


    def request_song(self,songCover, songTitle, songArtist, path, unzip):
        if not os.path.isdir(self.folder_path):
            youtube = yt.youtubeSearch()
            youtubeUrl = youtube.scrape_songs_from_youtube(songTitle, songArtist)
            self.logger.debug(f'YoutubeUrl: {youtubeUrl}')

            if youtubeUrl != None:
                obj = {
                    "youtube_url": youtubeUrl,
                    "audio_metadata_title": songTitle,
                    "audio_metadata_artist": songArtist,
                    "difficulties": "Hard,Expert,ExpertPlus",
                    "modes":"Standard",
                    "events":"DotBlocks,Obstacles",
                    "system_tag":"v2"
                }


                idResponse = requests.post(self.createUrl, data=obj, headers=self.headers)

                id = json.loads(idResponse.text)['id']

                while(json.loads((requests.get(self.heartBeatUrl + id, self.headers)).text)['status'] == "PENDING"):
                    print("Waiting for BeatSage to create the level, job order is {0}".format(id), flush=True)
                    self.logger.info("Waiting for BeatSage to create the level, job order is {0}".format(id))
                    time.sleep(10)

                    
                print("Song has finished generating! Downloading now", flush=True)
                
                download = requests.get(self.downloadUrl + id, self.headers)

                if download.status_code == 200:
                    with open(self.zipPath, "wb+") as f:
                        self.logger.debug(f'Downloading song, status code is {download.status_code}')
                        f.write(download.content)

                    
                    if unzip == True:
                        with ZipFile(self.zipPath, "r") as z:
                            os.mkdir(self.folder_path)
                            z.extractall(self.folder_path)
                            shutil.copy(songCover, os.path.join(self.folder_path, "cover.jpg"))
                        os.remove(self.zipPath)
                    elif unzip == False:
                        self.remove_from_zip(self.zipPath, 'cover.jpg')
                        with ZipFile(self.zipPath, "a") as z:
                            z.write(songCover, arcname="cover.jpg")
                    print("Downloaded {0}!".format(songTitle), flush=True)
                    return 'done'
                else:
                    raise SystemError("BeatSage had an unexpected server error, or is down. Please try again later. Server Response Code: {0}".format(download.status_code))
            else:
                return None
        else:
            print('Song {0} is already generated. Skipping'.format(songTitle).encode('utf-8'), flush=True)
            self.logger.info('Song {0} is already generated. Skipping'.format(songTitle).encode('utf-8'))

            return 'done'



