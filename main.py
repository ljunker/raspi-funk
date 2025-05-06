import os
import threading
from display import init_display, display_lines, update_display
from lora import init_lora, listen_lora, broadcast_loop, cleanup_loop
from buttons import handle_buttons
from wlan import wlan_setup
from web import app

IS_DEBUG = os.getenv("LORACOM_DEBUG", "0") == "1"

if __name__ == '__main__':
    init_display()
    display_lines(["WLAN prüfen..."])
    if not IS_DEBUG:
        wlan_setup()
    display_lines(["Kommunikator bereit"])
    update_display()

    init_lora()

    if not IS_DEBUG:
        threading.Thread(target=handle_buttons, daemon=True).start()
        threading.Thread(target=listen_lora, daemon=True).start()
        threading.Thread(target=broadcast_loop, daemon=True).start()
    threading.Thread(target=cleanup_loop, daemon=True).start()

    app.run(host="0.0.0.0", port=8080)