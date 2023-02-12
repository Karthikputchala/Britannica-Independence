import streamlit as st
import re
import json
import pandas as pd
from user_input_check import similar_name
from similarity import newcosine
view_raw_data = "https://www.britannica.com/biography/"

def page_config():
    st.set_page_config(layout="wide",initial_sidebar_state = "expanded")

def captions():
    url = "https://www.britannica.com/biographies/history/independence"
    view_raw_data = "https://www.britannica.com/biography/Bal-Gangadhar-Tilak"
    st.header(':black[Exploring Similarities in the people known for Independence]')
    st.write('There are many people who are known to fight for the Independece of their country.\
        From many of them BRITANNICA (Encyclopædia publishing company) had made a database of most\
        prominently known Freedom fighters.'+"[(More details about the Data)](%s)" % url)
    #st.caption(" [(View raw Data of the article)](%s)"% view_raw_data)
    st.write('In this project user could extract the top similarites between any two selected doctuments from the [(source)](%s) by just selecting the person names'% url)

def person_details():
    pass

def display_data(person_a_sent,person_b_sent,first_name,second_name):
    count = len(person_a_sent)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(first_name)
        for i in range(count):
            person_a_sent[i] = re.sub(r'[^\w\s]','',person_a_sent[i])
            text = str(i+1) + ") " + person_a_sent[i]+"."
            st.write(text)
    with col2:
        st.subheader(second_name)
        for i in range(count):
            person_b_sent[i] = re.sub(r'[^\w\s]','',person_b_sent[i])
            text = str(i+1) + ") " + person_b_sent[i]+"."
            st.write(text)

def similarity_project(first_name,second_name,df,com_no):
    stop = similar_name(first_name,second_name)
    if stop != True:
        sent_a, sent_b = newcosine(first_name, second_name, df,com_no)
        display_data(sent_a,sent_b,first_name,second_name)


