import time
import requests
import json
import csv
import os

def appendDataToCSV(filename, channelName, jsonString):
    # Create a dictionary to store the last prompt for each user
    lastPrompts = {}
    for value in jsonString:
        if (value['author']['username'] == 'Midjourney Bot'):
            try:
                user = value['mentions'][0]['id']
            except IndexError:
                continue
            unformattedPrompt = value['content']
            userPrompt = formatPrompt(unformattedPrompt)
            timeStamp = value['timestamp']
            # Update the dictionary with the current prompt for this user
            lastPrompts[user] = [channelName, user, userPrompt, timeStamp]

    # Append the last prompts to the CSV file
    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in lastPrompts.values():
            try:
                writer.writerow(row)
            except UnicodeEncodeError:
                continue

def retrieve_messages(channelDictionary, headers):
    for key, value in channelDictionary.items():
        r = requests.get(f'https://discord.com/api/v9/channels/{value}/messages', headers=headers)
        jsonString = json.loads(r.text)
        appendDataToCSV('SeniorProject\Project\Scraped Data\Multichannel Extract.csv', key, jsonString)
        time.sleep(1)

def formatPrompt(unformattedPrompt):
    delimiter = "**"
    start_marker = unformattedPrompt.find(delimiter) + 2
    end_marker = unformattedPrompt.find(delimiter, start_marker)
    formattedPrompt = unformattedPrompt[start_marker:end_marker]
    return formattedPrompt

def getMessages():
    auth_TM1 = os.environ.get('midJourneyDiscordAPI_TM1')
    auth_TM2 = os.environ.get('midJourneyDiscordAPI_TM2')
    auth_TM3 = os.environ.get('midJourneyDiscordAPI_TM3')
    auth_LM  = os.environ.get('midJourneyDiscordAPI_LM')
    auth_EV  = os.environ.get('midJourneyDiscordAPI_EV')

    authorizations = {
        auth_LM : {
            'newbies-113' : '1008571057562714113',
            'newbies-143' : '1008571132938555432',
            'newbies-173' : '1008571200508796978'   
        },
        auth_TM1 : {
            'newbies-3'   : '966491171142631444',
            'newbies-33'  : '989739661045940294',
            'newbies-63'  : '997267551082008616',
            'newbies-93'  : '997271845210439750'
        },
        auth_TM2 : {
            'newbies-17'  : '981697635591290970',
            'newbies-47'  : '990816855088328734',
            'newbies-77'  : '997270112400838766'
        },
        auth_TM3 : {
            'newbies-13'  : '981697547171151953',
            'newbies-43'  : '990816806581198869',
            'newbies-73'  : '997267906461192284'
        },
        auth_EV : {
            'newbies-26'  : '989268337886367754',
            'newbies-56'  : '997261049373929592',
            'newbies-86'  : '997271714792742922'
        }
    }
    
    for authorization_key, channelDictionary in authorizations.items():
        headers = {
        'authorization' : authorization_key
        }
        retrieve_messages(channelDictionary, headers)

getMessages()
