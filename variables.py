my_id = ""
known_devices = {}
selected_index = 0
last_message = ""
message_to_send = ""

def set_message(msg):
    global message_to_send
    message_to_send = msg
    print(f"Nachricht gesetzt: {message_to_send}")

def get_message():
    global message_to_send
    return message_to_send

def set_my_id(id):
    global my_id
    my_id = id
    print(f"ID gesetzt: {my_id}")

def get_my_id():
    global my_id
    return my_id

def set_known_devices(devices):
    global known_devices
    known_devices = devices
    print(f"Bekannte Geräte gesetzt: {known_devices}")

def get_known_devices():
    global known_devices
    return known_devices

def set_selected_index(index):
    global selected_index
    selected_index = index
    print(f"Ausgewählter Index gesetzt: {selected_index}")

def get_selected_index():
    global selected_index
    return selected_index

def set_last_message(msg):
    global last_message
    last_message = msg
    print(f"Letzte Nachricht gesetzt: {last_message}")

def get_last_message():
    global last_message
    return last_message