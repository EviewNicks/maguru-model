# Panduan Testing API Maguru

## 🎯 Tujuan
Dokumen ini membantu melakukan testing API LangServe untuk memverifikasi bahwa backend berkerja dengan benar sebelum melakukan integrasi dengan frontend.

---

## 📁 File yang Dibuat

1. **`maguru-api.postman_collection.json`** - Koleksi Postman untuk testing
2. **`README.md`** - Dokumentasi lengkap dalam Bahasa Inggris
3. **`test_api.sh`** - Script bash untuk testing cepat dengan curl

---

## 🚀 Cara Testing

### Opsi 1: Postman (Disarankan)

1. **Jalankan server:**
   ```bash
   cd D:\.maguru\maguru-model
   python server.py
   ```

2. **Import ke Postman:**
   - Buka Postman
   - Klik **Import**
   - Pilih file `maguru-api.postman_collection.json`

3. **Test endpoint:**
   - Mulai dengan **Health Check**
   - Lanjut ke endpoint lain

### Opsi 2: Script Bash

```bash
cd D:\.maguru\maguru-model\api_test
bash test_api.sh
```

---

## ⚠️ Format Request yang Benar

**Semua request POST HARUS dibungkus dalam `input`:**

✅ **BENAR:**
```json
{
  "input": {
    "question": "Apa itu Python?",
    "session_title": "Python Basics",
    "session_content": "...",
    "chat_history": []
  }
}
```

❌ **SALAH:**
```json
{
  "question": "Apa itu Python?",
  "session_title": "Python Basics"
}
```

---

## 📊 Endpoint untuk Dites

| # | Endpoint | Method | Deskripsi |
|---|----------|--------|-----------|
| 1 | `/health` | GET | Cek status server |
| 2 | `/chatbot/invoke` | POST | Chatbot biasa |
| 3 | `/chatbot/stream` | POST | Chatbot dengan streaming |
| 4 | `/explain-code/stream` | POST | Penjelasan kode |
| 5 | `/hint/stream` | POST | Generator hint |
| 6 | `/quiz-feedback/stream` | POST | Feedback kuis |
| 7 | `/greeting/stream` | POST | Sapaan personal |

---

## 🔍 Cara Menganalisis Hasil

### Jika Sukses (200 OK)
```
✅ Status: 200 OK
✅ Response mengandung "output" atau stream data
✅ Server berkerja dengan benar
```

### Jika Gagal (422 Unprocessable Entity)
```
❌ Error: 422
❌ Kemungkinan: Format request salah
❌ Cek apakah ada key "input" di body
```

### Jika Gagal (Connection Refused)
```
❌ Error: Connection refused
❌ Kemungkinan: Server tidak berjalan
❌ Jalankan: python server.py
```

---

## 📝 Checklist Testing

- [ ] Server berjalan (`python server.py`)
- [ ] Health check sukses (`/health`)
- [ ] Chatbot invoke berkerja
- [ ] Chatbot stream menghasilkan SSE
- [ ] Explain code berkerja
- [ ] Hint generator berkerja
- [ ] Quiz feedback berkerja
- [ ] Greeting berkerja

---

## 🔄 Langkah Berikutnya

Setelah API berkerja dengan benar di Postman:

1. **Perbaiki frontend** - Update `api.ts` untuk membungkus request dalam `{"input": ...}`
2. **Perbaiki types** - Update `types/index.ts` agar sesuai dengan field backend
3. **Integrasi** - Test frontend dengan backend yang sudah berkerja

---

## ❓ Pertanyaan Umum

**Q: Apakah perlu mengubah backend?**
A: Tidak, backend sudah benar. Yang perlu diperbaiki adalah frontend.

**Q: Kenapa harus dibungkus dalam `input`?**
A: Itu format standar LangServe. Dokumentasi LangServe menyatakan semua request ke `/stream` endpoint harus mengandung key `input`.

**Q: Apakah bisa tanpa Postman?**
A: Ya, bisa pakai `test_api.sh` atau curl langsung. Postman hanya memudahkan visualisasi.

---

**Dibuat:** 2025-03-06
**Versi:** 1.0
