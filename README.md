# 🏥 Thyroid Cancer Risk Prediction

## Overview
The Thyroid Cancer Risk Prediction App is a full-stack machine learning application designed to classify thyroid cancer cases as malignant or benign. It consists of a FastAPI backend that handles model inference and database management, and a Streamlit frontend that provides a user-friendly interface for interacting with the application. The entire app is containerized using Docker to ensure easy deployment and scalability.

## 📁 Project Structure
```
thyroid-cancer-risk-prediction/
├── backend/
│   ├── data/
│   │   └── thyroid_cancer_risk_data.csv  # Contains training data
│   ├── database/
│   │   └── database.py  # Manages database connections
│   ├── migrations/
│   │   ├── versions/  # Keeps track of database changes
│   │   ├── env.py
│   │   ├── README
│   │   └── script.py.mako
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py  # Base class for models
│   │   └── thyroid_cancer_data.py  # Defines data model
│   ├── routers/
│   │   └── prediction.py  # Handles prediction requests
│   ├── saved_models/  # Stores trained models and encoders
│   │   ├── encoder.pkl
│   │   └── model.pkl
│   ├── schemas/
│   │   └── prediction.py  # Defines input/output schemas
│   ├── services/
│   │   └── prediction_service.py  # Logic for making predictions
│   ├── .dockerignore
│   ├── alembic.ini
│   ├── app.py  # Main backend application
│   ├── Dockerfile  # Defines backend container
│   └── requirements.txt  # Backend dependencies
├── frontend/
│   ├── Dockerfile  # Defines frontend container
│   ├── frontend.py  # Streamlit app for user interaction
│   └── requirements.txt  # Frontend dependencies
├── images/  # Sample results
│   ├── test_benign.png
│   └── test_malignant.png
├── .env
├── .gitignore
├── docker-compose.yml  # Manages both backend and frontend containers
```

## 🚀 Running the Project

### Local Setup

To run this project locally, follow these steps:

**1. Set up PostgreSQL Database**
- Create a PostgreSQL database named `ThyroidCancerRisk`.

**2. Set up the .env file**

Before running the application, create a .env file in the root directory of the project and define the following environment variables:
```
DATABASE_URL=postgresql://postgres:your_password_here@localhost:5432/ThyroidCancerRisk
API_URL=http://localhost:9999
```
- **DATABASE_URL:** The connection string to your PostgreSQL database, including the username (postgres),
password (your_password_here), and database name (ThyroidCancerRisk).

- **API_URL:** The URL where the FastAPI backend will be running.

**3. Install dependencies**
```
pip install -r requirements.txt
```

**4. Apply Database Migrations**
```
alembic upgrade head
```

**5. Start the Backend**
```
cd backend
uvicorn app:app --reload --port 9999
```

**6. Start the Frontend**
```
cd frontend
streamlit run frontend.py
```

### 🐳 Running with Docker (Recommended)

To run the entire application with Docker, which simplifies the process of launching both the backend and frontend, execute:
```
docker-compose up
```
This will start both the backend API service and the frontend user interface in separate containers.

### 🎯 How It Works

On the first execution, the application will train a new model and save the necessary files (model.pkl and encoder.pkl) in the saved_models directory. This process may take some time.

On subsequent runs, the application will load the saved model for faster predictions.

The Streamlit frontend provides an interactive interface where users can input data related to thyroid cancer, such as medical features or test results. After submitting the data, the application instantly processes it through the machine learning model and delivers a real-time prediction, indicating whether the cancer is malignant or benign.

### 📊 Sample Predictions
Below are some examples of predictions made by the application:

**🩺 Benign Case**

<img src="images/test_benign.png" alt="Benign Prediction" width="700"/>

</br>

**⚠️ Malignant Case**

<img src="images/test_malignant.png" alt="Malignant Prediction" width="700"/>

### 🛠️ Technologies Used

- **Backend:** FastAPI, PostgreSQL, SQLAlchemy, Alembic, Scikit-Learn, Uvicorn

- **Frontend:** Streamlit

- **Containerization:** Docker, Docker Compose