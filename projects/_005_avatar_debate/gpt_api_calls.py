from io import BytesIO
from PIL import Image
import streamlit as st
from openai import OpenAI
import base64


def create_avatar_image(character_name, character_description):
    api_key = st.session_state.api_key
    client = OpenAI(api_key = api_key)

    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Illustrate the following character in the style of Pixar Animation Studios: {character_name}. with a hint of a blurred natural background to suggest a sunny day. The character should have Pixar's signature appeal, including their approach to lighting and texture. Character description: {character_description}",
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
            filename = f"projects/_005_avatar_debate/{character_image_path}.png"
            image.save(filename, format="PNG")

            return filename

    return "Failed to generate the image"