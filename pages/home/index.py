import streamlit as st
def home():
    st.title("🚀 100 GenAI projects 🤖")
    st.write(
        "I can't wait to explore what's possible with generative AI with you by shipping 100 happy and helpful use-cases. Try them out for yourself, and [subscribe for the newest possibilities](https://fairylightsai.substack.com/) 💌🥰")

    st.subheader("Thought Checker")
    st.write("Enter a journal entry and this GenAI program will auto-detect unhelpful thinking patterns (cognitive distortions) that are present in your entry, so you can focus on reframing them.")
    st.markdown("[Try it out!](https://100-genai-projects.streamlit.app/?project=thought-checker)")
    st.image("images/featured/thought_checker.png", use_column_width=True)