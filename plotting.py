import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap

# Plotting area chart
def plotting_fn(speaker_to_analyze, emotion_classifier_df):
    #data = pd.read_csv(os.path.abspath(dataframe))
    data = pd.read_csv('trailCSVplot.csv')
    #later_data = data = dataframe
    later_data = data
    data = data.reset_index(drop=True)
    data = data.set_index("statement")

    print(data)

    # Define options for dropdown menu
    options = ['Sentence with highest conviction about future POSTIVE performance', 'Sentence with conviction about future NEGATIVE performance']

    # Create dropdown menu and get user's selection
    option = st.selectbox('Select an option', options)

    # Find sentence with highest tonal score
    if option == options[0]:
        max_sentence = later_data.loc[later_data[speaker_to_analyze].idxmax(), 'statement']
        st.subheader(f' **_:green["{max_sentence}"]_** ')
    # Find sentence with lowest tonal score
    elif option == options[1]:
        min_sentence = later_data.loc[later_data[speaker_to_analyze].idxmin(), 'statement']
        st.subheader(f' **_:red["{min_sentence}"]_** ')

    # Show default message if no option is selected
    else:
        st.write("Please select an option")

    ################################################################
    #st.subheader("Overall Audio Emotion: _:orange[{}]_ {}".format('disgust', '🤨'))
    st.subheader("Overall Audio Emotion")
    st.dataframe(emotion_classifier_df)
    ################################################################
    #data = data.fillna(0)

    col1, col2, col3 = st.columns(3)
    col2.metric(label="Average Tonal Sentiment Score", value=round(data[speaker_to_analyze].mean(), 4))#, delta=round(data['Robert Reffkin'].mean(), 4) - 0)
    col3.metric("Maximum Tonal Score", value=round(data[speaker_to_analyze].max(), 4), delta = round(data[speaker_to_analyze].max() - data[speaker_to_analyze].mean(), 4))
    col1.metric("Minimum Tonal Score", value=round(data[speaker_to_analyze].min(), 4), delta = round(data[speaker_to_analyze].min() - data[speaker_to_analyze].mean(), 4))

    st.subheader("{}'s value on our Tonal Sentiment Scale".format(speaker_to_analyze))
    ################################################################
    # Define the color gradient
    cmap = LinearSegmentedColormap.from_list('RedBlue', ['#FF0000', '#0000FF'])

    # Define the x-axis values
    x = np.linspace(-5, 5, num=100)

    # Set the value to indicate with a vertical line
    val = round(data[speaker_to_analyze].mean(), 4)

    # Find the index of the closest value to `val` in the x-axis array
    idx = np.abs(x - val).argmin()

    # Create the plot
    fig, ax = plt.subplots(figsize=(10,0.5))
    ax.axvline(x=x[idx], color='black', lw=2)
    ax.imshow(np.array([x]), aspect='auto', cmap=cmap, extent=[-5, 5, -1, 1])
    ax.set_xlim([-5, 5])
    ax.set_ylim([-1, 1])
    ax.set_xticks(np.arange(-5, 6, 1))
    ax.set_yticks([])

    ax.set_facecolor('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')

    ax.set_xlabel('Tonal Sentiment Score')

    # Display the plot in the Streamlit app
    st.pyplot(fig)
    ################################################################
    st.subheader("Tonal Sentiment behind each of his sentences")

    # Plotting metrics
    #diff = (data['Robert Reffkin'].mean() - data['Interviewer 1'].mean()) / 2

    st.bar_chart(data[speaker_to_analyze])
    ################################################################