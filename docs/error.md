(base) PS D:\.maguru\maguru-model> conda activate D:\conda_envs\maguru                           
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> pip install pytest flake8                     
Requirement already satisfied: pytest in d:\conda_envs\maguru\lib\site-packages (9.0.2)
Collecting flake8
  Using cached flake8-7.3.0-py2.py3-none-any.whl.metadata (3.8 kB)
Requirement already satisfied: colorama>=0.4 in d:\conda_envs\maguru\lib\site-packages (from pytest) (0.4.6)
Requirement already satisfied: iniconfig>=1.0.1 in d:\conda_envs\maguru\lib\site-packages (from pytest) (2.3.0)
Requirement already satisfied: packaging>=22 in d:\conda_envs\maguru\lib\site-packages (from pytest) (24.2)
Requirement already satisfied: pluggy<2,>=1.5 in d:\conda_envs\maguru\lib\site-packages (from pytest) (1.6.0)
Requirement already satisfied: pygments>=2.7.2 in d:\conda_envs\maguru\lib\site-packages (from pytest) (2.19.2)
Collecting mccabe<0.8.0,>=0.7.0 (from flake8)
  Using cached mccabe-0.7.0-py2.py3-none-any.whl.metadata (5.0 kB)
Collecting pycodestyle<2.15.0,>=2.14.0 (from flake8)
  Using cached pycodestyle-2.14.0-py2.py3-none-any.whl.metadata (4.5 kB)
Collecting pyflakes<3.5.0,>=3.4.0 (from flake8)
  Using cached pyflakes-3.4.0-py2.py3-none-any.whl.metadata (3.5 kB)
Using cached flake8-7.3.0-py2.py3-none-any.whl (57 kB)
Using cached mccabe-0.7.0-py2.py3-none-any.whl (7.3 kB)
Using cached pycodestyle-2.14.0-py2.py3-none-any.whl (31 kB)
Using cached pyflakes-3.4.0-py2.py3-none-any.whl (63 kB)
Installing collected packages: pyflakes, pycodestyle, mccabe, flake8
Successfully installed flake8-7.3.0 mccabe-0.7.0 pycodestyle-2.14.0 pyflakes-3.4.0
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> pytest --version
pytest 9.0.2
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> flake8 --version
7.3.0 (mccabe: 0.7.0, pycodestyle: 2.14.0, pyflakes: 3.4.0) CPython 3.12.12 on Windows
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> python -m py_compile server.py
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> python -m py_compile app.py
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> Get-ChildItem -Path ai_chains -Filter *.py -Recurse | ForEach-Object { python -m py_compile $_.FullName }
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> pytest tests/ --tb=short --disable-warnings
===================================== test session starts ======================================
platform win32 -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0 -- D:\conda_envs\maguru\python.exe
cachedir: .pytest_cache
rootdir: D:\.maguru\maguru-model
configfile: pytest.ini
plugins: anyio-4.12.1, langsmith-0.7.3, cov-7.0.0
collected 0 items                                                                               

==================================== no tests ran in 0.06s =====================================
ERROR: file or directory not found: tests/

(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> python test_ai_chains_simple.py
============================================================
Testing Maguru AI Chains
============================================================

[TEST 1] Code Explanation Chain
----------------------------------------
No `_type` key found, defaulting to `prompt`.
Input code:
nama = 'Budi'
umur = 25

Output:
### Penjelasan Kode Python untuk Siswa Indonesia
**Kode:**
```python
nama = 'Budi'
umur = 25
```

#### 1. Apa yang dilakukan setiap baris?
- **Baris pertama (`nama = 'Budi'`):**
  Kita menyimpan teks `'Budi'` ke dalam sebuah **kotak** yang bernama `nama`.
  *Contoh analogi:* Kita meletakkan nama "Budi" ke dalam kotak yang kita sebut `nama`.

- **Baris kedua (`umur = 25`):**
  Kita menyimpan angka `25` ke dalam sebuah **kotak** yang bernama `umur`.
  *Contoh analogi:* Kita meletakkan angka 25 ke dalam kotak yang kita sebut `umur`.

#### 2. Mengapa kode bekerja seperti itu?
- **Python otomatis mengenali tipe data:**
  - `'Budi'` di dalam tanda kutip (`' '`) → **string** (teks).
  - `25` tanpa tanda kutip → **integer** (angka).
  Python tidak perlu dijelaskan tipe data, karena ia bisa mendeteksi sendiri!

- **Operator `=` fungsinya:**
  Simbol `=` di Python bukan seperti penjumlahan, tapi sebagai **penanda** ("ini kotaknya"). Kita meletakkan nilai di sebelah kanan ke kotak di sebelah kiri.

#### 3. Kesalahan Umum yang Harus Dihindari
- **Menggunakan tanda kutip salah:**
  - **Salah:** `nama = "Budi` (tutup kutip di bagian akhir tidak ada).
  - **Benar:** `'Budi'` atau `"Budi"` (tanda kutip harus sama di awal dan akhir).

- **Mengubah tipe data secara tidak sengaja:**
  - Jika kita tulis `umur = "25"` (dengan tanda kutip), angka `25` menjadi **string** (teks), bukan angka.

- **Variabel yang salah ditulis:**
  - Jika kita tulis `Nama` (dengan huruf besar) di baris lain, Python akan **salah paham** karena `Nama` berbeda dari `nama`.

#### **Semangat!**
Python sangat ramah untuk pemula! Kode sederhana seperti ini adalah **langkah pertama menciptakan program**. Setiap kotak (variabel) kita isi dengan nilai, dan Python akan menjaga seluruh logikanya. Jika ada kesalahan, Python akan memberi **pemberitahuan** yang jelas. Terus praktekkan, dan kamu akan bisa membuat program yang menarik! 🚀
[PASS] Test 1 completed

============================================================
[TEST 2] Hint Generator Chain
----------------------------------------
No `_type` key found, defaulting to `prompt`.

Level 1:


Berikut hint dalam Bahasa Indonesia untuk tugas membuat variabel 'kota':

**Level 1 (Halus):**
Coba tulis kode seperti ini:
`var kota = "Jakarta";`
*(Petunjuk halus: Gunakan kata kunci `var` untuk mendeklarasikan variabel, lalu tulis nama variabel `kota` dan isinya dalam tanda kutip)*

**Level 2 (Konseptual):**
`kota` adalah variabel yang menyimpan nama suatu tempat. Contoh:
```javascript
var kota = "Surabaya";
console.log(kota); // Menampilkan "Surabaya"
```
*(Konsep: Variabel seperti kotak yang menyimpan data. Isinya bisa berubah, seperti mengganti "Surabaya" menjadi "Yogyakarta")*

**Level 3 (Langsung):**
Jika kamu lupa bagian penting:
```javascript
var kota = "Bandung"; // ✗
```
**Masukkan tanda kurung kurawal untuk deklarasi!**
```javascript
var kota = "Bandung"; // ✓
```
*(Langsung: Tanda kurung kurawal `{}` diperlukan untuk menutup deklarasi variabel)*

**Catatan:**
- Gunakan tanda kutip untuk teks ("Surabaya").
- Jika ingin nilai berubah, tulis ulang variabelnya.
- Variabel `kota` bisa digunakan di kode lain (misal: `console.log(kota)`).

Level 2:


Berikut hint dalam Bahasa Indonesia untuk tugas membuat variabel `kota` pada level konseptual:   

**Level Konseptual (Jelaskan konsep dengan contoh serupa):**

> "Kita ingin menyimpan nama sebuah kota, seperti 'Jakarta' atau 'Surabaya'.
> **Contoh praktis:**
> `kota = "Yogyakarta"`
>
> **Penjelasan:**
> Di sini, `kota` adalah **variabel**. Variabel itu seperti sebuah kotak, kita beri nama (`kota`), lalu kita masukkan isinya, yaitu nama sebuah kota dalam tanda kutip (`"Yogyakarta"`).
>
> **Konsep:**
> - **Variabel** = Kotak yang menyimpan data (di sini, data adalah nama kota).
> - **Nama variabel** = Nama kotaknya (`kota`).
> - **Nilai variabel** = Isi kotaknya (`"Yogyakarta"`).
>
> **Perbedaan:**
> Jika kita tulis `print(kota)`, program akan menampilkan `Yogyakarta` di layar, seperti membuka kotak `kota` dan menuliskan isinya."

**Penjelasan singkat:**
Variabel `kota` adalah tempat menyimpan sebuah teks (string) yang mewakili nama kota. Kita beri nama variabelnya (`kota`), lalu berikan nilai (nama kota dalam tanda kutip).

Level 3:


Berikut pendekatan langsung untuk tugas variabel 'kota' dalam Bahasa Indonesia:

**Langkah-langkah yang harus dilakukan:**

1.  **Buat variabel bernama `kota`:**
    Tuliskan kode untuk deklarasi variabel dengan nama `kota` menggunakan keyword yang sesuai untuk bahasa pemrograman yang digunakan (misalnya: `var`, `let`, `const` untuk JavaScript; `kota =` untuk Python).
    *Contoh kode:*
    `var kota;`
    `let kota;`
    `const kota = "Jakarta";`
    `kota = "Surabaya";`

2.  **Berikan nilai ke variabel `kota`:**
    Setelah deklarasi variabel, **isi variabel tersebut dengan nilai tertentu**. Nilai ini biasanya berupa teks (string) yang menandakan nama kota.
    *Contoh kode:*
    `kota = "Jakarta";`
    `kota = "Surabaya";`
    `kota = "Yogyakarta";`

**Penjelasan Singkat (Level Langsung):**

> **Kamu perlu menciptakan sebuah variabel bernama `kota`.**
> **Langkah pertama:** Tuliskan deklarasi variabel `kota` (misal: `var kota;` atau `let kota;`). 

> **Langkah kedua:** **Tambahkan nilai** untuk variabel `kota` di belakang tanda sama dengan (`=`). Nilai ini adalah **nama kota** dalam bentuk teks (dalam tanda kutip ganda `" "`).
> **Contoh lengkap:**
> `var kota = "Jakarta";`
> `let kota = "Surabaya";`
> `const kota = "Yogyakarta";`
> `kota = "Bandung";`
> **Jadi, kode lengkapnya adalah:** `kota = "NamaKamu";` (ganti `"NamaKamu"` dengan nama kota yang ingin kamu simpan).

**Catatan Penting:**
*   **Tanda kutip ganda `" "`** adalah **harus** digunakan untuk menyatukan teks (nama kota).    
*   **Kamu bisa menggunakan `var`, `let`, atau `const`** untuk deklarasi variabel, tergantung konteks dan kebutuhan kamu.
*   **Nilai yang dimasukkan adalah string** (teks), bukan angka atau logika.

**Contoh Penyelesaian Lengkap (JavaScript):**
```javascript
// Deklarasi dan memberi nilai
let kota = "Jakarta"; // Simpan nama kota Jakarta

// Menggunakan variabel kota
console.log(kota); // Menampilkan "Jakarta" di console
```
[PASS] Test 2 completed

============================================================
[TEST 3] Quiz Feedback Chain
----------------------------------------

[Correct Answer Test]
No `_type` key found, defaulting to `prompt`.
Feedback: 

**Rayakandan Jelaskan Mengapa Benar!**

**Output print(2+2) adalah 4!** 🎉

**Penjelasan:**
Kamu benar-benar hebat! Operasi penjumlahan dasar seperti `2 + 2` di Python pasti menghasilkan angka **4**. Ini karena Python secara otomatis menghitung nilai aritmatika sebelum menampilkan hasilnya.

**Mengapa ini benar?**
1. **Python menghitung operasi** secara otomatis sebelum menampilkan output.
2. **2 + 2 = 4** adalah rumus dasar yang tidak ada konflik.
3. **Syntax print()** hanya digunakan untuk menampilkan hasil, bukan mengubah logika perhitungan.


**Semangat untuk kamu!** Semakin kamu latihan, semakin menguasai konsep dasar ini. Kita lanjutkan ke tantangan berikutnya! 🚀

[Incorrect Answer Test]
Feedback: 

**Jawaban dengan lembut dan semangat:**

**"Wah, semangat ya! Kamu sudah berusaha dan itu sangat baik. Ternyata jawabannya salah, tapi jangan berkecil hati. Mari kita lihat: operator `+` di Python selalu menambahkan angka, bukan menggabungkan huruf atau karakter. Jadi, `2 + 2` menghasilkan angka **4**, bukan 5.

Contoh lainnya: jika kamu menulis `print(3 + 1)`, akan keluar angka **4**. Tapi kalau kamu menulis `print("2" + "2")`, itu akan menampilkan **"22"** karena operator `+` di sini menggabungkan teks (string).

Kamu bisa coba lagi! Setiap kesalahan itu pelajaran baru. Semangat ya, kamu bisa!* 💛"**
[PASS] Test 3 completed

============================================================
[TEST 4] Q&A Chatbot Chain
----------------------------------------
No `_type` key found, defaulting to `prompt`.
Question: Apa itu variabel?
Answer:
Salam, siswa! **Variabel** adalah konsep dasar yang sangat penting dalam pemrograman, termasuk Python. Dalam konteks sesi kita sekarang, **variabel adalah wadah atau kotak yang digunakan untuk menyimpan data**, seperti angka, teks, atau nilai lainnya.

**Referensi ke materi sesi:**
Di sesi ini, kita belajar bahwa membuat variabel di Python sangat mudah. Anda hanya perlu memberikan nama variabel, diikuti tanda sama dengan (`=`), dan nilai yang ingin disimpan. Contohnya:    
`nama_siswa = "Budi"`
Di sini, `"Budi"` adalah data yang disimpan dalam variabel `nama_siswa`.

**Penjelasan dengan contoh:**
1. **Simpan angka:**
   ```python
   umur = 25
   ```
   Di sini, variabel `umur` menyimpan nilai `25` (angka integer).

2. **Simpan teks:**
   ```python
   nama = "Ana"
   ```
   Di sini, variabel `nama` menyimpan teks `"Ana"` (dalam tanda kutip).

3. **Simpan logika benar/salah:**
   ```python
   is_laki = True
   ```
   Di sini, variabel `is_laki` menyimpan nilai logika `True` (benar) atau `False` (salah).       

**Penting untuk diingat:**
- Variabel hanya menyimpan *nilai*, bukan kode.
- Nama variabel harus **unik** dan **jelas** (misal: `total_harga` lebih baik daripada `x`).     
- Python **sensitif terhadap huruf besar/kecil**, jadi `nama` berbeda dengan `Nama`.

**Nada yang sabar dan memberikan semangat:**
Siswa, jangan khawatir jika konsep ini masih terdengar baru. Variabel adalah alat yang sangat praktis untuk memanajemen data dalam program. Setiap kali Anda menulis kode, variabel akan membantu Anda mengorganisir informasi dengan mudah.

**Contoh praktis:**
Apa jika Anda ingin membuat program hitung umur tahun depan?
```python
tahun_lahir = 2000  # Variabel menyimpan tahun lahir
tahun_sekarang = 2023  # Variabel menyimpan tahun sekarang
umur = tahun_sekarang - tahun_lahir  # Variabel menghitung umur
print(umur)  # Output: 23
```
Lihat? Variabel `tahun_lahir`, `tahun_sekarang`, dan `umur` bekerja sama untuk menjawab pertanyaan tersebut!

**Pertanyaan untuk dipertanyakan:**
Jika ada pertanyaan seperti: *"Apa bedanya `nama = 'Budi'` dan `nama = 'Budi'`?"*
Jawabannya: Tidak ada perbedaan sama sekali! Tanda kutip di Python hanya untuk menandai teks, tidak mengubah nilai.

Saya yakin kamu bisa! Jangan ragu untuk bertanya lagi jika ada yang tidak paham. 😊
[PASS] Test 4 completed

============================================================
[TEST 5] AI Greeting Chain
----------------------------------------
No `_type` key found, defaulting to `prompt`.
Student: Budi
Course: Python Basics
Greeting:


Hey Budi! 😎 Keren banget nih kamu mau mulai belajar Python Basics. Python itu bahasa yang super fleksibel, bisa dipakai buat web, AI, data science, bahkan game!

Apa pengalaman kamu dulu dengan Python atau program lain?
[PASS] Test 5 completed

============================================================
All tests completed!
============================================================
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
0
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
.\.claude\hooks\check_input.py:10:12: W292 no newline at end of file
.\.claude\hooks\log_pre_tool_use.py:53:7: W292 no newline at end of file
.\.claude\hooks\macos_notification.py:7:1: E302 expected 2 blank lines, found 1
.\.claude\hooks\macos_notification.py:19:15: F541 f-string is missing placeholders
.\.claude\hooks\macos_notification.py:20:9: F841 local variable 'result' is assigned to but never used
.\.claude\hooks\macos_notification.py:21:15: F541 f-string is missing placeholders
.\.claude\hooks\macos_notification.py:27:1: E302 expected 2 blank lines, found 1
.\.claude\hooks\macos_notification.py:31:1: W293 blank line contains whitespace
.\.claude\hooks\macos_notification.py:60:1: W293 blank line contains whitespace
.\.claude\hooks\macos_notification.py:63:1: E305 expected 2 blank lines after class or function definition, found 1
.\.claude\hooks\macos_notification.py:63:7: W292 no newline at end of file
.\.claude\hooks\play_audio.py:54:7: W292 no newline at end of file
.\.claude\hooks\ts_lint.py:9:1: C901 'main' is too complex (12)
.\.claude\hooks\ts_lint.py:84:7: W292 no newline at end of file
.\.claude\hooks\use_bun.py:8:1: C901 'main' is too complex (11)
.\.claude\hooks\use_bun.py:8:1: E302 expected 2 blank lines, found 1
.\.claude\hooks\use_bun.py:22:9: F841 local variable 'yarn_pattern' is assigned to but never used
.\.claude\hooks\use_bun.py:23:9: F841 local variable 'npx_pattern' is assigned to but never used 
.\.claude\hooks\use_bun.py:73:128: E501 line too long (157 > 127 characters)
.\.claude\hooks\use_bun.py:84:1: E305 expected 2 blank lines after class or function definition, found 1
.\.claude\hooks\use_bun.py:84:7: W292 no newline at end of file
.\.claude\hooks\utils\generate_audio_clips.py:9:1: C901 'main' is too complex (11)
.\.claude\hooks\utils\generate_audio_clips.py:78:7: W292 no newline at end of file
.\.claude\hooks\windows_notification.py:7:1: E302 expected 2 blank lines, found 1
.\.claude\hooks\windows_notification.py:14:1: W293 blank line contains whitespace
.\.claude\hooks\windows_notification.py:43:1: W293 blank line contains whitespace
.\.claude\hooks\windows_notification.py:47:1: E305 expected 2 blank lines after class or function definition, found 1
.\.claude\hooks\windows_notification.py:47:7: W292 no newline at end of file
.\ai_chains\chains\__init__.py:12:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\ai_greeting.py:11:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\ai_greeting.py:19:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\ai_greeting.py:33:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\ai_greeting.py:63:5: F841 local variable 'e' is assigned to but never used    
.\ai_chains\chains\explain_code.py:10:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\explain_code.py:18:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\hint_generator.py:10:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\hint_generator.py:18:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\hint_generator.py:41:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\qa_chatbot.py:11:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\qa_chatbot.py:21:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\qa_chatbot.py:22:20: E128 continuation line under-indented for visual indent  
.\ai_chains\chains\qa_chatbot.py:47:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\quiz_feedback.py:10:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\quiz_feedback.py:18:1: E302 expected 2 blank lines, found 1
.\ai_chains\chains\quiz_feedback.py:19:22: E128 continuation line under-indented for visual indent
.\ai_chains\chains\quiz_feedback.py:40:5: F841 local variable 'e' is assigned to but never used  
.\app.py:15:1: E402 module level import not at top of file
.\app.py:16:1: E402 module level import not at top of file
.\app.py:49:1: C901 'main' is too complex (14)
.\server.py:14:1: F401 'asyncio' imported but unused
.\server.py:15:1: F401 'typing.Optional' imported but unused
.\server.py:15:1: F401 'typing.AsyncGenerator' imported but unused
.\server.py:19:1: F401 'fastapi.responses.StreamingResponse' imported but unused
.\server.py:50:1: E302 expected 2 blank lines, found 1
.\tests\test_ai_chains_simple.py:77:128: E501 line too long (164 > 127 characters)
.\tests\test_ai_chains_simple.py:80:11: F541 f-string is missing placeholders
.\tests\test_ai_chains_simple.py:102:11: F541 f-string is missing placeholders
.\utils\quiz_validator.py:7:1: F401 'typing.Optional' imported but unused
.\utils\session_manager.py:9:1: F401 'typing.Optional' imported but unused
4     C901 'main' is too complex (12)
2     E128 continuation line under-indented for visual indent
19    E302 expected 2 blank lines, found 1
3     E305 expected 2 blank lines after class or function definition, found 1
2     E402 module level import not at top of file
2     E501 line too long (157 > 127 characters)
6     F401 'asyncio' imported but unused
4     F541 f-string is missing placeholders
5     F841 local variable 'result' is assigned to but never used
8     W292 no newline at end of file
4     W293 blank line contains whitespace
59
(D:\conda_envs\maguru) PS D:\.maguru\maguru-model> 