# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:07:27 2024

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

# Dictionary of bike companies with their codes and models
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

# Prediction function
def prediction(var):
    input_variables = pd.DataFrame([var],
                                   columns=['yeardiff', 'model', 'company ', 'cc '],
                                   dtype=float)
    
    pred1 = loadmodel.predict(input_variables)
    pred = pred1 + 0.35*pred1
    return pred[0]

def main():
    st.title("BikesPe")

    # Getting input data from user
    Year = st.number_input("Enter the year", min_value=1900, max_value=datetime.now().year, value=2010)
    Month = st.number_input("Enter the month", min_value=1, max_value=12, value=1)
    
    yrdays = Year * 365
    mondays = Month * 30
    total = yrdays + mondays
    
    currmon = datetime.now().month
    curryy = datetime.now().year
    yrdays1 = curryy * 365
    mondays1 = currmon * 30
    total1 = yrdays1 + mondays1
    
    final = (total1 - total) / 365

    # Create the dropdown for company selection
    selected_company = st.selectbox(
        "Select Make",
        ["Select Make"] + list(bike_companies.keys())
    )

    # Model selection based on selected company
    model_code = None
    cc_value = None
    if selected_company != "Select Make":
        company_models = bike_companies[selected_company]["models"]
        if company_models:
            selected_model = st.selectbox(
                "Select Model",
                ["Select Model"] + list(company_models.keys())
            )
            if selected_model != "Select Model":
                model_code = company_models[selected_model]
                cc_value = cc_data.get(model_code, "Unknown")
                st.write(f"The CC value for the selected model is: {cc_value}")
        else:
            st.warning(f"No models available for {selected_company}")

    # Predict price
    if st.button("Predict Base Price"):
        if selected_company == "Select Make" or (bike_companies[selected_company]["models"] and model_code is None):
            st.error("Please select both company and model (if available).")
        else:
            company_code = bike_companies[selected_company]["code"]
            base_price = prediction([final, model_code or 0, company_code, float(cc_value)])
            st.session_state.current_price = base_price
            st.session_state.condition_level = 2  # Start at "Good" condition
            st.success(f"The predicted base price is: ₹{base_price:.2f}")

            # Store the input and predicted price in the database
            new_bike = Bike(year=Year, month=Month, yeardiff=final, cc=cc_value, company=selected_company, model=selected_model if model_code else "N/A", predicted_price=base_price)
            session.add(new_bike)
            session.commit()
            st.write("Data stored in the database successfully!")

    # Condition buttons and price display
    if 'current_price' in st.session_state:
        conditions = ["Bad", "Fair", "Good", "Very Good", "Excellent"]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        columns = [col1, col2, col3, col4, col5]

        for i, (condition, col) in enumerate(zip(conditions, columns)):
            if col.button(condition, key=f"condition_{i}"):
                st.session_state.condition_level = i

        # Calculate price range
        condition_factor = 1 + (st.session_state.condition_level - 2) * 0.02
        min_price = st.session_state.current_price * condition_factor
        max_price = min_price * 1.02  # Assuming a 40% range

        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
             <h3 style="color: #276bf2;">Automobile to dealer in {conditions[st.session_state.condition_level]} Condition is valued at</h3>
             <h2 style="color: #276bf2;">₹{min_price:,.0f} - ₹{max_price:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

# Display condition buttons
        st.markdown(
            f"""
            <style>
            .stButton > button {{
                width: 100%;
                height: 50px;
                font-size: 14px;
            }}
            </style>
            """,
            unsafe_allow_html=True,
         )


if __name__ == "__main__":
    main()
