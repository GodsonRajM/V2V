def detect_intent(text: str):

    text = text.lower()

    emergency_words = ["help", "danger", "emergency"]
    request_words = ["water", "food", "please"]

    if any(word in text for word in emergency_words):
        return "EMERGENCY"

    elif any(word in text for word in request_words):
        return "REQUEST"

    else:
        return "GENERAL"