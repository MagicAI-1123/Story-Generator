import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_transcript_from_audio():
    audio_file = open("./data/audio/Oct 2022 Beach Trip.m4a", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    with open("./data/transcript/Oct 2022 Beach Trip.txt", "w") as txt_file:
        txt_file.write(transcript["text"])
    return transcript["text"]


def get_profile_information(text: str):
    instrcutor = """
    You are a Profile Generator.
    User will give you context and you have to refer to it to identify unique characters and list them in the <name>: <short profile information> paris.
    Create each character profile as short as possible without missing any characteristics mentioned in the context.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": instrcutor},
            {"role": "user", "content": text},
        ]
    )

    with open("./data/characteristics/Oct 2022 Beach Trip Characters.txt", "w") as txt_file:
        txt_file.write(response.choices[0].message.content)
    return response.choices[0].message.content


def create_scene_description(text: str):
    instructor = f"""
        I want you to act as fairy tale writer and stage director.
        I want to come up with creative and funny stories that can engage childrens for long periods of time as intended in the given scenario.
        The aim is to write something that has an outstanding plotline, engaging characters and unexpected climaxes.
        Childrens like funny, adventurous and fantastic stories so I will write funny, adventurous and fantastic fairy tale.
        I will create between 1,000 to 2,000 words of nearly 20 to 30 pages that 3 years old childrens can understand easily and feel fun according to given scenario below.
        Every sentence will have about 12 - 15 words.
        So for that I want you will create about 4 to 5 scenes on which my story's characters will behaive and act according to my scenario.
        So you can understand about these five scenes as the description of several places not the fairy tale sentence.
        So your scenes may not contain human and human's action because it's only the description about the environment and nation.
        I will refer to given context as my scenario so you can create scenes based on this context.
        These scenes should be suitable for my story so that I can write my fairy tale based on your scenes.
        So you should output the description about your creative and funny scenes detail by one or two sentences per scenes and entire plot of my story will flow on these 4 to 5 scenes.
        It is better that these scenes are independent for each other so that you can write your fairy tale more creatively and freely.
        My first request will start with "I need you to write scenes."
        I will give you sample output.

        -----------------------
        This is the given scenario you can refer to.
        {text}

        -----------------------
        This is the sample output.

        Scenes:

        scene 1:
        There is a small house with the beautiful garden in a town and a family of 5 members sit in the garden.
        It's a sunny day so the sun shinning and there is no cloud in the sky.

        scene 2:
        ...
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": instructor},
                {"role": "user", "content": "I need you to write scenes."}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        raise e


def rewrite_basic_story(text: str):
    characters = ""
    with open("./data/characteristics/Oct 2022 Beach Trip Characters.txt", "rb") as txt_file:
        characters = str(txt_file.read())

    scene_description = create_scene_description(text)

    instructor = f"""
        I want you to act as fairy tale writer.
        I need you to write fairy tale as long as possible without adding any event not mentioned in my scenario.
        You will come up with creative and funny stories that can engage 3 years old childrens for long periods of time as intended in the given scenario.
        The aim is to write something that has an outstanding plotline, engaging characters and unexpected climaxes.
        Childrens like funny, adventurous and fantastic stories so you will write funny, adventurous and fantastic fairy tale.
        You will create between 1,000 to 2,000 words sentences of nearly 25 pages that 3 years old childrens can understand easily and feel fun according to given scenario below.
        Every sentence will have about 10 - 12 words and each page must be described exactly on any one of given scenes below.
        The most important thing is that you should write your fairy tale with 25 pages based on given scenes below.
        I mean your story's charactors should appear on these given scenes and should play their parts.
        So I want you create a funny fairy tale according to and based on given scenes.
        Split the story into 20 to 30 pages with their page number.
        I want you output exactly one scene that each page based on at the end of each page.
        My first request will start with "I need you to write a fairy tale."
        I will give you sample output.
        -----------------------
        This is the characters mentioned in the scenario.
        -----------------------
        {characters}

        -----------------------
        This is the given scenes you can refer to.
        {scene_description}
        
        -----------------------
        This is the given scenario you can refer to.
        {text}
        
        -----------------------
        This is the sample output.

        Basic Story:

        Page 1:
        Their lives were ordinary until one sunny day, in the wonderful month of October, they decided to embark on a grand adventure to the enchanting land of Santa Rosa Beach, Florida.
        [scene 3]

        Page 2:
        And that is why till this day, smiles spark up at the mere mention of the wonderful Florida trip.
        [scene 1]
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": instructor},
            {"role": "user", "content": "I need you to write a fairy tale."}

        ]
    )
    with open("./data/story/Oct 2022 Beach Trip Basic Story.txt", "w") as txt_file:
        txt_file.write(response.choices[0].message.content)
    return response.choices[0].message.content


def rewrite_adventure_story(text: str):
    characters = ""
    with open("./data/characteristics/Oct 2022 Beach Trip Characters.txt", "rb") as txt_file:
        characters = str(txt_file.read())

    instrcutor = f"""
    I need you to re-write my story in an extremely adventurous style as long as possible.
    You can add your own drama or an adventurous event that has never mentioned on my story to make the story as adventurous as possible.
    Write the story with the words that 3 years old children can understand easily.
    Story must be between 1,000 to 2,000 words that will be spread across 20 to 30 pages in a children's book.
    Split the story into 20 to 30 pages with their page number.
    
    This is the characters mentioned in the story.
    -------------
    {characters}
    -------------

    This is my story.
    ------------
    {text}
    ------------
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": instrcutor},
        ]
    )
    with open("./data/story/Oct 2022 Beach Trip Adventurous Story.txt", "w") as txt_file:
        txt_file.write(response.choices[0].message.content)
    return response.choices[0].message.content


def get_image_generation_prompt(text: str):
    characters = ""
    with open("./data/characteristics/Oct 2022 Beach Trip Characters.txt", "rb") as txt_file:
        characters = str(txt_file.read())
    instrcutor = f"""
    1. General Description
    I need you to create image generation prompt for Stable Diffusion model for each page.
    I'll give you a story which splitted into pages.
    Your role is to generate image generation prompt for each page that will be used for Stable Diffusion.
    You'll be given characters that will appear in the story also.
    When you generate image prompt, you must name all of the characters in the prompt so Stable Diffusion model can pick the right character.
    Also, you have to generate a background description like where, time of day, etc.
    Each Page's Story has background description so you have to refer to that background description for generationg prompt.
    *****Background description like place, time of day must based on each page's story.*****
    2. Image Generation Prompt
    Prompt must in this format.
    ---------
    Create an image with <<character>>, <<character>> and <<character>> doing <<related subject>> at <<somewhere>> in <<time of day>>
    ---------
    3. Important Note
    All of the characters in the prompt must be named exactly so Stable Diffusion can identify all of the characters.
    Never say ambigious characters like "he", "she", "children", "they", "whole family", and etc.
    Find the exact character name in the characters lists given and name that character in the prompt.
    This is examples of bad and good prompt.
    Bad prompt: Create an image with A enjoying time with his three children at their backyard during a sunny afternoon.
    Good prompt: Create an image with A enjoying time with B,C,D at their backyard during a sunny afternoon.


    This is the characters mentioned in the story.
    -------------
    {characters}
    -------------

    This is the story.
    ------------
    {text}
    ------------
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": instrcutor},
        ]
    )
    with open("./data/image-generation-prompts/Oct 2022 Beach Trip Basic Story Image Generation Prompt.txt", "w") as txt_file:
        txt_file.write(response.choices[0].message.content)
    return response.choices[0].message.content


