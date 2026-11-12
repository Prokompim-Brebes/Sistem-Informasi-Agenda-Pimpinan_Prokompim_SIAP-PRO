"""
Script untuk menghasilkan Buku Panduan Resmi SIAP-PRO dalam format DOCX dan HTML
sesuai standar Tata Naskah Dinas Instansi Pemerintah:
- Ukuran: A4 Portrait (21 x 29.7 cm)
- Margin: Kiri 3.5 cm, Kanan 2.5 cm, Atas 3.0 cm, Bawah 3.0 cm
- Font: Arial 11 pt, Line Spacing 1.15, Justify
- Heading 1: 16 pt Bold Navy (#1E3A8A)
- Heading 2: 13 pt Bold Navy
- Heading 3: 12 pt Bold
- Tabel formal dengan header Navy & border bersih
"""

import os
import docx
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_docx(output_path):
    doc = docx.Document()
    
    # Page setup A4
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(3.5)
        section.right_margin = Cm(2.5)
        section.top_margin = Cm(3.0)
        section.bottom_margin = Cm(3.0)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Pemerintah Kabupaten Brebes • Sekretariat Daerah • Bagian Prokompim")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun = fp.add_run("Buku Panduan Pengguna SIAP-PRO — Edisi 2026 (Versi 2.0)")
        frun.font.name = "Arial"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)

    # Base Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(15, 23, 42)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    NAVY = RGBColor(30, 58, 138)      # #1E3A8A
    DARK_BLUE = RGBColor(15, 23, 42)  # #0F172A
    MUTED = RGBColor(71, 85, 105)     # #475569

    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, color=DARK_BLUE, size=11):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Arial'
        run.font.size = Pt(size)
        run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(16)
        run.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(13)
        run.font.color.rgb = NAVY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.font.color.rgb = DARK_BLUE
        return p

    def add_callout(title, text, is_warning=False):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        bg = "FEF3C7" if is_warning else "EFF6FF"
        border_col = "D97706" if is_warning else "1E3A8A"
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_col}"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_title = p.add_run(title + "\n")
        r_title.bold = True
        r_title.font.name = "Arial"
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = RGBColor(180, 83, 9) if is_warning else NAVY
        
        r_text = p.add_run(text)
        r_text.font.name = "Arial"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = DARK_BLUE
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_custom_table(headers, rows, col_widths=None):
        table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="CBD5E1", sz="4")
        
        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            cell = hdr_cells[i]
            cell.text = header_text
            set_cell_background(cell, "1E3A8A")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.bold = True
                r.font.name = "Arial"
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(255, 255, 255)
        
        # Data Rows
        for r_idx, row_data in enumerate(rows):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.text = str(val)
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                if c_idx == 0 and len(str(val)) <= 4:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = DARK_BLUE
                    
        # Apply Column Widths if provided
        if col_widths and len(col_widths) == len(headers):
            for row in table.rows:
                for c_idx, w in enumerate(col_widths):
                    row.cells[c_idx].width = Cm(w)
                    
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ------------------ COVER PAGE ------------------
    add_p("PEMERINTAH KABUPATEN BREBES", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=15, color=NAVY, space_after=2)
    add_p("SEKRETARIAT DAERAH", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, color=NAVY, space_after=2)
    add_p("BAGIAN PROTOKOL DAN KOMUNIKASI PIMPINAN", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13, color=NAVY, space_after=18)
    
    add_p("_______________________________________________________________________________", align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED, space_after=24)
    
    add_p("BUKU PANDUAN PENGGUNA", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=20, color=NAVY, space_after=6)
    add_p("SISTEM INFORMASI AGENDA PIMPINAN PROKOMPIM", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, color=DARK_BLUE, space_after=4)
    add_p("(SIAP-PRO)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=18, color=NAVY, space_after=12)
    
    add_p("Edisi Pembaruan Tahun 2026 • Versi 2.0", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12, color=MUTED, space_after=6)
    add_p("Buku Agenda Digital Terpusat Penatausahaan Kegiatan Pimpinan Daerah", align=WD_ALIGN_PARAGRAPH.CENTER, size=11, color=MUTED, space_after=40)
    
    add_p("_______________________________________________________________________________", align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED, space_after=30)
    
    add_p("Bagian Protokol dan Komunikasi Pimpinan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=11, color=DARK_BLUE, space_after=2)
    add_p("Sekretariat Daerah Kabupaten Brebes", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=11, color=DARK_BLUE, space_after=2)
    add_p("Jl. Proklamasi No. 77, Brebes, Jawa Tengah 52212", align=WD_ALIGN_PARAGRAPH.CENTER, size=10, color=MUTED, space_after=2)
    add_p("Tahun 2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=11, color=NAVY, space_after=0)
    
    doc.add_page_break()

    # ------------------ KATA PENGANTAR ------------------
    add_h1("KATA PENGANTAR")
    add_p("Puji syukur senantiasa kita panjatkan ke hadirat Allah SWT, Tuhan Yang Maha Esa, atas tersusun dan diterbitkannya Buku Panduan Pengguna Sistem Informasi Agenda Pimpinan Prokompim (SIAP-PRO) ini.")
    add_p("Buku panduan ini disusun sebagai pegangan kerja operasional sehari-hari bagi seluruh pegawai dan staf di lingkungan Bagian Protokol dan Komunikasi Pimpinan (Prokompim) Sekretariat Daerah Kabupaten Brebes. SIAP-PRO hadir untuk mentransformasi tata kelola agenda kerja pimpinan daerah yang sebelumnya banyak dikelola secara manual menjadi sistem digital yang terintegrasi, akurat, transparan, dan akuntabel.")
    add_p("Dengan adanya SIAP-PRO, seluruh alur kegiatan pimpinan—mulai dari masuknya surat permohonan acara, penataan jadwal Bupati dan Wakil Bupati, penugasan petugas protokol, juru liput, hingga driver, serta pemantauan naskah sambutan dan kelengkapan dokumen Surat Pertanggungjawaban (SPJ)—dapat terpantau secara langsung (real-time).")
    add_p("Panduan ini dirancang dengan tata naskah dinas resmi, visual yang bersih, dan bahasa yang sistematis agar seluruh staf dapat langsung mempraktikkannya dalam pelaksanaan tugas sehari-hari. Dokumen ini juga memuat panduan khusus bagi tenaga pendukung teknis (IT Support) guna menjamin kelangsungan operasional sistem.")
    add_p("Semoga buku panduan ini memberikan manfaat nyata dalam mewujudkan pelayanan keprotokolan dan komunikasi pimpinan yang prima, profesional, dan berintegritas.")
    
    add_p("\nBrebes, November 2026", align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_p("Kepala Bagian Protokol dan Komunikasi Pimpinan", bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_p("Sekretariat Daerah Kabupaten Brebes\n\n\n", align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_p("( ____________________________________ )", bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_p("NIP. ............................................................", align=WD_ALIGN_PARAGRAPH.RIGHT)
    
    doc.add_page_break()

    # ------------------ DAFTAR ISI ------------------
    add_h1("DAFTAR ISI LENGKAP")
    daftar_isi = [
        ("KATA PENGANTAR", "i"),
        ("DAFTAR ISI LENGKAP", "ii"),
        ("BAGIAN I — PANDUAN PENGGUNA OPERASIONAL (INTERNAL)", ""),
        ("  BAB I     PENDAHULUAN & PENGENALAN SISTEM", "1"),
        ("  BAB II    HAK AKSES DAN JENIS PENGGUNA", "3"),
        ("  BAB III   CARA MASUK DAN KELUAR SISTEM (LOGIN & LOGOUT)", "4"),
        ("  BAB IV    HALAMAN UTAMA (DASBOR EKSEKUTIF)", "6"),
        ("  BAB V     KALENDER AGENDA KERJA", "8"),
        ("  BAB VI    WORKSHEET (LEMBAR KERJA UTAMA)", "9"),
        ("  BAB VII   DETAIL KEGIATAN & PENGELOLAAN BERKAS SPJ", "14"),
        ("  BAB VIII  REKAPITULASI LAPORAN (EXCEL & PDF)", "16"),
        ("  BAB IX    PENGELOLAAN DATA PETUGAS (MASTER PETUGAS)", "17"),
        ("  BAB X     DATA INSTANSI PENYELENGGARA (LEADING SECTOR)", "19"),
        ("  BAB XI    MANAJEMEN PENGGUNA (KHUSUS ADMINISTRATOR)", "20"),
        ("  BAB XII   RIWAYAT AKTIVITAS SISTEM (AUDIT LOG)", "21"),
        ("  BAB XIII  ALUR RESMI PERJALANAN STATUS KEGIATAN", "22"),
        ("  DAFTAR ISTILAH & TANYA JAWAB (FAQ)", "24"),
        ("BAGIAN II — PANDUAN TEKNIS IT SUPPORT DAN PENGEMBANG SISTEM", ""),
        ("  BAB XIV   INFORMASI AKUN PLATFORM DAN INFRASTRUKTUR", "26"),
        ("  BAB XV    PROSEDUR PENANGANAN KENDALA SISTEM (TROUBLESHOOTING)", "29"),
        ("PENUTUP", "31"),
    ]
    for judul, hal in daftar_isi:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(judul)
        if not hal and not judul.startswith(" "):
            r1.bold = True
            r1.font.color.rgb = NAVY
        else:
            r1.font.name = "Arial"
            r1.font.size = Pt(10)
            if hal:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                dots_len = max(5, 75 - len(judul))
                r_dots = p.add_run(" " + "." * dots_len + " ")
                r_dots.font.color.rgb = RGBColor(148, 163, 184)
                r_hal = p.add_run(hal)
                r_hal.bold = True
                r_hal.font.color.rgb = DARK_BLUE
                
    doc.add_page_break()

    # ------------------ BAGIAN I ------------------
    add_p("BAGIAN I", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, color=MUTED, space_after=2)
    add_p("PANDUAN PENGGUNA OPERASIONAL (INTERNAL)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, color=NAVY, space_after=18)
    
    # BAB I
    add_h1("BAB I — PENDAHULUAN & PENGENALAN SISTEM")
    add_h2("1.1 Mengenal Aplikasi SIAP-PRO")
    add_p("SIAP-PRO (Sistem Informasi Agenda Pimpinan Prokompim) adalah aplikasi berbasis web (web-based information system) yang dirancang khusus untuk mendukung kelancaran pelaksanaan tugas Bagian Protokol dan Komunikasi Pimpinan Sekretariat Daerah Kabupaten Brebes. Sistem ini berfungsi sebagai buku agenda kerja digital terpusat yang menggantikan tata kelola administrasi manual dan pencatatan yang sebelumnya tersebar di berbagai saluran tidak resmi seperti grup pesan instan (WhatsApp), lembaran disposisi fisik, dan berkas spreadsheet lokal.")
    add_p("Dengan SIAP-PRO, seluruh rangkaian kegiatan pimpinan daerah—Bupati, Wakil Bupati, Sekretaris Daerah, maupun pejabat yang mewakili—dikelola dalam satu pangkalan data yang terpadu, mutakhir, dan dapat diakses bersama secara aman oleh seluruh pemangku kepentingan di lingkungan Bagian Prokompim.")

    add_h2("1.2 Manfaat dan Kemudahan Utama")
    add_p("Penerapan aplikasi SIAP-PRO memberikan berbagai kemanfaatan strategis dan operasional, antara lain:")
    poin_manfaat = [
        ("Mencegah Jadwal Ganda (Conflict Scheduling)", "Memastikan pimpinan tidak terjadwal pada dua atau lebih agenda di lokasi berbeda pada waktu yang bersamaan."),
        ("Distribusi Penugasan yang Transparan", "Memudahkan pembagian tugas bagi Petugas Protokol, Juru Liput, dan Pengemudi (Driver), serta memperjelas koordinator penanggung jawab di lapangan."),
        ("Pemantauan Kesiapan Naskah Sambutan", "Memastikan ketersediaan teks sambutan, pidato, atau arahan pimpinan sebelum acara berlangsung melalui indikator status yang jelas."),
        ("Penyelesaian Berkas SPJ Tepat Waktu", "Menyediakan daftar periksa (checklist) pemantauan 7 dokumen wajib Surat Pertanggungjawaban (SPJ) hingga tuntas 100%."),
        ("Rekapitulasi Pelaporan Instan", "Menghasilkan laporan rekapitulasi agenda bulanan maupun tahunan dalam format resmi dokumen cetak (PDF) dan lembar kerja elektronik (Microsoft Excel) secara otomatis."),
        ("Audit dan Transparansi", "Mencatat setiap riwayat penambahan, pengubahan, dan penghapusan data secara otomatis demi menjamin akuntabilitas penyelenggaraan administrasi pemerintahan.")
    ]
    for judul, isi in poin_manfaat:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.7)
        p.paragraph_format.space_after = Pt(3)
        r_b = p.add_run(f"• {judul}: ")
        r_b.bold = True
        p.add_run(isi)

    # BAB II
    add_h1("BAB II — HAK AKSES DAN JENIS PENGGUNA")
    add_h2("2.1 Tiga Tingkatan Akun Pengguna")
    add_p("Guna menjamin keamanan sistem, integritas data, dan pemisahan tugas (segregation of duties), akun pengguna SIAP-PRO dibagi menjadi tiga tingkatan wewenang:")
    add_custom_table(
        ["No.", "Tingkatan Akun", "Peran Sistem", "Deskripsi Wewenang"],
        [
            ["1.", "Administrator", "ADMIN", "Pengelola teknis tertinggi dengan wewenang penuh atas seluruh fitur, termasuk pendaftaran, perbaikan, dan pengaturan hak akses pengguna lain."],
            ["2.", "Staf Prokompim", "STAFF", "Pengguna operasional harian yang bertugas menginput acara, menugaskan personel, memperbarui status naskah sambutan, dan melengkapi dokumen SPJ."],
            ["3.", "Kepala Bagian", "KEPALA_BAGIAN", "Pengguna eksekutif dengan hak pemantauan (read-only) dan pencetakan laporan resmi, tanpa akses untuk mengubah atau menghapus data kegiatan."]
        ],
        col_widths=[1.2, 3.5, 2.5, 7.8]
    )

    add_h2("2.2 Matriks Wewenang dan Hak Akses")
    add_custom_table(
        ["No.", "Modul / Fitur Sistem", "Admin", "Staf", "Kabag"],
        [
            ["1.", "Mengakses Dasbor Eksekutif", "Ya", "Ya", "Ya"],
            ["2.", "Melihat Lembar Kerja (Worksheet)", "Ya", "Ya", "Ya"],
            ["3.", "Menginput Kegiatan Baru", "Ya", "Ya", "Tidak"],
            ["4.", "Mengubah Data Kegiatan", "Ya", "Ya", "Tidak"],
            ["5.", "Menghapus Data Kegiatan", "Ya", "Ya", "Tidak"],
            ["6.", "Mengelola Master Data Petugas", "Ya", "Ya", "Tidak"],
            ["7.", "Mengelola Master Leading Sector", "Ya", "Ya", "Tidak"],
            ["8.", "Mengelola Akun Pengguna (User Management)", "Ya", "Tidak", "Tidak"],
            ["9.", "Melihat Riwayat Aktivitas (Activity Log)", "Ya", "Ya", "Ya"],
            ["10.", "Mengunduh Rekapitulasi Excel & Mencetak PDF", "Ya", "Ya", "Ya"],
        ],
        col_widths=[1.2, 7.8, 2.0, 2.0, 2.0]
    )

    # BAB III
    add_h1("BAB III — CARA MASUK DAN KELUAR SISTEM (LOGIN & LOGOUT)")
    add_h2("3.1 Kredensial Akun Administrator Utama")
    add_p("Untuk masuk ke aplikasi SIAP-PRO sebagai Administrator utama bagian, gunakan kredensial resmi berikut:")
    add_custom_table(
        ["Parameter Masuk", "Nilai Pengaturan"],
        [
            ["Alamat URL Aplikasi", "Sesuai tautan resmi SIAP-PRO yang telah ditetapkan"],
            ["Username", "admin"],
            ["Password", "prokompim"],
            ["Tingkatan Hak Akses", "Administrator (ADMIN)"]
        ],
        col_widths=[4.5, 10.5]
    )
    add_callout(
        "PERHATIAN KEAMANAN ADMINISTRASI:",
        "Kredensial di atas merupakan akun kedinasan Administrator internal SIAP-PRO. Jagalah kerahasiaan kata sandi dan jangan meninggalkan perangkat komputer dalam keadaan terbuka tanpa pengawasan.",
        is_warning=True
    )

    add_h2("3.2 Langkah-Langkah Masuk (Login)")
    langkah_login = [
        "Membuka Peramban Web: Buka peramban internet standar kedinasan (Google Chrome, Microsoft Edge, atau Mozilla Firefox) pada komputer kerja.",
        "Mengakses Tautan SIAP-PRO: Masukkan alamat URL resmi aplikasi SIAP-PRO pada bilah alamat (address bar), lalu tekan tombol Enter.",
        "Memasukkan Kredensial: Ketikkan Username pada kolom nama pengguna dan Password pada kolom kata sandi.",
        "Eksekusi Masuk: Klik tombol biru bertuliskan Masuk.",
        "Konfirmasi Masuk: Sistem akan memverifikasi kecocokan akun. Apabila valid, pengguna diarahkan ke Dasbor Eksekutif."
    ]
    for i, l in enumerate(langkah_login, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.7)
        p.paragraph_format.space_after = Pt(2)
        p.add_run(f"{i}. {l}")

    add_h2("3.3 Langkah Keluar (Logout) yang Aman")
    add_p("Apabila komputer kerja digunakan secara bergantian oleh beberapa pegawai, sangat penting untuk selalu keluar dari sistem setelah selesai bertugas:")
    add_p("1. Arahkan kursor ke sudut kanan atas layar aplikasi;\n2. Klik tombol atau ikon Keluar / Logout;\n3. Pada jendela konfirmasi yang muncul, pilih opsi Ya, Keluar;\n4. Pastikan tampilan layar telah kembali ke halaman muka form login sebelum meninggalkan meja kerja.")

    # BAB IV
    add_h1("BAB IV — HALAMAN UTAMA (DASBOR EKSEKUTIF)")
    add_p("Halaman Dasbor menyajikan ringkasan eksekutif berbasis visual mengenai status seluruh agenda kerja pimpinan daerah secara terpadu tanpa mengharuskan pengguna membuka baris data satu per satu.")
    add_h2("4.1 Empat Kartu Angka Kunci")
    add_custom_table(
        ["No.", "Kartu Informasi", "Definisi dan Cara Perhitungan"],
        [
            ["1.", "Kegiatan Bulan Ini", "Akumulasi total agenda pimpinan yang terjadwal sepanjang bulan berjalan (tanggal 1 s.d. akhir bulan)."],
            ["2.", "Kegiatan Hari Ini", "Jumlah agenda yang berlangsung tepat pada hari penanggalan komputer saat ini."],
            ["3.", "Total Sambutan", "Rasio kesiapan teks sambutan pimpinan, menampilkan perbandingan antara sambutan yang Sudah Siap (angka hijau) dan Belum Siap (angka kuning)."],
            ["4.", "Kegiatan Tahun Berjalan", "Total kumulatif seluruh kegiatan sepanjang tahun kalender yang dipilih, disertai rincian jumlah kegiatan yang telah berstatus selesai terlaksana."]
        ],
        col_widths=[1.2, 4.5, 9.3]
    )

    add_h2("4.2 Grafik Kegiatan Bulanan & Agenda Terdekat")
    add_p("Di bawah kartu angka kunci terdapat grafik batang yang memetakan persebaran volume kegiatan dari bulan Januari hingga Desember pada tahun yang aktif. Di samping kanan grafik terdapat panel Kegiatan Terdekat yang menampilkan 5 jadwal acara terdekat yang akan segera berlangsung untuk persiapan lebih awal.")

    add_h2("4.3 Progres Dokumen dan Filter Tahun")
    add_p("Dasbor dilengkapi indikator Progres SPJ (persentase kelengkapan berkas 0-100%) dan Top 5 Leading Sector. Gunakan menu dropdown Filter Tahun di sudut kanan atas untuk melihat statistik tahun-tahun sebelumnya.")

    # BAB V
    add_h1("BAB V — KALENDER AGENDA KERJA")
    add_p("Menu Kalender menyajikan agenda kerja pimpinan dalam bentuk penanggalan bulanan yang intuitif, memungkinkan pemantauan kepadatan jadwal secara spasial.")
    add_h2("5.1 Membaca Kode Warna Status pada Kalender")
    add_custom_table(
        ["No.", "Indikator Warna", "Status Kegiatan", "Makna Operasional Keprotokolan"],
        [
            ["1.", "🟣 Ungu", "Acara Masuk", "Surat undangan telah diagendakan, namun belum dilakukan disposisi penetapan personel."],
            ["2.", "🟡 Kuning", "Menunggu Penugasan", "Agenda telah disetujui, sedang dalam proses penentuan personel lapangan atau persiapan naskah."],
            ["3.", "🟢 Hijau", "Kegiatan Selesai", "Acara telah selesai diselenggarakan di lapangan oleh tim pendamping pimpinan."],
            ["4.", "🔵 Biru", "SPJ Selesai", "Seluruh berkas administrasi dan laporan SPJ telah rampung 100%."]
        ],
        col_widths=[1.2, 3.0, 4.0, 6.8]
    )

    # BAB VI
    add_h1("BAB VI — WORKSHEET (LEMBAR KERJA UTAMA)")
    add_p("Lembar Kerja (Worksheet) adalah modul utama aplikasi SIAP-PRO. Seluruh transaksi pendataan, penyuntingan, pemantauan status, dan ekspor data dilakukan melalui lembar kerja ini.")
    add_h2("6.1 Rincian Kolom Data Kegiatan")
    add_custom_table(
        ["No.", "Nama Kolom", "Jenis", "Penjelasan Isi Data"],
        [
            ["1.", "Tanggal & Waktu", "Waktu", "Hari, tanggal, dan jam pelaksanaan acara (JJ:MM WIB)."],
            ["2.", "Nama Kegiatan", "Teks", "Nama resmi atau judul agenda pimpinan."],
            ["3.", "Tempat", "Teks", "Lokasi spesifik penyelenggaraan kegiatan."],
            ["4.", "Pejabat", "Pilihan", "Nama pejabat yang diagendakan hadir (Bupati, Wabup, Sekda, dll.)."],
            ["5.", "Leading Sector", "Pilihan", "OPD, instansi, atau badan penyelenggara kegiatan."],
            ["6.", "Status Sambutan", "Status", "Kesiapan naskah pidato/sambutan (SUDAH / BELUM)."],
            ["7.", "Status Kegiatan", "Status", "Tahapan proses kegiatan saat ini."],
            ["8.", "Petugas Protokol", "Relasi", "Nama staf protokol yang ditugaskan di lokasi."],
            ["9.", "Petugas Liputan", "Relasi", "Nama tim dokumentasi dan publikasi yang ditugaskan."],
            ["10.", "Petugas Driver", "Relasi", "Nama pengemudi dinas yang bertugas melayani perjalanan."],
            ["11.", "Jenis Penugasan", "Pilihan", "Klasifikasi penugasan: Kegiatan / Lembur / SPPD."],
            ["12.", "Link Upload", "Tautan", "Tautan folder Google Drive berkas kegiatan."],
            ["13.", "Aksi", "Tombol", "Tombol Detail Berkas (🔗), Ubah (✏️), dan Hapus (🗑️)."]
        ],
        col_widths=[1.2, 3.8, 2.5, 7.5]
    )

    add_h2("6.2 Penugasan Petugas yang Fleksibel & Semua Crew")
    add_p("Sistem memperbolehkan pemilihan seluruh staf aktif lintas kategori (Liputan dapat bertugas sebagai Protokol). Jika staf yang sama terpilih pada dua peran berbeda, sistem memberi highlight kuning sebagai konfirmasi. Untuk acara besar, centang 'Semua Crew' untuk menugaskan seluruh regu secara otomatis.")

    # BAB VII
    add_h1("BAB VII — DETAIL KEGIATAN & PENGELOLAAN BERKAS SPJ")
    add_p("Klik ikon rantai tautan (🔗) pada kolom Aksi lembar kerja untuk membuka halaman khusus Detail Kegiatan & Manajemen Berkas SPJ.")
    add_h2("7.1 Tujuh (7) Dokumen Wajib SPJ yang Dipantau")
    add_custom_table(
        ["No.", "Jenis Dokumen Wajib", "Format / Bukti Fisik yang Disyaratkan"],
        [
            ["1.", "Surat Tugas", "Surat perintah tugas resmi yang ditandatangani pimpinan/Sekda."],
            ["2.", "Surat Undangan", "Berkas surat undangan resmi dari penyelenggara yang telah terdisposisi."],
            ["3.", "Naskah Sambutan", "Salinan naskah pidato/sambutan yang dibacakan oleh pimpinan."],
            ["4.", "Dokumentasi Foto", "Berkas foto resolusi tinggi pelaksanaan acara di lapangan."],
            ["5.", "Dokumentasi Video", "Rekaman cuplikan visual atau video pendek publikasi kegiatan."],
            ["6.", "Berkas SPJ", "Berkas kuitansi, daftar tanda terima, kuitansi bensin, atau bukti riil keuangan."],
            ["7.", "Laporan Akhir", "Naskah laporan pelaksanaan tugas yang disusun oleh staf pendamping."]
        ],
        col_widths=[1.2, 4.3, 9.5]
    )

    # BAB VIII
    add_h1("BAB VIII — REKAPITULASI LAPORAN (EXCEL & PDF)")
    add_p("Menu Laporan menyediakan sarana pembuatan rekapitulasi kegiatan resmi yang dapat disesuaikan kolomnya dan langsung dicetak ke dokumen formal:")
    add_p("• Unduh Format Excel: Klik tombol Export Excel untuk mendapatkan berkas spreadsheet (.xlsx) siap olah.\n• Cetak Format PDF: Klik tombol Cetak Laporan untuk membuka pratinjau cetak resmi berstandar kedinasan.")

    # BAB IX - XIII RINGKASAN
    add_h1("BAB IX — PENGELOLAAN DATA PETUGAS (MASTER PETUGAS)")
    add_p("Modul Master Petugas mengelola data tim Protokol, Liputan, dan Driver. Staf yang mutasi/pensiun sebaiknya dinonaktifkan (jangan dihapus) agar riwayat penugasan lama pada SPJ tetap terbaca utuh.")

    add_h1("BAB X — DATA INSTANSI PENYELENGGARA (LEADING SECTOR)")
    add_p("Mengelola pangkalan data OPD, Forkopimda, instansi vertikal, BUMN/BUMD, kecamatan, dan instansi swasta penyelenggara kegiatan pimpinan daerah.")

    add_h1("BAB XI — MANAJEMEN PENGGUNA (KHUSUS ADMINISTRATOR)")
    add_p("Modul khusus Administrator untuk mendaftarkan akun pegawai baru, memperbarui peran (Admin/Staff/Kepala Bagian), dan melakukan reset password staf yang lupa kata sandi.")

    add_h1("BAB XII — RIWAYAT AKTIVITAS SISTEM (AUDIT LOG)")
    add_p("Merekam secara otomatis seluruh peristiwa perubahan data (CREATE, UPDATE, DELETE), identitas pengguna yang mengubah, serta waktu tepat kejadian untuk keperluan audit.")

    add_h1("BAB XIII — ALUR RESMI PERJALANAN STATUS KEGIATAN")
    add_p("Setiap agenda mematuhi 4 tahapan alur resmi: Acara Masuk ➔ Menunggu Penugasan ➔ Kegiatan Selesai ➔ SPJ Selesai.")

    add_h2("Daftar Istilah & Pertanyaan yang Sering Diajukan (FAQ)")
    add_p("• PIC: Narahubung utama penyelenggara acara.\n• SPPD: Surat Perintah Perjalanan Dinas ke luar daerah.\n• Progress Bar: Indikator visual kelengkapan 7 berkas SPJ dari 0% hingga 100%.")

    doc.add_page_break()

    # ------------------ BAGIAN II ------------------
    add_p("BAGIAN II", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, color=MUTED, space_after=2)
    add_p("PANDUAN TEKNIS IT SUPPORT DAN PENGEMBANG SISTEM", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, color=NAVY, space_after=18)
    add_callout(
        "INFORMASI TERBATAS / STRICTLY CONFIDENTIAL:",
        "Bagian ini memuat informasi rahasia mengenai infrastruktur server, akun layanan cloud, dan kunci akses basis data (API Keys). Dokumen ini HANYA diperuntukkan bagi Tim IT Support, Tenaga Ahli IT, dan Pengembang Sistem. DILARANG disebarluaskan kepada pihak umum atau pengguna operasional biasa.",
        is_warning=True
    )

    # BAB XIV
    add_h1("BAB XIV — INFORMASI AKUN PLATFORM DAN INFRASTRUKTUR")
    add_h2("14.1 Akun Google Master (Gmail Prokompim)")
    add_p("Akun Google kedinasan ini merupakan akun induk (master account) pusat autentikasi Single Sign-On (SSO) untuk seluruh infrastruktur cloud:")
    add_custom_table(
        ["Parameter Kredensial", "Nilai Resmi"],
        [
            ["Alamat Surel (Email)", "prokompimbrebes@gmail.com"],
            ["Kata Sandi (Password)", "prokompimbrebes2026"],
            ["Peruntukan Layanan", "Autentikasi SSO untuk Vercel, Supabase, dan penyimpanan Google Drive"]
        ],
        col_widths=[5.0, 10.0]
    )

    add_h2("14.2 Platform Hosting dan Deployment (Vercel)")
    add_p("Akses Vercel digunakan ketika website SIAP-PRO tidak dapat diakses (down/crash).")
    add_p("Prosedur Masuk Vercel:\n1. Pastikan peramban telah login ke akun Gmail prokompimbrebes@gmail.com;\n2. Akses https://vercel.com/ lalu klik Log In;\n3. Pilih Continue with Google dan pilih akun prokompimbrebes@gmail.com;\n4. Periksa tab Deployments untuk melihat log kesalahan server.")

    add_h2("14.3 Platform Basis Data (Supabase PostgreSQL)")
    add_p("Akses Supabase digunakan ketika website dapat dibuka, namun data kegiatan hilang atau tidak dapat disimpan.")
    add_custom_table(
        ["Parameter Kredensial Supabase", "Nilai Konfigurasi"],
        [
            ["Alamat Akses", "https://supabase.com/"],
            ["Email Login", "prokompimbrebes@gmail.com"],
            ["Password Login Akun", "Prokompimbrebes2026!"],
            ["Password Basis Data (PostgreSQL)", "Prokompimbrebes2026!"],
            ["Wilayah Server", "aws-0-ap-southeast-1 (Singapura)"]
        ],
        col_widths=[6.0, 9.0]
    )

    add_h2("14.4 Repositori Kode Sumber (GitHub)")
    add_custom_table(
        ["Parameter Kredensial GitHub", "Nilai Resmi"],
        [
            ["Alamat Repositori", "https://github.com/"],
            ["Username", "Prokompim-Brebes"],
            ["Email Terdaftar", "prokompimbrebes@gmail.com"],
            ["Password", "prokompimbrebes2026"]
        ],
        col_widths=[5.0, 10.0]
    )

    add_h2("14.5 Konfigurasi Variabel Lingkungan dan API Key")
    add_p("Variabel lingkungan berikut wajib terkonfigurasi pada Vercel dan file .env lokal:")
    add_p("1. DATABASE_URL (Koneksi Pooler Transaksi):\npostgresql://postgres.obhnufrsrjjuwyywrlkf:6SRPOrw6awJDUHxm@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true\n\n2. DIRECT_URL (Koneksi Migrasi Prisma):\npostgresql://postgres.obhnufrsrjjuwyywrlkf:6SRPOrw6awJDUHxm@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres\n\n3. AUTH_SECRET (Token Sesi JWT):\n61e65a8c4ac2ed8c8f90ea648dd0ca3d")

    # BAB XV
    add_h1("BAB XV — PROSEDUR PENANGANAN KENDALA SISTEM (TROUBLESHOOTING)")
    add_h2("15.1 Kasus A: Aplikasi Web Tidak Dapat Diakses (Down / Crash)")
    add_p("1. Masuk ke dasbor Vercel menggunakan akun Google prokompimbrebes@gmail.com;\n2. Periksa versi deployment teratas yang berstatus gagal (tanda merah);\n3. Buka Build Logs / Runtime Logs untuk melihat pesan error;\n4. Perbaiki kode sumber melalui GitHub, lalu jalankan git push origin main untuk deploy ulang otomatis.")

    add_h2("15.2 Kasus B: Aplikasi Dapat Diakses Namun Data Kosong / Hilang")
    add_p("1. Masuk ke dasbor Supabase dengan email prokompimbrebes@gmail.com dan password Prokompimbrebes2026!;\n2. Periksa status proyek basis data. Jika berstatus 'Paused', klik tombol 'Restore Project' dan tunggu 2-3 menit;\n3. Buka Table Editor untuk memastikan tabel kegiatan dan petugas masih menyimpan data;\n4. Periksa variabel DATABASE_URL di Vercel apakah masih cocok dengan konfigurasi Supabase aktif.")

    # PENUTUP
    doc.add_page_break()
    add_h1("PENUTUP")
    add_p("Buku Panduan Pengguna Sistem Informasi Agenda Pimpinan Prokompim (SIAP-PRO) ini disusun dengan komitmen penuh untuk meningkatkan profesionalisme, efisiensi, dan akuntabilitas penatausahaan keprotokolan di lingkungan Pemerintah Kabupaten Brebes.")
    add_p("Dengan pemahaman yang menyeluruh atas seluruh panduan operasional maupun teknis yang tercantum dalam dokumen ini, diharapkan seluruh jajaran di Bagian Protokol dan Komunikasi Pimpinan serta tenaga pendukung sistem dapat bersinergi secara optimal dalam menyukseskan pelayanan agenda pimpinan daerah.")
    
    add_p("\nDitetapkan di Brebes\npada tanggal 12 November 2026", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("BAGIAN PROTOKOL DAN KOMUNIKASI PIMPINAN\nSEKRETARIAT DAERAH KABUPATEN BREBES", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=NAVY)

    # Save
    doc.save(output_path)
    print(f"DOCX successfully generated at: {output_path}")

if __name__ == "__main__":
    out_docx = os.path.join("docs", "BUKU PANDUAN SIAP-PRO.docx")
    build_docx(out_docx)
