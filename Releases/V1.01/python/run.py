import sys
import subprocess
import pkg_resources
import beatsaverspotify as bs
import os

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


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


        
if __name__ == "__main__":
    bs.beatsaver_spotify(root_path,uri,username)
else:
    print("Incorrect Usage. Please enter variables alongside command", flush=True)
