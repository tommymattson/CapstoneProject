'''
Thomas Mattson
Westmont College
CS-195 Senior Seminar
April 29, 2023
'''

import time
import requests
import json
import os
import pandas as pd


def appendDataToCSV(filename, channelName, jsonString):
    '''
    Appends the last prompts for each user to a CSV file.

    Args:
        filename (str): The name of the CSV file.
        channelName (str): The name of the channel.
        jsonString (list): The JSON response containing the prompts.

    '''
    # Create a DataFrame to store the last prompt for each user
    lastPrompts = []
    for value in jsonString:
        if value['author']['username'] == 'Midjourney Bot':
            try:
                user = value['mentions'][0]['id']
            except IndexError:
                continue
            unformattedPrompt = value['content']
            userPrompt = formatPrompt(unformattedPrompt)
            timeStamp = value['timestamp']
            # Append the current prompt to the DataFrame
            lastPrompts.append([channelName, user, userPrompt, timeStamp])

    # Append the last prompts to the CSV file using pandas
    df = pd.DataFrame(lastPrompts, columns=['Channel', 'User', 'Prompt', 'Timestamp'])
    df.to_csv(filename, mode='a', index=False, header=not os.path.isfile(filename))


def retrieve_messages(channelDictionary, headers):
    '''
    Retrieves messages from Discord channels and appends the prompts to a CSV file.

    Args:
        channelDictionary (dict): A dictionary mapping channel names to channel IDs.
        headers (dict): The headers to include in the HTTP request.

    '''
    for key, value in channelDictionary.items():
        r = requests.get(f'https://discord.com/api/v9/channels/{value}/messages', headers=headers)
        jsonString = json.loads(r.text)
        appendDataToCSV('SeniorProject\Project\Scraped Data\Multichannel Extract.csv', key, jsonString)
        time.sleep(1)


def formatPrompt(unformattedPrompt):
    '''
    Removes '**' at the beginning and end of prompt

    Args:
        unformattedPrompt (str): The unformatted prompt.

    Returns:
        str: The formatted prompt.

    '''
    delimiter = "**"
    start_marker = unformattedPrompt.find(delimiter) + 2
    end_marker = unformattedPrompt.find(delimiter, start_marker)
    formattedPrompt = unformattedPrompt[start_marker:end_marker]
    return formattedPrompt


def getMessages():
    '''
    Retrieves messages from multiple channels using different authorization tokens.

    '''
    # Retrieve authorization tokens from environment variables
    auth_TM1 = os.environ.get('midJourneyDiscordAPI_TM1')
    auth_TM2 = os.environ.get('midJourneyDiscordAPI_TM2')
    auth_TM3 = os.environ.get('midJourneyDiscordAPI_TM3')
    auth_LM  = os.environ.get('midJourneyDiscordAPI_LM')
    auth_EV  = os.environ.get('midJourneyDiscordAPI_EV')

    # Define authorizations dictionary with channel IDs for each token
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
