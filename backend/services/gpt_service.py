from openai import OpenAI
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
def single_driver_analysis(track, data, circuit_info):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        
        if isinstance(data, pd.DataFrame):
            data = data.to_json(orient="records")

        if isinstance(circuit_info, pd.DataFrame):
            circuit_info = circuit_info.to_json(orient="records")

        prompt = f"Here is the telemetry data of a professional F1 driver: {data}.\
            Here is information of where each corner on a circuit is in terms of distance from the start line: {circuit_info}\
            You are an F1 race engineer. \
            The data you have been provided is of an F1 driver who has just done a lap around {track}. \
            The data you are seeing is of speed, throttle usage, brake usage, and gear usage. \
            Each of those bits of data are a json where the attribute is the index, and the \
            corresponding value is the actual data.\
            All these are plotted against distance from the start line (labelled \'Distance\'). \
            The information on the circuit tells you where are all the corners relative to the start line\
            Using this data, I need you to identify the critical braking points, any \
            potential mistakes the driver made through the lap, and any tips for improvement. \
            Make sure those three things are always presented! Refer to the points of interest by \
            corner numbers rather than the index of the json."

        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            store = True,
            messages = [
                {"role": "user", "content": prompt}
            ]
        )

        message = completion.choices[0].message
        return message

    except Exception as e:
        return e


def comparative_analysis(track, user_data, pro_data, circuit_info, setup_data):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

        if isinstance(pro_data, pd.DataFrame):
            pro_data = pro_data.to_json(orient="records")

        if isinstance(circuit_info, pd.DataFrame):
            circuit_info = circuit_info.to_json(orient="records")

        if isinstance(user_data, pd.DataFrame):
            user_data = user_data.to_json(orient="records")

        prompt = f"Here is the telemetry data of a professional F1 driver: {pro_data}.\
            Here is the telemetry data of my driving: {user_data}. I am an average driver.\
            Here is information of where each corner on a circuit is in terms of distance from the start line: {circuit_info}\
            Here is information on how the car is set up: {setup_data}\
            You are an F1 race engineer.\
            The data I have given you is from laps done around the {track} F1 track. \
            This data is of speed, throttle usage, brake usage, gear usage, and distance from the start line. \
            All these are plotted against distance from the start line (labelled \'Distance\'). \
            The information on the circuit tells you where are all the corners relative to the start line\
            I want you to compare the two sets of data, and tell me what I have done wrong in comparison to the F1 driver. \
            For example, whether I braked too early, whether my throttle usage is too sharp, etc. \
            Mention the corners where these errors have been made and give advice on how I can improve upon that.\
            Also, try and use the setup data that has been given to you. Talk about how that also affects my lap time.\
            Do not just give me an index number from the JSON data you see instead of corners!!"

        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            store = True,
            messages = [
                {"role": "user", "content": prompt}
            ]
        )

        message = completion.choices[0].message
        return message

    except Exception as e:
        return e


