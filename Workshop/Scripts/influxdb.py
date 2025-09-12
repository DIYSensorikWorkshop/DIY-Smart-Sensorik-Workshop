import random
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "Token"
org = "Organisation"
url = "http://localhost:8086"
bucket = "Bucket"

# Client erstellen
client = InfluxDBClient(url=url, token=token, org=org)

# Write API vom Client holen
write_api = client.write_api(write_options=SYNCHRONOUS)

# Beispiel-Daten schreiben
while True:
    value = random.uniform(20.0, 30.0)  # z.B. Temperatur zwischen 20 und 30
    point = (
        Point("measurement1")
        .tag("sensor", "sensor-1")
        .field("temperature", value)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    print(f"Gespeichert: {value:.2f}")
    time.sleep(3)  # alle 3 Sekunden