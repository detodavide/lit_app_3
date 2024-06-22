import streamlit as st

def app():
    request = st.text_area("Insert a request", "")  # Creates a text area for user input

    if st.button("Submit"):  # Button to submit the request
        st.write(f"Request submitted: {request}")  # Display the submitted request


