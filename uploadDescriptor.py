import uploadAudio
#from createTask import descriptorURL
#from createJSON import descriptorFileName
from dotenv import load_dotenv
import requests
import os
import mimetypes
import json
import time

load_dotenv()

def upload_descriptor(descriptorFileName, descriptorURL):
  fullDescriptorFilePath = os.path.abspath(descriptorFileName)

  print("FULL DESCRIPTOR FILE PATH: {}".format(fullDescriptorFilePath))


  print("File type of audio uploaded is: " + str(mimetypes.guess_type(fullDescriptorFilePath)[0]))

  with open(fullDescriptorFilePath, 'rb') as f:
      payload = f.read()
      #print("File type of audio uploaded is: " + str(mimetypes.guess_type(payload)[0]))

  url = descriptorURL

  #payload = fullDescriptorFilePath # Comment this out

  headers = {
    'x-api-key': os.getenv("X-API-KEY"),
    'Content-Type': 'application/json'
  }

  response = requests.request("PUT", url, headers=headers, data=payload)

  print("Descriptor Upload Status Code: {}". format(response.status_code))