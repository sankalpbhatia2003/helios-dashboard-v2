#import uploadDescriptor
import os
#from createTask import taskId
import typer
import json
import time
import requests
from getResults import get_result
from dotenv import load_dotenv
from loadingBar import loading_bar
import streamlit as st
import pprint

load_dotenv()

def get_task(taskId, unique_speaker_names, df, emotion_classifier_df):
    #taskId = 'wrGKXh7KhsnDtNirBv3S'
    taskStatus = ""
    while (taskStatus != "COMPLETED"):

        print('')
        
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1, text=progress_text)
            
        loading_bar()
        #time.sleep(10)

        print('')
        print('')
        print("taskId: " + taskId)
        url = "https://mercury.api.helioslife.ventures/v1/tasks/" + str(taskId)

        payload = ""
        headers = {
        'x-api-key': os.getenv("X-API-KEY")
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code

        response = json.loads(response.text)

        #response = json.loads(response)
        #print(response)
        print(json.dumps(response, indent=4))
        #pprint.pprint(response)

        taskStatus = response["status"]

        descriptor_validation = response["audioConfigs"][0]["descriptor"]["uploadStatus"]
        audio_validation = response["audioConfigs"][0]["audio"]["uploadStatus"]

        print("DESCRIPTOR STATUS: " + descriptor_validation)
        print("AUDIO STATUS: " + audio_validation)

        resultId = response["analysisProducts"][0]["resultId"]

        print("Result ID: {}".format(resultId))

        print("GET Task Status Code: {}".format(status_code))

        if (audio_validation == "VALIDATION_FAILED"):
            typer.echo(typer.style("AUDIO FILE VALIDATION HAS FAILED", fg=typer.colors.RED, bg =typer.colors.WHITE, bold=True, blink = False))
            #print("AUDIO FILE VALIDATION HAS FAILED")
            quit()
        elif (descriptor_validation == "VALIDATION_FAILED"):
            typer.echo(typer.style("DESCRIPTOR FILE VALIDATION HAS FAILED", fg=typer.colors.RED, bg =typer.colors.WHITE, bold=True, blink = False))
            #print("DESCRIPTOR FILE VALIDATION HAS FAILED")
            quit()
        elif (taskStatus == "ANALYSIS_FAILED"):
            typer.echo(typer.style("ANALYSIS HAS FAILED. PLEASE TRY AGAIN LATER", fg=typer.colors.RED, bg =typer.colors.WHITE, bold=True, blink = False))
            #print("ANALYSIS HAS FAILED. PLEASE TRY AGAIN LATER")
            quit()
        else:
            continue
    get_result(resultId, unique_speaker_names, df, emotion_classifier_df)
