import os
from zipfile import ZipFile
import io
import sys
import subprocess
import pkg_resources
import logger as l
from json.decoder import JSONDecodeError


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import requests
    from requests.auth import HTTPBasicAuth

    from fuzzywuzzy import fuzz
    import wget
except ImportError:
    install("requests")
    install("fuzzywuzzy")
    install("python-Levenshtein")
    install("wget")
    import requests
    from requests.auth import HTTPBasicAuth
    from fuzzywuzzy import fuzz
    import wget


class BeatSaver:
    def __init__(self):
        self.headers = {"user-agent": "BeatSaberSpotify"}
        self.invalid = '<>:"/\|?*'
        self.logger = l.create_logger()

    def get_song_info(self, track, artist):
        trackParsed = track.replace(" ", "%20")
        # get the url
        url = "https://beatsaver.com/api/search/text/page:?q=" + str(trackParsed)
        # say hi to beatsaver, and see if he has the song

        # refine result
        # return the first key, hash and name
        try:
            resp = requests.get(
                url, headers=self.headers, auth=HTTPBasicAuth("user", "pass")
            )
            info = resp.json()
            self.logger.info(f"Response back from BeatSaver is {info}".encode("utf-8"))
            content = info["docs"]

            songsInfo = []
            for i in range(4):
                songID = content[i]["key"]
                songName = content[i]["name"]
                username = content[i]["uploader"]["username"]
                correct = fuzz.partial_ratio(songName.lower(), track.lower())
                self.logger.info(
                    f"Certainty for {track}: {correct} (Returned song is {songName})".encode(
                        "utf-8"
                    )
                )

                if correct > 70:
                    songSubName = content[i]["metadata"]["songSubName"]
                    songAuthorName = content[i]["metadata"]["songAuthorName"]
                    self.logger.info(
                        f"SongSubName is {songSubName}, SongAuthorName is {songAuthorName}".encode(
                            "utf-8"
                        )
                    )
                    if (
                        artist.lower() in songSubName.lower()
                        or artist.lower() in songAuthorName.lower()
                    ):
                        stats = content[i]["stats"]
                        rating = stats["rating"]
                        if rating >= 0.7:
                            songsInfo.append(
                                {
                                    "rating": rating,
                                    "songID": songID,
                                    "songName": songName,
                                    "username": username,
                                }
                            )
                        else:
                            print(
                                "Song: {0} has low rating. Skipping".format(
                                    track
                                ).encode("utf-8"),
                                flush=True,
                            )
                    else:
                        print(
                            f"Song {songName}'s author on BeatSaver is not the same. Skipping".encode(
                                "utf-8"
                            ),
                            flush=True,
                        )
            if songsInfo:
                # Credit: https://stackoverflow.com/a/5326622
                song = max(songsInfo, key=lambda x: x["rating"])
                for char in self.invalid:
                    song["songName"] = song["songName"].replace(char, "")
                return song["songID"], song["songName"], song["username"]
            else:
                print(
                    "Song: {0} not found. Falling back to BeatSage".format(
                        track
                    ).encode("utf-8"),
                    flush=True,
                )
                return None, None, None

        except (KeyError, IndexError):
            print(
                "Song: {0} does not exist. Falling back to BeatSage".format(
                    track
                ).encode("utf-8"),
                flush=True,
            )
            self.logger.exception(f"Song: {track} exited with Exception:")
            return None, None, None

    def download_song_from_id(self, id, song_name, username, root_path, unzip):

        # get the url
        url = "https://beatsaver.com/api/download/key/" + str(id)
        resp = requests.get(url, headers=self.headers, stream=True)

        folder_path = os.path.join(
            root_path, "{0} ({1} - {2})".format(id, song_name, username)
        )

        self.logger.info(f"Folder path is {folder_path}".encode("utf-8"))
        # stolen from stack overflow - gets the song download id, downloads, and copies it into a zip file with the correct name
        if not os.path.isdir(folder_path) and not os.path.isfile(folder_path + ".zip"):
            if unzip == True:
                z = ZipFile(io.BytesIO(resp.content))
                z.extractall(folder_path)
            elif unzip == False:
                with open(folder_path + ".zip", "wb") as f:
                    f.write(resp.content)
            print("Downloaded {0}".format(song_name).encode("utf-8"), flush=True)
            self.logger.info("Downloaded {0}".format(song_name).encode("utf-8"))
        else:
            print(
                "Song: {0} already downloaded. Skipping".format(song_name).encode(
                    "utf-8"
                ),
                flush=True,
            )
            self.logger.info(
                "Song: {0} already downloaded. Skipping".format(song_name).encode(
                    "utf-8"
                )
            )
