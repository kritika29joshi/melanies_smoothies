import streamlit as st
from snowflake.snowpark import Session

# Create a Snowflake session using Streamlit secrets
def create_session():
    connection_parameters = st.secrets["snowflake"]
    return Session.builder.configs(connection_parameters).create()

session = create_session()

# Fetch fruit options from the Snowflake table
my_dataframe = session.table('Smoothies.public.fruit_options').select('fruit_name').to_pandas()
fruit_options = my_dataframe['FRUIT_NAME'].tolist()

# UI components
st.title(':cup_with_straw: Customize Your Smoothie! :cup_with_straw:')
name_on_order = st.text_input('Name: ')
st.write('The name on your Smoothie will be:', name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', fruit_options, max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    my_insert_stmt = f"""
    INSERT INTO Smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon='✅')
