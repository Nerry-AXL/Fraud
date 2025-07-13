import streamlit as st
import tensorflow as tf 
from tf.keras.models import load_model
import numpy as np

# Load the trained model
model = load_model("fraud_model.h5")

# Set up page config
st.set_page_config(page_title="Online Fraud Detection", layout="centered")

# Custom HTML styling (from your HTML file)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #1f2937, #6b21a8, #000000);
        color: white;
    }
    label {
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown("<h1 style='text-align: center; color: #c084fc;'>Fraud Detection in e-transer</h1>", unsafe_allow_html=True)

# === INPUT FIELDS ===
with st.form(key="fraud_form"):
    amount = st.number_input("Transaction Amount", step=0.01)
    oldbalanceOrg = st.number_input("Old Sender Balance", step=0.01)
    newbalanceOrig = st.number_input("New Sender Balance", step=0.01)
    oldbalanceDest = st.number_input("Old Destination Balance", step=0.01)
    newbalanceDest = st.number_input("New Destination Balance", step=0.01)

    type_encoded = st.selectbox("Transaction Type", [
        "CASH-IN", "CASH-OUT", "DEBIT", "PAYMENT", "TRANSFER"
    ])
    type_map = {"CASH-IN": 0, "CASH-OUT": 1, "DEBIT": 2, "PAYMENT": 3, "TRANSFER": 4}
    type_val = type_map[type_encoded]

    nameOrig_encoded = st.text_input("Sender Name", value="eg. john")
    nameDest_encoded = st.text_input("Destination Name", value="eg. conner")

    submit = st.form_submit_button("Predict Fraud")

# === PREDICTION ===
if submit:
    # Simple encoding: Convert letters to ASCII sum (or replace with your real encoding logic)
    nameOrig_sum = sum([ord(c) for c in nameOrig_encoded.upper() if c.isalpha()])
    nameDest_sum = sum([ord(c) for c in nameDest_encoded.upper() if c.isalpha()])

    # Prepare input for the model
    input_data = np.array([[amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest,
                            type_val, nameOrig_sum, nameDest_sum]])

    # Predict
    prediction = model.predict(input_data)[0][0]

    # Display result
    st.markdown("---")
    if prediction > 0.5:
        st.markdown(f"<p style='color: #facc15; text-align:center; font-weight:600;'>⚠️ This transaction is <span style='color:red;'>FRAUDULENT</span>.</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: #4ade80; text-align:center; font-weight:600;'>✅ This transaction is <span style='color:green;'>LEGITIMATE</span>.</p>", unsafe_allow_html=True)
