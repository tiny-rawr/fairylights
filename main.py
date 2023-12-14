from components.main_sidebar import sidebar
import uuid
import streamlit as st

def init_session_state():
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())

init_session_state()

sidebar()





