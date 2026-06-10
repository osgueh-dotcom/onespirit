# Panduan Rehearsal Demo Klien (Client Demo Rehearsal)

Dokumen ini memandu presenter/demo lead dalam melakukan gladi bersih dan menyajikan demo sistem **OneSpirit Workflow System** kepada manajemen dan perwakilan PT One Spirit Asia dalam waktu **15–25 menit**.

---

## ⏱️ Rangkuman Alur Waktu Demo

| Langkah | Halaman/Modul | Durasi | Fokus Narasi |
| :--- | :--- | :--- | :--- |
| **1** | Halaman Login | 2 Menit | Autentikasi aman & Pengantar modernisasi |
| **2** | Executive Dashboard | 3 Menit | Gambaran besar operasional & Keuangan manajemen |
| **3** | Projects & Kanban | 3 Menit | Manajemen siklus hidup proyek & Filter analitik |
| **4** | Project Detail & Readiness | 4 Menit | Safeguards instrumen CL/ROS/CK/PNL & Activity logs |
| **5** | PM Control Center | 3 Menit | Kesiapan operasional lapangan & Beban kerja PM |
| **6** | PO Control Center | 3 Menit | Penjualan, prioritas follow-up quotation, & Risiko |
| **7** | Pusat Source & Vendor | 2 Menit | Evaluasi rujukan hotel & Kinerja vendor partner |
| **8** | Keuangan (Finance) | 2 Menit | Rekonsiliasi invoice penagihan & Pembayaran lunas |
| **9** | Pusat Import Data (Excel) | 2 Menit | Migrasi data historis & Validasi format |
| **10**| Sesi Q&A & Validasi | 5 Menit | Formulir Masukan Klien & Umpan Balik |

---

## 🎤 Skrip Langkah-demi-Langkah

### Langkah 1: Halaman Login & Autentikasi (2 Menit)
- **Tujuan Halaman**: Membuka portal web dan menjelaskan peran dinamis PO & PM.
- **Tindakan**: Buka `/login`, masukkan email `demo@onespirit.asia` dan password `OneSpiritDemo2026!`. Tunjukkan pesan error jika password salah sebagai pembuka validasi login.
- **Narasi**:
  > "Selamat pagi bapak/ibu dari One Spirit Asia. Hari ini saya akan mendemonstrasikan MVP OneSpirit Workflow System yang dirancang untuk mendigitalkan koordinasi proyek dari inquire awal sampai laporan keuangan akhir. Pertama, kita login dengan akun demo klien. Sistem ini menerapkan keamanan JWT Token, di mana staf operasional ditunjuk secara dinamis sebagai Program Owner (PO) atau Program Manager (PM) per proyek."
- **Pertanyaan Validasi**:
  - *"Apakah login dengan format e-mail korporat ini sudah sesuai dengan standar akun internal Anda?"*
- **Backup Plan**: Jika halaman login gagal merespons, periksa apakah docker compose port 8000 dan 5173 sudah aktif di terminal, atau lakukan refresh browser.

### Langkah 2: Executive Dashboard (3 Menit)
- **Tujuan Halaman**: Memperlihatkan performa operasi, target pendapatan tahunan, dan kesehatan keuangan.
- **Tindakan**: Masuk ke `/`, gulir secara perlahan ke bawah untuk menunjukkan KPI summary, Conversion Rates, Revenue Tracker, dan Catatan Evaluasi Cerdas.
- **Narasi**:
  > "Setelah login, manajemen langsung disajikan Executive Dashboard. Di sini kita melihat total inquiry, deal rate, sisa pembayaran outstanding (belum lunas), dan progress target pendapatan tahunan secara real-time. Bagian bawah memiliki Review Kualitas Data otomatis yang langsung mendeteksi proyek bermasalah, seperti proyek batal tanpa alasan atau kontrak CL yang belum diunggah."
- **Pertanyaan Validasi**:
  - *"Apakah metrik di Dashboard ini (seperti Deal Rate dan Outstanding Payment) mencerminkan angka penting yang biasa direview oleh jajaran direksi?"*
- **Backup Plan**: Jika grafik dashboard kosong, pastikan data dummy sudah ter-seed dengan benar.

### Langkah 3: Projects & Kanban (3 Menit)
- **Tujuan Halaman**: Menjelaskan katalog proyek dan penggunaan filter pencarian.
- **Tindakan**: Masuk ke `/projects`, ubah mode tampilan antara "Board" (Kanban) dan "List". Gunakan filter "PM" atau "PO" di bagian atas untuk menyaring data.
- **Narasi**:
  > "Menu Projects adalah pusat pengelolaan seluruh event yang sedang ditangani. Kita bisa melihat project dalam bentuk board Kanban untuk mengetahui status operasional atau dalam bentuk List tabel. Filter di atas memudahkan kita melacak proyek berdasarkan PM, PO, sumber referensi hotel, atau status pembayaran dengan satu ketukan."
- **Pertanyaan Validasi**:
  - *"Apakah status kolom Kanban ini (Inquiry, Confirmed, Preparation, Ready, Running, Completed, Closed) sudah mewakili siklus hidup event harian Anda?"*

### Langkah 4: Project Detail & Readiness (4 Menit)
- **Tujuan Halaman**: Memperlihatkan detail data event dan safeguards instrumen (CL/ROS/CK/PNL).
- **Tindakan**: Klik salah satu proyek (misal: "Gathering corporate"). Klik tab **Overview**, lalu tab **Instruments** (CL, ROS, CK, PNL). Cobalah melakukan transisi status proyek ke 'Confirmed' dan tunjukkan warning blockers jika kelayakan operasional belum lengkap.
- **Narasi**:
  > "Di halaman detail, kita memantau profil lengkap event. Untuk memastikan kualitas acara, sistem dilengkapi instrumen pelaporan: CL (Contract Letter), ROS (Rundown), CK (Checklist), dan PNL (Profit & Loss). Jika PM lapangan belum mengunggah dokumen wajib tersebut, sistem akan mencegah transisi status ke tahap berikutnya untuk menghindari kesalahan operasional di lapangan."
- **Pertanyaan Validasi**:
  - *"Bagaimana tanggapan bapak/ibu mengenai fitur safeguards (pencegahan otomatis) ini saat PM belum mengisi rundown (ROS) atau PNL?"*

### Langkah 5: PM Control Center (3 Menit)
- **Tujuan Halaman**: Memantau kesiapan lapangan dari sisi Program Manager.
- **Tindakan**: Masuk ke `/pm-control-center`, tunjukkan Readiness Score, Overdue Instruments, dan workload PM.
- **Narasi**:
  > "PM Control Center adalah workspace khusus untuk Program Manager. Di sini kita memantau Readiness Score setiap proyek operasional secara otomatis. Kita juga dapat mendeteksi dokumen yang terlambat (overdue) dan melihat beban kerja operasional masing-masing PM."
- **Pertanyaan Validasi**:
  - *"Apakah tampilan workload PM ini membantu manajemen dalam melakukan pembagian staf acara?"*

### Langkah 6: PO Control Center (3 Menit)
- **Tujuan Halaman**: Memantau penjualan, follow-up quotation, dan risiko komersial.
- **Tindakan**: Masuk ke `/po-control-center`, tunjukkan tab Prioritas Follow-up, Kinerja Komersial, dan Risiko Komersial.
- **Narasi**:
  > "Bagi Program Owner yang berfokus pada sisi komersial, PO Control Center menyajikan data penawaran harga (Quotation) yang menunggu tindak lanjut, estimasi revenue, dan risiko transaksi komersial (seperti proyek deal dengan nilai Rp 0)."
- **Pertanyaan Validasi**:
  - *"Apakah kategori prioritas follow-up quotation ini membantu PO agar penawaran tidak tertunda?"*

### Langkah 7: Pusat Source & Vendor (2 Menit)
- **Tujuan Halaman**: Menganalisis sumber rujukan (Lead Source) dan performa vendor.
- **Tindakan**: Masuk ke `/source-vendor-performance`, tunjukkan data kontribusi rujukan hotel dan disclaimer data vendor.
- **Narasi**:
  > "Di Pusat Source & Vendor, tim manajemen bisa menganalisis hotel atau agensi mana yang memberikan kontribusi deal event terbesar, serta melacak total pembayaran yang keluar untuk vendor pendukung acara."
- **Pertanyaan Validasi**:
  - *"Apakah data performa source ini berguna untuk menentukan pembagian komisi atau hubungan dengan partner hotel?"*

### Langkah 8: Keuangan (Finance) (2 Menit)
- **Tujuan Halaman**: Memperlihatkan penagihan tagihan (invoice) dan kwitansi (receipt).
- **Tindakan**: Buka `/finance`, tunjukkan tab Tagihan Invoice dan tab Kuitansi Pembayaran.
- **Narasi**:
  > "Pada halaman Keuangan, bagian finance korporat melacak invoice tagihan yang sudah dikirim ke klien dan mencatat bukti penerimaan pembayaran (receipts) untuk menjaga ketelitian cashflow."
- **Pertanyaan Validasi**:
  - *"Apakah pencatatan penagihan bertahap (termin) ini sudah mencukupi kebutuhan penagihan event Anda?"*

### Langkah 9: Pusat Import Data (2 Menit)
- **Tujuan Halaman**: Mendemonstrasikan migrasi data dari file Excel lama secara aman.
- **Tindakan**: Buka `/imports`, klik tombol drag-drop area, tunjukkan proses validasi kolom inisial PO/PM yang tidak cocok dalam data excel pratinjau.
- **Narasi**:
  > "Terakhir, untuk memindahkan data historis dari Excel lama, kami menyediakan Pusat Import Data. Sistem melakukan pengecekan kualitas data sebelum disimpan ke database, mendeteksi jika inisial PO/PM tidak terdaftar, sehingga integritas data operasional tetap terjaga."
- **Pertanyaan Validasi**:
  - *"Apakah format kolom import ini sesuai dengan template file Excel proyek yang biasa Anda gunakan?"*

### Langkah 10: Sesi Q&A & Validasi (5 Menit)
- **Tujuan**: Mengumpulkan feedback klien dan mencatat masukan.
- **Tindakan**: Bagikan lembar kuesioner dari [client-feedback-form.md](file:///e:/GVsys Project/One Spirit/docs/client-feedback-form.md).
- **Narasi**:
  > "Demikian demo sistem MVP OneSpirit Workflow. Kami ingin mendiskusikan masukan bapak/ibu dari sisi alur kerja, data, tampilan, dan prioritas pengembangan sebelum sistem ini dirilis ke lingkungan produksi."
