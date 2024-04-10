from projects._008_youtube_summariser_email.youtube_api import get_channel_id_from_username, get_channel_details, get_videos_from_playlist
from projects._008_youtube_summariser_email.gpt_api import summarise_transcript
from projects._008_youtube_summariser_email.email_template import generate_summarised_video_section, generate_email_template, send_email
import streamlit as st
import pandas as pd

def load_prompts(url):
    df = pd.read_csv(url)
    prompts = df.set_index('Name')['Prompt'].to_dict()
    return prompts

def get_youtuber_details(username):
    channel_id = get_channel_id_from_username(username.strip())
    channel_details = get_channel_details(channel_id)
    return {
        "channel_id": channel_id,
        "channel_username": username.strip(),
        "channel_name": channel_details['snippet']['title'],
        "thumbnail": channel_details['snippet']['thumbnails']['medium']['url'],
        "uploads_playlist_id": channel_details['contentDetails']['relatedPlaylists']['uploads']
    }
def display_youtuber_details(youtubers):
    num_cols = 5

    for i, youtuber in enumerate(youtubers):
        if i % num_cols == 0:
            cols = st.columns(num_cols)

        col_index = i % num_cols

        with cols[col_index]:
            name = youtuber["channel_name"]
            thumbnail = youtuber['thumbnail']
            st.image(thumbnail, use_column_width=True)
            html_link = f'<div>👉 <a href="https://www.youtube.com/@{youtuber["channel_username"]}" style="font-size: 14px;" target="_blank"><b>{name}</b></a></div>'
            st.markdown(html_link, unsafe_allow_html=True)

def youtube_summariser():
    st.title('📼️ YouTube Summariser')
    st.markdown("Learn how to send yourself a recurring email summarising YouTube videos released by your top 5 favourite channels.")

    with st.expander("✨ See project details (and learning objectives)"):
        st.subheader("Why I built this")
        st.markdown("I'm teaching my first workshop at the University of Technology Sydney as part of Sydney's AI Happy Hour Meetup. I gave three project ideas to choose from and this was the one chosen.")
        st.subheader("Problem this solves")
        st.write("Getting a summary of videos released by your favourite YouTube channels means that you can decide which one is worth spending your limited time watching, without missing out on any of the content of your other channels.")
        st.subheader("The Workshop: Learning Objectives")
        st.write("✅ Enter the RSS feed URL to your favourite channels and get back the videos published by them over a chosen time period, along with key channel details like name, description & image.")
        st.write("✅ Get the transcript of the video using Whisper.")
        st.write("✅ Write a prompt to extract the key details you care about from the transcript using OpenAI Funciton calling.")
        st.write("✅ Write a prompt to turn your extracted info into a content block formatted the way you want it to with GPT-3.5.")
        st.write("✅ Extract video screenshots at key timestamps.")
        st.write("✅ Create an email template for sharing your summaries.")
        st.write("✅ Send an automated email to yourself with YouTube video summaries.")
        st.subheader("Demo Video")
        st.write("[INSERT DEMO VIDEO]")

    st.subheader("Step 1: Get YouTube Channel Details")

    youtubers_input = st.text_input(
        "Enter YouTuber usernames (as comma-separated list):",
        placeholder="timferriss, jamesbriggs, DonatienThorez, plumvillageonline, AIJasonZ",
        value="timferriss, jamesbriggs, DonatienThorez, plumvillageonline, AIJasonZ"
    )
    youtubers = youtubers_input.split(",")

    get_youtubers = st.button("Get Channels")

    if get_youtubers:
        st.session_state['youtuber_usernames'] = youtubers

    all_youtuber_details = []

    if 'youtuber_usernames' in st.session_state:
        for youtuber_username in st.session_state['youtuber_usernames']:
            details = get_youtuber_details(youtuber_username)
            all_youtuber_details.append(details)
        display_youtuber_details(all_youtuber_details)

    st.subheader("2: Write prompt instructions")
    st.write("Tell GPT how you want it to summarise video transcripts. You can try one of our demo prompts below or write your own.")

    with st.expander("📝Prompt writing tips"):
        st.markdown("Prompt writing tips from [OpenAI's Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering/six-strategies-for-getting-better-results):")
        st.markdown("- **Write clear instructions:** Describe the steps needed to complete a task. If outputs are too long, ask for brief replies and specify the format you want.")
        st.markdown("- **Give good examples**: Find a profile you really like and ask an LLM to describe it's writing style and tone. Use that to help you write better bio-writing prompt instructions.")
        st.markdown("- **Split tasks into simpler subtasks:** For example, if you want both a long and short bio to be used on different parts of the site, create a long bio first and then use that long bio to create the short one in two separate tasks.")
        st.markdown("- **Adopt a persona:** Ask the model to pretend they are the specialist writing their own bio.")
        st.markdown("- **Follow-ups**: If you find yourself adding follow-up prompts to modify some part of the output, that might be a good candidate to add back into the original prompt.")

    prompts = load_prompts("https://docs.google.com/spreadsheets/d/e/2PACX-1vTOEXm4-jguHN7ADkLX4dedTAzJ3UAsahHSuhc4T2hAW8PzcsGWaxyUAX4ScuGhW-cyffOAg4IGxWY8/pub?gid=0&single=true&output=csv")
    selected_prompt = st.selectbox("Use a demo prompt:", options=list(prompts.keys()), index=0, key="prompt_selection")
    prompt = st.text_area("Write your own prompt:", value=prompts[selected_prompt], height=150, key="prompt_instructions")

    st.subheader("Step 3: Retrieve & Summarise videos")
    timeframe_options = {"Week": 7, "Month": 30, "Quarter": 120}
    selected_timeframe = st.selectbox("Pick the timeframe you want to retrieve videos from:", list(timeframe_options.keys()))

    retrieve_videos = st.button(f"Get videos from the last {selected_timeframe.lower()}")
    if 'summary_html_sections' not in st.session_state:
        st.session_state['summary_html_sections'] = []

    if retrieve_videos:
        all_videos = []
        status = st.empty()
        for youtuber in all_youtuber_details:
            playlist_id = youtuber["uploads_playlist_id"]
            channel_name = youtuber["channel_name"]
            status.info(f"Getting videos from {channel_name}'s channel")
            videos = get_videos_from_playlist(playlist_id, timeframe_options[selected_timeframe])
            all_videos.append(videos)

        flat_videos = [video for group_videos in all_videos for video in group_videos]

        st.success(f"{len(flat_videos)} videos were published over the last {selected_timeframe.lower()}")

        for video_index, video_obj in enumerate(flat_videos):
            if video_index % 2 == 0:
                col1, col2 = st.columns(2)

            transcript = video_obj.get('transcript', '')[:70000]
            summary = summarise_transcript(prompt, transcript)
            st.session_state['summary_html_sections'].append(generate_summarised_video_section(video_obj, summary))

            col = col1 if video_index % 2 == 0 else col2

            with col:
                col.image(video_obj.get('thumbnail', ''), use_column_width=True)
                html_link = f'<div>👉 <a href="https://www.youtube.com/watch?v={video_obj.get("video_id", "")}" style="font-size: 14px;" target="_blank"><b>{video_obj.get("title", "")}</b></a></div>'
                col.markdown(html_link, unsafe_allow_html=True)
                col.write(summary)

    st.subheader("Step 4: Send summaries via email")
    sender_email = st.text_input("Sender Email:", placeholder="sender@fairylights.com")
    subscribers = st.text_input("Comma-separated subscriber list:", placeholder="subscriber1@gmail.com, subscriber2@yahoo.com")
    subject_line = st.text_input("Email subject line:", value="🤖 YAYY YouTube Summaries Woo Hoo!")

    email_body = generate_email_template(sender_email, subject_line, st.session_state['summary_html_sections'])

    send_one_email = st.button("Send email to subscribers now")

    if send_one_email:
        send_email(sender_email, subscribers, subject_line, email_body)
        st.success("Email sent!")








