# Explainable Credit Risk Assessment Dashboard 🏦🚀

A production-ready, Dockerized full-stack web application for assessing credit risk and explaining loan approval decisions.

## ✨ Features
- **FastAPI Backend**: High-performance RESTful API serving machine learning predictions.
- **Explainable AI (XAI)**: Understand *why* a decision was made with feature importance and probability metrics.
- **Modern Dashboard**: Premium dark-themed, responsive frontend UI to visualize risk probabilities.
- **Containerized**: Fully Dockerized using Docker Compose for seamless deployment and execution across any environment.
- **Database Integrated**: Local SQLite (or PostgreSQL) integration for persistent data storage and historical inferences.

## 🛠️ Technology Stack
- **Backend:** Python, FastAPI, Scikit-learn, Pandas
- **Frontend:** Vanilla JS, HTML5, Modern CSS (Glassmorphism, Dark Mode)
- **Infrastructure:** Docker, Docker Compose

## 🚀 Quick Start (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - **Frontend:** `http://localhost:80` (or the port specified in docker-compose.yml)
   - **API Docs:** `http://localhost:8000/docs`

## 🧠 Machine Learning Overview
This project takes a standard machine learning model (e.g., Random Forest or Logistic Regression) and elevates it to a robust API endpoint. Model predictions are accompanied by explainability signals to provide transparency in financial decision-making.
