import streamlit as st
import requests
from projects._005_avatar_debate.gooey_api_calls import generate_talking_avatar
api_key = "sk-LaCFnN1i18qlrf6wVNPKER7dDEwPJjWe1sJl19RMQnpIv23V"
import json

def avatar_debate():
    st.title("Lip Syncing Avatar App")

    image = "projects/_005_avatar_debate/photo.png"
    audio = "projects/_005_avatar_debate/audio.wav"

    avatar_url = generate_talking_avatar(image, audio)

    st.video(avatar_url)


if __name__ == "__main__":
    avatar_debate()
