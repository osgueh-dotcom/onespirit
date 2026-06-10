# CHANGELOG - OneSpirit Workflow System

Semua perubahan penting pada project ini dicatat di dokumen ini.

---

## [Sprint 10.2] - 2026-06-10

### Added
- Membuat dokumen baru `docs/demo-readiness.md` berisi panduan demo operasional 15-30 menit, data dummy, peran pengguna, dan pertanyaan umpan balik klien.
- Membuat dokumen baru `docs/mvp-limitations.md` berisi batasan MVP saat ini, risiko keamanan, rekomendasi rilis produksi, dan backlog Sprint 11.

### Changed
- Mengganti seluruh placeholder pada dokumen `README.md`, `PROJECT_CONTEXT.md`, `SPRINT_LOG.md`, dan `CHANGELOG.md` dengan informasi nyata yang mendeskripsikan stack teknologi, istilah bisnis (CL/ROS/CK/PNL), dan alur operasional PT One Spirit Asia.
- Menambahkan roadmap refactoring komponen komersial sebagai dokumentasi JSDoc di file frontend `frontend/src/views/PoControlCenter.vue` untuk modularisasi 9 sub-komponen pada Sprint 11.

### Fixed
- Memperbaiki kegagalan koneksi database pada unit testing backend di Windows dengan membuat folder `E:\tmp` secara otomatis untuk SQLite db.
- Menambahkan pemeriksaan runtime pytest di `backend/app/main.py` sehingga server testing mengabaikan koneksi ke PostgreSQL dan dapat berjalan murni secara lokal menggunakan SQLite.

### Security
- Menambahkan filter `*.env` dan direktori `uploads/`, `backend/app/uploads/` pada file `.gitignore` untuk mencegah kebocoran data sensitif operasional dan file rahasia lokal ke repositori git.
- Melakukan review pada file `.env.example` untuk menjamin tidak ada credentials / JWT secrets riil yang tersimpan di repositori.
- Menambahkan dokumentasi yang memperingatkan evaluator mengenai kredensial admin default (`admin@onespirit.asia` / `OneSpirit2026!`) yang hanya diperuntukkan bagi lingkungan demo/development.

---

## [Sprint 10.1] - 2026-06-09

### Added
- Penambahan filter komersial tingkat lanjut di PO Control Center.
- Panel pendeteksi resiko komersial (proyek batal tanpa alasan, deal dengan budget Rp 0, outstanding payment, missing PO / Lead Source).

### Changed
- Pembenahan antarmuka PO Control Center dengan styling glassmorphism yang seragam.

---

## [Sprint 10.0] - 2026-06-08

### Added
- Inisialisasi awal PO Control Center (Program Owner Dashboard).
- Statistik nilai proyek rata-rata dan tingkat konversi deal rate.

---

## [Sprint 9.0] - 2026-06-05

### Added
- PM Control Center Dashboard untuk Program Manager.
- Perhitungan readiness score berdasarkan kelengkapan instrumen operasional (CL, ROS, CK, PNL).
- Deteksi overdue instruments dan timeline visual event operasional.

---

## [Sprint 6.0] - 2026-06-02

### Added
- Modul import data masal dari template Excel untuk migrasi data proyek historis.
- Validasi kualitas data otomatis saat upload file Excel.

---

## [Sprint 2.0] - 2026-05-25

### Added
- Modul inti CRM (Customer Relationship Management) dan Proyek/Event.
- Pelacakan status transisi siklus hidup proyek (Inquiry -> Closed).
