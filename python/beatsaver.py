
import os
import zipfile
import io
import sys
import run
try:
    import requests
    from fuzzywuzzy import fuzz
except ImportError:
    run.install('requests')
    run.install('fuzzywuzzy')

# we are totally a web browser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_song_info(song_name):
    # get the url
    url = "https://beatsaver.com/api/search/text/page:?q=" + str(song_name)
    # say hi to beatsaver, and see if he has the song
    resp = requests.get(url, headers=headers)
    info = resp.json()
    # refine result
    content = info["docs"]
    # return the first key, hash and name
    try:

        songID = content[0]["key"]
        songHash = content[0]["hash"]
        songName = content[0]["name"]
        uploader = content[0]['uploader']
        username = uploader['username']
        if check_correct(songName, song_name, 65) == True:
            return songID, songHash, songName, username
        else:
            print("Song: {0} not found. Skipping".format(song_name.encode('utf-8')), flush=True)
    except KeyError:
        print("Song: {0} not found. Skipping".format(song_name.encode('utf-8')), flush=True)
    except IndexError:
        print("Song: {0} not found. Skipping".format(song_name.encode('utf-8')), flush=True)


def download_song_from_id(id,song_name,username,path):
    #  get the url
    url = 'https://beatsaver.com/api/download/key/' + str(id)
    resp = requests.get(url, headers=headers, stream=True)
    folder_path = os.path.join(path, '{0} {1} - {2}'.format(id, song_name, username))
    # stolen from stack overflow - gets the song download id, downloads, and copies it into a zip file with the correct name
    if not os.path.isdir(folder_path):
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        z.extractall(folder_path)
        print("Downloaded {0}".format(song_name), flush=True)
    else:
        print("Song: {0} already downloaded. Skipping".format(song_name.encode('utf-8')), flush=True)


def check_correct(returned_song_name, required_song_name, threshold):
    # use complicated maf to check the ratio of how accurate the song is
    check = fuzz.token_sort_ratio(returned_song_name, required_song_name)
    # if it is above the threshold, then we have found it. otherwise DENIED
    if check > threshold:
        return True
