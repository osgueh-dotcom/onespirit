# Alur Demo Sistem One Spirit

Dokumen ini memandu presenter dalam mendemonstrasikan **One Spirit Workflow & Business Analytics System** kepada direksi dan manajemen **PT. One Spirit Asia**. 

Tujuan utama demo ini adalah memvalidasi hasil modernisasi alur kerja dari *spreadsheet* Excel menjadi sistem web terintegrasi serta menyelaraskan ekspektasi MVP (Minimum Viable Product).

---

## 1. Pembukaan (Opening)
- **Tujuan**: Menjelaskan latar belakang masalah dan nilai modernisasi sistem.
- **Poin Penyampaian**:
  - GVSys (Gueh Visual Systems) mendesain sistem ini untuk memodernisasi alur kerja operasional PT. One Spirit Asia yang sebelumnya dikelola manual menggunakan file Excel terpisah.
  - Memperkenalkan nama aplikasi: **One Spirit Workflow & Business Analytics System**.
  - Menjelaskan nilai modernisasi: menghilangkan risiko duplikasi data, meningkatkan transparansi beban kerja tim internal, memantau *pipeline* penjualan dengan data yang terpusat dan terbarui, serta mengidentifikasi ketidaklengkapan data operasional secara otomatis sebelum rapat evaluasi bulanan.

## 2. Halaman Login dan Konteks Pengguna (Login & Role Context)
- **Tujuan**: Membuka aplikasi dan menjelaskan model penugasan internal.
- **Langkah Tindakan**:
  - Buka halaman login utama di browser.
  - Masuk sebagai akun Administrator/Manajemen.
  - **Poin Penjelasan**:
    - Sistem memiliki modul pengguna internal yang dinamis.
    - Menjelaskan konsep bahwa **Program Owner (PO)** dan **Program Manager (PM)** bukan merupakan jabatan atau hak akses permanen, melainkan peran dinamis (staf internal) yang ditugaskan secara fleksibel untuk setiap proyek/event.

## 3. Executive Dashboard (Dashboard Evaluasi Manajemen)
- **Tujuan**: Menunjukkan pusat analisis bisnis dan pencapaian target.
- **Langkah Tindakan**:
  - Arahkan ke menu **Dashboard** (ini adalah tampilan halaman default setelah masuk).
  - Tunjukkan ringkasan indikator:
    - **Total Inquiry**: Seluruh catatan event/proyek yang masuk ke sistem.
    - **Total Deal & Deal Conversion Rate**: Jumlah proyek yang berhasil disepakati beserta persentase keberhasilannya.
    - **Cancellation Rate**: Tingkat pembatalan proyek yang memerlukan perhatian.
    - **Revenue Summary**: Menunjukkan *Potential Pipeline*, *Confirmed Revenue*, *Target Revenue* (target tahunan direksi), dan *Target Achievement Rate* secara dinamis.
    - **Actually Received Cash**: Total pembayaran tunai yang sudah diterima dan terkonfirmasi lunas.
    - **Collection Rate & Outstanding Amount**: Rasio penagihan piutang dan sisa tagihan terutang.
  - Tunjukkan **Catatan Evaluasi Manajemen (Management Review Notes)**:
    - Menjelaskan sistem penalaran cerdas yang otomatis mengidentifikasi kekuatan bisnis (misal: Deal Rate tinggi) dan risiko bottlenecks (misal: Cancel Rate tinggi, tagihan outstanding).
  - Tunjukkan **Executive Summary Narrative**:
    - Paragraf bahasa Indonesia otomatis yang meringkas kinerja penjualan periode berjalan untuk memudahkan presentasi manajemen.

## 4. Alur Kerja Proyek (Project Workflow)
- **Tujuan**: Mendemonstrasikan visualisasi status proyek dan penggunaan filter analitik.
- **Langkah Tindakan**:
  - Arahkan ke menu **Projects**.
  - Tunjukkan daftar proyek dalam bentuk papan atau tabel alur kerja.
  - Tunjukkan penggunaan **Filter Analitik**:
    - Saring berdasarkan nama Program Owner (PO).
    - Saring berdasarkan nama Program Manager (PM).
    - Saring berdasarkan Kategori Pelanggan (Corporate, Agency, Government).
    - Saring berdasarkan Sumber Event (Hotel, Partner, Direct, dsb).
  - Tunjukkan respons sistem yang cepat memperbarui data dashboard/list proyek sesuai parameter filter.

## 5. Rincian Proyek (Project Detail)
- **Tujuan**: Menunjukkan transparansi riwayat dan kelengkapan satu proyek spesifik.
- **Langkah Tindakan**:
  - Klik salah satu proyek contoh yang datanya lengkap untuk membuka halaman detail.
  - Tunjukkan bagian-bagian detail:
    - Profil Pelanggan & Sumber Event.
    - Penugasan staf internal (PO & PM).
    - Nilai Anggaran (Budget).
    - Rincian Tahapan Siklus Proyek (Quotation, Program, Payment, dan Project Status).
    - **Status Timeline**: Alur progres proyek dari tahap awal hingga penutupan secara visual.
    - **Activity Log**: Rekam jejak perubahan status dan tindakan yang dilakukan pengguna sistem untuk audit operasional.
    - **Documentation / Project Instruments (CL, ROS, CK, PNL)**: Tautan dokumen penting proyek (Contract Letter, Rundown of Show, Check List, Profit & Loss) yang saat ini disediakan melalui tautan dokumentasi terintegrasi. Jelaskan bahwa instrumen ini diidentifikasi sebagai bagian penting dari kelengkapan operasional proyek yang akan divalidasi alur status spesifiknya.

## 6. Penjelasan Konteks Bisnis Khusus (Sales & PO/PM)
- **Tujuan**: Menyelaraskan konsep operasional khusus yang disepakati.
- **Poin Penjelasan**:
  - **Sales**: Menegaskan kembali bahwa sales bersifat eksternal dan melekat pada sisi vendor/sumber event (Event Source), bukan sebagai akun pengguna sistem internal.
  - **PO & PM Dynamic Allocation**: Menunjukkan fleksibilitas penunjukan PO dan PM langsung di dalam form edit proyek/event.

## 7. Validasi Excel Import (Excel Import & Data Validation)
- **Tujuan**: Menunjukkan proses migrasi data dari format lama.
- **Langkah Tindakan**:
  - Arahkan ke menu **Import/Excel Import**.
  - Simulasikan upload file Excel template operasional.
  - Tunjukkan **Import Preview**:
    - Bagaimana sistem menampilkan data Excel sebelum disimpan ke database database utama.
    - Bagaimana sistem menandai baris data yang salah format atau tidak valid.

## 8. Review Kualitas Data (Data Quality Review)
- **Tujuan**: Menunjukkan bagaimana sistem membantu menjaga kebersihan data operasional.
- **Langkah Tindakan**:
  - Kembali ke Dashboard, gulir ke panel **Review Kualitas Data**.
  - **Poin Penjelasan**:
    - Panel ini mendeteksi ketidaklengkapan data secara otomatis berdasarkan kondisi terkini database seperti: PO/PM belum ditunjuk, anggaran bernilai nol, pembatalan tanpa mencantumkan alasan (cancel reason), proyek Closed tapi invoice belum dibayar, atau dokumen pendukung drive kosong.

## 9. PM Control Center & Operational Priorities
- **Tujuan**: Menunjukkan workspace PM dalam memantau event mendatang, kesiapan operasional instrumen, dan penentuan prioritas aksi.
- **Langkah Tindakan**:
  - Arahkan ke menu **PM Control Center**.
  - Tunjukkan KPI summary harian operasional.
  - Jelaskan tab: Prioritas Tindakan (Critical/High), Jadwal Event, Checklist & Overdue, PM Workload.

## 10. PO Control Center & Commercial Dashboard
- **Tujuan**: Menunjukkan workspace PO dalam memantau status quotation, total revenue (potential vs confirmed), deal/cancel rate, kontribusi partner hotel, outstanding payment, dan prioritas follow-up tindakan komersial.
- **Langkah Tindakan**:
  - Arahkan ke menu **PO Control Center**.
  - Tunjukkan KPI komersial di bagian atas (Deal Rate, Confirmed Revenue, Outstanding).
  - Tunjukkan tab **Prioritas Follow-up** (misal: proyek deal Rp 0, piutang overdue) dan **Risiko Komersial** (cancel without reason, missing PO/source).
  - Tunjukkan tab **Kinerja Komersial** (PO Performance workloads, Source/Vendor lead contribution).

## 11. Laporan Cetak (Print / Save PDF Report)
- **Tujuan**: Mendemonstrasikan kesiapan ekspor laporan fisik untuk rapat manajemen.
- **Langkah Tindakan**:
  - Klik tombol **Print / Save Report** di bagian kanan atas Dashboard Header.
  - Tunjukkan tampilan pratinjau cetak browser (print preview).
  - **Poin Penjelasan**:
    - CSS cetak khusus otomatis menyembunyikan sidebar navigasi, filter pencarian, tombol aksi, serta beralih ke latar belakang putih bersih agar hasil cetak PDF terlihat profesional dan siap dibagikan kepada komisaris.

## 12. Penutup & Rangkuman MVP (Closing)
- **Tujuan**: Menjelaskan batasan sistem saat ini dan mengarahkan diskusi ke validasi masa depan.
- **Poin Penyampaian**:
  - Menjelaskan bahwa fitur-fitur di atas adalah inti dari fase MVP.
  - Membuka sesi tanya jawab menggunakan kuesioner validasi untuk menyepakati fitur pengembangan fase lanjutan.
