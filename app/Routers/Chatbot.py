from fastapi import APIRouter, Form, UploadFile, File
from app.Utils.OpenAI_API import get_answer_using_audio
from app.Utils.elevenlabs import text_to_speech
import shutil
import os
router = APIRouter()


@router.post("/transcript-audio-file")
def transcript_audio_file(file: UploadFile = File(...)):
    UPLOAD_DIRECTORY = "./data"
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = get_answer_using_audio(file_location)
    print(result)
    return text_to_speech(result)
    # return file.filename + " - goldrace"
