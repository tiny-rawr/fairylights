import streamlit as st

def home():
    st.title('✨ Fairylights | 100 GenAI projects')
    st.write("This is page one.")

def page_two():
    st.title('🧠 Thought Checker')
    st.write("Enter a journal entry, and this program will auto-detect unhelpful thinking patterns (cognitive distortions) in your thinking patterns.")

def page_three():
    st.title('🪖 Interview Analyser')
    st.write("Upload interview transcripts, and this program will pull out direct quotes from the transcripts related to any question you want.")

# Categories sidebar
with st.sidebar:
    # Use columns to center the image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image('images/profile-avatar.png')

    st.markdown("<div style='text-align: center;'>"
                "<h2>🧪🤖 100 GenAI Projects</h2>"
                "<p>Sign up to <a href='https://fairylightsai.substack.com/' target='_blank'>newsletter</a> for deep dives"
                "</div>", unsafe_allow_html=True)

    openai_api_key = st.text_input(" ", type="password", placeholder="Enter your OpenAI API key")

    page = st.radio("Choose a project", ["Home", "#1. Thought Checker", "#2. Interview Analyser"])

if page == "Home":
  home()
elif page == "#1. Thought Checker":
  page_two()
elif page == "#2. Interview Analyser":
  page_three()
