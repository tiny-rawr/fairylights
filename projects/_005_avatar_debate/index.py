import streamlit as st
from projects._005_avatar_debate.gooey_api_calls import generate_talking_avatar
from projects._005_avatar_debate.gpt_api_calls import create_avatar_image, text_to_speech


def avatar_debate():
    st.title("Chatty Character")
    st.write(
        "Chat to a custom character. Record or type a message, and your avatar will chat back to you (speech, lip syncing, emotions and gestures).")

    form_input = st.empty()

    with form_input.form("Character Information"):
        character_name = st.text_input("Character Name", value="Alina")
        age = st.number_input("Age", min_value=0, value=29)
        gender = st.radio("Gender", ["Female", "Male", "Other"])
        eye_color = st.text_input("Eye Color", value="Blue")
        hair_description = st.text_input("Hair Description", value="Long curly red hair")
        clothing_description = st.text_input("Clothing Description",
                                             value="Deep green hoodie with a cute dinosaur on the front")

        character_description = f"Age: {age} years old.\nGender: {gender}.\nEyes: {eye_color} eyes.\nHair: {hair_description}.\nClothing: {clothing_description}"
        submit_button = st.form_submit_button("Generate Character")

    character = st.empty()
    progress = st.empty()

    if submit_button:
        api_key = st.session_state.get('api_key', '')

        if not api_key:
            st.error("🔐  Please enter an OpenAI API key in the sidebar to proceed.")
            return

        progress.info("1/3) Generating character image with GPT-Vision...")
        character_image = create_avatar_image(character_name, character_description)

        progress.info("2/3) Generating Audio from response")
        text_to_speech(gender, f"Hello, my name is {character_name}!")
        audio = "projects/_005_avatar_debate/audio.wav"

        progress.info("3/3) Generating Lip Syncing character with Gooey.AI")
        avatar_url = generate_talking_avatar(character_image, audio)
        character.video(avatar_url)
        progress.empty()
        form_input.empty()


    #with st.form("Messenger"):
        #message = st.input_area("Write a message")
        #submit = st.submit_button("Send message")

        #if submit("")

if __name__ == "__main__":
    avatar_debate()
