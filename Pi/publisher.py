import sys
import serial
import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "sensor/soil"

arduino_port = "/dev/ttyACM0"
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate)

client = mqtt.Client()

if client.connect(BROKER, PORT, 60) != 0:
    print("Couldn't connect to the MQTT broker")
    sys.exit(1)


sensor_value_dry = 455
sensor_value_wet = 186

try:
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            sensor_value, voltage, raw_humidity = line.split(",")
            sensor_value = int(sensor_value)
            voltage = float(voltage)

            humidity_percentage = 100 * (sensor_value_dry - sensor_value) / (se>
            humidity_percentage = max(0, min(100, humidity_percentage))

            message = {
                "sensor_value": sensor_value,
                "voltage": voltage,
                "humidity_percentage": round(humidity_percentage, 2)
            }
            print(f"Publishing: {message} to topic {TOPIC}")
            client.publish(TOPIC, json.dumps(message))
except KeyboardInterrupt:
    print("Exiting...")
finally:
    arduino.close()
    client.disconnect()
