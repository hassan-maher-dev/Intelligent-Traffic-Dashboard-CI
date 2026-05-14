# 🚦 Intelligent Traffic Management Dashboard

A microservices-based system for monitoring and visualizing **simulated real-time traffic data**.

The project demonstrates:

- 📡 Traffic data simulation
- 🌐 Real-time dashboard visualization
- 🐳 Docker containerization
- ⚙️ CI/CD automation with Jenkins
- ☸️ GitOps deployment using ArgoCD & Kubernetes

---

# 📂 Repository Structure

```bash
.
├── dashboard/      # Flask web dashboard
├── collector/      # Traffic sensor simulator
└── Jenkinsfile     # CI/CD pipeline configuration
```

## 📊 dashboard/

A Flask-based web application that:

- Receives traffic data through an API
- Stores data in SQLite
- Displays congestion levels and traffic status in real time

---

## 📡 collector/

A Python-based traffic sensor simulator that:

- Generates random traffic data
- Simulates IoT traffic sensors
- Continuously sends traffic updates to the dashboard

---

## ⚙️ Jenkinsfile

Defines the CI/CD pipeline responsible for:

- Building Docker images
- Pushing images to Docker Hub
- Updating GitOps deployment manifests automatically

---

# 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML / CSS |
| Database | SQLite |
| Containerization | Docker |
| CI/CD | Jenkins |
| GitOps | ArgoCD |
| Orchestration | Kubernetes (EKS) |

---

# 🚀 Running Locally

You can run the project locally using Docker.

---

## 1️⃣ Run the Dashboard

```bash
cd dashboard

docker build -t traffic-dashboard .

docker run -d -p 5000:5000 traffic-dashboard
```

---

## 2️⃣ Run the Traffic Collector

> ⚠️ Make sure the dashboard container is already running.

```bash
cd collector

docker build -t traffic-collector .

docker run -d --network="host" traffic-collector
```

---

# 🌐 Access the Application

Open your browser and visit:

```bash
http://localhost:5000
```

---

# 🔄 CI/CD Workflow

This project uses **Jenkins** for Continuous Integration and Deployment.

## ✅ Pipeline Workflow

Whenever code is pushed to the repository, Jenkins will:

1. Build Docker images for:
   - Traffic Dashboard
   - Traffic Collector

2. Push the images to Docker Hub with unique build tags

3. Automatically update Kubernetes deployment manifests in the GitOps repository

4. Trigger ArgoCD synchronization

5. Deploy the updated application to the AWS EKS cluster

---

# 📦 Deployment Architecture

```text
Collector Service
        │
        ▼
Flask Dashboard API
        │
        ▼
     SQLite
        │
        ▼
 Real-Time Dashboard
```

---

# 👨‍💻 Author

Developed as a DevOps & Microservices project demonstrating:

- Dockerized applications
- Jenkins CI/CD pipelines
- GitOps workflows
- Kubernetes deployments
- Real-time data simulation