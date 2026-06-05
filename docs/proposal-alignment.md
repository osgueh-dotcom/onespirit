# Penyelarasan Proposal Sistem (Proposal Alignment)

Dokumen ini memetakan butir-butir penawaran fitur dalam proposal **GVSys (Gueh Visual Systems)** terhadap status implementasi sistem **One Spirit Workflow & Business Analytics System** saat ini.

---

## Tabel Penyelarasan Fitur (Feature Alignment Table)

| Fitur Proposal | Status Implementasi | Siap Demo (Demo Ready) | Catatan Operasional / Bisnis |
| :--- | :--- | :---: | :--- |
| **Web-based Workflow System** | Implemented | **Ya** | Sistem berjalan lancar di browser lokal menggunakan arsitektur modern FastAPI & Vue 3. |
| **Internal User Management** | Implemented | **Ya** | Manajemen akun staf internal yang dapat mengedit proyek dan dinominasikan sebagai PO/PM. |
| **Customer Management** | Implemented | **Ya** | Modul data pelanggan (CRM) terintegrasi dengan kategori Corporate, Government, Agency. |
| **Event Source / Vendor / Sales External** | Implemented | **Ya** | Penanganan sales eksternal yang melekat pada sisi vendor/sumber event (Event Source). |
| **Project/Event Workflow** | Implemented | **Ya** | Pengelolaan status daur hidup proyek dari tahap masuk penawaran hingga proyek diselesaikan. |
| **PO Assignment** | Implemented | **Ya** | Penugasan dinamis Program Owner internal untuk memimpin proyek tertentu. |
| **PM Assignment** | Implemented | **Ya** | Penugasan dinamis Program Manager internal untuk mengatur detail operasional proyek. |
| **Quotation Status** | Implemented | **Ya** | Siklus penawaran: *Draft*, *Sent*, *Follow Up*, *Revision*, *Signed & Deal*, *Cancel*. |
| **Program Status** | Implemented | **Ya** | Progres persiapan event: *Inquiry*, *Confirmed*, *Preparation*, *Ready*, *Running*, *Completed*, *Reporting*, *Closed*, *Cancel*. |
| **Payment Status** | Implemented | **Ya** | Siklus billing: *Not Invoiced*, *Invoice Sent*, *Partial Paid*, *Paid*, *Outstanding*, *Overdue*. |
| **Project Status** | Implemented | **Ya** | Status proyek utama: *Open*, *Active*, *Reporting*, *Closed*, *Canceled*. |
| **Documentation Links** | Implemented | **Ya** | Kolom tautan dokumen eksternal Google Drive resmi untuk mempermudah arsip dokumen legal/kontrak. |
| **Activity Log** | Implemented | **Ya** | Audit trail otomatis mencatat riwayat perubahan status, tanggal, dan inisiator pengguna. |
| **Status Timeline** | Implemented | **Ya** | Tampilan visual linimasa tahapan status proyek di halaman detail untuk transparansi progres. |
| **Excel Import** | Implemented | **Ya** | Pengunggahan file Excel operasional lama dengan fitur pratinjau validasi baris data sebelum masuk database. |
| **Executive Dashboard** | Implemented | **Ya** | Halaman utama evaluasi bisnis dengan KPI utama, rangkuman grafik, dan narasi kinerja bahasa Indonesia. |
| **Revenue Analytics** | Implemented | **Ya** | Analisis pendapatan terkonfirmasi (*Confirmed*) dan potensi pendapatan (*Potential Pipeline*) terhadap target direksi. |
| **PO Performance** | Implemented | **Ya** | Evaluasi KPI jumlah proyek dipimpin, deal dimenangkan, cancel, dan kontribusi omset per Program Owner. |
| **PM Workload** | Implemented | **Ya** | Pemantauan beban kerja aktif, persiapan, running, dan pelaporan per Program Manager. |
| **Finance/Payment Summary** | Implemented | **Ya** | Ringkasan billing, dana tunai masuk (*Received Cash*), rasio kolektibilitas (*Collection Rate*), dan piutang. |
| **Source Analytics** | Implemented | **Ya** | Grafik pangsa pasar sumber masuk event (Hotel, Instagram, Direct, dsb) terhadap omset penjualan. |
| **Customer Analytics** | Implemented | **Ya** | Analisis pangsa pasar segmen kategori pelanggan (Corporate, Agency, Government). |
| **Data Quality Dashboard** | Implemented | **Ya** | Audit kebersihan data real-time mendeteksi kelalaian input PO/PM, budget kosong, dan berkas drive kosong. |
| **Print/Save Report** | Implemented | **Ya** | Tombol cetak instan dengan media print CSS teroptimasi untuk menghasilkan laporan PDF bersih. |

---

## Ringkasan Kesiapan
Seluruh 24 fitur utama yang ditawarkan dalam proposal teknis GVSys telah **selesai diimplementasikan (100% Implemented)** dan **siap untuk didemonstrasikan** secara lokal kepada PT. One Spirit Asia. Tidak ada fitur tertunda atau parsial untuk lingkup inti MVP.
