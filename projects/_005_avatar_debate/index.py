import streamlit as st
from projects._005_avatar_debate.gooey_api_calls import generate_talking_avatar
from projects._005_avatar_debate.gpt_api_calls import create_avatar_image

def avatar_debate():
    st.title("Avatar Debate")
    st.write("Watch as your favourite characters debate a given topic, and join in on the conversation if you want. Multi-model project including character image generation, conversation generation, text-to-speech and lip-syncing avatar generation.")

    audio = "projects/_005_avatar_debate/audio.wav"

    character_name = st.text_input("Character name", value="Harry Potter")
    character2_name = st.text_input("Character name", value="Voldemort")

    submit_button = st.button("Generate Talking Avatar")

    if submit_button:
        api_key = st.session_state.get('api_key', '')

        if not api_key:
            st.error("🔐  Please enter an OpenAI API key in the sidebar to proceed.")
            return


        # Generate character images
        character_image = create_avatar_image(character_name)
        character2_image = create_avatar_image(character2_name)

        col1, col2 = st.columns(2)

        with col1:
            character = st.empty()
            caption = st.empty()
            character.image(character_image)
            caption.write(f"Caption for Image {character_name}")


        with col2:
            character2 = st.empty()
            caption2 = st.empty()
            print(character2_image)
            character2.image(character2_image)
            caption2.write(f"Caption for Image {character2_name}")

        avatar_url = generate_talking_avatar(character_image, audio)
        character.video(avatar_url)
        avatar2_url = generate_talking_avatar(character2_image, audio)
        character2.video(avatar2_url)


if __name__ == "__main__":
    avatar_debate()
