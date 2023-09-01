# Import the Streamlit library
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Add a title to your app
st.title("Simple Streamlit App")

# Add some text
st.write("Welcome to this simple Streamlit app.")

# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

project_id = 'ga4bigquery-364118'
client = bigquery.Client(credentials=credentials,project=project_id)


@st.cache_data(ttl=600)
def run_query(query):
    select = client.query(query)
    return select.to_dataframe()
  

all_data = run_query(" SELECT * FROM `ga4bigquery-364118.mongoDB.all_data` ")
all_data['fees'] = pd.to_numeric(all_data['fees'], errors='coerce').astype('float')


# Create a Streamlit selectbox to choose a degree
selected_degree = st.selectbox("Select a degree", ['Bachelor','Master'])

# Create a Streamlit selectbox to choose a admissionType
selected_admissionType = st.selectbox("Select a admissionType", ['direct','pathway','both'])

# Create a Streamlit selectbox to choose a university
selected_university = st.selectbox("Select a University", all_data['university'].unique())

# Filter the DataFrame based on the selected university
filtered_data = all_data[(all_data['university'] == selected_university) & (all_data['degree'] == selected_degree)
                         & (all_data['admissionType'] == selected_admissionType)]

# Display the filtered data
st.write(f"Data for students from {selected_university}:")
st.write(filtered_data)



