# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:07:27 2024

@author: Shubham Singhal
"""

import os
import numpy as np 
import pickle
import pandas as pd
import sqlite3
import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# Ensure setupdb.py is in the same directory and properly configured


# Create a SQLite database connection


# Load the model
loadmodel = pickle.load(open('finalmodel.sav', 'rb'))



bike_companies = {
    "Bajaj": {
        "code": 1,
        "models": {
            "Avenger 220": 1007,
            "CT 100": 1016,
            "Discover 100T": 1019,
            "Dominar 400cc": 1020,
            "Platina": 1045,
            "Pulsar 150 CC": 1047,
            "Vikrant v15": 1060,
            "V15": 1062
        }
    },
 
    "Hero": {
        "code": 3,
        "models": {
            "Achiever 150": 1001,
            "CBZ Xtreme 200": 1013,
            "CD 110": 1014,
            "Destini 125": 1018,
            "Glamour EFI": 1029,
            "HF Deluxe": 1031,
            "Hunk": 1033,
            "MaestroEDGE 110": 1041,
            "Passion PRO": 1043,
            "Pleasure": 1046,
            "Shine": 1053,
            "Splendor iSmart": 1036,
            "Xtreme Sports": 1058,
            "Xpulse": 1061
        }
    },
    "Honda": {
        "code": 4,
        "models": {
            "Activa 3G": 1002,
            "Activa 125": 1003,
            "Activa 5G": 1005,
            "Activa HET": 1006,
            "CB Hornet": 1010,
            "CB Shine": 1011,
            "CB Trigger": 1012,
            "Dream Yuga": 1021,
            "Grazia": 1030,
            "Livo": 1040,
            "Stunner": 1057,
            "Twister": 1064,
            "X Blade": 1063
        }
    },
    "Royal Enfield": {
        "code": 10,
        "models": {
            "Electra 350cc": 1024,
            "Himalyan 412": 1032,
            "Jawa ABS": 1037
        }
    },
    "Yamaha": {
        "code": 6,
        "models": {
            "Cygnus Alpha": 1017,
            "Fascino": 1026,
            "FZ-S": 1027,
            "R15": 1048,
            "Saluto": 1051,
            "SS 125cc": 1055,
            "SZ-RR": 1065
        }
    },
    "Suzuki": {
        "code": 11,
        "models": {
            "Access 125": 1000,
            "Burgman street": 1009,
            "Gixxer": 1028,
            "Intruder": 1034
        }
    },
    "TVS": {
        "code": 12,
        "models": {
            "Apache 160 RTR": 1008,
            "IQube": 1035,
            "Jupiter": 1038,
            "NTORQ": 1042,
            "Phoenix": 1044,
            "Radeon": 1049,
            "Raider": 1050,
            "Scooty Pep+": 1052,
            "Sport KLS": 1054,
            "Star Sport": 1056,
            "Victor": 1059
        }
    },
    "Importer Adishwar": {
        "code": 5,
        "models": {
            "Keeway SR 250": 1039
        }
    },
    "KTM": {
        "code": 7,
        "models": {
            "Duke 125cc": 1023
        }
    },
    "Mahindra": {
        "code": 8,
        "models": {
            "Centuro": 1015
        }
    },
    "Okaya": {
        "code": 9,
        "models": {
            "Faast F4": 1025
        }
    }
}


# Dictionary of cc values for each model
cc_data = {
    1000: 125, 1001: 150, 1002: 110, 1003: 125, 1005: 110, 1006: 110, 1007: 220, 1008: 160, 
    1009: 125, 1010: 160, 1011: 125, 1012: 150, 1013: 200, 1014: 110, 1015: 110, 1016: 100, 
    1017: 110, 1018: 125, 1019: 100, 1020: 400, 1021: 110, 1022: 110, 1023: 125, 1024: 350, 
    1025: 50, 1026: 110, 1027: 150, 1028: 110, 1029: 160, 1030: 125, 1031: 100, 1032: 412, 
    1033: 150, 1034: 150, 1035: 90, 1036: 100, 1037: 350, 1038: 110, 1039: 250, 1040: 125, 
    1041: 110, 1042: 125, 1043: 110, 1044: 125, 1045: 100, 1046: 110, 1047: 150, 1048: 155, 
    1049: 125, 1050: 125, 1051: 125, 1052: 90, 1053: 125, 1054: 110, 1055: 125, 1056: 110, 
    1057: 125, 1058: 150, 1059: 110, 1060: 150, 1061: 200, 1062: 150, 1063: 160, 1064: 110, 
    1065: 150
}

# Prediction function
# Prediction function with 35% increase for base price
def prediction(var):
    input_variables = pd.DataFrame([var],
                                   columns=['yeardiff', 'model', 'company ', 'cc '],
                                   dtype=float)
    
    pred1 = loadmodel.predict(input_variables)
    pred = pred1 * 1.10  # Applying 35% increase
    return pred[0]


condition_gauge_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bike Condition Gauge</title>
<style>
    .gauge-container {
        width: 200px;
        margin: 0 auto;
    }
    .gauge {
        width: 100%;
        height: 100px;
        position: relative;
        overflow: hidden;
    }
    .gauge:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 200px;
        border-radius: 100% 100% 0 0;
        background: conic-gradient(
            from 180deg,
            #ff0000 0deg 45deg,
            #ff7f00 45deg 90deg,
            #ffff00 90deg 117deg,
            #cccc00 117deg 144deg,
            #00ff00 144deg 180deg
        );
    }
    .gauge-mask {
        width: 100%;
        height: 100px;
        position: absolute;
        top: 0;
        left: 0;
        background: #fff;
        transform-origin: center bottom;
        transition: transform 0.5s ease-in-out;
    }
    .needle {
        width: 2px;
        height: 65px;
        background: #000;
        position: absolute;
        bottom: 0;
        left: 50%;
        transform-origin: bottom center;
        transition: transform 0.5s ease-in-out;
    }
    .gauge-value {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
    }
    .gauge-labels {
        display: flex;
        justify-content: space-between;
        margin-top: 5px;
        font-size: 12px;
        color: #666;
    }
</style>
</head>
<body>
<div class="gauge-container">
    <div class="gauge">
        <div class="gauge-mask" id="gaugeMask"></div>
        <div class="needle" id="gaugeNeedle"></div>
        <div class="gauge-value" id="gaugeValue"></div>
    </div>
    <div class="gauge-labels">
        <span>Bad</span>
        <span>Excellent</span>
    </div>
</div>
<script>
    function updateGauge(condition) {
        const conditions = ['Bad', 'Fair', 'Good', 'Very Good', 'Excellent'];
        const index = conditions.indexOf(condition);
        const angle = index * 45; // 180 degrees / 4 sections = 45 degrees per section

        const gaugeMask = document.getElementById('gaugeMask');
        const gaugeNeedle = document.getElementById('gaugeNeedle');
        const gaugeValue = document.getElementById('gaugeValue');

        gaugeMask.style.transform = `rotate(${180 - angle}deg)`;
        gaugeNeedle.style.transform = `rotate(${angle}deg)`;
        gaugeValue.textContent = condition;
    }
</script>
</body>
</html>
"""

def main():
    st.set_page_config(page_title="BikesPe", layout="wide")

    st.markdown("""
    <style>
    .main-header {text-align: center; color: #276bf2;}
    .sub-header {text-align: center; color: #4a4a4a;}
    .stButton>button {
        width: 100%;
        background-color: #276bf2;
        color: white;
    }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .warning-text {color: #ff0000; font-size: 14px; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>BikesPe</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Knowing the correct market price helps you take a wise decision while buying or selling a secondhand bike.</p>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Find the right price of a used bike</h2>", unsafe_allow_html=True)

    # Initialize session state
    if 'company' not in st.session_state:
        st.session_state.company = None
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'condition_level' not in st.session_state:
        st.session_state.condition_level = None
    if 'price_range' not in st.session_state:
        st.session_state.price_range = (0, 0)
    if 'current_price' not in st.session_state:
        st.session_state.current_price = 0
    if 'base_price_predicted' not in st.session_state:
        st.session_state.base_price_predicted = False
    if 'bad_condition_selected' not in st.session_state:
        st.session_state.bad_condition_selected = False

    col1, col2 = st.columns(2)

    with col1:
        selected_company = st.selectbox(
            "Select Make",
            ["Select Make"] + list(bike_companies.keys())
        )
        if selected_company != st.session_state.company:
            st.session_state.company = selected_company
            st.session_state.model = None  # Reset model if company changes

    with col2:
        if st.session_state.company and st.session_state.company != "Select Make":
            if st.session_state.company in bike_companies:
                company_models = bike_companies[st.session_state.company].get("models", {})
                if company_models:
                    selected_model = st.selectbox(
                        "Select Model",
                        ["Select Model"] + list(company_models.keys())
                    )
                    if selected_model != st.session_state.model:
                        st.session_state.model = selected_model
                else:
                    st.warning(f"No models available for {st.session_state.company}")
                    selected_model = "Select Model"
            else:
                st.warning(f"Company {st.session_state.company} not found.")
                selected_model = "Select Model"
        else:
            selected_model = "Select Model"

    col3, col4 = st.columns(2)

    with col3:
        Year = st.number_input("Year", min_value=2004, max_value=datetime.now().year, value=2015)

    with col4:
        Month = st.number_input("Month", min_value=1, max_value=12, value=1)

    kms_run = st.number_input("KMs Run", min_value=0, value=0)

    if st.button("Check Price"):
        if st.session_state.company == "Select Make" or st.session_state.model == "Select Model":
            st.warning("Please select a valid make and model.")
        else:
            if st.session_state.company in bike_companies:
                company_code = bike_companies[st.session_state.company]["code"]
                model_code = bike_companies[st.session_state.company]["models"].get(st.session_state.model, None)
                if model_code is None:
                    st.warning(f"Model {st.session_state.model} not found for {st.session_state.company}.")
                else:
                    current_year = datetime.now().year
                    age = current_year - Year
                    cc = cc_data.get(model_code, 100)  # Defaulting cc to 100 if not found
                    base_price = prediction([age, model_code, company_code, cc])
                    
                    st.session_state.current_price = base_price
                    st.session_state.condition_level = 2  # Default to "Good"
                    
                    # Set the initial price range for "Good" condition
                    min_price = base_price
                    max_price = min_price * 1.03
                    st.session_state.price_range = (min_price, max_price)

                    st.success(f"The predicted base price is: ₹{base_price:.2f}")
                    st.session_state.base_price_predicted = True

    if st.session_state.base_price_predicted:
        conditions = ["Bad", "Fair", "Good", "Very Good", "Excellent"]
        cols = st.columns(len(conditions))

        # Create two columns: one for the gauge and one for the price info
        gauge_col, info_col = st.columns([1, 2])

        with gauge_col:
            # Render the gauge
            components.html(condition_gauge_html, height=150)

        for i, (condition, col) in enumerate(zip(conditions, cols)):
            if col.button(condition, key=f"condition_{i}"):
                st.session_state.condition_level = i
                if condition == "Bad":
                    st.session_state.bad_condition_selected = True
                else:
                    st.session_state.bad_condition_selected = False
                    # Calculate price range for the selected condition
                    if condition == "Good":
                        min_price = st.session_state.current_price
                    elif condition == "Fair":
                        min_price = st.session_state.current_price * 0.93
                    else:
                        prev_min_price = st.session_state.price_range[0]
                        min_price = prev_min_price * 0.93 if condition == "Fair" else prev_min_price * 1.07

                    max_price = min_price * 1.03
                    st.session_state.price_range = (min_price, max_price)

                # Update the gauge
                gauge_update_script = f"""
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        updateGauge('{condition}');
                    }});
                </script>
                """
                components.html(gauge_update_script, height=0)

        # Display price range or warning
        with info_col:
            if st.session_state.condition_level is not None:
                if st.session_state.bad_condition_selected:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
                        <h3 style="color: #276bf2;">Best value for your pre-loved bike in {conditions[st.session_state.condition_level]} Condition</h3>
                        <p class="warning-text">We don't deal in bad condition bikes.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    min_price, max_price = st.session_state.price_range
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
                        <h3 style="color: #276bf2;">Best value for your pre-loved bike in {conditions[st.session_state.condition_level]} Condition is valued at</h3>
                        <h2 style="color: #276bf2;">₹{min_price:,.0f} - ₹{max_price:,.0f}</h2>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()