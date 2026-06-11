# Panduan Rehearsal Demo Klien

Dokumen ini memandu presenter/demo lead dalam melakukan gladi bersih dan menyajikan demo sistem **OneSpirit Workflow System** kepada manajemen dan perwakilan PT One Spirit Asia dalam waktu **15-25 menit**.

---

## Rangkuman Alur Waktu Demo

| Langkah | Halaman/Modul | Durasi | Fokus Narasi |
| :--- | :--- | :--- | :--- |
| **1** | Halaman Login | 2 Menit | Autentikasi aman dan pengantar modernisasi |
| **2** | Executive Dashboard | 3 Menit | Gambaran besar operasional dan keuangan manajemen |
| **3** | Projects & Kanban | 3 Menit | Siklus hidup proyek dan filter analitik |
| **4** | Project Detail & Readiness | 4 Menit | Safeguards CL, ROS, CK, PNL dan activity logs |
| **5** | PM Control Center | 3 Menit | Kesiapan operasional dan beban kerja PM |
| **6** | PO Control Center | 3 Menit | Sales follow-up, quotation, dan risiko komersial |
| **7** | Pusat Source & Vendor | 2 Menit | Evaluasi source dan vendor partner |
| **8** | Keuangan (Finance) | 2 Menit | Invoice dan pembayaran |
| **9** | Pusat Import Data | 2 Menit | Migrasi data historis dan validasi format |
| **10** | Q&A dan Validasi | 5 Menit | Feedback klien dan prioritas sprint berikutnya |

---

## Skrip Langkah-demi-Langkah

### Langkah 1: Halaman Login dan Autentikasi

- **Tujuan Halaman**: Membuka portal web dan menjelaskan role PO, PM, Finance, Staff, dan Management.
- **Tindakan**: Buka `/login`, masukkan email `demo@onespirit.asia` dan password demo yang disiapkan di environment `DEMO_PASSWORD`.
- **Narasi**: OneSpirit Workflow System dirancang untuk mendigitalkan koordinasi proyek dari inquiry awal sampai final report dan PNL. Login menggunakan JWT token, dan akses fitur dikendalikan oleh role.
- **Pertanyaan Validasi**: Apakah model login berbasis e-mail dan role ini sesuai dengan standar internal One Spirit Asia?

### Langkah 2: Executive Dashboard

- **Tujuan Halaman**: Memperlihatkan performa operasional, target revenue, deal rate, dan data quality.
- **Tindakan**: Masuk ke `/`, tunjukkan KPI, funnel, revenue tracker, source contribution, dan catatan evaluasi manajemen.
- **Narasi**: Dashboard memberi management gambaran cepat tentang total inquiry, deal rate, outstanding payment, dan progress target revenue.
- **Pertanyaan Validasi**: Apakah metrik Deal Rate, Outstanding Payment, dan Revenue Target mencerminkan angka yang biasa direview management?

### Langkah 3: Projects dan Kanban

- **Tujuan Halaman**: Menjelaskan pusat kendali project/event.
- **Tindakan**: Masuk ke `/projects`, ubah mode Board/List, lalu coba filter berdasarkan PO, PM, source, atau status payment.
- **Narasi**: Projects adalah katalog operasional untuk memantau status Inquiry, Confirmed, Preparation, Ready, Running, Completed, Reporting, dan Closed.
- **Pertanyaan Validasi**: Apakah status proyek ini sudah sesuai dengan alur kerja harian event operations?

### Langkah 4: Project Detail dan Readiness

- **Tujuan Halaman**: Memperlihatkan detail event, dokumen, activity log, dan readiness guard.
- **Tindakan**: Buka salah satu project, cek tab Overview dan Instruments, lalu tunjukkan CL, ROS, CK, PNL.
- **Narasi**: Sistem membantu mencegah project maju ke tahap berikutnya jika dokumen penting seperti CL, ROS, CK, atau PNL belum lengkap.
- **Pertanyaan Validasi**: Dokumen mana yang paling wajib menjadi blocker sebelum event dieksekusi?

### Langkah 5: PM Control Center

- **Tujuan Halaman**: Memantau kesiapan lapangan dari sisi Program Manager.
- **Tindakan**: Masuk ke `/pm-control-center`, tunjukkan readiness score, overdue instruments, dan workload PM.
- **Narasi**: PM Control Center membantu management melihat event mana yang butuh perhatian sebelum hari-H.
- **Pertanyaan Validasi**: Apakah workload PM cukup membantu untuk pembagian staf event?

### Langkah 6: PO Control Center

- **Tujuan Halaman**: Memantau sales follow-up, quotation, revenue, dan commercial risk.
- **Tindakan**: Masuk ke `/po-control-center`, tunjukkan summary cards, follow-up priority, dan commercial risks.
- **Narasi**: PO Control Center menyorot quotation yang perlu ditindaklanjuti dan risiko seperti outstanding payment atau proyek deal bernilai Rp 0.
- **Pertanyaan Validasi**: Apakah prioritas follow-up ini sesuai dengan cara PO bekerja?

### Langkah 7: Pusat Source & Vendor

- **Tujuan Halaman**: Menganalisis lead source dan vendor partner.
- **Tindakan**: Masuk ke `/source-vendor-performance`, tunjukkan contribution, conversion, cancellation, dan data quality warning.
- **Narasi**: Modul ini membantu management memahami source mana yang menghasilkan deal dan vendor mana yang paling sering terlibat.
- **Pertanyaan Validasi**: Apakah data source ini berguna untuk komisi, partnership hotel, atau evaluasi vendor?

### Langkah 8: Keuangan

- **Tujuan Halaman**: Memperlihatkan invoice dan pembayaran.
- **Tindakan**: Buka `/finance`, tunjukkan daftar invoice, payment, status outstanding, dan approval.
- **Narasi**: Finance Tracking membantu menjaga cashflow event dan rekonsiliasi pembayaran.
- **Pertanyaan Validasi**: Apakah pencatatan invoice dan payment ini sudah mencukupi kebutuhan penagihan event?

### Langkah 9: Pusat Import Data

- **Tujuan Halaman**: Mendemonstrasikan migrasi data dari Excel lama secara aman.
- **Tindakan**: Buka `/imports`, tunjukkan upload area dan validasi preview.
- **Narasi**: Sistem melakukan validasi sebelum data disimpan agar inisial PO/PM, company, dan program name tidak masuk dalam kondisi rusak.
- **Pertanyaan Validasi**: Apakah format import ini sesuai dengan template Excel yang digunakan saat ini?

### Langkah 10: Q&A dan Validasi

- **Tujuan**: Mengumpulkan feedback klien dan menentukan prioritas sprint berikutnya.
- **Tindakan**: Gunakan [client-feedback-form.md](client-feedback-form.md) untuk mencatat masukan.
- **Narasi**: Setelah demo, diskusikan prioritas produksi: permission UI, PDF export, email automation, backup, vendor normalization, dan deployment cloud.
