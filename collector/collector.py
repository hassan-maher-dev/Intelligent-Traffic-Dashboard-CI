import requests
import time
import random
import os
import logging

# Dashboard API داخل الـ Kubernetes Cluster
DASHBOARD_URL = os.getenv(
    'DASHBOARD_URL',
    'http://traffic-dashboard-service:80/api/data'
)

LOCATIONS = [
    "Main Street",
    "Highway 1",
    "Downtown",
    "North Bridge"
]

# Logging احترافي
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logging.info(f"Starting Smart Traffic Collector -> {DASHBOARD_URL}")

while True:
    try:
        # اختيار مكان عشوائي
        location = random.choice(LOCATIONS)

        # Traffic Patterns واقعية حسب المنطقة
        if location == "Highway 1":
            congestion = random.randint(50, 75)

        elif location == "Downtown":
            congestion = random.randint(35, 65)

        elif location == "Main Street":
            congestion = random.randint(20, 50)

        else:  # North Bridge
            congestion = random.randint(10, 40)

        # Rare Critical Events (8% فقط)
        if random.random() < 0.08:
            congestion = random.randint(80, 95)

        # البيانات المرسلة
        data = {
            "location": location,
            "congestion": congestion
        }

        # إرسال البيانات للـ Dashboard API
        response = requests.post(
            DASHBOARD_URL,
            json=data,
            timeout=5
        )

        logging.info(
            f"Traffic Sent | "
            f"Location={location} | "
            f"Congestion={congestion}% | "
            f"Status={response.status_code}"
        )

    except requests.exceptions.RequestException as e:
        logging.error(f"Network Error: {e}")

    except Exception as e:
        logging.error(f"Unexpected Error: {e}")

    # إرسال قراءة كل 5 ثواني
    time.sleep(5)