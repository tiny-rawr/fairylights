import streamlit as st
from pages.home.index import home
from projects._001_thought_checker.index import thought_checker
from projects._002_interview_analyser.index import interview_analyser
from projects._003_pitch_panda.index import pitch_panda
from projects._004_ask_your_spreadsheets.index import ask_your_spreadsheets
from projects._005_character_profiles.index import character_profiles

projects = {
    "Home": {"function": home, "tags": [], "published": True},
    "Thought Checker": {"function": thought_checker, "tags": ["OpenAI", "Streamlit"], "published": True},
    "Interview Analyser": {"function": interview_analyser, "tags": ["OpenAI", "Streamlit"], "published": False},
    "🏆 Pitch Panda": {"function": pitch_panda, "tags": ["OpenAI", "Eleven Labs", "Raspberry Pi"], "published": False},
    "Ask Your Spreadsheets": {"function": ask_your_spreadsheets, "tags": ["OpenAI", "Pandas", "Streamlit"], "published": False},
    "Generate character profiles": {"function": character_profiles, "tags": ["OpenAI", "Web Scraping", "Streamlit"], "published": False}
}


def get_unique_tags():
    unique_tags = set()
    for project in projects.values():
        for tag in project["tags"]:
            unique_tags.add(tag)
    return list(unique_tags)


def sidebar():
    with st.sidebar:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image('images/profile-avatar.png')

        st.markdown("<div style='text-align: center;'>"
                    "<h2>🧪🤖 100 GenAI Projects</h2>"
                    "<p>A truly magical time to be alive! 🤯</p>"
                    "</div>", unsafe_allow_html=True)

        with st.expander("✨ Fairylights Newsletter"):
            st.markdown(
                """
                <div style="display: flex; justify-content: center;">
                    <iframe src="https://fairylightsai.substack.com/embed" width="480" height="320" style="border:1px solid #EEE; background:white; display: flex; justify-content: center;" frameborder="0" scrolling="no"></iframe>
                </div>
                """,
                unsafe_allow_html=True
            )

        openai_api_key = st.text_input(" ", type="password", placeholder="Enter your OpenAI API key")

        with st.expander("Filter projects by tools used"):
            selected_tags = []
            all_tags = get_unique_tags()

            # Count the number of projects per tag for published projects
            tag_counts = {tag: sum(tag in project["tags"] for project in projects.values() if project.get("published", False)) for tag in all_tags}

            for tag in all_tags:
                if tag_counts[tag] > 0:
                    tag_label = f"{tag} ({tag_counts[tag]})"
                    if st.checkbox(tag_label, key=tag):
                        selected_tags.append(tag)

            if selected_tags:
                filtered_projects = {name: proj for name, proj in projects.items() if
                                     proj.get("published", False) and any(tag in proj["tags"] for tag in selected_tags)}
            else:
                filtered_projects = {name: proj for name, proj in projects.items() if proj.get("published", False)}

    page = st.sidebar.radio("Try a project", list(filtered_projects.keys()))

    filtered_projects[page]["function"]()