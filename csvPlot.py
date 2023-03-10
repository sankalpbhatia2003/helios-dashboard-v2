import pandas as pd
import streamlit as st
from plotting import plotting_fn

def create_csv_plot(unique_speakers, mercury_results, df, emotion_classifier_df):

    speaker_to_analyze = st.selectbox("Choose the speaker you'd like to analyze:", set(unique_speakers))

    print(unique_speakers)
    print(df)
    print("Mercury Results: ",mercury_results)

    feature_value_list = []
    for feature_dataset in mercury_results['results']:
        feature_value = feature_dataset['features'][0]
        feature_value_list.append(feature_value)

    df['feature_values'] = feature_value_list

    print(df)

    # Pivot the DataFrame to create the desired format
    df_pivot = df.pivot(index='statement', columns='speaker', values='feature_values')
    #df_pivot.index.name = 'Sentence'
    #df_pivot.fillna('-', inplace=True)


    print(df_pivot)

    df_pivot.to_csv('trailCSVplot.csv')

    plotting_fn(speaker_to_analyze, emotion_classifier_df) # Using trailCSVplot.csv in the next file

