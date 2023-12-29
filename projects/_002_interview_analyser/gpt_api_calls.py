from openai import OpenAI
import json
import streamlit as st
from mixpanel import Mixpanel
import re
from demo_data.veteran_interview_donald_dugan import transcript

#mp = Mixpanel(st.secrets["mixpanel"]["token"])

def create_key_name(text):
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[\s\t\n\r]{2,}', ' ', text)
    return re.sub(r'[ -]', '_', text.lower().strip())

def generate_properties(questions):
    properties = {
        "interview": {
            "type": "object",
            "properties": {}
        }
    }

    for question in questions:
        description = f"A direct quote from the interview that is relevant to '{question}'. Use direct quote only."
        properties["interview"]["properties"][question] = {
            "type": "array",
            "items": {
                "type": "string",
                "description": description
            }
        }

    return properties

def pull_quotes_from_transcript(questions, transcript):
    #api_key = st.session_state.api_key
    api_key = "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"
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system", "content": f"You extract direct relevant quotes for the following transcript based on these: {str(questions)}. This is the transcript"},
        {"role": "user", "content": transcript},
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=conversation,
        tools=[{
            "type": "function",
            "function": {
                "name": "extract_quotes_from_transcript",
                "description": "Extracts direct relevant quote/s from a transcript.",
                "parameters": {
                    "type": "object",
                    "properties": generate_properties(questions),
                },
                "required": [question for question in questions],
            }
        }]
    )

    #response_message =  response.choices[0].message
    return response
    #tool_calls = response_message.tool_calls
    #if tool_calls:
        #return json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    #else:
        #return {"interview": []}

def pull_quotes_from_transcript(transcript, questions):
    #api_key = st.session_state.api_key
    api_key = "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"
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system",
         "content": "You extract direct quotes related to provided areas of interest, from the following transcript:"},
        {"role": "user", "content": transcript},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=conversation,
        tools=[{
            "type": "function",
            "function": {
                "name": "extract_quotes",
                "description": "Extracts quotes related to a provided area of interest.",
                "parameters": {
                    "type": "object",
                    "properties": generate_properties(questions),
                    "required": ["quotes"]
                }
            },
        }],
    )
    response_message =  response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
      return json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    else:
      return {"interview": []}

if __name__ == "__main__":
    #print(transcript)
    questions = ["Why did you join the military?"]
    #print(generate_properties(questions))
    transcript = "I'll never be good at eating cabbage. I love the color pink and my hat is pink. The world is big and blue. The carrot is red. The world is big and green."
    #transcript = "I'll never be good at eating cabbage"
    transcript = "Never have I ever said never"
    questions = ["hat", "cabbage", "world"]
    quotes = pull_quotes_from_transcript(transcript, questions)
    print(quotes)
    print(" ")

