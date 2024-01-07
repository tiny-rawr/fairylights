import streamlit as st

def lip_syncing_avatar():
    st.title('🧙‍Lip Syncing Avatar')
    st.markdown("Turn any character image into a lip-syncing avatar that you can use in product demos, to bring your children's stories to life or create virtual gift cards!")

    with st.expander("✨ See project details"):
        st.subheader("Why I built this")
        st.markdown("I saw a [LinkedIn post by Steve Collins](https://www.linkedin.com/posts/stephenpaulcollins_linkedinavatar-aiinnovation-digitaltransformation-activity-7148969146737733632-tu4k?utm_source=share&utm_medium=member_desktop) where he created a lip-syncing avatar to introduce himself on LinkedIn. I immediately wanted to create one to enhance my 100 genai project demos (I don't like being on camera so this is really helpful)")
        st.subheader("Ways to use this")
        st.markdown("- 🐉 **Children's Bedtime Storties**: If you’re a parent, you can bring your kid’s bedtime stories to life by getting them to help you design a character, and even the voices for them! You can also use ai-generated voices for even more variety.")
        st.markdown("- 🎁 **Virtual Birthday Cards**: Imagine getting a video of an avatar who looks like your friend sitting on top of a giant cake singing you happy birthday in their actual voice! Or you know, in Morgan Freeman’s voice 😉")
        st.markdown("- 🚀 **Product Demos**: You can really easily create product demos where you get your avatar to present your product for you. You don’t even need to use your own voice if you’re really strapped for time.")
        st.subheader("Limitations")
        st.error("⚠️ **No API**: It would be really cool to be able to pass in text generated by an LLM, then converted to speech, and then get a pre-set character to lip-sync without having to upload the audio and image each time. I'm sure it won't be long before that's possible!")
        st.write("")

    st.video("projects/_004_lip_syncing_avatar/avatar_product_demo.mp4")
    st.markdown("If you want to create one of these yourself, I've written [a full step-by-step guide here](https://fairylightsai.substack.com/publish/post/140410588).")