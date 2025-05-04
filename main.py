import threading
import time

import adafruit_ssd1306
import board
import busio
import serial
from PIL import Image, ImageDraw, ImageFont
from bluezero import peripheral

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

def ble_receive(value):
    global last_message
    last_message = value.decode("utf-8")
    update_display()

ble_uart = peripheral.Peripheral(adapter_address=None, local_name='LoRaCom1')
ble_uart.add_service(srv_id=1, uuid="6E400001-B5A3-F393-E0A9-E50E24DCCA9E", primary=True)
ble_uart.add_characteristic(srv_id=1, chr_id=1,
                            uuid="6E400002-B5A3-F393-E0A9-E50E24DCCA9E",
                            value=[], notifying=True,
                            flags=["read", "notify"])
ble_uart.add_characteristic(srv_id=1, chr_id=2,
                            uuid="6E400003-B5A3-F393-E0A9-E50E24DCCA9E",
                            value=[], notifying=False,
                            flags=["write-without-response"],
                            write_callback=ble_receive)

display_message(["Bluetooth ready", "Waiting for messages..."])

threading.Thread(target=ble_uart.run, daemon=True).start()

while True:
    time.sleep(1)
