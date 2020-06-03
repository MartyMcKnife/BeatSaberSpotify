import sys
import subprocess
import pkg_resources
import beatsaverspotify as bs
import logging

log = logging.getLogger(__name__)
logging.basicConfig(filename="beatsaberspotify.log",level=logging.DEBUG)

required = {'spotipy', 'fuzzywuzzy', 'requests', 'zipfile', 'wget'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    try:
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    except Exception as e:
        print(e)
        print("ERROR: Could not get required packages",flush=True)
        
if __name__ == "__main__":
    bs.run()
