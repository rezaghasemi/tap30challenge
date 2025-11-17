Perfect! Thanks for clarifying. We can simplify the README by **removing the CI/CD and Kubernetes references**, keeping it accurate and clean. Here’s the updated version:

---

# Tapsi Ride Demand Prediction

![Python Version](https://img.shields.io/badge/python-3.10-blue?logo=python\&logoColor=white)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker\&logoColor=white)
![FastAPI](https://img.shields.io/badge/api-FastAPI-009688?logo=fastapi\&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-tracking-blue?logo=mlflow\&logoColor=white)

---

## Project Overview

Tapsi is a ridesharing company in Iran, recording approximately 200 million trips in 2024.
This project predicts taxi demand in Tehran at different times and locations. The city is divided into grid cells, and the model forecasts demand for each cell.

This project demonstrates a **MLOps workflow**, from data ingestion to model deployment via API.

---

## ML Pipeline Components

* **Data Ingestion**: Connects to Cloud Object Storage, retrieves ride data, and stores it locally.
* **Data Processing**: Cleans, transforms, and prepares the dataset for modeling.
* **Model Training**: Trains a Random Forest model using `scikit-learn`.
* **Experiment Tracking**: Uses MLflow to track metrics, parameters, and model versions.
* **API Deployment**: FastAPI exposes the model as a REST API.
* **Containerization**: Docker containerizes the project for reproducibility.

---

## Tools & Technologies

* **Python 3.10**
* **scikit-learn** – Machine learning models
* **FastAPI** – Web API framework
* **MLflow** – Experiment tracking
* **Docker** – Containerization

---

## Getting Started

### Prerequisites

* Python 3.10+
* Docker (optional, for containerized usage)
* MLflow (optional, for experiment tracking)

### Installation

Clone the repository:

```bash
git clone https://github.com/rezaghasemi/tap30challenge.git
cd tap30challenge
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Pipeline

### 1. Data Ingestion

```bash
python scr/data_ingestion.py
```

### 2. Data Processing

```bash
python scr/data_processing.py
```

### 3. Model Training

```bash
python scr/model_trainer.py
```

### 4. Running the API (Locally)

```bash
uvicorn web.app:app --reload
```