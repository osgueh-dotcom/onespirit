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
| Status | Sprint 13.1 - Minor Cleanup & Deployment Consistency Patch |
| Owner | PT One Spirit Asia |
| Lokasi Folder | `<PROJECT_ROOT>` |
| Tech Stack | FastAPI backend, Vue 3 + Tailwind CSS frontend |
| Database | PostgreSQL untuk Docker/production-like, SQLite untuk test lokal |

Current readiness summary:
- Backend test: `17 passed`
- Frontend build: success
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

Script frontend yang tersedia saat ini hanya `dev`, `build`, dan `preview`. Belum ada script lint/typecheck frontend terpisah.

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
2. **Permission UI**: API permission gate sudah ada, namun penyempurnaan visibility UI per role masih perlu diperdalam.
3. **Backup**: belum ada automated cloud backup database.
4. **External Integration**: belum ada e-mail automation dan direct PDF export service.
5. **Vendor Model**: vendor partner masih bergantung pada field tekstual dan belum menjadi entity relasional penuh.

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
- [Client Demo Rehearsal](docs/client-demo-rehearsal.md)
- [Client Feedback Form](docs/client-feedback-form.md)
- [Commercial Control Logic](docs/commercial-control-logic.md)
- [Source & Vendor Performance Logic](docs/source-vendor-performance-logic.md)
- [MVP Limitations](docs/mvp-limitations.md)
- [Project Context](PROJECT_CONTEXT.md)
- [Sprint Log](SPRINT_LOG.md)
- [Changelog](CHANGELOG.md)
