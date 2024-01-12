import streamlit as st
from projects._005_avatar_debate.gooey_api_calls import generate_talking_avatar
from projects._005_avatar_debate.gpt_api_calls import create_avatar_image

def avatar_debate():
    st.title("Avatar Debate")
    st.write("Watch as your favourite characters debate a given topic, and join in on the conversation if you want. Multi-model project including character image generation, conversation generation, text-to-speech and lip-syncing avatar generation.")

    audio = "projects/_005_avatar_debate/audio.wav"

    character_name = st.text_input("Character Name", value="Alina")
    character_description = st.text_area("Character Appearance", value="Age: 29 years old.\nNationality: Scottish.\nGender: Female.\nEyes: Green eyes.\nHair: Long curly red hair.\nClothing: Deep green spaghetti strap dress with sparkly sequins")

    submit_button = st.button("Generate Talking Avatar")

    character = st.empty()

    if submit_button:
        api_key = st.session_state.get('api_key', '')

        if not api_key:
            st.error("🔐  Please enter an OpenAI API key in the sidebar to proceed.")
            return

        character_image = create_avatar_image(character_name, character_description)

        avatar_url = generate_talking_avatar(character_image, audio)
        character.video(avatar_url)


if __name__ == "__main__":
    avatar_debate()
