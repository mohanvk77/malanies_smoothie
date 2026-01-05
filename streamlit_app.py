# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Cutomize your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)
name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on the Smoothie will be ',name_on_order)
# title = st.text_input("Movie title", "Life of Brian")
# st.write("The current movie title is", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to five ingredients:' ,my_dataframe,max_selections = 5)

if ingredients_list:
    ingredients_string = ''
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    for fruit_choosen in ingredients_list:
        ingredients_string+= fruit_choosen
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
      
    import requests
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    st.text(smoothiefroot_response)
