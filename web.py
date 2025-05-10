import time

from flask import Flask, request, render_template_string
from display import update_display, display_lines
from lora import send_message
from variables import set_message, set_my_id

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<title>LoRaCom</title>
<h2>Nachricht senden</h2>
<form method=post action="/">
  <input name=message type=text autofocus>
  <input type=submit value=Senden>
</form>
<h2>Kennung setzen</h2>
<form method=post action="/kennung">
  <input name=kennung type=text autofocus>
  <input type=submit value=Setzen>
<p>{{ feedback }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = ""
    if request.method == "POST":
        msg = request.form.get("message", "").strip()
        if msg:
            set_message(msg)
            send_message_with_display(msg)
            update_display()
            feedback = "Nachricht gespeichert."
    return render_template_string(HTML_PAGE, feedback=feedback)

@app.route("/kennung", methods=["POST"])
def set_id():
    feedback = ""
    if request.method == "POST":
        new_id = request.form.get("kennung", "").strip()
        if new_id:
            set_my_id(new_id)
            with open("kennung.txt", "w") as f:
                f.write(new_id)
            feedback = f"Kennung gesetzt: {new_id}"
            update_display()

    return render_template_string(HTML_PAGE, feedback=feedback)

def send_message_with_display(msg):
    # put the message in 20 char blocks:
    blocks = [msg[i:i+20] for i in range(0, len(msg), 20)]
    display_lines(blocks)
    send_message(msg)
    time.sleep(3)