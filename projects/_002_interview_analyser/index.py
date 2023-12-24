import streamlit as st
from streamlit import session_state
import time
from gpt_api_calls import pull_quotes_from_transcript
from projects._002_interview_analyser.interviews.tim_ferris_hugh_jackman import interview

def display_uploaded_transcripts():
    # Display transcripts if available
    if st.session_state.transcripts:
        with st.expander(f"👀 See uploaded transcripts (x {len(st.session_state.transcripts)})"):
            transcript_labels = [f"Transcript {i + 1}" for i in range(len(st.session_state.transcripts))]
            selected_transcript_index = st.selectbox("Select Transcript", transcript_labels)

            selected_index = transcript_labels.index(selected_transcript_index)
            st.markdown(f"#### Transcript {selected_index + 1}")
            st.markdown(
                f"""
                            <div style="overflow-y: scroll; height: 300px;">
                                {st.session_state.transcripts[selected_index]}
                            </div>
                            """,
                unsafe_allow_html=True
            )

def finish_uploading():
    st.session_state.render_transcript_form = False
    st.session_state.finished_uploading = True

def finish_adding_questions():
    st.session_state.render_questions_form = False
    st.session_state.finished_adding_questions = True


def analyse_transcripts(questions, transcripts):
    progress = st.empty()
    question_quotes_mapping = {}  # Dictionary to store quotes grouped by questions

    for index, transcript in enumerate(transcripts, start=1):
        transcript_name = f"Transcript {index}"
        progress.info(f"Analysing {index}/{len(transcripts)} transcripts")
        analysed_transcript = pull_quotes_from_transcript(questions, transcript)  # Assuming pull_quotes_from_transcript is defined

        for question, quotes in analysed_transcript['interview'].items():
            formatted_question = f"{question.replace('_', ' ').capitalize()}?"
            if formatted_question not in question_quotes_mapping:
                question_quotes_mapping[formatted_question] = []

            for quote in quotes:
                question_quotes_mapping[formatted_question].append((quote, transcript_name))

    display_uploaded_transcripts()
    # Display quotes grouped by questions
    for question, quotes_and_sources in question_quotes_mapping.items():
        st.subheader(f"{question}")
        for quote, source in quotes_and_sources:
            st.write(f"- \"{quote}\" *(source: {source})*")

    progress.success("Finished analysing transcripts")

    #with st.spinner("Loading..."):
        #time.sleep(5)  # Sleep for 5 seconds as an example
    #st.success("Transcript analysis complete!")

def add_question_form():
    if 'questions' not in st.session_state:
        st.session_state.questions = []

    with st.form("question_form"):
        st.markdown("#### Step 2/3: Ask questions")
        st.info("We will use your questions/topics to pull relevant quotes from the transcript/s you've uploaded. For example, you might want to get an overview of why many different world war 2 veterans joined the military, or what users liked or disliked about a product or service, etc.")
        question_text = st.text_input("Enter a question or topic:", value="What motivated you to join the military?")

        # Submit button for the form
        submit_button = st.form_submit_button("Add question")

        if submit_button and question_text:
            if question_text not in st.session_state.questions:
                # Add the new question/topic to the list
                st.session_state.questions.append(question_text)
            else:
                st.warning("You've already added this question")
            st.write("Added Questions/Topics:")
            for question in st.session_state.questions:
                st.markdown(f"- {question}")

    if st.session_state.questions and not st.session_state.finished_adding_questions:
        api_key = st.session_state.get('api_key', '')

        if not api_key:
            st.error("🔐  Please enter an OpenAI API key in the sidebar.")
            return
        else:
            st.button("Finished adding questions", on_click=finish_adding_questions)

def interview_analyser():
    st.title('🎙Transcript Analyser')
    st.markdown("Upload interview transcripts, and this GenAI program will pull out direct quotes from the transcripts related to your custom questions. Great for founders who want to learn from user interviews but don't have the time to comb through them to extract insights for specific questions/topics.")
    if not st.session_state.get('finished_uploading', False):
        with st.expander("✨️  See Project Details"):
            st.markdown("- ⏰ **Impact:** Saved a founder 30 hours analysing past user interview transcripts, so he was able to action insights same day.")
            st.markdown("- 🛠️ **Tools:** OpenAI - gpt-3.5-turbo [chat completion model](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) with function calling (see [code snippet](https://gist.github.com/tiny-rawr/e411d3ff31af0cf5a6a72b640502ea3f)).")
            st.markdown("- 💖 **Pain Point Addressed:** Instead of spending hours reading through user interview transcripts, pulling out quotes that are relevant to the questions/topics you care about, you can instead invest your energy in actioning the insights gained.")
            st.markdown("- ⚠️ **Limitations:** You need to do a separate API call per question to get a more comprehensive list of quotes. You can ask multiple questions in a single call, but the more you ask the less quotes you get per question because of the limited context window (amount of text that can be retrieved per single call).")
            st.markdown("- 💌 Read the full [deep dive build process here](https://fairylightsai.substack.com/p/4-ask-questions-about-interview-transcripts).")

        if 'render_transcript_form' not in st.session_state:
            st.session_state.render_transcript_form = True
        if 'finished_uploading' not in st.session_state:
            st.session_state.finished_uploading = False
        if 'finished_adding_questions' not in st.session_state:
            st.session_state.finished_adding_questions = False

    if 'transcripts' not in st.session_state:
        st.session_state.transcripts = []

    if st.session_state.render_transcript_form:
        with st.form("transcript_form"):
            st.markdown("#### Step 1/3: Upload your transcript/s")
            st.info("You could upload interviews with world war 2 veterans (like this demo example), user interviews for an app or product, YouTube transcripts, Podcast transcripts, Research papers and more.")
            transcript_text = st.text_area("Paste Transcript Text (5000 characters max):",
                                       height=200, value=interview)

            # Submit button for the form
            submit_button = st.form_submit_button("Add transcript")

            if submit_button:
                if transcript_text:
                    if len(transcript_text) < 500:
                        st.error("Transcript must be at least 500 characters long.")
                    elif transcript_text in st.session_state.transcripts:
                        st.warning("This transcript has already been added.")
                    else:
                        st.session_state.transcripts.append(transcript_text)
                else:
                    st.error("Please enter a transcript before submitting.")

    if st.session_state.transcripts and not st.session_state.finished_uploading:
        display_uploaded_transcripts()
        st.button("Finished adding transcripts", on_click=finish_uploading)

    # Step 2: Add Questions Form
    if st.session_state.finished_uploading and not st.session_state.finished_adding_questions:
        display_uploaded_transcripts()
        add_question_form()

    # Step 3: Analyse Transcripts
    if st.session_state.finished_adding_questions:
        questions = st.session_state.questions
        transcripts = st.session_state.transcripts

        analyse_transcripts(questions, transcripts)
