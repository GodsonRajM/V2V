from fastapi import FastAPI
from intent_module import detect_intent
from emergency_module import check_emergency
from speech_module import speech_to_text

app = FastAPI()


@app.get("/")
def home():
    return {"message": "V2V Backend Running"}


# Intent detection API
@app.post("/intent")
def get_intent(text: str):

    intent = detect_intent(text)
    alert = check_emergency(intent)

    return {
        "text": text,
        "intent": intent,
        "alert": alert
    }


# Gesture processing API
@app.post("/gesture")
def process_gesture(gesture: str):

    intent = detect_intent(gesture)
    alert = check_emergency(intent)

    return {
        "gesture": gesture,
        "intent": intent,
        "alert": alert
    }


# Speech processing API
@app.post("/speech")
def process_speech(audio_path: str):

    text = speech_to_text(audio_path)

    intent = detect_intent(text)
    alert = check_emergency(intent)

    return {
        "speech_text": text,
        "intent": intent,
        "alert": alert
    }