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
import idgrabber 
import multiprocessing as mp

class BeatSaberSpotify:
    def __init__(self, root_path, username, playlist_id, headsetType):
        self.total_songs = 0
        self.download_directory = os.path.join(os.getcwd(), "downloads")
        Path(self.download_directory).mkdir(parents=True, exist_ok=True)
        if headsetType == "sidequest":
            root_path = os.getcwd()
            self.unzip = False
        self.unzip = True
        self.custom_songs_directory = os.path.join(root_path, "Beat Saber_Data\\CustomLevels")
        self.custom_playlists_directory = os.path.join(root_path, 'Playlists')

        if not os.path.isdir(self.custom_songs_directory):
            raise OSError('Could not find custom songs directory. Make sure you have the right path and try again')

        self.playlist_template = {
            "playlistTitle": "Placholder",
            "playlistAuthor": username,
            "playlistDescription": "Made with BeatSaberSpotify",
            "image": "Placeholder" ,
            "songs": [

            ]

        }
        
    def SpotifyWriter(self, username, playlist_id):
        """
        Fetches all required info from spotify
        """
        spotify = sp.SpotifyAPI()
        self.artist_file = spotify.write_playlist(username, playlist_id, self.download_directory)
        self.track_file = self.artist_file.replace("- Artists.txt", "- Tracks.txt")
        self.playlist_name = self.artist_file.replace(" - Artists.txt", "")
        image = spotify.get_playlist_image(playlist_id, self.download_directory, self.playlist_name)
        self.encoded_image = spotify.base64_encode(os.path.join(self.download_directory, image))
        os.remove(image)

    def downloadSong(self, songName, artistName):
        downloader = bs.BeatSaver()
        songCover = os.path.join(self.download_directory, songName + ".png")

        bsSongId, bsSongName, bsUsername = downloader.get_song_info(songName)

        if bsSongId != None:
            downloader.download_song_from_id(bsSongId, bsSongName, bsUsername, self.custom_songs_directory, self.unzip)
        elif bsSongId == None:
            downloaded = ai.BeatSage(songName, artistName, self.custom_songs_directory).request_song(
                songCover,
                songName,
                artistName,
                self.custom_songs_directory,
                self.unzip
            )
            if downloaded == None:
                bsSongId = None
            else:
                bsSongId = "BeatSage"
                bsSongName = songName
                bsUsername = artistName
        os.remove(songCover)
        if bsSongId != None:
            sp.got_songs += 1
            print(u'Current' + str(sp.got_songs))
            return idgrabber.get_id(os.path.join(self.custom_songs_directory, "{0} ({1} - {2})".format(bsSongId, bsSongName, bsUsername)))
        else:
            return ''
    def addToJson(self, jsonFile, write=False, songName=None, hash=None):
        """
        Adds given track to Beatsaber Playlist
        """
        if write == True:
            with open(jsonFile, 'w+') as f:
                stuff = json.dumps(self.playlist_template, indent=4, sort_keys=True)
                print(self.playlist_template)
                f.write(stuff)
        elif write == False:
            with open(jsonFile, 'r') as f:
                songlist = json.load(f)
                songlist['songs'].append(
                    {
                        'songName': songName,
                        'hash': hash
                    }
                )
                f.write(json.dumps(songlist, indent=4, sort_keys=True))


        

    
    def run(self, username, playlist_id):
        self.SpotifyWriter(username, playlist_id)
        self.playlist_template['playlistTitle'] = self.playlist_name
        self.playlist_template['image'] = "data:image/png;base64," + self.encoded_image
        self.addToJson(os.path.join(self.custom_playlists_directory,
                                    "{0}.json".format(self.playlist_name)), write=True)


        with open(self.artist_file, 'r', encoding='utf-16') as a:
            with open(self.track_file, 'r', encoding='utf-16') as t:
                tracks = [line.rstrip() for line in t]
                artists = [line.rstrip() for line in a]
                self.total_songs = len(tracks)
                print('Total' + str(self.total_songs), flush=True)
                print('Collecting songs from BeatSaber and BeatSage. This can take a while, depending on the size of the playlist', flush=True)
                items = list(zip(tracks, artists))
                with mp.Pool(processes=mp.cpu_count() - 1) as p:
                    ids = p.starmap(self.downloadSong, items)
                
                songDict = [
                    {'songName': songName,
                    'hash': hash} for songName, hash in zip(tracks, ids)
                ]
                
                self.playlist_template["songs"].append(songDict)
                print('Done!', flush=True)
                print('Got {0} of {1} songs'.format(sp.got_songs, self.total_songs), flush=True)
        os.remove(self.artist_file)
        os.remove(self.track_file)
                

path = os.path.join(os.getcwd(), 'test.json')

BeatSaberSpotify(os.getcwd(), 'Seen', '1234', 'notSidequest').addToJson(path, write=True)
BeatSaberSpotify(os.getcwd(), 'Seen', '1234', 'notSidequest').addToJson(
    path, songName='Beeg', hash='1234')
