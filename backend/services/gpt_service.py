from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
def single_driver_analysis(track, data):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

        prompt = f"Here is some data: {data}. You are an F1 race engineer. The data you have been provided is of an F1 driver who has just done a lap around {track}. The data you are seeing is of speed, throttle usage, brake usage, and gear usage. All these are plotted against distance from the start line, and the corner numbers are marked too. Using this data, I need you to identify the critical braking points, any potential mistakes the driver made through the lap, and any tips for improvement. Make sure those three things are always available! Refer to the points of interest by corner numbers."

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


def comparative_analysis(track, user_data, pro_data):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

        prompt = f"Here is dataset 1: {pro_data}. Here is dataset 2: {user_data}. You are an F1 race engineer. You have been given data of 2 drivers. The first bit of data you have been provided is of an F1 driver who has just done a lap around {track}. The data you are seeing is of speed, throttle usage, brake usage, and gear usage. All these are plotted against distance from the start line, and the corner numbers are marked too. The second bit of data you have been provided is of mine, an average driver. It is the same kind of data about the same track, just a different driver. I want you to compare the two sets of data, and tell me what I have done wrong in comparison to the f1 driver. For example, whether I braked too early, whether my throttle usage is too sharp, etc. Mention the corners where these errors have been made and give advice on how I can improve upon that."

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


