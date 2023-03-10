import pandas as pd
import os
from dotenv import load_dotenv
from uploadAudio import upload_audio
from uploadDescriptor import upload_descriptor
from getTask import get_task
#from createJSON import descriptorFileName
#from main_file import deepgramAnalysis, pathfile
import requests
import time
import json

load_dotenv()

def create_task(audioPathFile, descriptorFileName, API_request_title, unique_speaker_names, df, emotion_classifier_df):
  AudioFileName = os.path.abspath(audioPathFile) #str(input("Enter the name of your audio file: \n"))  #str(input("Enter the name of your audio file: \n"))
  fullDescriptorFilePath = os.path.abspath(descriptorFileName)
  title = API_request_title #str(input("Enter the title of your API request: \n"))

  url = "https://mercury.api.helioslife.ventures/v1/tasks"

  payload = json.dumps({
    "analysisProducts": [
      {
        "product": "TONAL_SENTIMENT_ATST",
        "version": "2.1.0"
      }
    ],
    "audioConfigs": [
      {
        "audio": {
          "fileName": AudioFileName,
          "fileType": "MP3",
          "type": "EARNINGS_CALL"
        },
        "descriptor": {
          "fileName": fullDescriptorFilePath,
          "fileType": "JSON",
          "type": "AUDIO_INDEX"
        }
      }
    ],
    "title": title,
    "tags": [
      {
        "name": "hello",
        "value": "world"
      }
    ]
  })
  headers = {
    'x-api-key': os.getenv("X-API-KEY"),
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  #print(response)

  #print(response.text)

  response = json.loads(response.text)

  audioURL = response["audioConfigs"][0]["audio"]["uploadUrl"]
  descriptorURL = response["audioConfigs"][0]["descriptor"]["uploadUrl"]

  #print("AUDIO URL")
  #print(audioURL)
  #print('')
  #print("DESCRIPTOR URL")
  #print(descriptorURL)

  upload_audio(AudioFileName, audioURL)
  upload_descriptor(fullDescriptorFilePath, descriptorURL)

  time.sleep(5)
  
  taskId = response["taskId"]
  print("Task ID: {}".format(taskId))
  get_task(taskId, unique_speaker_names, df, emotion_classifier_df)