# Hier fügen wir alle nötigen Bibliotheken ein
import time
import board
import busio
from adafruit_scd4x import SCD4X

# Mit diesem Code wird die I²C-Schnittstelle des Raspberry Pi initialisiert
i2c = busio.I2C(board.SCL, board.SDA)

# Hier starten wir den SCD41-Sensor
scd41 = SCD4X(i2c)
scd41.start_periodic_measurement()
print("SCD41-Sensor gestartet. Warte auf erste Messwerte...")

# Der Sensor liefert alle 5 Sekunden neue Werte
time.sleep(5)

try:
    while True:  # Solange der Prozess nicht abgebrochen wird führt der Raspberry folgenden Schleife immer wieder aus.
        if scd41.data_ready:  # Hier wird geprüft, ob neue Messwerte verfügbar sind
            co2 = scd41.CO2       # CO2 in PPM
            temperature = scd41.temperature  # Temperatur in °C
            humidity = scd41.relative_humidity  # Luftfeuchtigkeit in %

            # Messwerte im Terminal ausgeben
            print(f"CO₂: {co2} ppm | Temperatur: {temperature:.1f} °C | Luftfeuchtigkeit: {humidity:.1f} %")
        else:
            print("Warte auf neue Sensordaten...")

        time.sleep(5)  # Alle 5 Sekunden neue Messwerte abrufen
except KeyboardInterrupt:
    # Falls du eine Taste drückst wird der Prozess abgebrochen.
    print("\nProgramm beendet. Sensor gestoppt.")