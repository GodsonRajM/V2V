import streamlit as st
import cv2
import mediapipe as mp
import pyttsx3
import requests
import time

st.set_page_config(page_title="V2V Gesture System", layout="wide")

st.title("🤖 V2V - Voice to Vision AI")

API_URL = "http://127.0.0.1:8000/gesture"

# -----------------------------
# TEXT TO SPEECH
# -----------------------------

engine = pyttsx3.init()
engine.setProperty("rate",150)

import os

VOICE_ENABLED = True

# Disable voice on cloud servers like Render
if "RENDER" in os.environ:
    VOICE_ENABLED = False

if VOICE_ENABLED:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate",150)

def speak(text):
    if not VOICE_ENABLED:
        return

    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# -----------------------------
# SESSION STATE
# -----------------------------

if "last_gesture" not in st.session_state:
    st.session_state.last_gesture = ""

# -----------------------------
# GESTURE ICONS
# -----------------------------

gesture_icons = {
"Help":"🆘",
"Yes":"👍",
"No":"✋",
"Stop":"🛑",
"Hello":"👋",
"Thank You":"🙏",
"Please":"🤲",
"Water":"💧",
"Food":"🍽️",
"Doctor":"🩺",
"OK":"👌",
"Wait":"⏳",
"Come":"👉",
"Go":"➡️",
"Good":"⭐"
}

# -----------------------------
# LAYOUT
# -----------------------------

cam_col, info_col = st.columns([3,2])

with cam_col:
    st.subheader("📷 Camera Feed")
    frame_placeholder = st.empty()

with info_col:

    icon_box = st.empty()
    gesture_box = st.empty()
    intent_box = st.empty()
    sentence_box = st.empty()
    emergency_box = st.empty()

# -----------------------------
# MEDIAPIPE SETUP
# -----------------------------

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# -----------------------------
# CAMERA
# -----------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("Camera not detected")
    st.stop()

# -----------------------------
# GESTURE BUFFER
# -----------------------------

gesture_buffer = []
buffer_size = 6

last_valid_gesture = "Detecting..."

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

    gesture = None

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            lm = hand_landmarks.landmark

            thumb_tip = lm[4]
            index_tip = lm[8]
            middle_tip = lm[12]
            ring_tip = lm[16]
            pinky_tip = lm[20]

            thumb_ip = lm[3]
            index_pip = lm[6]
            middle_pip = lm[10]
            ring_pip = lm[14]
            pinky_pip = lm[18]

            if lm[17].x < lm[5].x:
                thumb_up = thumb_tip.x > thumb_ip.x
            else:
                thumb_up = thumb_tip.x < thumb_ip.x

            index_up = index_tip.y < index_pip.y - 0.02
            middle_up = middle_tip.y < middle_pip.y - 0.02
            ring_up = ring_tip.y < ring_pip.y - 0.02
            pinky_up = pinky_tip.y < pinky_pip.y - 0.02

            fingers = [
                int(thumb_up),
                int(index_up),
                int(middle_up),
                int(ring_up),
                int(pinky_up)
            ]

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

            elif fingers == [1,1,0,0,0]:
                gesture = "Thank You"

            elif fingers == [1,1,1,0,0]:
                gesture = "Please"

            elif fingers == [0,0,0,1,0]:
                gesture = "Water"

            elif fingers == [0,1,1,1,0]:
                gesture = "Food"

            elif fingers == [0,0,0,0,1]:
                gesture = "Doctor"

            elif fingers == [0,0,0,1,1]:
                gesture = "OK"

            elif fingers == [1,1,1,1,0]:
                gesture = "Wait"

            elif fingers == [0,1,1,1,1]:
                gesture = "Come"

            elif fingers == [0,1,0,1,0]:
                gesture = "Go"

            elif fingers == [0,0,1,1,1]:
                gesture = "Good"

    # -----------------------------
    # GESTURE BUFFER
    # -----------------------------

    if gesture is not None:
        gesture_buffer.append(gesture)

    if len(gesture_buffer) > buffer_size:
        gesture_buffer.pop(0)

    if len(gesture_buffer) > 0:
        stable_gesture = max(set(gesture_buffer), key=gesture_buffer.count)
        last_valid_gesture = stable_gesture
    else:
        stable_gesture = last_valid_gesture

    # -----------------------------
    # BACKEND API
    # -----------------------------

    try:

        response = requests.post(API_URL, params={"gesture": stable_gesture})

        data = response.json()

        intent = data.get("intent","")
        sentence = data.get("sentence","")

    except:

        intent = "Backend Offline"
        sentence = ""

    # -----------------------------
    # VOICE OUTPUT
    # -----------------------------

    if stable_gesture != "Detecting..." and stable_gesture != st.session_state.last_gesture:

        speak(sentence)

        st.session_state.last_gesture = stable_gesture

    # -----------------------------
    # DISPLAY
    # -----------------------------

    frame_placeholder.image(frame, channels="BGR")

    icon = gesture_icons.get(stable_gesture,"✋")

    icon_box.markdown(f"# {icon}")

    gesture_box.markdown(f"### Gesture: **{stable_gesture}**")

    intent_box.markdown(f"### Intent: **{intent}**")

    sentence_box.markdown(f"### Sentence: **{sentence}**")

    if intent == "EMERGENCY":
        emergency_box.error("🚨 EMERGENCY DETECTED!")
    else:
        emergency_box.empty()

    time.sleep(0.05)