#!/usr/bin/python3

import json
import os

def load_fl_record(filename: str):
    with open(filename) as f:
        jsonObject = json.load(f)
        f.close()
    return jsonObject

def watchQuality(watchedQuality: str, jsonObject, watchResponseText = True, stripSpaces = False, separator = "-------" + os.linesep):
    # set up some initial values to compare against
    oldTitle = None
    oldDescription = None
    oldLevel = 'UNKNOWN'

    for interaction in jsonObject:
        requestURL = interaction['url']
        # we are interested only in responses to these endpoints
        relevantEndpoints = ["https://api.fallenlondon.com/api/storylet/choosebranch"]

        if requestURL not in relevantEndpoints:
            continue
        # all requests to relevantEndpoints should receive a response field in the reply
        response = interaction['response']

        # messages are stored for responses to a '/choosebranch' request
        messages = response['messages'] if 'messages' in response else {}

        # look at quality changes
        for message in messages:
            if not 'possession' in message:
                continue
            modifiedQuality = message['possession']['name']
            if modifiedQuality == watchedQuality:
                newLevel = message['possession']['level']
                print("%s changed from %s to %s" % (modifiedQuality, oldLevel, newLevel))

                # cache old Level as base for next comparison
                oldLevel = newLevel

                # now we print out the impact of changes
                if watchResponseText:
                    # we assume these keys exist because a quality got modified
                    # that means we got a response to a '/choosebranch' request
                    # (this implication assumes that relevant qualities cannot be changed by Living Stories)
                    title: str = response['endStorylet']['event']['name']
                    description: str = response['endStorylet']['event']['description']
                    if stripSpaces:
                        title = title.strip()
                        description = description.strip()

                    print('Associated text:',
                          title if title != oldTitle or oldTitle == None else "[title unchanged]",
                          description if description != oldDescription or oldDescription == None else "[description unchanged]",
                          end=separator,
                          sep=os.linesep)

                    # cache title and description as base for next comparison
                    oldTitle = title
                    oldDescription = description


if __name__ == '__main__':

    watchQuality("Second Airs For CourtRoom", load_fl_record("fallen-london-court-2022081523245.log"))



