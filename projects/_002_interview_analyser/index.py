import streamlit as st
from streamlit import session_state

def interview_analyser():
    st.title('🪖 Interview Analyser')
    st.markdown("Upload interview transcripts, and this program will pull out direct quotes from the transcripts related to any question you want. Great for founders who want to learn from user interviews but don't have the time to comb through them to extract quotes on specific topics.")
    with st.expander("✨️  See Project Details"):
        st.markdown("- ⏰ **Impact:** Saved a founder 30 hours analysing past user interview transcripts, so he was able to action insights same day.")
        st.markdown("- 🛠️ **Tools:** OpenAI - gpt-3.5-turbo [chat completion model](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) with function calling (see [code snippet](https://gist.github.com/tiny-rawr/e411d3ff31af0cf5a6a72b640502ea3f)).")
        st.markdown("- 💖 **Pain Point Addressed:** Instead of spending hours reading through user interview transcripts, pulling out quotes that are relevant to the questions/topics you care about, you can instead invest your energy in actioning the insights gained.")
        st.markdown("- ⚠️ **Limitations:** You need to do a separate API call per question to get a more comprehensive list of quotes. You can ask multiple questions in a single call, but the more you ask the less quotes you get per question because of the limited context window (amount of text that can be retrieved per single call).")
        st.markdown("- 💌 Read the full [deep dive build process here](https://fairylightsai.substack.com/p/4-ask-questions-about-interview-transcripts).")

    info_placeholder = st.empty()

    transcript_text = st.text_area("Paste Transcript Text (5000 characters max):", height=200, max_chars=5000)

    if 'transcripts' not in st.session_state:
        st.session_state.transcripts = []

    if st.button("Submit"):
        if transcript_text:
            st.session_state.transcripts.append(transcript_text)
            st.success("Transcript Added!")

    if st.session_state.transcripts:
        transcript_labels = [f"Transcript {i + 1}" for i in range(len(st.session_state.transcripts))]
        selected_transcript_index = st.selectbox("Select Transcript", transcript_labels)

        if st.button("Clear All"):
            st.session_state.transcripts.clear()
            st.success("All Transcripts Cleared!")
        else:
            selected_index = transcript_labels.index(selected_transcript_index)
            st.subheader("Selected Transcript")
            st.write(st.session_state.transcripts[selected_index])

    api_key = st.session_state.get('api_key', '')

    if not api_key:
        info_placeholder.error("🔐  Please enter an OpenAI API key in the sidebar.")
        return