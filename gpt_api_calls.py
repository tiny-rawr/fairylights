from openai import OpenAI
import json


def identify_cognitive_distortions(api_key, journal_entry):
    client = OpenAI()
    client.api_key = api_key

    conversation = [
        {"role": "system",
         "content": "You generate a SQL statement to retrieve data from multiple tables based on a question asked in plain English. Column names in the SQL statement have double quotes around them"},
        {"role": "user", "content": journal_entry},
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

    return json.loads(response.choices[0].message.tool_calls[0].function.arguments).get('quotes')