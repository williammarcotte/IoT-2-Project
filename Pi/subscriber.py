from gpiozero import OutputDevice
import paho.mqtt.client as mqtt
import json

RELAY_PIN = 17
BROKER = "localhost"
PORT = 1883
TOPIC = "sensor/soil"
HUMIDITY_MIN = 40
HUMIDITY_MAX = 60

relay = OutputDevice(RELAY_PIN, active_high=False, initial_value=True)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        humidity = payload.get("humidity_percentage")
        if humidity is not None:
            if humidity < HUMIDITY_MIN:
                relay.on()  # Solenoid ON
                print("humidity levels critically low!")
            elif humidity > HUMIDITY_MAX:
                relay.off()  # Solenoid OFF
    except Exception as e:
        print(f"Error: {e}")

def mqtt_subscriber():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_forever()

if __name__ == "__main__":
    try:
        mqtt_subscriber()
    except KeyboardInterrupt:
        pass




