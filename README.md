# 🚀 Three-Tier Docker Application

## 📌 Overview
A full-stack containerized application built using Docker and Docker Compose, implementing a secure three-tier architecture.

## 🏗 Architecture
- **Frontend**: Nginx (Reverse Proxy)
- **Backend**: Flask API
- **Database**: PostgreSQL (Persistent Storage)

## ⚙️ Features
- User authentication system
- Note-taking dashboard
- Multi-container orchestration using Docker Compose

## 🔐 Security
- Non-root container execution
- Private network between services
- Vulnerability scanning using Trivy
- Multi-stage Docker builds

## ▶️ How to Run

```bash
docker-compose up --build
