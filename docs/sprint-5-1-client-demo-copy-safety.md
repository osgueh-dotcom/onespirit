# Sprint 5.1 — Polish Redaksi & Keamanan Dokumentasi (Client Demo Copy & Safety Patch)

Dokumen ini mencatat detail penyesuaian, perbaikan klaim berlebihan, standardisasi glosarium, dan keamanan dokumentasi pada **Sprint 5.1 — Client Demo Copy & Safety Patch**.

---

## 1. Tujuan Sprint 5.1 (Objective)
Tujuan utama dari patch dokumentasi ini adalah memastikan seluruh dokumen penunjang demonstrasi kepada **PT. One Spirit Asia** memosisikan sistem secara tepat sebagai **working local MVP / prototype** untuk kebutuhan validasi alur kerja, bukan sebagai sistem produksi final yang 100% selesai. 

Langkah ini diambil untuk mengelola ekspektasi klien secara profesional dan transparan serta menghindari risiko kesalahpahaman kontrak sebelum masuk ke fase implementasi produksi nyata.

---

## 2. Perubahan Redaksi & Klaim (Copywriting Changes & Overclaim Fixes)

### A. Penghapusan Klaim "100% Implemented" / "Seluruh Fitur Selesai"
Seluruh kalimat yang mengindikasikan bahwa sistem telah selesai 100% atau tidak memiliki fitur tertunda telah diubah menjadi bahasa yang menekankan kesiapan validasi MVP lokal:
- **Sebelum**: *"selesai diimplementasikan (100% Implemented)"*, *"seluruh fitur selesai"*, *"tidak ada fitur tertunda"*.
- **Sesudah**: *"Fitur inti untuk demonstrasi MVP telah tersedia dan siap divalidasi bersama PT. One Spirit Asia"*, *"Sistem saat ini berada pada tahap working local MVP untuk kebutuhan validasi alur kerja (workflow), dashboard, dan kebutuhan bisnis."*

### B. Penghapusan Klaim "Real-time"
Klaim real-time yang tidak didukung oleh infrastruktur sinkronisasi langsung (seperti WebSocket/SSE) telah dihaluskan untuk mencerminkan mekanisme penyimpanan database terpusat yang aman:
- **Sebelum**: *"real-time"*, *"secara real-time"*, *"diperbarui secara instan"*.
- **Sesudah**: *"terpusat dan terbarui berdasarkan database"*, *"secara otomatis mendeteksi ketidaklengkapan data"*, *"lebih cepat diperbarui dibanding rekap manual Excel"*, *"mendukung evaluasi yang lebih cepat dan terstruktur"*.

---

## 3. Glosarium & Istilah Khusus (One Spirit Terminology)
Dibuat satu glosarium resmi untuk menyelaraskan istilah-istilah di dalam sistem dengan proses bisnis internal PT. One Spirit Asia. Rincian selengkapnya terdapat di **[onespirit-terminology.md](onespirit-terminology.md)**.

### Peran Dinamis PO & PM:
- Menegaskan bahwa **PO (Program Owner)** dan **PM (Program Manager)** adalah alokasi staf dinamis tingkat proyek, bukan jabatan akun pengguna (*user role*) yang permanen.

### Instrumen Operasional Proyek (Project Instruments / Operational Checklist):
Memperkenalkan istilah instrumen proyek spesifik:
- **CL**: Contract Letter / Confirmation Letter (Surat Kontrak/Konfirmasi)
- **ROS**: Rundown of Show (Jadwal Susunan Acara Lapangan)
- **CK**: Check List (Daftar Periksa Kesiapan Logistik/Teknis)
- **PNL**: Profit and Loss (Berkas Analisis Laba Rugi Anggaran Proyek)

Instrumen-instrumen ini diposisikan di dalam MVP sebagai **"Partially represented through documentation links"** (Penautan Link Google Drive).

---

## 4. Perbaikan Tautan Dokumen (Link Fixes)
Seluruh tautan yang menggunakan path absolut Windows (`file:///E:/GVsys%20Project/...`) di dalam seluruh dokumen panduan folder `docs/` dan root `README.md` telah dibersihkan dan diganti menggunakan **tautan relatif markdown** agar dapat dibuka dengan aman di perangkat mana pun tanpa patah tautan.

---

## 5. Daftar Dokumen yang Diperbarui (Documents Updated)

1. **[README.md](../README.md)**: Pembersihan tautan absolut, penghalusan klaim, penambahan referensi posisi demo.
2. **[docs/README.md](README.md)**: Pembersihan tautan absolut, penambahan tautan glosarium baru dan dokumen pemosisian demo.
3. **[docs/demo-positioning.md](demo-positioning.md)**: Panduan resmi cara membuka presentasi dan memosisikan local MVP.
4. **[docs/onespirit-terminology.md](onespirit-terminology.md)**: Glosarium resmi PO, PM, Sales, CL, ROS, CK, PNL.
5. **[docs/client-demo-flow.md](client-demo-flow.md)**: Penyesuaian skenario peninjauan instrumen operasional dan pembersihan klaim real-time.
6. **[docs/demo-script.md](demo-script.md)**: Penambahan naskah bicara terkait instrumen proyek serta penghalusan klaim real-time.
7. **[docs/demo-checklist.md](demo-checklist.md)**: Penambahan poin daftar periksa untuk mencatat feedback instrumen operasional.
8. **[docs/demo-data-recommendation.md](demo-data-recommendation.md)**: Penambahan pedoman data proyek bagus (kelengkapan link CL, ROS, CK, PNL).
9. **[docs/proposal-alignment.md](proposal-alignment.md)**: Pemetaan ulang baris fitur instrumen proyek khusus sebagai *Planned/Future Phase* dan penyesuaian status ringkasan kesiapan.
10. **[docs/mvp-scope.md](mvp-scope.md)**: Penegasan bahwa modul alur status instrumen (CL/ROS/CK/PNL) serta pembatasan akses PNL masuk Fase Lanjutan.
11. **[docs/client-validation-questions.md](client-validation-questions.md)**: Penambahan kuesioner Bagian 8 khusus instrumen proyek dan pembatasan akses PNL.
12. **[docs/known-limitations-before-client-demo.md](known-limitations-before-client-demo.md)**: Penambahan penjelasan batas pelacakan instrumen proyek dan PNL di MVP awal.
13. **[docs/sprint-5-client-demo-preparation.md](sprint-5-client-demo-preparation.md)**: Pembersihan tautan absolut dan penghalusan status implementasi.

---

## 6. Langkah Rekomendasi Berikutnya (Recommended Next Steps)
1. Gunakan naskah pemosisian demo yang tertera di **[demo-positioning.md](demo-positioning.md)** saat memulai rapat bersama jajaran direksi PT. One Spirit Asia.
2. Manfaatkan Bagian 8 pada kuesioner **[client-validation-questions.md](client-validation-questions.md)** untuk memandu diskusi khusus terkait bagaimana mereka ingin mengelola alur dokumen CL, ROS, CK, dan PNL di dalam aplikasi pada fase pengembangan berikutnya.
3. Catat umpan balik dan kelola revisi minor alur kerja pasca-demo sebelum menutup keseluruhan proyek technical modernization ini.
