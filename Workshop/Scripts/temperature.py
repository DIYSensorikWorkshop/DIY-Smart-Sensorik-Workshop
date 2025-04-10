#!/usr/bin/env python3
import random
import time
import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# ### InfluxDB-Verbindungsdetails ###
token = "TOKEN=="
org = "Organisations Name"         # Organisation
url = "http://localhost:8086"      # InfluxDB URL
bucket = "SensorData"              # Name des Buckets

# InfluxDB Client initialisieren
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Sensor-Konfiguration für Temperatur
sensor_id = "Temperature_Sensor"

def generate_temperature_data():
    """
    Generiert einen Zufallswert für die Temperatur.
    Hier erweitern wir den Bereich auf 16-30 °C, um unterschiedliche Zustände zu simulieren.
    """
    temperature = round(random.uniform(16.0, 30.0), 2)
    return {"sensor_id": sensor_id, "temperature": temperature}

if __name__ == '__main__':
    print("Starte Temperatur-Simulation...")
    try:
        while True:
            data = generate_temperature_data()  # Temperatur-Daten generieren
            point = (
                Point("temperature_data")      # Neues Measurement für Temperatur
                .tag("sensor_id", data["sensor_id"])
                .field("temperature", data["temperature"])
            )
            write_api.write(bucket=bucket, org=org, record=point)
            print(f"Gesendet: {data}")
            time.sleep(5)  # Wartezeit 5 Sekunden

    except KeyboardInterrupt:
        print("Simulation beendet.")

# Hinweis:
# Die folgenden Schwellenwerte kannst du in Grafana definieren:
# - Kalt: Temperatur < 18 °C
# - Ideal: 18 °C ≤ Temperatur ≤ 24 °C
# - Warm: 24 °C < Temperatur ≤ 28 °C
# - Zu heiß: Temperatur > 28 °C
