# Maguru - LangServe API Server

> **AI Backend Server** for Maguru Learning Platform - Exposes AI chains via FastAPI + LangServe

## 📋 Overview

LangServe-based API server that provides AI-powered learning assistance for the Maguru platform. Supports streaming chatbot responses, code explanations, hint generation, and quiz feedback.

## 🚀 Tech Stack

| Component | Technology |
|-----------|------------|
| **API Framework** | FastAPI |
| **AI Framework** | LangChain (LCEL) + LangServe |
| **LLM Provider** | OpenRouter (supports GPT-4, Gemma, Claude, etc.) |
| **Streaming** | Server-Sent Events (SSE) |

## Setup

### Backend (maguru-model/)

1. **Copy environment template:**
```bash
cp .env.example .env
```

2. **Edit `.env` and add your API keys:**
```bash
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_MODEL=google/gemma-7b-it:free
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run server:**
```bash
python server.py
# → Running on http://localhost:8000
```

### Frontend Integration

1. **Copy environment template:**
```bash
cp .env.local.example .env.local
```

2. **(Optional) Edit if backend runs on different port:**
```bash
NEXT_PUBLIC_LANGSERVE_URL=http://localhost:8000
```

3. **Install and run:**
```bash
npm install
npm run dev
# → Running on http://localhost:3000
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **CORS errors** | Check `ALLOWED_ORIGINS` in backend `.env` |
| **Connection refused** | Ensure backend is running on port 8000 |
| **API errors** | Verify `OPENROUTER_API_KEY` is valid |
| **Missing .env** | Copy `.env.example` to `.env` first |

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
