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
