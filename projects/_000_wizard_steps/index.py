import streamlit as st
from datetime import date

def init_session_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'data' not in st.session_state:
        st.session_state.data = {}

def save_input(key, input_data):
    st.session_state.data[key] = input_data

def validate_input(key, value):
    if value:
        save_input(key, value)
        return True
    else:
        st.error(f"{key.capitalize()} is required.")
        return False

def can_proceed(inputs):
    for key, value in inputs.items():
        if not validate_input(key, value):
            return False
    return True

def step_1():
    st.subheader("Step 1: Personal Information")
    st.write("Please enter your name and email address.")
    name = st.text_input("Name", key='name')
    email = st.text_input("Email", key='email')

    if st.button("Save & Next", key='save1', on_click=lambda: save_and_next(2, {'name': name, 'email': email})):
        pass

def step_2():
    st.subheader("Step 2: Employment Details")
    st.write("Share your company name and position.")
    company = st.text_input("Company Name", key='company')
    position = st.text_input("Position", key='position')

    if st.button("Save & Next", key='save2', on_click=lambda: save_and_next(3, {'company': company, 'position': position})):
        pass

def step_3():
    st.subheader("Step 3: Preferences")
    st.write("Would you like to subscribe to our newsletter?")
    newsletter = st.checkbox("Subscribe to newsletter?", key='newsletter')
    save_input('newsletter', newsletter)
    if st.button("Save & Next", key='save3', on_click=lambda: save_and_next(4)):
        pass

def step_4():
    st.subheader("Step 4: Schedule Meeting")
    st.write("Select a date for the meeting.")
    meeting_date = st.date_input("Meeting Date", key='meeting_date', value=date.today())
    if st.button("Save & Next", key='save4', on_click=lambda: save_and_next(5, {'meeting_date': meeting_date})):
        pass

def step_5():
    st.subheader("Step 5: Review & Submit")
    st.write("Review all the data submitted and click submit if everything is correct.")
    if st.button("Submit", key='submit', on_click=submit_form):
        pass

def save_and_next(next_step, inputs=None):
    if inputs is None or can_proceed(inputs):
        st.session_state.current_step = next_step

def submit_form():
    st.write("All submitted data:")
    st.json(st.session_state.data)
    st.success("Form submitted successfully!")

def render_step(step):
    if step == 1:
        step_1()
    elif step == 2:
        step_2()
    elif step == 3:
        step_3()
    elif step == 4:
        step_4()
    elif step == 5:
        step_5()

    if step > 1:
        if st.button("Previous", on_click=go_previous):
            pass

def go_previous():
    st.session_state.current_step -= 1

def wizard_steps():
  init_session_state()
  render_step(st.session_state.current_step)

wizard_steps()
