import hashlib
import os
import json
from zipfile import ZipFile


def get_id(songPath, unzip):
    if unzip:
        item = open(os.path.join(songPath, "Info.dat"), "r", encoding='utf-8', errors='ignore')
        mapList, thing_to_hash = getInfo(item)
        item.close()
        return sha1Object(mapList, songPath, thing_to_hash)
    else:
        songPath += ".zip"
        item = ZipFile(songPath, 'r')
        try: mapList, thing_to_hash = getInfo(item, Info="info.dat")
        except (FileNotFoundError, KeyError): mapList, thing_to_hash = getInfo(item, Info="Info.dat")
        item.close()
        return sha1Object(mapList, songPath, thing_to_hash)


        
def getInfo(item, Info = None):

    thing_to_hash = item.read(Info)

    jsonfile = json.loads(thing_to_hash)
    mapNameList = []
    
    for maps in jsonfile["_difficultyBeatmapSets"]:
    
        for beatmaps in maps["_difficultyBeatmaps"]:
            mapNameHolder = []
            for filename in beatmaps["_beatmapFilename"]:
                mapNameHolder.append(filename)
                mapName = "".join(mapNameHolder)
    
            mapNameList.append(mapName)
    return mapNameList, thing_to_hash

    

def sha1Object(mapList, songPath, thing_to_hash):
    
    if ".zip" not in songPath:
        for item in mapList:
            with open(os.path.join(songPath, item), "r") as e:
                thing_to_hash += e.read()
        hash_object = hashlib.sha1(thing_to_hash.encode('utf-8'))
        return hash_object.hexdigest()

    else:
        for item in mapList:
            with ZipFile(songPath, "r") as e:
                thing_to_hash += e.read(item)
        hash_object = hashlib.sha1(thing_to_hash)
        return hash_object.hexdigest()

    


