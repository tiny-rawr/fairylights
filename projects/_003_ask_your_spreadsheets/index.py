import streamlit as st
import pandas as pd
import sqlite3
from projects._003_ask_your_spreadsheets.gpt_api_calls import generate_sql_statement

def project_details():
    st.title('📈 Ask Your Database')
    st.warning('Use-case in progress 🥰 (build in public)')
    st.write("Upload your databases (as CSV files), and ask questions in plain english. This program will auto-generate and execute SQL queries to retrieve the data needed to answer your question. It can also generate question ideas to help you get the most business insight from your data.")

    with st.expander("✨ See project details"):
        st.subheader("Why I built this")
        st.write("One of the founders at my co-working space said one of their biggest pain points for their data business was being able to answer complex questions about their industry based on the data because 1) The data was spread across multiple spreadsheets and was difficult to find, and 2) Writing queries to retrieve data based on complex questions required time and expertise. I thought that GenAI could be used to solve this.")
        st.warning("I initially planned to let people connect to their own database, like MySQL/PostgreSQL by entering their database connection details, but decided against this for security reasons.")
        st.subheader("Ways to use this")
        st.markdown("- 🩺 **Healthcare Data**: Anonymised data around patient records, treatment details, and outcomes data. This would allow for queries like, 'Show the average recovery time for patients aged 60-70 with a specific condition,' or create questions such as, 'Which treatments have the highest success rate for chronic diseases?'")
        st.markdown("- 🏘️ **Real-estate Market Trends**:  Use datasets on property sales, prices, demographics, and economic indicators. This can help answer questions like, 'What is the average price of three-bedroom houses in a specific area?' or generate queries like, 'What factors most significantly affect property values in urban areas?'")
        st.markdown("- 🌳 **Environmental Data Analysis**: Use datasets related to climate, pollution levels, or wildlife populations. This might answer queries like, 'What has been the average air quality index in urban areas over the past five years?' and generate questions like, 'What is the correlation between temperature changes and wildlife migration patterns?'")
        st.markdown("- 🚂 **Transportation and Logistics**: Work with data related to public transportation usage, traffic patterns, and logistic operations. This can help in answering questions such as, 'What are the peak hours for public transportation usage in major cities?' or suggest questions like, 'How do weather conditions affect transportation delays?'")
        st.subheader("Limitations")
        st.write('I initially planned to let people connect to their own database, like MySQL/PostgreSQL by entering their database connection details, but decided against this for security reasons, so you have to export your databases to CSV files and upload each time you want to ask questions.')
        st.error("⚠️ **Accuracy**: SQL statements are not always correct, and can struggle with very complex queries involving 2+ datasets.")
        st.subheader("Extra")
        st.markdown("- 💌 Read the [newsletter about this](https://fairylightsai.substack.com/p/4-ask-questions-about-interview-transcripts).")
        st.write("")

def get_table_schemas_with_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    schemas_with_data = ""

    for table_name in table_names:
        cursor.execute(f"PRAGMA table_info('{table_name[0]}')")
        columns = cursor.fetchall()
        table_schemas = f"CREATE TABLE {table_name[0]} (\n"
        data_query = f"SELECT * FROM {table_name[0]} LIMIT 1;"
        cursor.execute(data_query)
        first_row_data = cursor.fetchone()

        for column in columns:
            column_name = column[1].replace(' ', '_')
            column_type = column[2]
            # Exclude long text content by checking column type
            if "text" not in column_type.lower():
                table_schemas += f"    {column_name} {column_type},\n"

        table_schemas = table_schemas.rstrip(",\n") + "\n);\n\n"
        # Append the first row data (excluding long text content)
        table_schemas += f"First Row Data: {first_row_data}\n\n"
        schemas_with_data += table_schemas

    return schemas_with_data

def execute_sql_statement(conn, sql_statement):
    try:
        result = pd.read_sql_query(sql_statement, conn)
        return result
    except Exception as e:
        return None

def step_1():
    st.title("Step 1/2: Upload CSV Files")
    uploaded_files = st.file_uploader("Upload CSV Files", type=["csv"], accept_multiple_files=True)

    if uploaded_files:
        conn = sqlite3.connect(':memory:')
        dataframes = {}

        for file in uploaded_files:
            df = pd.read_csv(file)
            df.columns = [col.replace(' ', '_') for col in df.columns]
            table_name = file.name.split('.')[0]
            dataframes[file.name] = df
            df.to_sql(table_name, conn, index=False)

        st.session_state['conn'] = conn  # Save the connection to session state
        st.session_state['dataframes'] = dataframes  # Save dataframes to session state

        if st.button("Finished Uploading Data"):
            st.session_state.step = 2

def step_2():
    st.title("Step 2/2: Ask a Question")
    st.write("Enter a question in plain English")

    question = st.text_input("Question:")
    if st.button("Ask Question"):
        conn = st.session_state['conn']
        table_schemas = get_table_schemas_with_data(conn)  # Use the function from your first example
        sql_statement = generate_sql_statement(question, table_schemas)

        if sql_statement:
            st.write("Generated SQL Query:")
            st.code(sql_statement, language='sql')

            result_df = execute_sql_statement(conn, sql_statement)  # Use the function from your first example

            if result_df is not None and not result_df.empty:
                st.write("Results:")
                st.dataframe(result_df)
            else:
                st.info("No results or unable to execute the query.")
        else:
            st.warning("Failed to generate SQL statement.")

def ask_your_spreadsheets():
    project_details()

    if 'step' not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        step_1()
    elif st.session_state.step == 2:
        step_2()