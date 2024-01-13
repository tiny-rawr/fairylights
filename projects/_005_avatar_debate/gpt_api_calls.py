from io import BytesIO
from PIL import Image
import streamlit as st
from openai import OpenAI
import base64

def respond_to_message(message, character_description):
    api_key = st.session_state.api_key
    client = OpenAI(api_key = api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. Respond to the following message in 1-3 sentences. Also, this is a description of the character you are in case you are asked: {character_description}"},
            {"role": "user", "content": message},
        ]
    )

    return response.choices[0].message.content

def create_avatar_image(character_name, character_description):
    api_key = st.session_state.api_key
    client = OpenAI(api_key = api_key)

    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Illustrate the following character in the style of 3D Pixar Animation Studios: {character_name}, {character_description}. The character will face the viewer with a hint of a blurred natural background to suggest a sunny day. The overall effect is one of a three-dimensional appearance on a two-dimensional medium, with a careful balance between detail and softness that gives the character a lifelike presence.",
        size="1024x1024",
        quality="standard",
        n=1,
        response_format="b64_json",
    )

    if response:
        image_data = response.data[0].b64_json

        if image_data:
            # Decode the base64 string to bytes
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            character_image_path = character_name.lower().replace(" ", "_")
            filename = f"projects/_005_avatar_debate/photo.png"
            image.save(filename, format="PNG")

            return filename

    return "Failed to generate the image"

def text_to_speech(gender="female", text="Hello, my name is Alina!"):
    api_key = st.session_state.api_key
    client = OpenAI(api_key=api_key)

    gender = gender.lower()
    voice = "shimmer"

    if gender == "female":
        voice = "nova"
    elif gender == "male":
        voice = "onyx"

    speech_file_path = "projects/_005_avatar_debate/audio.wav"
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )

    response.stream_to_file(speech_file_path)

if __name__ == "__main__":
    print(respond_to_message("Hello"))