# Pins für die drei LEDs (nach BCM-Nummern)
LED_ROT   = 22
LED_GRUEN = 27
LED_BLAU  = 17

# Grenzwerte, die ihr bei Bedarf ändern könnt
TEMP_UNTERGRENZE = 25.0  # unterhalb davon: kalt
TEMP_OBERGRENZE  = 26.0    # oberhalb davon: warm
CO2_SCHWELLENWERT_GUT = 1000  #ppm CO₂ Schwellenwert

# Benötigte Bausteine laden: Zeitfunktionen, Hardware-Pins, I²C-Bus, Sensor-Treiber
import time, board, busio, RPi.GPIO as GPIO
from adafruit_scd4x import SCD4X

# Pi-GPIOs vorbereiten und LED-Pins als Ausgänge setzen (starten aus = LOW)
GPIO.setmode(GPIO.BCM)
for p in (LED_ROT, LED_GRUEN, LED_BLAU):
    GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)

# Hilfsfunktion: LEDs gezielt ein- oder ausschalten
def leds(rot=0, gruen=0, blau=0):
    GPIO.output(LED_ROT,   rot)
    GPIO.output(LED_GRUEN, gruen)
    GPIO.output(LED_BLAU,  blau)

# Alle drei LEDs gemeinsam blinken lassen
# zyklen = wie oft, an/aus = Sekunden pro Phase
def blink_alle(zyklen=8, an=0.3, aus=0.3):
    for _ in range(zyklen):
        leds(1, 1, 1); time.sleep(an)
        leds(0, 0, 0); time.sleep(aus)

# Verbindung zum Sensor aufbauen
i2c = busio.I2C(board.SCL, board.SDA)
scd = SCD4X(i2c)
scd.start_periodic_measurement()         # Messung starten
print("SCD41 gestartet. Warte auf Messwerte...")
time.sleep(5)                             # Sensor braucht ein paar Sekunden

try:
    while True:                           # Endlosschleife, läuft bis ihr stoppt
        if scd.data_ready:                # Nur lesen, wenn neue Daten vorliegen
            co2 = scd.CO2
            temperatur = scd.temperature
            luftfeuchte = scd.relative_humidity

            # Zahlen im Terminal anzeigen
            print(f"CO₂: {co2} ppm | Temperatur: {temperatur:.1f} °C | Luftfeuchte: {luftfeuchte:.1f} %")

            # 1) CO₂-Prüfung hat Priorität: zu hoch -> alle LEDs blinken
            if co2 is not None and co2 > CO2_SCHWELLENWERT_GUT:
                blink_alle()
                continue  # danach nächste Runde, Temperatur-LEDs werden übersprungen

            # 2) Sonst Temperatur-Lampe setzen:
            if temperatur is not None and temperatur > TEMP_OBERGRENZE:
                leds(1, 0, 0)   # rot = zu warm
            elif temperatur is not None and temperatur >= TEMP_UNTERGRENZE:
                leds(0, 1, 0)   # grün = im Zielbereich
            elif temperatur is not None:
                leds(0, 0, 1)   # blau = zu kalt
            else:
                leds(0, 0, 0)   # keine Daten

        time.sleep(5)            # alle 5 Sekunden wieder prüfen
except KeyboardInterrupt:        # Strg+C gedrückt
    pass
finally:
    leds(0, 0, 0)                # LEDs aus
    try:
        scd.stop_periodic_measurement()  # Messung sauber stoppen
    except Exception:
        pass
    GPIO.cleanup()               # Pins freigeben
    print("Programm beendet.")