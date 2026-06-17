# Production Readiness Audit - Sprint 14

Tanggal: 2026-06-11  
Status: foundation complete, production belum dideklarasikan

## Area yang Sudah Aman

- Backend validation lulus dengan `36 passed`.
- Frontend memiliki ESLint, Vitest baseline, safety scan, dan production build.
- Frontend ESLint baseline sudah bersih dengan `0 errors` dan `0 warnings`.
- GitHub Pages demo memakai hash routing dan configurable `VITE_API_BASE_URL`.
- CORS backend mendukung origin lokal dan origin GitHub Pages yang spesifik.
- Menu, route, dan action utama memakai permission/role visibility helper.
- Link PNL dimasking backend untuk role di luar Super Admin, Management, dan Finance.
- Seluruh endpoint dashboard modular sekarang membutuhkan token.
- Production mode menolak debug, database/JWT/password default, dan demo/placeholder user seeding.
- `.env` di-ignore dan env example hanya berisi placeholder.

## Area yang Belum Aman untuk Production

- `docker-compose.yml` dan Dockerfile masih development/demo-oriented: Vite dev server, Uvicorn `--reload`, dan image rebuild diperlukan setelah perubahan source.
- Port PostgreSQL masih dipublish ke host untuk kebutuhan lokal.
- `/docs` dan OpenAPI sudah nonaktif saat `ENV=production`, tetapi belum ada staging access policy.
- `AUTO_CREATE_TABLES` dan seeding startup belum menjadi migration-first production flow.
- Backup automation, off-site retention, encryption, dan restore drill belum tersedia.
- Monitoring, alerting, rate limiting, dan centralized logging belum tersedia.
- Role PO/PM/Admin belum menjadi role backend formal; `Staff` masih menjadi representasi operasional umum.
- Dashboard utama masih dapat dibaca semua user terautentikasi, belum dibatasi per sensitivitas data.
- PDF resmi CL, ROS, CK, PNL, final report, dan management report belum diimplementasikan.

## Risiko Tinggi

- Menjalankan production dengan credential development/default.
- Mengekspos port PostgreSQL atau memakai tunnel demo sebagai akses permanen.
- Menjalankan migration tanpa backup dan restore drill.
- Mengandalkan frontend visibility sebagai security gate.
- Menganggap Docker Compose lokal atau GitHub Pages demo sebagai production architecture.

## Risiko Sedang

- Permission `projects:write` masih luas, termasuk mutation instrumen PNL.
- Import backend menerima `admin` atau `projects:write`; pembatasan Admin/Management saat ini baru diterapkan di UI.
- Masih ada 1 warning test dari Starlette/httpx compatibility.
- Full frontend `npm audit` bersih setelah upgrade Vite 8/esbuild dan Node 24 image.
- Vendor analytics masih memakai textual fallback.

## Scope Aman Sprint 14

- ESLint, Vitest, dan safety scan frontend.
- Role-aware route/menu/action visibility tanpa rewrite auth.
- Authentication gate untuk endpoint dashboard modular.
- Deprecation cleanup mekanis tahap awal.
- Checklist, backup/restore plan, secret rotation plan, deployment runbook, dan PDF flow plan.
- Documentation alignment dan validation baseline.

## Ditunda ke Sprint 15+

- Production Compose/reverse proxy/cloud deployment final.
- Role dan ownership authorization granular untuk PO/PM/Finance.
- Cleanup Starlette/httpx test stack warning.
- Automated encrypted backup serta restore drill.
- Server-side PDF generation.
- Vendor normalization.
