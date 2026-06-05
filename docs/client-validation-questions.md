# Pertanyaan Validasi Klien (Client Validation Questions)

Kuesioner ini digunakan oleh presenter **GVSys** saat berdiskusi dengan manajemen **PT. One Spirit Asia** untuk menyelaraskan alur operasional nyata dengan logika sistem.

---

## 1. Alur Kerja Proyek & Status (Workflow & Statuses)
1. **Daur Hidup Status**: Sistem membagi proyek ke dalam 4 jenis status (Quotation, Program, Payment, Project). Apakah pembagian ini sudah sesuai dengan realitas kerja di One Spirit?
2. **Pilihan Status**:
   - Apakah status Quotation (*Draft, Sent, Follow Up, Revision, Signed & Deal, Cancel*) sudah lengkap?
   - Apakah status Program (*Inquiry, Confirmed, Preparation, Ready, Running, Completed, Reporting, Closed, Cancel*) sudah sesuai?
   - Apakah ada kondisi di mana proyek yang sudah berstatus *Completed* di program, namun status Project-nya masih aktif/open karena urusan dokumentasi?

## 2. Penugasan PO / PM (PO & PM Assignment)
1. **Definisi Peran**: Apakah definisi **Program Owner (PO)** sebagai penanggung jawab proyek/penjualan secara keseluruhan, dan **Program Manager (PM)** sebagai penanggung jawab teknis persiapan program di lapangan sudah tepat?
2. **Kuantitas Staf**: Apakah satu proyek dipastikan hanya memiliki maksimal **satu PO** dan **satu PM**?
3. **Fleksibilitas Peran**: Apakah PO dan PM dapat diubah di tengah jalan setelah proyek berstatus running?
4. **Beban Kerja**: Bagaimana manajemen menilai batas maksimal proyek aktif yang dapat ditangani oleh seorang PM dalam satu waktu?

## 3. Sumber Event & Sales Eksternal (Event Source & Sales)
1. **Database Sales**: Saat ini nama Sales dicatat langsung pada sisi sumber masuk event (Event Source) karena bersifat eksternal (pihak vendor/hotel). Apakah di masa depan Anda memerlukan database Sales tersendiri lengkap dengan nomor telepon dan alamat email mereka?
2. **Kontak Sumber**: Apakah data hotel/partner (Event Source) memerlukan kolom kontak personal (misalnya nama GM Hotel atau Banquet Manager)?
3. **Kategori Sumber**: Apakah pilihan tipe sumber saat ini (*Hotel, Direct, Repeater, Partner, Instagram, Web*) sudah mencakup seluruh jalur masuknya klien?

## 4. Pelanggan (Customer Management)
1. **Kategori Klien**: Apakah pembagian kategori pelanggan (*Corporate, Government, Agency*) sudah mencakup profil klien Anda saat ini?
2. **Kontak Ganda**: Apakah satu profil perusahaan pelanggan perlu didesain untuk memiliki lebih dari satu kontak person (misalnya kontak HRD dan kontak tim Keuangan)?
3. **Duplikasi Data**: Bagaimana One Spirit menangani pelanggan lama yang berganti nama? Apakah sistem perlu memiliki fitur penggabungan (*merge*) data pelanggan yang duplikat?

## 5. Keuangan & Pembayaran (Finance & Payment)
1. **Kolektibilitas**: Sistem memantau nominal *Received Cash* (dana masuk) dan *Outstanding Amount* (piutang). Apakah One Spirit terbiasa menggunakan termin pembayaran (DP 30%, Termin 2 40%, Pelunasan 30%)?
2. **Invoice**: Apakah pencatatan status tagihan (*Invoice Sent, Paid, Partial Paid*) sudah cukup, atau apakah One Spirit membutuhkan pembuatan file invoice langsung dari sistem web ini?
3. **Tanggal Jatuh Tempo**: Apakah ada aturan durasi standar (misal: jatuh tempo 14 hari setelah invoice dikirim) untuk menetapkan status pembayaran menjadi *Overdue* (terlambat)?

## 6. Dashboard & Metrik Evaluasi (Management Analytics)
1. **Prioritas KPI**: Metrik apa yang paling krusial bagi manajemen saat mengevaluasi kinerja mingguan? (Pendapatan terkonfirmasi, rasio deal, atau efisiensi PM?)
2. **Target Revenue**: Target pendapatan tahunan 2025 disetel sebesar Rp9.2 Miliar. Apakah target ini sudah final, dan bagaimana mekanisme pembagian target per kuartal/bulan?
3. **PO & PM Reviews**: Apakah kolom evaluasi *PO Performance* (kontribusi omset) dan *PM Workload* (jumlah proyek running) sudah menampilkan informasi yang dibutuhkan untuk penilaian bonus akhir tahun staf?

## 7. Pelaporan & Ekspor (Reporting)
1. **Format Ekspor**: Apakah fitur cetak instan ke PDF (*Print to PDF*) lewat browser sudah cukup untuk kebutuhan pelaporan cepat, atau apakah manajemen memerlukan file Excel (.xlsx) yang dapat diunduh untuk diolah kembali?
2. **Template Laporan**: Apakah One Spirit memiliki format template laporan evaluasi bulanan tertentu yang harus diikuti oleh sistem di masa depan?
