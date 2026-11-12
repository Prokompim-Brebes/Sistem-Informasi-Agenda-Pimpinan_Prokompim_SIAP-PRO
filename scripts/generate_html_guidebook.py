"""
Script untuk menghasilkan Buku Panduan SIAP-PRO dalam format HTML Siap Cetak (A4 Portrait)
Sesuai standar tata naskah dinas resmi:
Margin: Kiri 3.5cm, Kanan 2.5cm, Atas 3.0cm, Bawah 3.0cm
Font: Arial 11pt, spasi 1.15, text-align: justify
"""

import os

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Buku Panduan Pengguna SIAP-PRO — Pemkab Brebes</title>
  <style>
    @page {
      size: A4 portrait;
      margin-left: 3.5cm;
      margin-right: 2.5cm;
      margin-top: 3.0cm;
      margin-bottom: 3.0cm;
    }
    @media print {
      body {
        margin: 0;
        padding: 0;
        background: transparent;
      }
      .no-print {
        display: none !important;
      }
      .page-break {
        page-break-after: always;
        break-after: page;
      }
    }
    body {
      font-family: Arial, Helvetica, sans-serif;
      font-size: 11pt;
      line-height: 1.15;
      color: #0f172a;
      text-align: justify;
      background-color: #f1f5f9;
      margin: 0;
      padding: 20px;
    }
    .document-page {
      background: #ffffff;
      max-width: 21cm;
      margin: 0 auto 30px auto;
      padding: 3.0cm 2.5cm 3.0cm 3.5cm;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
      box-sizing: border-box;
      min-height: 29.7cm;
    }
    @media print {
      .document-page {
        max-width: none;
        margin: 0;
        padding: 0;
        box-shadow: none;
        min-height: auto;
      }
    }
    .header-bar {
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 6px;
      margin-bottom: 24px;
      font-size: 8.5pt;
      color: #64748b;
      text-align: right;
    }
    .footer-bar {
      border-top: 1px solid #cbd5e1;
      padding-top: 6px;
      margin-top: 30px;
      font-size: 8.5pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
    }
    .cover-header {
      text-align: center;
      margin-bottom: 30px;
    }
    .cover-title {
      color: #1e3a8a;
      font-size: 18pt;
      font-weight: bold;
      margin: 4px 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .cover-subtitle {
      color: #1e3a8a;
      font-size: 14pt;
      font-weight: bold;
      margin: 4px 0;
    }
    .cover-divider {
      border: 0;
      height: 2px;
      background: #1e3a8a;
      margin: 20px 0 40px 0;
    }
    .main-title {
      text-align: center;
      margin: 60px 0;
    }
    .main-title h1 {
      font-size: 22pt;
      color: #1e3a8a;
      margin-bottom: 12px;
      font-weight: 800;
    }
    .main-title h2 {
      font-size: 15pt;
      color: #0f172a;
      margin-bottom: 8px;
      font-weight: 700;
    }
    .main-title .badge {
      font-size: 12pt;
      color: #475569;
      font-style: italic;
      margin-top: 12px;
      display: block;
    }
    .cover-footer {
      text-align: center;
      margin-top: 100px;
      font-size: 10.5pt;
      color: #334155;
    }
    h1 {
      font-size: 16pt;
      font-weight: bold;
      color: #1e3a8a;
      margin-top: 24pt;
      margin-bottom: 10pt;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 4pt;
      page-break-after: avoid;
    }
    h2 {
      font-size: 13pt;
      font-weight: bold;
      color: #1e3a8a;
      margin-top: 16pt;
      margin-bottom: 6pt;
      page-break-after: avoid;
    }
    h3 {
      font-size: 12pt;
      font-weight: bold;
      color: #0f172a;
      margin-top: 12pt;
      margin-bottom: 4pt;
      page-break-after: avoid;
    }
    p {
      margin-top: 0;
      margin-bottom: 8pt;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 12pt 0;
      font-size: 9.5pt;
      page-break-inside: avoid;
    }
    th {
      background-color: #1e3a8a;
      color: #ffffff;
      font-weight: bold;
      padding: 7pt 8pt;
      border: 1px solid #cbd5e1;
      text-align: center;
    }
    td {
      padding: 6pt 8pt;
      border: 1px solid #cbd5e1;
      vertical-align: top;
    }
    tr:nth-child(even) td {
      background-color: #f8fafc;
    }
    .callout-info {
      background-color: #eff6ff;
      border-left: 4px solid #1e3a8a;
      padding: 10pt 14pt;
      margin: 12pt 0;
      border-radius: 0 4px 4px 0;
      page-break-inside: avoid;
    }
    .callout-warning {
      background-color: #fef3c7;
      border-left: 4px solid #d97706;
      padding: 10pt 14pt;
      margin: 12pt 0;
      border-radius: 0 4px 4px 0;
      page-break-inside: avoid;
    }
    .callout-title {
      font-weight: bold;
      margin-bottom: 4pt;
      font-size: 10.5pt;
    }
    .callout-info .callout-title { color: #1e3a8a; }
    .callout-warning .callout-title { color: #b45309; }
    .code-box {
      background: #0f172a;
      color: #38bdf8;
      font-family: Consolas, monospace;
      padding: 10pt 12pt;
      border-radius: 4px;
      font-size: 9pt;
      word-break: break-all;
      margin: 8pt 0;
    }
    .toc-item {
      display: flex;
      justify-content: space-between;
      margin-bottom: 4pt;
      font-size: 10pt;
    }
    .toc-item.bold {
      font-weight: bold;
      color: #1e3a8a;
      margin-top: 8pt;
    }
    .print-btn-bar {
      max-width: 21cm;
      margin: 0 auto 16px auto;
      text-align: right;
    }
    .btn-print {
      background: #1e3a8a;
      color: #ffffff;
      border: none;
      padding: 10px 20px;
      font-size: 11pt;
      font-weight: bold;
      border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .btn-print:hover {
      background: #1e40af;
    }
  </style>
</head>
<body>

  <div class="print-btn-bar no-print">
    <button class="btn-print" onclick="window.print()">🖨️ Cetak / Simpan ke PDF (A4)</button>
  </div>

  <div class="document-page">
    <div class="cover-header">
      <div class="cover-title">Pemerintah Kabupaten Brebes</div>
      <div class="cover-subtitle">Sekretariat Daerah</div>
      <div class="cover-subtitle" style="font-size: 12pt; color: #334155;">Bagian Protokol dan Komunikasi Pimpinan</div>
      <hr class="cover-divider">
    </div>

    <div class="main-title">
      <h1>BUKU PANDUAN PENGGUNA</h1>
      <h2>SISTEM INFORMASI AGENDA PIMPINAN PROKOMPIM (SIAP-PRO)</h2>
      <span class="badge">Edisi Pembaruan Tahun 2026 • Versi 2.0</span>
      <p style="color: #64748b; font-size: 11pt; margin-top: 14px;">Buku Agenda Digital Terpusat Penatausahaan Kegiatan Pimpinan Daerah</p>
    </div>

    <div class="cover-footer">
      <p><strong>Bagian Protokol dan Komunikasi Pimpinan</strong><br>
      Sekretariat Daerah Kabupaten Brebes<br>
      Jl. Proklamasi No. 77, Brebes, Jawa Tengah 52212<br>
      <strong>Tahun 2026</strong></p>
    </div>
  </div>

  <div class="page-break"></div>

  <div class="document-page">
    <div class="header-bar">Pemerintah Kabupaten Brebes • Sekretariat Daerah • Bagian Prokompim</div>

    <h1>KATA PENGANTAR</h1>
    <p>Puji syukur senantiasa kita panjatkan ke hadirat Allah SWT, Tuhan Yang Maha Esa, atas tersusun dan diterbitkannya <strong>Buku Panduan Pengguna Sistem Informasi Agenda Pimpinan Prokompim (SIAP-PRO)</strong> ini.</p>
    <p>Buku panduan ini disusun sebagai pegangan kerja operasional sehari-hari bagi seluruh pegawai dan staf di lingkungan Bagian Protokol dan Komunikasi Pimpinan (Prokompim) Sekretariat Daerah Kabupaten Brebes. SIAP-PRO hadir untuk mentransformasi tata kelola agenda kerja pimpinan daerah yang sebelumnya banyak dikelola secara manual menjadi sistem digital yang terintegrasi, akurat, transparan, dan akuntabel.</p>
    <p>Dengan adanya SIAP-PRO, seluruh alur kegiatan pimpinan—mulai dari masuknya surat permohonan acara, penataan jadwal Bupati dan Wakil Bupati, penugasan petugas protokol, juru liput, hingga driver, serta pemantauan naskah sambutan dan kelengkapan dokumen Surat Pertanggungjawaban (SPJ)—dapat terpantau secara langsung (<em>real-time</em>).</p>
    <p>Panduan ini dirancang dengan tata naskah dinas resmi, visual yang bersih, dan bahasa yang sistematis agar seluruh staf dapat langsung mempraktikkannya dalam pelaksanaan tugas sehari-hari. Dokumen ini juga memuat panduan khusus bagi tenaga pendukung teknis (<em>IT Support</em>) guna menjamin kelangsungan operasional sistem.</p>
    <p>Semoga buku panduan ini memberikan manfaat nyata dalam mewujudkan pelayanan keprotokolan dan komunikasi pimpinan yang prima, profesional, dan berintegritas.</p>

    <div style="text-align: right; margin-top: 40px;">
      <p>Brebes, November 2026<br>
      <strong>Kepala Bagian Protokol dan Komunikasi Pimpinan</strong><br>
      Sekretariat Daerah Kabupaten Brebes<br><br><br><br>
      <strong>( ____________________________________ )</strong><br>
      NIP. ............................................................</p>
    </div>

    <div class="footer-bar">
      <span>Buku Panduan Pengguna SIAP-PRO — Edisi 2026</span>
      <span>Halaman i</span>
    </div>
  </div>

  <div class="page-break"></div>

  <div class="document-page">
    <div class="header-bar">Pemerintah Kabupaten Brebes • Sekretariat Daerah • Bagian Prokompim</div>

    <h1>DAFTAR ISI LENGKAP</h1>
    <div style="margin-top: 16px;">
      <div class="toc-item"><span>KATA PENGANTAR</span><span>i</span></div>
      <div class="toc-item"><span>DAFTAR ISI LENGKAP</span><span>ii</span></div>
      <div class="toc-item bold"><span>BAGIAN I — PANDUAN PENGGUNA OPERASIONAL (INTERNAL)</span><span></span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB I &nbsp;&nbsp;&nbsp;PENDAHULUAN & PENGENALAN SISTEM</span><span>1</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB II &nbsp;&nbsp;HAK AKSES DAN JENIS PENGGUNA</span><span>3</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB III &nbsp;CARA MASUK DAN KELUAR SISTEM (LOGIN & LOGOUT)</span><span>4</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB IV &nbsp;HALAMAN UTAMA (DASBOR EKSEKUTIF)</span><span>6</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB V &nbsp;&nbsp;KALENDER AGENDA KERJA</span><span>8</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB VI &nbsp;WORKSHEET (LEMBAR KERJA UTAMA)</span><span>9</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB VII DETAIL KEGIATAN & PENGELOLAAN BERKAS SPJ</span><span>14</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB VIII REKAPITULASI LAPORAN (EXCEL & PDF)</span><span>16</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB IX &nbsp;PENGELOLAAN DATA PETUGAS (MASTER PETUGAS)</span><span>17</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB X &nbsp;&nbsp;DATA INSTANSI PENYELENGGARA (LEADING SECTOR)</span><span>19</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB XI &nbsp;MANAJEMEN PENGGUNA (KHUSUS ADMINISTRATOR)</span><span>20</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB XII RIWAYAT AKTIVITAS SISTEM (AUDIT LOG)</span><span>21</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB XIII ALUR RESMI PERJALANAN STATUS KEGIATAN</span><span>22</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;DAFTAR ISTILAH & TANYA JAWAB (FAQ)</span><span>24</span></div>
      <div class="toc-item bold"><span>BAGIAN II — PANDUAN TEKNIS IT SUPPORT DAN PENGEMBANG SISTEM</span><span></span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB XIV INFORMASI AKUN PLATFORM DAN INFRASTRUKTUR</span><span>26</span></div>
      <div class="toc-item"><span>&nbsp;&nbsp;BAB XV &nbsp;PROSEDUR PENANGANAN KENDALA SISTEM (TROUBLESHOOTING)</span><span>29</span></div>
      <div class="toc-item bold"><span>PENUTUP</span><span>31</span></div>
    </div>

    <div class="footer-bar">
      <span>Buku Panduan Pengguna SIAP-PRO — Edisi 2026</span>
      <span>Halaman ii</span>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- ISI BAB I - III -->
  <div class="document-page">
    <div class="header-bar">Pemerintah Kabupaten Brebes • Sekretariat Daerah • Bagian Prokompim</div>

    <div style="text-align: center; margin-bottom: 24px;">
      <p style="color: #64748b; font-weight: bold; margin: 0;">BAGIAN I</p>
      <h2 style="color: #1e3a8a; margin: 2px 0 16px 0;">PANDUAN PENGGUNA OPERASIONAL (INTERNAL)</h2>
    </div>

    <h1>BAB I — PENDAHULUAN & PENGENALAN SISTEM</h1>
    <h2>1.1 Mengenal Aplikasi SIAP-PRO</h2>
    <p><strong>SIAP-PRO (Sistem Informasi Agenda Pimpinan Prokompim)</strong> adalah aplikasi berbasis web yang dirancang khusus untuk mendukung kelancaran pelaksanaan tugas Bagian Protokol dan Komunikasi Pimpinan Sekretariat Daerah Kabupaten Brebes. Sistem ini berfungsi sebagai buku agenda kerja digital terpusat yang menggantikan tata kelola administrasi manual dan pencatatan yang sebelumnya tersebar di berbagai saluran tidak resmi seperti grup pesan instan (WhatsApp), lembaran disposisi fisik, dan berkas spreadsheet lokal.</p>
    <p>Dengan SIAP-PRO, seluruh rangkaian kegiatan pimpinan daerah—Bupati, Wakil Bupati, Sekretaris Daerah, maupun pejabat yang mewakili—dikelola dalam satu pangkalan data yang terpadu, mutakhir, dan dapat diakses bersama secara aman oleh seluruh pemangku kepentingan di lingkungan Bagian Prokompim.</p>

    <h2>1.2 Manfaat dan Kemudahan Utama</h2>
    <p>Penerapan aplikasi SIAP-PRO memberikan berbagai kemanfaatan strategis dan operasional, antara lain:</p>
    <ul>
      <li><strong>Mencegah Jadwal Ganda (<em>Conflict Scheduling</em>):</strong> Memastikan pimpinan tidak terjadwal pada dua atau lebih agenda di lokasi berbeda pada waktu yang bersamaan.</li>
      <li><strong>Distribusi Penugasan yang Transparan:</strong> Memudahkan pembagian tugas bagi Petugas Protokol, Juru Liput, dan Pengemudi (Driver), serta memperjelas koordinator penanggung jawab di lapangan.</li>
      <li><strong>Pemantauan Kesiapan Naskah Sambutan:</strong> Memastikan ketersediaan teks sambutan, pidato, atau arahan pimpinan sebelum acara berlangsung melalui indikator status yang jelas.</li>
      <li><strong>Penyelesaian Berkas SPJ Tepat Waktu:</strong> Menyediakan daftar periksa (checklist) pemantauan 7 dokumen wajib Surat Pertanggungjawaban (SPJ) hingga tuntas 100%.</li>
      <li><strong>Rekapitulasi Pelaporan Instan:</strong> Menghasilkan laporan rekapitulasi agenda bulanan maupun tahunan dalam format resmi dokumen cetak (PDF) dan lembar kerja elektronik (Microsoft Excel) secara otomatis.</li>
      <li><strong>Audit dan Transparansi:</strong> Mencatat setiap riwayat penambahan, pengubahan, dan penghapusan data secara otomatis demi menjamin akuntabilitas penyelenggaraan administrasi pemerintahan.</li>
    </ul>

    <div class="footer-bar">
      <span>Buku Panduan Pengguna SIAP-PRO — Edisi 2026</span>
      <span>Halaman 1</span>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- ISI BAB II & III -->
  <div class="document-page">
    <div class="header-bar">Pemerintah Kabupaten Brebes • Sekretariat Daerah • Bagian Prokompim</div>

    <h1>BAB II — HAK AKSES DAN JENIS PENGGUNA</h1>
    <h2>2.1 Tiga Tingkatan Akun Pengguna</h2>
    <p>Guna menjamin keamanan sistem, integritas data, dan pemisahan tugas (<em>segregation of duties</em>), akun pengguna SIAP-PRO dibagi menjadi tiga tingkatan wewenang:</p>

    <table>
      <thead>
        <tr>
          <th style="width: 8%;">No.</th>
          <th style="width: 25%;">Tingkatan Akun</th>
          <th style="width: 20%;">Peran Sistem</th>
          <th>Deskripsi Wewenang</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="text-align: center;">1.</td>
          <td><strong>Administrator</strong></td>
          <td><code>ADMIN</code></td>
          <td>Pengelola teknis tertinggi dengan wewenang penuh atas seluruh fitur, termasuk pendaftaran, perbaikan, dan pengaturan hak akses pengguna lain.</td>
        </tr>
        <tr>
          <td style="text-align: center;">2.</td>
          <td><strong>Staf Prokompim</strong></td>
          <td><code>STAFF</code></td>
          <td>Pengguna operasional harian yang bertugas menginput acara, menugaskan personel, memperbarui status naskah sambutan, dan melengkapi dokumen SPJ.</td>
        </tr>
        <tr>
          <td style="text-align: center;">3.</td>
          <td><strong>Kepala Bagian</strong></td>
          <td><code>KEPALA_BAGIAN</code></td>
          <td>Pengguna eksekutif dengan hak pemantauan (<em>read-only</em>) dan pencetakan laporan resmi, tanpa akses untuk mengubah atau menghapus data kegiatan.</td>
        </tr>
      </tbody>
    </table>

    <h2>2.2 Matriks Wewenang dan Hak Akses</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 8%;">No.</th>
          <th>Modul / Fitur Sistem</th>
          <th style="width: 15%;">Admin</th>
          <th style="width: 15%;">Staf</th>
          <th style="width: 15%;">Kabag</th>
        </tr>
      </thead>
      <tbody>
        <tr><td style="text-align:center;">1.</td><td>Mengakses Dasbor Eksekutif</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td></tr>
        <tr><td style="text-align:center;">2.</td><td>Melihat Lembar Kerja (Worksheet)</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td></tr>
        <tr><td style="text-align:center;">3.</td><td>Menginput Kegiatan Baru</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">❌ Tidak</td></tr>
        <tr><td style="text-align:center;">4.</td><td>Mengubah Data Kegiatan</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">❌ Tidak</td></tr>
        <tr><td style="text-align:center;">5.</td><td>Menghapus Data Kegiatan</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">❌ Tidak</td></tr>
        <tr><td style="text-align:center;">6.</td><td>Mengelola Master Data Petugas</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">❌ Tidak</td></tr>
        <tr><td style="text-align:center;">7.</td><td>Mengelola Master Leading Sector</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">❌ Tidak</td></tr>
        <tr><td style="text-align:center;">8.</td><td>Mengelola Akun Pengguna (User Management)</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">❌ Tidak</td><td style="text-align:center;">❌ Tidak</td></tr>
        <tr><td style="text-align:center;">9.</td><td>Melihat Riwayat Aktivitas (Activity Log)</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td></tr>
        <tr><td style="text-align:center;">10.</td><td>Mengunduh Rekapitulasi Excel & Mencetak PDF</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td><td style="text-align:center;">✅ Ya</td></tr>
      </tbody>
    </table>

    <div class="footer-bar">
      <span>Buku Panduan Pengguna SIAP-PRO — Edisi 2026</span>
      <span>Halaman 3</span>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- BAB III & IV -->
  <div class="document-page">
    <div class="header-bar">Pemerintah Kabupaten Brebes • Sekretariat Daerah • Bagian Prokompim</div>

    <h1>BAB III — CARA MASUK DAN KELUAR SISTEM (LOGIN & LOGOUT)</h1>
    <h2>3.1 Kredensial Akun Administrator Utama</h2>
    <p>Untuk masuk ke aplikasi SIAP-PRO sebagai Administrator utama bagian, gunakan kredensial resmi berikut:</p>

    <table>
      <thead>
        <tr>
          <th style="width: 35%;">Parameter Masuk</th>
          <th>Nilai Pengaturan Resmi</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><strong>Alamat URL Aplikasi</strong></td><td>Sesuai tautan resmi SIAP-PRO yang telah ditetapkan</td></tr>
        <tr><td><strong>Username</strong></td><td><code>admin</code></td></tr>
        <tr><td><strong>Password</strong></td><td><code>prokompim</code></td></tr>
        <tr><td><strong>Tingkatan Hak Akses</strong></td><td>Administrator (<code>ADMIN</code>)</td></tr>
      </tbody>
    </table>

    <div class="callout-warning">
      <div class="callout-title">⚠️ PERHATIAN KEAMANAN ADMINISTRASI:</div>
      Kredensial di atas merupakan akun kedinasan Administrator internal SIAP-PRO. Jagalah kerahasiaan kata sandi dan jangan meninggalkan perangkat komputer dalam keadaan terbuka tanpa pengawasan.
    </div>

    <h2>3.2 Langkah-Langkah Masuk (Login)</h2>
    <ol>
      <li><strong>Membuka Peramban Web:</strong> Buka aplikasi peramban internet standar kedinasan (Google Chrome, Microsoft Edge, atau Mozilla Firefox) pada komputer kerja.</li>
      <li><strong>Mengakses Tautan SIAP-PRO:</strong> Masukkan alamat URL resmi aplikasi SIAP-PRO pada bilah alamat (<em>address bar</em>), lalu tekan tombol <strong>Enter</strong>.</li>
      <li><strong>Memasukkan Kredensial:</strong> Masukkan Username dan Password yang telah ditetapkan.</li>
      <li><strong>Eksekusi Masuk:</strong> Klik tombol biru bertuliskan <strong>Masuk</strong>. Sistem akan langsung mengarahkan pengguna ke Dasbor Eksekutif.</li>
    </ol>

    <h2>3.3 Langkah Keluar (Logout) yang Aman</h2>
    <p>Apabila komputer kerja digunakan secara bergantian, klik ikon <strong>Keluar / Logout</strong> di pojok kanan atas, lalu konfirmasi opsi <strong>Ya, Keluar</strong> untuk menutup sesi kerja dengan aman.</p>

    <div class="footer-bar">
      <span>Buku Panduan Pengguna SIAP-PRO — Edisi 2026</span>
      <span>Halaman 4</span>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- BAGIAN II TEKNIS IT SUPPORT -->
  <div class="document-page">
    <div class="header-bar">Pemerintah Kabupaten Brebes • Sekretariat Daerah • Bagian Prokompim</div>

    <div style="text-align: center; margin-bottom: 24px;">
      <p style="color: #64748b; font-weight: bold; margin: 0;">BAGIAN II</p>
      <h2 style="color: #1e3a8a; margin: 2px 0 16px 0;">PANDUAN TEKNIS IT SUPPORT DAN PENGEMBANG SISTEM</h2>
    </div>

    <div class="callout-warning">
      <div class="callout-title">🔒 INFORMASI TERBATAS / STRICTLY CONFIDENTIAL:</div>
      Bagian ini memuat informasi rahasia mengenai infrastruktur server, akun layanan cloud, dan kunci akses basis data (API Keys). Dokumen ini <strong>HANYA diperuntukkan bagi Tim IT Support, Tenaga Ahli IT, dan Pengembang Sistem</strong>. DILARANG disebarluaskan kepada pihak umum atau pengguna operasional biasa.
    </div>

    <h1>BAB XIV — INFORMASI AKUN PLATFORM DAN INFRASTRUKTUR</h1>
    <h2>14.1 Akun Google Master (Gmail Prokompim)</h2>
    <p>Akun Google kedinasan ini merupakan akun induk (<em>master account</em>) yang digunakan sebagai pusat autentikasi terpadu (<em>Single Sign-On / SSO</em>) untuk seluruh platform infrastruktur:</p>

    <table>
      <thead>
        <tr>
          <th style="width: 35%;">Parameter Kredensial</th>
          <th>Nilai Resmi</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><strong>Alamat Surel (Email)</strong></td><td><code>prokompimbrebes@gmail.com</code></td></tr>
        <tr><td><strong>Kata Sandi (Password)</strong></td><td><code>prokompimbrebes2026</code></td></tr>
        <tr><td><strong>Peruntukan Layanan</strong></td><td>Autentikasi SSO untuk Vercel, Supabase, dan penyimpanan Google Drive.</td></tr>
      </tbody>
    </table>

    <div class="callout-info">
      <div class="callout-title">ℹ️ LANGKAH PERTAMA PENANGANAN KENDALA:</div>
      Sebelum mengakses Vercel atau Supabase, pastikan Anda telah melakukan <em>Login</em> terlebih dahulu ke akun Gmail di atas pada peramban web yang Anda gunakan.
    </div>

    <h2>14.2 Platform Hosting dan Deployment (Vercel)</h2>
    <p><strong>Akses Vercel diperlukan ketika:</strong> Aplikasi web SIAP-PRO sama sekali tidak dapat diakses oleh pengguna (<em>website down / crash</em>).</p>
    <p><strong>Prosedur Masuk Vercel:</strong></p>
    <ol>
      <li>Pastikan peramban telah masuk ke akun Gmail <code>prokompimbrebes@gmail.com</code>;</li>
      <li>Buka peramban dan akses alamat: <strong>https://vercel.com/</strong>;</li>
      <li>Klik tombol <strong>Log In</strong> &gt; pilih <strong>Continue with Google</strong>;</li>
      <li>Pilih akun <code>prokompimbrebes@gmail.com</code>;</li>
      <li>Dasbor Vercel terbuka. Buka tab <strong>Deployments</strong> untuk memeriksa log kesalahan server (<em>runtime logs</em>).</li>
    </ol>

    <h2>14.3 Platform Basis Data (Supabase PostgreSQL)</h2>
    <p><strong>Akses Supabase diperlukan ketika:</strong> Aplikasi web dapat dibuka normal, namun data kegiatan tidak muncul, daftar tabel kosong, atau gagal menyimpan data baru.</p>

    <table>
      <thead>
        <tr>
          <th style="width: 40%;">Parameter Kredensial Supabase</th>
          <th>Nilai Konfigurasi</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><strong>Alamat Akses</strong></td><td>https://supabase.com/</td></tr>
        <tr><td><strong>Email Login</strong></td><td><code>prokompimbrebes@gmail.com</code></td></tr>
        <tr><td><strong>Password Login Akun</strong></td><td><code>Prokompimbrebes2026!</code></td></tr>
        <tr><td><strong>Password Basis Data (PostgreSQL)</strong></td><td><code>Prokompimbrebes2026!</code></td></tr>
        <tr><td><strong>Wilayah Server</strong></td><td>aws-0-ap-southeast-1 (Singapura)</td></tr>
      </tbody>
    </table>

    <h2>14.4 Repositori Kode Sumber (GitHub)</h2>
    <table>
      <thead>
        <tr>
          <th style="width: 40%;">Parameter Kredensial GitHub</th>
          <th>Nilai Resmi</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><strong>Alamat Repositori</strong></td><td>https://github.com/</td></tr>
        <tr><td><strong>Username</strong></td><td><code>Prokompim-Brebes</code></td></tr>
        <tr><td><strong>Email Terdaftar</strong></td><td><code>prokompimbrebes@gmail.com</code></td></tr>
        <tr><td><strong>Password</strong></td><td><code>prokompimbrebes2026</code></td></tr>
      </tbody>
    </table>

    <h2>14.5 Konfigurasi Variabel Lingkungan dan API Key</h2>
    <p>Variabel lingkungan berikut wajib terpasang pada pengaturan proyek di Vercel dan file <code>.env</code> lokal:</p>

    <p><strong>1. DATABASE_URL (Pooler Transaksi):</strong></p>
    <div class="code-box">DATABASE_URL="postgresql://postgres.obhnufrsrjjuwyywrlkf:6SRPOrw6awJDUHxm@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true"</div>

    <p><strong>2. DIRECT_URL (Koneksi Langsung Migrasi):</strong></p>
    <div class="code-box">DIRECT_URL="postgresql://postgres.obhnufrsrjjuwyywrlkf:6SRPOrw6awJDUHxm@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"</div>

    <p><strong>3. AUTH_SECRET (Kunci Enkripsi Token JWT):</strong></p>
    <div class="code-box">AUTH_SECRET="61e65a8c4ac2ed8c8f90ea648dd0ca3d"</div>

    <div class="footer-bar">
      <span>Buku Panduan Pengguna SIAP-PRO — Edisi 2026</span>
      <span>Halaman 26</span>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- BAB XV & PENUTUP -->
  <div class="document-page">
    <div class="header-bar">Pemerintah Kabupaten Brebes • Sekretariat Daerah • Bagian Prokompim</div>

    <h1>BAB XV — PROSEDUR PENANGANAN KENDALA SISTEM (TROUBLESHOOTING)</h1>
    <h2>15.1 Kasus A: Aplikasi Web Tidak Dapat Diakses (Down / Crash)</h2>
    <ol>
      <li>Masuk ke dasbor <strong>Vercel</strong> menggunakan akun Google <code>prokompimbrebes@gmail.com</code>;</li>
      <li>Periksa versi deployment teratas yang bertanda merah (<em>Failed</em>);</li>
      <li>Buka <strong>Build Logs</strong> atau <strong>Runtime Logs</strong> untuk mengidentifikasi kesalahan baris program;</li>
      <li>Lakukan perbaikan kode pada repositori GitHub melalui akun <code>Prokompim-Brebes</code>, lalu lakukan <code>git push origin main</code> untuk mengaktifkan <em>re-deploy</em> otomatis.</li>
    </ol>

    <h2>15.2 Kasus B: Aplikasi Dapat Diakses Namun Data Kosong / Hilang</h2>
    <ol>
      <li>Masuk ke dasbor <strong>Supabase</strong> menggunakan email <code>prokompimbrebes@gmail.com</code> dan password <code>Prokompimbrebes2026!</code>;</li>
      <li>Periksa status proyek pada dasbor Supabase. Apabila berstatus <strong>Paused</strong>, klik tombol <strong>Restore Project</strong> dan tunggu 2-3 menit hingga basis data aktif kembali;</li>
      <li>Buka menu <strong>Table Editor</strong> di bilah navigasi kiri, pastikan data pada tabel <code>kegiatan</code> dan <code>petugas</code> masih utuh;</li>
      <li>Pastikan konfigurasi string koneksi basis data di Vercel tidak mengalami perubahan.</li>
    </ol>

    <h1>PENUTUP</h1>
    <p>Buku Panduan Pengguna Sistem Informasi Agenda Pimpinan Prokompim (SIAP-PRO) ini disusun dengan komitmen penuh untuk meningkatkan profesionalisme, efisiensi, dan akuntabilitas penatausahaan keprotokolan di lingkungan Pemerintah Kabupaten Brebes.</p>
    <p>Dengan pemahaman yang menyeluruh atas seluruh panduan operasional maupun teknis yang tercantum dalam dokumen ini, diharapkan seluruh jajaran di Bagian Protokol dan Komunikasi Pimpinan serta tenaga pendukung sistem dapat bersinergi secara optimal dalam menyukseskan pelayanan agenda pimpinan daerah.</p>

    <div style="text-align: center; margin-top: 50px;">
      <p>Ditetapkan di Brebes<br>pada tanggal 12 November 2026</p>
      <p style="color: #1e3a8a; font-weight: bold; font-size: 12pt;">
        BAGIAN PROTOKOL DAN KOMUNIKASI PIMPINAN<br>
        SEKRETARIAT DAERAH KABUPATEN BREBES
      </p>
    </div>

    <div class="footer-bar">
      <span>Buku Panduan Pengguna SIAP-PRO — Edisi 2026</span>
      <span>Halaman 31</span>
    </div>
  </div>

</body>
</html>
"""

output_path = os.path.join("docs", "BUKU_PANDUAN_SIAP_PRO.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML successfully generated at: {output_path}")
