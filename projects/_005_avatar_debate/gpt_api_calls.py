from io import BytesIO
from PIL import Image
import streamlit as st
from openai import OpenAI
import base64


def create_avatar_image(character):
    api_key = st.session_state.api_key
    client = OpenAI(api_key = api_key)

    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Create a character image in a 3D style for {character}. There should be a single character.",
        size="1024x1792",
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
            character_image_path = character.lower().replace(" ", "_")
            filename = f"projects/_005_avatar_debate/{character_image_path}.png"
            image.save(filename, format="PNG")

            return filename

    return "Failed to generate the image"