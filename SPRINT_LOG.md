# SPRINT LOG - OneSpirit Workflow System

Dokumen ini digunakan untuk mencatat riwayat sprint pengembangan OneSpirit Workflow System, mencakup tujuan, hasil implementasi, dan status verifikasi.

---

## Ringkasan Perjalanan Sprint

| Sprint | Judul / Fokus Utama | Tanggal | Status |
|---|---|---|---|
| **Sprint 0** | Project Documentation Foundation & Tech Archetype | 2026-05-15 | Done |
| **Sprint 1** | Domain Refactoring & DB Schema Alignment | 2026-05-20 | Done |
| **Sprint 2** | Core Workflow & CRM Management | 2026-05-25 | Done |
| **Sprint 3** | Project lifecycle & Status Transitions | 2026-05-30 | Done |
| **Sprint 4** | Readiness gates implementation (CL, ROS, CK, PNL) | 2026-06-01 | Done |
| **Sprint 5** | Finance tracking, invoices & payments integration | 2026-06-03 | Done |
| **Sprint 6** | Excel Import modules for mass data migration | 2026-06-04 | Done |
| **Sprint 7** | PM Control Center & Operational Workload Dashboard | 2026-06-05 | Done |
| **Sprint 8** | PO Control Center & Commercial Dashboard | 2026-06-07 | Done |
| **Sprint 9** | Bug Fixing & UI Polishing | 2026-06-08 | Done |
| **Sprint 10** | PO Control Center Commercial Follow-up & Risks | 2026-06-09 | Done |
| **Sprint 10.1** | Documentation & Commercial Control Cleanup | 2026-06-09 | Done |
| **Sprint 10 Finalization** | Commercial Control Stabilization & MVP Demo Readiness | 2026-06-10 | Done |
| **Sprint 11** | Source & Vendor Performance Center | 2026-06-10 | Done |
| **Sprint 12.2** | GitHub Pages Demo Deployment | 2026-06-11 | Done |
| **Sprint 12.1** | Client Demo Polish & Presentation Rehearsal | 2026-06-11 | Done |
| **Sprint 12** | UI/UX Client Presentation & Responsive Experience | 2026-06-11 | Done |

---

---

## Sprint 12.2 — GitHub Pages Demo Deployment

Tanggal: 2026-06-11  
Status: Done  
AI Agent: Antigravity  
Branch: sprint-12-ui-ux-presentation-readiness  
Commit: Sprint 12.2: configure GitHub Pages frontend deployment workflow  

### Tujuan

Mengonfigurasi frontend agar dapat dideploy ke GitHub Pages secara otomatis via GitHub Actions dan menghubungkannya dengan API backend lokal menggunakan secure tunnel.

### Scope

- **Vite Path**: Menambahkan `base: '/onespirit/'` pada `frontend/vite.config.js`.
- **Router Hash Mode**: Mengubah router mode ke `createWebHashHistory()` di `frontend/src/router/index.js` untuk mencegah error 404 pada GitHub Pages.
- **Axios Configuration**: Mengatur global `baseURL` Axios dengan `import.meta.env.VITE_API_BASE_URL` di `frontend/src/main.js`.
- **Environment Example**: Membuat file `frontend/.env.production.example` sebagai referensi setup backend tunnel URL.
- **GitHub Actions**: Membuat `.github/workflows/deploy-pages.yml` menggunakan Node 22 dan `actions/deploy-pages@v4`.
- **Documentation**: Membuat panduan `docs/github-pages-demo-deployment.md`, panduan arsitektur hibrida `docs/demo-architecture.md`, dan memperbarui `docs/public-demo-safety-checklist.md` dengan CORS requirement.

### Di Luar Scope

- Tidak men-deploy backend dan database ke GitHub Pages.
- Tidak menyertakan database credentials atau JWT secrets ke dalam file frontend.

### File/Modul Terkait

- `frontend/vite.config.js`
- `frontend/src/router/index.js`
- `frontend/src/main.js`
- `frontend/.env.production.example`
- `.github/workflows/deploy-pages.yml`
- `docs/github-pages-demo-deployment.md`
- `docs/demo-architecture.md`
- `docs/public-demo-safety-checklist.md`

### Hasil Implementasi

1. **SPA Route Stability**: Hash routing berhasil diimplementasikan, sehingga navigasi URL (misalnya `#/login`) berjalan lancar di static site hosting tanpa 404 error saat direfresh.
2. **Flexible API Target**: Frontend dapat dideploy satu kali dan dikoneksikan ke berbagai dynamic tunnel URL (VS Code / ngrok) hanya dengan memperbarui GitHub repository secret `VITE_API_BASE_URL`.
3. **CORS Security**: Didefinisikan aturan origin CORS baru di backend untuk menerima request dari `https://osgueh-dotcom.github.io`.

### Test Yang Dilakukan (Sprint 12.2 Validation)

Backend:
- Command: `pytest app/tests -q` (run di backend folder)
- Result: Sukses melewati seluruh tes.

Frontend:
- Command: `npm run build` (run di frontend folder)
- Result: Build berhasil tanpa warning.

---

## Sprint 12.1 — Client Demo Polish & Presentation Rehearsal

Tanggal: 2026-06-11  
Status: Done  
AI Agent: Antigravity  
Branch: sprint-12-ui-ux-presentation-readiness  
Commit: Sprint 12.1: polish client demo and rehearsal readiness  

### Tujuan

Polishing, rehearsal, microcopy, responsive QA, demo account setup, dan safety checklist untuk persiapan demo presentasi klien.

### Scope

- **Keamanan Demo**: Membuat panduan kepatuhan keamanan demo di `docs/public-demo-safety-checklist.md`.
- **Rehearsal Script**: Menyusun skrip presentasi langkah-demi-langkah (15-25 menit) di `docs/client-demo-rehearsal.md`.
- **Feedback Form**: Menyediakan formulir umpan balik klien di `docs/client-feedback-form.md`.
- **Demo Account**: Mengonfigurasi akun `demo@onespirit.asia` dengan password default dan mengaitkannya ke role Management dengan akses dokumen tambahan.
- **Indonesian Translation**: Menerjemahkan semua views frontend (metrik, tombol, status, filter) ke bahasa Indonesia profesional.
- **Password Safety**: Menambahkan validasi backend untuk menolak password default admin/demo di production environment.

### File/Modul Terkait

- `docs/public-demo-safety-checklist.md`
- `docs/client-demo-rehearsal.md`
- `docs/client-feedback-form.md`
- `backend/app/modules/auth/router.py`
- `frontend/src/views/` (seluruh views)

### Test Yang Dilakukan (Sprint 12.1 Validation)

Backend:
- Command: `pytest app/tests -q`
- Result: 17 passed

Frontend:
- Command: `npm run build`
- Result: Build sukses

---

## Sprint 12 — UI/UX Client Presentation & Responsive Experience

Tanggal: 2026-06-11  
Status: Done  
AI Agent: Antigravity  
Branch: main  
Commit: Sprint 12: improve UI/UX and mobile responsive layout  

### Tujuan

Meningkatkan tampilan, pengalaman pengguna, navigasi, keterbacaan data, dan responsive layout agar OneSpirit Workflow siap dipresentasikan ke client dan nyaman digunakan di PC maupun mobile.

### Scope

- **Shared UI Components**: Menggunakan AppPageHeader, AppStatCard, AppEmptyState, AppLoadingState, dan AppErrorState secara konsisten.
- **Global Layout & Navigation**: Menyempurnakan navigasi di `App.vue` dengan pengelompokan menu bisnis riil dan hamburger sidebar drawer yang optimal untuk perangkat mobile.
- **Responsive Layout Fallbacks**: Membuat tampilan card list responsif (`block md:hidden`) untuk tabel-tabel kompleks pada resolusi mobile (Kanban projects, PM Control tables, PO Control tables, Source & Vendor tables, Finance ledger, Import previews, dan CRM).
- **Indonesian Microcopy**: Mengubah label teknis bahasa Inggris menjadi microcopy operasional bahasa Indonesia yang ramah pengguna.
- **Documentation**: Membuat dokumen kesiapan presentasi klien `docs/ui-ux-presentation-readiness.md` dan memperbarui logs perubahan.

### Di Luar Scope

- Tidak menambahkan fitur bisnis atau modul fungsional baru.
- Tidak mengubah database schema backend.

### File/Modul Terkait

- `frontend/src/views/PmControlCenter.vue`
- `frontend/src/views/PoControlCenter.vue`
- `frontend/src/views/SourceVendorPerformance.vue`
- `frontend/src/views/Finance.vue`
- `frontend/src/views/Imports.vue`
- `frontend/src/views/CRM.vue`
- `frontend/src/components/commercial/PoControlSummaryCards.vue`
- `docs/ui-ux-presentation-readiness.md`
- `SPRINT_LOG.md`
- `CHANGELOG.md`
- `PROJECT_CONTEXT.md`

### Hasil Implementasi

1. **Responsivitas Viewport 360px**: Seluruh halaman dapat diakses dengan nyaman di perangkat ponsel cerdas tanpa ada layout breaking atau horizontal overflow.
2. **Kesesuaian Istilah Bisnis**: Navigasi dan label-label telah diselaraskan dengan terms PNL, CL, ROS, CK.
3. **Kombinasi Dual Tampilan**: Data tabel penuh dipertahaman untuk PC eksekutif, dan diubah menjadi card grid yang indah di layar mobile.

### Test Yang Dilakukan (Sprint 12 Validation)

Backend:
Command:
pytest app/tests -q (run in backend dir)
Result:
17 passed, 903 warnings

Frontend:
Command:
npm run build (run in frontend dir)
Result:
build success

---

## Sprint 11 — Source & Vendor Performance Center

Tanggal: 2026-06-10  
Status: Done  
AI Agent: Antigravity  
Branch: sprint-11-source-vendor-performance  
Commit: Sprint 11: add source and vendor performance center  

### Tujuan

Membangun Source & Vendor Performance Center untuk membantu management/owner/PO melihat performa sumber proyek (lead source), vendor partner, conversion rate, revenue contribution, commercial risk, dan follow-up priority berdasarkan data proyek yang sudah ada.

### Scope

- **Backend Module**: Menambahkan endpoint `/api/v1/dashboard/source-vendor-performance` dan service layer `source_vendor_service.py` untuk mengagregasi data proyek, conversion rate, cancellation rate, outstanding payments, risk alerts, serta kualitas data lead source dan vendor.
- **Frontend Dashboard**: Membuat halaman `/source-vendor-performance` dengan layout premium (glassmorphism), menampilkan summary cards, tabel kinerja source, tabel kinerja vendor partner (dengan fallback aman karena nama vendor belum terstruktur penuh), alokasi PO + Source, panel alert risiko komersial, dan audit kualitas data.
- **Unit Testing**: Membuat berkas pengujian `test_source_vendor_performance.py` untuk memverifikasi fungsionalitas kalkulasi dan response contract API.
- **Documentation**: Menyusun panduan kalkulasi bisnis di `docs/source-vendor-performance-logic.md` dan memperbarui daftar batasan di `docs/mvp-limitations.md`.

### Di Luar Scope

- Tidak menormalisasi tabel database vendor partner pada sprint ini (menggunakan field textual `vendor_name` di tabel `EventSource`).
- Tidak membuat relasi entitas baru antara Project dan Vendor secara terpisah.

### File/Modul Terkait

- `backend/app/modules/dashboard/schemas.py`
- `backend/app/modules/dashboard/router.py`
- `backend/app/modules/dashboard/source_vendor_service.py`
- `backend/app/tests/test_source_vendor_performance.py`
- `frontend/src/views/SourceVendorPerformance.vue`
- `frontend/src/router/index.js`
- `frontend/src/App.vue`
- `docs/source-vendor-performance-logic.md`
- `docs/mvp-limitations.md`
- `PROJECT_CONTEXT.md`
- `SPRINT_LOG.md`
- `CHANGELOG.md`

### Hasil Implementasi

1. **Endpoint Kinerja Source & Vendor Aktif**: API `/api/v1/dashboard/source-vendor-performance` mengembalikan data dengan penanganan pembagian dengan nol (division-by-zero protection) dan isolasi status proyek batal/confirmed yang tepat.
2. **Dashboard UI Interaktif**: Pengguna dapat memfilter berdasarkan PO, rentang tanggal event, serta menyertakan proyek closed/batal secara real-time.
3. **Peringatan Risiko & Audit Kualitas**: Sistem mendeteksi jika rasio proyek batal tinggi, outstanding tagihan bernilai besar, atau ada proyek berjalan tanpa mapping lead source/vendor.

### Test Yang Dilakukan (Sprint 11 Validation)

Tanggal Pengujian: 2026-06-10

Backend:
Command:
pytest app/tests/test_source_vendor_performance.py -q
Result:
1 passed

Frontend:
Command:
cmd /c npm run build
Result:
build success

Docker:
Command:
docker compose up --build
Result:
Sistem container berjalan sehat dan sinkron.

---

## Sprint 10 Finalization — Commercial Control Stabilization & MVP Demo Readiness

Tanggal: 2026-06-10  
Status: Done  
AI Agent: Antigravity  
Branch: main  
Commit: Sprint 10: stabilize commercial control and prepare MVP demo

### Tujuan

Menstabilkan fitur komersial, melengkapi metrik PO Control Center, merapikan dokumentasi root dan folder docs, menjaga keamanan configuration, serta memvalidasi kesiapan unit tests dan frontend build agar OneSpirit Workflow siap menjadi MVP demo yang profesional bagi PT One Spirit Asia.

### Scope

- **Commercial Control Stabilization**: Menambahkan 6 metrik baru ke backend PO Control Center (`active_projects`, `pending_quotation_projects`, `follow_up_needed_projects`, `cancelled_projects`, `outstanding_payment`, `commercial_risk_count`) dan memperbarui endpoint dan model Pydantic.
- **Frontend KPI Card Update**: Memodifikasi template `PoControlCenter.vue` pada card Outstanding Pembayaran untuk menampilkan nilai nominal mata uang IDR riil, disertai jumlah klien dalam tanda kurung.
- **New Commercial Control Documentation**: Membuat dokumen baru `docs/commercial-control-logic.md` yang merinci formula bisnis, definisi status, sumber data, dan fallback untuk ketidaklengkapan data.
- **Documentation Cleanup**: Menghapus semua placeholder di `README.md`, `PROJECT_CONTEXT.md`, `SPRINT_LOG.md`, dan `CHANGELOG.md` serta menyinkronkan isinya dengan kondisi terkini.
- **Security & Config Audit**: Memastikan `.gitignore` melindungi file `.env`, file database local SQLite, dan upload media. Memastikan `.env.example` aman tanpa kredensial asli.
- **Test & Build Verification**: Menghindari crash PostgreSQL pada pytest run dengan mendeteksi mode runtime pytest di `main.py`, membuat folder SQLite `E:\tmp` otomatis, dan menjalankan unit test PO Control Center dengan assertions metrik baru. Menjalankan production build Vue 3 via Vite.

### Di Luar Scope

- Tidak menambahkan fitur baru besar di luar stabilisasi commercial control.
- Tidak mendesain ulang arsitektur sistem.

### File/Modul Terkait

- `backend/app/modules/dashboard/schemas.py`
- `backend/app/modules/dashboard/po_control_service.py`
- `backend/app/tests/test_po_control_center.py`
- `frontend/src/views/PoControlCenter.vue`
- `docs/commercial-control-logic.md`
- `docs/demo-readiness.md`
- `docs/mvp-limitations.md`
- `README.md`
- `PROJECT_CONTEXT.md`
- `SPRINT_LOG.md`
- `CHANGELOG.md`
- `.gitignore`
- `.env.example`

### Hasil Implementasi

1. **PO Control Center Stabil**: Endpoint backend dan UI frontend terintegrasi penuh untuk metrik komersial riil tanpa angka palsu/placeholder. Outstanding payment terhitung dari selisih nominal invoice terbit dikurangi payment disetujui (`status = 'approved'`).
2. **Commercial Logic Terarsip**: Panduan formula komersial telah dibuat di [commercial-control-logic.md](docs/commercial-control-logic.md).
3. **Test Suite 100% Pass**: Seluruh 16 unit tests backend berhasil dijalankan dengan SQLite secara lokal dan lulus 100%.
4. **Frontend Build Sukses**: Vite production build berhasil mengompilasi aset Vue 3 secara sempurna dengan command `npm.cmd run build`.
5. **Keamanan Konfigurasi Terjaga**: File `.env` terabaikan di git, dan default credentials demo/development terdokumentasi dengan warning yang jelas.

### Test Yang Dilakukan (Sprint 10 Final Validation)

Tanggal Pengujian: 2026-06-10

Backend:
Command:
pytest app/tests -q
Result:
16 passed

Frontend:
Command:
npm run build
Result:
build success

Docker:
Command:
docker compose up --build
Result:
backend, frontend, database running

Manual Regression Check:
Diverifikasi via agen browser otomatis untuk menguji demo/handover flow:
- Login berhasil menggunakan akun `admin@onespirit.asia`.
- Executive Dashboard memuat metrik secara normal.
- Projects Kanban Board menampilkan data proyek dengan benar.
- PM Control Center memuat operational readiness scoring dan checklist.
- PO Control Center (refactored) merender visual dashboard, filter dropdown, prioritas follow-up, daftar proyek, kinerja komersial, dan risiko komersial (`CommercialRisksPanel`) tanpa error runtime/JS console.
- Excel Migration & Sync Hub (Imports page) memuat drop-zone dengan aman.

### Penanganan Risiko Teridentifikasi (Mitigated & Resolved)

1. **Kredensial Super Admin Seeding**:
   - **Risiko**: Sebelumnya data kredensial super admin demo (`admin@onespirit.asia` / `OneSpirit2026!`) di-hardcode secara statis dalam kode database seeding.
   - **Mitigasi**: Telah dipindahkan ke konfigurasi environment variables (`ADMIN_EMAIL`, `ADMIN_PASSWORD`) yang dimuat secara dinamis.
   - **Validasi Produksi**: Sistem akan menolak untuk start (ValueError) pada environment `production` jika password super admin masih menggunakan nilai default `OneSpirit2026!` atau `JWT_SECRET` belum diubah.
2. **Cetak Laporan Premium**:
   - **Risiko**: Cetak laporan operasional dan komersial (ROS, PNL) masih menggunakan browser print dan hasilnya berpotensi berantakan.
   - **Mitigasi**: Ditambahkan print stylesheet khusus A4 landscape pada `frontend/src/assets/index.css`. Pengguna kini dapat mencetak laporan premium secara rapi dan bersih (menyembunyikan sidebar, navbar, dropdown, tombol, dan menyesuaikan layout) menggunakan pintasan bawaan `Ctrl+P` browser untuk cetak fisik atau Save as PDF.

---

## Sprint 12.1 — Client Demo Polish & Presentation Rehearsal

Tanggal: 2026-06-11  
Status: Done  
AI Agent: Antigravity  
Branch: sprint-12-1-client-demo-polish  
Commit: Sprint 12.1: polish client demo and rehearsal readiness

### Tujuan

Meningkatkan kesiapan presentasi klien MVP dengan memperluas visualisasi bahasa Indonesia profesional (microcopy), memperkuat responsive layout hingga 360px viewport, menyiapkan dan mengamankan akun demo klien (`demo@onespirit.asia`), serta melengkapi dokumentasi safety, rehearsal flow, dan feedback capture.

### Scope

- **Demo Account Setup**: Menyiapkan variabel `DEMO_EMAIL` dan `DEMO_PASSWORD` pada `config.py` dan `.env`, menambahkan validasi keamanan produksi, menambahkan izin `documents:write` pada Management role, dan melakukan seeding akun demo klien secara otomatis pada startup database.
- **UI/UX Microcopy Polish**: Menerjemahkan teks antarmuka utama (Sign Out -> Keluar, filter dropdowns, loading indicators, table headers, empty states) ke dalam bahasa Indonesia profesional yang konsisten pada semua halaman view.
- **Documentation Sync**: Membuat dokumen `docs/public-demo-safety-checklist.md`, `docs/client-demo-rehearsal.md`, `docs/client-feedback-form.md`, serta menyelaraskan links pada `README.md` dan `PROJECT_CONTEXT.md`.
- **Test & Validation**: Menjalankan unit tests backend (17 passed) dan build frontend Vite.

### File/Modul Terkait

- `backend/app/core/config.py`
- `backend/app/modules/auth/service.py`
- `frontend/src/views/Login.vue`
- `frontend/src/views/Dashboard.vue`
- `frontend/src/views/Projects.vue`
- `frontend/src/views/ProjectDetail.vue`
- `frontend/src/views/PoControlCenter.vue`
- `frontend/src/views/SourceVendorPerformance.vue`
- `frontend/src/views/Finance.vue`
- `frontend/src/views/CRM.vue`
- `frontend/src/views/Documents.vue`
- `frontend/src/App.vue`
- `docs/public-demo-safety-checklist.md`
- `docs/client-demo-rehearsal.md`
- `docs/client-feedback-form.md`
- `README.md`
- `PROJECT_CONTEXT.md`
- `CHANGELOG.md`
- `SPRINT_LOG.md`
- `.env`
- `.env.example`

### Hasil Implementasi

1. **Akun Demo Siap & Aman**: Akun `demo@onespirit.asia` otomatis di-seed dengan role Management. Hak akses Management ditambah `"documents:write"` untuk upload dokumen. Password aman dari hardcoding dan divalidasi saat startup di environment produksi.
2. **Bahasa Antarmuka Konsisten**: Metrik penjualan, filter pencarian, loading states, dan tombol keluar (Sign Out -> Keluar) diterjemahkan ke dalam bahasa Indonesia profesional.
3. **Dokumen Demo Lengkap**: Panduan rehearsal skrip (15-25 menit), formulir feedback klien, dan panduan keamanan port-forwarding telah diarsipkan dalam folder `docs/`.
4. **Verifikasi Green**: Seluruh unit test backend (17 passed) dan frontend build selesai dengan sukses tanpa regresi.

### Test Yang Dilakukan (Sprint 12.1 Final Validation)

Backend:
Command:
pytest app/tests -q
Result:
17 passed

Frontend:
Command:
npm run build
Result:
build success

Docker:
Command:
docker compose up -d
Result:
Sistem container berjalan sehat dan sinkron.
