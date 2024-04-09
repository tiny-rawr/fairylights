import streamlit as st
from projects._008_youtube_summariser_email.youtube_api import get_channel_id_from_username, get_channel_details


def youtube_summariser():
    st.title('📼️ YouTube Email Summariser Workshop')
    st.markdown("Learn how to send yourself a monthly email summarising YouTube videos released by your top 5 favourite channels.")

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

    youtubers_input = st.text_input("Enter YouTuber usernames (as comma-separated list):", placeholder="timferriss, jamesbriggs, DonatienThorez, plumvillageonline, AIJasonZ", value="timferriss, jamesbriggs, DonatienThorez, plumvillageonline, AIJasonZ")
    youtubers = youtubers_input.split(",")

    get_youtubers = st.button("Get Channels")

    if youtubers and get_youtubers:
        num_cols = 5

        for i, youtuber in enumerate(youtubers):
            if i % num_cols == 0:
                cols = st.columns(num_cols)

            col_index = i % num_cols

            with cols[col_index]:
                # Example values for demonstration purposes
                # channel_id = get_channel_id_from_username(youtuber.strip())
                # channel_details = get_channel_details(channel_id)
                # name = channel_details['snippet']['title']
                # thumbnail = channel_details['snippet']['thumbnails']['medium']['url']
                name = "Tim Ferris"
                thumbnail = "https://i.imgur.com/BUpvSqA.jpg"
                st.image(thumbnail, use_column_width=True)
                html_link = f'<div>👉 <a href="https://www.youtube.com/@{youtuber}" style="font-size: 14px;" target="_blank"><b>{youtuber}</b></a></div>'
                st.markdown(html_link, unsafe_allow_html=True)