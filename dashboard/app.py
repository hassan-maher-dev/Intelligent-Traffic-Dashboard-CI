from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os
import random

app = Flask(__name__)
DB_FILE = os.getenv('DB_FILE', 'traffic.db')

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/traffic')
def traffic_api():
    conn = get_db_connection()
    # Fetch last 15 records
    rows = conn.execute("SELECT * FROM traffic ORDER BY id DESC LIMIT 15").fetchall()
    
    # Calculate KPIs
    total_roads = conn.execute("SELECT COUNT(DISTINCT location) FROM traffic").fetchone()[0] or 0
    avg_congestion = conn.execute("SELECT AVG(congestion) FROM traffic").fetchone()[0] or 0
    critical_zones = conn.execute("SELECT COUNT(*) FROM traffic WHERE congestion > 80").fetchone()[0] or 0
    
    conn.close()
    
    # Mock Infrastructure Metrics for Enterprise Feeling
    mock_latency = f"{random.randint(20, 65)}ms"
    
    return jsonify({
        "traffic_data": [dict(row) for row in rows],
        "stats": {
            "total_roads": total_roads,
            "avg_congestion": round(avg_congestion, 1),
            "critical_zones": critical_zones,
        },
        "infra": {
            "api_latency": mock_latency,
            "collector_status": "Online",
            "db_health": "Healthy",
            "uptime": "99.98%"
        }
    })

@app.route('/api/data', methods=['POST'])
def receive_data():
    req = request.get_json()
    if not req or 'location' not in req or 'congestion' not in req:
        return jsonify({"error": "Invalid data"}), 400

    conn = get_db_connection()
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