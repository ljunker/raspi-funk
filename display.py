import os

from variables import get_known_devices, get_selected_index, get_my_id, get_last_message, get_message

IS_DEBUG = os.getenv("LORACOM_DEBUG", "0") == "1"

if not IS_DEBUG and False:
    import board
    import busio
    import adafruit_ssd1306
    from PIL import Image, ImageDraw, ImageFont

# OLED state
oled = None
draw = None
image = None
font = None


def init_display():
    global oled, draw, image, font
    if IS_DEBUG:
        print("Display initialisieren (Debug-Modus)")
        return
    i2c = busio.I2C(board.SCL, board.SDA)
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
    image = Image.new("1", (128, 64))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()


def display_lines(lines):
    if IS_DEBUG:
        print("[DISPLAY]", "\n", "\n".join(lines))
        return
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)
    for i, line in enumerate(lines):
        draw.text((0, i * 10), line, font=font, fill=255)
    oled.image(image)
    oled.show()


def update_display():
    ids = sorted(get_known_devices().keys())
    current_target = ids[get_selected_index()] if ids else "<keine>"
    message_to_send = get_message()
    display_lines([
        f"Ziel: {current_target}",
        f"Meine ID: {get_my_id()}",
        "Letzte Nachricht:",
        get_last_message()[-20:] if get_last_message() else " - ",
        "Nachricht senden:",
        message_to_send[:20] if message_to_send else " - ",
    ])