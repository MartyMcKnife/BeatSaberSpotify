import sys
import subprocess
import pkg_resources
import beatsaverspotify as bs
import logging


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("Opening Log File", flush=True)

sys.stdout = open('beatsaver.log', 'w+')
sys.stderr = sys.stdout

print("Installing Packages", flush=True)
print(help('modules'))
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

print("Installed Available Packages", flush=True)
print("Connecting to Spotify", flush=True)
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        root_path = sys.argv[0]
        uri = sys.argv[1]
        username = sys.argv[2]
        bs.beatsaver_spotify(root_path,uri,username)
    else:
        print("Incorrect Usage. Please enter variables alongside command", flush=True)