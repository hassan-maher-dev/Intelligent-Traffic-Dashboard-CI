# 🚦 Intelligent Traffic Management Dashboard

This repository contains the source code for the Intelligent Traffic Management system. The project is designed with a microservices approach to monitor and display simulated real-time traffic data.

## 📂 Repository Structure

- **`/dashboard`**: A Flask-based web application that serves as the real-time traffic dashboard. It receives data via an API, stores it in SQLite, and displays congestion levels and traffic status.
- **`/collector`**: A Python script simulating IoT traffic sensors. It generates random traffic data (locations and congestion levels) and sends it to the dashboard continuously.
- **`Jenkinsfile`**: The CI/CD pipeline configuration that builds the Docker images, pushes them to Docker Hub, and automatically updates the GitOps repository.

## 🛠️ Technologies Used
- **Languages/Frameworks:** Python, Flask, HTML/CSS
- **Database:** SQLite
- **Containerization:** Docker
- **CI/CD:** Jenkins

## 🚀 How to Run Locally (For Testing)

You can test the application locally using Docker.

**1. Run the Dashboard:**
```bash
cd dashboard
docker build -t traffic-dashboard .
docker run -d -p 5000:5000 traffic-dashboard

2. Run the Traffic Collector:
(Ensure the dashboard is running first)

Bash
cd collector
docker build -t traffic-collector .
docker run -d --network="host" traffic-collector
Now, open your browser and visit: http://localhost:5000

🔄 CI/CD Workflow
This project uses Jenkins for continuous integration. Upon every push to this repository, Jenkins will:

Build independent Docker images for both the dashboard and collector.

Push the newly built images to Docker Hub with a unique build tag.

Automatically update the Kubernetes deployment manifests in the GitOps repository, triggering ArgoCD to sync and deploy the new changes to the AWS EKS Cluster.