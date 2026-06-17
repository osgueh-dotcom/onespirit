# PROJECT CONTEXT - OneSpirit Workflow System

Dokumen ini berisi konteks bisnis, peran pengguna, terminologi operasional, workflow utama, modul sistem, dan batasan teknis dari OneSpirit Workflow System.

Dokumen ini wajib dipahami oleh pengembang dan AI agent sebelum memodifikasi kode program.

---

## 1. Identitas Project

| Informasi | Keterangan |
|---|---|
| Nama Project | OneSpirit Workflow System |
| Owner | PT One Spirit Asia |
| Client / Internal | PT One Spirit Asia (Internal Operation & Commercial) |
| Jenis Sistem | Sistem Workflow Komersial & Operasional Event |
| Bidang Bisnis | Event Operations, Project Workflow, Document Tracking, dan Finance |
| Status Project | Sprint 19 - Backend Test Stack Cleanup |
| Lokasi Folder | `<PROJECT_ROOT>` |
| Frontend Deployment Strategy | Local Zoom demo; VS Code Port Forwarding as temporary fallback |
| Backend Deployment Strategy | Local backend; temporary port forwarding only when required |
| Database | Private local Docker |

---

## 1.1 Status Sprint 13.1 & Zoom Demo Access Model

Sprint 13.1 focuses on safe Zoom demo and basic access management. Sprint ini menambahkan Settings, change own password, admin user creation, password reset, activate/deactivate user, dan dokumentasi keamanan demo.

Deployment model saat ini:

- Local PC dan Zoom screen share sebagai mode demo utama.
- VS Code Port Forwarding hanya sebagai fallback jika client perlu mencoba langsung.
- GitHub Pages deployment ditunda untuk alur demo ini.
- GitHub Pages workflow hanya dapat dijalankan manual (`workflow_dispatch`).
- Local/private database.
- Not production deployment.

Project sudah cukup kuat untuk demo client, tetapi belum masuk kategori production-ready cloud deployment.

Role mapping sementara:

- `super_admin` dan `admin` menggunakan role `Super Admin`/permission `admin`.
- `management` menggunakan `Management`.
- `finance` menggunakan `Finance`.
- `po` dan `pm` masih menggunakan `Staff` sampai permission matrix granular disepakati.
- Akun demo menggunakan akses `Management` untuk kebutuhan presentasi workflow.

---

## 1.2 Status Sprint 14 & Production Readiness Direction

Sprint 14 moves the project from demo readiness toward production planning. Sprint ini membangun fondasi production readiness tanpa mendeklarasikan production deployment final.

Sprint 14 mencakup:

- Frontend ESLint, Vitest, dan safety scan baseline.
- Role-aware UI audit.
- Backend deprecation cleanup phase 1.
- Production readiness checklist.
- Backup and restore planning.
- Secret rotation planning.
- Deployment runbook.
- PDF export flow planning untuk CL, ROS, CK, PNL, final report, dan management report.

Production is not yet declared. GitHub Pages dan backend tunnel tetap diposisikan sebagai demo deployment model.

Current validation after Sprint 19:

- Backend: `36 passed`.
- Frontend lint: `0 errors`, `0 warnings`.
- Frontend test: `3 passed`.
- Frontend build: success.

Sprint 19 menambahkan dependency `httpx2` untuk menyelaraskan FastAPI/Starlette TestClient dan menghapus warning test backend terakhir.

Sprint 18 membersihkan sisa warning ESLint legacy di frontend tanpa mengubah workflow bisnis CL, ROS, CK, PNL, atau response contract backend.

Role visibility frontend sudah membatasi control center, imports, project actions, PNL link, dan developer tools. Backend tetap menjadi security authority; role PO/PM/Admin dan ownership per project belum formal.

## 1.3 Status Sprint 14.1 & Brand UI Direction

Sprint 14.1 focuses on improving visual identity, dashboard clarity, and client-facing presentation quality. Sprint ini menambahkan brand polish dan visual analytics enhancement tanpa mengubah arsitektur atau workflow bisnis inti.

Fokus sprint:

- Brand integration One Spirit pada login, app shell, dan favicon.
- Light mode consistency yang lebih clean dan professional.
- Shared UI components yang lebih seragam.
- Dashboard analytics yang lebih mudah dibaca untuk demo dan review operasional.

Sprint 14.1 tidak mendeklarasikan perubahan backend business logic. Perubahan utama berada pada presentasi, token visual, dan hierarchy UI.

---

## 2. Latar Belakang Bisnis

Project ini dikembangkan untuk PT One Spirit Asia guna menyelesaikan masalah berikut:

1. **Koordinasi Manual yang Rumit**: Penyelenggaraan event melibatkan banyak instrumen (CL, ROS, CK, PNL) yang sebelumnya tersebar dalam bentuk spreadsheet atau chat manual.
2. **Keterlambatan Penagihan (Outstanding Payments)**: Kurangnya visibilitas bagi Program Owner (PO) komersial untuk melacak status quotation dan pembayaran klien, yang menyebabkan tagihan sering overdue.
3. **Resiko Kesiapan Event (Readiness Risk)**: Sulitnya mendeteksi ketidaksiapan operasional (readiness gates) sebelum event dimulai, seperti Contract Letter (CL) belum ditandatangani atau Rundown (ROS) belum disepakati.

Sistem ini membantu operasional agar lebih rapi, terdokumentasi secara terpusat, mudah dipantau melalui dashboard kendali, dan meminimalkan resiko operasional.

---

## 3. Peran Pengguna (User Roles)

Sistem membagi akses berdasarkan peran bisnis nyata di PT One Spirit Asia:

| Role | Kebutuhan & Hak Akses |
|---|---|
| **Super Admin** | Hak akses penuh terhadap user management, CRM, setup database, serta bypass otorisasi operasional. |
| **Management / Executive** | Memantau seluruh performa komersial, laporan keuntungan PNL, performa staff, dan analitik bisnis global. |
| **Program Owner (PO)** | Penanggung jawab komersial. Mengelola CRM klien, membuat quotation, melacak deal/cancel proyek, memantau revenue, dan menangani follow-up pembayaran. |
| **Program Manager (PM)** | Penanggung jawab operasional di lapangan. Mengelola event schedule, rundown (ROS), checklist kebutuhan (CK), kesiapan dokumen, dan menugaskan staff. |
| **Finance** | Memantau PNL proyek, menerbitkan invoice, mencatat termin pembayaran, dan menandai tagihan overdue. |

---

## 4. Istilah Penting & Terminologi Bisnis

Untuk memastikan keselarasan istilah, sistem menggunakan terminologi bisnis asli PT One Spirit Asia berikut:

| Istilah | Arti / Keterangan | Catatan dalam Sistem |
|---|---|---|
| **PNL** | *Profit and Loss* | Laporan estimasi dan aktual laba/rugi suatu event/proyek. Menentukan kelayakan finansial sebelum dan sesudah pelaksanaan. |
| **CL** | *Contract Letter / Confirmation Letter* | Dokumen kontrak hukum atau surat konfirmasi kerja sama dengan klien. |
| **ROS** | *Rundown Of Show* | Jadwal detail menit-demi-menit pelaksanaan event di lapangan. |
| **CK** | *Check List* | Daftar checklist kebutuhan logistik, perlengkapan, dan tugas teknis event. |

---

## 5. Alur Kerja Bisnis Utama (Core Event Workflow)

Siklus hidup setiap proyek/event di One Spirit berjalan melalui tahap berikut:

```text
Inquiry (Klien Request) -> Client Confirmation (Deal) -> CL (Kontrak Terbit) -> Project Setup (Operasional Dimulai) -> Planning (Rencana Lapangan) -> ROS (Rundown Dibuat) -> CK (Checklist Disiapkan) -> Execution (Event Berjalan) -> PNL (Pemberesan Keuangan) -> Final Report / Archive (Laporan Akhir)
```

1. **Inquiry**: Program Owner menerima inquiry klien dan menginput data awal proyek ke sistem dengan estimasi nilai budget.
2. **Client Confirmation**: Klien menyetujui quotation (deal) dan proyek ditandai sebagai `confirmed`.
3. **CL (Contract Letter)**: Kontrak disiapkan, dikirim, dan diunggah ke sistem.
4. **Project Setup & Planning**: PM ditugaskan untuk mulai menyusun rencana lapangan, jadwal event, dan tim.
5. **ROS & CK**: Rundown Of Show (ROS) disusun detail dan Checklist (CK) operasional disiapkan untuk mengontrol kesiapan logistik.
6. **Execution**: Event berjalan di lokasi.
7. **PNL**: Finance melakukan rekonsiliasi pengeluaran aktual vs budget untuk menerbitkan laporan laba-rugi akhir.
8. **Final Report / Archive**: Pengarsipan dokumen proyek setelah semua tagihan lunas dibayar.

---

## 6. Modul Utama Sistem

| Modul | Deskripsi | Status |
|---|---|---|
| **CRM** | Kelola data pelanggan, kontak utama, dan kategori klien. | Selesai |
| **Projects** | Siklus hidup proyek, transisi status, detail pendaftaran instrumen (CL/ROS/CK/PNL). | Selesai |
| **PM Control Center** | Visualisasi readiness score, monitoring overdue instrumen, workload tim operasional. | Selesai |
| **PO Control Center** | Analitik performa komersial, potensi revenue, lead source contribution, prioritas follow-up. | Selesai |
| **Source & Vendor Performance** | Dashboard analisis kinerja lead source, kontribusi vendor partner, alokasi PO-source, serta audit kualitas data. | Selesai |
| **Imports** | Import batch proyek dari template Excel dengan data validation checks. | Selesai |
| **Finance** | Pelacakan invoice, rekonsiliasi payment term, monitoring outstanding/overdue. | Selesai |

---

## 7. Tech Stack

- **Frontend**: Vue 3, Vite, Tailwind CSS untuk styling. State management menggunakan Pinia dan komunikasi API dengan Axios.
- **Backend**: FastAPI (Python 3), SQLAlchemy 2.0 (ORM), Pydantic v2 (Validation & Schemas).
- **Migration**: Alembic untuk versioning database.
- **Database**: PostgreSQL (Docker-compose) untuk server data, SQLite untuk unit testing yang cepat.
- **Testing**: Pytest untuk automated backend unit tests.

---

## 8. Batasan Sistem MVP saat Ini

- **Local & Docker-only**: Belum di-deploy di cloud-native server dengan HTTPS.
- **Granular UI Roles**: Hak akses sudah dibatasi di level API Backend, namun UI masih menampilkan beberapa tombol yang dinonaktifkan di backend.
- **No PDF Export**: Cetak PNL, ROS, dan Invoice masih menggunakan print browser bawaan (belum memiliki engine PDF khusus).
- **No Email Automation**: Notifikasi overdue atau penagihan ke klien belum terintegrasi dengan e-mail server otomatis.

---

## 9. Kebijakan Pengembangan (AI & Developer Rules)

1. **Preserve existing conventions**: Modifikasi modul harus mematuhi modular arsitektur FastAPI dan SPA pattern Vue 3.
2. **No destructive database changes**: Schema migration harus menggunakan file Alembic yang teratur.
3. **Maintain business terminology**: Dilarang mengganti istilah PNL, CL, ROS, dan CK dengan istilah umum di database atau antarmuka sistem.
