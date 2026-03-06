from fastapi import FastAPI
from intent_module import detect_intent
from emergency_module import check_emergency
from speech_module import speech_to_text

app = FastAPI()

latest_data = {
    "gesture": "",
    "intent": "",
    "sentence": ""
}

sentence_map = {
    "Help": "I need help",
    "Hello": "Hello nice to meet you",
    "Stop": "Please stop",
    "Yes": "Yes that is correct",
    "No": "No that is not correct"
}


@app.get("/")
def home():
    return {"message": "V2V Backend Running"}


@app.post("/gesture")
def receive_gesture(gesture: str):

    intent = detect_intent(gesture)

    latest_data["gesture"] = gesture
    latest_data["intent"] = intent
    latest_data["sentence"] = sentence_map.get(gesture, "")

    return latest_data


@app.get("/latest")
def get_latest():
    return latest_data


@app.post("/speech")
def process_speech(audio_path: str):

    text = speech_to_text(audio_path)

    intent = detect_intent(text)

    return {
        "speech_text": text,
        "intent": intent
    }