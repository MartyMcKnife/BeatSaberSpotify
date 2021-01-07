# Import Libs
import beatsaver as bs
import spotify as sp
import os
import re
from pathlib import Path
import json
import sys
import beatsage as ai
import idgrabber 
import multiprocessing as mp
import logger as l 
import youtube as y


class BeatSaberSpotify:
    def __init__(self, root_path, username, headsetType):
        self.total_songs = 0
        self.unzip = True
        customlevels = "Beat Saber_Data\\CustomLevels"
        playlist = 'Playlists'
        
        if headsetType == "sidequest":
            self.unzip = False
            customlevels = 'Songs'
            playlist = 'Playlist'

        self.download_directory = os.path.join(os.getcwd(), "downloads")
        self.custom_songs_directory = os.path.join(root_path, customlevels)
        self.custom_playlists_directory = os.path.join(root_path, playlist)

        self.invalid = '<>"|?*\/'
        if self.unzip == False:
            Path(self.custom_playlists_directory).mkdir(parents=True, exist_ok=True)
            Path(self.custom_songs_directory).mkdir(parents=True, exist_ok=True)

        Path(self.download_directory).mkdir(parents=True, exist_ok=True)

        self.logger = l.create_logger()


        self.logger.debug(f'Download Directory: {self.download_directory}'.encode('utf-8'))
        self.logger.debug(f'Custom Songs Directory: {self.custom_songs_directory}'.encode('utf-8'))
        self.logger.debug(f'Custom Playlists Directory: {self.custom_playlists_directory}'.encode('utf-8'))
        self.logger.debug(f'Unzip?: {self.unzip}')
        
        

        if not os.path.isdir(self.custom_songs_directory) and self.unzip == True:
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
        self.logger.info('Speaking to Spotify API')
        spotify = sp.SpotifyAPI()
        self.artist_file = spotify.write_playlist(username, playlist_id, self.download_directory)
        self.track_file = self.artist_file.replace("- Artists.txt", "- Tracks.txt")
        self.playlist_name = self.artist_file.replace(" - Artists.txt", "")
        image = spotify.get_playlist_image(playlist_id, self.download_directory, self.playlist_name)
        self.encoded_image = spotify.base64_encode(os.path.join(self.download_directory, image))
        self.jsonFile = os.path.join(self.custom_playlists_directory,
                                    "{0}.json".format(self.playlist_name))
        os.remove(image)
        self.logger.info(f'Playlist Name: {self.playlist_name}'.encode('utf-8'))

    def youtubeWriter(self, playlist_id):
        self.logger.info("Speaking to YouTube API")
        self.playlist_name, playlistResp = y.scrape_playlist(playlist_id, self.download_directory)
        self.track_file = self.playlist_name + "- Tracks.txt"
        self.artist_file = self.playlist_name + "- Artists.txt"
        image = y.getCoverImage(playlistResp, self.playlist_name, self.download_directory)
        self.encoded_image = y.base64_encode(os.path.join(self.download_directory, image))
        self.jsonFile = os.path.join(self.custom_playlists_directory,
                                    "{0}.json".format(self.playlist_name))
        os.remove(image)
        self.logger.info(f'Playlist Name: {self.playlist_name}'.encode('utf-8'))


    def downloadSong(self, songName, artistName, got_songs, songlist, locker):
        print('Grabbing {0} by {1}'.format(songName, artistName).encode('utf-8'), flush=True)
        self.logger.info('Grabbing {0} by {1}'.format(songName, artistName).encode('utf-8'))
        # downloader = bs.BeatSaver()
        songCover = os.path.join(self.download_directory, songName + ".png")
        self.logger.debug(f'Song Cover: {songCover}'.encode('utf-8'))
        #Disabled BeatSaver module as it currently is denying all requests made by this script
        # bsSongId, bsSongName, bsUsername = downloader.get_song_info(songName, artistName)
        # self.logger.debug(f'BeatSaver Song Info for {songName}: {bsSongId}, {bsSongName}, {bsUsername}'.encode('utf-8'))

        # if bsSongId != None:
        #     downloader.download_song_from_id(bsSongId, bsSongName, bsUsername, self.custom_songs_directory, self.unzip)
        # elif bsSongId == None:
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
        try:
            os.remove(songCover) 
        except (FileNotFoundError) as e:
            self.logger.warn(f'Song Cover could not be removed. Exception: {e}')
        if bsSongId != None:
            got_songs.value += 1
            print(u'Current' + str(got_songs.value), flush=True)
            for char in self.invalid:
                bsSongName = bsSongName.replace(char, '')
            hash = idgrabber.get_id(os.path.join(self.custom_songs_directory, "{0} ({1} - {2})".format(bsSongId, bsSongName, bsUsername)), self.unzip)
            with open(self.jsonFile, 'r') as f:songlist = json.load(f)
            print(f'Adding {bsSongName} to playlist file'.encode('utf-8'), flush=True)
            lock = locker.acquire()
            self.addToJson(songName=bsSongName, hash=hash, songlist=songlist)
            if lock:
                locker.release()
        else:
            return
            
    def addToJson(self, songlist = None, write=False, songName=None, hash=None, ):
        """
        Adds given track to Beatsaber Playlist
        """
        if write == True:
            with open(self.jsonFile, 'w+') as f:
                stuff = json.dumps(self.playlist_template, indent=4, sort_keys=True)
                f.write(stuff)
        elif write == False:
            with open(self.jsonFile, 'r+') as f:
                songlist['songs'].append(
                    {
                        'hash': hash
                    }
                )
                f.write(json.dumps(songlist, indent=4, sort_keys=True))
    
    def run(self, username, playlist_id):
        if "spotify" in playlist_id:
            
            self.SpotifyWriter(username, playlist_id)
        else:
            self.youtubeWriter(playlist_id)
        self.playlist_template['playlistTitle'] = self.playlist_name
        self.playlist_template['image'] = "data:image/png;base64," + self.encoded_image
        self.addToJson(write=True)
        manager = mp.Manager()
        got_songs = manager.Value('i', 0)
        songlist = manager.dict()
        locker = manager.Lock()



        with open(self.artist_file, 'r', encoding='utf-8') as a:
            with open(self.track_file, 'r', encoding='utf-8') as t:
                tracks = [line.rstrip() for line in t]
                artists = [line.rstrip() for line in a]
                self.total_songs = len(tracks)
                print('Total' + str(self.total_songs), flush=True)
                print('Collecting songs from BeatSaber and BeatSage. This can take a while, depending on the size of the playlist', flush=True)
                items = list(zip(tracks, artists))
                self.logger.debug(f'Items to download: {items}'.encode('utf-8'))
                for i, item in enumerate(items):
                    item = list(item)
                    item.extend((got_songs, songlist, locker))
                    items[i] = item
                
                with mp.Pool(processes=mp.cpu_count() - 1) as p:
                    p.starmap(self.downloadSong, items)
            
                print('Done!', flush=True)
                print('Got {0} of {1} songs'.format(got_songs.value, self.total_songs), flush=True)
        os.remove(self.artist_file)
        os.remove(self.track_file)
                


