import os

from flask import Flask, render_template, jsonify, Response
import threading
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
import json

from auth import auth_bp
from auth.routes import login_manager
from controllers.mainController import main_bp

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(main_bp, url_prefix="/")
app.secret_key = os.urandom(24)

login_manager.init_app(app)

BROKER = "raspberrypi.local"
PORT = 1883
TOPIC = "sensor/soil"

latest_data = {"sensor_value": None, "voltage": None, "humidity_percentage": None}

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client.greenify_db
collection = db.humidity_readings

# send data  to mongodb
def on_message(client, userdata, msg):
    global latest_data
    payload = msg.payload.decode()
    try:
        data = eval(payload)
        latest_data.update(data)

        document = {
            "sensor_value": data.get("sensor_value"),
            "voltage": data.get("voltage"),
            "humidity_percentage": data.get("humidity_percentage"),
            "recorded_at": datetime.now()
        }
        collection.insert_one(document)
        print(f"Updated latest_data: {latest_data}")
    except Exception as e:
        print(f"Error: {e}")


def mqtt_thread():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.subscribe(TOPIC)
    client.loop_forever()

# start mqtt
threading.Thread(target=mqtt_thread, daemon=True).start()

#stream with sse for live humidity
@app.route('/stream')
def stream():
    def event_stream():
        previous_data = None
        while True:
            if previous_data != latest_data:
                yield f"data: {json.dumps(latest_data)}\n\n"
                previous_data = latest_data
    return Response(event_stream(), content_type='text/event-stream')

#retrieve data from mongodb
@app.route('/api/humidity_data')
def get_humidity_data():
    try:
        data = list(collection.find({}, {"_id": 0, "humidity_percentage": 1, "recorded_at": 1}).sort("recorded_at", 1))

        formatted_data = {
            "timestamps": [doc["recorded_at"].strftime('%Y-%m-%d %H:%M:%S') for doc in data],
            "humidity": [doc["humidity_percentage"] for doc in data]
        }
        return jsonify(formatted_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
