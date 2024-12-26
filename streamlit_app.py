# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

#options = st.selectbox('What is your favorite fruit?',('Banana','Strawberries', 'Peaches'))

#st.write('You Selected',options)

from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect('Choose upto 5 Ingredients:', my_dataframe)

if ingredient_list:
   #st.write(ingredient_list)
   #st.text(ingredient_list)

    ingredients_string = ''

    for fruit_choosen in ingredient_list:
        ingredients_string += fruit_choosen + ' '
    
    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
                values ('""" + ingredients_string + """')"""
    
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')


    if time_to_insert:    
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
        
    












