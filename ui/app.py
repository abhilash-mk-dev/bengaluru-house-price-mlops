# import streamlit as st
# import requests

# API_URL = "http://localhost:8000/predict"   # calls internal API in same space
# # API_URL = "https://abhi20033-houseprice-mlops.hf.space/predict"

# st.title("Bengaluru House Price Predictor (CI/CD)")

# locality = st.selectbox("Locality", [
#     "Attibele", "BTM Layout", "Electronic City", "Indiranagar",
#     "Jayanagar", "K R Puram", "Malleshwaram", "Marathahalli", "Yalahanka"
# ])

# area = st.slider("Area (sq ft)", 200, 5000, 565)
# rent = st.slider("Monthly Rent (₹)", 5000, 200000, 20060, step=500)
# bhk = st.slider("BHK", 1, 5, 1)
# bathrooms = st.slider("Bathrooms", 1, 10, 1)
# facing = st.selectbox("Facing", ["East","North","North-East","North-West","South","South-East","West"])
# parking = st.selectbox("Parking", ["Bike", "Car", "Bike and Car"])

# if st.button("Predict Price per Sqft"):
#     data = {
#         "area": area,
#         "rent": rent,
#         "locality": locality,
#         "BHK": bhk,
#         "facing": facing,
#         "bathrooms": bathrooms,
#         "parking": parking
#     }
#     r = requests.post(API_URL, json=data)
#     if r.status_code == 200:
#         pred = r.json()['prediction']
#         st.success(f"Predicted price per sqft: ₹{pred:,.2f}")
#     else:
#         st.error("Error getting prediction")


import streamlit as st
import requests
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

# ====================================
# Setup
# ====================================
API_URL = "http://localhost:8000/predict"  # internal API in same space
# API_URL = "https://abhi20033-houseprice-mlops.hf.space/predict"

st.title("🏠 Bengaluru House Price Predictor (CI/CD)")

# ====================================
# Initialize session state for tracking performance
# ====================================
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "Locality", "Predicted", "Expected", "Error"
    ])

# ====================================
# Input section
# ====================================
st.header("Enter Property Details")

locality = st.selectbox("Locality", [
    "Attibele", "BTM Layout", "Electronic City", "Indiranagar",
    "Jayanagar", "K R Puram", "Malleshwaram", "Marathahalli", "Yalahanka"
])

area = st.slider("Area (sq ft)", 200, 5000, 565)
rent = st.slider("Monthly Rent (₹)", 5000, 200000, 20060, step=500)
bhk = st.slider("BHK", 1, 5, 1)
bathrooms = st.slider("Bathrooms", 1, 10, 1)
facing = st.selectbox("Facing", ["East","North","North-East","North-West","South","South-East","West"])
parking = st.selectbox("Parking", ["Bike", "Car", "Bike and Car"])

expected_price = st.number_input("Expected Price per sqft (₹)", min_value=0.0, step=100.0, value=6000.0)

# ====================================
# Prediction button
# ====================================
if st.button("Predict and Compare"):
    data = {
        "area": area,
        "rent": rent,
        "locality": locality,
        "BHK": bhk,
        "facing": facing,
        "bathrooms": bathrooms,
        "parking": parking
    }

    try:
        r = requests.post(API_URL, json=data)
        if r.status_code == 200:
            pred = float(r.json()['prediction'])
            st.success(f"Predicted price per sqft: ₹{pred:,.2f}")

            # Record and compute error
            err = expected_price - pred
            st.session_state.history.loc[len(st.session_state.history)] = {
                "Locality": locality,
                "Predicted": pred,
                "Expected": expected_price,
                "Error": err
            }

        else:
            st.error("Error getting prediction")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")

# ====================================
# Performance Metrics
# ====================================
if len(st.session_state.history) > 0:
    st.header("📈 Model Performance (User Feedback)")

    df = st.session_state.history

    # Calculate RMSE and R²
    rmse = np.sqrt(mean_squared_error(df["Expected"], df["Predicted"]))
    r2 = r2_score(df["Expected"], df["Predicted"])

    st.metric("RMSE", f"{rmse:,.2f}")
    st.metric("R² Score", f"{r2:.4f}")

    # Show history table
    st.dataframe(df, use_container_width=True)

    # Optionally plot performance
    st.line_chart(df[["Expected", "Predicted"]])

    # Option to clear session data
    if st.button("Reset Performance Data"):
        st.session_state.history = pd.DataFrame(columns=[
            "Locality", "Predicted", "Expected", "Error"
        ])
        st.success("Performance data reset successfully.")

else:
    st.info("👋 Enter values and expected price to begin tracking performance.")
