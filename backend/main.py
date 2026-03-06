from fastapi import FastAPI
from speech_module import speech_to_text
from record_audio import record_audio

app = FastAPI()

latest_data = {
    "gesture": "",
    "intent": "",
    "sentence": ""
}

@app.get("/")
def home():
    return {"message": "V2V Backend Running"}


# -------------------
# Gesture API
# -------------------

@app.post("/gesture")
def receive_gesture(gesture: str):

    intent = "NORMAL"

    if gesture in ["Help","Doctor"]:
        intent = "EMERGENCY"

    sentence_map = {

        "Help":"I need help",
        "Hello":"Hello nice to meet you",
        "Stop":"Please stop",
        "Yes":"Yes that is correct",
        "No":"No that is not correct",

        "Thank You":"Thank you very much",
        "Please":"Please help me",
        "Water":"I need water",
        "Food":"I need food",
        "Doctor":"Please call a doctor",

        "OK":"Everything is okay",
        "Wait":"Please wait",
        "Come":"Please come here",
        "Go":"You may go",
        "Good":"That is good"
    }

    latest_data["gesture"] = gesture
    latest_data["intent"] = intent
    latest_data["sentence"] = sentence_map.get(gesture,"")

    return latest_data


@app.get("/latest")
def get_latest():
    return latest_data


# -------------------
# Speech API
# -------------------

@app.post("/speech")
def process_speech():

    audio_file = record_audio()

    text = speech_to_text(audio_file)

    intent = "GENERAL"

    if "help" in text.lower():
        intent = "EMERGENCY"

    return {
        "speech_text": text,
        "intent": intent
    }