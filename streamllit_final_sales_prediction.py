import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Configure Streamlit page
st.set_page_config(page_title="Final Retail Sales Forecast", layout="wide", initial_sidebar_state="auto")

# Load dataset
df = pd.read_csv(r"C:\Users\ADMIN\Videos\capstion_project\final_project\data_analysis.csv") 


# Load the model
with open(r"C:\Users\ADMIN\Videos\capstion_project\final_project\random_regression.pkl", 'rb') as file:
    model = pickle.load(file)

# Create columns for inputs
column1, column2 = st.columns([2, 2], gap='small')

# Define min and max for inputs
min_temp = df['Temperature_fahr'].min()
max_temp = df['Temperature_fahr'].max()
min_fuel_price = df['Fuel_Price'].min()
max_fuel_price = df['Fuel_Price'].max()
min_cpi = df['CPI'].min()
max_cpi = df['CPI'].max()
min_unemployment = df['Unemployment'].min()
max_unemployment = df['Unemployment'].max()
min_week = df['week_of_number'].min()
max_week = df['week_of_number'].max()
min_markdown = df['MarkDown'].min()
max_markdown = df['MarkDown'].max()

with column1:
    Store = st.selectbox("**Select a Store Id:**", options=df['Store'].unique())
    Temperature_fahr = st.number_input(f'**Enter Temperature_fahr (Min: {min_temp}, Max: {max_temp}):**', min_value=min_temp, max_value=max_temp)
    Fuel_Price = st.number_input(f'**Enter Fuel Price (Min: {min_fuel_price}, Max: {max_fuel_price}):**', min_value=min_fuel_price, max_value=max_fuel_price)
    CPI = st.number_input(f'**Enter CPI (Min: {min_cpi}, Max: {max_cpi}):**', min_value=min_cpi, max_value=max_cpi)
    Unemployment = st.number_input(f'**Enter Unemployment (Min: {min_unemployment}, Max: {max_unemployment}):**', min_value=min_unemployment, max_value=max_unemployment)
    IsHoliday = st.selectbox("**Is Holiday?:**", options=[True, False])

with column2:
    Dept = st.selectbox("**Select a Dept Id:**", options=df['Dept'].unique())
    Type = st.selectbox("**Select a Type:**", options=df['Type'].unique())
    MarkDown = st.number_input(f'**Enter MarkDown (Min: {min_markdown}, Max: {max_markdown}):**', min_value=min_markdown, max_value=max_markdown)
    week_of_number = st.number_input(f'**Enter Week Number (Min: {min_week}, Max: {max_week}):**', min_value=min_week, max_value=max_week)
    year = st.number_input('**Enter the Year:**', min_value=2000, max_value=2100)  # Adjust year range as needed

# Prepare input list for prediction
inputs = [
    int(Store),
    Temperature_fahr,
    Fuel_Price,
    CPI,
    Unemployment,
    1.0 if IsHoliday else 0.0,  # Convert boolean to float
    int(Dept),
    {"A": 0.0, "B": 1.0, "C": 2.0}.get(Type),  # Map Type to corresponding float value
    MarkDown,
    year,
    week_of_number
]

# Prediction button
if st.button("Submit"):
    y = np.array([inputs])
    prediction = model.predict(y)[0]  
    formatted_prediction = f"{prediction:.2f}"  


    st.markdown(f"# :green[Prediction of weekly sales price is: :red['{formatted_prediction}']]")
