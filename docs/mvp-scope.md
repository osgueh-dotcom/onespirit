# Cakupan MVP & Pengembangan Lanjutan (MVP Scope)

Dokumen ini mendefinisikan batasan sistem **One Spirit Workflow & Business Analytics System** saat ini (MVP) serta mengidentifikasi fitur-fitur yang direkomendasikan untuk pengembangan fase lanjutan (Fase 2).

---

## 1. MVP Siap Demo (MVP Demo Ready)
Fitur-fitur ini telah teruji secara lokal, stabil, dan siap disajikan penuh saat demo kepada PT. One Spirit Asia:
- **Dashboard Eksekutif**: Rangkuman KPI bisnis (*Total Inquiry, Deal Rate, Cancel Rate, Average Project Value*).
- **Executive Summary Narrative**: Ringkasan performa otomatis berbahasa Indonesia.
- **Catatan Evaluasi Manajemen**: Pendeteksian kekuatan operasional, bottlenecks, dan rekomendasi aksi secara dinamis.
- **Analisis Pendapatan & Target**: Pencapaian omset terhadap target tahunan direksi.
- **Ringkasan Keuangan & Pembayaran**: Pemantauan billing count, Received Cash, Collection Rate, dan sisa piutang.
- **Review Kualitas Data**: Audit otomatis ketidaklengkapan berkas/anggaran/penanggung jawab proyek berdasarkan database terpusat.
- **Alur Kerja Proyek**: Kanban board terintegrasi dengan filter pencarian lanjut (PO, PM, Customer, Source).
- **Rincian Proyek (Detail)**: Profil klien, status daur hidup proyek, linimasa visual status (*Status Timeline*), dan audit trail log aktivitas (*Activity Log*).
- **Gerbang Kesiapan & Kontrol Eksekusi Event**: Validasi otomatis transisi status (Ready, Running, Completed, Closed, Cancel) dengan deteksi warning/blocker, override via pembaruan paksa (force update), serta integrasi panel kontrol eksekusi event (Execution Control Panel) di detail proyek.
- **PM Control Center (Operational Dashboard)**: Pusat kontrol harian/mingguan bagi Program Manager untuk memantau event mendatang, project tidak siap, instrument overdue, instrument butuh revisi, serta daftar aksi prioritas (Priority Actions) berdasarkan tingkat urgensi.
- **PO Control Center (Commercial Dashboard)**: Pusat kontrol komersial bagi Program Owner untuk memantau status quotation, revenue (potential vs confirmed), deal/cancel rate, kontribusi lead source/partner, outstanding payment, serta daftar prioritas follow-up tindakan komersial.
- **Project Documentation Links**: Penautan langsung tautan dokumen eksternal Google Drive proyek pada halaman rincian proyek (siap demo).
- **Excel Import**: Alat migrasi data *spreadsheet* lama disertai deteksi kesalahan format otomatis.
- **Ekspor Laporan Cetak**: Fitur browser print layout putih bersih bebas sidebar untuk ekspor PDF instan.

---

## 2. MVP Membutuhkan Validasi Klien (MVP Needs Validation)
Fitur-fitur ini sudah berjalan, namun GVSys memerlukan masukan dan konfirmasi alur bisnis dari PT. One Spirit Asia:
- **Definisi Peran PO & PM**: Apakah penunjukan staf internal sebagai PO dan PM per proyek sudah sesuai dengan praktik lapangan?
- **Status Lifecycles**: Apakah daftar pilihan status untuk Quotation, Program, Payment, dan Project sudah mencakup seluruh variasi proses bisnis Anda?
- **Project Readiness & Instruments**: Kami telah membangun pelacakan status operasional instrumen proyek (**CL, ROS, CK, PNL, PF, MATRIX**) beserta formula **Skor Kesiapan Proyek (Readiness Score)**. Kami memerlukan masukan apakah pembobotan formula (60% instrumen, 20% ketersediaan dokumen, 20% konsistensi status) serta aturan peringatan otomatis (seperti penyerahan CL wajib saat quotation Signed & Deal) sudah sesuai dengan regulasi operasional internal.
- **Sifat Data Sales Eksternal**: Apakah sales eksternal (sisi vendor/sumber hotel) sudah cukup dicatat sebagai teks penanda saja atau perlu dibuatkan tabel database khusus dengan informasi kontak detail?
- **Setelan Target Target Tahunan**: Apakah target tahunan 2025 senilai Rp9.2 Miliar sudah tepat dan apakah target ini perlu diubah sendiri oleh manajemen dari menu administrasi?

---

## 3. Pengembangan Fase Lanjutan (Future Phase Recommendations)
Fitur-fitur di bawah ini **tidak termasuk** dalam lingkup MVP awal GVSys dan diposisikan sebagai pengembangan fase lanjutan setelah MVP disetujui:
- **Advanced PDF Report Generator**: Pembuatan file PDF laporan formal secara langsung dari server dengan layout kop surat resmi PT. One Spirit Asia.
- **Automated Quotation Generator**: Pembuatan file surat penawaran harga otomatis berdasarkan detail budget item proyek yang diisi di sistem.
- **Invoice Generation & Nominal Termin Refinement**: Pembuatan invoice otomatis dengan penanganan pembayaran parsial (termin 1, DP, pelunasan) beserta tracking nominal tanggal jatuh tempo secara ketat.
- **Integrasi Pihak Ketiga**:
  - **Google Drive Integration**: Upload berkas dari sistem langsung terbuat folder otomatis di Google Drive proyek.
  - **WhatsApp / Email Notifications**: Pengiriman notifikasi pengingat otomatis ke PM/PO jika target persiapan event sudah mendekati hari-H atau invoice mendekati tanggal jatuh tempo.
- **Keamanan & Administrasi Lanjut**:
  - **Advanced Role Permission Matrix**: Pembatasan menu edit/view secara granular berdasarkan departemen staf (misal: PM tidak bisa melihat detail omset keuangan sama sekali). *Catatan: Di MVP Sprint 7, pembatasan dasar tautan PNL sensitif untuk peran Staff telah diimplementasikan.*
  - **Advanced Audit Trail**: Pencatatan riwayat revisi data field demi field secara mendetail (misalnya: mencatat perubahan budget dari nilai A menjadi B).
- **Analitik Lanjut**:
  - **Multi-year Comparative Analytics**: Grafik perbandingan performa penjualan antar tahun.
  - **Monthly/Quarterly Executive Report Export**: Ekspor otomatis laporan kuartalan untuk bahan rapat komisaris.
- **Infrastruktur Produksi**:
  - **Production Cloud Deployment & Backup**: Pemasangan sistem di server cloud (AWS/GCP/DigitalOcean) milik PT. One Spirit Asia beserta konfigurasi pencadangan database harian otomatis.
