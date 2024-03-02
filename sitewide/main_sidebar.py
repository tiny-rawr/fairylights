import streamlit as st
from pages.home.index import home
from projects._000_wizard_steps.index import wizard_steps
from projects._001_thought_checker.index import thought_checker
from projects._002_interview_analyser.index import interview_analyser
from projects._003_ask_your_spreadsheets.index import ask_your_spreadsheets
from projects._004_lip_syncing_avatar.index import lip_syncing_avatar
from projects._005_avatar_debate.index import avatar_debate
from projects._006_pitch_panda.index import pitch_panda
from projects._007_member_discovery.index import member_discovery
import re

def is_valid_api_key(api_key):
    if api_key.startswith("sk-") and len(api_key) == 51:
        return True
    else:
        return False

def create_slug(name):
    slug = name.lower()
    # Remove patterns like "#1. "
    slug = re.sub(r'#[0-9]+\.\s+', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    # Remove special characters
    slug = re.sub(r'[^a-zA-Z0-9-]', '', slug)

    return slug

# Define the projects dictionary with dynamically generated slugs
projects = {
    "Home": {"function": home, "tags": [], "published": True},
    #"Wizard Steps": {"function": wizard_steps, "tags": [], "skills": [], "published": True},
    "#1. Thought Checker": {"function": thought_checker, "tags": ["Text generation", "Text extraction"], "skills": ["Text generation", "Text extraction"], "published": True},
    "#2. Transcript Analyser": {"function": interview_analyser, "tags": ["Text extraction"], "skills": ["Text extraction"], "published": True},
    "#3. Ask Your Database": {"function": ask_your_spreadsheets, "tags": ["Code generation"], "published": True},
    "#4. Lip Syncing Avatar": {"function": lip_syncing_avatar, "tags": ["Image generation", "Lip syncing", "Voice cloning", "Video generation"], "published": True},
    "#5. Chatty Character": {"function": avatar_debate, "tags": ["Text generation","Image generation", "Text-to-speech", "Lip syncing"], "published": True},
    "#6. Pitch Panda": {"function": pitch_panda, "tags": ["IOT", "Text generation", "Text-to-speech"], "published": True},
    "#7. Member Discovery": {"function": member_discovery, "tags": ["RAG", "Text generation"], "published": True},
}

# Add slugs dynamically
for project_name, project_data in projects.items():
    project_data["slug"] = create_slug(project_name)

def get_unique_tags():
    unique_tags = set()
    for project in projects.values():
        for tag in project["tags"]:
            unique_tags.add(tag)
    return list(unique_tags)

def get_unique_skills():
    unique_skills = set()
    for project in projects.values():
        for skill in project["skills"]:
            unique_skills.add(skill)
    return list(unique_skills)

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

        openai_api_key = st.text_input("Your OpenAI API Key:", type="password", placeholder="Enter your OpenAI API key")
        st.info("🔐 We don't save your API keys or any data you enter (it's lost on refresh)")

        if 'api_key_input_attempted' not in st.session_state:
            st.session_state.api_key_input_attempted = False

        if openai_api_key:
            st.session_state.api_key_input_attempted = True

        if st.session_state.api_key_input_attempted:
            if is_valid_api_key(openai_api_key):
                st.session_state.api_key = openai_api_key
            else:
                st.error("Please enter a valid OpenAI API key.")

        with st.expander("Filter projects by skills used"):
            selected_tags = []
            all_tags = get_unique_tags()

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

    url_param = st.experimental_get_query_params().get("project")

    # Get the default project slug from the URL, fallback to 'home' if not found
    default_project_slug = url_param[0] if url_param and url_param[0] in [proj["slug"] for proj in
                                                                          projects.values()] else "home"
    default_project = next((name for name, proj in projects.items() if proj["slug"] == default_project_slug), None)

    project_names = list(filtered_projects.keys())
    default_index = project_names.index(default_project) if default_project in project_names else 0

    # Radio button for selecting a project
    selected_project = st.sidebar.radio("Try a project", project_names, index=default_index)

    # Set the project query parameter in the URL when a project is selected
    st.experimental_set_query_params(project=filtered_projects[selected_project]["slug"])

    # Show the content associated with the selected project
    filtered_projects[selected_project]["function"]()