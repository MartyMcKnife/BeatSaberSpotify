import sys
import beatsaverspotify as bs
import os
#TODO 
# Add to json after download
# Logging
# Add headset type to gui
# FIXME
# Current is mcbroken
# Formatting and Commenting
# output with multiprocessing is pretty shit


sidequestHeadsets = ['Quest', 'Quest 2']
unzip = True

if len(sys.argv) > 1:
    root_path = sys.argv[1]
    print("Path:" + str(root_path), flush=True)
    uri = sys.argv[2]
    print("URI:" + str(uri), flush=True)
    username = sys.argv[3]
    print("Username:" + str(username), flush=True)
    global client_id 
    client_id = sys.argv[4]
    global secret_id
    secret_id = sys.argv[5]
    headsetType = sys.argv[6]
    print("Headset:" + headsetType)
    if headsetType in sidequestHeadsets:
        headsetType = "sidequest"
    
root_path = os.getcwd()
username = 'Sean'
uri = 'spotify:playlist:76I3PWDYjNyJ0z8mAnMxEq'
headsetType = 'notsidequest'



if __name__ == '__main__':
    bs.BeatSaberSpotify(root_path, username, uri, headsetType).run(username, uri)
