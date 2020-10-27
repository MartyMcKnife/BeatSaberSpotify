import hashlib, os
import json
cwd = os.getcwd()
rootPath = "downloads\ITMSC (We Both Reached for the Gun - Marcia Lewis)"


with open(os.path.join(rootPath, "Info.dat"), "r", encoding="utf-8") as i:
    thing_to_hash = i.read()

    json = json.loads(thing_to_hash)
    mapNameList = []
    count = 0
    for maps in json["_difficultyBeatmapSets"]:
        count += 1
        for beatmaps in maps["_difficultyBeatmaps"]:
            mapNameHolder = []
            for filename in beatmaps["_beatmapFilename"]:
                mapNameHolder.append(filename)
                mapName = "".join(mapNameHolder)
        
            mapNameList.append(mapName)

    print(mapNameList)

    mapContents = []
    for item in mapNameList:
        with open(os.path.join(rootPath, item), "r") as e:
            thing_to_hash += e.read()
            

    #print(thing_to_hash)
    hash_object = hashlib.sha1(thing_to_hash.encode("utf-8"))
    print(hash_object.hexdigest())

        


            