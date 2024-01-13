import streamlit as st
from projects._005_avatar_debate.gooey_api_calls import generate_talking_avatar
from projects._005_avatar_debate.gpt_api_calls import create_avatar_image, text_to_speech, respond_to_message

def generate_new_avatar(character_name, character_description, gender, progress):
    api_key = st.session_state.get('api_key', '')

    if not api_key:
        st.error("🔐  Please enter an OpenAI API key in the sidebar to proceed.")
        return None

    # Step 1: Generate character image
    progress.info("1/3) Generating character image with GPT-Vision...")
    character_image = create_avatar_image(character_name, character_description)

    # Step 2: Generate audio
    intro_message = f"Hello, my name is {character_name}!"
    text_to_speech(gender, intro_message)
    audio = "projects/_005_avatar_debate/audio.wav"

    # Step 3: Generate lip-syncing character
    progress.info("3/3) Generating Lip Syncing character with Gooey.AI")
    avatar_url = generate_talking_avatar(character_image, audio)

    return avatar_url, intro_message

def chat_to_avatar(message, character_image, character_description, gender, progress):
    response = respond_to_message(message, character_description)
    print(response)

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
    st.write("Chat to a custom character. Record or type a message, and your avatar will chat back to you (speech, lip syncing, emotions and gestures).")

    # Initialize conversation history and current index
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []
    if 'current_index' not in st.session_state:
        st.session_state['current_index'] = -1  # -1 indicates no conversation yet

    # Character Information Form
    with st.form("Character Information"):
        character_name = st.text_input("Character Name", value="Alina")
        age = st.number_input("Age", min_value=0, value=29)
        gender = st.radio("Gender", ["Female", "Male", "Other"])
        eye_color = st.text_input("Eye Color", value="Blue")
        hair_description = st.text_input("Hair Description", value="Long curly red hair")
        clothing_description = st.text_input("Clothing Description", value="Deep green hoodie with a cute dinosaur on the front")
        character_description = f"Age: {age} years old.\nGender: {gender}.\nEyes: {eye_color} eyes.\nHair: {hair_description}.\nClothing: {clothing_description}"
        submit_button = st.form_submit_button("Generate Character")

    progress = st.empty()

    # Carousel Navigation
    if len(st.session_state['conversation_history']) > 0:
        current_index = st.session_state['current_index']
        max_index = len(st.session_state['conversation_history']) - 1

        col1, col2 = st.columns(2)
        if current_index > 0 and col1.button('Previous'):
            st.session_state['current_index'] -= 1
            current_index -= 1

        if current_index < max_index and col2.button('Next'):
            st.session_state['current_index'] += 1
            current_index += 1

        # Displaying the Current Conversation Item
        current_item = st.session_state['conversation_history'][current_index]
        st.video(current_item['avatar_url'])
        captions = f"You: {current_item['message']}\n{character_name}: {current_item['response']}"
        st.write(captions)

    # Message Submission
    message = st.text_area("Write message")
    submit = st.button("Submit")

    if submit_button or submit:
        if submit_button:
            # Generate New Avatar
            avatar_url, intro_message = generate_new_avatar(character_name, character_description, gender, progress)
            new_message = "Character Introduction"
            new_response = intro_message
        else:
            # Chat with Avatar
            avatar_url, new_response = chat_to_avatar(message, "projects/_005_avatar_debate/photo.png", character_description, gender, progress)
            new_message = message

        if avatar_url:
            progress.empty()
            st.session_state['conversation_history'].append({
                'message': new_message,
                'response': new_response,
                'avatar_url': avatar_url
            })
            st.session_state['current_index'] = len(st.session_state['conversation_history']) - 1

            # Update Carousel
            st.experimental_rerun()

if __name__ == "__main__":
    avatar_debate()
