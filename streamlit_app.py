import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


#-------------------------------------------------


#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") # testing connection
#my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
#my_data_rows = my_cur.fetchall()
#my_data_row = my_cur.fetchone()
#st.text("Hello from :")
#st.text(my_data_row)
st.info("This current page has been made with Streamlit and Snowflake as a backend. Both of them connected by Python. The current data may need to be refreshed by 3rd November of 2023. Developed by FairCuratorLtd")
st.title("Fresh fruit for a healthy lifestyle. Our favorites:")
#------------------------------
# Snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
      return my_cur.fetchall()

# Add a button to load the fruit
if st.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   # display table
   base_df = pd.DataFrame(my_data_rows)
   st.dataframe( base_df)#[base_df[0].str.contains(fruits_selected2)])
   
#----------------------------------------------------
#st.dataframe(my_data_rows2)
# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('"+ new_fruit +"')")
      my_cnx.close()
      return 'Thanks for adding '+ new_fruit
add_my_fruit = st.text_input(label='What input would you like to add?', max_chars=50)
#st.write('Thanks for adding ', add_my_fruit)

if st.button('Add a Fruit to the List'):
   my_cnx=snowflake.connector.connect(**st.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   st.text(back_from_function)
# don't run anything past here while we troubleshoot
#st.stop()
## this will not work correctly but just go with it for now
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
#-----


st.header('1. Our recommended menu examples!*  :sunglasses:')
st.caption(' _*If you have any medical condition, please seek advice from a medical doctor, since they may adjust your menu to your condition for better outcomes._ ')
st.header('Breakfast Menu')
   
st.text('🥣 Omega 3 % Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑 Guacamole burritos')
st.text('🍞 beans in toast')

st.header('🍌🥭 2. Hands-on! Build your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display table
st.dataframe(fruits_to_show)

#-----------------------------------------------------------------

def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
   #st.text(fruityvice_response.json())
   # write your own comment -what does the next line do? 
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

   
###### FRUIT SELECTION
st.header("3. Fruityvice Fruit Advice!* :book: ")
st.caption(' _*If you have any medical condition, please seek advice from a medical doctor, since they may adjust your menu to your condition for better outcomes._ ')

try:   
   fruit_choice = st.text_input('What fruit would you like information about?')
   if not fruit_choice:
      st.error("Please select a fruit to get information.")
   else: 
      #st.write('The user entered ', fruit_choice) 
      back_from_function = get_fruityvice_data(fruit_choice)
      # write your own comment - what does this do?
      st.dataframe(back_from_function)
except URLError as e:
   st.error()

