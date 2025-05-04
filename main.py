import threading
import time

import adafruit_ssd1306
import board
import busio
import serial
from PIL import Image, ImageDraw, ImageFont

#i2c = busio.I2C(board.SCL, board.SDA)
#oled_width = 128
#oled_height = 64
#oled = adafruit_ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#image = Image.new("1", (oled_width, oled_height))
#draw = ImageDraw.Draw(image)
#font = ImageFont.load_default()

#def display_message(lines):
#    draw.rectangle((0, 0, oled_width, oled_height), outline=0, fill=0)
#    for i, line in enumerate(lines):
#        draw.text((0, i * 10), line, font=font, fill=255)
#    oled.image(image)
#    oled.show()

def display_message(lines):
    # Placeholder function for displaying messages
    print("\n".join(lines))

bluetooth_connected = False
while not bluetooth_connected:
    try:
        bluetooth_serial = serial.Serial('/dev/rfcomm0', baudrate=9600, timeout=1)
        bluetooth_connected = True
    except serial.SerialException:
        display_message(["Connecting to Bluetooth...", "Retrying..."])
        time.sleep(1)

display_message(["Bluetooth connected!", "Ready to receive data."])

device_ids = ["Alpha", "Bravo", "Charlie"]
selected_index = 0
my_id = "Delta"
last_message = ""

def update_display():
    lines = [
        f"Ziel: {device_ids[selected_index]}",
        f"ID: {my_id}",
        "Letzte Nachricht:",
        last_message[-20:] if last_message else " - ",
    ]
    display_message(lines)

def listen_bluetooth():
    global last_message
    while True:
        if bluetooth_serial.in_waiting:
            msg = bluetooth_serial.readline().decode('utf-8').strip()
            if msg:
                last_message = msg
                update_display()

threading.Thread(target=listen_bluetooth, daemon=True).start()

while True:
    time.sleep(1)
