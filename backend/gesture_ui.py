import streamlit as st
import cv2
import mediapipe as mp
import joblib
import numpy as np

# Load model
model = joblib.load("gesture_model.pkl")

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# UI
st.title("V2V - Voice to Vision")
st.subheader("Real-time Gesture Translation")

run = st.checkbox("Start Camera")

frame_window = st.image([])

gesture_text = st.empty()
sentence_text = st.empty()

gesture_sentences = {
    "Help": "I need help",
    "Yes": "Yes that is correct",
    "No": "No that is not correct",
    "Stop": "Please stop",
    "Hello": "Hello nice to meet you"
}

cap = cv2.VideoCapture(0)

while run:

    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image)

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

            thumb_up = thumb_tip.y < thumb_ip.y
            index_up = index_tip.y < index_pip.y
            middle_up = middle_tip.y < middle_pip.y
            ring_up = ring_tip.y < ring_pip.y
            pinky_up = pinky_tip.y < pinky_pip.y

            features = [[
                int(thumb_up),
                int(index_up),
                int(middle_up),
                int(ring_up),
                int(pinky_up)
            ]]

            gesture = model.predict(features)[0]

    sentence = gesture_sentences.get(gesture,"")

    gesture_text.markdown(f"### Gesture: {gesture}")
    sentence_text.markdown(f"### Sentence: {sentence}")

    frame_window.image(image)

cap.release()