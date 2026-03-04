from fastapi import UploadFile, File
import shutil

@app.post("/speech")
def process_speech(file: UploadFile = File(...)):

    audio_path = "temp_audio.wav"

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = speech_to_text(audio_path)

    intent = detect_intent(text)
    alert = check_emergency(intent)

    return {
        "speech_text": text,
        "intent": intent,
        "alert": alert
    }