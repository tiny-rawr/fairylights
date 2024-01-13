import streamlit as st
from projects._005_avatar_debate.gooey_api_calls import generate_talking_avatar
from projects._005_avatar_debate.gpt_api_calls import create_avatar_image, text_to_speech, respond_to_message

def generate_new_avatar(character_name, character_description, gender, progress):
    api_key = st.session_state.get('api_key', '')

    if not api_key:
        st.error("🔐 Please enter an OpenAI API key in the sidebar to proceed.")
        return None

    # Step 1: Generate character image
    progress.info("1/3) Generating character image with GPT-Vision...")
    character_image = create_avatar_image(character_name, character_description)

    # Step 2: Generate audio
    progress.info("2/3) Generating audio with OpenAI's text-to-speech")
    intro_message = f"Hello, my name is {character_name}!"
    text_to_speech(gender, intro_message)
    audio = "projects/_005_avatar_debate/audio.wav"

    # Step 3: Generate lip-syncing character
    progress.info("3/3) Generating Lip Syncing character with Gooey.AI")
    avatar_url = generate_talking_avatar(character_image, audio)

    return avatar_url, intro_message

def chat_to_avatar(message, character_image, character_description, gender):
    response = respond_to_message(message, character_description)
    progress = st.empty()

    # Step 2: Generate audio
    progress.info("1/2) Generating Audio from response")
    text_to_speech(gender, response)
    audio = "projects/_005_avatar_debate/audio.wav"

    # Step 3: Generate lip-syncing character
    progress.info("2/2) Generating Lip Syncing character with Gooey.AI")
    avatar_url = generate_talking_avatar(character_image, audio)

    return avatar_url, response

def avatar_debate():
    st.title("Chatty Character")
    st.markdown("Create a custom character, and chat to them via text. They'll respond to you by actually speaking. You can swap out the free lip-syncing API I used ([GooeyAI](gooey.ai/lipsync-maker)) for a higher-quality paid version for better results (like [Verbalate](verbalate.ai), [HeyGen](heygen.com) or [D-ID](https://www.d-id.com/)).")

    with st.expander("✨ See project details"):
        st.subheader("Why I built this")
        st.markdown("After creating the talking avatar demo video using online tools in the previous project, I wanted to play around with using APIs to do this programatically.")
        st.subheader("Ways to use this")
        st.markdown("- 🎙️ **Virtual debates**: Create two avatars and get them to have a debate on a topic where they respond to each other. Maybe you could jump in on the conversation too!")
        st.markdown("- 🎓 **Generate 3D avatar lectures**: Learn science by generating an avatar of Richard Feynman and ask him to explain physics in 6 easy pieces. The character chatting can be more engaging that reading text responses.")
        st.subheader("Limitations")
        st.error("⚠️ **Low-quality lip-syncing**: I'm using a free API for the lip-syncing because all of the high-quality lip-syncing API's are expensive. If I were to turn this into a production-quality app the investment would be worth it.")
        st.error("⚠️ **Not real-time (yet)**: The biggest bottleneck is the image generation at the start. The latency of the other steps also means that the conversation isn't real-time.")
        st.write("")

    # Initialize conversation history and character information
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []
    if 'character_info' not in st.session_state:
        st.session_state['character_info'] = {
            'character_name': 'Alina',
            'age': 29,
            'gender': 'Female',
            'eye_color': 'Blue',
            'hair_description': 'Long curly red hair',
            'clothing_description': 'Deep green hoodie with a cute dinosaur on the front'
        }

    # Character Information Form
    if len(st.session_state['conversation_history']) == 0:
        with st.form("Character Information"):
            st.session_state['character_info']['character_name'] = st.text_input("Character Name", st.session_state['character_info']['character_name'])
            st.session_state['character_info']['age'] = st.number_input("Age", min_value=0, value=st.session_state['character_info']['age'])
            st.session_state['character_info']['gender'] = st.radio("Gender", ["Female", "Male", "Other"], index=["Female", "Male", "Other"].index(st.session_state['character_info']['gender']))
            st.session_state['character_info']['eye_color'] = st.text_input("Eye Color", st.session_state['character_info']['eye_color'])
            st.session_state['character_info']['hair_description'] = st.text_input("Hair Description", st.session_state['character_info']['hair_description'])
            st.session_state['character_info']['clothing_description'] = st.text_input("Clothing Description", st.session_state['character_info']['clothing_description'])
            submit_button = st.form_submit_button("🚀 Generate Character")

            if submit_button:
                # Extract character details from session state
                character_name = st.session_state['character_info']['character_name']
                age = st.session_state['character_info']['age']
                gender = st.session_state['character_info']['gender']
                eye_color = st.session_state['character_info']['eye_color']
                hair_description = st.session_state['character_info']['hair_description']
                clothing_description = st.session_state['character_info']['clothing_description']
                character_description = f"Age: {age} years old.\nGender: {gender}.\nEyes: {eye_color} eyes.\nHair: {hair_description}.\nClothing: {clothing_description}"

                progress = st.empty()
                avatar_url, intro_message = generate_new_avatar(character_name, character_description, gender, progress)
                if avatar_url:
                    st.session_state['conversation_history'].append({
                        'message': "Character Introduction",
                        'response': intro_message,
                        'avatar_url': avatar_url
                    })
                    st.experimental_rerun()

    # Carousel Navigation
    if len(st.session_state['conversation_history']) > 0:
        current_index = st.session_state.get('current_index', 0)
        max_index = len(st.session_state['conversation_history']) - 1

        col1, col2 = st.columns(2)
        if current_index > 0 and col1.button(f'Previous'):
            st.session_state['current_index'] -= 1
            current_index -= 1

        if current_index < max_index and col2.button(f'Next'):
            st.session_state['current_index'] += 1
            current_index += 1

        # Displaying the Current Conversation Item
        current_item = st.session_state['conversation_history'][current_index]
        st.video(current_item['avatar_url'])
        character_name = st.session_state['character_info']['character_name'] # Define character_name
        captions = f"You: {current_item['message']}\n{character_name}: {current_item['response']}"
        st.write(captions)

    # Message Submission
    if len(st.session_state['conversation_history']) > 0:
        message = st.text_area("Write message")
        submit = st.button("💌 Send Message")

        if submit:
            character_description = f"Age: {st.session_state['character_info']['age']} years old.\nGender: {st.session_state['character_info']['gender']}.\nEyes: {st.session_state['character_info']['eye_color']} eyes.\nHair: {st.session_state['character_info']['hair_description']}.\nClothing: {st.session_state['character_info']['clothing_description']}"
            gender = st.session_state['character_info']['gender']
            avatar_url, response = chat_to_avatar(message, "projects/_005_avatar_debate/photo.png", character_description, gender)
            if avatar_url:
                st.session_state['conversation_history'].append({
                    'message': message,
                    'response': response,
                    'avatar_url': avatar_url
                })
                st.session_state['current_index'] = len(st.session_state['conversation_history']) - 1

                # Update Carousel
                st.experimental_rerun()

if __name__ == "__main__":
    avatar_debate()
