import streamlit as st

def testimonial(name, quote, profile_image='images/profile-avatar.png'):
    st.markdown("---")

    col1, col2 = st.columns([1, 9])

    with col1:
        st.image(profile_image, width=50, use_column_width=False)

    with col2:
        st.markdown(f"**{name}**")
        st.write(quote)

    st.markdown("---")

def home():
    st.title("✨ Fairylights | 100 GenAI projects 🤖")
    st.write("I'm on a mission to explore what's possible with generative AI, by shipping 100 useful projects. Each project is accompanied with a [behind the scenes deep dive](https://fairylightsai.substack.com/) 🤿")

def page_one():
    st.title('🧠 Thought Checker')
    st.write("Enter a journal entry, and this program will auto-detect unhelpful thinking patterns (cognitive distortions) in your thinking patterns, so you can focus on the more helpful reframing part.")

def page_two():
    st.title('🪖 Interview Analyser')
    st.write("Upload interview transcripts, and this program will pull out direct quotes from the transcripts related to any question you want.")
    st.success("⏰ Saved 30 hours of sentiment analysis, so insights could be actioned faster")
    testimonial('Tam Asaad - CEO of Foura', "Quote")

def page_three():
    st.title('🐼 Pitch Panda')
    st.write("A collaborative project with [Stan](https://www.linkedin.com/in/stanleaf?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADRVb2QB43kcXPLI2AI7fGY09X8uBpCfO8k&lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_all%3Bx%2FVwbXzhRCOLCLq6CnlpFw%3D%3D), combining his IOT superpowers with my GenAI skills. We developed this robotic plush panda you can have a two-way conversation with.")
    st.success("🏆 Winner of the [People's Choice Award at Fishburners young entrepreneur pitch night 2023](https://www.linkedin.com/posts/fishburners_entrepreneurs-genz-ai-activity-7120150734930673664-v_Wq)")
    testimonial('Martin Karafilis - CEO of Fishburners', "👏🏼 People's Choice: 🦕 Becca Williams, Founder of fairylights.ai, in a landslide victory after the most captivating display of generative-AI + tech in action we've ever seen!", 'images/testimonials/martin-karafilis.jpeg')

def page_four():
    st.title('📈 Ask Your Spreadsheets')
    st.write("Upload your spreadsheets and ask questions in plain english. This program will auto-generate and execute SQL queries to retrieve the data needed to answer your question.")

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

    page = st.radio("Choose a project", ["Home", "#1. Thought Checker", "#2. Interview Analyser", "#3. Pitch Panda 🏆", "#4. Ask Your Spreadsheets"])

if page == "Home":
  home()
elif page == "#1. Thought Checker":
  page_one()
elif page == "#2. Interview Analyser":
  page_two()
elif page == "#3. Pitch Panda 🏆":
  page_three()
elif page == "#4. Ask Your Spreadsheets":
  page_four()
