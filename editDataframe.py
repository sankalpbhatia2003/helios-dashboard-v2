import pandas as pd
import json
from createJSON import create_json
import warnings
warnings.filterwarnings("ignore")

def edit_dataframe(data, audioPathFile, fileName, API_request_title, editJSON, unique_speaker_names, emotion_classifier_df):

    #print("ORIGINAL DF...")
    #print(data)

    i = 0
    while i < len(data['statement']):
        if ((data['stop'][i] > data['start'][i]) and ((data['stop'][i] - data['start'][i]) > 1)):
            pass
        else:
            data = data.drop(labels=i, axis=0)
        i += 1

    #print("EDITED DF...")
    #print(data)

    data = data.reset_index(inplace=False)

    i = 1
    while i < len(data['statement']):
        if (data['start'][i] < data['stop'][i-1]):
            data['start'][i] = data['stop'][i-1]
        else:
            pass
        i += 1

    #print('')

    data['type'][0:3] = "CALIBRATION"
    data['type'][3:len(data)] = "ANALYSIS"

    #print("PRINTING DATA FROM EDITED DATAFRAME FILE...")
    #print(data)

    create_json(data, audioPathFile, fileName, API_request_title, editJSON, unique_speaker_names, emotion_classifier_df)