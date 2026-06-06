# Dokumentasi Proyek One Spirit (Project Documentation Index)

Selamat datang di repositori dokumentasi **One Spirit Workflow & Business Analytics System** yang dikembangkan oleh **GVSys (Gueh Visual Systems)** untuk **PT. One Spirit Asia**.

Folder ini mengonsolidasikan seluruh catatan teknis pengerjaan sistem dan panduan demonstrasi evaluasi manajemen.

---

## 1. Catatan Riwayat Sprint (Sprint Logs)
Catatan lengkap mengenai arsitektur, modifikasi kode, hasil pengujian, dan walkthrough setiap sprint:
- **[Sprint 0 — Modernisasi Teknis](sprint-0-technical-modernization.md)**: Transisi awal teknologi database, setup Alembic migrations, Docker compose, dan penanganan autentikasi token.
- **[Sprint 1 — Refaktor Domain](sprint-1-domain-refactor.md)**: Desain ulang skema database relational (Project, Customer, EventSource, Document, User) dan normalisasi database.
- **[Sprint 2 — Workflow UI & Kualitas Data](sprint-2-workflow-ui-data-quality.md)**: Pembangunan Kanban Board, form edit status proyek, penautan tautan Drive, dan validasi data Excel import.
- **[Sprint 2.5 — Stabilisasi & QA](sprint-2-5-stabilization-qa.md)**: Perbaikan fungsionalitas pengujian otomatis, perbaikan login admin, dan stabilisasi endpoint workflow patch.
- **[Sprint 2.6 — Patch Stabilisasi Lokal](sprint-2-6-local-stabilization-patch.md)**: Konfigurasi proxy server Vite, inisialisasi kode inisial staf di database, dan environment docker-compose.
- **[Sprint 3 — Pondasi Dashboard Analytics](sprint-3-dashboard-analytics-foundation.md)**: Pembuatan API endpoint agregasi performa, radar pencapaian omset, workload PO/PM, dan audit ketidaklengkapan data.
- **[Sprint 4 — Laporan Eksekutif & Layout Presentasi](sprint-4-dashboard-presentation-executive-reporting.md)**: Penyusunan paragraf narasi otomatis, pembuatan print CSS layout putih bersih untuk browser print PDF, dan penentuan catatan rekomendasi bisnis cerdas.
- **[Sprint 4.1 — Polish Demo Dashboard](sprint-4-1-dashboard-demo-polish.md)**: Pemisahan kartu ringkasan billing keuangan, standardisasi format mata uang/persentase Indonesia, penambahan error banner, dan tombol refresh data.
- **[Sprint 5 — Persiapan Demo Klien](sprint-5-client-demo-preparation.md)**: Ringkasan kesiapan sistem, pemetaan cakupan MVP, dan panduan data demo.
- **[Sprint 5.1 — Polish Redaksi & Keamanan Dokumentasi](sprint-5-1-client-demo-copy-safety.md)**: Penyempurnaan redaksi bahasa, pembersihan klaim overclaims, glosarium istilah operasional (CL, ROS, CK, PNL), dan relativitas link.
- **[Sprint 7 — Refinement Workflow & Instrumen Proyek](sprint-7-project-instruments-workflow-refinement.md)**: Implementasi tab instrumen operasional proyek (CL, ROS, CK, PNL) dan checklist item.
- **[Sprint 7.1 — Stabilisasi Kesiapan Instrumen](sprint-7-1-instruments-readiness-stabilization.md)**: Sinkronisasi status instrumen dengan readiness gates dan validasi.
- **[Sprint 8 — Kesiapan Proyek & Kontrol Eksekusi Event](sprint-8-project-readiness-event-execution-control.md)**: Pembangunan Event Execution Control, logic transisi status, dan integrasi force-update override.
- **[Sprint 9 — Dashboard Operasional & PM Control Center](sprint-9-operational-dashboard-pm-control-center.md)**: Dashboard operasional PM untuk tracking event mendatang dan instrument overdue.
- **[Sprint 9.1 — Stabilisasi PM Control Center](sprint-9-1-pm-control-center-stabilization.md)**: Patch stabilisasi untuk computed import, skala readiness score, dan PM initial code fallback.
- **[Sprint 10 — PO Control Center & Commercial Follow-up](sprint-10-po-control-center-commercial-follow-up.md)**: Pusat kontrol komersial PO untuk tracking quotation, revenue conversion, dan outstanding payments.
- **[Sprint 10.1 — Penyelarasan Dokumentasi & Kontrol Komersial](sprint-10-1-documentation-commercial-control-cleanup.md)**: Pembersihan tautan absolute, standardisasi formula finansial PO, dan disclaimer prioritas follow-up.

---

## 2. Aset Pendukung Demonstrasi Klien (Client Demo Assets)
Gunakan dokumen-dokumen berikut saat mempersiapkan dan melakukan demonstrasi sistem di depan direksi PT. One Spirit Asia:
- **[Panduan Posisi Demonstrasi (Demo Positioning)](demo-positioning.md)**: Panduan menyajikan sistem sebagai working local MVP untuk validasi kebutuhan bisnis.
- **[Glosarium Istilah Operasional (One Spirit Glossary)](onespirit-terminology.md)**: Daftar istilah operasional khusus (PO, PM, Sales, CL, ROS, CK, PNL) dan penugasannya di sistem.
- **[Alur Demo Langkah Demi Langkah](client-demo-flow.md)**: Panduan alur navigasi menu aplikasi selama demo berlangsung.
- **[Naskah Demonstrasi (Indonesian Script)](demo-script.md)**: Naskah bicara bahasa Indonesia terstruktur untuk presenter GVSys.
- **[Daftar Periksa Demo (Checklist)](demo-checklist.md)**: Checklist wajib sebelum, selama, dan setelah demo untuk meminimalkan gangguan teknis.
- **[Rekomendasi Pilihan Data Demo](demo-data-recommendation.md)**: Panduan memilih record database (Good Data vs Data Issues) untuk disajikan kepada klien.
- **[Penyelarasan Proposal Fitur](proposal-alignment.md)**: Tabel pemetaan modul proposal teknis terhadap status implementasi sistem (tahap MVP).
- **[Cakupan Sistem MVP](mvp-scope.md)**: Penjelasan batasan fitur yang masuk MVP awal dan fitur yang didelegasikan ke Fase Lanjutan (Fase 2).
- **[Daftar Kuesioner Validasi Bisnis](client-validation-questions.md)**: Lembar pertanyaan interaktif untuk menyelaraskan alur status dan penagihan dengan klien.
- **[Daftar Batasan Teknis MVP](known-limitations-before-client-demo.md)**: Ringkasan batasan sistem yang dikemas dalam bahasa bisnis yang aman untuk klien.
