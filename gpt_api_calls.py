from openai import OpenAI
import json
import streamlit as st

def identify_cognitive_distortions(journal_entry):
    api_key = st.session_state.api_key
    st.write(api_key)
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system",
         "content": "You go through each sentence and extract every single example of a cognitive distortion in a journal entry, using direct quotes only."},
        {"role": "user", "content": journal_entry},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
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
                    "description": "A direct quote from the journal entry that represents a cognitive distortion"
                  }
                }
              },
              "required": ["quotes"]
            }
          },
        }],
    )

    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)

def categorise_cognitive_distortions(quotes):
    api_key = st.session_state.api_key
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system",
         "content": "You categorise cognitive distortions and explain why they are an example of that cognitive distortion"},
        {"role": "user", "content": str(quotes)},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
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

    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)