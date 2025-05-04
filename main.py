import asyncio
import threading
import time

import adafruit_ssd1306
import board
import busio
import serial
from PIL import Image, ImageDraw, ImageFont
from bleak import BleakClient


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

async def ble_receive():
    ble_address = "338312FA-C3D1–183F-325A-0726AFDBEB78"
    characteristic_uuid = "15171002-4947-11E9-8646-D663BD873D93"

    async with BleakClient(ble_address) as client:
        data = await client.read_gatt_char(characteristic_uuid)
        print(data)

asyncio.run(ble_receive())

while True:
    time.sleep(1)
