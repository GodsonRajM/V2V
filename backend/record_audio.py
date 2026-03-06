import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="speech.wav", duration=5, fs=16000):

    print("Speak now...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    sd.wait()

    write(filename, fs, recording)

    print("Recording finished")

    return filename