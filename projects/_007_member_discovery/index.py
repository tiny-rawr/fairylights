import streamlit as st
import webbrowser

def member_discovery():
    st.title('👷‍♀️ Member Discovery')
    st.markdown("A RAG-based (retrieval-only) application for a Build Club Build Bounty Competition.")

    with st.expander("✨ See project details", expanded=True):
        st.subheader("Why I built this")
        st.markdown("This was a competition for Build Club, where we were given an AirTable containing Build Club member data from the onboarding process (e.g. what are you currently building and what have you worked on), and the build updates (live build in public updates for specific projects).")
        st.subheader("My solution")
        st.write("I started out by building a non-ai solution. So you can see all members, their projects and build updates. I also got carried away with the cute areas of expertise chips (emojis are 🥰), and added build club branding and CTAs to make it easier for us to add projects and build updates.")
        st.write("Then I learned how to implement a RAG-based system for the first time (Retrieval Augmented Generation). Or at least, the retrieval step because I decided not to generate content based on the retrieved results this time because it wasn't needed. The future projects this has unlocked is crazy awesome!")
        st.write("The coolest thing about this (to me), is that when you search 'who is working in law', it retrieves projects and build updates related to the legal space. So the more projects you ship in public, the more discoverable you are as an expert in the search results.")
        st.subheader("Demo Video")
        st.video("projects/_007_member_discovery/build_bounty_member_chatbot.mp4")

    if st.button('Try live version of Member Discovery'):
        webbrowser.open('https://build-club-member-discovery.streamlit.app/')
