from zipfile import ZipFile
import os
import json
import time
import base64
import subprocess
import pkg_resources
import sys
import idgrabber

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import requests
except ImportError:
    install("requests")
    import requests


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}


def request_song(youtubeUrl, songCover, songTitle, songArtist, path):
    createUrl = "https://beatsage.com/beatsaber_custom_level_create"
    heartBeatUrl = "https://beatsage.com/beatsaber_custom_level_heartbeat/"
    downloadUrl = "https://beatsage.com/beatsaber_custom_level_download/"



    obj = {
        "youtube_url": youtubeUrl,
        "cover_art": songCover,
        "audio_metadata_title": songTitle,
        "audio_metadata_artist": songArtist,
        "difficulties": "Hard,Expert,ExpertPlus",
        "modes":"Standard",
        "events":"DotBlocks,Obstacles",
        "system_tag":"v2-flow"
    }

    idResponse = requests.post(createUrl, obj, headers)

    id = json.loads(idResponse.text)['id']



    while(json.loads((requests.get(heartBeatUrl + id, headers)).text)['status'] == "PENDING"):
        print("Waiting for BeatSage to create the level, job order is {0}".format(id), flush=True)
        time.sleep(10)

        
    print("Song has finished generating! Downloading now", flush=True)
    
    download = requests.get(downloadUrl + id, headers)

    folder_path = os.path.join(path, 'BeatSage ({0} - {1})'.format(songTitle, songArtist))

    with open(folder_path +".zip", "wb") as f:
        f.write(download.content)

    with ZipFile(folder_path +".zip", "r") as z:
        z.extractall(folder_path)

    os.remove(folder_path + '.zip')

    mapId = idgrabber.get_id(folder_path)

    return mapId


