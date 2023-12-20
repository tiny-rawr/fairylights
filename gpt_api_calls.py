from openai import OpenAI
import json
import streamlit as st
from mixpanel import Mixpanel
import re

mp = Mixpanel(st.secrets["mixpanel"]["token"])

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
        properties["interview"]["properties"][create_key_name(question)] = {
            "type": "array",
            "items": {
                "type": "string",
                "description": description
            }
        }

    return properties

def pull_quotes_from_transcript(questions, transcript):
    api_key = st.session_state.api_key
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system", "content": f"You extract direct relevant quotes for the following transcript based on these: {questions}. This is the transcript"},
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
                "required": ["interview"],
            }
        }]
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    else:
        return {"interview": []}

def identify_cognitive_distortions(journal_entry):
    api_key = st.session_state.api_key
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system",
         "content": "You go through each sentence and extract every single example of a cognitive distortion in a journal entry, using direct quotes only."},
        {"role": "user", "content": journal_entry},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=conversation,
        tools=[{
            "type": "function",
            "function": {
                "name": "identify_cognitive_distortions",
                "description": "Identifies all cognitive distortion present in a journal entry and complements journal entry provider.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "quotes": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A direct quote from the journal entry that represents a cognitive distortion."
                            }
                        }
                    },
                    "required": ["quotes"]
                }
            },
        }],
    )

    mp.track(st.session_state['session_id'], "OpenAI API Call", {
        "event": "OpenAI API Call",
        "Model": response.model,
        "Project": "Thought Checker",
        "Method": "identify_cognitive_distortions",
        "Input tokens": response.usage.prompt_tokens,
        "Output tokens": response.usage.completion_tokens
    })

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    else:
        return {"quotes": []}


def categorise_cognitive_distortions(quotes):
    api_key = st.session_state.api_key
    client = OpenAI(api_key=api_key)

    if len(quotes) > 0:

        conversation = [
            {"role": "system",
             "content": "You categorise cognitive distortions and explain why they are an example of that cognitive distortion"},
            {"role": "user", "content": str(quotes)},
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=conversation,
            tools=[{
                "type": "function",
                "function": {
                    "name": "identify_cognitive_distortions",
                    "description": "Identifies all cognitive distortion present in a journal entry.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "thinking_patterns": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "quote": {
                                            "type": "string",
                                            "description": "A direct quote from the journal entry that most represents this thinking pattern"
                                        },
                                        "thinking_pattern": {
                                            "type": "string",
                                            "enum": ["Black or white thinking", "Overgeneralisation", "Labelling",
                                                     "Fortune telling", "Mind reading", "Blaming",
                                                     "Catastrophising",
                                                     "Discounting the positives", "Emotional reasoning"]
                                        },
                                        "explanation": {
                                            "type": "string",
                                            "description": "Explain why this is an example of the thinking pattern and suggest a more helpful reframe."
                                        },
                                    },
                                    "required": ["quote", "thinking_pattern", "explanation"]
                                }
                            }
                        },
                        "required": ["thinking_patterns"]
                    },
                },
            }],
        )
        mp.track(st.session_state['session_id'], "OpenAI API Call", {
            "event": "OpenAI API Call",
            "Model": response.model,
            "Project": "Thought Checker",
            "Method": "categorise_cognitive_distortions",
            "Input tokens": response.usage.prompt_tokens,
            "Output tokens": response.usage.completion_tokens
        })

        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    else:
        return {"thinking_patterns": []}


if __name__ == "__main__":
    questions = ["What motivated you to join the army?"]
    #print(generate_properties(questions))


    #questions = ["What motivated you to join the army?", "What did you do while in the army", "What was your training like?"]
    #questions = ["What motivated you to join the army?", "What did you do while in the army"]
    questions = ["What motivated you to join the army?"]
    print(generate_properties(questions))
    quotes = pull_quotes_from_transcript(questions, interview)
    print(quotes)
