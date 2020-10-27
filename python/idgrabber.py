import hashlib
import os
import json


def get_id(pathToFolder):

    with open(os.path.join(pathToFolder, "Info.dat"), "r", encoding="utf-8") as i:
        thing_to_hash = i.read()

        jsonfile = json.loads(thing_to_hash)
        mapNameList = []
        
        for maps in jsonfile["_difficultyBeatmapSets"]:
        
            for beatmaps in maps["_difficultyBeatmaps"]:
                mapNameHolder = []
                for filename in beatmaps["_beatmapFilename"]:
                    mapNameHolder.append(filename)
                    mapName = "".join(mapNameHolder)
        
                mapNameList.append(mapName)

        

        for item in mapNameList:
            with open(os.path.join(pathToFolder, item), "r") as e:
                thing_to_hash += e.read()
            


        hash_object = hashlib.sha1(thing_to_hash.encode("utf-8"))
        return hash_object.hexdigest()

        


            