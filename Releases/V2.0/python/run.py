import sys
import beatsaberspotify as bs
import os
import multiprocessing as mp
import logging
import spotify
import subprocess
import logger as l

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == '__main__':
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
        if headsetType == 'Oculus Quest/Quest 2':
            headsetType = "sidequest"

    with open('beatsaberspotify.log', 'w+'): pass



    bss = bs.BeatSaberSpotify(root_path, username, headsetType)
    logger = l.create_logger()
    logger.info('\n' * 10)
    logger.info('Program started')

    

    print('Starting up', flush=True)
    try:
        bss.run(username, uri)
    except Exception as e:
        print('Error has occured! Check log for more details', flush=True)
        logger.error('Exception has occured', exc_info=True)
    
