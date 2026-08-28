Ran command: `Get-Content "D:\.maguru\maguru-model\docs\SERVER_RUNNING_GUIDE.md"`

Membaca isi file `docs/SERVER_RUNNING_GUIDE.md`...

Berikut adalah penjelasan lengkap dan panduan praktis berdasarkan dokumen [**`docs/SERVER_RUNNING_GUIDE.md`**](file:///D:/.maguru/maguru-model/docs/SERVER_RUNNING_GUIDE.md) untuk menjalankan dan menguji (*manual testing*) apakah backend AI **`maguru-model`** dan endpoint **LangServe / FastAPI** berjalan dengan baik:

---

## 🚀 1. Cara Menjalankan Server AI Backend

Untuk menjalankan server AI, Anda membutuhkan terminal (PowerShell atau Command Prompt) dengan langkah-langkah berikut:

### Langkah A: Aktifkan Conda Environment
Karena seluruh library Python (`langchain`, `langgraph`, `langserve`, `fastapi`) terpasang pada Conda environment `maguru`:
```powershell
conda activate D:\conda_envs\maguru
```

### Langkah B: Masuk ke Folder Project
```powershell
cd D:\.maguru\maguru-model
```

### Langkah C: Jalankan Server
Gunakan launcher script:
```powershell
python server.py
```
*(Atau gunakan perintah uvicorn langsung:* `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`*)*

✅ Server akan aktif di **`http://localhost:8000`**.

---

## 🧪 2. Cara Melakukan Manual Testing (4 Metode)

Ada **4 cara praktis** untuk menguji apakah seluruh chain AI dan endpoint LangServe merespons dengan benar:

### 🌟 Cara 1: Menggunakan LangServe Playground (Paling Visual & Interaktif)
LangServe secara otomatis menyediakan UI antarmuka web khusus (*web playground*) untuk menguji AI tanpa perlu tool tambahan:
* **Chatbot AI Co-Teacher**: Buka [`http://localhost:8000/chatbot/playground/`](http://localhost:8000/chatbot/playground/)
* **Explain Code Chain**: Buka [`http://localhost:8000/explain-code/playground/`](http://localhost:8000/explain-code/playground/)
* **Hint Generator**: Buka [`http://localhost:8000/hint/playground/`](http://localhost:8000/hint/playground/)
* **Quiz Feedback**: Buka [`http://localhost:8000/quiz-feedback/playground/`](http://localhost:8000/quiz-feedback/playground/)

> **Cara tes:** Buka URL di browser, ketik pertanyaan/soal pada form input, lalu klik tombol **Start Streaming** atau **Invoke**. Anda akan melihat respons AI muncul secara langsung.

---

### 📋 Cara 2: Menggunakan Swagger UI (FastAPI Interactive Docs)
Untuk menguji endpoint REST API lengkap (termasuk SSE Streaming, Generate Quiz, dan Ingestion):
1. Buka browser ke **[`http://localhost:8000/docs`](http://localhost:8000/docs)**.
2. Anda akan melihat seluruh daftar endpoint:
   - `GET /health` : Cek apakah server online (respons: `{"status": "ok"}`).
   - `POST /api/v1/chat/invoke` : Uji chat Q&A dengan thread persistence.
   - `POST /api/v1/generate-quiz` : Uji pembuatan soal kuis otomatis.
   - `POST /api/v1/ingest` : Uji input materi teks ke knowledge base RAG.
3. Klik endpoint ➔ klik **Try it out** ➔ isi parameter JSON ➔ klik **Execute**.

---

### 📬 Cara 3: Menggunakan Postman Collection
Jika Anda lebih terbiasa menggunakan aplikasi **Postman**:
1. Buka aplikasi Postman.
2. Klik tombol **Import** (di pojok kiri atas).
3. Pilih file koleksi yang sudah disiapkan di:  
   [`D:\.maguru\maguru-model\postman\maguru_ai_postman_collection.json`](file:///D:/.maguru/maguru-model/postman/maguru_ai_postman_collection.json).
4. Seluruh request endpoint sudah tersusun rapi dengan contoh payload body yang siap dieksekusi.

---

### ⚡ Cara 4: Menggunakan Automated Unit Test (`pytest`)
Untuk memastikan semua logika internal, skema data, dan integrasi chain berfungsi tanpa mengonsumsi kuota token LLM (menggunakan mocking):
```powershell
python -m pytest tests/ -v
```
*(Saat ini seluruh 18 test telah terkonfigurasi dan 100% PASS).*

---

## 🛠️ Ringkasan Troubleshooting

| Gejala Error | Penyebab | Solusi |
|---|---|---|
| `ModuleNotFoundError` | Environment Conda belum aktif | Jalankan `conda activate D:\conda_envs\maguru` |
| `Address already in use` | Port 8000 sedang digunakan aplikasi lain | Matikan aplikasi lain di port 8000 atau ubah nilai `PORT` di `.env` |
| `500 Internal Server Error` saat invoke | Kunci API OpenRouter belum diisi / expired | Periksa isi parameter `OPENROUTER_API_KEY` di file `.env` |