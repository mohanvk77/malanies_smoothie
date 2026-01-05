# Import python packages
import streamlit as st
import requests
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
# Convert the snowpark dataframe to a panda dataframe so we can use the LOC function
#pd_df = my_dataframe.to_pandas()
#st.dataframe = (pd_df)
#st.stop()

ingredients_list = st.multiselect('Choose up to five ingredients:' ,my_dataframe,max_selections = 5)

if ingredients_list:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string+= fruit_choosen + ' '
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
        sf_df = st.dataframe(data = smoothiefroot_response.json(),use_container_width = True)
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
