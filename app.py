from flask import Flask, render_template, jsonify
import threading
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime

from controllers.mainController import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp, url_prefix='/')

BROKER = "raspberrypi.local"
PORT = 1883
TOPIC = "sensor/soil"

latest_data = {"sensor_value": None, "voltage": None, "humidity_percentage": None}

# MongoDB Configuration
mongo_client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB server address
db = mongo_client.greenify_db
collection = db.humidity_readings


def on_message(client, userdata, msg):
    global latest_data
    payload = msg.payload.decode()
    try:
        # Parse MQTT payload
        data = eval(payload)
        latest_data = data

        # Add timestamp and insert into MongoDB
        document = {
            "sensor_value": data.get("sensor_value"),
            "voltage": data.get("voltage"),
            "humidity_percentage": data.get("humidity_percentage"),
            "recorded_at": datetime.now()
        }
        collection.insert_one(document)
        print(f"Inserted into MongoDB: {document}")
    except Exception as e:
        print(f"Failed to parse or insert message: {payload}. Error: {e}")


def mqtt_thread():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_forever()


threading.Thread(target=mqtt_thread, daemon=True).start()


@app.route('/')
def home():
    return render_template('home.html', data=latest_data)


@app.route('/api/data')
def api_data():
    return jsonify(latest_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
