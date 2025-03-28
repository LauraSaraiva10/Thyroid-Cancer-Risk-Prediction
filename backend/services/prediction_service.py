import os
import joblib
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.pipeline import Pipeline as Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

logging.basicConfig(level=logging.INFO)

MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")


def make_prediction(data: pd.DataFrame) -> int:
    # Load or train the model if not found
    model, encoder = __load_or_train_model()

    # Encode categorical features in data
    data_encoded = __encode_data(data, encoder)

    # Standardize the data and make prediction
    prediction = model.predict(data_encoded)

    print("Prediction: " + str(prediction[0]))

    return int(prediction[0])


def __load_or_train_model():
    if not os.path.exists(MODEL_PATH):
        logging.info("Model not found. Training the model...")
        __train_and_save_model()
    else:
        logging.info("Loading existing model...")
    return __load_model()


def __load_model():
    try:
        model = joblib.load(MODEL_PATH)
        encoder_dict = joblib.load(ENCODER_PATH)
        logging.info("Model and encoder loaded successfully.")
        return model, encoder_dict
    except FileNotFoundError as e:
        logging.error(f"Error loading model or encoder: {e}")
        raise


def __encode_data(data: pd.DataFrame, encoder_dict: dict) -> pd.DataFrame:
    categorical_columns = data.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if col in encoder_dict:
            data[col] = encoder_dict[col].transform(data[col])
        else:
            print(f"Warning: No encoder found for column {col}")
    return data


def __train_and_save_model():
    # Load dataset
    df = pd.read_csv('data/thyroid_cancer_risk_data.csv')

    # Drop unnecessary columns
    df.drop(columns=['Patient_ID', 'Country', 'Ethnicity'], inplace=True)

    # Encode categorical variables using LabelEncoder
    encoder_dict = {}
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
        encoder_dict[col] = encoder

    # Define features and target
    X = df.drop(columns=['Diagnosis'])
    y = df['Diagnosis']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # Define pipeline with StandardScaler, SMOTE, and XGBoost
    pipeline = Pipeline([
        ('scaler', StandardScaler()),      # Standardizing features
        ('smote', SMOTE(random_state=42)),  # Handling class imbalance
        ('classifier', XGBClassifier(random_state=42))  # XGBoost model
    ])

    # Train pipeline
    pipeline.fit(X_train, y_train)

    # Ensure the model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Save the trained model and encoder
    joblib.dump(pipeline, MODEL_PATH)
    joblib.dump(encoder_dict, ENCODER_PATH)
    logging.info("Model and encoder saved successfully.")