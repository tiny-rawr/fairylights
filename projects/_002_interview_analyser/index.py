import streamlit as st
from projects._002_interview_analyser.gpt_api_calls import extract_quotes
from projects.shared.genai_utils import chunk_text
import json

def initialize_session_state():
    if 'render_transcript_form' not in st.session_state:
        st.session_state.render_transcript_form = True
    if 'finished_uploading' not in st.session_state:
        st.session_state.finished_uploading_transcripts = False
    if 'finished_adding_questions' not in st.session_state:
        st.session_state.finished_adding_questions = False
    if 'transcripts' not in st.session_state:
        st.session_state.transcripts = []

def add_transcript_to_session(transcript_name, transcript_source, transcript_text):
    if any(transcript['name'] == transcript_name for transcript in st.session_state.transcripts):
        st.error("A transcript with this name already exists.")
    else:
        transcript = {
            'name': transcript_name,
            'source': transcript_source,
            'transcript': transcript_text
        }
        st.session_state.transcripts.append(transcript)

def add_question_to_session(question_text):
    if question_text not in st.session_state.questions:
        st.session_state.questions.append(question_text)
    else:
        st.warning("You've already added this question")

def display_uploaded_transcripts():
    if st.session_state.get('transcripts'):
        with st.expander(f"👀 See uploaded transcripts (x {len(st.session_state.transcripts)})"):
            transcript_names = [transcript['name'] for transcript in st.session_state.transcripts]
            selected_transcript_index = st.selectbox("Select Transcript", transcript_names)
            selected_transcript = next(
                (t for t in st.session_state.transcripts if t['name'] == selected_transcript_index), None)
            if selected_transcript:
                st.markdown(f"#### Transcript: {selected_transcript['name']}")
                st.markdown(f"**Source:** {selected_transcript['source']}")
                st.markdown(f"<div style='overflow-y: scroll; height: 300px;'>{selected_transcript['transcript']}</div>",
                            unsafe_allow_html=True)

def display_questions():
    st.write("Added Questions/Topics:")
    for question in st.session_state.questions:
        st.markdown(f"- {question}")

def add_transcript_form():
    from projects._002_interview_analyser.demo_data.veteran_interview_donald_dugan import transcript

    with st.form("transcript_form"):
        st.markdown("#### Step 1/3: Upload your transcript/s")
        transcript_name = st.text_input("Transcript Name:", value=transcript['name'])
        transcript_source = st.text_input("Transcript Source:", value=transcript['source'])
        transcript_text = st.text_area("Paste Transcript Text (5000 characters max):", height=200, value=transcript['transcript'])

        submit_button = st.form_submit_button("Add transcript")

        if submit_button:
            add_transcript_to_session(transcript_name, transcript_source, transcript_text)

def add_question_form():
    if 'questions' not in st.session_state:
        st.session_state.questions = []

    with st.form("question_form"):
        st.markdown("#### Step 2/3: Ask questions")
        question_text = st.text_input("Enter a question or topic:", value="What motivated you to join the military?")
        submit_button = st.form_submit_button("Add question")

        if submit_button and question_text:
            add_question_to_session(question_text)
            display_questions()

    if st.session_state.questions and not st.session_state.finished_adding_questions:
        api_key = st.session_state.get('api_key', '')

        if not api_key:
            st.error("🔐  Please enter an OpenAI API key in the sidebar to proceed.")
            return

        else:
            st.button("Finished adding questions", on_click=finish_adding_questions)

def finish_uploading_transcripts():
    st.session_state.render_transcript_form = False
    st.session_state.finished_uploading_transcripts = True

def finish_adding_questions():
    st.session_state.render_questions_form = False
    st.session_state.finished_adding_questions = True

def display_extracted_quotes(quote_obj):
    for question, quotes in quote_obj.items():
        print(f"### {question}")
        for quote in quotes:
            print(f"- {quote}")

def analyse_transcripts(questions, transcripts):
    progress = st.empty()
    question_quotes_mapping = {}

    for index, transcript in enumerate(transcripts, start=1):
        transcript_name = transcript['name']
        progress.info(f"Analyzing transcript {index}/{len(transcripts)}: {transcript_name}")

        for current_question in questions:
            quotes_json_str = extract_quotes(transcript['transcript'], current_question)
            quotes_dict = json.loads(quotes_json_str)
            for question, quotes in quotes_dict.items():
                if question not in question_quotes_mapping:
                    question_quotes_mapping[question] = set()
                question_quotes_mapping[question].update(quotes)

    display_uploaded_transcripts()

    for question, quotes in question_quotes_mapping.items():
        st.subheader(question.strip())
        for quote in quotes:
            st.markdown(f"- {quote}")

    progress.success("Finished analysing transcripts")



def analyse_transcript(questions, transcript):
    transcript_name = transcript['name']
    transcript_source = transcript['source']
    transcript_text = transcript['transcript']

    transcript_chunks = chunk_text(transcript_text)
    question_quotes = {}

    for chunk_index, chunk in enumerate(transcript_chunks, start=1):
        analysed_transcript = pull_quotes_from_transcript(chunk, questions)

        for question in questions:
            quotes = analysed_transcript['interview'].get(question, [])
            if quotes:
                if question not in question_quotes:
                    question_quotes[question] = []
                formatted_quotes = [f"{quote} ([source: {transcript_name}]({transcript_source}))" for quote in quotes]
                question_quotes[question].extend(formatted_quotes)

    return question_quotes


def display_project_details():
    with st.expander("✨ See project details"):
        st.subheader("Why I built this")
        st.write("A founder friend mentioned they had done around 20 user interviews a while back, but didn't have the time to go through and extract insights related to their questions. They had tried existing tools which were great at sentiment analysis but struggled to extract quotes related to more nuanced domain-specific questions like 'How did members make friends using our service' for example. This solution solved that problem for them and they were able to start actioning insights immediately.")
        st.subheader("Real-life Impact")
        st.warning("⏰ **Saved time:** Saved founder 30 hours of user interview analysis so they were able to act on insights the same day.")
        st.subheader("Ways to use this")
        st.markdown("- **✅ Actionable User interview insights**: Upload transcripts of user interviews, and pull out quotes to help you decide what to change/improve on. E.g. What did they like? Dislike? Common improvement suggestions. I built this little solution for this use-case and saved a founder 30+ hours of analysing their interviews when they already had a ton of fires to put out and just wanted to get started on making changes.")
        st.markdown("- **🪖 World-building**: Let's say you want to build a world for a novel you're writing. You can upload transcripts with that group (e.g. war veterans), and pull out quotes to help you flesh out that world, e.g. Slang, weather patterns, routines, clothing, technology, vehicles, weaponry, meals etc.")
        st.markdown("- **🎙️ Pitch video tips:** I uploaded transcripts from many pitch nights where founders pitched their startup ideas to a panel of investors at Fishburners, then extracted all the questions that founders were asked by the panel of investors, and also go to market strategies etc.")
        st.subheader("Limitations")
        st.error("⚠️ **Non-exhaustive quotes**: The more you ask the less quotes you get per question because of the limited context window (amount of text that can be processed per single call).")
        st.subheader("Extra")
        st.markdown("- 💌 Read the [newsletter about this](https://fairylightsai.substack.com/p/4-ask-questions-about-interview-transcripts).")

def interview_analyser():
    st.title('🎙Transcript Analyser')
    st.markdown("Upload interview transcripts, and this GenAI program will pull out direct quotes from the transcripts related to your custom questions. See project details for cool ways of using this.")

    if not st.session_state.get('finished_uploading_transcripts', False):
        st.warning("👷‍Use-case in progress!")
        display_project_details()
        initialize_session_state()

    if st.session_state.render_transcript_form:
        add_transcript_form()

    if st.session_state.transcripts and not st.session_state.finished_uploading_transcripts:
        display_uploaded_transcripts()
        st.button("Finished adding transcripts", on_click=finish_uploading_transcripts)

    if st.session_state.finished_uploading_transcripts and not st.session_state.finished_adding_questions:
        display_uploaded_transcripts()
        add_question_form()

    if st.session_state.finished_adding_questions:
        questions = st.session_state.questions
        transcripts = st.session_state.transcripts
        analyse_transcripts(questions, transcripts)