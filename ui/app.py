import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"   # calls internal API in same space
# API_URL = "https://abhi20033-houseprice-mlops.hf.space/predict"

st.title("Bengaluru House Price Predictor (CI/CD)")

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

if st.button("Predict Price per Sqft"):
    data = {
        "area": area,
        "rent": rent,
        "locality": locality,
        "BHK": bhk,
        "facing": facing,
        "bathrooms": bathrooms,
        "parking": parking
    }
    r = requests.post(API_URL, json=data)
    if r.status_code == 200:
        pred = r.json()['prediction']
        st.success(f"Predicted price per sqft: ₹{pred:,.2f}")
    else:
        st.error("Error getting prediction")
