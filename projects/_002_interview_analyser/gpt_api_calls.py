from openai import OpenAI
import streamlit as st
from mixpanel import Mixpanel
#from demo_data.veteran_interview_donald_dugan import transcript

#mp = Mixpanel(st.secrets["mixpanel"]["token"])


def extract_quotes(text, topic):
    #api_key = st.session_state.api_key
    api_key = "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"
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": f"""
Using the text provided below, extract a maximum of 2 quotes that directly address the topic: [User-Provided Topic]. 

1. Identify sections of the text relevant to the topic.
2. Extract quotes from these sections that are directly relevant to the topic.
3. Present these quotes in a list format.

Text for Quote Extraction:
{str(text)}

Topic:
"{topic}"

Ensure that the quotes are contextually accurate and maintain the original meaning from the text.

Do not include any quotes from the interviewer. If there are no relevant quotes, return nothing.

Make sure every quote makes sense in light of the topic.

the JSON output should always have the key "{topic}"
        """},
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=conversation,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    #print(transcript)
    questions = ["Why did you join the military?", "What food did you eat?", "What clothing did you wear?"]
    for question in questions:
        quotes = extract_quotes(transcript, question)
        print(quotes)



