# LoRaCom – Tragbarer LoRa-Kommunikator

Ein tragbares Kommunikationsgerät mit LoRa, OLED-Display, Tastern und WLAN-Interface.

## 🔧 Verwendete Bauteile

| Bauteil                    | Beschreibung                |
| -------------------------- | --------------------------- |
| Raspberry Pi Zero W        | Zentrale Steuereinheit      |
| RFM9x LoRa-Modul (868 MHz) | Funkmodul für LoRa-Kommunikation |
| SSD1306 OLED (128x64)      | Anzeige über I2C            |
| 2x Taster                  | Navigation                  |
| Widerstände 10kΩ           | Pull-down bei Bedarf        |
| Stromversorgung            | z. B. über Powerbank via Micro-USB |

## ⚙️ GPIO-Verdrahtung

### OLED (SSD1306, I2C)

| OLED-Pin | Raspberry Pi GPIO   |
| -------- | ------------------- |
| VCC      | 3.3V (Pin 1)        |
| GND      | GND (Pin 6)         |
| SCL      | GPIO 3 (SCL, Pin 5) |
| SDA      | GPIO 2 (SDA, Pin 3) |

### RFM9x (LoRa SPI-Modul)

| RFM9x-Pin | Raspberry Pi GPIO    |
| --------- | -------------------- |
| VIN       | 3.3V (Pin 17)        |
| GND       | GND (Pin 9)          |
| SCK       | GPIO 11 (SPI SCLK)   |
| MISO      | GPIO 9 (SPI MISO)    |
| MOSI      | GPIO 10 (SPI MOSI)   |
| CS        | GPIO 8 (CE0, Pin 24) |
| RST       | GPIO 25 (Pin 22)     |

### Taster

| Funktion       | GPIO-Pin (BCM) |
| -------------- | -------------- |
| Weiterblättern | GPIO 17        |
| Auswählen      | GPIO 27        |

> Hinweis: Bei Verwendung ohne Pull-Down-Widerstände bitte `GPIO.PUD_UP` im Code aktivieren (ist bereits integriert).

## 🖥️ Bedienung

* 📱 Verbindung über iPhone-Hotspot oder WLAN
* 📶 LoRa-Geräte erkennen sich durch regelmäßige Broadcasts
* 🖲️ Taster zur Auswahl des Empfängers
* 🖋️ Texteingabe über Weboberfläche: `http://<IP>:8080`

## 🧪 Debug-Modus (Mac-kompatibel)

Zum lokalen Testen auf dem Mac ohne Hardware:

```bash
LORACOM_DEBUG=1 python3 main.py
```

Dadurch werden GPIO, I2C, SPI und WLAN deaktiviert bzw. simuliert.
