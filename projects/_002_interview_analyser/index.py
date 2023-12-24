import streamlit as st
from gpt_api_calls import pull_quotes_from_transcript
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

def count_tokens(text):
  tokenizer = tiktoken.get_encoding('cl100k_base')
  tokens = tokenizer.encode(
    text,
    disallowed_special=()
  )
  return len(tokens)

def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=100,
        length_function=count_tokens,
        separators=['\n\n', '\n', ' ', '']
    )

    return text_splitter.split_text(text)

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
                st.markdown(f"<div style='overflow-y: scroll; height: 300px;'>{selected_transcript['transcript']}</div>", unsafe_allow_html=True)

def add_transcript_form():
    from projects._002_interview_analyser.veteran_interview_donald_dugan import transcript

    with st.form("transcript_form"):
        st.markdown("#### Step 1/3: Upload your transcript/s")
        transcript_name = st.text_input("Transcript Name:", value=transcript['name'])
        transcript_source = st.text_input("Transcript Source:", value=transcript['source'])
        transcript_text = st.text_area("Paste Transcript Text (5000 characters max):", height=200, value=transcript['transcript'])

        submit_button = st.form_submit_button("Add transcript")

        if submit_button:
            if any(t['name'] == transcript_name for t in st.session_state.transcripts):
                st.error("A transcript with this name already exists.")
            else:
                transcript = {
                    'name': transcript_name,
                    'source': transcript_source,
                    'transcript': transcript_text
                }
                st.session_state.transcripts.append(transcript)

def finish_uploading():
    st.session_state.render_transcript_form = False
    st.session_state.finished_uploading = True

def finish_adding_questions():
    st.session_state.render_questions_form = False
    st.session_state.finished_adding_questions = True

def analyse_transcripts(questions, transcripts):
    progress = st.empty()
    question_quotes_mapping = {}

    for index, transcript in enumerate(transcripts, start=1):
        transcript_name = transcript['name']
        transcript_source = transcript['source']
        transcript_text = transcript['transcript']

        progress.info(f"Analyzing transcript {index}/{len(transcripts)}: {transcript_name}")

        transcript_chunks = chunk_text(transcript_text)  # Split the transcript into smaller chunks
        total_chunks = len(transcript_chunks)

        for chunk_index, chunk in enumerate(transcript_chunks, start=1):
            analysed_transcript = pull_quotes_from_transcript(questions, chunk)

            for question, quotes in analysed_transcript['interview'].items():
                formatted_question = f"{question.replace('_', ' ').capitalize()}?"
                if formatted_question not in question_quotes_mapping:
                    question_quotes_mapping[formatted_question] = []

                for quote in quotes:
                    # Format the source as a hyperlink
                    formatted_source = f"[{transcript_name}]({transcript_source})"
                    question_quotes_mapping[formatted_question].append((quote, formatted_source))

            # Display the progress
            progress.info(f"Analyzing chunk {chunk_index}/{total_chunks} from transcript {index}/{len(transcripts)}: {transcript_name}")

    display_uploaded_transcripts()

    for question, quotes_and_sources in question_quotes_mapping.items():
        st.subheader(f"{question}")
        for quote, source in quotes_and_sources:
            st.markdown(f"- \"{quote}\" *(source: {source})*")

    progress.success("Finished analysing transcripts")

def display_questions():
    st.write("Added Questions/Topics:")
    for question in st.session_state.questions:
        st.markdown(f"- {question}")

def add_question_form():
    if 'questions' not in st.session_state:
        st.session_state.questions = []

    with st.form("question_form"):
        st.markdown("#### Step 2/3: Ask questions")
        question_text = st.text_input("Enter a question or topic:", value="What motivated you to join the military?")
        submit_button = st.form_submit_button("Add question")

        if submit_button and question_text:
            if question_text not in st.session_state.questions:
                st.session_state.questions.append(question_text)
            else:
                st.warning("You've already added this question")
            display_questions()

    if st.session_state.questions and not st.session_state.finished_adding_questions:
        api_key = st.session_state.get('api_key', '')

        if not api_key:
            st.error("🔐  Please enter an OpenAI API key in the sidebar to proceed.")
            return

        else:
            st.button("Finished adding questions", on_click=finish_adding_questions)



def interview_analyser():
    st.title('🎙Transcript Analyser')
    st.markdown(
        "Upload interview transcripts, and this GenAI program will pull out direct quotes from the transcripts related to your custom questions. Great for founders who want to learn from user interviews but don't have the time to comb through them to extract insights for specific questions/topics.")

    if not st.session_state.get('finished_uploading', False):
        st.warning("👷‍Use-case in progress!")
        with st.expander("✨️  See Project Details"):
            st.markdown(
                "- ⏰ **Impact:** Saved a founder 30 hours analysing past user interview transcripts, so he was able to action insights same day.")
            st.markdown(
                "- 🛠️ **Tools:** OpenAI - gpt-3.5-turbo [chat completion model](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) with function calling (see [code snippet](https://gist.github.com/tiny-rawr/e411d3ff31af0cf5a6a72b640502ea3f)).")
            st.markdown(
                "- 💖 **Pain Point Addressed:** Instead of spending hours reading through user interview transcripts, pulling out quotes that are relevant to the questions/topics you care about, you can instead invest your energy in actioning the insights gained.")
            st.markdown(
                "- ⚠️ **Limitations:** You need to do a separate API call per question to get a more comprehensive list of quotes. You can ask multiple questions in a single call, but the more you ask the less quotes you get per question because of the limited context window (amount of text that can be retrieved per single call).")
            st.markdown(
                "- 💌 Read the full [deep dive build process here](https://fairylightsai.substack.com/p/4-ask-questions-about-interview-transcripts).")

        if 'render_transcript_form' not in st.session_state:
            st.session_state.render_transcript_form = True
        if 'finished_uploading' not in st.session_state:
            st.session_state.finished_uploading = False
        if 'finished_adding_questions' not in st.session_state:
            st.session_state.finished_adding_questions = False

    if 'transcripts' not in st.session_state:
        st.session_state.transcripts = []

    if st.session_state.render_transcript_form:
        add_transcript_form()

    if st.session_state.transcripts and not st.session_state.finished_uploading:
        display_uploaded_transcripts()
        st.button("Finished adding transcripts", on_click=finish_uploading)

    if st.session_state.finished_uploading and not st.session_state.finished_adding_questions:
        display_uploaded_transcripts()
        add_question_form()

    if st.session_state.finished_adding_questions:
        questions = st.session_state.questions
        transcripts = st.session_state.transcripts
        analyse_transcripts(questions, transcripts)
