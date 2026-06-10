# CHANGELOG - OneSpirit Workflow System

Semua perubahan penting pada project ini dicatat di dokumen ini.

---

## [Sprint 12.2] - 2026-06-11

### Added
- Membuat file GitHub Actions workflow `.github/workflows/deploy-pages.yml` untuk build dan deploy frontend otomatis ke GitHub Pages.
- Membuat file `.env.production.example` di folder `frontend` untuk template setup URL backend tunnel.
- Membuat dokumen panduan deployment `docs/github-pages-demo-deployment.md`.
- Membuat dokumen panduan arsitektur demo `docs/demo-architecture.md`.

### Changed
- Mengonfigurasi `base: '/onespirit/'` pada `frontend/vite.config.js` agar resource dan file statis dimuat relatif ke path GitHub Pages.
- Mengubah Vue Router ke mode Hash routing (`createWebHashHistory()`) di `frontend/src/router/index.js` untuk mencegah error 404 pada routing static hosting.
- Mengatur global baseURL Axios menggunakan environment variable `VITE_API_BASE_URL` di `frontend/src/main.js`.
- Memperbarui `docs/public-demo-safety-checklist.md` untuk melengkapi instruksi CORS dengan origin `https://osgueh-dotcom.github.io`.
- Memperbarui `README.md` dan `PROJECT_CONTEXT.md` dengan informasi deployment.

## [Sprint 12.1] - 2026-06-11

### Added
- Membuat dokumen `docs/public-demo-safety-checklist.md` untuk panduan keamanan demo.
- Membuat dokumen `docs/client-demo-rehearsal.md` berisi panduan rehearsal skrip presentasi 15-25 menit.
- Membuat dokumen `docs/client-feedback-form.md` berisi form kuesioner masukan klien.

### Changed
- Mengintegrasikan akun demo klien `demo@onespirit.asia` / `OneSpiritDemo2026!` dengan role Management.
- Menambahkan izin `documents:write` pada Management role agar akun demo klien dapat menguji alur upload dokumen.
- Menerjemahkan metrik penjualan, filter, loading indicators, table headers, dan button keluar (Sign Out -> Keluar) ke bahasa Indonesia profesional di seluruh views.
- Memperbarui `README.md` dan `PROJECT_CONTEXT.md` dengan detail akun demo klien dan dokumentasi baru.

### Fixed
- Menolak default password akun super admin/demo jika berjalan di environment `production` dengan ValueError validation.

## [Sprint 12] - 2026-06-11

### Added
- Membuat komponen-komponen UI bersama di `frontend/src/components/ui/` seperti `AppPageHeader.vue`, `AppStatCard.vue`, `AppStatusBadge.vue`, `AppEmptyState.vue`, `AppLoadingState.vue`, `AppErrorState.vue`.
- Menyediakan layout alternatif (card list fallback) di resolusi mobile untuk seluruh tabel penting (Kanban projects, PM Control Center, PO Control Center, Source & Vendor performance, Finance, Imports, dan CRM) guna mencegah layout breakage pada lebar minimal 360px.
- Membuat panduan presentasi klien di `docs/ui-ux-presentation-readiness.md`.

### Changed
- Memperbarui global navigasi utama di `App.vue` dengan pengelompokan menu komersial/operasional dan integrasi drawer sidebar mobile.
- Mengganti label teknis bahasa Inggris menjadi microcopy bahasa Indonesia yang ramah pengguna operasional.
- Menyempurnakan filter responsif di PM Control Center, PO Control Center, dan CRM.

## [Sprint 11] - 2026-06-10

### Added
- Membuat endpoint baru `/api/v1/dashboard/source-vendor-performance` untuk melacak kinerja lead source dan vendor.
- Membuat halaman frontend baru `SourceVendorPerformance.vue` yang menampilkan dashboard metrik kinerja source, vendor partner, alokasi PO + Source, panel alert risiko, dan kualitas data.
- Menambahkan route `/source-vendor-performance` dan menu navigasi bersimbol `ChartBarIcon` ke sidebar utama.
- Membuat dokumen logika analitik dan fallback di `docs/source-vendor-performance-logic.md`.
- Menambahkan unit testing backend `/dashboard/source-vendor-performance` pada `backend/app/tests/test_source_vendor_performance.py` untuk memvalidasi perhitungan metrik komersial, pengecualian pembatalan, dan perhitungan konversi secara presisi.

### Changed
- Memperbarui `PROJECT_CONTEXT.md` untuk mengintegrasikan modul Source & Vendor Performance Center ke daftar fitur utama.
- Memperbarui batasan vendor pada `docs/mvp-limitations.md` untuk memperjelas keterbatasan data vendor yang masih berupa field teks pada tabel EventSource.

## [Sprint 10 Finalization] - 2026-06-10

### Added
- Melengkapi API response schema PO Control Center di backend dengan 6 metrik komersial baru: `active_projects`, `pending_quotation_projects`, `follow_up_needed_projects`, `cancelled_projects`, `outstanding_payment`, dan `commercial_risk_count`.
- Membuat file panduan logika komersial `docs/commercial-control-logic.md` untuk memperjelas metode perhitungan revenue potensial vs terkonfirmasi, tagihan outstanding, serta penanganan resiko data.
- Membuat dokumen baru `docs/demo-readiness.md` berisi panduan demo operasional 15-30 menit, data dummy, peran pengguna, dan pertanyaan umpan balik klien.
- Membuat dokumen baru `docs/mvp-limitations.md` berisi batasan MVP saat ini, risiko keamanan, rekomendasi rilis produksi, dan backlog Sprint 11.

### Changed
- Memperbarui antarmuka card Outstanding Pembayaran pada `PoControlCenter.vue` untuk merender nilai mata uang IDR riil, bukan sekadar jumlah klien.
- Mengganti seluruh placeholder pada dokumen `README.md`, `PROJECT_CONTEXT.md`, `SPRINT_LOG.md`, dan `CHANGELOG.md` dengan informasi nyata yang mendeskripsikan stack teknologi, istilah bisnis (CL/ROS/CK/PNL), dan alur operasional PT One Spirit Asia.
- Melakukan refactor minimal pada `PoControlCenter.vue` dengan mengekstrak modul visual komersial menjadi 4 subkomponen terpisah di bawah `frontend/src/components/commercial/`: `PoControlSummaryCards.vue`, `PoControlFilters.vue`, `FollowUpPriorityList.vue`, dan `CommercialRisksPanel.vue`. Ini menyederhanakan file utama dari 900+ baris menjadi 500 baris dengan komunikasi event emitter Vue 3.

### Fixed
- Memperbaiki kegagalan koneksi database pada unit testing backend di Windows dengan membuat folder `E:\tmp` secara otomatis untuk SQLite db.
- Menambahkan pemeriksaan runtime pytest di `backend/app/main.py` sehingga server testing mengabaikan koneksi ke PostgreSQL dan dapat berjalan murni secara lokal menggunakan SQLite.
- Membersihkan dan memperbaiki semua absolute local path link (seperti `file:///e:/...`) menjadi relative path link di seluruh file dokumentasi markdown.
- Menambahkan stylesheet optimasi cetak `@media print` A4 landscape pada file css utama `frontend/src/assets/index.css` agar cetak cetak halaman/Save-as-PDF (Ctrl+P) otomatis menghasilkan layout laporan yang premium, bersih, dan bebas dari elemen navigasi sidebar/navbar/tombol.

### Security
- Menambahkan filter `*.env` dan direktori `uploads/`, `backend/app/uploads/` pada file `.gitignore` untuk mencegah kebocoran data sensitif operasional dan file rahasia lokal ke repositori git.
- Melakukan review pada file `.env.example` untuk menjamin tidak ada credentials / JWT secrets riil yang tersimpan di repositori, serta menambahkan placeholder konfigurasi `ADMIN_EMAIL` dan `ADMIN_PASSWORD`.
- Menambahkan dokumentasi yang memperingatkan evaluator mengenai kredensial admin default (`admin@onespirit.asia` / `OneSpirit2026!`) yang hanya diperuntukkan bagi lingkungan demo/development.
- Memindahkan kredensial Super Admin seeding dari kode database seed (`auth/service.py`) ke environment variables (`ADMIN_EMAIL` & `ADMIN_PASSWORD`) di config Settings, serta memvalidasi perubahan password tersebut pada environment `production` guna menghindari celah keamanan.

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
