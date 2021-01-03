import sys
import beatsaberspotify as bs
import os
import multiprocessing as mp
import logging
import spotify
import subprocess
import logger as l
import beatsage as b

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == '__main__':
    logger = l.create_logger()
    with open('beatsaberspotify.log', 'w+'): pass
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
        logger.info("Path:" + str(root_path))
        uri = sys.argv[2]
        logger.info("URI:" + str(uri))
        username = sys.argv[3]
        logger.info("Username:" + str(username))
        client_id = sys.argv[4]
        spotify.client_id = client_id
        secret_id = sys.argv[5]
        spotify.client_secret = secret_id
        headsetType = sys.argv[6]
        logger.info("Headset:" + headsetType)
        if headsetType == 'Oculus Quest/Quest 2':
            headsetType = "sidequest"
        version = sys.argv[7]
        b.version = version
        logger.info("Version:" + version)


    


    logger.info('\n' * 10)
    logger.info('Program started')
    bss = bs.BeatSaberSpotify(root_path, username, headsetType)
    

    

    print('Starting up', flush=True)
    try:
        bss.run(username, uri)
    except Exception as e:
        print('Error has occured! Check log for more details', flush=True)
        logger.error('Exception has occured', exc_info=True)
    
