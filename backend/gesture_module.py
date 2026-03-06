# gesture_module.py

def get_gesture_label(prediction):
    """
    Convert model prediction to gesture label
    """

    gesture_map = {
        0: "Hello",
        1: "Help",
        2: "Stop",
        3: "Yes",
        4: "No"
    }

    return gesture_map.get(prediction, "Unknown")