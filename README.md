# Greenify: IoT 2 Final Project

**Course**: IoT 2, Champlain College St-Lambert
**Professor**: Haikel Hichri  
**Project Name**: Greenify  
**Author**: William Marcotte 

---

## **Project Overview**
Greenify is an innovative soil moisture monitoring system designed to optimize plant health by providing real-time data, notifications, and historical insights. This project integrates hardware and software solutions to create an efficient and user-friendly experience for monitoring soil conditions.

---

## **Features**
- **Real-Time Data**:
  - Collects and displays live soil moisture data from sensors.
  - Streams data to a web interface using Server-Sent Events (SSE).
- **Notifications**:
  - Alerts when soil moisture falls below critical thresholds.
  - Ensures plants are watered on time.
- **Historical Data**:
  - Stores sensor data in MongoDB for long-term analysis.
  - Visualizes trends with an interactive graph.
- **Offline Functionality**:
  - Stores data locally in SQLite when offline.
  - Syncs to MongoDB when the system reconnects.
- **User Customization**:
  - Allows users to set minimum and maximum soil moisture thresholds.

---

## **Technology Stack**
### **Hardware**
- **Raspberry Pi**:
  - Runs the MQTT subscriber and temporary storage system.
  - Interfaces with soil moisture sensors.
- **Sensors**:
  - Measure soil moisture levels and publish data.

### **Software**
- **Flask**:
  - Hosts the web interface and API endpoints.
- **MongoDB**:
  - Stores historical data for analysis.
- **SQLite**:
  - Acts as a local offline buffer for temporary data storage.
- **Chart.js**:
  - Displays interactive visualizations for historical data trends.
- **MQTT**:
  - Facilitates communication between sensors and the system.

---

## **System Architecture**
1. **Sensors**:
   - Measure soil moisture and send data to the Raspberry Pi.
2. **Raspberry Pi**:
   - Publishes data to the MQTT broker.
   - Temporarily stores data in SQLite during offline periods.
3. **Web App**:
   - Streams live data and provides visualizations for historical data.
   - Hosts user settings and notification alerts.
4. **MongoDB**:
   - Stores synchronized sensor readings for long-term storage.

---

## **Endpoints**
### **Web Interface**
- `/`: Displays live sensor data.
- `/stream`: Streams real-time data updates to the browser.
- `/settings`: Allows users to configure minimum and maximum soil moisture levels.
- `/notifications`: Displays alerts for critical soil moisture levels.

### **API**
- `/api/humidity_data`: Returns historical humidity data in JSON format.

---

## **Setup Instructions**
1. **Hardware Setup**:
   - Connect soil moisture sensors to the Raspberry Pi.
   - Ensure the Raspberry Pi is connected to the same network as your PC.

2. **Software Installation**:
   - Clone this repository:
     ```bash
     git clone [repository_url]
     ```
   - Install required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Start the Flask app:
     ```bash
     python app.py
     ```

3. **Database Setup**:
   - Ensure MongoDB is running locally or on a server.
   - Configure MongoDB connection details in `app.py`.

4. **Run the Project**:
   - Start the MQTT subscriber on the Raspberry Pi.
   - Access the web app at `http://<your-server-ip>:5000`.
---
Project Demo can be found here:
https://www.youtube.com/watch?v=yU7lL_g5PbA
---

## **Acknowledgments**
Special thanks to Professor Haikel Hichri for guiding us through the IoT 2 course and enabling this project.
