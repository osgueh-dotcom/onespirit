# Dokumentasi Proyek One Spirit (Project Documentation Index)

Selamat datang di repositori dokumentasi **One Spirit Workflow & Business Analytics System** yang dikembangkan oleh **GVSys (Gueh Visual Systems)** untuk **PT. One Spirit Asia**.

Folder ini mengonsolidasikan seluruh catatan teknis pengerjaan sistem dari tahap awal modernisasi hingga persiapan demo evaluasi manajemen.

---

## 1. Catatan Riwayat Sprint (Sprint Logs)
Catatan lengkap mengenai arsitektur, modifikasi kode, hasil pengujian, dan walkthrough setiap sprint:
- **[Sprint 0 — Modernisasi Teknis](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-0-technical-modernization.md)**: Transisi awal teknologi database, setup Alembic migrations, Docker compose, dan penanganan autentikasi token.
- **[Sprint 1 — Refaktor Domain](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-1-domain-refactor.md)**: Desain ulang skema database relational (Project, Customer, EventSource, Document, User) dan normalisasi database.
- **[Sprint 2 — Workflow UI & Kualitas Data](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-2-workflow-ui-data-quality.md)**: Pembangunan Kanban Board, form edit status proyek, penautan tautan Drive, dan validasi data Excel import.
- **[Sprint 2.5 — Stabilisasi & QA](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-2-5-stabilization-qa.md)**: Perbaikan fungsionalitas pengujian otomatis, perbaikan login admin, dan stabilisasi endpoint workflow patch.
- **[Sprint 2.6 — Patch Stabilisasi Lokal](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-2-6-local-stabilization-patch.md)**: Konfigurasi proxy server Vite, inisialisasi kode inisial staf di database, dan environment docker-compose.
- **[Sprint 3 — Pondasi Dashboard Analytics](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-3-dashboard-analytics-foundation.md)**: Pembuatan API endpoint agregasi performa, radar pencapaian omset, workload PO/PM, dan audit ketidaklengkapan data.
- **[Sprint 4 — Laporan Eksekutif & Layout Presentasi](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-4-dashboard-presentation-executive-reporting.md)**: Penyusunan paragraf narasi otomatis, pembuatan print CSS layout putih bersih untuk browser print PDF, dan penentuan catatan rekomendasi bisnis cerdas.
- **[Sprint 4.1 — Polish Demo Dashboard](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-4-1-dashboard-demo-polish.md)**: Pemisahan kartu ringkasan billing keuangan, standardisasi format mata uang/persentase Indonesia, penambahan error banner, dan tombol refresh data.
- **[Sprint 5 — Persiapan Demo Klien](file:///E:/GVsys%20Project/One%20Spirit/docs/sprint-5-client-demo-preparation.md)**: Rangkuman kesiapan sistem, validasi proposal, dan penyelarasan ekspektasi MVP.

---

## 2. Aset Pendukung Demonstrasi Klien (Client Demo Assets)
Gunakan dokumen-dokumen berikut saat mempersiapkan dan melakukan demonstrasi sistem di depan direksi PT. One Spirit Asia:
- **[Alur Demo Langkah Demi Langkah](file:///E:/GVsys%20Project/One%20Spirit/docs/client-demo-flow.md)**: Panduan alur navigasi menu aplikasi selama demo berlangsung.
- **[Naskah Demonstrasi (Indonesian Script)](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-script.md)**: Naskah bicara bahasa Indonesia terstruktur untuk presenter GVSys.
- **[Daftar Periksa Demo (Checklist)](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-checklist.md)**: Checklist wajib sebelum, selama, dan setelah demo untuk meminimalkan gangguan teknis.
- **[Rekomendasi Pilihan Data Demo](file:///E:/GVsys%20Project/One%20Spirit/docs/demo-data-recommendation.md)**: Panduan memilih record database (Good Data vs Data Issues) untuk disajikan kepada klien.
- **[Penyelarasan Proposal Fitur](file:///E:/GVsys%20Project/One%20Spirit/docs/proposal-alignment.md)**: Tabel pemetaan 24 fitur proposal teknis terhadap status implementasi sistem.
- **[Cakupan Sistem MVP](file:///E:/GVsys%20Project/One%20Spirit/docs/mvp-scope.md)**: Penjelasan batasan fitur yang masuk MVP awal dan fitur yang didelegasikan ke Fase Lanjutan (Fase 2).
- **[Daftar Kuesioner Validasi Bisnis](file:///E:/GVsys%20Project/One%20Spirit/docs/client-validation-questions.md)**: Lembar pertanyaan interaktif untuk menyelaraskan alur status dan penagihan dengan klien.
- **[Daftar Batasan Teknis MVP](file:///E:/GVsys%20Project/One%20Spirit/docs/known-limitations-before-client-demo.md)**: Ringkasan batasan sistem yang dikemas dalam bahasa bisnis yang aman dan aman untuk klien.
