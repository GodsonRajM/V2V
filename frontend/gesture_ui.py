import streamlit as st
import cv2
import mediapipe as mp
import pyttsx3

st.set_page_config(page_title="V2V Gesture System", layout="wide")

st.title("🤖 V2V - Voice to Vision AI")

# -----------------------------
# TEXT TO SPEECH
# -----------------------------

engine = pyttsx3.init()
engine.setProperty("rate",150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# remember last gesture
if "last_gesture" not in st.session_state:
    st.session_state.last_gesture = ""

# -----------------------------
# SENTENCE MAP
# -----------------------------

gesture_sentences = {
    "Help":"I need help",
    "Yes":"Yes that is correct",
    "No":"No that is not correct",
    "Stop":"Please stop",
    "Hello":"Hello nice to meet you"
}

# -----------------------------
# MEDIAPIPE SETUP
# -----------------------------

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("Camera not detected")
    st.stop()

# -----------------------------
# UI PLACEHOLDERS
# -----------------------------

frame_placeholder = st.empty()
gesture_box = st.empty()
sentence_box = st.empty()

gesture = "Detecting..."

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture = "Detecting..."

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]

            thumb_ip = hand_landmarks.landmark[3]
            index_pip = hand_landmarks.landmark[6]
            middle_pip = hand_landmarks.landmark[10]
            ring_pip = hand_landmarks.landmark[14]
            pinky_pip = hand_landmarks.landmark[18]

            thumb_up = thumb_tip.x < thumb_ip.x
            index_up = index_tip.y < index_pip.y
            middle_up = middle_tip.y < middle_pip.y
            ring_up = ring_tip.y < ring_pip.y
            pinky_up = pinky_tip.y < pinky_pip.y

            fingers = [
                int(thumb_up),
                int(index_up),
                int(middle_up),
                int(ring_up),
                int(pinky_up)
            ]

            # -----------------------------
            # GESTURE MAPPING
            # -----------------------------

            if fingers == [0,1,0,0,0]:
                gesture = "Help"

            elif fingers == [1,0,0,0,0]:
                gesture = "Yes"

            elif fingers == [0,0,0,0,0]:
                gesture = "No"

            elif fingers == [1,1,1,1,1]:
                gesture = "Stop"

            elif fingers == [0,1,1,0,0]:
                gesture = "Hello"

    sentence = gesture_sentences.get(gesture,"")

    # -----------------------------
    # SPEAK WHEN GESTURE CHANGES
    # -----------------------------

    if gesture != "Detecting..." and gesture != st.session_state.last_gesture:

        speak(sentence)

        st.session_state.last_gesture = gesture

    frame_placeholder.image(frame, channels="BGR")

    gesture_box.markdown(f"## ✋ Gesture: **{gesture}**")

    sentence_box.markdown(f"## 💬 Sentence: **{sentence}**")