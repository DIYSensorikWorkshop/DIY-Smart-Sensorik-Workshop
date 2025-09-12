import time
import RPi.GPIO as GPIO
import board, busio
from adafruit_scd4x import SCD4X

#Pins 
LED_ROT   = 22   # warm
LED_GRUEN = 27   # mittel
LED_BLAU  = 17   # kühl
RELAY_PIN = 23   # Relais-IN

TEMP_UNTERGRENZE = 24.0          # °C
TEMP_OBERGRENZE  = 26.0          # °C  → ab 26.0 °C Heizung AUS
CO2_SCHWELLENWERT = 1000         # ppm darüber blinken alle LEDs

# Relais-Typ: False = aktiv-HIGH (HIGH=EIN), True = aktiv-LOW (LOW=EIN)
RELAIS_AKTIV_LOW = True  

def relais_on():
    GPIO.output(RELAY_PIN, GPIO.LOW if RELAIS_AKTIV_LOW else GPIO.HIGH)

def relais_off():
    GPIO.output(RELAY_PIN, GPIO.HIGH if RELAIS_AKTIV_LOW else GPIO.LOW)

def leds(r=0, g=0, b=0):
    GPIO.output(LED_ROT, r); GPIO.output(LED_GRUEN, g); GPIO.output(LED_BLAU, b)

def blink_alle(n=8, an=0.3, aus=0.3):
    for _ in range(n):
        leds(1,1,1); time.sleep(an)
        leds(0,0,0); time.sleep(aus)

def gpio_setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for p in (LED_ROT, LED_GRUEN, LED_BLAU, RELAY_PIN):
        GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)
    leds(0,0,0)
    relais_off()  # sicher AUS (COM+NO verwenden)

# SCD41
def scd41_setup():
    i2c = busio.I2C(board.SCL, board.SDA)
    scd = SCD4X(i2c)
    scd.start_periodic_measurement()
    print("SCD41 gestartet. Warte auf Messwerte …")
    time.sleep(5)
    return scd

# Logik 
def set_heater_by_temp(t):
    
    if t is None:
        relais_off(); return
    if t >= TEMP_OBERGRENZE:
        relais_off();  print("Relais AUS (Heizung aus)")
    else:
        relais_on();   print("Relais AN  (Heizung an)")

def set_temp_leds(t):
    if t is None:
        leds(0,0,0); return
    if t > TEMP_OBERGRENZE:
        leds(1,0,0)       # warm → rot
    elif t >= TEMP_UNTERGRENZE:
        leds(0,1,0)       # mittel → grün
    else:
        leds(0,0,1)       # kühl  → blau

def verarbeite_messung(co2, t):
    if co2 is not None and co2 > CO2_SCHWELLENWERT:
        blink_alle()
    else:
        set_temp_leds(t)
    set_heater_by_temp(t)

# Main 
def main():
    gpio_setup()
    scd = scd41_setup()
    try:
        while True:
            if scd.data_ready:
                co2 = scd.CO2
                t   = scd.temperature
                h   = scd.relative_humidity
                print(f"CO₂: {co2:.0f} ppm | Temperatur: {t:.1f} °C | Luftfeuchte: {h:.1f} %")
                verarbeite_messung(co2, t)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nBeendet mit Strg+C.")
    finally:
        try: scd.stop_periodic_measurement()
        except Exception: pass
        leds(0,0,0); relais_off(); GPIO.cleanup()
        print("Sensor gestoppt. GPIO freigegeben.")

if __name__ == "__main__":
    main()
