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
| Status Project | MVP Demo Readiness (Sprint 10 Finalization) |
| Lokasi Folder | `e:/GVsys Project/One Spirit` |

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
Inquiry (Klien Request) ➔ Client Confirmation (Deal) ➔ CL (Kontrak Terbit) ➔ Project Setup (Operasional Dimulai) ➔ Planning (Rencana Lapangan) ➔ ROS (Rundown Dibuat) ➔ CK (Checklist Disiapkan) ➔ Execution (Event Berjalan) ➔ PNL (Pemberesan Keuangan) ➔ Final Report / Archive (Laporan Akhir)
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
