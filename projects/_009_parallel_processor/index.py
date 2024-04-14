from projects._009_parallel_processor.generate_requests import generate_chat_completion_requests
from projects._009_parallel_processor.api_request_parallel_processor import process_api_requests_from_file
import asyncio
import logging
import streamlit as st
import pandas as pd
import random
import json
import requests

def load_prompts(url):
    df = pd.read_csv(url)
    prompts = df.set_index('Name')['Prompt'].to_dict()
    return prompts


class StreamlitLogHandler(logging.Handler):
    def __init__(self, placeholder):
        super().__init__()
        self.placeholder = placeholder

    def emit(self, record):
        if record.levelno == logging.INFO:
            log_entry = self.format(record)
            self.placeholder.info(log_entry)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def read_results_from_jsonl(jsonl_filepath):
    results = {}
    with open(jsonl_filepath, 'r') as file:
        for line in file:
            data = json.loads(line)
            if len(data) > 1 and 'choices' in data[1] and len(data[1]['choices']) > 0:
                choice = data[1]['choices'][0]
                if 'message' in choice and 'content' in choice['message']:
                    generated_content = choice['message']['content'].strip()
                    # Use the prompt from the first dictionary as the key
                    prompt_key = data[0]['messages'][-1]['content'].strip()
                    results[prompt_key] = generated_content
    return results



def reverse_prompt_data(data):
    return data[::-1]

def parallel_processor():
    if 'errors' not in st.session_state:
        st.session_state.errors = {}

    st.title("📊 Run 1000s of GPT tasks fast: One prompt, different data")
    with st.expander("About this App"):
        st.info("This app lets you bulk process thousands of GPT tasks in under 2 minutes. Each task uses the same prompt, but different data.")
        st.write("""
        1. Upload a spreadsheet where each row represents a different "thing". E.g. real estate properties, animals ready for adoption, product details etc.
        2. Choose the data you want to include in your GPT prompt (if generating profile bios, you don't need profile photo urls and slugs for example).
        3. Write your prompt instructions: Tell GPT what you want it to do with the data (e.g. write a bio).
        4. Run the tasks (you can run all rows or just some of them), they will be processed in parallel for speed.
        """)
        st.write("Watch the demo video below for use-case ideas:")

    st.subheader("1: Upload your data")
    st.markdown("Upload a spreadsheet containing your scraped data, or use the demo data. The demo data includes scraped [Australian Real Estate data (a free dataset from kaggle)](https://www.kaggle.com/datasets/smmmmmmmmmmmm/australia-real-estate-dataset), which we will use to bulk write bios.")

    use_demo = st.checkbox("Use demo data")
    csv_file = None if use_demo else st.file_uploader("Choose a CSV file", type=['csv'])

    if use_demo:
        csv_data = pd.read_csv("projects/_009_parallel_processor/demo_data/aus_real_estate.csv")
        csv_data.index += 1  # Shift index to start from 1
    else:
        csv_data = pd.read_csv(csv_file) if csv_file else None
        if csv_data is not None:
            csv_data.index += 1  # Shift index to start from 1

    if csv_data is not None:
        st.session_state['original_csv'] = csv_data
        st.write(csv_data)
        st.session_state.errors.pop('original_csv', None)

    st.subheader("2: Choose data to feed into prompt")

    if 'original_csv' in st.session_state and st.session_state['original_csv'] is not None:
        df = st.session_state['original_csv']

        options = st.multiselect('Choose the data you want to include in each bio:', df.columns.tolist(),
                                 default=df.columns.tolist())
        if options:
            st.write("Here is the data you selected for 3 random rows in your spreadsheet")
            bio_data_details = []
            for _, row in df.iterrows():
                row_data = [f"{option}: {row[option]}," for option in options if pd.notna(row[option])]
                bio_data_details.append("\n".join(row_data))

            st.session_state['bio_data_details'] = bio_data_details

            if bio_data_details:
                random_bios = random.sample(bio_data_details, 3)
                cols = st.columns(3)
                for index, bio in enumerate(random_bios):
                    with cols[index]:
                        st.info(bio)
    else:
        st.warning("📊 Upload a spreadsheet or use demo data first.")

    st.subheader("3: Write prompt instructions")
    st.write("Tell your LLM what you want it to do with your data. You can try one of our demo prompts below or write your own.")

    with st.expander("📝Prompt writing tips"):
        st.markdown("Prompt writing tips from [OpenAI's Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering/six-strategies-for-getting-better-results):")
        st.markdown("- **Write clear instructions:** Describe the steps needed to complete a task. If outputs are too long, ask for brief replies and specify the format you want.")
        st.markdown("- **Give good examples**: Find a profile you really like and ask an LLM to describe it's writing style and tone. Use that to help you write better bio-writing prompt instructions.")
        st.markdown("- **Split tasks into simpler subtasks:** For example, if you want both a long and short bio to be used on different parts of the site, create a long bio first and then use that long bio to create the short one in two separate tasks.")
        st.markdown("- **Adopt a persona:** Ask the model to pretend they are the specialist writing their own bio.")
        st.markdown("- **Follow-ups**: If you find yourself adding follow-up prompts to modify some part of the output, that might be a good candidate to add back into the original prompt.")

    prompts = load_prompts("https://docs.google.com/spreadsheets/d/e/2PACX-1vRvi_faLdtyiU0OaB5nJcnVN8a3JJVpZ5lQSi7jn35P9qwoTzg_0jTAEy1pYIU6XYha88TGf-VYXGEH/pub?gid=0&single=true&output=csv")
    selected_prompt = st.selectbox("Use a demo prompt:", options=list(prompts.keys()), index=0, key="prompt_selection")
    prompt = st.text_area("Write your own prompt:", value=prompts[selected_prompt], height=300, key="prompt_instructions")

    st.session_state["prompt"] = prompt

    st.subheader("4: Perform task with LLM using your data and prompt")
    st.write("Before committing to processing thousands of records, test your prompt with just a few rows first.")


    if 'original_csv' in st.session_state and st.session_state['original_csv'] is not None:
        total_rows = len(st.session_state['original_csv'])

        row_range = st.slider(
            'Select rows to process',
            1,
            total_rows,
            (1, min(5, total_rows))
        )

        selected_rows = st.session_state['original_csv'].iloc[
                        row_range[0] - 1:row_range[1]]  # Adjust indexing for 0-based indexing

        modified_rows = selected_rows[options].copy()

        for index, row in modified_rows.iterrows():
            row_data = [f"{option}: {row[option]}," for option in options if pd.notna(row[option])]
            prompt_data = "\n".join(row_data)
            modified_rows.at[index, 'prompt_data'] = prompt_data

        for index, row in modified_rows.iterrows():
            if not options:
                options = modified_rows.columns.tolist()  # Select all columns if options is empty
            row_data = [f"{option}: {row[option]}," for option in options if pd.notna(row[option])]
            prompt_data = "\n".join(row_data)
            modified_rows.at[index, 'prompt_data'] = prompt_data

        modified_rows_placeholder = st.empty()
        modified_rows_placeholder.write(modified_rows)

        num_tasks = row_range[1] - row_range[0] + 1
        run_button_text = f"Run {num_tasks} tasks" if num_tasks > 1 else "Run 1 task"

        run_button_placeholder = st.empty()
        log_placeholder = st.empty()

        if run_button_placeholder.button(run_button_text):
            if 'processed_csv' not in st.session_state:
                st.session_state['processed_csv'] = selected_rows[options].copy()
                st.session_state['processed_csv']['prompt_data'] = modified_rows['prompt_data'].copy()
                st.session_state['processed_csv']['generated_content'] = None
            logger.addHandler(StreamlitLogHandler(log_placeholder))
            modified_rows_placeholder.empty()
            run_button_placeholder.empty()

            st.session_state['download_button_placeholder'] = st.empty()

            # Generate requests JSONL file
            requests_filepath = "projects/_009_parallel_processor/example_requests_to_chat_completion.jsonl"
            requests_output_filepath = "projects/_009_parallel_processor/example_requests_to_chat_completion_results.jsonl"
            generate_chat_completion_requests(requests_filepath, modified_rows['prompt_data'], st.session_state["prompt"])

            info_placeholder = st.empty()

            api_key = st.session_state.get('api_key', '')

            if not api_key:
                info_placeholder.error("🔐  Please enter an OpenAI API key in the sidebar.")
                return

            # Parallel process the requests
            asyncio.run(
                process_api_requests_from_file(
                    requests_filepath=requests_filepath,
                    save_filepath=requests_output_filepath,
                    request_url="https://api.openai.com/v1/chat/completions",
                    api_key=api_key,  # Replace with your actual API key
                    max_requests_per_minute=7500, #75% of our max RPM limit.
                    max_tokens_per_minute=750000, #75% of our max TPM limit.
                    token_encoding_name="cl100k_base",
                    max_attempts=3,
                    logging_level=logging.INFO,
                )
            )

            # Read the results from the JSONL file and update the 'generated_content' field in the processed CSV
            results = read_results_from_jsonl(requests_output_filepath)
            for index, row in st.session_state['processed_csv'].iterrows():
                prompt_data = row['prompt_data']
                if prompt_data in results:
                    st.session_state['processed_csv'].at[index, 'generated_content'] = results[prompt_data]

            # Create a new DataFrame containing all original data for selected rows, 'prompt_data', and 'generated_content'
            all_selected_rows = st.session_state['original_csv'].iloc[row_range[0] - 1:row_range[1]].copy()
            all_selected_rows['prompt_data'] = modified_rows['prompt_data'].copy()
            all_selected_rows['generated_content'] = st.session_state['processed_csv']['generated_content'].copy()

            st.write("Here is the processed data for the selected rows:")
            st.write(all_selected_rows)

            # Create a download button for the new DataFrame
            download_all_selected_rows_button_placeholder = st.empty()
            download_all_selected_rows_button_placeholder.download_button(
                "Download your content",
                all_selected_rows.to_csv(index_label='Row').encode('utf-8'),
                "processed_results_all_selected_rows.csv",
                "text/csv"
            )

    else:
        st.warning("📊 Upload a spreadsheet or use demo data first.")


if __name__ == "__main__":
    parallel_processor()