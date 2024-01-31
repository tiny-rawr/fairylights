import streamlit as st
import pandas as pd


def parallel_processor():
    st.title("Parallel Processor")
    st.markdown("Bulk process 1000s of GPT-3.5-Turbo requests in a couple of minutes (depending on your OpenAI Tier).")

    with st.expander("✨ See project details (and demo video)"):
        st.subheader("Why I built this")
        st.write("Do x")
        st.subheader("Demo video")
        #st.video("demo_videos/chatty_avatar_demo.mp4")
        st.subheader("Ways to use this")
        st.markdown("- 🎙️ **Cat**: Text")
        st.subheader("Limitations")
        st.error("⚠️ **Cat**: Text.")
        st.write("")

    csv_file = st.file_uploader("Upload a CSV file", type=["csv"])


    if csv_file:
        df = pd.read_csv(csv_file, header=None)
        st.write(df.iloc[:, 0].rename("Your Data"))
