import streamlit as st
import requests
import json

# إعدادات الصفحة
st.set_page_config(page_title="House Price Predictor", page_icon="🏡", layout="centered")
st.title("🏡 House Price Prediction App")
st.write("Enter the property details below to get an estimated price.")

# تحميل ملف الأماكن
try:
    with open("locations.json", "r") as f:
        locations = json.load(f)
except FileNotFoundError:
    st.error("Error: 'locations.json' not found. Please ensure it's in the same directory.")
    locations = ["other"]

# واجهة إدخال البيانات
col1, col2 = st.columns(2)

with col1:
    area = st.number_input("Carpet Area (sqft)", min_value=100.0, value=1200.0, step=50.0)
    floor = st.number_input("Floor Number", min_value=1.0, value=3.0, step=1.0)
    bathrooms = st.number_input("Number of Bathrooms", min_value=1.0, value=2.0, step=1.0)
    balcony = st.number_input("Number of Balconies", min_value=0.0, value=1.0, step=1.0)
    loc = st.selectbox("Location", locations)

with col2:
    furnishing = st.selectbox("Furnishing Status", ["Unfurnished", "Semi-Furnished", "Furnished"])
    transaction = st.selectbox("Transaction Type", ["Resale", "New Property"])
    ownership = st.selectbox("Ownership Type", ["Freehold", "Leasehold", "Co-operative Society", "Power of Attorney"])
    facing = st.selectbox("Facing Direction", ["East", "West", "North", "South", "North-East", "North-West", "South-East", "South-West"])

# زرار التوقع
if st.button("Predict Price 🚀", use_container_width=True):
    # تجميع البيانات
    payload = {
        "carpet_area_sqft": area,
        "floor_num": floor,
        "Bathroom": bathrooms,
        "Balcony": balcony,
        "location_grouped": loc,
        "Furnishing": furnishing,
        "Transaction": transaction,
        "Ownership": ownership,
        "facing": facing
    }

    # إرسال البيانات للـ Backend (FastAPI)
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            price = result["predicted_price_rupees"]
            st.success(f"### Estimated Price: ₹ {price:,.2f} Rupees")
            st.balloons()
        else:
            st.error(f"Error from API: {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the backend API. Please make sure FastAPI is running.")
    except Exception as e:
        st.error(f"An error occurred: {e}")