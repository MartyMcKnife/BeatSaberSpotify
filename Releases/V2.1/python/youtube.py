import os
import sys
import pkg_resources
import logger as l
import subprocess
import base64


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
    import wget
except ImportError:
    install('requests')
    install("wget")
    import requests
    import wget

def scrape_playlist(youtubePlaylist, pathForCovers):
    invalid = '<>:"/\|?*'
    logger = l.create_logger()
    tracks = []
    artists = []
    nextPageToken = ""
    if "https://www.youtube.com/playlist?list=" in youtubePlaylist:
        youtubePlaylist = youtubePlaylist.replace("https://www.youtube.com/playlist?list=", "")
    apiKey = "AIzaSyD_yFlfIHjLlnok73b3iS8x6389ZFEr9AM"

    playlistName = requests.get(f"https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2C%20contentDetails&id={youtubePlaylist}&key={apiKey}")
    if playlistName.status_code == 200:

        title = playlistName.json()["items"][0]["snippet"]["title"]
        itemNumber = playlistName.json()["items"][0]["contentDetails"]["itemCount"]

        print(f"Writing {itemNumber} tracks to {title}.txt, and grabbing cover art".encode("utf-8"), flush=True)

        while True:
            
            contents = requests.get(f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={youtubePlaylist}&pageToken={nextPageToken}&key={apiKey}")

            items = contents.json()["items"]
            try:
                for video in items:
                    snippet = video["snippet"]
                    track = snippet["title"]
                    artist = snippet["channelTitle"]
                    for char in invalid:
                        track = track.replace(char, '')
                        artist = artist.replace(char, '')
                    tracks.append(track + "\n")
                    artists.append(artist + "\n")
                    coverUrl = snippet["thumbnails"]["standard"]['url']
                    try:
                        fullPath = os.path.join(pathForCovers, str(track) + ".png")
                        if not os.path.isfile(fullPath):
                            wget.download(coverUrl, fullPath)
                        else:
                            print(f"Skipping downloading of {track}'s cover - already downloaded".encode('utf-8'), flush=True)
                    except Exception as e:
                        print(f"Could not download {track}'s cover, {e} occured".encode('utf-8'), flush=True)
                        logger.warn(f"Could not download {track}'s cover, {e} occured")
            except (IndexError, KeyError) as e:
                print(f"Skipping {track} by {artist}, no thumbnail?".encode('utf-8'))
                logger.warning(f"{track} was skipped due to {e}")

            if "nextPageToken" in contents.json():
                nextPageToken = contents.json()["nextPageToken"]
            else:
                break

        with open(title + "- Tracks.txt", "w+", encoding="utf-8") as f:
            f.writelines(tracks)
            print("Wrote Tracks", flush=True)

        with open(title + "- Artists.txt", "w+", encoding="utf-8") as f:
            f.writelines(artists)
            print("Wrote Artists", flush=True)

        return title, playlistName
    else:
        raise SystemError(f"Youtube API responded with incorrect header {playlistName.status_code}")

def getCoverImage(playlistResp, playlistName, path):
    url = playlistResp.json()["items"][0]["snippet"]["thumbnails"]["standard"]["url"]
    path_full = os.path.join(path, playlistName + str(".png"))
    filename = wget.download(url, path_full)
    return filename



def base64_encode(path):
    with open(path, "rb") as f:
        encoded=base64.b64encode(f.read())
        return encoded.decode('utf-8')
