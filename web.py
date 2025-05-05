from flask import Flask, request, render_template_string
from display import update_display
from variables import set_message

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<title>LoRaCom</title>
<h2>Nachricht senden</h2>
<form method=post>
  <input name=message type=text autofocus>
  <input type=submit value=Senden>
</form>
<p>{{ feedback }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = ""
    if request.method == "POST":
        msg = request.form.get("message", "").strip()
        if msg:
            set_message(msg)
            update_display()
            feedback = "Nachricht gespeichert."
    return render_template_string(HTML_PAGE, feedback=feedback)
