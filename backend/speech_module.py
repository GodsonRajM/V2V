from faster_whisper import WhisperModel
import os

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

def speech_to_text(audio_path):

    if not os.path.exists(audio_path):
        return "Audio file not found"

    segments, info = model.transcribe(audio_path)

    text = ""

    for segment in segments:
        text += segment.text + " "

    return text.strip()