import streamlit as st
import pandas as pd

from streamlit_frontend import page_config, captions, similarity_project
from data import create_dataFrame
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
# Create a dataset with sentences and its embeddings for all the files
data_path = r"C:\Users\personal\Projects\Britannica-Independence\Data"
#create_dataFrame(data_path)

# Read the DataFrame
df = pd.read_csv(r"C:\Users\personal\Projects\Britannica-Independence\data.csv", 
                 encoding='ISO-8859-1', low_memory=False)
                
# Nmaes of the People
people_names = df.Names.unique().tolist()
page_config()
captions()
col1,col2 = st.columns(2)
First_Person = col1.selectbox('First Person',people_names)
Second_Person = col2.selectbox('Second Person',people_names)
com_no = 5

if st.button('Generate'):
  similarity_project(First_Person,Second_Person,df,com_no)