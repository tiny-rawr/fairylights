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
        prompt=f"3D character with white background {character}",
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
            image.save("projects/_005_avatar_debate/photo.png", format="PNG")

            return "Image saved as 'photo.png'"

    return "Failed to generate the image"