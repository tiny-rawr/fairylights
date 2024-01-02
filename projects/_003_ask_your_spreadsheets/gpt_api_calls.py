from openai import OpenAI
import streamlit as st
import json
import re

def answer_question(user_question, table_rows):
    api_key = st.session_state.api_key
    client = OpenAI(api_key=api_key)

    conversation = [
        {"role": "system", "content": "Answer the following question as fully as possible using only the information provided."},
        {"role": "user", "content": f"Question: {user_question}. Answer that question with this info in plain simple and easy to understand language: {table_rows}"},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    return response.choices[0].message.content


def generate_sql_statement(user_question, table_schemas):
    api_key = st.session_state.api_key
    client = OpenAI(api_key=api_key)

    # Escape backslashes in table_schemas
    table_schemas = re.sub(r'\\', r'\\\\', table_schemas)

    conversation = [
        {"role": "system", "content": "You generate a SQL statement to retrieve data from multiple tables based on a question asked in plain English. Column names in the SQL statement have double quotes around them"},
        {"role": "user", "content": f"Table schema: {table_schemas}"},
        {"role": "user", "content": f"User question: {user_question}"}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "generate_sql_statement",
                    "description": "Read the question, schema and first row of the table carefully, then generate the simplest SQL statement you can. When handling date values, use strftime, use the CAST function to remove leading zeros and the DATE function to extract the date part from a datetime. Specify source name for columns in any join queries. Use the most appropriate columns for each query. Statements should be written in this order: 'SELECT [Columns to Select] FROM [Source Table(s)] WHERE [Conditions if needed] GROUP BY [Columns for Grouping if needed] HAVING [Conditions for Grouping if needed] ORDER BY [Columns for Sorting].''",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_statement": {
                                "type": "string",
                                "description": "A simple SQL statement to get data based on question",
                            },
                        },
                        "required": ["sql_statement"],
                    },
                },
            }
        ],
    )

    return json.loads(response.choices[0].message.tool_calls[0].function.arguments).get('sql_statement')