# Session 1.2: Tipe Data dalam Python

## Tujuan Pembelajaran
- Mengenali tipe data dasar Python
- Menggunakan fungsi type()
- Melakukan konversi tipe data
- Memahami perbedaan setiap tipe data

## Konsep
Python memiliki beberapa tipe data dasar:

**Integer (int)**: Bilangan bulat
```python
umur = 25
jumlah_siswa = 30
```

**Float**: Bilangan desimal
```python
tinggi = 1.75
berat = 65.5
```

**String (str)**: Teks atau karakter
```python
nama = "Maguru"
pesan = 'Belajar Python'
```

**Boolean (bool)**: True atau False
```python
sudah_lulus = True
masih_belajar = False
```

## Contoh
```python
# Mengecek tipe data
umur = 25
print(type(umur))  # <class 'int'>

tinggi = 1.75
print(type(tinggi))  # <class 'float'>

nama = "Maguru"
print(type(nama))  # <class 'str'>

sudah_lulus = True
print(type(sudah_lulus))  # <class 'bool'>

# Konversi tipe data
angka_str = "100"
angka_int = int(angka_str)  # Konversi ke integer
print(angka_int + 50)  # 150

desimal = int(3.7)  # 3 (dibulatkan ke bawah)
teks = str(123)     # "123"
```

## Tugas Praktik
1. Buat variabel dengan setiap tipe data (int, float, str, bool)
2. Gunakan type() untuk memeriksa tipe data setiap variabel
3. Konversi string "25" ke integer dan tambahkan 10
4. Konversi angka 100 ke string dan gabungkan dengan teks "Nilai: "

## Pertanyaan Diskusi
- Kapan kita harus menggunakan float bukan integer?
- Mengapa hasil type("25") berbeda dengan type(25)?
- Apa yang terjadi jika kita menjumlahkan string dengan angka tanpa konversi?
