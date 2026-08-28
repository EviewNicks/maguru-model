# Panduan Manual Testing - Maguru MVP

Document ini berisi panduan langkah-demi-langkah untuk melakukan **End-to-End (E2E) Testing** pada aplikasi Maguru.

---

## Prasyarat Testing

### 1. Setup Environment

Pastikan semua dependency sudah terinstall:

```bash
# Install dependencies
pip install -r requirements.txt

# Pastikan file .env ada dengan API keys
# OPENROUTER_API_KEY atau ZAI_API_KEY
```

### 2. Jalankan Aplikasi

```bash
cd D:\.maguru\maguru-model
streamlit run app.py
```

Aplikasi akan berjalan di: `http://localhost:8501`

---

## Skenario Testing 1: Complete Learning Flow

**Tujuan:** Memastikan alur belajar lengkap berjalan dengan baik

### Langkah 1-5: Select Course & AI Greeting (UPDATED - 2025-02-12)

**Tujuan:** Memastikan AI greeting yang personalized, menarik, dan token-efficient.

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 1 | Buka http://localhost:8501 | Lihat halaman home dengan form input nama | - |
| 2 | Masukkan nama "Budi" → klik "Mulai Belajar" | Form hilang, muncul greeting yang MENARIK & PERSONALIZED (bukan "Halo" saja) | - |
| 3 | Lihat daftar kursus "Python Basics for Beginners" | Kartu kursus muncul dengan: judul, deskripsi, difficulty badge (🟢 beginner), durasi | - |
| 4 | Klik "Mulai Belajar - Python Basics for Beginners" | **AI Greeting muncul**: Greeting MENARIK (2-4 kalimat), menggunakan nama siswa, menyebut kursus & tujuan | *Property 8 terpenuhi* |

### Langkah 6-10: Learn Page Navigation

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 7 | Lihat konten session_1_1 | Markdown ter-render dengan benar, theory/examples/practice muncul | - |
| 8 | Lihat progress bar di atas | Menunjukkan "0/4 sesi selesai" atau progress bar | - |
| 9 | Lihat kolom kanan (chatbot) | Muncul pesan default "💡 Tanyakan apa saja..." | - |
| 10 | Klik "✅ Tandai Selesai" | Tombol berubah menjadi "✅ Sesi Selesai" | - |

### Langkah 11-13: Chatbot Interaction

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 11 | Ketik pertanyaan "Apa itu variabel?" → klik "Kirim" | Pesan muncul di bubble biru (Anda) | - |
| 12 | Tunggu AI merespon | Pesan AI muncul di bubble hijau dengan jawaban | - |
| 13 | Ulangi kirim 10+ pesan | Total pesan tetap 10 (FIFO - pesan lama dihapus) | *Property 4 terpenuhi* |

### Langkah 14-16: Quiz Completion

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 14 | Klik menu "Quiz" di sidebar | Halaman berpindah ke Quiz dengan instruksi, passing score 70%, waktu 15 menit | - |
| 15 | Isi semua pertanyaan (10 soal) | Radio button untuk pilihan ganda, text input untuk code completion | - |
| 16 | Klik "📤 Kirim Jawaban" | Muncul hasil dengan skor, persentase, status | *Property 2 terpenuhi* |

### Langkah 17-18: Progress & Verify

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 17 | Klik menu "Progress" di sidebar | Lihat overall progress, module checklist, quiz history | - |
| 18 | Verifikasi session_1_1 completed | Checklist menunjukkan ✓ untuk session_1_1 | - |

**✅ Kriteria Sukses Skenario 1:**
- [ ] AI Greeting muncul dengan nama siswa
- [ ] Konten session ter-render dengan benar
- [ ] Chatbot merespon pertanyaan
- [ ] Quiz bisa dijawab dan disubmit
- [ ] Progress menunjukkan session yang selesai
- [ ] State preserved saat navigasi antar halaman

---

## Skenario Testing 2: Failed Quiz Flow

**Tujuan:** Memastikan alur ketika gagal kuis berjalan dengan baik (retry mechanism)

### Langkah 1-3: Ambil Quiz dengan Jawaban Salah

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 1 | Di halaman Quiz, sengaja jawab semua soal SALAH | - | - |
| 2 | Klik "📤 Kirim Jawaban" | Skor < 70%, muncul "😅 Nilai Anda belum mencapai kelulusan" | *Property 3 terpenuhi* |
| 3 | Scroll ke bawah | Lihat detail jawaban per soal (✅ Benar / ❌ Salah) dengan penjelasan | - |

### Langkah 4-6: Weak Areas & Retry

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 4 | Lihat bagian "📚 Topik yang Perlu Ditinjau" | Muncul list topik dari jawaban yang salah | - |
| 5 | Klik tombol "🔄 Coba Lagi" | Quiz reset, jawaban dikosongkan, bisa isi lagi | *Property 20 terpenuhi* |
| 6 | Isi jawaban dengan BENAR → Submit | Skor >= 70%, muncul "🎉 Selamat! Anda LULUS!" | - |
| 7 | Kembali ke halaman Progress | Quiz history menunjukkan 2 attempt (attempt 1 gagal, attempt 2 lulus) | - |

**✅ Kriteria Sukses Skenario 2:**
- [ ] Pesan gagal muncul jelas saat skor < 70%
- [ ] Weak areas teridentifikasi dengan benar
- [ ] Tombol retry berfungsi
- [ ] Retry tidak menghapus hasil attempt sebelumnya
- [ ] Bisa lulus setelah retry

---

## Skenario Testing 3: Chat Context Flow

**Tujuan:** Memastikan chat history terbatas 10 pesan (FIFO)

### Langkah 1-5: Test Message Limit

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 1 | Di halaman Learn, kirim 15 pesan berurutan | - | - |
| 2 | Cek jumlah pesan yang ditampilkan | Hanya 10 pesan terakhir yang muncul | *Property 4 terpenuhi* |
| 3 | Lihat session state | `st.session_state.chat_history` hanya berisi 10 pesan | - |
| 4 | Kirim pesan ke-16 | Pesan 1-5 hilang, pesan 6-16 tersimpan (FIFO) | - |
| 5 | Verifikasi AI context | AI hanya melihat 10 pesan terakhir untuk konteks | - |

**✅ Kriteria Sukses Skenario 3:**
- [ ] Tepat 10 pesan ditampilkan
- [ ] Pesan ke-11 dan seterusnya dihapus otomatis
- [ ] AI response tetap relevan (context dari 10 pesan terakhir)

---

## Skenario Testing 4: Navigation Flow

**Tujuan:** Memastikan state preserved saat berpindah halaman

### Langkah 1-6: Cross-Page Navigation

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 1 | Di Home, pilih kursus → student_name terisi | State tersimpan | - |
| 2 | Pindah ke Learn → kirim chat message | Chat history muncul di Learn | - |
| 3 | Pindah ke Quiz → isi beberapa jawaban | Quiz answers tersimpan di state | - |
| 4 | Pindah ke Progress | Progress data muncul (completed sessions, quiz scores) | - |
| 5 | Kembali ke Home | Student name, course selection masih ada | *Property 6 terpenuhi* |
| 6 | Kembali ke Learn → Quiz → Progress | Semua state sebelumnya masih ada | - |

### Langkah 7-8: Session State Verification

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 7 | Cek `st.session_state` di console | Keys: initialized, student_name, current_course, current_module, current_session, completed_sessions, quiz_scores, chat_history, current_page | - |
| 8 | Refresh browser (F5) | Session state hilang (normal behavior Streamlit) | - |

**✅ Kriteria Sukses Skenario 4:**
- [ ] Student name preserved
- [ ] Current course/module/session preserved
- [ ] Chat history preserved
- [ ] Completed sessions preserved
- [ ] Quiz scores preserved
- [ ] Current page selection preserved

---

## Skenario Testing 5: AI Greeting Flow (UPDATED - 2025-02-12)

**Tujuan:** Memastikan AI greeting yang personalized, menarik, dan bervariasi (setiap kali bisa berbeda)

### Langkah 1-5: First Course Selection

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 1 | Buka app (fresh session) | Form input nama muncul | - |
| 2 | Masukkan nama "Siti" | Student name tersimpan | - |
| 3 | Pilih kursus "Python Basics" | AI greeting muncul di success banner | *Property 8 terpenuhi* |
| 4 | Baca pesan greeting | Berisi: "Siti", "Python Basics for Beginners", learning objectives | - |
| 5 | Cek chat history | Ada pesan AI greeting di riwayat chat | - |

### Langkah 6-8: Re-select Same Course

| Langkah | Aksi | Ekspektasi | Catatan |
|---------|-------|--------------|----------|
| 6 | Pilih kursus yang sama lagi | AI greeting TAMPIL DI KONTEN (bukan di sidebar) | - |
| 7 | Pindah ke halaman lain lalu kembali ke Home | State masih preserved, greeting tidak muncul ulang | - |
| 8 | Logout (refresh) dan pilih kursus lain | AI greeting baru untuk kursus baru | - |

**✅ Kriteria Sukses Skenario 5:**
- [ ] AI greeting muncul dengan variasi (tidak monoton/sama setiap kali)
- [ ] Greeting berisi nama siswa dan info kursus
- [ ] Greeting tidak muncul ulang untuk kursus yang sama
- [ ] Greeting baru muncul untuk kursus berbeda

---

## Checklist Testing Final

Setelah semua skenario diuji, tandai yang sudah completed:

### Functional Requirements
- [ ] **Property 1**: Session initialization works correctly
- [ ] **Property 2**: Quiz score calculation accurate
- [ ] **Property 3**: Pass/fail threshold 70% enforced
- [ ] **Property 4**: Chat history limited to 10 messages (FIFO)
- [ ] **Property 5**: Content hierarchy loads correctly
- [ ] **Property 6**: State preserved across page navigation
- [ ] **Property 7**: Next session unlocks after quiz pass
- [ ] **Property 8**: AI greeting triggers on first course selection (dengan variasi & personalisasi)
- [ ] **Property 16**: AI greeting includes student name + objectives

### UI/UX Requirements
- [ ] Sidebar navigation works smoothly
- [ ] All pages accessible from sidebar
- [ ] Course cards display all information
- [ ] Progress bars render correctly
- [ ] Chat messages have role-based styling
- [ ] Quiz questions display correctly (MC and code completion)
- [ ] Results page shows detailed feedback
- [ ] Indonesian language used throughout

### Error Handling
- [ ] Graceful handling when course content missing
- [ ] Graceful handling when API keys missing
- [ ] User-friendly error messages
- [ ] App doesn't crash on invalid input

---

## Bug Reporting Template

Jika menemukan bug selama testing, dokumentasikan dengan format:

```markdown
### Bug #[NOMOR]

**Skenario**: [Skenario 1-5]
**Langkah**: [Langkah detail saat bug terjadi]
**Ekspektasi**: [Yang seharusnya terjadi]
**Aktual**: [Yang sebenarnya terjadi]
**Screenshot**: [Opsional]
**Severity**: [Critical/High/Medium/Low]
```

---

## Next Steps Setelah Testing

Setelah selesai testing, lanjutkan ke:

### Task 15: Polish and Bug Fixes
- Perbaiki bug yang ditemukan
- Tambahkan loading indicators untuk AI responses
- Improve error messages
- Test responsive design (mobile)

### Deployment Preparation
- Pastikan environment variables siap untuk production
- Buat dokumentasi cara setup untuk pengguna baru
- Consider hosting options (Streamlit Cloud, Railway, dll)

---

**Document Version**: 1.0
**Created**: 2025-02-11
**Status**: Ready for Manual Testing
