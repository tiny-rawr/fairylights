import streamlit as st
import webbrowser

def home():
    st.title("🚀 100 GenAI projects 🤖")
    st.write("I'm on a mission to ship 100 happy and helpful GenAI projects. Every project shipped here has solved a problem for at least one real person.")

    with st.expander("✨ Subscribe for deep dives about each project"):
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <iframe src="https://fairylightsai.substack.com/embed" width="480" height="320" style="border:1px solid #EEE; background:white; display: flex; justify-content: center;" frameborder="0" scrolling="no"></iframe>
            </div>
            """,
            unsafe_allow_html=True
        )

    projects = [
        {
            "title": "#9. Parallel Processor",
            "description": "Run 1000s of GPT tasks in under 2m. Same prompt, different data. E.g. Write 1000s of real-estate bios using scraped data in a spreadsheet.",
            "url": "https://100-genai-projects.streamlit.app/?project=parallel-processor",
            "image": "images/featured/parallel_processor.png",
        },
        {
            "title": "#8. YouTube Summariser",
            "description": "Learn how to use GenAI to summarise YouTube videos released by your favourite channels over the last week, month or quarter! Send them as a recurring email too!",
            "url": "https://100-genai-projects.streamlit.app/?project=youtube-summariser",
            "image": "images/featured/youtube_summariser.png",
        },
        {
            "title": "#7. Member Discovery",
            "description": "Search for Build Club members who are working in Law, or who can help you build Retrieval Augmented Generation projects, etc (RAG-app built on top of AirTable for a competition).",
            "url": "https://100-genai-projects.streamlit.app/?project=member-discovery",
            "image": "images/featured/member_discovery.png",
        },
        {
            "title": "#6. Pitch Panda",
            "description": "A robotic plush panda you can have a two-way convo with! Winner of the People's Choice Award at a Young Entrepreneur Pitch night. Collab project!",
            "url": "https://100-genai-projects.streamlit.app/?project=pitch-panda",
            "image": "images/featured/pitch_panda.png",
        },
        {
            "title": "#5. Chatty Characters",
            "description": "Generate a 3D avatar character and then chat to them via text, they will respond back to you by talking! The voice matches character gender too (male, female, other).",
            "url": "https://100-genai-projects.streamlit.app/?project=chatty-character",
            "image": "images/featured/chatty_characters.png",
        },
        {
            "title": "#4. Lip Syncing Avatar",
            "description": "Turn any character image into a lip-syncing avatar that you can use in product demos, to bring your children's stories to life or create virtual gift cards!",
            "url": "https://100-genai-projects.streamlit.app/?project=lip-syncing-avatar",
            "image": "images/featured/lip_syncing_avatar.png",
        },
        {
            "title": "#3. Ask Your Database",
            "description": "Upload CSV files, ask questions about your data in plain English and this GenAI program will auto-generate and execute a SQL statement to retrieve the data you need to answer the question.",
            "url": "https://100-genai-projects.streamlit.app/?project=ask-your-database",
            "image": "images/featured/ask_your_database.png",
        },
        {
            "title": "#2. Transcript Analyser",
            "description": "Upload transcripts of user interviews, YouTube videos, podcasts etc and get back direct quotes that are related to specific questions or topics.",
            "url": "https://100-genai-projects.streamlit.app/?project=transcript-analyser",
            "image": "images/featured/transcript_analyser.png",
        },
        {
            "title": "#1. Thought Checker",
            "description": "Enter a journal entry and this GenAI program will auto-detect unhelpful thinking patterns (cognitive distortions) that are present in your entry, so you can focus on reframing them.",
            "url": "https://100-genai-projects.streamlit.app/?project=thought-checker",
            "image": "images/featured/thought_checker.png",
        },
    ]

    for i in range(0, len(projects), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(projects):
                with cols[j]:
                    project = projects[i + j]
                    st.image(project["image"], use_column_width=True)
                    st.subheader(project["title"])
                    st.write(project["description"])
                    st.markdown(f"👉 [Try it out!]({project['url']})")