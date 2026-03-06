import cv2
import mediapipe as mp
import requests
import pyttsx3
import threading
import joblib
import os

# Load model
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "..", "gesture_model.pkl")

model = joblib.load(model_path)

# Text to speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# Gesture sentences
gesture_sentences = {
    "Help": "I need help",
    "Yes": "Yes that is correct",
    "No": "No that is not correct",
    "Stop": "Please stop",
    "Hello": "Hello nice to meet you"
}

sentence = ""
intent = ""
last_spoken_gesture = ""

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

API_URL = "http://127.0.0.1:8000/gesture"

gesture_buffer = []
buffer_size = 8

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    gesture = ""

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

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

            features = [[
                int(thumb_up),
                int(index_up),
                int(middle_up),
                int(ring_up),
                int(pinky_up)
            ]]

            gesture = model.predict(features)[0]

    if gesture != "":
        gesture_buffer.append(gesture)

        if len(gesture_buffer) > buffer_size:
            gesture_buffer.pop(0)

    stable_gesture = ""

    if len(gesture_buffer) == buffer_size and gesture_buffer.count(gesture_buffer[-1]) == buffer_size:
        stable_gesture = gesture_buffer[-1]

    if stable_gesture != "" and stable_gesture != last_spoken_gesture:

        try:

            response = requests.post(
                API_URL,
                params={"gesture": stable_gesture}
            )

            data = response.json()

            intent = data.get("intent", "")
            sentence = gesture_sentences.get(stable_gesture, "")

            speak(sentence)

            if intent == "EMERGENCY":
                speak("Emergency detected. This person needs help.")

            last_spoken_gesture = stable_gesture

        except:
            intent = "Backend Offline"

    display_gesture = stable_gesture if stable_gesture else "Detecting..."

    cv2.putText(img, f"Gesture: {display_gesture}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(img, f"Intent: {intent}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.putText(img, f"Sentence: {sentence}", (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("V2V Gesture Detection", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()