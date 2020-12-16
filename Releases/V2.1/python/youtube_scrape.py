import json
import subprocess
import pkg_resources
import sys
import logger as l

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from youtube_search import YoutubeSearch
    import requests
except ImportError:
    install("youtube-search")
    install('requests')
    import youtube_search
    import requests

logger = l.create_logger()
def scrape_songs_from_youtube(song,artist):
    results = YoutubeSearch("{0} - {1}".format(song, artist), max_results=1).to_json()
    try:
        logger.debug(f'Response back from Youtube is {results}')
        resultsDict = (json.loads(results))["videos"]
        url = resultsDict[0]["id"]
        contentResp = requests.get("https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id={0}&items%2FcontentDetails%2Fduration&key={1}".format(url, "AIzaSyD_yFlfIHjLlnok73b3iS8x6389ZFEr9AM"))
        logger.debug(f"Video information is {contentResp.json()}")
        
        if contentResp.status_code == 403: raise KeyError("Youtube API key is expired, please try again in 24 hours")
        allowedList = contentResp.json()['items'][0]['contentDetails']
        if len(resultsDict[0]["duration"]) < 5:
            if "regionRestriction" in allowedList:
                if "US" not in allowedList['regionRestriction']['allowed']:
                    print("Video is blocked in the US, so BeatSage can't acess it - Skipping", flush=True)
                    return None
            return "https://youtube.com/watch?v=" + url
        else:
            print("Video is longer than 10 minutes - Skipping", flush=True)
            return None
    except (KeyError, IndexError):
        print("Could not find video on YouTube - Skipping", flush=True)
        return None


