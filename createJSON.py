import time
import pandas as pd
import json
from createTask import create_task
import typer
#from editDataframe import df
#from main_file import fileName

def create_json(df, audioPathFile, fileName, API_request_title, editJSON, unique_speaker_names, emotion_classifier_df):
    try:
        df.pop('index')
    except:
        pass
    try:
        df.pop('Unnamed: 0')
    except:
        pass
    try:
        df.pop('level_0')
    except:
        pass

    json_data = df.to_json(orient ='records' , indent=4)

    my_dict = {}
    my_dict["statements"] = json.loads(json_data)

    #print(json.dumps(my_dict, indent=4))

    #descriptorFileName = str(input('Type your descriptor file name WITH the .json extension: \n'))

    descriptorFileName = fileName + ".json"
    # Writing to sample.json
    with open(descriptorFileName, "w") as outfile:
        json.dump(my_dict, outfile)

    outfile.close()

    if (editJSON == 'YES' or editJSON == 'yes' or editJSON == 'Yes'):
        typer.echo(typer.style("Your descriptor file has been saved here: " + descriptorFileName, fg=typer.colors.YELLOW, bg =typer.colors.BLACK, bold=True, blink = False))
        typer.echo(typer.style("The program has now stopped for you to edit your descriptor file", fg=typer.colors.YELLOW, bg =typer.colors.BLACK, bold=True, blink = False))
        quit()

    create_task(audioPathFile, descriptorFileName, API_request_title, unique_speaker_names, df, emotion_classifier_df)