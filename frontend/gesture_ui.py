import streamlit as st
import cv2
import mediapipe as mp
import pyttsx3
import requests
import time

st.set_page_config(page_title="V2V Gesture System")

left, center, right = st.columns([1,2,1])

with center:

    st.title("🤖 V2V - Voice to Vision AI")

    API_URL = "http://127.0.0.1:8000/gesture"

    # -------------------
    # TEXT TO SPEECH
    # -------------------

    engine = pyttsx3.init()
    engine.setProperty("rate",150)

    def speak(text):
        try:
            engine.stop()
            engine.say(text)
            engine.runAndWait()
        except:
            pass

    if "last_gesture" not in st.session_state:
        st.session_state.last_gesture = ""

    # -------------------
    # MEDIAPIPE SETUP
    # -------------------

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

    frame_placeholder = st.empty()

    gesture_box = st.empty()
    intent_box = st.empty()
    sentence_box = st.empty()
    emergency_box = st.empty()

    # -------------------
    # MAIN LOOP
    # -------------------

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

                # -------------------------
                # GESTURE MAPPING
                # (UNCHANGED)
                # -------------------------

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

        # -------------------------
        # BACKEND API
        # -------------------------

        try:

            response = requests.post(API_URL, params={"gesture": gesture})

            data = response.json()

            intent = data.get("intent","")
            sentence = data.get("sentence","")

        except:

            intent = "Backend Offline"
            sentence = ""

        # -------------------------
        # VOICE OUTPUT
        # -------------------------

        if gesture != "Detecting..." and gesture != st.session_state.last_gesture:

            speak(sentence)

            st.session_state.last_gesture = gesture

        # -------------------------
        # UI DISPLAY
        # -------------------------

        frame_placeholder.image(frame, channels="BGR")

        gesture_box.markdown(f"### ✋ Gesture: **{gesture}**")

        intent_box.markdown(f"### 🧠 Intent: **{intent}**")

        sentence_box.markdown(f"### 💬 Sentence: **{sentence}**")

        if intent == "EMERGENCY":

            emergency_box.error("🚨 EMERGENCY DETECTED!")

        else:

            emergency_box.empty()

        time.sleep(0.05)