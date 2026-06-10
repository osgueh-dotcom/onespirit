# DOKUMEN DEMO READINESS - OneSpirit Workflow System

Dokumen ini disusun untuk membantu Program Owner, Developer, dan Evaluator Klien dalam menjalankan demo aplikasi MVP OneSpirit Workflow System secara terstruktur dalam waktu 15–30 menit.

---

## 1. Tujuan Demo MVP

- Mendemonstrasikan kelayakan sistem untuk mengelola koordinasi operasional dan komersial event/proyek secara end-to-end.
- Memvalidasi istilah bisnis (CL, ROS, CK, PNL) dan alur kerja (PO & PM) di PT One Spirit Asia.
- Menunjukkan otomatisasi kesiapan proyek (*readiness score*) dan pendeteksian resiko komersial.
- Memperoleh masukan taktis dari tim internal PT One Spirit Asia sebelum rilis produksi.

---

## 2. Pengguna & Kredensial untuk Demo

Untuk keperluan demo lokal/evaluasi, gunakan akun Super Admin yang mencakup semua kemampuan lintas-peran:

- **E-mail**: `admin@onespirit.asia`
- **Password**: `OneSpirit2026!`
- **Akses**: Super Admin (dapat mengakses PM Control Center, PO Control Center, CRM, Projects, Finance, dan Imports).

*Catatan Keamanan: Kredensial ini hanya untuk lingkungan demo/development lokal.*

---

## 3. Alur Demo Terstruktur (15–30 Menit)

Berikut adalah langkah-langkah berurutan saat melakukan presentasi/demo sistem kepada manajemen atau klien evaluator:

### Langkah 1: Autentikasi (2 Menit)
- Buka portal web di [http://localhost:5173](http://localhost:5173).
- Input kredensial admin dan tunjukkan validasi error (jika password salah).
- Login dan masuk ke halaman Dashboard Utama.

### Langkah 2: Executive Dashboard (3 Menit)
- Tunjukkan KPI Card global (Total ongoing projects, pipeline status, monthly trends, dan activity logs).
- Jelaskan bahwa dashboard ini memberi gambaran cepat kesehatan operasional dan komersial perusahaan kepada direksi/management.

### Langkah 3: Modul CRM & Customer (3 Menit)
- Navigasi ke menu **CRM**.
- Tunjukkan daftar klien komersial PT One Spirit.
- Buat satu Customer Baru (misal: "PT Sukses Bersama", Kategori: "Corporate"). Tunjukkan bahwa data tersimpan dengan rapi.

### Langkah 4: Project Lifecycle & Detail Proyek (5 Menit)
- Navigasi ke menu **Projects**. Tunjukkan daftar proyek yang terbagi berdasarkan siklus hidup event.
- Buat Proyek Baru dari Customer yang baru dibuat tadi (misal: "One Spirit Annual Gathering 2026").
- Atur status awal sebagai `inquiry` dengan nilai budget tertentu.
- Buka detail proyek baru tersebut. Jelaskan bagian instrumen operasional:
  - **CL (Contract Letter)**
  - **ROS (Rundown Of Show)**
  - **CK (Checklist)**
  - **PNL (Profit & Loss)**
- Tunjukkan cara unggah file CL dan perubahan status instrumen (misal: ROS disetujui, CK terisi).
- Lakukan simulasi transisi status proyek dari `inquiry` ke `confirmed`. Tunjukkan warning jika ada instrumen wajib yang belum terpenuhi (readiness safeguards).

### Langkah 5: PM Control Center - Operasional (5 Menit)
- Navigasi ke **PM Control Center** (Dashboard Program Manager).
- Tunjukkan **Readiness Score** proyek-proyek operasional. Jelaskan bahwa score ini otomatis dihitung dari persentase kesiapan CL, ROS, CK, dan PNL.
- Tunjukkan daftar **Upcoming Events** (jadwal acara terdekat).
- Tunjukkan tabel **Overdue Instruments** (daftar dokumen yang terlambat diselesaikan oleh PM).
- Tunjukkan analitik **Workload PM** (distribusi proyek per staff operasional).

### Langkah 6: PO Control Center - Komersial (5 Menit)
- Navigasi ke **PO Control Center** (Dashboard Program Owner).
- Tunjukkan KPI komersial (Total deal rate, potential revenue, confirmed revenue, outstanding payments).
- Pindah ke **Tab Prioritas Follow-up**: Tunjukkan daftar proyek komersial kritis yang mendekati tanggal event namun penawaran (quotation) atau kontraknya belum ditandatangani. Tunjukkan rekomendasi aksi otomatis dari sistem.
- Pindah ke **Tab Risiko Komersial**: Tunjukkan proyek yang batal tanpa alasan, proyek deal dengan budget Rp 0, atau proyek overdue payment.

### Langkah 7: Simulasi Import Proyek dari Excel (3 Menit)
- Navigasi ke menu **Imports**.
- Unduh template Excel proyek One Spirit (jika tersedia), atau upload file spreadsheet historis.
- Tunjukkan bagaimana modul import memvalidasi baris data (data quality check) dan menampilkan peringatan jika format inisial PM/PO tidak cocok dengan data user terdaftar di sistem.
- Tunjukkan commit data ke database.

### Langkah 8: Tanya Jawab & Pertanyaan Validasi (4 Menit)
- Akhiri demo dengan mengajukan pertanyaan umpan balik kepada PT One Spirit Asia.

---

## 4. Prasyarat Data Dummy untuk Demo

Sistem sudah memiliki data dummy bawaan saat database diinisialisasi (seeded data):
- Akun Super Admin: `admin@onespirit.asia`
- Akun staff operasional dengan inisial: `JIP`, `AR`, `BR`, `SBK`, `SR`, `TF`, `JC`, `SYS`, `MWB`, `RA`, `OME`, `SB`, `UT`, `MDL` (untuk pencocokan kolom PM/PO di Excel Import).
- Data dummy CRM (beberapa nama klien hotel & corporate).
- Beberapa proyek sampel di status `inquiry`, `preparation`, `running`, dan `closed` untuk memunculkan visualisasi chart dan grafik di dashboard secara langsung.

---

## 5. Yang Siap Didemokan (MVP Scope)

1. Dashboard Eksekutif interaktif (Chart menggunakan SVG/CSS modern).
2. Sistem Autentikasi JWT yang aman.
3. CRM CRUD lengkap.
4. Manajemen Proyek & Status Transition Log.
5. PM Control Center (Readiness, Upcoming, Overdue, Workload).
6. PO Control Center (Follow-up Priorities, Commercial Performance, Lead Source Contribution, Risks Panel).
7. Validasi dan Commit Import Excel Proyek.
8. Modul Keuangan (Invoices & Payments tracking).

---

## 6. Pertanyaan Umpan Balik untuk PT One Spirit Asia

Saat menunjukkan demo kepada perwakilan PT One Spirit Asia, tanyakan poin-poin berikut untuk keselarasan bisnis:

1. **Terminologi**: Apakah penggunaan singkatan **CL**, **ROS**, **CK**, dan **PNL** sudah sesuai dengan cara kerja harian tim operasional PT One Spirit Asia?
2. **Readiness Score**: Apakah formula skor kesiapan operasional (berdasarkan persentase CL, ROS, CK, PNL) sudah tepat untuk menggambarkan kesiapan event sebelum hari H?
3. **PM & PO Flow**: Apakah pemisahan dashboard PM (fokus operasional/readiness) dan PO (fokus komersial/prioritas follow-up/keuangan) mempermudah koordinasi staff?
4. **Excel Import**: Apakah kolom-kolom proyek dalam spreadsheet historis mereka sudah terakomodasi di dalam skema penyesuaian import sistem?
5. **Outstanding Payment**: Apakah pembagian status keuangan (Invoice Sent, Paid, Outstanding, Overdue) sudah mencerminkan termin komersial mereka?
