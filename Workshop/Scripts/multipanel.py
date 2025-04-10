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

# Sensor-Konfiguration für Multipanel
sensor_id = "MultiPanel_Sensor"

def generate_multi_panel_data():
    """
    Generiert Zufallswerte für Temperatur, CO₂ und Luftfeuchtigkeit.
    Dabei wird auch der Temperaturbereich erweitert, um in Grafana unterschiedliche Panels zu testen.
    """
    temperature = round(random.uniform(16.0, 30.0), 2)
    co2 = round(random.uniform(400.0, 800.0), 2)
    humidity = round(random.uniform(30.0, 60.0), 2)
    
    return {
        "sensor_id": sensor_id,
        "temperature": temperature,
        "co2": co2,
        "humidity": humidity
    }

if __name__ == '__main__':
    print("Starte MultiPanel-Simulation...")
    try:
        while True:
            data = generate_multi_panel_data()  # Sensor-Daten generieren
            # Erstelle ein InfluxDB-Point mit mehreren Feldern
            point = (
                Point("multipanel_data")       # Spezifisches Measurement für Multipanel
                .tag("sensor_id", data["sensor_id"])
                .field("temperature", data["temperature"])
                .field("co2", data["co2"])
                .field("humidity", data["humidity"])
            )
            write_api.write(bucket=bucket, org=org, record=point)
            print(f"Gesendet: {data}")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("Simulation beendet.")
