# Responsi Praktikum Pekan 7: Aplikasi Pengambilan Matakuliah (KRS)

Sistem informasi berbasis web untuk pengelolaan Kartu Rencana Studi (KRS) mahasiswa yang dikembangkan menggunakan framework Python Flask dan database MariaDB/MySQL. Project ini disusun untuk memenuhi kriteria evaluasi Responsi Pekan 7 Praktikum Pemrograman Web.

## Informasi Mahasiswa
- **Nama:** Fadhilah Fausta Alhasny
- **NIM:** 3253111003
- **Program Studi:** D3 Sistem Informasi
  

---

## Fitur & Cakupan Teknologi

- **Virtual Environment & Flask Framework:** Lingkungan eksekusi terisolasi menggunakan `venv` pada sistem operasi Fedora Linux.
- **Autentikasi & Flask Session:** Fitur login/logout berbasis NIM dan Password dengan pengelolaan sesi pengguna (`session`).
- **Integrasi Database Relasional:** Menggunakan `mysql-connector-python` untuk menghubungkan Flask ke database MariaDB (`db_responsi_pweb`).
- **Skema Relasi Many-to-Many:** Menghubungkan entitas `mahasiswa` dan `matakuliah` melalui tabel pivot `matakuliah_diambil`.
- **Tampilan Interaktif Bootstrap 5:** Antarmuka responsif untuk katalog mata kuliah yang tersedia dan daftar mata kuliah yang berhasil diambil/dibatalkan.

---

## Penjelasan Alur Kerja Aplikasi

1. **Autentikasi Mahasiswa (`/login`):**
   - Mahasiswa melakukan autentikasi menggunakan NIM dan Password.
   - Sistem mencocokkan kredensial dengan tabel `mahasiswa`. Jika valid, data identitas disimpan ke dalam `session` dan mengarahkan ke dashboard.

2. **Dashboard KRS (`/dashboard`):**
   - Menampilkan data profil singkat mahasiswa yang sedang aktif.
   - Menyajikan dua tabel utama:
     - **Mata Kuliah Tersedia:** Daftar seluruh mata kuliah dari database beserta aksi **"Ambil"**.
     - **Mata Kuliah yang Dipilih:** Daftar mata kuliah yang sudah didaftarkan mahasiswa beserta aksi **"Batal"**.

3. **Transaksi KRS (`/ambil/<id>` & `/hapus/<id>`):**
   - Tombol **Ambil** menyimpan entri baru ke dalam tabel pivot `matakuliah_diambil` sesuai `mahasiswa_id` dan `matakuliah_id`.
   - Tombol **Batal** menghapus entri mata kuliah terkait dari tabel pivot.

---

## Skema Basis Data (`db_responsi_pweb`)

```text
+---------------+       +--------------------+       +---------------+
|   mahasiswa   |       | matakuliah_diambil |       |  matakuliah   |
+---------------+       +--------------------+       +---------------+
| id (PK)       |<------| mahasiswa_id (FK)  |       | id (PK)       |
| nim           |       | matakuliah_id (FK) |------>| kode_mk       |
| nama          |       | id (PK)            |       | nama_mk       |
| password      |       | tanggal_ambil      |       | sks           |
+---------------+       +--------------------+       +---------------+
