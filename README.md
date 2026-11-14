# SIM Laundry - Sistem Informasi Manajemen Operasional Jasa Laundry
> **Proyek Praktikum Rekayasa Perangkat Lunak (RPL) - Kelompok 3**

Aplikasi desktop manajemen operasional laundry modern berbasis **Python**, antarmuka grafis **CustomTkinter**, dan basis data relasional **MySQL/MariaDB**, yang dibangun mengikuti arsitektur **MVC (Model-View-Controller)** serta dilengkapi dengan **Role-Based Access Control (RBAC)** dan **CI/CD Pipeline**.

---

## 👥 Pembagian Tugas Kelompok

| Anggota | Peran / Fokus | Berkas Tanggung Jawab |
| :---: | :--- | :--- |
| **Anggota 1** | **MVC – Model Pelanggan & Paket** | `models/pelanggan_model.py`, `models/paket_model.py` |
| **Anggota 2** | **MVC – Model Transaksi & Controller** | `models/transaksi_model.py`, `controller/laundry_controller.py` |
| **Anggota 3** | **MVC – View Laundry** | `views/laundry_view.py` |
| **Anggota 4** | **MVC – Dashboard & Tampilan Utama** | `views/dashboard_view.py`, `assets/logo.png`, `main.py` |
| **Anggota 5** | **Modul VII – Autentikasi & Registrasi** | `models/user_model.py`, `controller/auth_controller.py`, `views/login_view.py`, `views/register_view.py` |
| **Anggota 6** | **Modul VI & VII – Otorisasi & Unit Testing** | `tests/test_laundry.py`, `tests/test_auth.py`, `tests/test_models.py` |
| **Anggota 7** | **Modul VIII – CI/CD & Dokumentasi Teknis** | `.github/workflows/ci_pipeline.yml`, `requirements.txt`, `README.md`, `.gitignore` |

---

## 🛠️ Arsitektur & Struktur Proyek

```
Projek_UTS_PraktikumRPL_Klp3/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml       # GitHub Actions CI (Flake8 & Pytest)
├── assets/
│   └── logo.png                  # Logo visual SIM Laundry
├── config/
│   └── database.py               # Konfigurasi koneksi MySQL dinamis
├── controller/
│   ├── auth_controller.py        # Controller autentikasi & validasi akun
│   └── laundry_controller.py     # Controller operasional laundry & RBAC
├── database/
│   └── db_laundry.sql            # Skema DDL tabel MySQL & data bawaan
├── models/
│   ├── paket_model.py            # Model CRUD paket layanan
│   ├── pelanggan_model.py        # Model CRUD master pelanggan
│   ├── transaksi_model.py        # Model CRUD transaksi laundry
│   └── user_model.py             # Model akun pengguna & hashing SHA-256
├── tests/
│   ├── test_auth.py              # Unit test autentikasi & registrasi
│   ├── test_laundry.py           # Unit test transaksi & RBAC
│   └── test_models.py            # Unit test model pelanggan & paket
├── views/
│   ├── dashboard_view.py         # Antarmuka ringkasan KPI & riwayat
│   ├── laundry_view.py           # Antarmuka input & tabel transaksi
│   ├── login_view.py             # Antarmuka login pengguna
│   └── register_view.py          # Antarmuka registrasi akun operator baru
├── .flake8                       # Konfigurasi linter Flake8
├── .gitignore                    # Berkas pengecualian Git
├── main.py                       # Titik masuk utama aplikasi (Main GUI)
├── requirements.txt              # Daftar dependensi Python
└── README.md                     # Dokumentasi teknis proyek
```

---

## 🌟 Fitur Utama

1. **Pola MVC Murni**: Pemisahan jelas antara layer data (`models`), layer bisnis (`controller`), dan antarmuka (`views`).
2. **Autentikasi Aman & Hashing SHA-256**: Password pengguna disimpan dalam bentuk digest SHA-256 (64 digit heksadesimal).
3. **Role-Based Access Control (RBAC)**:
   - **Admin**: Akses penuh ke seluruh fitur (tambah/edit/hapus transaksi, tambah/hapus paket layanan, hapus pelanggan).
   - **User (Operator)**: Akses terbatas (hanya menginput transaksi baru dan melihat dashboard).
4. **Perhitungan Biaya Real-Time**: Total biaya dihitung otomatis saat bobot atau paket layanan dipilih.
5. **Penyempurnaan Fungsi UPDATE**: Pembaruan transaksi menggunakan SQL `UPDATE` murni pada `id_transaksi` yang sama, menjaga integritas nomor nota dan relasi database.
6. **Dashboard Dinamis**: Statistik real-time total pendapatan, berat cucian, transaksi harian, status pengerjaan, dan riwayat pelanggan.
7. **Automated Testing & CI/CD**: Pengujian otomatis menggunakan `pytest` (12 unit test) dan linter `flake8` yang terintegrasi pada GitHub Actions.

---

## 🚀 Panduan Instalasi & Menjalankan Aplikasi

### 1. Prasyarat Sistem
- Python versi 3.10 atau lebih baru.
- MySQL / MariaDB (disarankan menggunakan Laragon atau XAMPP).

### 2. Konfigurasi Basis Data
1. Buka Laragon atau XAMPP, lalu jalankan modul **MySQL**.
2. Buka phpMyAdmin atau HeidiSQL, buat basis data baru bernama `db_laundry`:
   ```sql
   CREATE DATABASE db_laundry;
   ```
3. Import berkas `database/db_laundry.sql` ke dalam basis data `db_laundry`.

### 3. Instalasi Dependensi
Buka terminal pada direktori proyek, lalu pasang dependensi:
```powershell
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi
Jalankan perintah berikut:
```powershell
python main.py
```

### 🔑 Akun Bawaan untuk Pengujian
- **Admin**:
  - Username: `atmin`
  - Password: `atmin123`
  - Akses: Semua fitur CRUD transaksi, paket, dan pelanggan aktif.
- **User (Operator)**:
  - Registrasi langsung akun baru melalui tombol **"Daftar Akun Baru"** pada jendela login.
  - Akun baru otomatis memperoleh role `User`.

---

## 🧪 Pengujian Otomatis & Pemeriksaan Kualitas Kode

### Menjalankan Unit Test (Pytest)
```powershell
pytest -v
```
*Hasil: 12 pengujian unit berhasil (100% Passed).*

### Menjalankan Pemeriksaan Sintaks (Flake8)
```powershell
flake8
```
*Hasil: Bebas kesalahan sintaks (0 error/warning).*

---

## 📦 Panduan Packaging (.exe) Menggunakan PyInstaller

Sesuai ketentuan Modul VIII, aplikasi dapat dikemas menjadi berkas biner `.exe` mandiri:

1. Jalankan perintah PyInstaller:
   ```powershell
   pyinstaller --noconsole --onefile --add-data "assets;assets" --name "SIM-Laundry" main.py
   ```
2. Berkas eksekusi akan dibuat di folder `dist/SIM-Laundry.exe`.

### 🏷️ GitHub Release (v1.0.0)
Untuk menyiapkan rilis GitHub Release versi `v1.0.0`:
1. Buat tag Git:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0 - SIM Laundry Sistem Operasional"
   git push origin v1.0.0
   ```
2. Buka menu **Releases** di GitHub, klik **Draft a new release**, pilih tag `v1.0.0`, lampirkan berkas `SIM-Laundry.exe` dari folder `dist/`, dan publikasikan.
