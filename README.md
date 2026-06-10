# OneSpirit Workflow System

## Ringkasan Project

`OneSpirit Workflow` adalah sistem workflow operasional dan komersial yang dirancang khusus untuk PT One Spirit Asia. Sistem ini membantu mengelola siklus hidup proyek dan event secara end-to-end, mulai dari inquiry awal pelanggan hingga pelaporan laba/rugi akhir (Profit and Loss / PNL).

Sistem ini dikembangkan secara bertahap untuk mendigitalkan koordinasi operasional, melacak kesiapan proyek (readiness), meminimalkan kesalahan manusia, dan meningkatkan visibilitas finansial proyek bagi manajemen.

---

## Status Project

| Informasi | Keterangan |
|---|---|
| Nama Project | OneSpirit Workflow System |
| Jenis Sistem | Sistem Workflow Komersial & Operasional Event |
| Status | MVP Demo Readiness (Sprint 10.2) |
| Owner | PT One Spirit Asia |
| Lokasi Folder | `e:/GVsys Project/One Spirit` |
| Tech Stack | FastAPI (Backend) & Vue 3 + Tailwind CSS (Frontend) |
| Database | PostgreSQL (Production/Docker) & SQLite (Testing/Lokal) |

---

## Fitur Utama

1. **CRM & Customer Management**: Manajemen klien, kategori klien (Corporate, Agency, dll.), dan kontak terasosiasi.
2. **Project & Event Management**: Pelacakan siklus hidup proyek (Inquiry -> Confirmed -> Prep -> Ready -> Running -> Completed -> Reporting -> Closed).
3. **Readiness Control Center & Instruments**: Manajemen dokumen Contract Letter (CL), Rundown of Show (ROS), Checklist (CK), dan Profit & Loss (PNL).
4. **PM Control Center**: Dashboard Program Manager untuk melihat upcoming events, readiness scores, overdue instruments, dan workload staff.
5. **PO Control Center**: Dashboard Program Owner (Commercial) untuk memantau status quotation, potensi & konversi revenue, kontribusi lead source, dan resiko komersial.
6. **Excel Imports**: Modul untuk melakukan import data proyek dari format Excel standar One Spirit secara massal dengan validasi kualitas data.
7. **Finance Tracking**: Pembuatan dan pelacakan invoice serta status pembayaran (Invoice Sent, Paid, Outstanding, Overdue).

---

## Struktur Folder Utama

```text
One Spirit/
├── backend/                  # Kode Backend (FastAPI)
│   ├── alembic/              # File migrasi database Alembic
│   └── app/                  # Sumber kode utama backend
│       ├── core/             # Konfigurasi, db connection, security, deps
│       ├── models/           # Model data global
│       ├── modules/          # Modul fungsional (auth, crm, projects, dll.)
│       └── tests/            # Suite unit testing backend (pytest)
├── frontend/                 # Kode Frontend (Vue 3, Vite, Tailwind)
│   ├── dist/                 # Hasil build produksi frontend
│   └── src/                  # Sumber kode utama Vue 3
│       ├── components/       # Komponen UI modular
│       ├── views/            # Halaman utama (Dashboard, Control Centers)
│       └── router/           # Konfigurasi vue-router
├── docs/                     # Dokumentasi sprint, terminologi, dan demo
├── docker-compose.yml        # Konfigurasi multi-container Docker
└── run.cmd                   # Script launcher otomatis untuk Windows
```

---

## Cara Menjalankan Project

### 1. Menjalankan dengan Docker (Rekomendasi untuk Demo)

Pastikan Docker Desktop sudah aktif di komputer Anda. Cukup jalankan script launcher di root folder:

```bash
run.cmd
```

Atau jalankan perintah docker compose secara manual:

```bash
docker-compose up -d --build
```

Setelah berhasil, aplikasi akan dapat diakses di:
- **Frontend / Web Portal**: [http://localhost:5173](http://localhost:5173)
- **Backend Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs) (atau port 8001 tergantung pemetaan host)

---

### 2. Menjalankan Secara Lokal (Langkah Developer)

#### A. Backend (FastAPI)

1. Masuk ke folder backend:
   ```bash
   cd backend
   ```
2. Buat python virtual environment dan aktifkan:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Buat file `.env` berdasarkan `.env.example`.
5. Jalankan backend:
   ```bash
   uvicorn app.main:app --reload
   ```

#### B. Frontend (Vue 3 / Vite)

1. Masuk ke folder frontend:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm.cmd install
   ```
3. Jalankan server development:
   ```bash
   npm.cmd run dev
   ```
4. Buka browser pada alamat [http://localhost:5173](http://localhost:5173).

---

## Cara Menjalankan Test Backend

Pastikan Anda berada di virtual environment backend, lalu jalankan:

```bash
pytest app/tests -q
```

*Catatan: Tes menggunakan database SQLite in-memory / lokal di `E:\tmp` sehingga tidak memerlukan database PostgreSQL Docker berjalan.*

---

## Cara Build Frontend

Untuk mengompilasi frontend ke dalam bentuk production bundle (dist folder):

```bash
cd frontend
npm.cmd run build
```

---

## Alur Demo Bawaan (Default Demo Flow)

Untuk melakukan demo sistem dalam waktu 15–30 menit, silakan gunakan alur berikut:
1. **Login**: Gunakan akun super admin `admin@onespirit.asia` / password `OneSpirit2026!`.
2. **Dashboard**: Tinjau statistik keseluruhan, pipeline proyek, tren pendapatan bulanan, dan aktivitas terbaru.
3. **CRM**: Lihat daftar klien dan kontak.
4. **Projects**: Buka daftar proyek komprehensif, buat proyek baru dengan status `inquiry`.
5. **Project Detail**: Buka detail proyek dan periksa status readiness gates (CL, ROS, CK, PNL). Cobalah melakukan transisi status.
6. **PM Control Center**: Masuk ke dashboard PM untuk memantau status operasional dan readiness score.
7. **PO Control Center**: Masuk ke dashboard PO untuk melihat performa komersial, quotation, dan resiko pembayaran.
8. **Excel Import**: Coba upload template Excel proyek One Spirit untuk menguji kecocokan import masal.

---

## Batasan Sistem (Known Limitations)

1. **Keamanan**: Saat ini masih menggunakan JWT rahasia bawaan untuk development. Belum ada HTTPS hardening secara cloud-native.
2. **Permission**: Hak akses role (Admin, PO, PM, Finance, Management) sudah divalidasi pada level API gate, namun penyesuaian UI secara granular berdasarkan role masih dalam tahap MVP awal.
3. **Data Backup**: Belum mendukung backup database otomatis ke penyimpanan cloud.
4. **Integrasi Eksternal**: Belum terhubung dengan sistem e-mail otomatis untuk follow-up klien atau export PDF langsung.

---

## Dokumentasi Tambahan

Semua panduan detail lainnya terletak di folder `docs/`:
- `docs/demo-readiness.md` — Panduan alur demo dan checklist pertanyaan validasi klien.
- `docs/mvp-limitations.md` — Batasan teknis sistem secara mendalam dan backlog Sprint 11.
- `PROJECT_CONTEXT.md` — Detail bisnis dan istilah operasional (CL, ROS, CK, PNL).
- `CHANGELOG.md` — Log perubahan versi aplikasi.
- `SPRINT_LOG.md` — Log riwayat pengerjaan sprint pengembangan.
