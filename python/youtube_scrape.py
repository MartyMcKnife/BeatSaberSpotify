import json
import subprocess
import pkg_resources
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from youtube_search import YoutubeSearch
except ImportError:
    install("youtube-search")
    import youtube_search



def scrape_songs_from_youtube(song,artist):
    print("Getting link from YouTube", flush="utf-8")
    results = YoutubeSearch("{0} - {1}".format(song, artist), max_results=1).to_json()
    try:
        resultsDict = (json.loads(results))["videos"]

        url = resultsDict[0]["id"]
        if len(resultsDict[0]["duration"]) < 5:
            return "https://youtube.com/watch?v=" + url
        else:
            print("Video is longer than 10 minutes - Skipping", flush=True)
            return ""
    except KeyError:
        print("Could not find video on YouTube - Skipping", flush=True)
        return ""
    





