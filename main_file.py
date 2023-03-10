import os
import pandas as pd
import json, asyncio
import nltk
from datetime import datetime
from dotenv import load_dotenv

#Importing other files
from editDataframe import edit_dataframe

from deepgram import Deepgram
from nltk.tokenize.treebank import TreebankWordDetokenizer

#Libraries to create CLI commands
import typer
from rich import print
from rich.console import Console
from rich.traceback import Traceback

#To check file types
import mimetypes
import streamlit as st

# To analyse text
from textAnalysis import text_analysis

# Define the Typer app
app = typer.Typer()

load_dotenv()
console = Console()

# Settign dataframe displaying options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main_file_commands(audioPathFile, emotion_classifier_df, editJSON="NO",API_request_title='MercuryDashboardAPI'):

    print(f"File path: {audioPathFile}")
    #print(f"Speaker name: {speaker_name}")

    print("File type of audio uploaded is: " + str(mimetypes.guess_type(audioPathFile)[0]))

    fileType = audioPathFile[-4:] # Gets .mp3
    #typer.echo(fileType)
    fileName = audioPathFile[:-4] # Gets the name of the file without the .mp3

    if ((fileType.lower() != ".mp3")):
        #print("Only MP3 files are allowed. Please enter a valid audio file and try again.")
        st.error("Only MP3 files are allowed. Please enter a valid audio file and try again.")
        quit()

    #speaker_name = str(input("Enter the name of the speaker: \n"))
    section = "Q_AND_A"

    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

    try:
        FILE = audioPathFile
        MIMETYPE = 'audio/{}'.format(fileType) #mp3
    except:
        FILE = str(input("Drag the audio file or enter its pathname: \n"))
        MIMETYPE = 'audio/{}'.format(fileType) #mp3

    data = ""
    async def main():
        try:
            global data
            # Initialize the Deepgram SDK
            deepgram = Deepgram(DEEPGRAM_API_KEY)

            options = { "punctuate": True, "model": "finance", "tier":"enhanced", "language": "en", "diarize":True }

            # Check whether requested file is local or remote, and prepare source
            if FILE.startswith('http'):
                # file is remote
                # Set the source
                source = {
                'url': FILE
                }
            else:
                # file is local
                # Open the audio file
                audio = open(FILE, 'rb')

                # Set the source
                source = {
                'buffer': audio,
                'mimetype': MIMETYPE
                }

            # Send the audio to Deepgram and get the response
            response = await asyncio.create_task(
                deepgram.transcription.prerecorded(
                source,options
                )
            )

            #print(json.dumps(response))
            #print(json.dumps(response['results']['channels'][0]['alternatives'][0]['words'], indent=4))

            transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
            transcript = transcript.replace("...",".")
            transcript = transcript.replace("?",".")
            transcript = transcript.replace(",","")

            #print(str(transcript))

            #print(transcript)

            sentences = nltk.sent_tokenize(transcript)
            #print(sentences)

            data = response['results']['channels'][0]['alternatives'][0]['words']

            speaker_list = []
            sentence_start_time = {}
            sentence_end_time = {}
            start_processed_words = set()
            end_processed_words = set()
            for sentence in sentences:
                sentence_words = sentence.split()
                if len(sentence_words) != 1:
                    start_time = None
                    end_time = None
                    for word_data in data:
                        #print(word_data['word'].upper()+ str(word_data["start"]))
                        if (word_data['word'].upper()+ str(word_data["start"])) in start_processed_words:
                            continue
                        start_processed_words.add(word_data['word'].upper() + str(word_data["start"]))
                        if word_data['word'].upper() == sentence_words[0].upper():
                            start_time = word_data["start"]

                            #speaker_list.append(word_data['speaker'])

                            sentence_start_time[sentence] = (start_time)
                            #print(sentence_start_time)
                            break

                    speaker_number_list = []
                    for word_data in data:
                        #print("WORD DATA: {}".format(word_data))
                        #print(word_data['word'].upper() + str(word_data["end"]))
                        if (word_data['word'].upper() + str(word_data["end"])) in end_processed_words:
                            continue
                        end_processed_words.add(word_data['word'].upper() + str(word_data["end"]))
                        word = word_data['word'] + "."
                        #print(word.upper())
                        #print(sentence_words[-1].upper())
                        #print('------------------')
                        if word.upper() == sentence_words[-1].upper():
                            end_time = word_data["end"]
                            if len(sentence) != 1:
                                sentence_end_time[sentence] = (end_time)
                                speaker_list.append(word_data['speaker'])
                                #speaker_number_list.append(word_data[''])
                                #print(sentence_end_time)
                            else:
                                pass
                            break
                else:
                    pass

            df = pd.DataFrame([sentence_start_time, sentence_end_time])
            df = df.transpose()
            df = df.reset_index(inplace=False)

            column_list = ["statement","start", "stop"]

            df.columns = column_list

            df.insert(loc = 0,
                column = "speaker",
                value = speaker_list #[speaker_name] * len(df['statement'])
            )

            df.insert(loc = 1,
                    column = "section",
                    value = [section] * len(df['statement'])
                    )

            df.insert(loc = 3,
                    column = "type",
                    value = [""] * len(df['statement'])
                    )

            #print(speaker_list)

            #df['speaker_name'] = speaker_list # Adding speaker number column

            data = df

            #print(data)

            #print((data['speaker'].unique()))
            unique_speaker_numbers = [int(value) for value in (data['speaker'].unique())]
            unique_speaker_numbers_legth = len(unique_speaker_numbers)

            #df_filtered = df[df['speaker'] == unique_speaker_numbers_legth and df['speaker'] == 1 and df['speaker'] == 2]
            #print(df_filtered)
            #print(unique_speaker_numbers)

            print(data[['speaker','statement']])
            #typer.echo(typer.style("{} speaker(s) identified in this audio".format(unique_speaker_numbers_legth), fg=typer.colors.BRIGHT_YELLOW, bg=typer.colors.BLACK, bold=True, blink = False))
            st.write("{} speaker(s) identified in this audio".format(unique_speaker_numbers_legth))
            for num in unique_speaker_numbers:
                speaker_name_user_input = st.text_input("Enter the name of speaker {}".format(num))
                data['speaker'] = data['speaker'].replace(num, speaker_name_user_input)
            
            df = df.reset_index(inplace=False)

            unique_speaker_names = [str(name) for name in (data['speaker'].unique())]

            #print(data)

            text_analysis(transcript)
            edit_dataframe(data, audioPathFile, fileName, API_request_title, editJSON, unique_speaker_names, emotion_classifier_df)

        except Exception as e:
            #typer.echo("Make sure you've entered the correct filepath. Please try again")
            st.error(e, icon="🚨")
            quit()

    print(asyncio.run(main()))

if __name__ == '__main__':
    app()