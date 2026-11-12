# Progress 12 November 2026 — Penyusunan Buku Panduan Resmi SIAP-PRO Standar Tata Naskah Dinas & Panduan Teknis Infrastruktur

> **Status: ✅ Selesai Penuh (Buku Panduan Pengguna SIAP-PRO Versi 2.0 Berhasil Disusun Komprehensif dalam Format Markdown, Microsoft Word DOCX Standar Kedinasan A4, dan HTML Siap Cetak PDF; Dilengkapi Kredensial Resmi Administrator & Panduan Infrastruktur IT Support untuk Serah Terima Sistem)**

---

## 📋 Ringkasan Progres Hari Ini

Hari ini diselesaikan penyusunan dokumen dokumentasi resmi kepemerintahan berupa **Buku Panduan Pengguna Sistem Informasi Agenda Pimpinan Prokompim (SIAP-PRO) Edisi 2026 • Versi 2.0**. Dokumen ini dirancang dengan mematuhi prinsip tata naskah dinas instansi pemerintah Republik Indonesia serta memisahkan secara tegas panduan operasional pengguna internal dan panduan teknis infrastruktur untuk *IT Support* / pengembang mendatang.

| # | Modul / Dokumen | Deskripsi Pekerjaan | Status |
|---|-----------------|---------------------|--------|
| 1 | **Buku Panduan Master Markdown** (`SIAP-PRO_Guidebook.md` & `docs/BUKU_PANDUAN_SIAP_PRO.md`) | Menyusun naskah panduan lengkap yang mencakup 13 Bab materi pengguna operasional, FAQ, alur kerja diagram Mermaid, serta Bagian Khusus IT Support & Developer. | ✅ Selesai |
| 2 | **Format Dokumen Word Kedinasan** (`docs/BUKU PANDUAN SIAP-PRO.docx`) | Mengenerasi berkas Microsoft Word resmi dengan spesifikasi kertas A4 Portrait, margin standar (Kiri 3,5 cm, Kanan 2,5 cm, Atas 3 cm, Bawah 3 cm), tipografi Arial 11 pt spasi 1,15 *justify*, judul bab 16 pt *Navy*, subbab 13 pt, serta tabel berbingkai rapi. | ✅ Selesai |
| 3 | **Format HTML Siap Cetak A4 / PDF** (`docs/BUKU_PANDUAN_SIAP_PRO.html`) | Membuat berkas HTML responsif berstandar cetak `@page` CSS A4 Portrait. Memungkinkan siapa pun membuka berkas di peramban dan langsung menekan `Ctrl + P` untuk mencetak atau menyimpan dokumen menjadi PDF resmi berkualitas tinggi. | ✅ Selesai |
| 4 | **Pencatatan Kredensial Administrator Internal** | Mendokumentasikan akun login resmi Administrator operasional sistem (`username: admin`, `password: prokompim`) dengan hak akses penuh pengelolaan pengguna dan data agenda. | ✅ Selesai |
| 5 | **Panduan Infrastruktur & Troubleshooting IT Support** | Menyusun prosedur penanganan kendala server untuk tim teknis: autentikasi Google SSO (`prokompimbrebes@gmail.com`), pemecahan masalah *website down* di Vercel, pemecahan masalah *data kosong / database paused* di Supabase PostgreSQL, repositori GitHub, serta inventarisasi *Environment Variables* / API Key. | ✅ Selesai |
| 6 | **Skrip Otomasi Pembangun Dokumen** (`scripts/generate_guidebook.py` & `scripts/generate_html_guidebook.py`) | Membangun skrip Python untuk meregenerasi dokumen DOCX dan HTML secara otomatis apabila di kemudian hari terdapat pembaruan materi. | ✅ Selesai |

---

## 🏛️ Rincian Struktur Buku Panduan SIAP-PRO (Versi 2.0)

Buku panduan disusun secara modular ke dalam dua bagian utama demi menjamin keamanan data dan kemudahan pembacaan:

### BAGIAN I — PANDUAN PENGGUNA OPERASIONAL (INTERNAL)
Diperuntukkan bagi staf pelaksana, operator data, dan pimpinan bagian:
- **BAB I: Pendahuluan & Pengenalan Sistem** — Latar belakang, manfaat eliminasi jadwal ganda, dan ruang lingkup SPBE.
- **BAB II: Hak Akses dan Jenis Pengguna** — Matriks wewenang 3 peran: Administrator (`ADMIN`), Staf Prokompim (`STAFF`), dan Kepala Bagian (`KEPALA_BAGIAN` - *read only*).
- **BAB III: Cara Masuk dan Keluar Sistem (Login & Logout)** — Informasi login Admin (`admin` / `prokompim`), langkah login aman, dan penanganan lupa kata sandi.
- **BAB IV: Halaman Utama (Dasbor Eksekutif)** — 4 kartu angka kunci, grafik bulanan 12 bulan, panel 5 kegiatan terdekat, progres SPJ, dan penggunaan filter tahun.
- **BAB V: Kalender Agenda Kerja** — Membaca grid kalender, kode warna status (Ungu, Kuning, Hijau, Biru), dan *pop-up* informasi cepat.
- **BAB VI: Worksheet (Lembar Kerja Utama)** — Penjelasan 22 kolom data, pencarian dan filter bertingkat, penambahan agenda baru, penugasan petugas protokol/liputan/driver yang fleksibel, fitur *Semua Crew*, serta ekspor lembar kerja ke Excel.
- **BAB VII: Detail Kegiatan & Pengelolaan Berkas SPJ** — Pemantauan 7 dokumen wajib SPJ (Surat Tugas, Undangan, Sambutan, Foto, Video, Berkas SPJ, Laporan Akhir), pengisian link Google Drive, *Progress Bar* 0–100%, dan riwayat perubahan data.
- **BAB VIII: Rekapitulasi Laporan (Excel & PDF)** — Penyesuaian kolom tampil, unduh file `.xlsx`, dan cetak pratinjau kedinasan.
- **BAB IX: Pengelolaan Data Petugas (Master Petugas)** — Manajemen tim Protokol, Liputan, Driver, dan kebijakan nonaktifkan (bukan hapus) untuk menjaga keutuhan laporan lama.
- **BAB X: Data Instansi Penyelenggara (Leading Sector)** — Master data OPD, Forkopimda, instansi vertikal, dan kecamatan.
- **BAB XI: Manajemen Pengguna (Khusus Administrator)** — Pembuatan akun baru, mutasi peran, dan reset kata sandi staf.
- **BAB XII: Riwayat Aktivitas Sistem (Audit Log)** — Pemantauan jejak audit perubahan data (`CREATE`, `UPDATE`, `DELETE`).
- **BAB XIII: Alur Resmi Perjalanan Status Kegiatan** — Diagram alur 4 tahap acara (*Acara Masuk ➔ Menunggu Penugasan ➔ Kegiatan Selesai ➔ SPJ Selesai*).
- **Daftar Istilah & FAQ** — Penjelasan terminologi (PIC, SPPD, Dresscode, Progress Bar) dan solusi pertanyaan lazim staf.

---

### BAGIAN II — PANDUAN TEKNIS IT SUPPORT DAN PENGEMBANG SISTEM (CONFIDENTIAL)
Diperuntukkan khusus bagi Administrator IT dan pengembang pemelihara sistem:
- **BAB XIV: Informasi Akun Platform dan Infrastruktur**:
  1. **Akun Google Master (Gmail Prokompim)**:
     - Email: `prokompimbrebes@gmail.com`
     - Password: `prokompimbrebes2026`
     - Peran: Akun *Single Sign-On* (SSO) untuk otentikasi Vercel, Supabase, dan folder Google Drive.
  2. **Platform Hosting (Vercel)**:
     - Tautan: `https://vercel.com/` (Login via *Continue with Google*).
     - Prosedur pemantauan *Deployments* dan *Runtime Logs* saat web tidak dapat diakses (*down*).
  3. **Platform Basis Data (Supabase PostgreSQL)**:
     - Tautan: `https://supabase.com/`
     - Email: `prokompimbrebes@gmail.com` | Password Akun & DB: `Prokompimbrebes2026!`
     - Wilayah Server: `aws-0-ap-southeast-1` (Singapura).
     - Prosedur *Restore Project* jika basis data *paused* serta verifikasi tabel via *Table Editor*.
  4. **Repositori Kode Sumber (GitHub)**:
     - Tautan: `https://github.com/` | Username: `Prokompim-Brebes`
     - Email: `prokompimbrebes@gmail.com` | Password: `prokompimbrebes2026`
  5. **Variabel Lingkungan & API Key Produksi**:
     - `DATABASE_URL`: Koneksi pooler transaksi port 6543 (PgBouncer).
     - `DIRECT_URL`: Koneksi langsung port 5432 untuk migrasi skema Prisma.
     - `AUTH_SECRET`: Kunci enkripsi token sesi JWT 32-karakter.
- **BAB XV: Prosedur Penanganan Kendala Sistem (Troubleshooting)**:
  - Penanganan Kasus A (Aplikasi *Down / Crash* / Error 502).
  - Penanganan Kasus B (Aplikasi dapat dibuka namun data hilang/kosong).
  - Standar Operasional Prosedur (SOP) pencadangan basis data berkala (*Database Backup Dump*).

---

## 📁 Berkas Luaran yang Dihasilkan

1. [`docs/BUKU_PANDUAN_SIAP_PRO.md`](file:///D:/Rafa/Projek/SIAP-PRO_Sistem%20Informasi%20Agenda%20Pimpinan%20Prokompim/sistem-spj-protokom/docs/BUKU_PANDUAN_SIAP_PRO.md) — Naskah master panduan Markdown.
2. [`docs/BUKU PANDUAN SIAP-PRO.docx`](file:///D:/Rafa/Projek/SIAP-PRO_Sistem%20Informasi%20Agenda%20Pimpinan%20Prokompim/sistem-spj-protokom/docs/BUKU%20PANDUAN%20SIAP-PRO.docx) — Berkas Microsoft Word resmi siap cetak / arsip kedinasan.
3. [`docs/BUKU PANDUAN SIAP-PRO_backup.docx`](file:///D:/Rafa/Projek/SIAP-PRO_Sistem%20Informasi%20Agenda%20Pimpinan%20Prokompim/sistem-spj-protokom/docs/BUKU%20PANDUAN%20SIAP-PRO_backup.docx) — Salinan cadangan versi dokumen sebelumnya.
4. [`docs/BUKU_PANDUAN_SIAP_PRO.html`](file:///D:/Rafa/Projek/SIAP-PRO_Sistem%20Informasi%20Agenda%20Pimpinan%20Prokompim/sistem-spj-protokom/docs/BUKU_PANDUAN_SIAP_PRO.html) — Berkas pratinjau cetak A4 instan (bisa di-*Save as PDF* langsung dari browser).
5. [`scripts/generate_guidebook.py`](file:///D:/Rafa/Projek/SIAP-PRO_Sistem%20Informasi%20Agenda%20Pimpinan%20Prokompim/sistem-spj-protokom/scripts/generate_guidebook.py) — Skrip Python pembuat berkas DOCX.
6. [`scripts/generate_html_guidebook.py`](file:///D:/Rafa/Projek/SIAP-PRO_Sistem%20Informasi%20Agenda%20Pimpinan%20Prokompim/sistem-spj-protokom/scripts/generate_html_guidebook.py) — Skrip Python pembuat berkas HTML.

---

## 🎯 Nilai Tambah & Dampak Positif
1. **Standarisasi Operasional Kedinasan**: Staf dan pimpinan Bagian Prokompim Setda Brebes memiliki buku pegangan kerja yang baku, terstruktur, dan tidak bergantung pada instruksi lisan.
2. **Kesiapan Serah Terima Jabatan & Magang**: Seluruh dokumentasi teknis, kredensial master, serta langkah-langkah *troubleshooting* tersusun rapi, menjamin keberlanjutan (*sustainability*) sistem SIAP-PRO di masa mendatang tanpa risiko kehilangan kendali teknis.
