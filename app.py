"""
Maguru - AI Coding Learning Platform
Main Streamlit Application

A platform for learning Python coding with AI assistance.
"""

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import UI pages
from ui.pages import home, learn, quiz, progress
from utils.session_manager import init_session

# Page configuration
st.set_page_config(
    page_title="Maguru - Belajar Coding dengan AI",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #F0F2F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stProgress > div > div > div > div {
        background-color: #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function with multi-page routing."""

    # Initialize session
    if not st.session_state.get("initialized"):
        init_session()

    # Initialize current page if not set
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    # Sidebar navigation (hidden on Learn page for better chatbot visibility)
    current_page = st.session_state.get("current_page", "Home")

    if current_page != "Learn":
        with st.sidebar:
            st.title("🐍 Maguru")

            st.markdown("---")

            # Student info
            if st.session_state.get("student_name"):
                st.markdown(f"👤 **{st.session_state.student_name}**")
            else:
                st.markdown("👤 **Tamu**")

            st.markdown("---")

            # Navigation
            st.markdown("### Navigasi")

            page = st.radio(
                "Menu Utama:",
                ["Home", "Learn", "Quiz", "Progress"],
                index=["Home", "Learn", "Quiz", "Progress"].index(
                    st.session_state.get("current_page", "Home")
                )
            )

            # Update current page
            if page != st.session_state.current_page:
                st.session_state.current_page = page
                st.rerun()

            st.markdown("---")

            # Current course info
            if st.session_state.get("current_course"):
                from utils.content_loader import load_course_metadata
                metadata = load_course_metadata(st.session_state.current_course)
                if metadata:
                    st.markdown(f"**Kursus:** {metadata.get('title', 'N/A')}")

                if st.session_state.get("current_module"):
                    st.markdown(f"**Modul:** {st.session_state.current_module}")

                if st.session_state.get("current_session"):
                    st.markdown(f"**Sesi:** {st.session_state.current_session}")

            st.markdown("---")

            # Footer
            st.markdown("""
            <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            Made with ❤️ by Maguru Team
            </div>
            """, unsafe_allow_html=True)

    # Page routing
    current_page = st.session_state.get("current_page", "Home")

    if current_page == "Home":
        home.show()
    elif current_page == "Learn":
        learn.show()
    elif current_page == "Quiz":
        quiz.show()
    elif current_page == "Progress":
        progress.show()
    else:
        home.show()


if __name__ == "__main__":
    main()
