"""
Maguru - AI Coding Learning Platform
Main Streamlit Application

A platform for learning Python coding with AI assistance.
"""

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""

    # Header
    st.markdown('<h1 class="main-header">🐍 Maguru</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Belajar Coding dengan AI sebagai Co-Teacher</p>",
                unsafe_allow_html=True)

    # Introduction
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='info-box'>
        <h3>🎯 Interaktif</h3>
        <p>Belajar dengan AI chatbot yang siap membantu menjawab pertanyaan Anda.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='info-box'>
        <h3>📚 Personal</h3>
        <p>Learning path yang disesuaikan dengan kemampuan dan kebutuhan Anda.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='info-box'>
        <h3>🚀 Adaptif</h3>
        <p>Sistem review otomatis jika mengalami kesulitan pada materi.</p>
        </div>
        """, unsafe_allow_html=True)

    # Coming Soon Section
    st.markdown("---")
    st.subheader("🚀 Coming Soon")

    st.markdown("""
    Maguru sedang dalam pengembangan. Fitur yang akan tersedia:

    - **Interactive Learning Flow** - Belajar teori dengan bimbingan AI
    - **Code Explanation** - Penjelasan kode yang mudah dipahami
    - **Hint System** - Bantuan bertahap saat stuck
    - **Quiz & Challenges** - Uji pemahaman dengan feedback detail
    - **Progress Tracking** - Pantau perkembangan belajar Anda
    - **Adaptive Review** - Review otomatis jika gagal kuis
    """)

    # Tech Stack
    with st.expander("🔧 Tech Stack"):
        st.markdown("""
        - **UI**: Streamlit
        - **AI Framework**: LangChain (LCEL + LangGraph)
        - **LLM**: GPT-3.5-turbo
        - **Language**: Python
        """)

    # Documentation
    with st.expander("📚 Documentation"):
        st.markdown("""
        Lihat dokumentasi lengkap di repository:

        - [Project Specification](docs/new-project.md) - Detail fitur MVP
        - [Original Concept](docs/project.md) - Konsep awal proyek
        - [Contributing Guide](CONTRIBUTING.md) - Cara berkontribusi
        """)

    # Status
    st.markdown("---")
    st.info("🚧 **Status**: Project dalam tahap pengembangan. Ikuti perkembangannya di repository ini!")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    <p>Made with ❤️ by Maguru Team</p>
    <p>© 2025 Maguru. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
