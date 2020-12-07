import json
import subprocess
import pkg_resources
import sys
import logger as l

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
except ImportError:
    install("requests")
    import requests

class youtubeSearch:
    def __init__(self):
        self.API_KEY = "AIzaSyD_yFlfIHjLlnok73b3iS8x6389ZFEr9AM"
        self.logger = l.create_logger()
    def scrape_songs_from_youtube(self, song, artist):
        print("Getting link from YouTube", flush=True)

        id, duration, allowed = self.YoutubeSearch("{0} - {1}".format(song, artist), 1)
        if id != None:
            if len(duration) >= 8:
                print("Song is longer than 10 Minutes. Skipping", flush=True)
                self.logger.debug(f'{song} skipped as it is longer than 10 mins ({duration})')
                return None
            elif allowed != True:
                print("Song is blocked in the US, so BeatSage cannot download it. Skipping", flush=True)
                self.logger.debug(f'{song} skipped as it is blocked in the us')
                return None
            else:
                self.logger.debug(f'Sending back {id}')
                return "https://www.youtube.com/watch?v=" + str(id)
        else:
            return id
        


    def YoutubeSearch(self, query, results):
        """
        Searches Youtube for given string
        """
        refinedQuery = query.replace(" ", "%20")
        try:
            allowed = True
            request = requests.get("https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={0}&fields=items%2Fid%2FvideoId&key={1}".format(refinedQuery, self.API_KEY))
            id = request.json()["items"][0]["id"]["videoId"]
            contentResp = requests.get("https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id={0}&items%2FcontentDetails%2Fduration&key={1}".format(id, self.API_KEY))
            duration = contentResp.json()["items"][0]["contentDetails"]["duration"]
            allowedList = contentResp.json()['items'][0]['contentDetails']
            if "regionRestriction" in allowedList:
                if "US" not in allowedList['regionRestriction']['allowed']:
                    allowed = False
            return id, duration, allowed
        except (KeyError, IndexError):
            print("Song cannot be found on YouTube. Skipping", flush=True)
            self.logger.debug(f'{query} skipped as it could not be found')
            return None, None, None
       
        