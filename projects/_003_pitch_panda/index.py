import streamlit as st
from components.testimonials import testimonial

def pitch_panda():
    st.title('🐼 Pitch Panda')
    st.write("A collaborative project with [Stan](https://www.linkedin.com/in/stanleaf?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADRVb2QB43kcXPLI2AI7fGY09X8uBpCfO8k&lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_all%3Bx%2FVwbXzhRCOLCLq6CnlpFw%3D%3D), combining his IOT superpowers with my GenAI skills. We developed this robotic plush panda you can have a two-way conversation with.")
    st.write("🛠️ OpenAI (GPT-3.5-turbo, function calling), Eleven Labs, Raspberry Pi")
    st.success("🏆 Winner of the [People's Choice Award at Fishburners young entrepreneur pitch night 2023](https://www.linkedin.com/posts/fishburners_entrepreneurs-genz-ai-activity-7120150734930673664-v_Wq)")
    testimonial('Martin Karafilis - CEO of Fishburners', "👏🏼 People's Choice: 🦕 Becca Williams, Founder of fairylights.ai, in a landslide victory after the most captivating display of generative-AI + tech in action we've ever seen!", 'images/testimonials/martin-karafilis.jpeg')
