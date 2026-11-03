# Progress 03 November 2026 - Fitur Pemilihan Tahun & Visualisasi Grafik 12 Bulan Dashboard

## Latar Belakang
Berdasarkan evaluasi dan feedback presentasi laporan pimpinan:
1. **Visualisasi Grafik Bulanan**: Grafik kegiatan bulanan sebelumnya menggunakan jendela geser 6 bulan (3 bulan lalu dan 3 bulan ke depan). Feedback menghendaki visualisasi langsung menampilkan **12 bulan penuh (Januari s/d Desember)** dalam satu tahun kalender agar sebaran agenda tahunan terlihat menyeluruh.
2. **Fleksibilitas Analisis Tahunan**: Diperlukan fitur pemilihan tahun (filter tahun) yang memungkinkan pengguna meninjau grafik bulanan dan kartu statistik tahunan pada tahun tertentu (misal: 2026, 2027, 2028, dst.).

---

## Rincian Implementasi

### 1. Komponen Pemilihan Tahun (`DashboardYearSelect`)
- **File**: `src/app/(protected)/dashboard/dashboard-year-select.tsx`
- **Tipe**: Client Component (`use client`)
- **Fitur**:
  - Menggunakan React 19 `useTransition` dan Next.js `useRouter` untuk update parameter URL `?tahun=YYYY` secara mulus tanpa *full page reload*.
  - Menampilkan indikator loading animasi spinner (`Loader2`) saat transisi server component sedang berjalan.
  - Dropdown styling konsisten dengan UI SIAP-PRO (warna navy, border-app, rounded-xl, shadow-sm).
  - Ditempatkan pada 2 posisi strategis:
    - Di header ringkasan kegiatan (atas kartu statistik).
    - Di header kartu grafik bulanan.

### 2. Visualisasi Grafik 12 Bulan Penuh (`DashboardCharts`)
- **File**: `src/app/(protected)/dashboard/dashboard-charts.tsx`
- **Fitur**:
  - Menampilkan 12 batang bar secara lengkap (`Jan`, `Feb`, `Mar`, `Apr`, `Mei`, `Jun`, `Jul`, `Agu`, `Sep`, `Okt`, `Nov`, `Des`) dengan `interval={0}` pada X-Axis sehingga semua label bulan selalu tampil rapi.
  - Tooltip informatif menampilkan nama bulan lengkap beserta tahun (contoh: `Januari 2026: 15 kegiatan`).
  - Empty state elegan jika tahun yang dipilih belum memiliki data agenda yang tercatat.

### 3. Logika Server & Sinkronisasi Tahunan (`DashboardPage`)
- **File**: `src/app/(protected)/dashboard/page.tsx`
- **Fitur**:
  - **Dinamis Opsi Tahun**: Memanfaatkan agregasi database `prisma.kegiatan.aggregate({ _min: { tanggal: true }, _max: { tanggal: true } })` digabung dengan tahun berjalan. Jika ke depannya ada input kegiatan di tahun 2027 atau 2028, opsi tahun akan otomatis muncul di dropdown tanpa perlu perubahan kode.
  - **Filter Rentang Waktu 1 Tahun**: Menggunakan rentang waktu UTC/WIB lengkap dari 1 Januari `00:00:00` sampai 31 Desember `23:59:59` untuk tahun terpilih.
  - **Kartu Dinamis `Kegiatan {selectedYear}`**: Kartu ke-4 menyesuaikan label dan nilai total kegiatan serta subteks jumlah yang telah terlaksana untuk tahun terpilih.
  - **Sinkronisasi Progress Dokumen & Top Sektor**: Data dokumen SPJ dan leading sector juga terfilter spesifik mengikuti tahun yang dipilih.
  - **Optimasi Next.js Image**: Menyesuaikan `quality={75}` pada foto gedung KPT untuk memenuhi standar Next.js 15+ tanpa peringatan terminal.

---

## Verifikasi & Pengujian
- **TypeScript Check**: `npx tsc --noEmit` lolos 100% tanpa error.
- **Production Build**: `npm run build` sukses mengompilasi seluruh rute, termasuk rute dinamis `/dashboard`.
