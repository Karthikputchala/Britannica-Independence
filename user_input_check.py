import streamlit as st

def similar_name(first_name,second_name):
    if first_name == second_name:
        st.subheader(":red[Select differnet names for both persons]")
        stop = True
    else:
        stop = False
    return stop
    


