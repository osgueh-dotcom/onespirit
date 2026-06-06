# Penyelarasan Proposal Sistem (Proposal Alignment)

Dokumen ini memetakan butir-butir penawaran fitur dalam proposal **GVSys (Gueh Visual Systems)** terhadap status implementasi sistem **One Spirit Workflow & Business Analytics System** saat ini.

---

## Tabel Penyelarasan Fitur (Feature Alignment Table)

| Fitur Proposal | Status Implementasi | Siap Demo (Demo Ready) | Catatan Operasional / Bisnis |
| :--- | :--- | :---: | :--- |
| **Web-based Workflow System** | Implemented (MVP) | **Ya** | Sistem berjalan lancar di browser lokal menggunakan arsitektur modern FastAPI & Vue 3. |
| **Internal User Management** | Implemented (MVP) | **Ya** | Manajemen akun staf internal yang dapat mengedit proyek dan dinominasikan sebagai PO/PM. |
| **Customer Management** | Implemented (MVP) | **Ya** | Modul data pelanggan (CRM) terintegrasi dengan kategori Corporate, Government, Agency. |
| **Event Source / Vendor / Sales External** | Implemented (MVP) | **Ya** | Penanganan sales eksternal yang melekat pada sisi vendor/sumber event (Event Source). |
| **Project/Event Workflow** | Implemented (MVP) | **Ya** | Pengelolaan status daur hidup proyek dari tahap masuk penawaran hingga proyek diselesaikan. |
| **PO Assignment** | Implemented (MVP) | **Ya** | Penugasan dinamis Program Owner internal untuk memimpin proyek tertentu. |
| **PM Assignment** | Implemented (MVP) | **Ya** | Penugasan dinamis Program Manager internal untuk mengatur detail operasional proyek. |
| **Quotation Status** | Implemented (MVP) | **Ya** | Siklus penawaran: *Draft*, *Sent*, *Follow Up*, *Revision*, *Signed & Deal*, *Cancel*. |
| **Program Status** | Implemented (MVP) | **Ya** | Progres persiapan event: *Inquiry*, *Confirmed*, *Preparation*, *Ready*, *Running*, *Completed*, *Reporting*, *Closed*, *Cancel*. |
| **Payment Status** | Implemented (MVP) | **Ya** | Siklus billing: *Not Invoiced*, *Invoice Sent*, *Partial Paid*, *Paid*, *Outstanding*, *Overdue*. |
| **Project Status** | Implemented (MVP) | **Ya** | Status proyek utama: *Open*, *Active*, *Reporting*, *Closed*, *Canceled*. |
| **Documentation Links** | Implemented (MVP) | **Ya** | Kolom tautan dokumen eksternal Google Drive resmi untuk mempermudah arsip dokumen legal/kontrak. |
| **Project Documentation Links** | Implemented (MVP) | **Ya** | Penyimpanan tautan/link berkas Google Drive untuk melampirkan instrumen proyek. |
| **Project Instruments / Operational Checklist** | Implemented (Sprint 7) | **Ya** | Pelacakan status operasional instrumen proyek (CL, ROS, CK, PNL, PF, MATRIX) terintegrasi dengan Readiness Score. |
| **CL Tracking** | Implemented (Sprint 7) | **Ya** | Pelacakan status dan tautan Contract Letter / Confirmation Letter per proyek. |
| **ROS Tracking** | Implemented (Sprint 7) | **Ya** | Pelacakan status dan tautan Rundown of Show per proyek. |
| **CK Tracking** | Implemented (Sprint 7) | **Ya** | Pelacakan status dan tautan Check List persiapan operasional per proyek. |
| **PNL Tracking** | Implemented (Sprint 7) | **Ya** | Pelacakan status Profit and Loss per proyek disertai dengan pembatasan hak akses tautan dokumen sensitif. |
| **Instrument Status Workflow** | Implemented (Sprint 7) | **Ya** | Alur perubahan status instrumen (Done, In Progress, Need Revision, Not Required) dengan tanggal penyelesaian otomatis dan activity log. |
| **Readiness Gates & Event Execution Control** | Implemented (Sprint 8) | **Ya** | Gerbang validasi transisi status (Ready, Running, Completed, Closed, Cancel) dengan deteksi warning/blocker, override via pembaruan paksa (force update), serta panel kontrol visual di detail proyek dan dashboard readiness. |
| **PM Control Center / Operational Dashboard** | Implemented (Sprint 9) | **Ya** | Dashboard operasional harian/mingguan bagi PM untuk memantau status kesiapan event terdekat, alarm instrument overdue/revisi, dan prioritas aksi (Priority Actions). |
| **Activity Log** | Implemented (MVP) | **Ya** | Audit trail otomatis mencatat riwayat perubahan status, tanggal, dan inisiator pengguna. |
| **Status Timeline** | Implemented (MVP) | **Ya** | Tampilan visual linimasa tahapan status proyek di halaman detail untuk transparansi progres. |
| **Excel Import** | Implemented (MVP) | **Ya** | Pengunggahan file Excel operasional lama dengan fitur pratinjau validasi baris data sebelum masuk database. |
| **Executive Dashboard** | Implemented (MVP) | **Ya** | Halaman utama evaluasi bisnis dengan KPI utama, rangkuman grafik, dan narasi kinerja bahasa Indonesia. |
| **Revenue Analytics** | Implemented (MVP) | **Ya** | Analisis pendapatan terkonfirmasi (*Confirmed*) dan potensi pendapatan (*Potential Pipeline*) terhadap target direksi. |
| **PO Performance** | Implemented (MVP) | **Ya** | Evaluasi KPI jumlah proyek dipimpin, deal dimenangkan, cancel, dan kontribusi omset per Program Owner. |
| **PM Workload** | Implemented (MVP) | **Ya** | Pemantauan beban kerja aktif, persiapan, running, dan pelaporan per Program Manager. |
| **Finance/Payment Summary** | Implemented (MVP) | **Ya** | Ringkasan billing, dana tunai masuk (*Received Cash*), rasio kolektibilitas (*Collection Rate*), dan piutang. |
| **Source Analytics** | Implemented (MVP) | **Ya** | Grafik pangsa pasar sumber masuk event (Hotel, Instagram, Direct, dsb) terhadap omset penjualan. |
| **Customer Analytics** | Implemented (MVP) | **Ya** | Analisis pangsa pasar segmen kategori pelanggan (Corporate, Agency, Government). |
| **Data Quality Dashboard** | Implemented (MVP) | **Ya** | Audit kebersihan data terpusat mendeteksi kelalaian input PO/PM, budget kosong, dan berkas drive kosong. |
| **Print/Save Report** | Implemented (MVP) | **Ya** | Tombol cetak instan dengan media print CSS teroptimasi untuk menghasilkan laporan PDF bersih. |

---

## Ringkasan Kesiapan
Fitur-fitur inti untuk demonstrasi MVP telah tersedia dan siap divalidasi bersama PT. One Spirit Asia. Sistem saat ini berada pada tahap *working local MVP* untuk kebutuhan validasi alur kerja (*workflow*), *dashboard*, instrumen kesiapan proyek terintegrasi (**CL, ROS, CK, PNL, PF, MATRIX**), dan analisis bisnis operasional. Beberapa fitur lanjutan seperti generator *invoice* formal otomatis dan integrasi langsung Google Drive API direkomendasikan untuk masuk ke tahap rencana pengembangan lanjutan/Fase berikutnya setelah umpan balik dari sesi demo ini dikonsolidasikan.
