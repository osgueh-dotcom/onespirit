# One Spirit Workflow & Business Analytics System

Sistem manajemen alur kerja operasional dan dashboard evaluasi bisnis berbasis web yang dikembangkan oleh **GVSys (Gueh Visual Systems)** untuk memodernisasi pengelolaan event dan proyek di **PT. One Spirit Asia**.

Sistem ini mendigitalisasi alur kerja manual berbasis spreadsheet Excel lama menjadi aplikasi web terintegrasi dengan database relasional terpusat serta dashboard analitik eksekutif.

---

## 1. Panduan Menjalankan Sistem Secara Lokal (Local Running Environment)

Sistem saat ini disiapkan sebagai **working local MVP (prototype)** untuk divalidasi secara lokal menggunakan Docker Desktop:

### Langkah Menjalankan:
Jalankan perintah berikut di direktori root proyek melalui terminal:
```bash
docker compose down
docker compose up -d --build
```

### Verifikasi Kesehatan Layanan (Health Checks):
- Pastikan status semua layanan kontainer aktif dan berjalan:
  ```bash
  docker compose ps
  ```
- **Backend API Diagnostics**: Akses `http://localhost:8000/health` di browser. Harus mengembalikan respon:
  ```json
  {"status":"ok","service":"onespirit-backend"}
  ```
- **Dokumentasi API Interaktif**: Akses `http://localhost:8000/docs` untuk melihat Swagger OpenAPI endpoints.

---

## 2. Alamat Port Layanan Utama

| Layanan (Service) | URL Lokal (Local URL) | Konteks & Kegunaan |
| :--- | :--- | :--- |
| **Frontend Web App** | [http://localhost:5173/](http://localhost:5173/) | Papan alur proyek, Dashboard Eksekutif, Impor Excel |
| **Backend REST API** | [http://localhost:8000/](http://localhost:8000/) | Layanan server backend (FastAPI) |
| **API Docs (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) | Dokumentasi teknis endpoints pengembang |
| **Layanan Diagnostics** | [http://localhost:8000/health](http://localhost:8000/health) | Status kesehatan sistem |

*Catatan: Akun login administrator awal telah disiapkan di database seed bawaan.*

---

## 3. Aset Pendukung Demonstrasi & Penyelarasan Klien

Untuk mendukung jalannya presentasi di hadapan direksi PT. One Spirit Asia, gunakan dokumen panduan di folder `docs/` dengan tautan relatif berikut:

- **[Panduan Posisi Demo (Demo Positioning)](docs/demo-positioning.md)**: Konsep menyajikan aplikasi sebagai working local MVP untuk validasi kebutuhan bisnis.
- **[Glosarium Istilah Operasional (One Spirit Glossary)](docs/onespirit-terminology.md)**: Daftar istilah domain (PO, PM, Sales, PNL, CL, ROS, CK) dan model penugasan dinamisnya.
- **[Alur Demo Langkah Demi Langkah](docs/client-demo-flow.md)**: Panduan alur navigasi menu selama demo berlangsung.
- **[Skrip Demonstrasi (Speech Script)](docs/demo-script.md)**: Template panduan percakapan presenter dalam bahasa Indonesia yang terstruktur.
- **[Daftar Periksa Persiapan (Checklist)](docs/demo-checklist.md)**: Checklist teknis sebelum, selama, dan sesudah rapat demo berjalan.
- **[Panduan Memilih Data Demo](docs/demo-data-recommendation.md)**: Rekomendasi data sampel ideal vs data peringatan masalah administrasi.
- **[Penyelarasan Proposal Teknis](docs/proposal-alignment.md)**: Pemetaan fitur proposal terhadap status implementasi sistem (lingkup MVP).
- **[Cakupan Sistem MVP & Fase Lanjutan](docs/mvp-scope.md)**: Daftar fitur yang tersedia di MVP vs fitur yang direkomendasikan masuk Fase 2 (termin billing, WhatsApp).
- **[Daftar Pertanyaan Validasi Klien](docs/client-validation-questions.md)**: Kuesioner interaktif untuk menyelaraskan alur kerja nyata dengan logika sistem.
- **[Batasan Fungsional MVP](docs/known-limitations-before-client-demo.md)**: Dokumen batasan sistem dalam bahasa bisnis yang aman bagi klien.

Indeks lengkap seluruh log teknis pengembang dari Sprint 0 hingga Sprint 10.1 dapat diakses melalui **[Dokumentasi Indeks Utama](docs/README.md)**.

---

## 4. Pusat Kontrol Utama (Current Control Centers)

Sistem One Spirit menyediakan tiga panel kontrol utama yang dirancang untuk kebutuhan pengguna yang berbeda:

- **Executive Dashboard**
  Berfokus pada evaluasi manajemen senior dan direksi, menampilkan target pendapatan, Target Achievement Rate, Received Cash, Collection Rate, sisa piutang, dan narasi evaluasi bahasa Indonesia otomatis.
- **PM Control Center**
  Workspace operasional bagi Program Manager (PM) untuk memantau kesiapan proyek, jadwal event mendatang, alarm instrumen overdue/revisi, dan prioritas tindakan operasional (Critical, High, Medium, Low).
- **PO Control Center**
  Workspace komersial bagi Program Owner (PO) untuk memantau quotation, deal/cancel rate, confirmed vs potential revenue, outstanding payment exposure, prioritas follow-up tindakan komersial, dan kontribusi lead source/vendor.

---

## 5. Batasan Tahap MVP Awal
- **Uji Coba Lokal**: Sistem dikonfigurasi untuk dijalankan secara lokal via kontainer Docker. Pemasangan server awan (cloud hosting) dan sistem pencadangan terpusat direkomendasikan pada fase lanjutan.
- **Validasi Data Awal**: Database relasional lokal diisi oleh data uji coba operasional bawaan. Migrasi database final akan disesuaikan setelah struktur data divalidasi bersama klien.
