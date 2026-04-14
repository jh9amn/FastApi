import streamlit as st
import requests

APP_URL = "http://localhost:8000"

st.title("Insurance Premium Prediction")
st.markdown("Enter the details below to predict your insurance premium:")

age = st.number_input("Age", min_value=0, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value = 65.0)
height = st.number_input("Height (m)", min_value=0.5, value=1.75)
income_lpa = st.number_input("Income (LPA)", min_value=0.0, value=10.0)
smoker = st.selectbox("Are you a smoker?", ["Yes", "No"])
city = st.text_input("City", value="New York")
occupation = st.text_input("Occupation",    
                        ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'])

if st.button("Predict Premium"):
    data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    
    try:
        response = requests.post(f"{APP_URL}/predict", json=data)
        result = response.json()

        if response.status_code == 200 and "response" in result:
            prediction = result["response"]
            st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
            st.write("🔍 Confidence:", prediction["confidence"])
            st.write("📊 Class Probabilities:")
            st.json(prediction["class_probabilities"])

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")