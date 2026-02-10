# Maguru - AI Coding Learning Platform

> **Vision**: Platform edtech berbasis AI yang membantu siswa Indonesia belajar coding dengan pendekatan interaktif, personal, dan adaptif.

## 📋 Overview

Maguru adalah platform pembelajaran coding berbasis AI di mana siswa belajar Python melalui alur interaktif: **Teori → Praktik dengan AI Chatbot → Kuis → Prasyarat Review (jika gagal)**.

### Target User
- Siswa dengan **basic knowledge** (tidak absolute beginner)
- Fokus bahasa: **Python**
- Belajar mandiri dengan AI sebagai co-teacher

## 🚀 Tech Stack

| Component | Technology |
|-----------|------------|
| **UI Framework** | Streamlit |
| **AI Framework** | LangChain (LCEL + LangGraph) |
| **LLM** | GPT-3.5-turbo |
| **Auth** | Anonymous (no login for MVP) |
| **Data Storage** | Streamlit Session State |

## 🎯 Core Features (MVP)

### 1. Interactive Learning Flow
- Course Selection → AI Greeting → Theory Content → Chatbot Q&A → Quiz → Pass/Fail Decision
- AI menyapa siswa secara personal dan menjelaskan apa yang akan dipelajari
- Materi disajikan dalam format terstruktur dengan bahasa Indonesia

### 2. AI Capabilities
| Feature | Description |
|---------|-------------|
| **Code Explanation** | Jelaskan cara kerja kode dengan analogi real-world |
| **Hint Generation** | 3 level: gentle → conceptual → direct |
| **Quiz Feedback** | Explain jawaban benar/salah dengan positive reinforcement |
| **Adaptive Learning** | Rekomendasi prasyarat jika gagal kuis |
| **Q&A Chatbot** | Jawab pertanyaan siswa dengan context-aware responses |

### 3. Assessment System
- **Format**: Multiple Choice + Code Completion
- **Passing Score**: 70%
- **Retry**: Unlimited dengan automatic prerequisite review
- **Progress Tracking**: Visual progress indicators

## 📁 Project Structure

```
maguru/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Dependencies
├── .env                            # API keys (not in repo)
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── LICENSE                         # MIT License
│
├── docs/                           # Documentation
│   ├── project.md                  # Original project concept
│   └── new-project.md              # Detailed MVP specification
│
├── data/                           # Course content
│   └── courses/
│       └── python_basics/
│           ├── course.yaml
│           └── modules/
│
├── langchain/                      # AI components
│   ├── chains/
│   │   ├── explain_code.py
│   │   ├── hint_generator.py
│   │   └── quiz_feedback.py
│   ├── graphs/
│   │   └── adaptive_learning.py
│   └── prompts/
│
├── ui/                             # UI components
│   ├── pages/
│   │   ├── home.py
│   │   ├── learn.py
│   │   ├── quiz.py
│   │   └── progress.py
│   └── components/
│       ├── chatbot.py
│       └── progress_bar.py
│
└── utils/                          # Utilities
    ├── session_manager.py
    ├── content_loader.py
    └── quiz_validator.py
```

## 🔧 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- OpenAI API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/maguru.git
cd maguru
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

## 📚 Documentation

Detailed project documentation is available in the `docs/` directory:

- **`docs/new-project.md`** - Comprehensive MVP specification with detailed feature descriptions
- **`docs/project.md`** - Original project concept and vision

## 🗺️ Roadmap

### Phase 1: Foundation (Week 1)
- [x] Project documentation
- [ ] Project setup (Streamlit + LangChain)
- [ ] Course content structure (YAML/Markdown)
- [ ] Basic UI (Home, Course Selection)
- [ ] Session state management
- [ ] Content loading system

### Phase 2: Core Features (Week 1-2)
- [ ] Theory content display
- [ ] Basic chatbot with LCEL
- [ ] Code explanation chain
- [ ] Quiz UI and validation
- [ ] Progress tracking

### Phase 3: AI Enhancement (Week 2)
- [ ] Hint generation system
- [ ] Quiz feedback chain
- [ ] LangGraph adaptive flow
- [ ] Prerequisite review logic

### Phase 4: Polish (Week 2-3)
- [ ] Progress visualization
- [ ] Error handling
- [ ] UI/UX improvements
- [ ] Testing and bug fixes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Maguru Team

## 🙏 Acknowledgments

- LangChain team for the excellent AI framework
- Streamlit team for the amazing UI framework
- OpenAI for GPT models

---

**Project Status**: 🚧 In Development

**Last Updated**: February 2025
