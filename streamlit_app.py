# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

#options = st.selectbox('What is your favorite fruit?',('Banana','Strawberries', 'Peaches'))

#st.write('You Selected',options)

name_on_order = st.text_input('Nmae On The Smoothie :')
st.write('The Name on your smoothie will be :', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect('Choose upto 5 Ingredients:', my_dataframe,max_selections = 5)

if ingredient_list:
   #st.write(ingredient_list)
   #st.text(ingredient_list)

    ingredients_string = ''

    for fruit_choosen in ingredient_list:
       ingredients_string += fruit_choosen + ' '

       search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
       st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

       st.subheader(fruit_choosen + ' Nutrition Information')
       smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
       sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')


    if time_to_insert:    
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
    











