# 🗺️ Roadmap & Desain Inovasi Masa Depan: AI Quiz Generator Engine

Dokumen ini mencatat visi arsitektur dan rencana inovasi jangka panjang (**Should-Have** & **Could-Have**) untuk fitur **Automated AI Quiz Generator** pada ekosistem Maguru (Next.js + FastAPI/LangServe).

---

## 📌 Executive Summary

AI Quiz Generator Maguru dirancang untuk berevolusi dari pembuat kuis statis menjadi **Intelligent Adaptive Assessment Engine**. Dokumen ini merangkum 5 inovasi tingkat lanjut yang akan diimplementasikan pada fase pengembangan berikutnya.

```mermaid
graph TD
    subgraph Phase 1: Must-Have [Fase 1: Must-Have - Aktif]
        H[Progressive Hints 1 & 2]
        M[Micro-Skill Tagging]
        B[Bug Hunting with Line Numbers]
    end

    subgraph Phase 2: Should-Have [Fase 2: Should-Have - Terencana]
        C[Quiz Health & Balance Meter]
        D[Dynamic Few-Shot Ingestion per Domain]
    end

    subgraph Phase 3: Could-Have [Fase 3: Could-Have - Next-Gen]
        R[AI Reflection Critic Pass Multi-Agent]
        W[In-Browser WASM Code Sandbox Runner]
        A[Course Autopilot Batch Generator]
    end

    Phase 1 --> Phase 2 --> Phase 3
```

---

## 🚀 1. Inovasi Fase 2 (Should-Have)

### 1.1 Quiz Health & Balance Score Meter (UI Dashboard)
* **Deskripsi:** Visual widget interaktif di panel samping CMS kuis yang mengevaluasi mutu kumpulan soal secara otomatis sebelum diterbitkan.
* **Komponen Penilaian:**
  1. **Keseimbangan Kunci Jawaban:** Memastikan kunci A, B, C, dan D terdistribusi merata (masing-masing mendekati ~25%), tidak ada bias kunci menumpuk pada satu huruf.
  2. **Ragam Arketipe Soal:** Menampilkan rasio antara soal koding, studi kasus cerita, dan pemahaman konsep.
  3. **Estimasi Durasi Pengerjaan:** Perhitungan cerdas estimasi waktu yang dibutuhkan siswa untuk menyelesaikan kuis (misal: 1.5 menit per soal kode, 45 detik per soal teori).
* **Rencana Implementasi:** Mengintegrasikan kalkulasi lokal pada `breakdown` useMemo di `QuizEditorPanel.tsx` dan merendernya dalam panel ringkasan modern.

### 1.2 Dynamic Few-Shot Ingestion per Course Category
* **Deskripsi:** Menyesuaikan contoh soal (*exemplars*) dalam prompt LLM berdasarkan kategori kursus secara otomatis.
* **Mekanisme:**
  * Kursus **Python/Backend**: Prompt otomatis menyertakan contoh soal bertipe *Output Tracing* dan *Error Handling*.
  * Kursus **Frontend/JavaScript**: Menyertakan contoh soal *State Management* dan *Event Handling*.
  * Kursus **Bisnis/Desain**: Menyertakan contoh soal *A/B Testing Scenario* atau *User Experience Trade-offs*.
* **Keuntungan:** LLM tidak lagi bingung menentukan gaya soal, dan menghasilkan pertanyaan yang sangat relevan dengan disiplin ilmu yang diajarkan.

---

## 🔮 2. Inovasi Fase 3 (Could-Have / Next-Gen)

### 2.1 AI Reflection Critic Pass (Verifikasi Solvabilitas Multi-Agent)
* **Deskripsi:** Menerapkan pola multi-agent *Reflection* menggunakan LangGraph/LangChain untuk menjamin akurasi 100% pada soal yang dihasilkan.
* **Alur Kerja:**
  ```mermaid
  sequenceDiagram
      autonumber
      participant C as Creator CMS
      participant G as Quiz Generator Agent
      participant R as Reflection Critic Agent
      participant DB as Maguru Database

      C->>G: Request Kuis (Jumlah, Gaya, Materi)
      G->>G: Draf Soal Awal (Pass 1)
      G->>R: Evaluasi Kualitas & Solvabilitas
      R->>R: Uji 1: Apakah sintaks kode valid?
      R->>R: Uji 2: Apakah ada ambiguitas pada opsi?
      R->>R: Uji 3: Apakah kunci jawaban 100% tepat?
      alt Lulus Evaluasi
          R->>C: Kirim Soal Terverifikasi
      else Ditemukan Bug / Ambiguitas
          R->>G: Feedback Perbaikan (Pass 2 Self-Correction)
          G->>C: Kirim Soal yang Telah Direvisi
      end
  ```

### 2.2 In-Browser Code Sandbox Runner (WebAssembly / Pyodide)
* **Deskripsi:** Tombol interaktif **"▶ Test Run Kode"** langsung di dalam kartu soal kuis koding.
* **Teknologi:** Memanfaatkan WebAssembly client-side (seperti [Pyodide](https://pyodide.org/) untuk Python) yang berjalan langsung di browser tanpa membebani server backend.
* **Manfaat:**
  * **Bagi Creator:** Memastikan cuplikan kode pada soal benar-benar menghasilkan output yang sesuai sebelum disimpan.
  * **Bagi Siswa:** Memberikan ruang eksplorasi eksperimental saat kuis mode latihan mandiri.

### 2.3 Course Autopilot (Batch Generator untuk Seluruh Modul)
* **Deskripsi:** Satu tombol untuk menghasilkan kuis akhir bab bagi seluruh bab yang ada di dalam sebuah kursus secara asinkron.
* **Mekanisme:**
  * Menggunakan antrean background worker (Celery/FastAPI BackgroundTasks).
  * Menghasilkan kuis per section berdasarkan isi lesson masing-masing section.
  * Memberikan notifikasi toast atau status badge pada sidebar modul ketika draf kuis siap ditinjau.

---

## 📋 Catatan Arsitektur & Kompatibilitas Database

Semua data kuis (termasuk fitur baru seperti *progressive hints* dan *micro-skills*) disimpan ke dalam tabel PostgreSQL `assessment_questions`.
* Struktur kolom `options` berjenis JSON/JSONB:
  ```json
  {
    "a": "Opsi A",
    "b": "Opsi B",
    "c": "Opsi C",
    "d": "Opsi D",
    "explanation": "Pembahasan edukatif...",
    "hints": [
      "Hint 1: Ingat kembali bahwa tipe data tuple bersifat immutable.",
      "Hint 2: Perhatikan baris kode yang mencoba mengubah elemen indeks ke-0."
    ],
    "microSkill": "tuple-immutability"
  }
  ```
* **Kelebihan Pendekatan Ini:** Tidak memerlukan *database migration* atau alter table yang berisiko mengubah skema PostgreSQL, sehingga 100% aman dan langsung kompatibel dengan sistem yang sudah berjalan.

---

**Status:** Rencana Terdokumentasi  
**Target Eksekusi Inovasi Lanjutan:** Sprint Berikutnya (Wave 7+)
