import streamlit as st
from gpt_api_calls import identify_cognitive_distortions, categorise_cognitive_distortions


def get_journal_entry():
    form_submission = False

    if not form_submission:
        form_container = st.empty()

        with form_container.form(key='thought_checker'):
            default_journal_entry = """Today was terrible, just like every other day. It started off with me burning my toast—what a perfect example of how I can't do anything right. Clearly, I'm a total failure, not just in toasting bread but in life. I'm so clumsy and useless; it's no wonder people don't want to be around me.\n\nI got to work late because of traffic. As I walked in, I caught a glimpse of my boss's face, and I knew he was thinking, "Here's that useless employee who can't even show up on time." Everyone at work must hate me; it's the only explanation. To top it off, a meeting was scheduled for tomorrow, and I'm convinced it's going to be about laying people off. I'm sure I'll be the first one to go.\n\nMy colleague complimented me on my presentation, but she was just being nice. Any idiot could have done it, and it probably didn't even matter because I stuttered during the Q&A. My whole career is a joke, built on some lucky breaks."""
            journal_text = st.text_area("Journal entry:", value=default_journal_entry, height=300, max_chars=2000)
            submitted = st.form_submit_button('Submit')

        if submitted:
            form_submission = True
            form_container.empty()  # Clear the form container

    if form_submission:
        return journal_text


def highlight_text(journal_entry, quotes):
    for quote in quotes:
        journal_entry = journal_entry.replace(quote, f"<span style='border: solid black 1px; border-radius: 5px; padding: 0px 5px; background: #31333F; color: white; hover: cursor;'>{quote}</span>")

    return journal_entry


def process_journal_entry(journal_text):
    info_placeholder = st.empty()

    info_placeholder.info("(1/2) Identifying all thinking patterns in your journal entry...")
    cognitive_distortions = identify_cognitive_distortions(journal_text)
    info_placeholder.info("(2/2) Explaining and reframing...")
    distortions = categorise_cognitive_distortions(cognitive_distortions.get("quotes"))
    distortions_by_category = {}
    info_placeholder.empty()

    for pattern in distortions.get("thinking_patterns"):
        category = pattern.get("thinking_pattern")
        quote = pattern.get("quote")
        explanation = pattern.get("explanation")
        reframe = pattern.get("reframe")

        if category not in distortions_by_category:
            distortions_by_category[category] = []
        distortions_by_category[category].append((quote, explanation, reframe))

    # Sort the categories by the number of entries (in descending order)
    sorted_categories = sorted(distortions_by_category.items(), key=lambda x: len(x[1]), reverse=True)

    # Display the categories in sorted order
    for category, entries in sorted_categories:
        with st.expander(f"{category} (x {len(entries)})"):
            for entry in entries:
                st.markdown(
                    f"- **\"{entry[0][0].upper() + entry[0][1:]}\"** - {entry[1]} \n<span style='background: #C7F5F0;'>{entry[2]}</span>",
                    unsafe_allow_html=True)


def thought_checker():
    st.title('🧠 Thought Checker')
    st.write(
        'Enter a journal entry, and this program will auto-detect unhelpful thinking patterns (cognitive distortions) that are present in your entry, so you can focus on the more helpful reframing part.')
    journal_text = get_journal_entry()
    if journal_text:
        distortions = identify_cognitive_distortions(journal_text).get("quotes")
        st.markdown(f"<div style='padding: 20px 20px 10px 20px; border-radius: 5px; background: #F0F2F6'>{highlight_text(journal_text, distortions)}</div>",unsafe_allow_html=True)
