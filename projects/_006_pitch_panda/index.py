import streamlit as st

def pitch_panda():
    st.title('🐼 Pitch Panda')
    st.markdown("A robotic plush panda you can have a two-way convo with! Winner of the People's Choice Award at a Young Entrepreneur Pitch night. Collab project with Stan!")

    with st.expander("✨ See project details"):
        st.subheader("Why I built this")
        st.markdown("Within 15m of seeing [this TikTok video by David from Dippaverse](https://vt.tiktok.com/ZSLEnCEGu/), where David had a conversation with a robotic plush brown bear, I had bought my own bear to do the same ✨🤯")
        st.subheader("Awards")
        st.warning("🏆 Late last year, my friend [Stan](https://www.linkedin.com/in/stanleaf?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADRVb2QB43kcXPLI2AI7fGY09X8uBpCfO8k&lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_all%3BRsO59E%2FURsO%2FFyTK4P%2FMQg%3D%3D) and I won the [People’s Choice Award at Fishburner’s Young Entrepreneur Pitch night](https://www.linkedin.com/posts/fishburners_entrepreneurs-genz-ai-activity-7120150734930673664-v_Wq), where I demo’d chatting with the panda on stage in front of 200+ founders and entrepreneurs 🐼🎤")
        st.markdown("The CEO of fishburners said: 👏🏼 People's Choice: 🦕 Becca Williams, Founder of fairylights.ai, in a landslide victory after the most captivating display of generative-AI + tech in action we've ever seen!")
        st.subheader("Limitations")
        st.error("⚠️ **Latency**: The conversation isn't real time, there is a noticable lag between finishing talking to the panda and it responding. Could be sped up by streaming the response and converting it to speech in chunks rather than waiting until it's all finished generating.")
        st.error("⚠️ **Incomplete**: The panda is unfinished. It's currentyl wearing a raspberry pi backpack with dubious wires sticking out everywhere instead of it all being safely housed in it's body.")

    st.video("projects/_006_pitch_panda/pitch_panda_demo.mp4")
    st.markdown("If you want to create one of these yourself, I've written [a full step-by-step guide here](https://fairylightsai.substack.com/p/8-chatgpt-powered-robot-panda).")