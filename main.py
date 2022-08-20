#!/usr/bin/python3

import json
import sys

def load_fl_record(filename: str):
    with open(filename) as f:
        jsonObject = json.load(f)
        f.close()
    return jsonObject

def watchQuality(quality: str, jsonObject, watchVariantText = True):
    for interaction in jsonObject:
        requestURL = interaction['url']
        if requestURL != "https://api.fallenlondon.com/api/storylet/choosebranch":
            continue
        response = interaction['response']
        messages = response['messages']
        for message in messages:
            if not 'possession' in message:
                continue
            modifiedQuality = message['possession']['name']
            if modifiedQuality == quality:
                newLevel = message['possession']['level']           
                print("%s changed to %s" % (modifiedQuality, newLevel))
                if watchVariantText:
                    title = str(response['endStorylet']['event']['name']).encode('utf-8')
                    description = str(response['endStorylet']['event']['description']).encode('utf-8')
                    print("Associated text:\n", title, description)
                    print("-------")
                    
    


if __name__ == '__main__':

    watchQuality("Second Airs For CourtRoom", load_fl_record("fallen-london-court-2022081523245.log"))



