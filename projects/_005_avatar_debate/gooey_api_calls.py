import requests
import json
import streamlit as st


def generate_talking_avatar(image_filepath, audio_filepath):
    api_key = st.secrets["gooey"]["gooey_api_key"]

    files = [
        ("input_face", open(image_filepath, "rb")),
        ("input_audio", open(audio_filepath, "rb")),
    ]

    payload = {}

    try:
        response = requests.post(
            "https://api.gooey.ai/v2/Lipsync/form/",
            headers={"Authorization": "Bearer " + api_key},
            files=files,
            data={"json": json.dumps(payload)},
        )
        response.raise_for_status()

        result = response.json()
        return result['output']['output_video']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    image_file = "path_to_your_image.gif"
    audio_file = "path_to_your_audio.wav"

    generate_talking_avatar(image_file, audio_file)