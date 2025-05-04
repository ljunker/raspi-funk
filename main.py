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
    global last_message
    feedback = ""
    if request.method == "POST":
        msg = request.form.get("message", "").strip()
        if msg:
            last_message = msg
            update_display()
            feedback = "Nachricht gespeichert."
    return render_template_string(HTML_PAGE, feedback=feedback)

# ---------------- MAIN ---------------- #
if __name__ == '__main__':
    display_message(["Kommunikator bereit."])

    app.run(host="0.0.0.0", port=8080)
