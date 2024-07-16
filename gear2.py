# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:22:28 2024

@author: Shubham Singhal
"""

import os
import numpy as np 
import pickle
import pandas as pd
import streamlit as st
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setupdb import Bike  # Ensure setupdb.py is in the same directory

# Create a SQLite database connection
engine = create_engine('sqlite:///bikes.db')
Session = sessionmaker(bind=engine)
session = Session()

# Load the model
loadmodel = pickle.load(open('finalmodel.sav', 'rb'))

# Assuming you have these dictionaries defined

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
    "GEM": {
        "code": 2,
        "models": {}
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


def prediction(var):
    input_variables = pd.DataFrame([var],
                                   columns=['yeardiff', 'model', 'company ', 'cc '],
                                   dtype=float)
    
    pred1 = loadmodel.predict(input_variables)
    pred = pred1 * 1.15  # Applying 15% increase
    return pred[0]

def main():
    st.title("BikesPe - Find the right price of a used bike")

    st.write("Knowing the correct market price helps you take a wise decision while buying or selling a secondhand bike.")

    col1, col2 = st.columns(2)

    with col1:
        selected_company = st.selectbox(
            "Select Make",
            ["Select Make"] + list(bike_companies.keys())
        )

    with col2:
        model_options = ["Select Model"]
        if selected_company != "Select Make":
            model_options += list(bike_companies[selected_company]["models"].keys())
        
        selected_model = st.selectbox("Select Model", model_options)

    col3, col4 = st.columns(2)

    with col3:
        location = st.selectbox("Select Location", ["Select Location", "Delhi", "Mumbai", "Bangalore", "Chennai"])

    with col4:
        current_year = datetime.now().year
        Year = st.selectbox("Select Year", range(current_year, 1990, -1))

    kms_run = st.number_input("KMs Run", min_value=0, value=25000, step=1000)

    if st.button("Check Price", key="check_price"):
        if selected_company == "Select Make" or selected_model == "Select Model" or location == "Select Location":
            st.error("Please select all required fields.")
        else:
            # Calculate yeardiff
            currmon = datetime.now().month
            curryy = datetime.now().year
            yrdays1 = curryy * 365
            mondays1 = currmon * 30
            total1 = yrdays1 + mondays1
            
            yrdays = Year * 365
            total = yrdays  # Assuming start of the year for simplicity
            
            final = (total1 - total) / 365

            # Get model code and cc value
            model_code = bike_companies[selected_company]["models"][selected_model]
            cc_value = cc_data.get(model_code, "Unknown")
            company_code = bike_companies[selected_company]["code"]

            # Predict base price
            base_price = prediction([final, model_code, company_code, float(cc_value)])

            st.subheader(f"Resale value of {selected_company} {selected_model} in {location}")
            st.write(f"Price of {Year} model {selected_company} {selected_model} in {location}")
            st.write("The value given below is an estimated value only. Actual value may vary depending on the condition of the two-wheeler and several other factors.")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Condition**")
                st.write("Fair")
                st.write("Good")
                st.write("Excellent")

            with col2:
                st.markdown("**Current Market Value**")
                st.write(f"Rs. {int(base_price * 0.95):,}")
                st.write(f"Rs. {int(base_price):,}")
                st.write(f"Rs. {int(base_price * 1.05):,}")

            # Store the input and predicted price in the database
            new_bike = Bike(year=Year, month=1, yeardiff=final, cc=cc_value, company=selected_company, model=selected_model, predicted_price=base_price)
            session.add(new_bike)
            session.commit()

    col1, col2 = st.columns(2)
    with col1:
        st.button(f"Buy used {selected_company} {selected_model} in {location}", key="buy_button")
    with col2:
        st.button(f"Sell {selected_company} {selected_model}", key="sell_button")

    # Add custom CSS to style the buttons and layout
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stDeployButton {
        display: none !important;
    }
    
    .viewerBadge_container__1QSob {
        display: none !important;
    }
    
    .stToolbar {
        display: none !important;
    }
    
    .stButton > button {
        width: 100%;
        height: 50px;
        font-size: 14px;
    }
    
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button {
        background-color: #dc3545;
        color: white;
    }
    
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button {
        background-color: #fd7e14;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()