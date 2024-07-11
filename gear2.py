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
    pred = pred1 + 0.35 * pred1
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
         

    # Condition buttons and price display
    if 'current_price' in st.session_state:
        conditions = ["Bad", "Fair", "Good", "Very Good", "Excellent"]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        columns = [col1, col2, col3, col4, col5]

        for i, (condition, col) in enumerate(zip(conditions, columns)):
            if col.button(condition, key=f"condition_{i}"):
                if condition == "Bad":
                    st.session_state.condition_level = -1
                else:
                    st.session_state.condition_level = i

        # Display message for bad condition
        if st.session_state.condition_level == -1:
            st.warning("We don't deal in bad condition.")
        else:
            # Calculate price range
            condition_factor = 1 + (st.session_state.condition_level) * 0.10
            min_price = st.session_state.current_price * condition_factor
            max_price = min_price * 1.02  # Assuming a 2% range

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
