import streamlit as st

st.set_page_config(
    page_title="Plot Bot",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    st.title("Welcome to Plot Bot")
    st.markdown(
    """
    Plot Bot is a football visualization app enhanced with AI chatbot assistance. It uses free data 
    from Hudl Statsbomb datasets and integrates Gemini AI for better interpretations. Select the Match Analysis in the sidebar to proceed.

    ### Features:
    - **Match Analysis**: Visualize actions for a specific match, and compare the two teams.
    """
    )

if __name__ == "__main__":
    main()