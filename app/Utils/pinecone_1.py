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


def get_answer(audio_file_name: str):
    destination_directory = "./transcript/"
    destination_file_path = os.path.join(
        destination_directory, audio_file_name + '.txt')
    with open(destination_file_path, 'r') as file:
        file_content = file.read()

    instructor = f"""
      I want you to act as a fairy tale writer.
      You will come up with creative and funny stories that can engage childrens for long periods of time as intended in the given scenario.
      The aim is to write something that has an outstanding plotline, engaging characters and unexpected climaxes.
      Childrens like funny, adventurous and fantastic stories so you will write funny, adventurous and fantastic fairy tale.
      The grammer of each sentence will almost correct and the easier it is to understand, the better.
      At the beginning of your story, you should output your story's characters' name with an introduction to each character.
      Next you will create about 80 to 90 sentences of nearly 30 pages that childrens can understand easily and feel fun according to given scenario below.
      Every sentence will have about 10 - 12 words.
      You should not omit pages like "...", and write exact one or two sentences on each page.
      So I think there are 30 pages from 1 page to 30 page in your story.
      
      
      -----------------------
      This is the given scenario you can refer to.
      {file_content}
      
      -----------------------
      This is the sample output.
      
      Characters:
      Jone : the caring father of failly.
      sophi : Jone's lovely wife.
      ...
      
      -----------------------
      Basic Story:
      
      Page 1:
      Once upon a time in a small town lived a delightful family of five.
      Their lives were ordinary until one sunny day, in the wonderful month of October, they decided to embark on a grand adventure to the enchanting land of Santa Rosa Beach, Florida.
      
      Page 2:
      And that is why till this day, smiles spark up at the mere mention of the wonderful Florida trip.
      There was so much to do that Luca and Adelina's eyes shone with merriment.
      
           
  """

    # And then I also want you to act as a stage director, so you should creat another 50-60 sentences of these nearly 30 pages' image creation commands and should output them
    # You will come up with lively and fun image creation command on every pages so that with these commands I can create images by DALL·E which is a A model that can generate and edit images given a natural language prompt.
    # These image creation command will contain lively expression of your characters and their behaviors and actions and suitable environments.
    # So I think there are another 30 pages from 1 page to 30 page in your Image descriptions part.

    # -----------------------
    # Image descriptions:

    # Page 1:
    # Create an image with a family of five members are resting in the garden of their small house in town.

    # Page 2:
    # Create an image with a family of five members are resting in the garden of their small house in town.

    answer_directory = "./answer/"
    answer_file_path = os.path.join(
        answer_directory, audio_file_name + '.txt')
    os.makedirs(answer_directory, exist_ok=True)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": instructor},
                {"role": "user", "content": "I need to write a fairy tale."}
            ],
        )
        with open(answer_file_path, 'w') as f:
            f.write(response.choices[0].message.content)
    except Exception as e:
        print(e)
