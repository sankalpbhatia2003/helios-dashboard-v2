import os
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import altair as alt
import pandas as pd
import numpy as np
import time
import os
from text_file import tonal_data_explanation, emotion_classifier
from youtubeToMP3 import youtube_to_mp3
from main_file import main_file_commands
import asyncio
import requests
import json

st.title("Tonal Sentiment Analysis")

st.subheader("What is Tonal Analysis?")
with st.expander("See Explanation"):
    st.write(tonal_data_explanation)

#st.write("You might have heard of text analysis? It is the process of analysing texts from a document. But texts can be highly deceivable. Simply a text isn't enough to understand what the speaker is trying to say. That is where Tonal Sentiment Analysis comes into the picture. Tonal Analysis is defined as using the speakers' various voice features such as loudness, pitch, frequency, etc., and quantifying them to retrieve insights which the speaker would exclusivley have. Tonal Analysis has a wide use case but we'll be focussing on how it can generate values that can give us an insight about what the company executives know about their company that others do not.")


#st.subheader("Analyzing the Audio from the YouTube Video")
#st.caption("The audio analyzed was released by CNBC after Robert Reffkin layed off his employs for the 3rd time")

with st.expander("ℹ️ Information about the Emotion Classifier"):
    st.info(emotion_classifier)

#emotion = 'Disgust'

 
#youtube_url = st.text_input("Drop the link of the YouTube video you'd like to analyze", None)
#youtube_code = (youtube_url[32:])
#st.video('https://youtu.be/{}'.format(youtube_code))

audio_file = st.file_uploader("Drop your MP3 file here", type=['MP3'], accept_multiple_files=False)

with st.spinner('Waiting for you to upload the MP3 file...'):
        time.sleep(10)
        st.success('Done!')

if audio_file is not None:
    # Save the MP3 file temporarily
    with open("temp.mp3", "wb") as f:
        f.write(audio_file.getbuffer())
    
    # Get the absolute path of the uploaded file
    audio_file_path = os.path.abspath("temp.mp3")
    st.write("File path:", audio_file_path)
    #main_file_commands(audio_file_path)
#elif (youtube_code is not None):
    #audio_file_path = youtube_to_mp3(youtube_code)
else:
    with st.spinner('Waiting for you to upload the MP3 file...'):
        time.sleep(10)
        st.success('Done!')
    st.write("Please upload your MP3 file")

#audio_file_path = mp3_bytes #os.fspath(audio_file)
#https://www.youtube.com/watch?v=72sz2zDQkqo
#st.audio(audio_file, format="audio/wav", start_time=0)

#def emotion_classifier_fn(audio_file_path): # Create an async functon

print('checkpoint 1')
API_URL = "https://api-inference.huggingface.co/models/harshit345/xlsr-wav2vec-speech-emotion-recognition"
print('checkpoint 2')
headers = {"Authorization": "Bearer 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"}
print('checkpoint 3')

#filename = "temp.mp3"
def query(filename):
    try:
        print('checkpoint 4')
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
    except Exception as e:
        print('checkpoint 4')
        print(e)
        pass

    try:
        return response.json()
    except Exception as e:
        print('Issue with Huggingface API')
        pass

time.sleep(20)
try:
    response = query("temp.mp3")
except:
    pass
# Parse the JSON response
# Convert dictionary to JSON string
#json_str = json.dumps(response)

# Create DataFrame from JSON string
print(response)
try:
    emotion_classifier_df = pd.DataFrame(response)
except Exception as e:
    emotion_classifier_df = pd.DataFrame(response, index=[0])
#emotion_classifier_df.index = range(len(emotion_classifier_df))

# Create a DataFrame from the JSON data
#emotion_classifier_df = pd.DataFrame(data)

#emotion_classifier_fn()
########################################################################
# Using Mercury API to send audio
main_file_commands(audio_file_path, emotion_classifier_df)

########################################################################
