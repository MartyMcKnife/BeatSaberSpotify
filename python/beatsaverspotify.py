# Import Libs
import beatsaver as bs
import spotify as sp
import os
import re
from pathlib import Path
import json
import sys
import beatsage as ai
import youtube_scrape as yt



# BEEEEEEG Function
def beatsaver_spotify(root_path, playlist_id, username):
    #Initialize Vars
    global total_songs
    global got_songs
    got_songs = 0
    total_songs = 0
    current_songs = 1
    custom_song_path = "Beat Saber_Data/CustomLevels"
    playlist_path = 'Playlists'

    #Set up all directory variables
    current_directory = os.getcwd()
    download_directory = os.path.join(current_directory, 'downloads')
    try:
        beatsaber_song_path = os.path.join(root_path, custom_song_path)
        beatsaber_playlist_path = os.path.join(root_path, playlist_path)
    except Exception as e:
        print(e)
        print("Could not find the playlist and Song directories for Beat Saber. Are sure you have the right path, and the plugins are installed?", flush=True)
        
    Path(download_directory).mkdir(parents=True, exist_ok=True)

    # Write the playlist, image and encode the image
    artist_file = sp.write_playlist(username, playlist_id, download_directory)
    tracks_file = artist_file.replace("- Artists.txt", "- Tracks.txt")
    playlist_name = re.sub("- Artists.txt$", "", artist_file)
    image = sp.get_playlist_image(playlist_id, download_directory, playlist_name)
    encoded_image = sp.base64_encode(os.path.join(download_directory, image))
    
    # Set up playlist dict/json file
    playlist = {
        "playlistTitle": playlist_name,
        "playlistAuthor": username,
        "playlistDescription": "Made with BeatSaberSpotify",
        "image": "data:image/jpg;base64," + str(encoded_image),
        "songs": [

        ]

        }

    #Open the file
    with open(artist_file, 'r', encoding='utf-8') as a:
        with open(tracks_file, 'r', encoding='utf-8') as t:
        #Get a list of all songs, and store it in variable. Also gets total number of songs
            tracks = [line.rstrip() for line in t]
            artists = [line.rstrip() for line in a]
            total_songs = len(tracks)
            print('Total' + str(total_songs), flush=True )
            print("Collecting Songs from BeatSaver and BeatSage. This can take a long time (depending on the size of the playlist)", flush=True)
            for track, artist in zip(tracks, artists):
                current_songs += 1
                
                try:
                    
                    #Get all the song info we need
                    songID, songHash, songName, username = bs.get_song_info(track)

                    # Add songs to the dict
                    keys = ['songName', 'hash']
                    names = [songName, songHash]
                    playlist["songs"].append(dict(zip(keys, names)))
                    #Download arr songs
                    got_songs += 1
                    bs.download_song_from_id(songID, songName, username, beatsaber_song_path)
                    #The library always throughs exceptions when something is missing, and then when you try and set variables to nothing it gets grmupy. So some silly error handling
                except TypeError:
                    print("", flush=True)

                    #Generate Song through BeatSage
                    link = yt.scrape_songs_from_youtube(track, artist)
                    if len(link) > 0:
                        got_songs += 1
                        if not os.path.isdir(os.path.join(beatsaber_song_path, "{0} - {1}".format(track, artist))):
                            mapId = ai.request_song(link, track + ".png", track, artist, beatsaber_song_path)
                        else:
                            print("Song: {0} already exists. Skipping generation".format(track).encode('utf-8'), flush=True)

                        keysAI = ['songName', "levelId"]
                        namesAI = [track, mapId]
                        playlist["songs"].append(dict(zip(keysAI, namesAI)))
                    else:
                        print("Song: {0} cannot be found on YouTube - Skipping".format(track).encode('utf-8'), flush=True)
                    

                print('Current' + str(current_songs), flush=True)
        # Write the dict to the json file
        with open(os.path.join(beatsaber_playlist_path, "{0}.json".format(playlist_name.rstrip())), 'w+') as f:
            print("Creating Playlist File", flush=True)
            stuff = json.dumps(playlist, indent=4, sort_keys=True)
            f.write(stuff)
            print('Done!', flush=True)
            print('Got {0} of {1} songs'.format(got_songs, total_songs), flush=True)



beatsaver_spotify("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Beat Saber", "spotify:playlist:47qyDl2OMGhIQ72AO2pHpT", "Sean")


