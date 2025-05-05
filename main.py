import os
import threading
import time
import uuid

from flask import Flask, request, render_template_string


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

def load_or_create_id():
    id_file = "kennung.txt"
    if os.path.exists(id_file):
        with open(id_file, "r") as file:
            return file.read().strip()
    new_id = str(uuid.uuid4())[:8]
    with open(id_file, "w") as file:
        file.write(new_id)
    return new_id

known_devices = {}
selected_index = 0
my_id = load_or_create_id()
last_message = ""
message_to_send = ""

def update_known_devices():
    now = time.time()
    device_ids = sorted(known_devices.keys())
    current_target = device_ids[selected_index] if device_ids else "<keine>"
    expired = [k for k, t in known_devices.items() if now - t > 60]
    for k in expired:
        del known_devices[k]
    update_device_list(current_target)

def update_device_list(current_target):
    global selected_index
    device_ids = sorted(known_devices.keys())
    if not device_ids:
        device_ids.append("<keine>")
    if selected_index >= len(device_ids):
        selected_index = 0
    if current_target in device_ids:
        selected_index = device_ids.index(current_target)
    update_display()

def update_display():
    device_ids = sorted(known_devices.keys())
    current_target = device_ids[selected_index] if device_ids else "<keine>"
    lines = [
        f"Ziel: {current_target}",
        f"ID: {my_id}",
        "Letzte Nachricht:",
        last_message[-20:] if last_message else " - ",
        "Nachricht senden:",
        message_to_send if message_to_send else " - ",
    ]
    display_message(lines)

def cleanup_loop():
    while True:
        update_known_devices()
        time.sleep(10)

# ---------------- Flask Web App ---------------- #
app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<title>LoRa-Kommunikator</title>
<h2>Text an Gerät senden</h2>
<form method=post>
  <input type=text name=message autofocus>
  <input type=submit value=Senden>
</form>
<p>{{ feedback }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global message_to_send
    feedback = ""
    if request.method == "POST":
        msg = request.form.get("message", "").strip()
        if msg:
            message_to_send = msg
            update_display()
            feedback = "Nachricht gespeichert."
    return render_template_string(HTML_PAGE, feedback=feedback)

# ---------------- MAIN ---------------- #
if __name__ == '__main__':
    display_message(["Kommunikator bereit."])
    update_known_devices()

    threading.Thread(target=cleanup_loop, daemon=True).start()

    app.run(host="0.0.0.0", port=8080)
