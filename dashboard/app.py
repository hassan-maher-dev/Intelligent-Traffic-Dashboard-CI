from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_FILE = os.getenv('DB_FILE', 'traffic.db')

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS traffic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            congestion INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    # جلب آخر 15 قراءة للمرور
    data = conn.execute("SELECT * FROM traffic ORDER BY id DESC LIMIT 15").fetchall()
    conn.close()
    return render_template('index.html', traffic_data=data)

# API for receiving data from the Collector.
@app.route('/api/data', methods=['POST'])
def receive_data():
    req = request.get_json()
    if not req or 'location' not in req or 'congestion' not in req:
        return jsonify({"error": "Invalid data"}), 400

    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO traffic (location, congestion, timestamp) VALUES (?, ?, ?)",
        (req['location'], req['congestion'], datetime.now().strftime("%H:%M:%S"))
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)