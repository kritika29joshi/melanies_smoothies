import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Initialize the Snowflake session
def get_active_session():
    # Replace the following with your Snowflake connection parameters
    connection_parameters = {
        "account": "KRITIKA_B3",
        "user": "Kritika02",
        "password": "Trial@2004",
        "role": "SYSADMIN",
        "warehouse": "COMPUTE_WH",
        "database": "SMOOTHIES",
        "schema": "PUBLIC"
    }
    return Session.builder.configs(connection_parameters).create()

st.title(':cup_with_straw: Customize Your Smoothie! :cup_with_straw:')
st.write('Choose the fruits you want in your custom Smoothie!')

name_on_order = st.text_input('Name: ')
st.write('The name on your Smoothie will be:', name_on_order)

# Get the active session
session = get_active_session()

# Fetch the fruit options from the Snowflake table
my_dataframe = session.table('Smoothies.public.fruit_options').select(col('fruit_name')).collect()

# Convert the collected data to a list for the multiselect
fruit_options = [row['fruit_name'] for row in my_dataframe]

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', fruit_options, max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Join selected fruits with a comma

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order) 
                         VALUES ('{ingredients_string}', '{name_on_order}')"""
   
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon='✅')
