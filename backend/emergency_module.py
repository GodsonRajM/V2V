def check_emergency(intent: str):

    if not intent:
        return False

    return intent.upper() == "EMERGENCY"