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

# Konfiguration für den Sensor
sensor_id = "Sensor_1"

def generate_sensor_data():
    """
    Generiert realistischere Zufallswerte für Temperatur (18-26 °C),
    CO₂ (400-800 ppm) und Luftfeuchtigkeit (30-60%).
    """
    temperature = round(random.uniform(18.0, 26.0), 2)
    co2 = round(random.uniform(400.0, 800.0), 2)
    humidity = round(random.uniform(30.0, 60.0), 2)

    return {
        "sensor_id": sensor_id,
        "temperature": temperature,
        "co2": co2,
        "humidity": humidity
    }

if __name__ == '__main__':
    print("Starte Sensor-Datenstrom-Simulation...")
    try:
        while True:
            data = generate_sensor_data()  # Sensor-Daten generieren
            
            # Erstelle ein InfluxDB-Point mit mehreren Feldern
            point = (
                Point("sensor_data")          # Name des Measurements
                .tag("sensor_id", data["sensor_id"])
                .field("temperature", data["temperature"])
                .field("co2", data["co2"])
                .field("humidity", data["humidity"])
            )

            # Schreibe die Daten in InfluxDB
            write_api.write(bucket=bucket, org=org, record=point)

            # Ausgabe in der Konsole
            print(f"Gesendet: {data}")

            # Wartezeit (z. B. 5 Sekunden)
            time.sleep(5)

    except KeyboardInterrupt:
        print("Simulation beendet.")
