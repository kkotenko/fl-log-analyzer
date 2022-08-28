#!/usr/bin/python3

import json
import os
import argparse

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
    newLevel = oldLevel

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
        
    # check if level changed at any point whatsoever
    if newLevel == 'UNKNOWN':
        print("Could not find any changes for that quality - did you spell it correctly?")

if __name__ == '__main__':
    scriptDescription = '''
    This script processes a recording of Fallen London API interactions. 
    Such a recording can be created by a program like FL Request Sounder 
    (https://github.com/lensvol/fl-request-sounder). 
    \n
    It also takes the name of a Fallen London character quality or World Quality
    and analyzes the log for changes of said quality.

    You can also get variant text that changes in the same response as
    the quality change occurred. 
    '''.strip()
    parser = argparse.ArgumentParser(description=scriptDescription)
    parser.add_argument('qualityName', 
                        help='Name of the quality you wish to track. ' \
                             'Use quotes around the name if it contains spaces or special characters.',
                        type=str, 
                        )
    parser.add_argument('log',
                        help='Relative path to the log file you want to analyze. ' \
                             'Use quotes around the file name if the path contains spaces or special characters.',
                        type=str,
                        )

    parser.add_argument('--no-response',
                        help='If set, will not print out changes in the response text (default: WILL print out changes). ' \
                            'Useful if you just want to see how a quality changes and are not interested in variant text.',
                        required=False,
                        action='store_false',
                        default=True
                        )
    parser.add_argument('--strip-spaces', '--strip', '--trim', '--trim-spaces',
                        help='If set, will strip spaces at the beginning and end of the title and description. ' \
                            'You will probably want to define a custom separator if you choose to do this. ' \
                            'Has no effect if `--no-response` is set. ',
                        required=False,
                        action='store_true',
                        default=False)

    parser.add_argument('--separator', '--sep',
                        help='Defines the string to be used as a seprator between individual entries of the response. ' \
                            'Default is a line break, followed by 7 dashes and another linebreak.' \
                            'Has no effect if `--no-response` is set. ',
                        default=os.linesep + '-' * 7 + os.linesep)

    args = parser.parse_args()
    watchQuality(args.qualityName, 
                load_fl_record(args.log),
                watchResponseText=args.no_response,
                stripSpaces=args.strip_spaces,
                separator=args.separator)
