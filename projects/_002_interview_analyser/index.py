import streamlit as st
from components.testimonials import testimonial

def interview_analyser():
    st.title('🪖 Interview Analyser')
    st.write("Upload interview transcripts, and this program will pull out direct quotes from the transcripts related to any question you want.")
    st.write("🛠️ OpenAI (GPT-3.5-turbo, function calling), Streamlit")
    st.success("⏰ Saved 30 hours of sentiment analysis, so insights could be actioned faster")
    testimonial('Tam Asaad - CEO of Foura', "Quote")