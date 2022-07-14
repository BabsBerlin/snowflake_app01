import pandas as pd
import requests
import streamlit
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')

streamlit.text('🥣 Blueberry Oatmeal')
streamlit.text('🐔 Scrambled Eggs')
streamlit.text('🥗 Green Salad')
streamlit.text('🥑 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# show fruit info from csv file
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
# add pick list
fruits_selected = streamlit.multiselect('Pick some fruits: ', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# display fruit table
streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # convert json response into pandas DF 
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # prints DF
    return fruityvice_normalized
    
# new section to show the api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  # let the user decide which fruit to look up
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get info!')
  else:
    streamlit.write('The user entered ', fruit_choice)
    # prints DF
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    streamlit.error()

streamlit.stop()

# connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# let the user decide which fruit to look up
fruit_choice_add = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('thanks for adding ', fruit_choice_add)


my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('FROM STREAMLIT');")



