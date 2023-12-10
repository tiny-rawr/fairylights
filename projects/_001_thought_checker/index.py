import streamlit as st
def thought_checker():
  st.title('🧠 Thought Checker')
  st.write("Enter a journal entry, and this program will auto-detect unhelpful thinking patterns (cognitive distortions) in your thinking patterns, so you can focus on the more helpful reframing part.")
  st.write("🛠️ OpenAI (GPT-3.5-turbo, function calling), Streamlit")