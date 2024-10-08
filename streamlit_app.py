# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your smoothie!.
    """
)

name_on_order = st.text_input('Name on the order:')

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredient_list:
    ingredients_string = ''
    
    for fruit in ingredient_list:
        ingredients_string += fruit + ' '

    # st.write(ingredients_string)

    my_insert_statement = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """','""" + name_on_order +  """')"""
    
    trim_to_insert = st.button('Submit Order')
    
    if trim_to_insert:
        session.sql(my_insert_statement).collect()

        st.success('Your Order has been placed ' + name_on_order + '!')
