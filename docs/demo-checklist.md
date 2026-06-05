# Checklist Persiapan Demo Klien

Dokumen checklist ini digunakan oleh presenter **GVSys** untuk memastikan seluruh infrastruktur, data, dan skenario demonstrasi berjalan tanpa kendala saat rapat bersama **PT. One Spirit Asia**.

---

## 1. Sebelum Demo (Before Demo)

### A. Infrastruktur & Runtime
- [ ] Pastikan Docker Desktop di laptop presentasi sudah berjalan aktif.
- [ ] Jalankan kontainer sistem dengan bersih:
  ```bash
  docker compose down
  docker compose up -d --build
  ```
- [ ] Verifikasi bahwa semua kontainer berjalan dan berstatus healthy:
  ```bash
  docker compose ps
  ```
- [ ] Uji koneksi endpoint kesehatan backend:
  - Buka browser ke: `http://localhost:8000/health`
  - Pastikan mengembalikan: `{"status":"ok","service":"onespirit-backend"}`
- [ ] Buka dokumentasi API interaktif untuk memastikan backend berfungsi penuh:
  - Buka browser ke: `http://localhost:8000/docs`

### B. Kesiapan Frontend & Login
- [ ] Buka alamat frontend lokal di browser: `http://localhost:5173/`
- [ ] Lakukan uji coba login menggunakan akun Administrator/Manajemen.
- [ ] Uji transisi antar halaman: Dashboard, Projects, CRM (Customers), Imports, dan pastikan tidak ada blank page atau error konsol.

### C. Kesiapan Data & Skenario
- [ ] Buka tab **Imports** dan lakukan import data Excel dari sampel spreadsheet yang valid untuk memastikan database memiliki records proyek.
- [ ] Masuk ke menu Dashboard, periksa apakah charts, KPI cards, tables PO/PM, dan analitik sumber event menampilkan data dan tidak crash/kosong.
- [ ] Siapkan **dua jenis proyek** untuk demo detail:
  1. **Proyek Model Utama (Good Data)**: Proyek dengan data lengkap (Customer, Source, PO, PM, Budget terisi) untuk menunjukkan visualisasi timeline progres proyek yang ideal.
  2. **Proyek Bermasalah (Data Quality Issue)**: Proyek dengan beberapa field kosong (misal: PM belum diisi, drive doc kosong) untuk menunjukkan keandalan panel audit Data Quality.
- [ ] Pastikan setelan printer browser dalam keadaan siap untuk mendemonstrasikan fitur *Print / Save Report* ke file PDF lokal.

---

## 2. Selama Demo (During Demo)

- [ ] Mulai presentasi dengan menceritakan transisi dari proses kerja Excel manual yang rawan kehilangan data menjadi sistem web terpadu.
- [ ] Tunjukkan **Executive Dashboard** terlebih dahulu sebagai pusat kendali evaluasi bisnis manajemen.
- [ ] Perlihatkan kemudahan membaca **Executive Summary Narrative** dan **Management Review Notes** yang otomatis dihasilkan sistem.
- [ ] Demonstrasikan penggunaan filter proyek (misal saring berdasarkan PO atau kategori customer) untuk menunjukkan efisiensi pencarian data.
- [ ] Buka detail salah satu proyek ideal, tunjukkan riwayat log aktivitas (*Activity Log*) dan linimasa status (*Status Timeline*) sebagai fitur transparansi kerja staf.
- [ ] Buka panel **Review Kualitas Data** untuk menunjukkan bagaimana sistem menjaga akurasi anggaran dan administrasi tim.
- [ ] Klik **Print / Save Report** untuk menunjukkan kemudahan mengunduh laporan PDF siap pakai.
- [ ] Masuk ke sesi tanya jawab dan ajukan kuesioner validasi alur kerja kepada perwakilan direksi.

---

## 3. Setelah Demo (After Demo)

- [ ] Catat seluruh masukan, feedback, dan keluhan klien terkait alur kerja status atau pembagian penugasan PO/PM.
- [ ] Lakukan konfirmasi terhadap cakupan fitur MVP (yang disepakati selesai) dan fitur yang digeser ke fase 2 (misal WhatsApp notification, termin payment detail).
- [ ] Dapatkan tanda tangan persetujuan / konfirmasi tertulis via email terkait hasil presentasi sistem sebagai acuan pengerjaan sprint penutup.
