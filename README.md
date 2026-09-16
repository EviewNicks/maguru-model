# Maguru - LangServe API Server (`maguru-model`)

> **AI Backend Server** for Maguru Learning Platform - Exposes AI chains via FastAPI + LangServe & RAG Vector Engine.

---

## 🚀 Quick Start (Running with Conda)

### 1. Aktifkan Environment Conda (`D:\conda_envs\maguru`)
```powershell
conda activate D:\conda_envs\maguru
```

### 2. Masuk ke Folder Project & Konfigurasi `.env`
```powershell
cd D:\.maguru\maguru-model
cp .env.example .env
```

### 3. Jalankan Server FastAPI
```powershell
python server.py
# → Running on http://localhost:8000
```

---

## 📚 Interactive Docs & Postman Testing

- **Swagger UI Interactive**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Postman Collection**: [postman/maguru_ai_postman_collection.json](file:///D:/.maguru/maguru-model/postman/maguru_ai_postman_collection.json)
- **Panduan Jalankan Server Lengkap**: [docs/SERVER_RUNNING_GUIDE.md](file:///D:/.maguru/maguru-model/docs/SERVER_RUNNING_GUIDE.md)

---

## 🛠️ Main Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | `GET` | Server Health Status |
| `/api/v1/generate-quiz` | `POST` | Automated Quiz Generation (JSON Schema) |
| `/api/v1/ingest` | `POST` | Auto-Ingest Creator Lesson Text into `pgvector` |
| `/chatbot/stream` | `POST` | LangServe SSE Streaming Chatbot |
| `/generate-quiz/invoke` | `POST` | LangServe Quiz Generator Chain Invoke |
