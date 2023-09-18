import openai
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

character_description = ''
scene_description = ''
basic_story = ''
final_story = ''


def get_answer(audio_file_name: str):
    destination_directory = "./transcript/"
    destination_file_path = os.path.join(
        destination_directory, audio_file_name + '.txt')
    with open(destination_file_path, 'r') as file:
        file_content = file.read()

    create_scene_description(file_content)


def create_scene_description(file_content: str):
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
        I will give you sample output.

        -----------------------
        This is the given scenario you can refer to.
        {file_content}

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
                {"role": "user", "content": "I need to write a fairy tale."}
            ],
        )
        scene_description = response.choices[0].message.content
    except Exception as e:
        print(e)

    create_basic_story(file_content, scene_description)


def create_basic_story(file_content: str, scene_description: str):
    instructor = f"""
        I want you to act as fairy tale writer.
        You will come up with creative and funny stories that can engage 3 years old childrens for long periods of time as intended in the given scenario.
        The aim is to write something that has an outstanding plotline, engaging characters and unexpected climaxes.
        Childrens like funny, adventurous and fantastic stories so you will write funny, adventurous and fantastic fairy tale.
        You will create between 1,000 to 2,000 words sentences of nearly 25 pages that 3 years old childrens can understand easily and feel fun according to given scenario below.
        Every sentence will have about 10 - 12 words and each page must be described exactly on any one of given scenes below.
        The most important thing is that you should write your fairy tale with 25 pages based on given scenes below.
        I mean your story's charactors should appear on these given scenes and should play their parts.
        So I want you create a funny fairy tale according to and based on given scenes.
        I want you output exactly one scene that each page based on at the end of each page.
        I will give you sample output.
        -----------------------
        This is the given scenes you can refer to.
        {scene_description}
        
        -----------------------
        This is the given scenario you can refer to.
        {file_content}
        
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
    answer_directory = "./answer/"
    answer_file_path = os.path.join(
        answer_directory, 'final.txt')
    os.makedirs(answer_directory, exist_ok=True)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": instructor},
                {"role": "user", "content": "I need to write a fairy tale."}
            ],
        )
        basic_story = response.choices[0].message.content
        with open(answer_file_path, 'w') as f:
            f.write(scene_description + '\n\n' + basic_story)
    except Exception as e:
        print(e)


# def create_final_story(scene_description: str, basic_story: str):
#     instructor = f"""
#         I want you to act as fairy tale writer.
#         You will complete the given story written by fairy tale writer.
#         Childrens like funny, adventurous and fantastic stories so you will write funny, adventurous and fantastic fairy tale.
#         I want this fairy tale will contain nearly 25 to 30 pages of 80 to 90 sentencesthat childrens can understand easily and feel fun according to given scenario below but this one has not enough pages.
#         So I want you complete the given story more richly, lively, and novelly.
#         But I don't want you change too many of given story.
#         You can insert some pages into given story and can change some expressions.
#         The most important thing is that this story has about 25 to 30 pages.
#         Every sentence will have about 10 - 12 words and each page must be described on any one of given scenes below.
#         So I want you adapt the fairy tale more interestingly than before according to and based on given scenes below.
#         I will give you sample output.
#         -----------------------
#         This is the given scenes you can refer to.
#         {scene_description}

#         -----------------------
#         This is the given story you can refer to.
#         {basic_story}

#         -----------------------
#         This is the sample output.

#         Final Story:

#         Page 1:
#         Their lives were ordinary until one sunny day, in the wonderful month of October, they decided to embark on a grand adventure to the enchanting land of Santa Rosa Beach, Florida.
#         [scene 2]

#         Page 2:
#         And that is why till this day, smiles spark up at the mere mention of the wonderful Florida trip.
#         [scene 1]

#     """
#     answer_directory = "./answer/"
#     answer_file_path = os.path.join(
#         answer_directory, 'final.txt')
#     os.makedirs(answer_directory, exist_ok=True)

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": instructor},
#                 {"role": "user", "content": "I need to write a fairy tale."}
#             ],
#         )
#         final_story = response.choices[0].message.content
#         with open(answer_file_path, 'w') as f:
#             f.write(scene_description + '\n\n' + final_story)

#     except Exception as e:
#         print(e)
