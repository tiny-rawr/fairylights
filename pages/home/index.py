import streamlit as st
def home():
    st.title("🚀 100 GenAI projects 🤖")
    st.write("I can't wait to explore what's possible with generative AI with you by shipping 100 happy and helpful use-cases. Every project shipped here has solved a problem for at least one real person. Try them out for yourself, and [subscribe for the newest possibilities](https://fairylightsai.substack.com/) 💌🥰")

    with st.expander("🥰 See Timeline of Magical Milestones"):
            st.markdown("**Dec 2023**")
            st.markdown("- 🎉 Launched this 100 GenAI project site with first use-case.")

            st.markdown("**Nov 2023**")
            st.markdown("- 🚀 One of my proprietry GenAI use-cases led to a 350% in organic traffic and 300% increase in patient bookings for a health startup in a single month.")
            st.write("")
            st.image("images/bookings-made-from-generated-profiles.png")

            st.markdown("**Oct 2023**")
            st.markdown("- 👷‍ Became a community advisor at [AI Builders Club](https://www.linkedin.com/company/the-builders-club-ai/) which does weekly hackathons and opens up a world of opportunities for fellow builders and founders (joined at 250 members on the Slack channel).")
            st.markdown("- 🚀‍ Launched [Humans of Builders club series](https://builder-club.beehiiv.com/), which interviews one builder about their incredibly inspiring build journeys.")

            st.markdown("**Sep 2023**")
            st.markdown("- 📈 First 50 subscribers at [Fairylights newsletter](https://fairylightsai.substack.com/).")
            st.markdown("- 🏆 Won people's choice award at Fishburners Young Entrepreneur Pitch Night for a robotic plush panda you can have a two-way convo with (collab project with a friend who did the IOT and I did the GenAI).")
            st.write("")
            st.image("images/pitch_panda.webp")

            st.markdown("**Aug 2023**")
            st.markdown("- 🚀 Started Fairylights newsletter ([sign up here](https://fairylightsai.substack.com/)).")
            st.write("")

    st.subheader("Thought Checker")
    st.write("Enter a journal entry and this GenAI program will auto-detect unhelpful thinking patterns (cognitive distortions) that are present in your entry, so you can focus on reframing them.")
    st.markdown("[Try it out!](https://100-genai-projects.streamlit.app/?project=thought-checker)")
    st.image("images/featured/thought_checker.png", use_column_width=True)