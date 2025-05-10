import os
import time
import uuid
from display import update_display
from variables import set_my_id, get_my_id, get_known_devices, set_last_message, get_selected_index, set_selected_index

IS_DEBUG = os.getenv("LORACOM_DEBUG", "0") == "1"
if not IS_DEBUG and False:
    import board
    import busio
    import digitalio
    import adafruit_rfm9x

rfm9x = None

def init_lora():
    global rfm9x

    id_file = "kennung.txt"
    if os.path.exists(id_file):
        with open(id_file, "r") as f:
            set_my_id(f.read().strip())
    else:
        set_my_id("DEV-" + str(uuid.uuid4())[:8])
        with open(id_file, "w") as f:
            f.write(get_my_id())
    if IS_DEBUG or True:
        print("LoRa initialisieren (Debug-Modus)")
        return
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D8)
    reset = digitalio.DigitalInOut(board.D25)
    rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 868)


def send_message(msg):
    ids = sorted(get_known_devices().keys())
    if not msg or not ids:
        return
    target = ids[get_selected_index()]
    packet = f"{target}|{get_my_id()}|{msg}"
    if IS_DEBUG or True:
        print("LoRa senden (Debug-Modus):", packet)
        return
    rfm9x.send(packet.encode("utf-8"))
    print("Gesendet:", packet)


def listen_lora():
    if IS_DEBUG or True:
        print("LoRa empfangen (Debug-Modus)")
        return
    while True:
        packet = rfm9x.receive(timeout=5.0)
        if packet:
            try:
                decoded = packet.decode("utf-8")
                to_id, from_id, msg = decoded.split("|", 2)
                if to_id == "BROADCAST":
                    get_known_devices()[from_id] = time.time()
                elif to_id == get_my_id():
                    get_known_devices()[from_id] = time.time()
                    set_last_message(f"{from_id}: {msg}")
                    update_display()
            except Exception as e:
                print("Fehler beim Empfangen:", e)


def broadcast_loop():
    if IS_DEBUG or True:
        print("LoRa Broadcast (Debug-Modus)")
        return
    while True:
        rfm9x.send(f"BROADCAST|{get_my_id()}|ping".encode("utf-8"))
        time.sleep(10)

def update_known_devices():
    now = time.time()
    device_ids = sorted(get_known_devices().keys())
    old_length = len(device_ids)
    current_target = device_ids[get_selected_index()] if device_ids else "<keine>"
    expired = [k for k, t in get_known_devices().items() if now - t > 60]
    for k in expired:
        del get_known_devices()[k]
    if len(get_known_devices()) != old_length:
        update_device_list(current_target)

def update_device_list(current_target):
    device_ids = sorted(get_known_devices().keys())
    if not device_ids:
        device_ids.append("<keine>")
    if get_selected_index() >= len(device_ids):
        set_selected_index(0)
    if current_target in device_ids:
        set_selected_index(device_ids.index(current_target))
    update_display()

def cleanup_loop():
    while True:
        update_known_devices()
        time.sleep(5)
