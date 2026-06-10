# DOKUMEN MVP LIMITATIONS & BACKLOG - OneSpirit Workflow System

Dokumen ini menjelaskan batasan sistem pada rilis MVP saat ini (Sprint 10 Finalization), risiko penggunaan langsung di lingkungan produksi, rekomendasi perbaikan sebelum Go-Live, serta backlog pengembangan untuk Sprint 11.

---

## 1. Batasan MVP Saat Ini

Sistem saat ini dikembangkan sebagai Minimum Viable Product (MVP) yang fokus pada pembuktian alur bisnis (*proof-of-concept*) dan validasi kegunaan sistem bagi PT One Spirit Asia. Berikut adalah batasan-batasan teknis saat ini:

1. **Security & Cryptography**:
   - Rahasia JWT (*JWT_SECRET*) masih dikonfigurasi menggunakan nilai default development pada `.env.example`.
   - Autentikasi belum dilengkapi dengan fitur Multi-Factor Authentication (MFA) atau pembatasan rate-limiting untuk mencegah serangan brute-force.
2. **Granular Frontend Authorization**:
   - Hak akses role (Admin, PO, PM, Finance, Management) sudah divalidasi dengan ketat pada API Backend. Namun, antarmuka frontend (UI) belum menyembunyikan elemen/tombol menu secara dinamis berdasarkan izin role, melainkan baru memberikan pesan error 403 Forbidden ketika tombol diklik.
3. **Data Loss & Backup Risk**:
   - Sistem belum diintegrasikan dengan cron job backup database otomatis atau replikasi cloud database. Kerusakan container database PostgreSQL dapat menyebabkan kehilangan data lokal jika volume Docker tidak dikelola dengan benar.
4. **No External Integration**:
   - Belum ada integrasi dengan SMTP/Email server untuk mengirim notifikasi penagihan keuangan otomatis atau pengingat instrumen operasional overdue.
   - Ekspor laporan (PNL, ROS, Invoice) masih mengandalkan pencetakan halaman web bawaan browser (Ctrl + P) karena belum tersedianya engine PDF generation di backend.

---

## 2. Risiko Menggunakan Langsung di Production

Sangat **TIDAK DIREKOMENDASIKAN** untuk menggunakan rilis MVP ini langsung di lingkungan produksi PT One Spirit Asia tanpa melakukan langkah-langkah pengerasan keamanan (production hardening). Resiko utama meliputi:
- **Kebocoran Data Komersial**: Jika dideploy dengan default `JWT_SECRET` tanpa HTTPS, penyerang dapat menyadap akses token admin dan mencuri data nilai transaksi, kontak klien, dan laporan laba/rugi PNL.
- **Kerusakan Data Tanpa Recovery**: Tanpa sistem backup terjadwal, kesalahan operasi database atau crash penyimpanan dapat menghapus seluruh riwayat proyek.

---

## 3. Rekomendasi Sebelum Production (Go-Live Checklist)

1. **Production Env Isolation**: Gunakan server database terkelola (seperti AWS RDS PostgreSQL atau Google Cloud SQL) dengan backup otomatis aktif harian.
2. **SSL/TLS Hardening**: Konfigurasikan HTTPS (SSL Certificate dari Let's Encrypt) pada reverse proxy (seperti Nginx atau Caddy) untuk melindungi data lalu lintas API.
3. **Environment Secrets**: Buat skrip deployment yang memasukkan rahasia unik (JWT Secret, Database Passwords) dari runner env (seperti GitHub Secrets atau Cloud Secret Manager) alih-alih menyimpannya di file `.env` lokal.
4. **Rate Limiting**: Tambahkan middleware rate-limiting pada FastAPI backend untuk membatasi request login per menit.

---

## 4. PO Control Center Refactoring Roadmap

Untuk meningkatkan kerapihan kode frontend, view `PoControlCenter.vue` (60KB) yang saat ini terkonsolidasi dalam satu file besar direncanakan untuk dipecah menjadi komponen modular:

- `components/commercial/PoControlSummaryCards.vue` - Menangani visualisasi KPI cards.
- `components/commercial/PoControlFilters.vue` - Panel select filter dan rentang tanggal.
- `components/commercial/FollowUpPriorityList.vue` - Menampilkan daftar kartu prioritas.
- `components/commercial/OwnedProjectsTable.vue` - Tabel daftar proyek PO.
- `components/commercial/QuotationSummary.vue` - Menampilkan perbandingan status quotation.
- `components/commercial/CommercialRevenueSummary.vue` - visualisasi average & conversion rates.
- `components/commercial/PoPerformanceTable.vue` - Tabel beban kerja program owner.
- `components/commercial/SourceContributionTable.vue` - Kontribusi lead partner.
- `components/commercial/CommercialRisksPanel.vue` - Daftar resiko keuangan & data missing.

Refactor ini diutamakan pada awal Sprint 11 setelah validasi fungsional awal disetujui oleh manajemen PT One Spirit Asia.

---

## 5. Rekomendasi Sprint Berikutnya: Sprint 11

### Nama Sprint:
`Sprint 11 — Source & Vendor Performance Center`

### Tujuan Utama:
Meningkatkan analitik komersial dengan memantau tingkat konversi lead partner (*lead source conversion rate*) dan beban kerja kinerja vendor/partner eksternal guna memaksimalkan profitabilitas event.

### Prioritas Backlog Sprint 11:
1. **Source/Vendor Performance Dashboard**: Modul analitik terpusat untuk melihat performance rate vendor eksternal.
2. **Lead Source Conversion Rate**: Analitik persentase konversi inquiry dari media sosial, hotel partner, website, dan repeater.
3. **Vendor Contribution Tracking**: Pencatatan kontribusi keuangan vendor pada PNL proyek.
4. **PO Performance Trend**: Grafik performa historis Program Owner dalam memenangkan deal bulanan.
5. **Project Profitability Refinement**: Perhitungan akurat laba bersih event setelah memperhitungkan biaya vendor aktual vs budget estimasi.
6. **More Granular UI Role Permissions**: Penyembunyian elemen UI dinamis berdasarkan role pengguna.
7. **Export PDF/Reporting Enhancement**: Integrasi pustaka untuk export laporan PNL dan invoice proyek ke format PDF.
