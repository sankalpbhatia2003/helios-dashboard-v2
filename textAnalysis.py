import requests
import os
import time
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

load_dotenv()

def text_analysis(transcript):
    
    API_URL = "https://api-inference.huggingface.co/models/nickmuchi/sec-bert-finetuned-finance-classification"
    headers = {"Authorization": "Bearer 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"} #{"Authorization": "Bearer {}".format(os.getenv("HUGGINGFACE-API-KEY"))}

    #while output['error'] == "Model nickmuchi/sec-bert-finetuned-finance-classification is currently loading":
    #progress_text = "Operation in progress. Please wait."
    
    #time.sleep(10)
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": transcript,
    })

    with st.spinner('Loading the analysis...'):
        time.sleep(20)
        st.success('Done!')
    #time.sleep(10)
    
    print(output)

    output = output[0]
    bearish_score = round(output[0]['score'], 4)
    neutral_score = round(output[1]['score'], 4)
    bullish_score = round(output[2]['score'], 4)

    # Define the CSS styles for each value
    #positive_style = "color:green;font-weight:bold"
    #negative_style = "color:red;font-weight:bold"
    #zero_style = "color:gray;font-weight:bold"

    #def delta_formatter(delta):
    #    return ""


    #col1, col2, col3 = st.columns(3)
    #col2.metric(label='Bearish', value=bearish_score, delta="", delta_color=negative_style)#, delta=round(data['Robert Reffkin'].mean(), 4) - 0)
    #col3.metric(label='Neutral', value=neutral_score, delta="", delta_color=zero_style)
    #col1.metric(label='Bullish', value=bullish_score, delta="", delta_color=positive_style)

    #output = output[0]
    #print(output)
    #output_df = pd.read_json(output, orient='columns')
    #st.dataframe(output_df)
    #print("Text Analysis: {}".format(output_df))

    #bearish_score = round(output[0][0][0]['score'], 6)
    #bullish_score = output[0][0][1]['score']
    #neutral_score = output[0][0][2]['score']

    #st.write(bearish_score)

    