from openai import OpenAI
import streamlit as st
from mixpanel import Mixpanel
#from demo_data.veteran_interview_donald_dugan import transcript

#mp = Mixpanel(st.secrets["mixpanel"]["token"])


def extract_quotes(text, topic):
    api_key = st.session_state.api_key
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system", "content": "You are a helpful assistant designed to extract a single relevant quote output as JSON."},
        {"role": "user", "content": f"""
Using the text provided below, extract one quote that directly address the topic: [User-Provided Topic]. 

1. Extract the most relevant quote from the text that is directly relevant to the topic. If there isn't a relevant quote, return nothing.
2. Make sure that the quote makes sense in light of the topic. If it doesn't, find another.
3. Present this quote as a string.

Text for Quote Extraction:
{str(text)}

Topic:
"{topic}"

Ensure that the quote is contextually accurate and maintains the original meaning from the text.

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



