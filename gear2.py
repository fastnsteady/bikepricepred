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
    pred = pred1 * 1.05  # Applying 35% increase
    return pred[0]

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
        if st.session_state.company:
            company_models = bike_companies[st.session_state.company]["models"]
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
            company_code = bike_companies[st.session_state.company]["code"]
            model_code = bike_companies[st.session_state.company]["models"].get(st.session_state.model, None)
            if model_code is None:
                st.warning(f"Model {st.session_state.model} not found for {st.session_state.company}.")
            else:
                current_year = datetime.now().year
                age = current_year - Year
                cc = cc_data.get(model_code, 100)  # Defaulting cc to 100 if not found
                price = prediction([age, model_code, company_code, cc])
                
                st.write(f"Predicted price for the bike is: ₹{price:.2f}")

                # Store the details in the database
                bike_record = Bike(
                    make=st.session_state.company,
                    model=st.session_state.model,
                    year=Year,
                    month=Month,
                    kms_run=kms_run,
                    predicted_price=price
                )
                session.add(bike_record)
                session.commit()

                st.success("Details have been saved successfully.")

if __name__ == "__main__":
    main()