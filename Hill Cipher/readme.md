# Program Hill Cipher 

## Identitas
- **Nama**  : Muhammad Zahran Muntazar
- **NPM**   : 140810230014

## Instalasi & Menjalankan Program
### Prasyarat
- Python 3.8+  
- Library: `numpy`

```bash
pip install numpy
```
### Menjalankan Program
Simpan sumber kode sebagai hill_cipher.py lalu jalankan:

```bash
python hill_cipher.py
```

## ✨ Fitur Utama
Program ini merupakan implementasi algoritma Hill Cipher dengan tiga fitur utama:

### 🔒 Enkripsi
- Pengguna memasukkan **plaintext** dan **matriks kunci**.
- Plaintext dipecah menjadi blok sesuai ukuran matriks.
- Setiap blok dikalikan dengan matriks kunci (mod 26) untuk menghasilkan **ciphertext**.

### 🔓 Dekripsi
- Pengguna memasukkan **ciphertext** dan **matriks kunci**.
- Program menghitung **determinan** matriks kunci, mencari **invers modulo 26**, lalu menyusun **invers matriks kunci**.
- Ciphertext dikalikan dengan matriks invers untuk mendapatkan kembali **plaintext**.

### 🔑 Pencarian Kunci dari Pasangan Plaintext & Ciphertext
- Pengguna memasukkan pasangan **plaintext** dan **ciphertext** dengan panjang minimal **n² huruf** (untuk kunci n×n).
- Program membangun matriks dari plaintext dan ciphertext, memilih submatriks yang dapat diinversi, lalu menghitung kunci dengan rumus:
  K ≡ C · P⁻¹ (mod 26)


## 💻 Alur Kerja Program
## Alur Program

1. **Mulai program**
   - Tampilkan judul dan menu utama.

2. **Tampilkan Menu Utama**

3. **Input pilihan menu**
- Jika **1 → Enkripsi**:
  1. Input ukuran matriks `n`.
  2. Input matriks kunci (per baris).
  3. Input plaintext.
  4. Konversi plaintext → angka.
  5. Bagi menjadi blok ukuran `n`.
  6. Kalikan blok dengan matriks kunci (mod 26).
  7. Gabungkan hasil menjadi ciphertext.
  8. Tampilkan ciphertext.

- Jika **2 → Dekripsi**:
  1. Input ukuran matriks `n`.
  2. Input matriks kunci (per baris).
  3. Input ciphertext.
  4. Hitung determinan kunci.
  5. Cari invers determinan (mod 26).
  6. Susun invers matriks kunci (mod 26).
  7. Kalikan ciphertext dengan matriks invers (mod 26).
  8. Gabungkan hasil menjadi plaintext.
  9. Tampilkan plaintext.

- Jika **3 → Mencari Kunci PT & CT**:
  1. Input ukuran matriks `n`.
  2. Input plaintext & ciphertext (≥ n² huruf).
  3. Bangun matriks P dan C dari blok teks.
  4. Cari submatriks P yang invertible (mod 26).
  5. Hitung K = C · P⁻¹ (mod 26).
  6. Tampilkan matriks kunci.

- Jika **0 → Keluar**:
  - Program berhenti.

4. **Kembali ke menu utama** (selama tidak memilih keluar).

5. **Selesai**

## 📊 Screenshot Running Program
### Menu Utama
![Menu Utama](screenshots/menu.png)

### Enkripsi
![Enkripsi](screenshots/enkripsi.png)

### Dekripsi
![Dekripsi](screenshots/dekripsi.png)

### Cari Kunci
![Cari Kunci](screenshots/cari_kunci.png)

## ⚠️ Catatan Penting
- Pastikan input plaintext/ciphertext panjangnya sesuai dengan ukuran kunci.