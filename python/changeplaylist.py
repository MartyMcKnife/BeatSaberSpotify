import idgrabber as i 
from fuzzywuzzy import process
import os
import logging



logging.basicConfig(filename='changeplaylist.log', encoding='utf-8', filemode='w', level= logging.INFO, format='[%(asctime)s] [%(levelname)s] - : %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def Update(pathToSongFolder, currentSongName, newSongName, zipped):
    """
    Gets the current hash for a song, and returns the new hash
    """
    try:
        folders = os.listdir(pathToSongFolder)
        logging.info(f'Current songs are {currentSongName}')
        logging.info(f'New songs are {currentSongName}')
        logging.info(f'Root Path is {pathToSongFolder}')
        logging.info(f'Folders availible are {folders}')

        for cSongName, nSongName in zip(currentSongName, newSongName):
            cSongNameF = process.extractOne(cSongName.lower(), folders)
            nSongNameF = process.extractOne(nSongName.lower(), folders)
            logging.info(f'Extracted cSongName is {cSongNameF}')
            logging.info(f'Extracted nSongName is {cSongNameF}')
            old_id = i.get_id(os.path.join(pathToSongFolder, cSongNameF[0]), zipped)
            new_id = i.get_id(os.path.join(pathToSongFolder, nSongNameF[0]), zipped)
            print('')
            print(f'Old ID for {cSongName} is {old_id} (this is the ID you need to find in the playlist.json)')
            print('')
            print(f'New ID for {cSongName} is {new_id} (this is the ID you replace the old id with)')
            print('' * 2)

        input('Press ENTER to exit')
    except Exception as e:
        print(e)
        print('An error has occured! Check the log for more details')
        logging.error('Exception has occured', exc_info=True)


"""
EDIT THE CODE BELOW HERE
"""
pathToSongFolder = 'Enter your path to your BeatSaber Custom Songs folder. If you are a quest user, there should be a directory called Songs'


currentSongName = [
    "A song that currently exists",
    "Another song that exists"
]

newSongName = [
    "The song that you want updated",
    "Cool Song"
]
# Set this to false if you are a quest user
folderArentZipped = True
"""
EDIT THE CODE Above HERE
"""

Update(pathToSongFolder, currentSongName, newSongName, folderArentZipped)