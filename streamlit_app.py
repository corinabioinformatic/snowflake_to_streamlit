import streamlit as st
import pandas as pd
import requests
import snowflake.connector


my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") # testing connection
my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
#my_data_row = my_cur.fetchone()
#st.text("Hello from :")
#st.text(my_data_row)

st.header("The fruit load list contains:")
#----
#my_unlisted_rows = pd.explode(my_data_rows)
st.text(type(my_data_rows))
st.text(type(my_data_rows[0]))
st.text(my_data_rows)

#my_data_rows2 = pd.DataFrame({'Fruits':pd.Series(my_data_rows)})
my_data_rows2 = pd.DataFrame(my_data_rows)
#my_data_rows2 = my_data_rows2.rename(columns={'0':'Fruits'})
my_data_rows2 = my_data_rows2.set_index(0)
# Let's put a pick list here so they can pick the fruit they want to include 
add_my_fruit = st.multiselect("Pick fruits to see:", list(my_data_rows2.index))
fruits_to_show2 = my_data_rows2 #my_data_rows2.loc[fruits_selected2]
st.text(add_my_fruit)
st.text(type(my_data_rows2))
st.text(len(my_data_rows2))
st.text(my_data_rows2.shape)
# df[df['A'].str.contains("hello")]
# display table
base_df = pd.DataFrame(my_data_rows)
st.dataframe( base_df)#[base_df[0].str.contains(fruits_selected2)])
#----
#st.dataframe(my_data_rows2)

st.write('Thanks for adding ', add_my_fruit2)

## this will not work correctly but just go with it for now
my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list values ('from streamlit')")
#-----


st.title('My Parents New Healthy Diner')
st.header('Breakfast Menu')
   
st.text('🥣 Omega 3 % Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑 Guacamole burritos')
st.text('🍞 beans in toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display table
st.dataframe(fruits_to_show)


###### FRUIT SELECTION
st.header("Fruityvice Fruit Advice!")
fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#st.text(fruityvice_response.json())

# write your own comment -what does the next line do? 
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
st.dataframe(fruityvice_normalized)
