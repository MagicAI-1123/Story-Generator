import requests
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()
CHUNK_SIZE = 1024
def text_to_speech(msg):
    # url = "https://api.elevenlabs.io/v1/voices"

    # response = requests.request("GET", url)

    # print(response.text)
    # CHUNK_SIZE = 1024
    url = f"https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
    }

    data = {
        "text": msg,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    return base64.b64encode(response.content).decode('utf-8')