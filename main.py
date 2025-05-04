import asyncio
import threading
import time

import adafruit_ssd1306
import board
import busio
import serial
from PIL import Image, ImageDraw, ImageFont
from dbus.mainloop.glib import DBusGMainLoop
from gi.overrides.GObject import GObject

from gatt_server.gatt_server import Characteristic, Service, Application


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

class RXCharacteristic(Characteristic):
    def __init__(self, service):
        super().__init__("6E400002-B5A3-F393-E0A9-E50E24DCCA9E", ["write", "write-without-response"], service)

    def WriteValue(self, value, options):
        global last_message
        last_message = bytes(value).decode("utf-8")
        update_display()

class UARTService(Service):
    def __init__(self, index):
        super().__init__(index, "6E400001-B5A3-F393-E0A9-E50E24DCCA9E", True)
        self.add_characteristic(RXCharacteristic(self))

DBusGMainLoop(set_as_default=True)
app = Application()
uart_service = UARTService(0)
app.add_service(uart_service)
app.register()

mainloop = GObject.MainLoop()
mainloop.run()
