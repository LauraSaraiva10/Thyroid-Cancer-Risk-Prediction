import streamlit as st
import requests
import pandas as pd
import dotenv
import os

dotenv.load_dotenv()

api_url = os.getenv('API_URL')

st.set_page_config(
    page_title="Thyroid Cancer Type Predictor",
    page_icon="🦠",
    layout="wide"
)

st.title("🦠 Thyroid Cancer Type Predictor")
st.write("Use this tool to assess whether your thyroid cancer is benign or malignant based on health and lifestyle factors.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Enter Your Health Data")

    age = st.slider("**Age**", min_value=0, max_value=120, value=30, step=1)

    col_gender, col_family_history = st.columns(2)

    with col_gender:
        gender = st.radio("**Gender**", ["Male", "Female"])

    with col_family_history:
        family_history = st.radio("**Family History of Thyroid Cancer**", ["Yes", "No"])

    col_radiation, col_iodine = st.columns(2)

    with col_radiation:
        radiation_exposure = st.radio("**History of Radiation Exposure**", ["Yes", "No"])

    with col_iodine:
        iodine_deficiency = st.radio("**Iodine Deficiency**", ["Yes", "No"])

    col_smoking, col_obesity = st.columns(2)

    with col_smoking:
        smoking = st.radio("**Smoking**", ["Yes", "No"])

    with col_obesity:
        obesity = st.radio("**Obesity**", ["Yes", "No"])

    diabetes = st.radio("**Diabetes**", ["Yes", "No"])

    tsh_level = st.number_input("**TSH Level (µIU/mL)**", min_value=0.1, value=2.5, max_value=10.0, step=0.1)

    t3_level = st.number_input("**T3 Level (ng/dL)**", min_value=0.5, value=1.0, max_value=3.5, step=0.1)

    t4_level = st.number_input("**T4 Level (µg/dL)**", min_value=4.5, value=5.0, max_value=12.0, step=0.1)

    nodule_size = st.number_input("**Nodule Size (cm)**", min_value=0.0, value=1.0, max_value=5.0, step=0.1)

    thyroid_cancer_risk = st.selectbox("**Thyroid Cancer Risk**", ["Low", "Medium", "High"])

    if st.button("🔮 Predict Risk"):
        data = {
            "age": age,
            "gender": gender,
            "family_history": family_history,
            "radiation_exposure": radiation_exposure,
            "iodine_deficiency": iodine_deficiency,
            "smoking": smoking,
            "obesity": obesity,
            "diabetes": diabetes,
            "tsh_level": tsh_level,
            "t3_level": t3_level,
            "t4_level": t4_level,
            "nodule_size": nodule_size,
            "thyroid_cancer_risk": thyroid_cancer_risk
        }

        try:
            response = requests.post(f"{api_url}/predict", json=data)

            if response.status_code == 200:
                prediction = response.json()['prediction']

                if prediction == "Benign":
                    st.success(f"Prediction: 🟢 **Benign**")
                else:
                    st.error(f"Prediction: 🔴 **Malignant**")
            else:
                st.error("Error making the prediction. Please try again!")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the prediction service. Is the backend server running?")

with col2:
    st.subheader("📜 Recent Predictions")

    try:
        response = requests.get(f"{api_url}/predict/history")
        if response.status_code == 200:
            history = response.json()
            if history:
                df = pd.DataFrame(history)
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M')
                st.dataframe(
                    df[['created_at', 'age', 'gender', 'family_history', 'radiation_exposure', 'iodine_deficiency',
                        'smoking', 'obesity', 'diabetes', 'tsh_level', 't3_level', 't4_level', 'nodule_size', 'prediction']])
            else:
                st.info("No prediction history available yet.")
        else:
            st.error("Error fetching prediction history.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the prediction service. Is the backend server running?")