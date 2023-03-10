import json
#from getTask import resultId
import os
from dotenv import load_dotenv
import requests
import streamlit as st
from csvPlot import create_csv_plot

load_dotenv()

def get_result(resultId, unique_speaker_names, df, emotion_classifier_df):
    url = "https://mercury.api.helioslife.ventures/v1/results/" + str(resultId)

    payload={}
    headers = {
    'x-api-key': os.getenv("X-API-KEY")
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print('')
    print('')
    print('YOUR RESULTS...')
    print('--------------------------------')
    json_data = json.loads(response.text)
    json_string = json.dumps(json_data, indent=4)
    print(json_string)
    print('--------------------------------')

    st.download_button(
        label="Download Helios Tonal data as JSON?",
        data=json_string,
        file_name='heliosAnalysis.json',
        mime='application/csv')

    create_csv_plot(unique_speaker_names, json_data, df, emotion_classifier_df)