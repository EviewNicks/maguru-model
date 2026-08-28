# 📊 Laporan Dependensi & Environment Python (`maguru-model`)

Dokumen ini memuat daftar lengkap dependensi library Python yang digunakan di modul AI **`maguru-model`** beserta status sinkronisasi antara Conda Environment (`D:\conda_envs\maguru`), `environment.yml`, dan `requirements.txt`.

---

## 📌 Status Sinkronisasi Environment

- **Conda Env Target**: `D:\conda_envs\maguru`
- **Python Version**: `Python 3.10`
- **Status Status**: ✅ **100% Synced & Production-Ready**

---

## 📋 Daftar Library Utama & Kegunaannya

| Category | Package | Version Spec | Purpose / Functionality |
|---|---|---|---|
| **Core AI / LCEL** | `langchain` | `>=0.2.0, <2.0.0` | Orchestration framework AI (LCEL Chains & Prompts) |
| | `langchain-openai` | `>=0.1.0, <2.0.0` | OpenRouter / OpenAI LLM Integrator |
| | `langchain-community` | `>=0.2.0, <2.0.0` | Document Loaders (`PyPDFLoader`, `TextLoader`) |
| | `langgraph` | `>=0.1.0, <2.0.0` | Stateful multi-agent flow orchestration |
| **API Server** | `fastapi` | `>=0.110.0, <1.0.0` | High-performance REST Web Framework |
| | `langserve[all]` | `>=0.3.0, <1.0.0` | Streaming SSE endpoint exporter untuk LangChain |
| | `uvicorn[standard]` | `>=0.27.0, <1.0.0` | ASGI Server |
| | `sse-starlette` | `>=1.6.0, <2.0.0` | Server-Sent Events (SSE) streaming engine |
| | `python-multipart` | `>=0.0.9` | Form-data file uploader handler (`/admin/ingest`) |
| **Database & Vector**| `pgvector` | `>=0.2.5` | Supabase PostgreSQL Vector store client |
| | `psycopg2-binary` | `>=2.9.9` | PostgreSQL database driver |
| **LLM & Embeddings** | `openai` | `>=1.35.0, <2.0.0` | OpenRouter REST client integration |
| | `tiktoken` | `>=0.7.0` | Token counting for LLM context management |
| | `pypdf` | `>=4.0.0` | Extraction text PDF |
| **Config & DTO** | `pydantic` | `>=2.0.0, <3.0.0` | Data Validation & Serialization |
| | `pydantic-settings` | `>=2.0.0` | `.env` settings loader |
| | `python-dotenv` | `>=1.0.0, <2.0.0` | Environment variables parser |
| | `pyyaml` | `>=6.0.1, <7.0.0` | Prompt YAML template loader |
| **Testing** | `pytest` | `>=7.4.0` | Automated testing framework |
| | `pytest-cov` | `>=4.1.0` | Test coverage reporting |

---

## ⚡ Langkah-Langkah Verifikasi & Update Library di Conda Env

Jika Anda ingin memperbarui atau memastikan seluruh library di Conda env `D:\conda_envs\maguru` sudah versi terbaru yang sesuai, jalankan perintah ini di Terminal PowerShell:

```powershell
# 1. Aktifkan Conda Env
conda activate D:\conda_envs\maguru

# 2. Masuk ke direktori maguru-model
cd D:\.maguru\maguru-model

# 3. Eksekusi update/install via pip
pip install -r requirements.txt --upgrade
```

---

## 📝 Kesimpulan & Rekomendasi
Semua library di `environment.yml` dan `requirements.txt` telah tersinkronisasi 100%. Tidak ada pustaka usang (*deprecated*) yang digunakan. Sistem siap dijalankan dengan stabil pada environment `D:\conda_envs\maguru`.
