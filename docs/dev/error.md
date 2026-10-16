# 📝 Klarifikasi Teknis Kebutuhan Sistem & Ruang Lingkup Evaluasi
**Dokumen Penyelarasan Bab III Penelitian R&D — Platform Pembelajaran MAGURU**  
*Tanggapan Resmi Tim Teknis atas Permintaan Klarifikasi CTO*  
**Status Dokumen:** Final Draft (Disusun Berdasarkan Repositori Aktif)  
**Target:** Penetapan Kebutuhan Fungsional & Batasan Evaluasi Skripsi  

---

## 1. 📌 Cakupan Fitur dan Status Implementasi

### 1.1. Fitur dan Alur yang Sudah Dapat Diuji End-to-End (E2E)
Seluruh alur utama berikut telah terhubung penuh antara Frontend (`maguru`) dan Backend AI (`maguru-model`) serta dapat diuji langsung melalui antarmuka web:

1. **Alur Belajar Siswa (*Student Learning Journey*):**
   - **Autentikasi & Masuk Kelas:** Siswa mendaftar/login, membuka katalog, dan masuk ke ruang kelas (`/course/[slug]/learn`).
   - **Initial Assessment (Pre-Test Wajib):** Sebelum materi terbuka, siswa wajib menyelesaikan tes diagnostik. Skor dihitung per topik.
   - **Adaptive Placement (Skip Materi Otomatis):** Jika skor topik mencapai ambang batas (≥ 70%), bab/materi terkait otomatis ditandai selesai (`completed`), dan silabus langsung menyesuaikan.
   - **Socratic Co-Teacher Chat:** Siswa bertanya pada AI Tutor di ruang belajar dengan respons *streaming* (SSE) yang memandu secara sokratik tanpa memberikan jawaban langsung (*anti-spoiler*).
   - **Pedagogical Code Explainer:** Siswa menyorot/memilih potongan kode untuk dibedah alur logika baris-per-baris dan analogi model mentalnya.
   - **Progressive Hint Scaffolding:** Siswa meminta petunjuk bertingkat (Hint 1: Konsep ➔ Hint 2: Logika ➔ Hint 3: Sintaks).
   - **Section Quiz & Progression Unlock:** Siswa mengerjakan kuis di akhir bab; skor ≥ 70% membuka bab materi berikutnya.

2. **Alur Pengajar / Pembuat Kursus (*Course Creator Journey*):**
   - **Penyusunan Kurikulum & Materi:** Pengajar membuat bab dan materi menggunakan editor TipTap.
   - **AI Quiz Generator & Manual Curation (HITL):** Pengajar meminta AI merancang draf soal kuis (`POST /api/v1/generate-quiz`), mereview/mengedit/menghapus soal di modal browser, lalu menyimpannya ke database kursus.
   - **One-Click Knowledge Base Sync:** Pengajar menekan tombol sinkronisasi materi untuk mengekstrak teks silabus ke dalam database vektor PostgreSQL `pgvector` (`POST /api/v1/ingest`).

---

### 1.2. Status Implementasi Initial Assessment & Rekomendasi Berbasis Aturan
* **Status Implementasi:** **100% SELESAI (IMPLEMENTED & AKTIF).**
* **Lokasi Kode Aktual:**
  - Frontend Logic: [`features/assessment-engine/`](file:///d:/.maguru/maguru/features/assessment-engine/)
  - Engine Penilaian: [`scoring.service.ts`](file:///d:/.maguru/maguru/features/assessment-engine/services/scoring.service.ts)
  - Engine Penempatan: [`placement.service.ts`](file:///d:/.maguru/maguru/features/assessment-engine/services/placement.service.ts)
  - API Submission: [`app/api/assessment/submit/route.ts`](file:///d:/.maguru/maguru/app/api/assessment/submit/route.ts)
* **Mekanisme Aturan (Rule-Based Algorithm):**
  - Menggunakan aturan deterministik berbasis ambang batas (`PLACEMENT_THRESHOLD = 70%`).
  - Sistem menghitung persentase kebenaran per topik materi secara terisolasi.
  - Jika `score(topik) >= 70%`, transaksi basis data otomatis membuat entri `lesson_progress` dengan status `completed = true` untuk materi terkait, sehingga siswa tidak perlu mempelajari ulang materi yang sudah dikuasainya.
  - *Catatan:* Keputusan menjalankan logika penempatan ini di server Next.js (bukan di LLM) adalah tepat karena bersifat deterministik, bebas halusinasi, dan dapat dipertanggungjawabkan dalam pengujian skripsi.

---

### 1.3. Status Fitur dalam Pengembangan vs Ruang Lingkup Skripsi
* **Rekomendasi Keputusan:** **DIKELUARKAN DARI RUANG LINGKUP EVALUASI SKRIPSI.**
* **Rasional:**
  Fitur-fitur tambahan seperti *server-side stateful LangGraph `interrupt()`*, *dashboard observabilitas LangSmith*, dan *audio Socratic* adalah optimasi teknis tingkat lanjut (*engineering enhancements*), bukan variabel pokok penelitian R&D. Seluruh alur inti yang dijanjikan pada metodologi pengembangan sudah lengkap dan berjalan.

---

### 1.4. Matriks Pemisahan Status Implementasi vs Status Pengujian

| Fitur / Modul | Status Implementasi | Status Pengujian Fungsional | Masuk Ruang Lingkup Skripsi? |
| :--- | :---: | :---: | :---: |
| **Initial Assessment (Pre-Test)** | 🟢 Selesai (100%) | 🟢 Lulus (Unit Test & E2E) | **YA (Wajib)** |
| **Rule-Based Placement Engine** | 🟢 Selesai (100%) | 🟢 Lulus (`scoring.service.test.ts`) | **YA (Wajib)** |
| **Socratic Co-Teacher Agent** | 🟢 Selesai (100%) | 🟢 Lulus (`tests/test_unit_chat.py`) | **YA (Wajib)** |
| **Progressive Hint Scaffolding** | 🟢 Selesai (100%) | 🟢 Lulus (`tests/test_unit_hint.py`) | **YA (Wajib)** |
| **Code Explainer Agent** | 🟢 Selesai (100%) | 🟢 Lulus (`tests/test_unit_explain.py`) | **YA (Wajib)** |
| **Quiz Generator & Client HITL** | 🟢 Selesai (100%) | 🟢 Lulus (`tests/test_unit_quiz.py`) | **YA (Wajib)** |
| **Course Ingest & pgvector RAG** | 🟢 Selesai (100%) | 🟢 Lulus (`tests/test_unit_ingest.py`) | **YA (Wajib)** |
| **PostgreSQL Multi-Turn Checkpoint**| 🟢 Selesai (100%) | 🟢 Lulus (`test_integration_checkpointer.py`)| **YA (Wajib)** |
| *Server-Side LangGraph `interrupt()`* | 🟡 Parsial | ⚪ Belum diuji E2E | ❌ **Dikeluarkan (Batasan Masalah)** |
| *LangSmith Observability Dashboard* | ⚪ Backlog | ⚪ N/A | ❌ **Dikeluarkan (Batasan Masalah)** |
| *Realtime Collaborative Editor* | ⚪ Backlog | ⚪ N/A | ❌ **Dikeluarkan (Batasan Masalah)** |

---

## 2. 📋 Persyaratan Fungsional sebagai Dasar Pengujian

### 2.1. Kesesuaian Spesifikasi dengan Implementasi Aktual
Spesifikasi kontrak Masukan-Keluaran (I/O) dan *Acceptance Criteria* yang tercantum pada memorandum **100% sesuai dengan implementasi aktif**. Seluruh schema Pydantic di backend AI ([`app/schemas/`](file:///d:/.maguru/maguru-model/app/schemas/)) dan schema Zod di frontend ([`features/assessment-engine/schemas/`](file:///d:/.maguru/maguru/features/assessment-engine/schemas/)) telah beroperasi sesuai definisi kontrak tersebut.

---

### 2.2. Daftar Persyaratan Fungsional Formal (Untuk BAB III Skripsi)

| ID | Nama Kebutuhan Fungsional | Deskripsi Perilaku Masukan - Keluaran | Kondisi Keberhasilan (*Acceptance Criteria*) |
| :---: | :--- | :--- | :--- |
| **FR-01** | **Tes Diagnostik Awal (*Pre-Test*)** | Input: Pilihan jawaban siswa terhadap butir soal diagnostik kursus.<br>Output: Data penilaian tersimpan dan ringkasan skor per topik. | Seluruh soal pre-test terjawab; siswa tidak dapat masuk ke materi sebelum pre-test diselesaikan. |
| **FR-02** | **Penempatan Materi Berbasis Aturan** | Input: Skor per topik (`topicScores`).<br>Output: Daftar materi yang dilewati (`skippedLessonIds`) dan status bab terbuka. | Topik dengan skor ≥ 70% otomatis ditandai `completed`; bab terkait terbuka tanpa harus membaca manual. |
| **FR-03** | **Bimbingan Sokrates AI (*Co-Teacher*)** | Input: Pertanyaan teks siswa + identitas sesi chat (`thread_id`).<br>Output: Aliran teks (SSE stream) respons reflektif sokrates. | AI tidak memberikan kode solusi instan pada 2 turn pertama; AI memandu siswa menemukan konsep mandiri. |
| **FR-04** | **Ketahanan Memori Percakapan** | Input: Input pertanyaan lanjutan pada `thread_id` yang sama.<br>Output: Respons AI yang mengacu pada percakapan sebelumnya. | Riwayat percakapan tidak hilang meski server di-restart (durable di Supabase PostgreSQL). |
| **FR-05** | **Petunjuk Bertingkat (*Progressive Hints*)** | Input: Kode siswa, tugas, dan nomor tingkat petunjuk (1, 2, atau 3).<br>Output: Petunjuk terstruktur sesuai tingkatan. | Tingkat 1: Konsep murni (0 kode); Tingkat 2: Alur logika; Tingkat 3: Panduan sintaks spesifik tanpa membocorkan jawaban penuh. |
| **FR-06** | **Pembongkaran Kode (*Code Explainer*)** | Input: Potongan kode sumber siswa.<br>Output: Penjelasan 4 bagian: Tujuan, Alur per Baris, Analogi Mental, dan Jebakan Umum. | Output memuat 4 sub-bagian lengkap tanpa ada halusinasi sintaks yang tidak ada pada kode input. |
| **FR-07** | **Penyusunan Kuis & Kurasi Pengajar (HITL)** | Input: Parameter bab materi/kursus + jumlah soal yang diinginkan pengajar.<br>Output: Draf array JSON butir kuis + opsi edit/simpan pengajar. | Draf kuis tampil di form edit; butir soal baru tersimpan ke database kurikulum jika tombol 'Simpan' ditekan pengajar. |
| **FR-08** | **Sinkronisasi Pengetahuan Kursus (RAG)** | Input: Konten teks materi bab kursus.<br>Output: Vektorisasi dokumen ke tabel `course_knowledge_chunks`. | Dokumen berhasil dipecah menjadi chunks dan similarity search mengembalikan materi relevan untuk Co-Teacher. |

---

### 2.3. Bagian yang Perlu Ditetapkan Sebelum Penyusunan *Test Case*
Hanya ada **2 parameter ambang batas kuantitatif** yang perlu disepakati:
1. **Batas Toleransi Latensi Respons AI:** Maksimal Time-to-First-Token (TTFT) aliran SSE < 3.0 detik pada koneksi internet standar kampus/laboratorium.
2. **Kriteria Kelulusan Kuis Bab (*Section Quiz*):** Ditetapkan konsisten pada nilai 70 (sesuai standar KKM/Threshold kurikulum pemrograman).

---

## 3. 👥 Ruang Lingkup Evaluasi Kualitas Respons AI

### 3.1. Konsistensi Eksekusi Skenario Uji & Penyimpanan Keluaran
* **Kesiapan Sistem:** **SUDAH SIAP.**
* **Mekanisme Teknis:**
  - Backend `maguru-model` dapat dijalankan dengan parameter deterministik (`temperature: 0.0` atau `0.2`) untuk pengujian baku.
  - Seluruh respons dari skenario uji dapat dicatat otomatis (*logged*) ke dalam format JSONL atau spreadsheet penilaian yang memuat: *ID Kasus, Input Siswa, Output AI, Waktu Respons, dan Kolom Skor Evaluator*.

---

### 3.2. Jumlah Skenario Uji Baku (50 Skenario: Kebutuhan vs Rekomendasi)
* **Status:** Usulan 50 skenario merupakan **REKOMENDASI AWAL TEKNIS**, bukan syarat mutlak.
* **Penyesuaian untuk Skripsi R&D:**
  - Evaluasi skripsi dilakukan oleh evaluator manusia (Dosen / Pakar). Menguji 50 skenario per agen akan menghasilkan beban evaluasi yang terlalu besar bagi dosen penguji.
  - **Rekomendasi Skripsi:** Cukup gunakan **20 hingga 25 Skenario Uji Representatif** (5 kasus per agen/kompetensi: Error Sintaks, Logika Looping, Rekursi, Konsep OOP, dan Uji Anti-Spoiler). Jumlah ini sudah sangat memenuhi kaidah validitas pengujian ahli (*Expert Judgment*) dalam penelitian R&D S1.

---

### 3.3. Urgensi Evaluator AI (*LLM-as-a-Judge*) dalam Skripsi
* **Keputusan:** **DITUNDA (TIDAK WAJIB UNTUK SKRIPSI).**
* **Rasional Ilmiah:**
  - Dalam sidang skripsi akademik, **penilaian oleh Dosen Ahli / Expert Judgment (Pakar Materi Pemrograman & Pakar Media Pembelajaran)** adalah data primer dengan bobot keabsahan tertinggi.
  - Pendekatan *LLM-as-a-Judge* membutuhkan validasi tambahan (apakah LLM penilai bebas bias) yang justru dapat memicu perdebatan metodologis baru dengan dosen pembimbing/penguji.
  - *LLM-as-a-Judge* cukup dicantumkan di Bab V sebagai *Saran Penelitian Lanjutan*.

---

## 4. 🎯 Batas Penggunaan RAG dan Komponen Tambahan

### 4.1. Cakupan Mekanisme RAG dalam Evaluasi
* **Ketetapan:** **RAG pada Co-Teacher adalah SATU-SATUNYA mekanisme RAG yang dievaluasi dalam skripsi.**
* **Tujuan Evaluasi:** Membuktikan bahwa tutor AI menjawab berdasarkan silabus kursus yang diunggah di Maguru (*curriculum-grounded*), bukan berhalusinasi atau mengambil materi di luar materi ajar.

---

### 4.2. Status Mode RAG pada Quiz Engine
* **Ketetapan:** **HANYA KEMAMPUAN TEKNIS OPSIONAL (TIDAK MASUK EVALUASI SKRIPSI).**
* **Rasional:**
  - Alur utama Quiz Engine yang digunakan pengajar di aplikasi nyata adalah **Direct Lesson Ingestion** (membuat soal langsung dari teks materi yang sedang dibuka/diedit pengajar).
  - Mode Direct Lesson ini jauh lebih presisi dan deterministik untuk kebutuhan evaluasi skripsi. Mode RAG pada Quiz Engine cukup menjadi *fallback feature* tanpa perlu dibebankan ke instrumen pengujian skripsi.

---

### 4.3. Fitur yang Wajib Dikeluarkan dari Ruang Lingkup Skripsi (Batasan Masalah)
Demi menjamin penelitian selesai tepat waktu dan terfokus pada kualitas pembelajaran, komponen-komponen berikut **secara resmi dikeluarkan dari ruang lingkup evaluasi skripsi**:
1. ❌ **Server-Side Stateful LangGraph `interrupt()`**: Evaluasi Human-in-the-Loop difokuskan pada kurasi pengajar di sisi web browser (*Client-Side Review* di `QuizEditorPanel.tsx`) yang sudah terbukti berjalan.
2. ❌ **Observability Platform Pihak Ketiga (LangSmith / OpenTelemetry Dashboard)**: Cukup gunakan logging performa standar bawaan FastAPI/Uvicorn.
3. ❌ **Automated LLM-as-a-Judge Pipeline**: Evaluasi kualitas pedagogis sepenuhnya diserahkan kepada instrumen kuesioner ahli manusia (Dosen).
4. ❌ **Multiplayer / Realtime Collaborative Code Editor**: Dinyatakan sebagai rencana pengembangan versi rilis berikutnya.

---

## 📌 Ringkasan Eksekutif untuk BAB III Skripsi

> **Pernyataan Ruang Lingkup Resmi:**  
> *"Penelitian pengembangan ini berfokus pada pengujian efektivitas sistem pembelajaran adaptif yang mencakup: (1) Asesmen diagnostik awal (Pre-Test) dengan algoritma penempatan materi berbasis aturan (Rule-Based Threshold), (2) Bimbingan belajar cerdas berpendekatan Sokrates (Co-Teacher) dengan memori percakapan persisten dan RAG berbasis silabus, (3) Asistensi pemrograman bertingkat (Progressive Hints & Code Explainer), serta (4) Pembuatan dan kurasi soal kuis oleh pengajar (Human-in-the-Loop di antarmuka CMS). Pengujian kualitas respons AI dilakukan melalui pengujian ahli (Expert Judgment) menggunakan 20–25 skenario uji terstandarisasi."*
