import streamlit as st

def youtube_summariser():
    st.title('📼️ YouTube Summariser')
    st.markdown("Learn how to send yourself a recurring email summarising YouTube videos released by your top 5 favourite channels.")

    with st.expander("✨ See project details (and learning objectives)"):
        st.subheader("YouTube Summariser Email")
        st.markdown("Learn [how to use GenAI to summarise YouTube videos](https://fairylightsai.substack.com/p/youtube-summariser-ai-workshop) released by your favourite channels over the last week, month or quarter! Send them as a recurring email too!")
        st.subheader("Why I built this")
        st.markdown("A YouTube Digest helps you deal with information overwhelm by sending yourself a curated list of videos from your favourite channels. The custom GenAI summaries lets you extract the most value from the content, by making it work for you.")
        st.markdown("- **🙈 Intentional:** Summarise the key points of each video so you can decide which you most want to watch.")
        st.markdown("- **✅ Actionable:** Distill the video into action steps so you can apply the ideas to your life right now.")
        st.markdown("- **🎯 Applicable:** Extract key ideas from a video and apply them to your personal goals.")
        st.subheader("YouTube Summaries Email example:")
        st.markdown("After following the exercises in this Google CoLab notebook, one of my workshop attendees was able to create this email:")
        st.image("images/youtube_email_example.png", use_column_width=True)
        st.subheader("Demo Video:")
        st.video("demo_videos/youtube_summariser_demo.mp4")


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








