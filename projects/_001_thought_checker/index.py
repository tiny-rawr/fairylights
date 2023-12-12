import streamlit as st
from gpt_api_calls import identify_cognitive_distortions, categorise_cognitive_distortions


def get_journal_entry():
    form_submission = False

    if not form_submission:

        form_container = st.empty()

        with form_container.form(key='thought_checker'):
            default_journal_entry = """(Replace this with your own journal entry if you want): \n\nToday was terrible, just like every other day. It started off with me burning my toast—what a perfect example of how I can't do anything right. Clearly, I'm a total failure, not just in toasting bread but in life. I'm so clumsy and useless; it's no wonder people don't want to be around me.\n\nI got to work late because of traffic. As I walked in, I caught a glimpse of my boss's face, and I knew he was thinking, "Here's that useless employee who can't even show up on time." Everyone at work must hate me; it's the only explanation. To top it off, a meeting was scheduled for tomorrow, and I'm convinced it's going to be about laying people off. I'm sure I'll be the first one to go.\n\nMy colleague complimented me on my presentation, but she was just being nice. Any idiot could have done it, and it probably didn't even matter because I stuttered during the Q&A. My whole career is a joke, built on some lucky breaks."""
            journal_text = st.text_area("Journal entry:", value=default_journal_entry, height=300, max_chars=2000)
            submitted = st.form_submit_button('Submit')

        if submitted:
            form_submission = True
            form_container.empty()  # Clear the form container

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


def thought_checker():
    st.title('🧠 Thought Checker')
    st.markdown("Enter a journal entry and this GenAI program will auto-detect unhelpful thinking patterns (cognitive distortions) that are present in your entry, so you can focus on reframing them.")
    with st.expander("✨️  See Project Details"):
      st.markdown("- 🛠️ **Tools:** OpenAI - gpt-3.5-turbo [chat completion model](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) with function calling (see [code snippet](https://gist.github.com/tiny-rawr/e411d3ff31af0cf5a6a72b640502ea3f)).")
      st.markdown("- 💖 **Pain Point Addressed:** Reading a journal entry multiple times trying to spot cognitive distortions is draining, and can reduce the likelihood of completing or attempting the exercise on low-energy/mood days. This program outsources the identification step, so all energy can go to the higher-impact reframing step.")
      st.markdown("- ⚠️ **Limitations:** 75% accuracy (still more helpful than not having the program at all). Sometimes labels factual or realistic statements as distortions, e.g. 'I will never see my cat again' can be flagged as 'fortune telling' when it's true (pet died).")
      st.markdown("- 💌 Read the full [deep dive build process here](https://fairylightsai.substack.com/p/analyse-a-journal-entry-for-unhelpful).")

    info_placeholder = st.empty()
    info_placeholder.info("We don't save or see any of your data, so once you refresh the page it'll be lost.")

    journal_text = get_journal_entry()
    api_key = st.session_state.get('api_key', '')

    if not api_key:
        info_placeholder.error("🔐  Please enter an OpenAI API key in the sidebar.")
        return

    if journal_text:
        info_placeholder.info("(1/2) Identifying all thinking patterns in your journal entry...")
        quotes = identify_cognitive_distortions(journal_text).get("quotes")

        info_placeholder.info("(2/2) Explaining and reframing...")
        distortions = categorise_cognitive_distortions(quotes)

        info_placeholder.empty()
        st.markdown(f"<div style='padding: 20px 20px 10px 20px; border-radius: 5px; background: #F0F2F6'>{highlight_text(journal_text, distortions)}</div>",unsafe_allow_html=True)
        st.success("💖 Your turn. Choose the thinking pattern that causes you the most pain right now, then replace it with a positive and balanced affirmation. Use statements that reflect a more realistic and compassionate view of yourself and the situation.")
