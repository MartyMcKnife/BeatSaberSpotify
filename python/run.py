import sys
import beatsaverspotify as bs
import os
import multiprocessing as mp
import logging
import spotify
#TODO 
# Logging
# Add headset type to gui
# FIXME
# Formatting and Commenting

logging.basicConfig(filename='beatsaberspotify.log', level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] - %(module)s / %(funcName)s (%process)d - : %(message)s', datefmt='%d-%b-%y %H:%M:%S')

unzip = True

if len(sys.argv) > 1:
    root_path = sys.argv[1]
    logging.info("Path:" + str(root_path))
    uri = sys.argv[2]
    logging.info("URI:" + str(uri))
    username = sys.argv[3]
    logging.info("Username:" + str(username))
    client_id = sys.argv[4]
    spotify.client_id = client_id
    secret_id = sys.argv[5]
    spotify.client_secret = secret_id
    headsetType = sys.argv[6]
    logging.info("Headset:" + headsetType)
    if headsetType is 'Oculus Quest/Quest 2':
        headsetType = "sidequest"


if __name__ == '__main__':
    print('Starting up', flush=True)
    try:
        bs.BeatSaberSpotify(root_path, username, uri, headsetType).run(username, uri)
    except Exception as e:
        logging.error('Exception has occured', exc_info=True)
    
