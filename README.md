# OneSpirit Workflow System

## Ringkasan Project

`OneSpirit Workflow` adalah sistem workflow operasional dan komersial untuk PT One Spirit Asia. Sistem ini membantu mengelola siklus hidup proyek dan event dari inquiry awal sampai final report dan PNL.

Produk ini dikembangkan untuk mendigitalkan koordinasi operasional, melacak readiness proyek, mengurangi kesalahan manual, dan memberi visibilitas finansial kepada manajemen.

---

## Status Project

| Informasi | Keterangan |
|---|---|
| Nama Project | OneSpirit Workflow System |
| Jenis Sistem | Sistem Workflow Komersial & Operasional Event |
| Status | Sprint 14 - Production Readiness Foundation |
| Owner | PT One Spirit Asia |
| Lokasi Folder | `<PROJECT_ROOT>` |
| Tech Stack | FastAPI backend, Vue 3 + Tailwind CSS frontend |
| Database | PostgreSQL untuk Docker/production-like, SQLite untuk test lokal |

Current readiness summary:
- Backend test: `29 passed, 39 warnings`
- Frontend build: success
- Frontend lint: `0 errors`, `26 warnings`
- Frontend test: `3 passed`
- GitHub Pages demo deployment: configured
- Backend tunnel: temporary demo access
- Database: private local Docker
- Production readiness: not yet

---

## Fitur Utama

1. **CRM & Customer Management**: manajemen klien, kategori klien, dan kontak terkait.
2. **Project & Event Management**: pelacakan siklus proyek dari Inquiry sampai Closed.
3. **Readiness Control Center & Instruments**: kontrol CL, ROS, CK, dan PNL.
4. **PM Control Center**: dashboard Program Manager untuk readiness score, overdue instruments, dan workload.
5. **PO Control Center**: dashboard Program Owner untuk quotation, revenue, follow-up, dan risiko komersial.
6. **Source & Vendor Performance Center**: evaluasi lead source, vendor partner, conversion, dan risiko data.
7. **Excel Imports**: import massal data proyek historis dengan validasi kualitas data.
8. **Finance Tracking**: pelacakan invoice, payment, outstanding, dan status pembayaran.

---

## Struktur Folder Utama

```text
One Spirit/
|-- backend/                  # Backend FastAPI
|   |-- alembic/              # Migrasi database Alembic
|   `-- app/                  # Source backend utama
|       |-- core/             # Config, database, security, deps
|       |-- models/           # Model data global
|       |-- modules/          # Modul auth, CRM, projects, dashboard, dll.
|       `-- tests/            # Test backend pytest
|-- frontend/                 # Frontend Vue 3 + Vite + Tailwind
|   `-- src/
|       |-- components/       # Komponen UI modular
|       |-- views/            # Halaman utama dan control centers
|       `-- router/           # Konfigurasi vue-router
|-- docs/                     # Dokumentasi sprint, demo, logic, dan terminologi
|-- docker-compose.yml        # Konfigurasi multi-container Docker
`-- run.cmd                   # Launcher demo Windows
```

---

## Cara Menjalankan Project

### 1. Docker Demo Mode

Pastikan Docker Desktop aktif, lalu jalankan dari root project:

```bash
run.cmd
```

Atau gunakan Docker Compose manual:

```bash
docker-compose up -d --build
```

Alamat lokal:
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs) atau port `8001`, sesuai mapping host.

### 2. Backend Lokal

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Frontend Lokal

```bash
cd frontend
npm.cmd install
npm.cmd run dev
```

Buka [http://localhost:5173](http://localhost:5173).

Untuk test lewat VS Code port forwarding, jalankan backend di workspace pada port `8000`, lalu forward/open frontend port `5173`. Jangan set `VITE_API_BASE_URL` untuk test lokal ini; frontend akan memakai request relatif `/api/v1/...` dan Vite akan memproxy ke backend.

---

## Validasi

Backend:

```bash
cd backend
pytest app/tests -q
```

Frontend:

```bash
cd frontend
npm.cmd run build
```

Script frontend quality yang tersedia:

```bash
cd frontend
npm.cmd run lint
npm.cmd run test
npm.cmd run quality:scan
npm.cmd run build
```

Sprint 14 menambahkan ESLint dan Vitest baseline. Component test, coverage threshold, dan typecheck belum tersedia.

---

## Production Readiness Status

OneSpirit Workflow saat ini **demo-ready**, tetapi **belum production-ready penuh**.

Status saat ini:
- MVP demo ready.
- GitHub Pages frontend demo ready.
- Backend dapat dijalankan lokal/tunnel untuk demo.
- Database masih private/local Docker.
- Production deployment permanen belum dilakukan.

Dokumen Sprint 14 production readiness:
- [Production Readiness Audit](docs/production-readiness-audit.md)
- [Frontend Quality Baseline](docs/frontend-quality-baseline.md)
- [Role-aware UI Audit](docs/role-aware-ui-audit.md)
- [Backend Deprecation Cleanup](docs/backend-deprecation-cleanup.md)
- [Production Readiness Checklist](docs/production-readiness-checklist.md)
- [Backup & Restore Plan](docs/backup-restore-plan.md)
- [Secret Rotation Plan](docs/secret-rotation-plan.md)
- [Deployment Runbook](docs/deployment-runbook.md)
- [PDF Export Flow Plan](docs/pdf-export-flow-plan.md)

---

## Alur Demo Bawaan

Gunakan akun demo klien `demo@onespirit.asia` dengan password development/demo yang diatur lewat environment `DEMO_PASSWORD`.

Alur demo 15 sampai 25 menit:
1. **Login**: masuk sebagai akun demo klien.
2. **Dashboard**: tinjau KPI, pipeline proyek, revenue trend, dan analytics charts.
3. **CRM**: lihat daftar klien dan kontak.
4. **Projects**: buka daftar proyek, mode Kanban/List, dan filter PO/PM/source.
5. **Project Detail**: cek CL, ROS, CK, PNL, activity log, dan status transition guard.
6. **PM Control Center**: pantau readiness score, overdue instruments, dan workload PM.
7. **PO Control Center**: lihat quotation follow-up, commercial risk, dan outstanding payment.
8. **Source & Vendor Performance**: evaluasi lead source dan vendor partner.
9. **Excel Import**: uji import data historis dan data quality validation.

---

## Known Limitations

1. **Security**: JWT secret dan default password demo/admin hanya boleh dipakai untuk development/demo. Environment `production` wajib memakai secret dan password berbeda.
2. **Permission UI**: role-aware visibility baseline sudah ada, tetapi role PO/PM/Admin dan project ownership backend belum formal.
3. **Backup**: belum ada automated cloud backup database.
4. **External Integration**: belum ada e-mail automation dan direct PDF export service.
5. **Vendor Model**: vendor partner masih bergantung pada field tekstual dan belum menjadi entity relasional penuh.
6. **Deployment**: Docker Compose dan Dockerfile saat ini masih development/demo oriented, bukan production runtime.

---

## GitHub Pages Demo Deployment

- Frontend demo: [https://osgueh-dotcom.github.io/onespirit/](https://osgueh-dotcom.github.io/onespirit/)
- Deployment guide: [docs/github-pages-demo-deployment.md](docs/github-pages-demo-deployment.md)
- Demo architecture: [docs/demo-architecture.md](docs/demo-architecture.md)
- Public demo safety checklist: [docs/public-demo-safety-checklist.md](docs/public-demo-safety-checklist.md)
- Client demo rehearsal: [docs/client-demo-rehearsal.md](docs/client-demo-rehearsal.md)
- Client feedback form: [docs/client-feedback-form.md](docs/client-feedback-form.md)
- Dashboard analytics visualization: [docs/dashboard-analytics-visualization.md](docs/dashboard-analytics-visualization.md)

Backend demo tetap berjalan di mesin lokal atau tunnel sementara. Jangan expose database PostgreSQL ke publik.

---

## Dokumentasi Tambahan

- [Dashboard Analytics Visualization](docs/dashboard-analytics-visualization.md)
- [Production Readiness Checklist](docs/production-readiness-checklist.md)
- [Deployment Runbook](docs/deployment-runbook.md)
- [Backup & Restore Plan](docs/backup-restore-plan.md)
- [Secret Rotation Plan](docs/secret-rotation-plan.md)
- [Client Demo Rehearsal](docs/client-demo-rehearsal.md)
- [Client Feedback Form](docs/client-feedback-form.md)
- [Commercial Control Logic](docs/commercial-control-logic.md)
- [Source & Vendor Performance Logic](docs/source-vendor-performance-logic.md)
- [MVP Limitations](docs/mvp-limitations.md)
- [Project Context](PROJECT_CONTEXT.md)
- [Sprint Log](SPRINT_LOG.md)
- [Changelog](CHANGELOG.md)
