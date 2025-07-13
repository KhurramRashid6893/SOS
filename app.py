  
# from flask import Flask, render_template, request, jsonify
# import os
# from datetime import datetime 

# app = Flask(__name__)

# if not os.path.exists('saved_data'): 
#     os.makedirs('saved_data')

# @app.route('/')
# def home():
#     return render_template('index.html') 

# @app.route('/send_sos', methods=['POST'])
# def send_sos():
#     data = request.get_json()
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
#     emergency_contact = data.get('emergency_contact', 'Not Provided')

#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     with open('saved_data/sos_records.txt', 'a') as file:
#         file.write(f"[{timestamp}] Latitude: {latitude}, Longitude: {longitude}, Emergency Contact: {emergency_contact}\n")

#     return jsonify({"message": "SOS received successfully!"})

# if __name__ == "__main__":
#     #app.run(debug=True)
#     app.run(host="0.0.0.0", port=5000, debug=False)


from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DATABASE = 'sos.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS sos_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                emergency_contact TEXT NOT NULL
            )
        ''')
        conn.commit()

# Call init_db() once at startup
init_db()

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

    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO sos_records (timestamp, latitude, longitude, emergency_contact)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, latitude, longitude, emergency_contact))
        conn.commit()

    return jsonify({"message": "🚨 SOS received and saved successfully!"})

@app.route('/history')
def view_history():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM sos_records ORDER BY id DESC')
        records = c.fetchall()

    return render_template('history.html', records=records)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
