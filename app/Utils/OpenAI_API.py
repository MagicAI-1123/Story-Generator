import os
import openai
from dotenv import load_dotenv
import os
import time


load_dotenv()


def get_answer(msg):
    start_time = time.time()
    instructor = f"""
        You will act as a human. Please answer to user's question.
    """
    print(msg)
    response = openai.ChatCompletion.create(
        model='gpt-4-1106-preview',
        max_tokens=2500,
        messages=[
            {'role': 'system', 'content': instructor},
            {'role': 'user', 'content': msg}
        ],
    )
    current_time = time.time()
    print("Elapsed time: ", current_time - start_time)
    return response.choices[0].message.content + '\n'


def get_answer_using_audio(file_location):
    audio_file = open(file_location, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # print(transcript)
    return get_answer(transcript["text"])

