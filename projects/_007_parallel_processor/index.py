import streamlit as st
import pandas as pd
from projects._007_parallel_processor.generate_request_file import generate_chat_completion_requests

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

    # Set the default CSV file path
    csv_file_path = "projects/_007_parallel_processor/input.csv"

    upload_csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if upload_csv_file:
        # Use the uploaded file if available
        df = pd.read_csv(upload_csv_file, header=None)
        csv_file_path = upload_csv_file.name  # Update the CSV file path
    else:
        df = pd.read_csv(csv_file_path, header=None)

    st.write(df.iloc[:, 0].rename("Your Data"))

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

    test_processor = st.button("Parallel process first 10 results (test)")

    if test_processor:
        generate_chat_completion_requests(csv_file_path, prompt)