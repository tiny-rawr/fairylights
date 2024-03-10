import streamlit as st
from datetime import date

def init_session_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'data' not in st.session_state:
        st.session_state.data = {}
    if 'errors' not in st.session_state:
        st.session_state.errors = {}

def save_input(key, input_data):
    st.session_state.data[key] = input_data
    # Clear error on successful input
    if key in st.session_state.errors:
        del st.session_state.errors[key]

def validate_input(key, value):
    if value:
        save_input(key, value)
        return True
    else:
        st.session_state.errors[key] = f"{key.capitalize()} is required."
        return False

def display_errors():
    for error_message in st.session_state.errors.values():
        st.error(error_message)

def can_proceed(inputs):
    st.session_state.errors.clear()
    validation_passed = True
    for key, value in inputs.items():
        if not validate_input(key, value):
            validation_passed = False
    return validation_passed

def on_click_next(step, inputs=None):
    if inputs is None or can_proceed(inputs):
        if not st.session_state.errors:
            st.session_state.current_step = step

def on_click_previous():
    st.session_state.current_step -= 1

def step_1():
    st.subheader("Step 1: Personal Information")
    name = st.text_input("Name", key='name')
    email = st.text_input("Email", key='email')
    next1 = st.button("Save & Next")
    if next1:
        on_click_next(2, {'name': name, 'email': email})
    display_errors()

def step_2():
    st.subheader("Step 2: Employment Details")
    company = st.text_input("Company Name", key='company')
    position = st.text_input("Position", key='position')
    next2 = st.button("Save & Next")
    if next2:
        on_click_next(3, {'company': company, 'position': position})
    display_errors()

def step_3():
    st.subheader("Step 3: Preferences")
    newsletter = st.checkbox("Subscribe to newsletter?", key='newsletter')
    save_input('newsletter', newsletter)
    next3 = st.button("Save & Next")
    if next3:
        on_click_next(4)
    display_errors()

def step_4():
    st.subheader("Step 4: Schedule Meeting")
    meeting_date = st.date_input("Meeting Date", key='meeting_date', value=date.today())
    next4 = st.button("Save & Next")
    if next4:
        on_click_next(5, {'meeting_date': meeting_date})
    display_errors()

def step_5():
    st.subheader("Step 5: Review & Submit")
    submit = st.button("Submit")
    if submit:
        submit_form()

def submit_form():
    st.write("All submitted data:")
    st.json(st.session_state.data)
    st.success("Form submitted successfully!")

def render_step(step):
    if step > 1:
        if st.button("Previous"):
            on_click_previous()

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

def wizard_steps():
    st.title("Multi-Step Form with Streamlit")
    init_session_state()
    render_step(st.session_state.current_step)