# AI Chains - Maguru Learning Platform

## Overview

Chain adalah modul AI yang masing-masing memiliki fungsi spesifik untuk membantu proses belajar siswa. Setiap chain menerima input tertentu dan memberikan output yang dirancang untuk kebutuhan pembelajaran.

| Chain | Fungsi Utama | Kapan Dipakai |
|-------|--------------|----------------|
| **explain_code** | Menjelaskan kode Python baris per baris | Saat siswa bingung memahami contoh kode |
| **qa_chatbot** | Menjawab pertanyaan dengan konteks dan riwayat | Saat siswa bertanya selama belajar |
| **hint_generator** | Memberikan bantuan bertahap 3 level | Saat siswa stuck pada tugas coding |
| **quiz_feedback** | Memberikan umpan balik hasil kuis | Setelah siswa menjawab soal kuis |
| **ai_greeting** | Menyapa siswa secara personal | Saat siswa membuka halaman Home |

---

## Perbandingan Chain

| Aspek | explain_code | qa_chatbot | hint_generator | quiz_feedback | ai_greeting |
|--------|-------------|-------------|----------------|----------------|-------------|
| **Tujuan** | Jelaskan kode | Jawab tanya | Beri hint | Umpan balik | Sapaan |
| **Input Utama** | Snippet kode | Pertanyaan + konteks | Tugas + level | Jawaban + status | Nama + kursus |
| **Output** | Penjelasan lengkap | Jawaban dengan referensi | Hint sesuai level | Feedback semangat/penjelasan | Sapaan ramah |
| **Kapan Dipakai** | Bingung dengan kode | Diskusi interaktif | Stuck pada tugas | Setelah kuis | Mulai belajar |

---

## Skenario Penggunaan

### Cerita: Perjalanan Belajar Budi

**1. Memulai Hari Belajar**
> Budi membuka aplikasi Maguru. Di halaman Home, dia disapa: *"Halo Budi! Selamat datang di kelas Python Dasar. Hari ini kita akan belajar tentang variabel dan tipe data. Mari kita mulai petualangan ini dengan semangat!"*
>
> **Chain yang dipakai:** `ai_greeting`

**2. Belajar Materi Baru**
> Budi membuka materi tentang variabel. Dia melihat contoh kode:
> ```python
> nama = "Budi"
> umur = 17
> ```
>
> Budi bingung, apa itu `=` dan kenapa pakai tanda kutip? Dia klik tombol "Jelaskan Kode".
>
> **Chain yang dipakai:** `explain_code`
>
> AI menjelaskan: *"Kode ini membuat dua variabel. Pertama, variabel `nama` berisi teks 'Budi'. Tanda kutip digunakan untuk teks. Kedua, variabel `umur` berisi angka 17 tanpa tanda kutip karena ini angka, bukan teks."*

**3. Mencoba Tugas Praktik**
> Budi diberi tugas: "Buat variabel `kota` dengan nama kotamu."
>
> Dia mencoba: `kota = Jakarta`
>
> Tapi jawabannya salah. Budi stuck dan tidak tahu kesalahannya. Dia meminta hint.
>
> **Hint Level 1:** "Perhatikan bagaimana contoh kode sebelumnya menulis teks..."
>
> Masih bingung, Budi minta hint lagi.
>
> **Hint Level 2:** "Ingat, tipe data teks (string) perlu ditulis dengan tanda kutip."
>
> Ah sekarang mengerti! Budi memperbaiki: `kota = "Jakarta"`
>
> **Chain yang dipakai:** `hint_generator`

**4. Bertanya ke AI Tutor**
> Budi penasaran: "Kenapa sih harus pakai tanda kutip? Kan ribet?"
>
> AI menjawab: "Tanda kutip membedakan teks dari nama variabel. Tanpa tanda kutip, Python mengira `Jakarta` adalah nama variabel lain, bukan teks. Ini juga membantu mencegah kebingungan."
>
> **Chain yang dipakai:** `qa_chatbot`

**5. Mengerjakan Kuis**
> Setelah belajar, Budi mengerjakan kuis.
>
> Soal: "Apa output dari `print(type(17))`?"
> Jawaban Budi: "integer"
> Status: Benar!
>
> AI memberikan umpan balik: "Benar! Bagus sekali! Tipe data integer memang digunakan untuk angka bulat seperti 17."
>
> **Chain yang dipakai:** `quiz_feedback`

---

## Detail Setiap Chain

### 1. Explain Code

**Ringkasan:** Tutor AI yang menjelaskan kode Python baris per baris dalam Bahasa Indonesia.

**Fungsi:**
Chain ini membantu siswa memahami contoh kode dengan memberikan penjelasan yang mudah dipahami. Penjelasan mencakup apa yang dilakukan kode, mengapa ditulis seperti itu, dan kesalahan umum yang perlu dihindari.

**Cara Kerja:**
1. Menerima snippet kode Python dari siswa
2. Mengirim kode ke LLM dengan prompt khusus untuk penjelasan
3. LLM menganalisis dan menjelaskan dalam Bahasa Indonesia
4. Hasil penjelasan dikirim kembali ke siswa

**Input:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `code_snippet` | str | Kode Python yang akan dijelaskan |

**Output:**
Penjelasan lengkap dalam Bahasa Indonesia yang mencakup:
- Apa yang dilakukan setiap baris
- Mengapa kode ditulis seperti itu
- Kesalahan umum yang sering terjadi

**Contoh Penggunaan:**
```python
from ai_chains.chains import explain_code

code = """
nama = "Budi"
umur = 17
print(nama)
"""

penjelasan = explain_code.explain_code(code)
# Output: "Kode ini membuat variabel nama dengan nilai 'Budi'..."
```

**Catatan:**
- Menggunakan lazy initialization (chain dibuat hanya saat pertama dipakai)
- Memiliki fallback LLM (OpenRouter → Z.AI) untuk memastikan selalu tersedia

---

### 2. Q&A Chatbot

**Ringkasan:** Menjawab pertanyaan siswa dengan memperhatikan konteks sesi dan riwayat percakapan.

**Fungsi:**
Chain ini memungkinkan siswa berdiskusi interaktif dengan AI selama proses belajar. AI memahami konteks materi yang sedang dipelajari dan mengingat percakapan sebelumnya untuk memberikan jawaban yang relevan.

**Cara Kerja:**
1. Menerima pertanyaan beserta konteks sesi dan riwayat chat
2. Memformat riwayat percakapan untuk prompt (maksimal 5 pesan terakhir)
3. Membatasi konten materi hingga 1000 karakter
4. Mengirim ke LLM dengan prompt yang sudah diformat
5. Mengembalikan jawaban dalam Bahasa Indonesia

**Input:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `question` | str | Pertanyaan dari siswa |
| `session_title` | str | Judul sesi/materi yang sedang dipelajari |
| `session_content` | str | Konten materi (dibatasi 1000 karakter) |
| `chat_history` | list | Riwayat percakapan (maksimal 5 pesan terakhir) |

**Output:**
Jawaban dalam Bahasa Indonesia yang memperhatikan konteks materi dan riwayat percakapan sebelumnya.

**Contoh Penggunaan:**
```python
from ai_chains.chains import qa_chatbot

question = "Apa itu variabel?"
session_title = "Python Dasar - Variabel"
session_content = "Variabel adalah tempat menyimpan data..."
chat_history = [
    {"role": "student", "content": "Halo"},
    {"role": "ai", "content": "Halo! Ada yang bisa dibantu?"}
]

jawaban = qa_chatbot.answer_question(
    question, session_title, session_content, chat_history
)
# Output: "Variabel adalah kotak penyimpanan untuk data..."
```

**Catatan:**
- Riwayat chat diformat sebagai "Siswa: ..." dan "AI: ..."
- Jika terjadi error, chain akan mengembalikan pesan error yang ramah

---

### 3. Hint Generator

**Ringkasan:** Sistem bantuan bertahap dengan 3 level kejelasan, dari halus hingga langsung.

**Fungsi:**
Chain ini membantu siswa yang stuck pada tugas coding tanpa langsung memberikan jawaban. Sistem hint bertahap membuat siswa tetap berpikir kritis sambil mendapatkan bantuan yang cukup.

**Cara Kerja:**
1. Menerima deskripsi tugas dan percobaan siswa
2. Menentukan level hint (1-3)
3. Mengirim informasi ke LLM dengan instruksi level-specific
4. LLM menghasilkan hint sesuai level yang diminta

**Input:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `task` | str | Deskripsi tugas yang dikerjakan siswa |
| `student_attempt` | str | Kode atau jawaban yang sudah dicoba siswa |
| `level` | int | Level hint: 1 (Halus), 2 (Konseptual), 3 (Langsung) |

**Level Hint:**
| Level | Nama | Karakteristik | Contoh |
|-------|------|---------------|--------|
| 1 | Halus | Arahkan tanpa memberi jawaban | "Coba perhatikan bagian yang mengelola teks..." |
| 2 | Konseptual | Jelaskan konsep dengan contoh serupa | "Ingat, tipe data teks (string) perlu tanda kutip. Perhatikan contoh di materi." |
| 3 | Langsung | Tunjukkan pendekatan solusi | "Tambahkan tanda kutip di sekitar 'Jakarta'" |

**Output:**
Hint dalam Bahasa Indonesia sesuai dengan level yang diminta.

**Contoh Penggunaan:**
```python
from ai_chains.chains import hint_generator

task = "Buat variabel kota dengan nama kotamu"
attempt = "kota = Jakarta"

# Hint level 1 - paling halus
hint1 = hint_generator.generate_hint(task, attempt, 1)
# Output: "Coba perhatikan bagaimana contoh kode menulis teks..."

# Hint level 2 - konseptual
hint2 = hint_generator.generate_hint(task, attempt, 2)
# Output: "Ingat perbedaan antara teks dan nama variabel..."

# Hint level 3 - langsung
hint3 = hint_generator.generate_hint(task, attempt, 3)
# Output: "Tambahkan tanda kutip: kota = \"Jakarta\""

# Atau ambil semua hint sekaligus
all_hints = hint_generator.get_all_hints(task, attempt)
# Returns: [hint1, hint2, hint3]
```

**Catatan:**
- Fungsi `get_all_hints()` menghasilkan semua 3 level sekaligus
- Level dipetakan ke nama dalam Bahasa Indonesia untuk prompt

---

### 4. Quiz Feedback

**Ringkasan:** Memberikan umpan balik yang sesuai setelah siswa menjawab soal kuis.

**Fungsi:**
Chain ini membuat pengalaman kuis lebih interaktif dengan memberikan umpan balik yang:
- Menyemangati jika jawaban benar
- Menjelaskan jika jawaban salah

**Cara Kerja:**
1. Menerima soal, jawaban siswa, kunci jawaban, dan status benar/salah
2. Mengubah status boolean menjadi teks ("Benar" atau "Salah")
3. Mengirim ke LLM dengan prompt feedback
4. LLM menghasilkan umpan balik yang sesuai

**Input:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `question` | str | Soal kuis |
| `student_answer` | str | Jawaban dari siswa |
| `correct_answer` | str | Kunci jawaban yang benar |
| `is_correct` | bool | True jika benar, False jika salah |

**Output:**
Umpan balik dalam Bahasa Indonesia:
- Jika benar: Pujian semangat dengan penjelasan singkat
- Jika salah: Penjelasan mengapa salah dan jawaban yang benar

**Contoh Penggunaan:**
```python
from ai_chains.chains import quiz_feedback

question = "Apa tipe data dari 17?"
student_answer = "string"
correct_answer = "integer"
is_correct = False

feedback = quiz_feedback.generate_feedback(
    question, student_answer, correct_answer, is_correct
)
# Output: "Kurang tepat. Angka 17 adalah tipe data integer (bulat), bukan string..."
```

**Catatan:**
- Jika LLM gagal, chain akan menggunakan fallback yang sederhana
- Fallback benar: "Benar! Bagus sekali!"
- Fallback salah: "Salah. Jawaban yang benar adalah: {kunci}"

---

### 5. AI Greeting

**Ringkasan:** Menyapa siswa secara personal saat memulai sesi belajar.

**Fungsi:**
Chain ini menciptakan pengalaman pembelajaran yang lebih personal dengan sapaan yang menyebut nama siswa dan informasi kursus yang diikuti.

**Cara Kerja:**
1. Menerima nama siswa dan metadata kursus
2. Mengformat learning objectives untuk prompt
3. Mengirim ke LLM dengan prompt greeting
4. Jika hasil terlalu pendek atau terlalu generik, gunakan fallback
5. Fallback menghasilkan variasi sapaan acak

**Input:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `student_name` | str | Nama siswa |
| `course_metadata` | dict | Informasi kursus dengan keys: `title` dan `learning_objectives` |

**Output:**
Sapaan personal dalam Bahasa Indonesia yang:
- Menyebut nama siswa
- Menyebut judul kursus
- Menyebut tujuan pembelajaran (jika ada)
- Bervariasi setiap kali dipanggil

**Contoh Penggunaan:**
```python
from ai_chains.chains import ai_greeting

student_name = "Budi"
course_metadata = {
    "title": "Python Dasar",
    "learning_objectives": [
        "Memahami variabel",
        "Menggunakan tipe data dasar",
        "Membuat program sederhana"
    ]
}

greeting = ai_greeting.generate_greeting(student_name, course_metadata)
# Output: "Halo Budi! Selamat datang di kelas Python Dasar. Hari ini kita akan mempelajari variabel, tipe data dasar, dan bagaimana membuat program sederhana. Mari kita mulai petualangan ini dengan semangat!"
```

**Catatan:**
- Sistem fallback memastikan sapaan selalu tersedia meskipun LLM gagal
- Fallback memiliki variasi acak untuk menghindari kebosanan
- Learning objectives dibatasi maksimal 3 untuk prompt

---

## Catatan Teknis (Untuk Developer)

### Shared LLM Instance
Semua chain menggunakan fungsi `get_llm()` dari `__init__.py` yang memiliki:
- **Fallback system**: OpenRouter (primary) → Z.AI (fallback)
- **Lazy initialization**: LLM hanya dibuat saat pertama dipakai
- **Connection testing**: OpenRouter diuji sebelum digunakan

### Error Handling
Setiap chain memiliki try-except block dengan fallback yang ramah untuk user. Ini memastikan aplikasi tetap berjalan meskipun ada masalah dengan LLM.

### Prompt Templates
Prompt templates disimpan di `ai_chains/prompts/` dalam format YAML:
- `explain_code.yaml`
- `qa_chatbot.yaml`
- `hint_generator.yaml`
- `quiz_feedback.yaml`
- `ai_greeting.yaml`

### Future Improvements
- [ ] Ekstraksi learning objectives dari materi secara otomatis
- [ ] Personalisasi hint berdasarkan sejarah kesalahan siswa
- [ ] Multi-language support untuk chain输出
