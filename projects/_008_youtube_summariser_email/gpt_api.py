from openai import OpenAI
import streamlit as st

def summarise_transcript(instructions, transcript):
    openai_api_key = st.secrets["openai"]["openai_api_key"]
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": transcript}
        ]
    )

    return response.choices[0].message.content