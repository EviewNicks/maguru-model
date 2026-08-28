# 🚀 Panduan Jalankan Server & Testing API Modul AI (`maguru-model`)

Dokumen ini berisi panduan lengkap langkah demi langkah untuk mengaktifkan environment Conda, menjalankan server FastAPI + LangServe, serta melakukan pengujian API menggunakan **Swagger UI**, **Playground**, dan **Postman**.

---

## 📌 1. Environment & Prasyarat

Server modul AI ini berjalan menggunakan **Python** pada lokasi Conda Environment khusus:
- **Lokasi Conda Env**: `D:\conda_envs\maguru` (atau nama env `maguru`)

---

## ⚙️ 2. Langkah-Langkah Jalankan Server

### Langkah A: Buka Terminal & Aktifkan Conda Environment
Jalankan perintah berikut di PowerShell atau Command Prompt:

```powershell
# 💡 Tips PowerShell jika muncul "CondaError: Run conda init":
(& "C:\ProgramData\Anaconda3\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression

# Aktifkan environment
conda activate D:\conda_envs\maguru
```

> **Alternatif Tanpa `conda activate` (Paling Cepat):**  
> Anda bisa langsung memanggil python env tanpa aktivasi:
> ```powershell
> & "D:\conda_envs\maguru\python.exe" server.py
> ```

### Langkah B: Masuk ke Folder Modul AI
```powershell
cd D:\.maguru\maguru-model
```

### Langkah C: Pastikan File `.env` Sudah Terkonfigurasi
Pastikan file `.env` berisi konfigurasi kunci API OpenRouter & database Supabase:

```env
PROJECT_NAME="Maguru AI Model Backend"
VERSION="1.0.0"
PORT=8000
HOST="0.0.0.0"

OPENROUTER_API_KEY="sk-or-v1-..."
OPENROUTER_MODEL="google/gemma-7b-it:free"

DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres"
```

### Langkah D: Jalankan Server FastAPI
Jalankan salah satu dari perintah di bawah ini:

```powershell
# Cara 1: Menggunakan launcher script server.py
python server.py

# Cara 2: Menggunakan uvicorn dengan fitur auto-reload
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Server akan aktif pada: **`http://localhost:8000`**

---

## 🧪 3. Cara Pengujian API (API Testing)

### Opsi 1: Menggunakan LangServe Playground (Interaktif Web)
- Chatbot Co-Teacher: **`http://localhost:8000/chatbot/playground/`**
- Explain Code: **`http://localhost:8000/explain-code/playground/`**

### Opsi 2: Menggunakan Swagger UI Interaktif (Browser)
- Buka **`http://localhost:8000/docs`** di browser Anda.
- Pilih endpoint yang ingin diuji (misal `POST /api/v1/generate-quiz` atau `POST /api/v1/chat/stream`).
- Klik **Try it out**, isi JSON body, lalu klik **Execute**.

### Opsi 3: Menggunakan Postman Collection
Telah disediakan file Postman Collection resmi di lokasi:
`D:\.maguru\maguru-model\postman\maguru_ai_postman_collection.json`

---

## ⚡ 4. Menjalankan Unit Test (Pytest)

Untuk menguji seluruh fungsi AI Backend secara otomatis tanpa memotong kuota API Key (menggunakan Mock):

```powershell
& "D:\conda_envs\maguru\python.exe" -m pytest tests/ -v
```

---

## 🛠️ Troubleshooting Singkat

| Error / Masalah | Penyebab | Solusi Cepat |
|---|---|---|
| `CondaError: Run conda init before conda activate` | Hook PowerShell belum dimuat | Jalankan: `(& "C:\ProgramData\Anaconda3\Scripts\conda.exe" "shell.powershell" "hook") \| Out-String \| Invoke-Expression` |
| `ModuleNotFoundError: No module named 'langchain_community'` | Menjalankan `uvicorn` global bawaan Anaconda base | Gunakan `python -m uvicorn app.main:app --reload` atau panggil `& "D:\conda_envs\maguru\python.exe" server.py` |
| `Address already in use` | Port 8000 sedang dipakai proses lain | Tutup proses lain atau ubah port di `.env` |
| `500 Internal Server Error` | `OPENROUTER_API_KEY` tidak valid atau terputus | Periksa kunci API di file `.env` |
