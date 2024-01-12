import streamlit as st
from projects._005_avatar_debate.gooey_api_calls import generate_talking_avatar
from projects._005_avatar_debate.gpt_api_calls import create_avatar_image

def avatar_debate():
    st.title("Lip Syncing Avatar App")

    #image = "projects/_005_avatar_debate/photo.png"
    audio = "projects/_005_avatar_debate/audio.wav"

    #avatar_url = generate_talking_avatar(image, audio)

    #st.video(avatar_url)

    character_name = st.text_input("Character name", value="Harry Potter")

    submit_button = st.button("Generate Talking Avatar")

    if submit_button:
        api_key = st.session_state.get('api_key', '')

        if not api_key:
            st.error("🔐  Please enter an OpenAI API key in the sidebar to proceed.")
            return

        character_img = create_avatar_image(character_name)
        print(character_img)
        character_image = "projects/_005_avatar_debate/photo.png"

        col1, col2 = st.columns(2)

        with col1:
            st.image(character_image)
            st.write("Caption for Image 1")

        with col2:
            avatar_url = generate_talking_avatar(character_image, audio)
            st.video(avatar_url)

if __name__ == "__main__":
    avatar_debate()
