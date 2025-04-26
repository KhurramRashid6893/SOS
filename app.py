 
from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

if not os.path.exists('saved_data'):
    os.makedirs('saved_data')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_sos', methods=['POST'])
def send_sos():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    emergency_contact = data.get('emergency_contact', 'Not Provided')

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('saved_data/sos_records.txt', 'a') as file:
        file.write(f"[{timestamp}] Latitude: {latitude}, Longitude: {longitude}, Emergency Contact: {emergency_contact}\n")

    return jsonify({"message": "SOS received successfully!"})

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
