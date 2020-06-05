import beatsaver as bs
import spotify as sp
import os
import re
from pathlib import Path
import json
import sys




def beatsaver_spotify(root_path, playlist_id, username):
    global total_songs
    global got_songs
    custom_song_path = "CustomLevels"
    playlist_path = 'Playlists'

    current_directory = os.getcwd()
    download_directory = os.path.join(current_directory, 'downloads')
    try:
        beatsaber_song_path = os.path.join(root_path, custom_song_path)
        beatsaber_playlist_path = os.path.join(root_path, playlist_path)
    except Exception as e:
        print(e)
        print("Could not find the playlist and Song directories for Beat Saber. Are sure you have the right path, and the plugins are installed?", flush=True)
        
    Path(download_directory).mkdir(parents=True, exist_ok=True)

    # write playlist - TBA
    file_name = sp.write_playlist(username, playlist_id)
    image = sp.get_playlist_image(playlist_id, download_directory)
    playlist_name = re.sub(".txt$", "", file_name)
    encoded_image = sp.base64_encode(os.path.join(download_directory, image))

    playlist = {
        "playlistTitle": playlist_name,
        "playlistAuthor": username,
        "playlistDescription": "Made with BeatSaberSpotify",
        "image": "data:image/jpg;base64," + str(encoded_image),
        "songs": [

        ]

        }

    with open(file_name, 'r') as f:
        lines = [line.rstrip() for line in f]
        total_songs = lines
        print('Total' + str(total_songs), flush=True )
        print("Writing to JSON file. This can take a long time (depending on the size of the playlist)", flush=True)
        for line in lines:
            try:
                got_songs += 1
                print('Current' + str(got_songs), flush=True)
                songID, songHash, songName, username = bs.get_song_info(line)
                # Add songs to the dict
                keys = ['songName', 'hash']
                names = [songName, songHash]
                playlist["songs"].append(dict(zip(keys, names)))
                bs.download_song_from_id(songID, songName, username, beatsaber_song_path)
            except TypeError:
                print("", flush=True)

    with open(os.path.join(beatsaber_playlist_path, "{0}.json".format(playlist_name)), 'w+') as f:
        stuff = json.dumps(playlist, indent=4, sort_keys=True)
        f.write(stuff)
        print('Done!', flush=True)
        print('Got {0} of {1} songs'.format(got_songs, total_songs), flush=True)




