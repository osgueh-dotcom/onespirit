# Sprint 5 — Client Demo Preparation & Proposal Alignment

Dokumen ini mencatat pencapaian, output dokumentasi, dan hasil penyelarasan sistem pada **Sprint 5 — Client Demo Preparation & Proposal Alignment**.

---

## 1. Tujuan Sprint 5
Tujuan utama Sprint 5 adalah mempersiapkan sistem **One Spirit Workflow & Business Analytics System** agar siap didemonstrasikan secara lokal kepada perwakilan manajemen **PT. One Spirit Asia**. Kegiatan difokuskan pada pemetaan cakupan MVP, penyusunan skrip bicara presenter, daftar periksa sebelum/selama/setelah rapat, dan formulasi kuesioner validasi bisnis.

---

## 2. Output Dokumentasi yang Dibuat (Deliverables)

Seluruh panduan presentasi dan penyelarasan proposal telah berhasil disusun di folder [docs/](file:///E:/GVsys%20Project/One%20Spirit/docs/):
1. **[Alur Demo Sistem](file:///E:/GVsys%20Project/One%20Spirit/docs/client-demo-flow.md)**: Panduan langkah demi langkah menyajikan modul dashboard, alur kerja, rincian proyek, kualitas data, hingga cetak laporan.
2. **[Skrip Demonstrasi](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-script.md)**: Panduan naskah bicara bahasa Indonesia yang terstruktur untuk presenter GVSys saat memandu jalannya presentasi di depan direksi.
3. **[Checklist Persiapan](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-checklist.md)**: Daftar tugas wajib sebelum demo (verifikasi Docker, health check), selama demo, dan setelah demo berakhir.
4. **[Rekomendasi Data Demo](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-data-recommendation.md)**: Petunjuk pemilihan record data yang ideal untuk demo (Good Data vs Data Quality Issues).
5. **[Penyelarasan Proposal](file:///E:/GVsys%20Project/One%20Spirit/docs/proposal-alignment.md)**: Tabel pencocokan antara 24 fitur proposal GVSys dengan status implementasi nyata (100% Implemented).
6. **[Cakupan MVP & Fase Lanjutan](file:///E:/GVsys%20Project/One%20Spirit/docs/mvp-scope.md)**: Penegasan batasan sistem yang masuk dalam MVP saat ini dan daftar fitur yang direkomendasikan bergeser ke Fase 2.
7. **[Pertanyaan Validasi Bisnis](file:///E:/GVsys%20Project/One%20Spirit/docs/client-validation-questions.md)**: Daftar kuesioner untuk memicu umpan balik klien mengenai transisi status proyek, peran PO/PM, dan detail termin billing.
8. **[Daftar Batasan MVP](file:///E:/GVsys%20Project/One%20Spirit/docs/known-limitations-before-client-demo.md)**: Rangkuman batasan teknis saat ini dalam bahasa yang aman dan profesional bagi klien.
9. **[Daftar Indeks Dokumentasi](file:///E:/GVsys%20Project/One%20Spirit/docs/README.md)**: Peta panduan yang menautkan seluruh berkas dokumentasi sprint.

---

## 3. Hasil Penyelarasan Fungsional
Berdasarkan audit proposal teknis, **seluruh 24 modul operasional inti yang dijanjikan telah selesai diimplementasikan**. Dashboard telah dipoles pada Sprint 4.1 dengan format Rupiah tanpa spasi (`Rp10.573.503.222`), desimal persentase menggunakan koma (`46,21%`), dan panel kualitas data berbahasa Indonesia.

Sistem siap didemonstrasikan tanpa crash karena didukung oleh penanganan error API yang kuat serta tombol muat ulang data.

---

## 4. Rekomendasi Langkah Setelah Rapat Demo (Next Steps)
1. **Pencatatan Masukan Klien**: Dokumentasikan seluruh catatan khusus dari direksi One Spirit terkait alur billing termin dan otorisasi hak akses staf.
2. **Persetujuan MVP**: Mintalah persetujuan formal terhadap lingkup MVP agar tim GVSys dapat melakukan persiapan penyebaran produksi (*deployment preparation*).
3. **Penyusunan Kontrak Fase 2**: Segera susun addendum proposal untuk fitur Fase Lanjutan (Integrasi WhatsApp, Google Drive, termin nominal penagihan otomatis, ekspor file Excel formal).
4. **Pemasangan Cloud Server (Fase Produksi)**: Menjadwalkan pengerjaan deployment cloud dan migrasi data final dari spreadsheet Excel lama milik klien setelah MVP disetujui.
