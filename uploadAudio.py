#from createTask import audioURL
#from main_file import pathfile
import requests
import os
from dotenv import load_dotenv
#from pydub import AudioSegment
#import io

load_dotenv()

def upload_audio(pathFile, audioURL):
  #print("Pathfile: " + pathFile)
  print(pathFile)
  url = audioURL

  #payload= pathFile

  with open(pathFile, 'rb') as f:
      payload = f.read()

  headers = {
    'x-api-key': os.getenv("X-API-KEY"),
    'Content-Type': 'audio/mpeg'
  }

  response = requests.request("PUT", url, headers=headers, data=payload)

  print("Audio Upload Status Code: {}". format(response.status_code))