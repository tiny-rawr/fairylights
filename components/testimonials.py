import streamlit as st

def testimonial(name, quote, profile_image='images/profile-avatar.png'):
    st.markdown("---")
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image(profile_image, width=50, use_column_width=False)
    with col2:
        st.markdown(f"**{name}**")
        st.write(quote)
    st.markdown("---")