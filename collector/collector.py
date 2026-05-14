import requests
import time
import random
import os

# The internal Dashboard URL inside the cluster.
DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'http://traffic-dashboard-service:80/api/data')
LOCATIONS = ["Main Street", "Highway 1", "Downtown", "North Bridge"]

print(f"Starting Traffic Collector. Sending data to {DASHBOARD_URL}")

while True:
    data = {
        "location": random.choice(LOCATIONS),
        "congestion": random.randint(10, 95)
    }
    try:
        response = requests.post(DASHBOARD_URL, json=data)
        print(f"Sent: {data} - Response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {e}")
    
    time.sleep(5) # Send a reading every 5 seconds.