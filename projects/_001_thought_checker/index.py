import streamlit as st

def process_journal_entry():
  with st.form(key='thought_checker'):
    default_journal_entry = """Today was terrible, just like every other day. It started off with me burning my toast—what a perfect example of how I can't do anything right. Clearly, I'm a total failure, not just in toasting bread but in life. I'm so clumsy and useless; it's no wonder people don't want to be around me.\n\nI got to work late because of traffic. As I walked in, I caught a glimpse of my boss's face, and I knew he was thinking, "Here's that useless employee who can't even show up on time." Everyone at work must hate me; it's the only explanation. To top it off, a meeting was scheduled for tomorrow, and I'm convinced it's going to be about laying people off. I'm sure I'll be the first one to go.\n\nMy colleague complimented me on my presentation, but she was just being nice. Any idiot could have done it, and it probably didn't even matter because I stuttered during the Q&A. My whole career is a joke, built on some lucky breaks."""
    journal_text = st.text_area("Journal entry:", value=default_journal_entry, height=300, max_chars=2000)

    # Form submission button
    submitted = st.form_submit_button('Submit')
    if submitted:
      st.write('You have submitted the following journal entry:')
      st.write(journal_text)


def thought_checker():
    st.title('🧠 Thought Checker')
    st.write('Enter a journal entry, and this program will auto-detect unhelpful thinking patterns (cognitive distortions) that are present in your entry, so you can focus on the more helpful reframing part.')
    process_journal_entry()