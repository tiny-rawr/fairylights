import streamlit as st
from mixpanel import Mixpanel

def track_page_view():
    mp = Mixpanel(st.secrets["mixpanel"]["token"])
    mp.track(st.session_state['session_id'], 'Page Viewed', {'page_name': 'Thought Checker'})


def track_text_input():
    if 'text_entered' not in st.session_state:
        mp = Mixpanel(st.secrets["mixpanel"]["token"])
        mp.track(st.session_state['session_id'], 'Text Input', {
            'event': 'Text Entered in Journal Field',
            'page_name': 'Thought Checker'
        })
        st.session_state['text_entered'] = True


def track_journal_entry_input(journal_text, default_journal_entry):
    mp = Mixpanel(st.secrets["mixpanel"]["token"])
    if journal_text != default_journal_entry:
        mp.track(st.session_state['session_id'], 'Text Input', {
            'event': 'Journal Entry Input',
            'page_name': 'Thought Checker',
            'type': 'custom',
            'word_count': len(journal_text.split())
        })
    else:
        mp.track(st.session_state['session_id'], 'Text Input', {
            'event': 'Journal Entry Input',
            'page_name': 'Thought Checker',
            'type': 'demo',
            'word_count': len(journal_text.split())
        })


def track_form_submission():
    mp = Mixpanel(st.secrets["mixpanel"]["token"])
    mp.track(st.session_state['session_id'], 'Form Submitted', {
        'event': 'Journal Entry Submitted',
        'page_name': 'Thought Checker'
    })