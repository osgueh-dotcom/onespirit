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
| **Project Instruments / Operational Checklist** | Partially Implemented | **Ya** | Diidentifikasi sebagai instrumen operasional penting (CL, ROS, CK, PNL), saat ini direpresentasikan melalui tautan dokumen. |
| **CL Tracking** | Planned / Future Phase | **Tidak** | Pelacakan status kontrak kerja sama (Contract Letter / Confirmation Letter) khusus per proyek. |
| **ROS Tracking** | Planned / Future Phase | **Tidak** | Pelacakan status rundown detail acara (Rundown of Show) khusus per proyek. |
| **CK Tracking** | Planned / Future Phase | **Tidak** | Pelacakan checklist persiapan logistik/peralatan (Check List) khusus per proyek. |
| **PNL Tracking** | Planned / Future Phase | **Tidak** | Pelacakan status instrumen keuangan proyek (Profit and Loss) khusus per proyek. |
| **Instrument Status Workflow** | Future Phase | **Tidak** | Alur persetujuan status instrumen proyek (CL, ROS, CK, PNL) oleh admin/manajemen. |
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
Fitur-fitur inti untuk demonstrasi MVP telah tersedia dan siap divalidasi bersama PT. One Spirit Asia. Sistem saat ini berada pada tahap *working local MVP* untuk kebutuhan validasi alur kerja (*workflow*), *dashboard*, dan kebutuhan bisnis operasional. Beberapa fitur lanjutan seperti modul *Project Instruments* khusus (CL, ROS, CK, PNL), penanganan status instrumen terintegrasi, generator *invoice*, dan integrasi otomatis Google Drive direkomendasikan untuk masuk ke tahap rencana pengembangan lanjutan/Fase berikutnya setelah umpan balik dari sesi demo ini dikonsolidasikan.
