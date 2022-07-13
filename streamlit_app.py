import pandas as pd
import streamlit


my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')

streamlit.text('🥣 Blueberry Oatmeal')
streamlit.text('🐔 Scrambled Eggs')
streamlit.text('🥗 Green Salad')
streamlit.text('🥑 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# add pick list
streamlit.multiselect('Pick some fruits: ', list(my_fruit_list.index))
# display fruit table
streamlit.dataframe(my_fruit_list)
