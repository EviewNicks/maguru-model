# Session 1.4: Input/Output Dasar

## Tujuan Pembelajaran
- Menggunakan print() untuk menampilkan output
- Menggunakan input() untuk menerima input user
- Membuat program interaktif sederhana
- Mengkonversi input string ke tipe data lain

## Konsep
**print()**: Menampilkan output ke console
**input()**: Menerima input dari user (selalu string!)
**Parameter print()**: sep (separator), end (karakter akhir)
**Escape characters**: \n (newline), \t (tab)

## Contoh
```python
# Print dasar
print("Hello, World!")
print("Nama saya", "Budi")  # Nama saya Budi

# Print dengan separator
print("2024", "05", "20", sep="-")  # 2024-05-20

# Print tanpa newline
print("Loading", end=" ")
print("selesai!")  # Loading selesai!

# Input dasar (selalu string!)
nama = input("Masukkan nama: ")
print(f"Halo, {nama}!")

# Input dengan konversi tipe
umur_str = input("Masukkan umur: ")
umur = int(umur_str)  # Konversi ke integer
tahun_lahir = 2024 - umur
print(f"Anda lahir sekitar {tahun_lahir}")

# Input langsung dengan konversi
umur = int(input("Masukkan umur: "))

# Program biodata sederhana
print("=" * 30)
print("   BIODATA SAYA")
print("=" * 30)
nama = input("Nama: ")
umur = input("Umur: ")
kota = input("Kota: ")
print(f"Nama: {nama}")
print(f"Umur: {umur} tahun")
print(f"Kota: {kota}")
print("=" * 30)
```

## Tugas Praktik
Buat program "Biodata Lengkap":
1. Minta: nama, umur, kota, hobi, minat_belajar
2. Tampilkan dengan format rapi menggunakan f-string
3. Gunakan print("=" * 30) untuk garis pembatas
4. Tampilkan hasil seperti:

```
====================
    BIODATA LENGKAP
====================
Nama      : Budi Santoso
Umur      : 25 tahun
Kota      : Jakarta
Hobi      : Membaca
Minat     : Python
====================
```

## Pertanyaan Diskusi
- Mengapa input() selalu mengembalikan string?
- Bagaimana cara menangani error jika user memasukkan "dua puluh" bukan angka?
- Apa yang terjadi jika kita lupa mengkonversi input string ke int/float?
