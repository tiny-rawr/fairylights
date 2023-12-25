import streamlit as st
from projects._001_thought_checker.demo_data.example_journal_entry import example_journal_entry as default_journal_entry
from projects._001_thought_checker.gpt_api_calls import identify_cognitive_distortions, categorise_cognitive_distortions
from projects._001_thought_checker.event_tracking import track_text_input, track_journal_entry_input, track_form_submission
import uuid

def initialize_session():
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())

def get_journal_entry(default_journal_entry):
    form_submission = False

    if not form_submission:
        form_container = st.empty()

        with form_container.form(key='thought_checker'):
            journal_text = st.text_area("Journal entry:", value=default_journal_entry, height=300, max_chars=2000)

            track_text_input()
            submitted = st.form_submit_button('Submit')

        if submitted:
            track_journal_entry_input(journal_text, default_journal_entry)
            track_form_submission()
            form_submission = True
            form_container.empty()

    if form_submission:
        return journal_text


def highlight_text(journal_entry, distortions):
    tooltip_style = '''
    <style>
    .tooltip {
      position: relative;
      background-color: #555;
      color: #fff;
      text-align: center;
      border-radius: 6px;
      padding: 5px;
      opacity: 1;
      transition: background-color 0.3s;
    }

    .tooltip:hover {
      background-color: #DF0082 !important;
      cursor: pointer;
    }

    .tooltiptext {
      visibility: hidden;
      width: 300px;
      background-color: #DF0082;
      color: #fff;
      text-align: center;
      border-radius: 6px;
      padding: 5px;
      position: absolute;
      z-index: 1;
      bottom: 125%; /* Position the tooltip above the text */
      left: 50%;
      margin-left: -150px;
      opacity: 0;
      transition: opacity 0.3s;
    }

    .tooltip:hover .tooltiptext {
      visibility: visible;
      opacity: 1;
    }
    </style>
    '''
    st.markdown(tooltip_style, unsafe_allow_html=True)
    for distortion in distortions.get("thinking_patterns"):
        quote = distortion.get("quote")
        pattern = distortion.get("thinking_pattern")
        explanation = distortion.get("explanation")
        quote_text = f"<span class='tooltip' style='border-radius: 5px; padding: 0px 5px; background: #31333F; color: white;'>{quote}"
        tooltip = f'{quote_text}<span class="tooltiptext"><strong>{pattern}</strong>: {explanation}</span></span>'
        journal_entry = journal_entry.replace(quote, tooltip)

    return journal_entry

def display_project_details():
    with st.expander("✨ See project details"):
        st.subheader("Why I built this")
        st.write("This was something I built for myself. A mental health exercise that really helps me, is re-reading past journal entries for days where I feel lower, identifying unhelpful thinking patterns based on a set list of cognitive distortions, then reframing the ones that are especially unhelpful and recurring. However, I rarely did this because re-reading past entries and identifying distortions was suuper draining, so I needed something to outsource that step for me so I could focus on reframing.")
        st.subheader("Real-life Impact")
        st.warning("🥰 **20 vs 1 exercise completions in a month:** I went from completing this super helpful reframing exercise once in a month to 20 times, because the emotionally exhausting step has been removed. I'm very grateful for this use-case.")
        st.subheader("Ways to use this")
        st.markdown("- **💖 Reframing thoughts:** Set a timer for 5 minutes and write a stream of conciousness about your day, with zero filter. Click submit and browse through the unhelpful thinking patterns that have been highlighted if any. Pick the one that is causing you the most pain right now, and focus on reframing just that. Reframing is where you come up with postive but truthful statements to help you nudge your mindset in a more empowering direction for a specific thought.")
        st.markdown("- **🎙️ News bias:** You can paste in a news article or transcript and spot unhelpful thinking patterns that can lead to strong negative feelings.")
        st.subheader("Limitations")
        st.markdown("- ⚠️ **75% accuracy** Sometimes labels factual or realistic statements as distortions, which can be extra frustrating for painful events, e.g. 'I will never see my cat again' can be flagged as 'fortune telling' when it's true (pet died). 75% accuracy is still better than not having it in my opinion.")
        st.markdown("- ⚠️ **Unique patterns**: Different parts of the exact same journal entry can be highlighted across different submissions. For the most part, the same ones are highlighted but not exact. Same as doing it manually as a human.")
        st.subheader("Extra")
        st.markdown("- 💌 Read the [newsletter about this](https://fairylightsai.substack.com/p/analyse-a-journal-entry-for-unhelpful).")


def thought_checker():
    initialize_session()

    st.title('🧠 Thought Checker')
    st.markdown("Enter a journal entry and this GenAI program will auto-detect unhelpful thinking patterns (cognitive distortions) that are present in your entry, so you can focus on reframing them.")
    display_project_details()
    info_placeholder = st.empty()
    info_placeholder.warning("⚠️ This app is not a replacement for professional medical or mental health advice. For personalized guidance, please consult a qualified healthcare or mental health professional 💖")

    journal_text = get_journal_entry(default_journal_entry)
    api_key = st.session_state.get('api_key', '')

    if not api_key:
        info_placeholder.error("🔐  Please enter an OpenAI API key in the sidebar.")
        return

    if journal_text:
        info_placeholder.info("(1/2) Identifying all thinking patterns in your journal entry...")
        quotes = identify_cognitive_distortions(journal_text).get("quotes")

        info_placeholder.info("(2/2) Explaining and reframing...")
        if len(quotes) > 0:
            distortions = categorise_cognitive_distortions(quotes)

            info_placeholder.empty()
            st.markdown(
                f"<div style='padding: 20px 20px 10px 20px; border-radius: 5px; background: #F0F2F6'>{highlight_text(journal_text, distortions)}</div>",
                unsafe_allow_html=True)
            st.success("💖 Your turn. Choose the thinking pattern that causes you the most pain right now, then replace it with a positive and balanced affirmation. Use statements that reflect a more realistic and compassionate view of yourself and the situation.")

        else:
            info_placeholder.info("No cognitive distortions found!")
            return