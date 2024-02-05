import streamlit as st
import pandas as pd
import asyncio
from projects._007_parallel_processor.generate_request_file import generate_chat_completion_requests
from projects._007_parallel_processor.save_to_csv import save_generated_data_to_csv
from projects._007_parallel_processor.process_requests import process_api_requests_from_file

def parallel_processor():
    st.title("Parallel Processor")
    st.markdown("Bulk process 1000s of GPT-3.5-Turbo-16k requests in a couple of minutes (depending on your OpenAI Tier).")

    with st.expander("✨ See project details (and demo video)"):
        st.subheader("Why I built this")
        st.write("Do x")
        st.subheader("Demo video")
        # st.video("demo_videos/chatty_avatar_demo.mp4")
        st.subheader("Ways to use this")
        st.markdown("- 🎙️ **Cat**: Text")
        st.subheader("Limitations")
        st.error("⚠️ **Cat**: Text.")
        st.write("")

    st.subheader("Step 1: Upload your data")
    st.write("Lets say you want to translate 1000 blog posts into a different language. The first step is to put each blog post it it's own cell in column A of your spreadsheet. Then export it as a CSV file and upload it here.")

    # Set the default CSV file path
    csv_file_path = "projects/_007_parallel_processor/input.csv"

    upload_csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if upload_csv_file:
        # Use the uploaded file if available
        df = pd.read_csv(upload_csv_file, header=None)
        csv_file_path = upload_csv_file.name  # Update the CSV file path
    else:
        df = pd.read_csv(csv_file_path, header=None)

    with st.expander("👀 View your uploaded data"):
      st.write("If you haven't uploaded your own data yet, you will see our demo data.")
      st.write(df.iloc[:, 0].rename("Your Data"))

    st.subheader("Step 2: Write a prompt")
    st.write("Write instructions for what you want to do with a single instance of your data. In this case, we will instruct ChatGPT to translate our blog post into a different language.")

    prompt = st.text_area("Enter your prompt here:", value="""Write me a comprehensive and professional medical profile in 3rd person that is factual and starts with the professionals name and title without headings:

    - The bio should be a minimum of 250 words.
    - Never say [name] is a [gender].
    - Use simple and to the point language.
    - Never say 'highly skilled' or 'highly experienced'.
    - Never say 'as an...'
    - The fields below have information you can use to create the content.
    - Where the field answer is empty, do not include and do not include missing fields.
    - Do not include information that is not completed.

    ---

    The writing style and tone should be as follows:

    The biography will informative and straightforward. It will presents factual information about a medical professional's background and areas of expertise. The language used will be clear and avoid complex medical jargon, ensuring that the information is easily accessible to a wide range of readers, including non-native English speakers and experts in the field.
    """)

    api_key = st.session_state.get('api_key', '')
    print(api_key)

    if not api_key:
        st.error("🔐  Please enter an OpenAI API key in the sidebar to proceed.")
        return

    if api_key:
      test_processor = st.button("Parallel process first 10 results (test)")

      if test_processor:
          generate_chat_completion_requests(csv_file_path, prompt)

          asyncio.run(
              process_api_requests_from_file(
                  requests_filepath="projects/_007_parallel_processor/requests.jsonl",
                  save_filepath="projects/_007_parallel_processor/requests_completed.jsonl",
                  request_url="https://api.openai.com/v1/chat/completions",
                  api_key=api_key,
                  max_requests_per_minute=float(4500),
                  max_tokens_per_minute=float(70000),
                  token_encoding_name="cl100k_base",
                  max_attempts=int(5),
                  logging_level=int(20),
              )
          )

          #st.write(display_jsonl_contents("projects/_007_parallel_processor/requests_completed.jsonl"))

          save_generated_data_to_csv("projects/_007_parallel_processor/requests_completed.jsonl")
          df = pd.read_csv("projects/_007_parallel_processor/output.csv")
          st.dataframe(df)

# Call the parallel_processor function to run the Streamlit app
if __name__ == "__main__":
    parallel_processor()
