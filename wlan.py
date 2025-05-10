import time
import os
IS_DEBUG = os.getenv("LORACOM_DEBUG", "0") == "1"
if not IS_DEBUG and False:
    import subprocess
    import RPi.GPIO as GPIO
    from display import display_lines

    BUTTON_NEXT = 17
    BUTTON_SELECT = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def scan_networks():
    if IS_DEBUG or True:
        print("WLAN scannen (Debug-Modus)")
        return ["TestNetz1", "TestNetz2"]
    result = subprocess.run(["sudo", "iwlist", "wlan0", "scan"], capture_output=True, text=True)
    essids = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("ESSID"):
            essid = line.split(":")[1].strip('"')
            if essid and essid not in essids:
                essids.append(essid)
    return essids


def connect_to(ssid):
    if IS_DEBUG or True:
        print("Mit WLAN verbinden (Debug-Modus):", ssid)
        return
    subprocess.run(["sudo", "nmcli", "device", "wifi", "connect", ssid], check=False)


def wlan_setup():
    if IS_DEBUG or True:
        print("WLAN-Setup (Debug-Modus)")
        return
    networks = scan_networks()
    if not networks:
        display_lines(["Keine WLANs", "gefunden"])
        time.sleep(3)
        return
    idx = 0
    display_lines(["WLAN auswählen:", networks[idx]])
    while True:
        if GPIO.input(BUTTON_NEXT) == GPIO.LOW:
            idx = (idx + 1) % len(networks)
            display_lines(["WLAN auswählen:", networks[idx]])
            time.sleep(0.3)
        elif GPIO.input(BUTTON_SELECT) == GPIO.LOW:
            display_lines(["Verbinde mit:", networks[idx]])
            connect_to(networks[idx])
            time.sleep(5)
            break
