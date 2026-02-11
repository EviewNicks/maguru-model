# Session 1.3: Operasi String

## Tujuan Pembelajaran
- Menggabungkan string
- Menggunakan metode string dasar
- Memformat string dengan f-strings
- Memahami indexing pada string

## Konsep
String adalah urutan karakter. Python menyediakan banyak cara untuk memanipulasi string.

**Penggabungan**: Gunakan + operator
**Metode**: upper(), lower(), strip(), replace()
**F-strings**: Format modern (Python 3.6+)
**Indexing**: Mengakses karakter dengan [index]

## Contoh
```python
# Penggabungan string
nama_depan = "Budi"
nama_belakang = "Santoso"
nama_lengkap = nama_depan + " " + nama_belakang
print(nama_lengkap)  # Budi Santoso

# Metode string
teks = "  Belajar Python  "
print(teks.upper())       # "  BELAJAR PYTHON  "
print(teks.lower())       # "  belajar python  "
print(teks.strip())       # "Belajar Python"
print(teks.replace("Python", "Java"))  # "  Belajar Java  "

# Panjang string
print(len("Hello"))  # 5

# Indexing (mulai dari 0)
kata = "Python"
print(kata[0])     # "P"
print(kata[-1])    # "n"
print(kata[0:3])   # "Pyt"

# F-strings
nama = "Budi"
umur = 25
print(f"Halo, {nama} umur {umur}")
# Halo, Budi umur 25

# Format dengan operasi
harga = 50000
diskon = 0.2
print(f"Diskon: Rp{harga * diskon:,}")
# Diskon: Rp 10,000
```

## Tugas Praktik
1. Buat program yang meminta nama dan hobi, tampilkan dengan f-string
2. Ubah "HEllo WOrLD" menjadi "hello world" dengan metode string
3. Ambil 3 karakter pertama dari nama kota Anda
4. Gabungkan dua string dengan spasi di antaranya

## Pertanyaan Diskusi
- Mengapa indexing dimulai dari 0 di Python?
- Apa perbedaan antara strip(), lstrip(), dan rstrip()?
- Kapan sebaiknya menggunakan f-strings dibanding cara lain?
