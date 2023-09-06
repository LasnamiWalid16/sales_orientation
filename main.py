# Import the Streamlit library
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery

# Add a title to your app
st.title("SAG Student Orientation")

# Add some text
st.write("Choose your best course in a few clicks!")

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

project_id = 'ga4bigquery-364118'
client = bigquery.Client(credentials=credentials, project=project_id)

@st.cache_data(ttl=600)
def run_query(query):
    select = client.query(query, job_config=job_config)
    return select.to_dataframe()

# Create a Streamlit selectbox to choose a localCountry
selected_localCountryName = st.selectbox("Select a local Country", ['Algeria', 'Nigeria', 'Morocco'])

# Create a Streamlit selectbox to choose a degree
selected_degree = st.selectbox("Select a degree", ['Bachelor', 'Master', 'Phd'])

# Create a Streamlit selectbox to choose a discipline
selected_discipline = st.selectbox("Select a discipline", ['Professions and Applied Sciences', 'Social Science', 'Art',
                                                           'Humanities', 'Formal Sciences', 'Natural Sciences'])

# Create a Streamlit selectbox to choose an admissionType
selected_admissionType = st.selectbox("Select an admissionType", ['pathway', 'direct', 'both'])

# Create a Streamlit selectbox to choose a country
selected_country = st.selectbox("Select a country you want to apply for", ['England', 'Northern Ireland', 'Scotland', 'Australia', 'Wales', 'Ireland', 'United States', 'Netherlands'])

# Create a submit button
if st.button("Show Results"):
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("degree", "STRING", selected_degree),
        ]
    )

    sql_query = f""" SELECT * FROM `ga4bigquery-364118.mongoDB.all_data` 
                     WHERE localCountryName = '{selected_localCountryName}'  
                     AND   degree = '{selected_degree}'  
                     AND   discipline = '{selected_discipline}'  
                     AND   admissionType = '{selected_admissionType}'  
                     AND   country = '{selected_country}'   """
                     
    all_data = run_query(sql_query)
    
    

    st.write(all_data)
