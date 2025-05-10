import time
import os

from lora import send_message
from variables import get_known_devices, get_message

IS_DEBUG = os.getenv("LORACOM_DEBUG", "0") == "1"

if not IS_DEBUG and False:
    import RPi.GPIO as GPIO
    from display import update_display

    BUTTON_NEXT = 17
    BUTTON_SELECT = 27

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handle_buttons():
    global selected_index
    if IS_DEBUG or True:
        print("Buttons initialisieren (Debug-Modus)")
        return
    while True:
        if GPIO.input(BUTTON_NEXT) == GPIO.LOW:
            ids = sorted(get_known_devices().keys())
            if ids:
                selected_index = (selected_index + 1) % len(ids)
            update_display()
            time.sleep(0.3)
        elif GPIO.input(BUTTON_SELECT) == GPIO.LOW:
            send_message(get_message())
            time.sleep(0.3)
