def detect_intent(text: str):

    if not text:
        return "UNKNOWN"

    text = text.lower()

    emergency_words = ["help", "danger", "emergency"]
    request_words = ["water", "food", "please"]
    greeting_words = ["hello", "hi"]
    command_words = ["stop"]

    if any(word in text for word in emergency_words):
        return "EMERGENCY"

    elif any(word in text for word in request_words):
        return "REQUEST"

    elif any(word in text for word in greeting_words):
        return "GREETING"

    elif any(word in text for word in command_words):
        return "COMMAND"

    else:
        return "GENERAL"