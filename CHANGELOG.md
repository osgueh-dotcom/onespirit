# CHANGELOG - OneSpirit Workflow System

Semua perubahan penting pada project ini dicatat di dokumen ini.

---

## [Sprint 23] - 2026-06-24

### Added
- Added quick project customer intake: project creation now accepts either an
  existing `customer_id` or a new `customer_name`.
- Added backend regression coverage for auto-created customers, normalized-name
  customer reuse, and missing customer validation.

### Changed
- Project creation now resolves customer names through CRM normalization before
  creating a minimal `Prospect` customer profile.
- Projects UI now lets users choose an existing Client Account or enter a new
  client name/category directly in the project creation form.
- Updated project status documentation for Sprint 23.

### Validation
- Backend targeted API tests passed with `17 passed`.
- Backend full suite passed with `41 passed`; `pip check` passed.
- Frontend lint, tests, quality scan, audit, and build passed.
- Docker Compose status, frontend HTTP, and backend health checks passed.
- Edge headless Projects modal check passed on desktop and mobile with console
  error count `0`.

---

## [Sprint 22] - 2026-06-24

### Added
- Added a `runtime` scope to the repo context snapshot for toolchain versions,
  local dependency state, Docker Compose service status, and dependency
  verification commands.
- Added the Sprint 22 repository audit with current machine runtime readiness,
  risk register updates, and next-sprint recommendation.

### Changed
- Updated `$onespirit-development` skill guidance, task routing, validation
  matrix, and skill metadata for agent/runtime readiness work.
- Updated README and PROJECT_CONTEXT to reflect Sprint 22 agent runtime
  readiness status.

### Validation
- Context snapshot `summary`, `runtime`, and `full` completed successfully.
- Backend local and container dependency checks passed.
- Frontend dependency tree and `npm audit` completed successfully.
- Backend tests, frontend lint/tests/quality scan/build, Docker Compose status,
  frontend HTTP, and backend health checks passed.

---

## [Sprint 21.1] - 2026-06-21

### Changed
- Verified frontend and backend access through the host LAN address from the
  Windows host, browser, and an isolated container network.
- Restricted the PostgreSQL host port to `127.0.0.1` while keeping application
  ports `5173` and `8000` available on the LAN.
- Added local-network access and troubleshooting guidance.

### Validation
- LAN frontend returned HTTP `200`; browser rendered the login screen and logo
  without console errors.
- LAN backend `/health` returned `ok`; frontend API proxy rejected
  unauthenticated access with `401`.
- Configured demo login, `/auth/me`, projects, and dashboard analytics succeeded
  through the LAN frontend proxy.
- PostgreSQL remained reachable on host loopback and was unreachable through the
  host LAN address.

---

## [Sprint 21] - 2026-06-21

### Added
- Added the repo-scoped `$onespirit-development` skill with progressive
  disclosure, task routing, workflow rules, validation guidance, and a read-only
  context snapshot script.
- Added focused backend and frontend `AGENTS.md` guidance.
- Added a dated repository risk audit and Sprint 22 recommendation.

### Changed
- Reduced the always-loaded root `AGENTS.md` to durable product, security,
  delivery, and review guardrails.
- Updated project status documentation for the Sprint 21 agent workflow.

### Validation
- Skill validator and skill-link checks passed; context snapshot completed.
- Backend: `38 passed`; `pip check` passed.
- Frontend: lint passed; tests `4 passed`; quality scan passed; audit found
  `0 vulnerabilities`; production build passed.
- Docker Compose rebuilt successfully; database and backend were healthy,
  frontend returned HTTP `200`, and backend `/health` returned `ok`.

---

## [Sprint 20] - 2026-06-17

### Changed
- Added formal backend roles for `Admin`, `PO`, and `PM`.
- Updated admin user creation aliases so `admin`, `po`, and `pm` resolve to formal workflow roles.
- Aligned project workflow guards for Admin/PM status transitions and Admin PNL visibility.
- Defaulted Settings user creation toward `Staff` instead of the first returned role.

### Validation
- Backend: `38 passed`; `pip check` passed.
- Frontend: lint `0 errors, 0 warnings`; tests `4 passed`; quality scan, audit, and build passed.
- Docker rebuild, role seed check, HTTP smoke test, and Edge headless login/route smoke test passed.

---

## [Sprint 19] - 2026-06-17

### Changed
- Added `httpx2` to the backend test stack so Starlette TestClient no longer falls back to deprecated `httpx` compatibility.
- Updated readiness and limitation documentation after backend tests reached a clean warning-free baseline.

### Validation
- Backend: `36 passed`; `pip check` passed.
- Frontend: lint `0 errors, 0 warnings`; tests `3 passed`; quality scan, audit, and build passed.
- Docker rebuild, HTTP smoke test, and Edge headless login/route smoke test passed.

---

## [Sprint 18] - 2026-06-17

### Changed
- Cleaned remaining frontend ESLint warnings from unused props, imports, chart variables, and stale style helpers.
- Updated frontend quality documentation after reaching a clean ESLint baseline.

### Validation
- Frontend: lint `0 errors, 0 warnings`; tests `3 passed`; quality scan, audit, build, and Edge headless login/route smoke test passed.
- Backend: `36 passed, 1 warning`.

---

## [Sprint 17] - 2026-06-17

### Changed
- Migrated remaining backend response schemas from Pydantic class-based `Config` to `ConfigDict`.
- Updated readiness documentation after Pydantic deprecation cleanup.

### Validation
- Backend: `36 passed, 1 warning`.
- Docker backend health check passed after rebuild.

---

## [Sprint 16] - 2026-06-17

### Changed
- Upgraded frontend toolchain to Vite 8, Vitest 4, and Node 24 Docker image.
- Updated frontend lockfile to clear Vite/esbuild audit findings.

### Validation
- Full frontend `npm audit`: `0 vulnerabilities`.
- Docker stack, frontend lint/test/build, and Edge smoke test passed.

---

## [Sprint 15] - 2026-06-17

### Changed
- Hardened Docker local demo configuration with `.dockerignore` files and modern Compose syntax.
- Removed Windows source bind mount dependency from Docker Compose demo runtime.
- Updated launcher and setup documentation for Docker Desktop and WSL/virtualization requirements.

### Validation
- Docker Compose stack started successfully after virtualization was enabled.
- Backend, frontend, and HTTP smoke checks passed.

---

## [Sprint 14] - 2026-06-11

### Added
- Production readiness audit and checklist.
- Frontend ESLint, Vitest, and safety scan baseline.
- Role-aware UI helper, audit matrix, and access tests.
- Backup/restore plan and secret rotation plan.
- Deployment runbook.
- Backend deprecation cleanup notes.
- PDF export flow plan for CL, ROS, CK, PNL, final report, and management report.
- Authentication regression tests for dashboard modular endpoints.

### Changed
- Restricted control center/import UI visibility by role.
- Disabled project transition controls for read-only users.
- Restricted dashboard developer tools to admin users.
- Removed the demo password from the frontend bundle.
- Let local/VS Code forwarded UI tests use Vite's relative `/api/v1` proxy instead of browser-side `localhost:8000`.
- Migrated backend startup to FastAPI lifespan.
- Migrated Project schemas/router to Pydantic v2 `ConfigDict` and `model_validate`.
- Added frontend lint/test/safety checks to GitHub Pages deployment.
- Updated README and project context with production readiness status.

### Security
- Added authentication to seven dashboard modular endpoints.
- Kept backend permissions as the primary security authority.

### Validation
- Backend: `36 passed, 37 warnings`.
- Frontend: lint `0 errors, 26 warnings`; tests `3 passed`; safety scan and build passed.
- Production dependency audit: `0 vulnerabilities`.

### Known Limitations
- Production deployment is not declared.
- Role PO/PM/Admin and project ownership authorization are not formalized.
- Backup automation, monitoring, rate limiting, and server-side PDF remain pending.
- Two moderate Vite/esbuild advisories remain in development dependencies.

---

## [Sprint 14.1] - 2026-06-12

### Added
- Brand UI guideline for One Spirit color direction, logo usage, component styling, and chart rules.
- Dashboard visual analytics refinement with cleaner chart cards and clearer hierarchy.

### Changed
- Refined global light mode consistency across core pages.
- Integrated One Spirit logo and brand palette into the login page, app shell, and favicon.
- Polished shared UI components, dashboard header, project detail header, and executive dashboard layout.
- Improved the presentation quality of Projects, PM Control Center, PO Control Center, Source & Vendor Performance, Finance, Imports, CRM, Documents, and Settings.

### Validation
- Frontend build remains successful after visual changes.
- Brand UI changes are scoped to presentation and do not alter backend contracts.

---

## [Sprint 13.1] - 2026-06-11

### Added
- Settings/Pengaturan page with account profile and change own password.
- Admin-only user list, create user, password reset, and activate/deactivate controls.
- Backend password and user-status endpoints with regression tests.
- Zoom demo safety checklist.
- `DEMO_USER_EMAIL` and `DEMO_USER_PASSWORD` environment aliases.
- Automated dev tunnel smoke test for frontend load, API proxy, login, current user, and backend health.

### Changed
- Cleaned sprint log chronology.
- Updated current project status in README.
- Added `BACKEND_CORS_ORIGINS` example.
- Clarified frontend demo environment variables.
- Simplified GitHub Pages deployment workflow.
- Paused automatic GitHub Pages deployment; the workflow is manual-only while Zoom/local demo is the primary mode.
- Set local Zoom screen share as the primary demo mode and VS Code Port Forwarding as fallback.
- Updated client rehearsal and public demo safety guidance.
- Reserved `/auth/users` for admin user management and added `/auth/users/options` for workflow references.

### Fixed
- Minor deployment documentation inconsistencies.
- Potential confusion between backend CORS env and frontend `VITE_API_BASE_URL`.

### Security
- Passwords are hashed with the existing Passlib password context and never returned by user APIs.
- Non-admin users cannot create, reset, activate, or deactivate users.
- Admin cannot deactivate their own account or the last active Super Admin.

### Validation
- Backend: `36 passed, 37 warnings`.
- Frontend: lint `0 errors, 26 warnings`; tests `3 passed`; safety scan and build passed.

### Known Limitations
- Production deployment is not finalized.
- PO/PM/Admin roles still use the existing role mapping.
- Existing JWT access tokens are not revoked automatically after a password reset.
- Vendor analytics still relies on textual fallback data.

---

## [Sprint 13] - 2026-06-11

### Added
- Membuat dokumen evaluasi menyeluruh Sprint 0 sampai Sprint 12.3 di `docs/sprint-13-full-sprint-audit-hardening.md`.

### Changed
- Memperbarui `README.md` agar portable, bebas karakter encoding rusak, bebas link lokal absolut, dan sesuai status Sprint 12.3.
- Membersihkan `docs/client-demo-rehearsal.md` dan `docs/public-demo-safety-checklist.md` agar siap dipakai untuk handover demo klien.
- Memperbaiki panduan GitHub Pages agar memakai env backend yang benar, yaitu `BACKEND_CORS_ORIGINS`.
- Menambahkan origin GitHub Pages ke default backend CORS untuk mendukung demo frontend publik.
- Mengganti hardcoded SQLite test path `/tmp/*.db` menjadi named in-memory database via helper `backend/app/tests/db_utils.py`.

### Security
- Mengganti output seeding admin/demo/staff dari `print()` yang menampilkan password menjadi `logger.info()` tanpa password.

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
- Mengintegrasikan akun demo klien `demo@onespirit.asia` dengan role Management.
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
- Membersihkan dan memperbaiki semua absolute local path link Windows menjadi relative path link di seluruh file dokumentasi markdown.
- Menambahkan stylesheet optimasi cetak `@media print` A4 landscape pada file css utama `frontend/src/assets/index.css` agar cetak cetak halaman/Save-as-PDF (Ctrl+P) otomatis menghasilkan layout laporan yang premium, bersih, dan bebas dari elemen navigasi sidebar/navbar/tombol.

### Security
- Menambahkan filter `*.env` dan direktori `uploads/`, `backend/app/uploads/` pada file `.gitignore` untuk mencegah kebocoran data sensitif operasional dan file rahasia lokal ke repositori git.
- Melakukan review pada file `.env.example` untuk menjamin tidak ada credentials / JWT secrets riil yang tersimpan di repositori, serta menambahkan placeholder konfigurasi `ADMIN_EMAIL` dan `ADMIN_PASSWORD`.
- Menambahkan dokumentasi yang memperingatkan evaluator mengenai kredensial admin default untuk lingkungan demo/development.
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
