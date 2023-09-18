import openai
import os
from dotenv import load_dotenv
from app.Utils.pinecone import get_transcript_from_audio, get_profile_information, rewrite_adventure_story, get_image_generation_prompt

get_transcript_from_audio()

file_content = ""
with open("./data/transcript/Oct 2022 Beach Trip.txt", "rb") as txt_file:
    file_content = str(txt_file.read())

get_profile_information(file_content)

rewrite_adventure_story(file_content)

get_image_generation_prompt(file_content)
