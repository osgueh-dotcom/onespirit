# SPRINT LOG - OneSpirit Workflow System

Dokumen ini digunakan untuk mencatat riwayat sprint pengembangan OneSpirit Workflow System, mencakup tujuan, hasil implementasi, dan status verifikasi.

---

## Ringkasan Perjalanan Sprint

| Sprint | Judul / Fokus Utama | Tanggal | Status |
|---|---|---|---|
| **Sprint 0** | Project Documentation Foundation & Tech Archetype | 2026-05-15 | Done |
| **Sprint 1** | Domain Refactoring & DB Schema Alignment | 2026-05-20 | Done |
| **Sprint 2** | Core Workflow & CRM Management | 2026-05-25 | Done |
| **Sprint 3** | Project lifecycle & Status Transitions | 2026-05-30 | Done |
| **Sprint 4** | Readiness gates implementation (CL, ROS, CK, PNL) | 2026-06-01 | Done |
| **Sprint 5** | Finance tracking, invoices & payments integration | 2026-06-03 | Done |
| **Sprint 6** | Excel Import modules for mass data migration | 2026-06-04 | Done |
| **Sprint 7** | PM Control Center & Operational Workload Dashboard | 2026-06-05 | Done |
| **Sprint 8** | PO Control Center & Commercial Dashboard | 2026-06-07 | Done |
| **Sprint 9** | Bug Fixing & UI Polishing | 2026-06-08 | Done |
| **Sprint 10** | PO Control Center Commercial Follow-up & Risks | 2026-06-09 | Done |
| **Sprint 10.1** | Documentation & Commercial Control Cleanup | 2026-06-09 | Done |
| **Sprint 10 Finalization** | Commercial Control Stabilization & MVP Demo Readiness | 2026-06-10 | Done |

---

## Sprint 10 Finalization — Commercial Control Stabilization & MVP Demo Readiness

Tanggal: 2026-06-10  
Status: Done  
AI Agent: Antigravity  
Branch: main  
Commit: Sprint 10: stabilize commercial control and prepare MVP demo

### Tujuan

Menstabilkan fitur komersial, melengkapi metrik PO Control Center, merapikan dokumentasi root dan folder docs, menjaga keamanan configuration, serta memvalidasi kesiapan unit tests dan frontend build agar OneSpirit Workflow siap menjadi MVP demo yang profesional bagi PT One Spirit Asia.

### Scope

- **Commercial Control Stabilization**: Menambahkan 6 metrik baru ke backend PO Control Center (`active_projects`, `pending_quotation_projects`, `follow_up_needed_projects`, `cancelled_projects`, `outstanding_payment`, `commercial_risk_count`) dan memperbarui endpoint dan model Pydantic.
- **Frontend KPI Card Update**: Memodifikasi template `PoControlCenter.vue` pada card Outstanding Pembayaran untuk menampilkan nilai nominal mata uang IDR riil, disertai jumlah klien dalam tanda kurung.
- **New Commercial Control Documentation**: Membuat dokumen baru `docs/commercial-control-logic.md` yang merinci formula bisnis, definisi status, sumber data, dan fallback untuk ketidaklengkapan data.
- **Documentation Cleanup**: Menghapus semua placeholder di `README.md`, `PROJECT_CONTEXT.md`, `SPRINT_LOG.md`, dan `CHANGELOG.md` serta menyinkronkan isinya dengan kondisi terkini.
- **Security & Config Audit**: Memastikan `.gitignore` melindungi file `.env`, file database local SQLite, dan upload media. Memastikan `.env.example` aman tanpa kredensial asli.
- **Test & Build Verification**: Menghindari crash PostgreSQL pada pytest run dengan mendeteksi mode runtime pytest di `main.py`, membuat folder SQLite `E:\tmp` otomatis, dan menjalankan unit test PO Control Center dengan assertions metrik baru. Menjalankan production build Vue 3 via Vite.

### Di Luar Scope

- Tidak menambahkan fitur baru besar di luar stabilisasi commercial control.
- Tidak mendesain ulang arsitektur sistem.

### File/Modul Terkait

- `backend/app/modules/dashboard/schemas.py`
- `backend/app/modules/dashboard/po_control_service.py`
- `backend/app/tests/test_po_control_center.py`
- `frontend/src/views/PoControlCenter.vue`
- `docs/commercial-control-logic.md`
- `docs/demo-readiness.md`
- `docs/mvp-limitations.md`
- `README.md`
- `PROJECT_CONTEXT.md`
- `SPRINT_LOG.md`
- `CHANGELOG.md`
- `.gitignore`
- `.env.example`

### Hasil Implementasi

1. **PO Control Center Stabil**: Endpoint backend dan UI frontend terintegrasi penuh untuk metrik komersial riil tanpa angka palsu/placeholder. Outstanding payment terhitung dari selisih nominal invoice terbit dikurangi payment disetujui (`status = 'approved'`).
2. **Commercial Logic Terarsip**: Panduan formula komersial telah dibuat di [commercial-control-logic.md](file:///e:/GVsys%20Project/One%20Spirit/docs/commercial-control-logic.md).
3. **Test Suite 100% Pass**: Seluruh 16 unit tests backend berhasil dijalankan dengan SQLite secara lokal dan lulus 100%.
4. **Frontend Build Sukses**: Vite production build berhasil mengompilasi aset Vue 3 secara sempurna dengan command `npm.cmd run build`.
5. **Keamanan Konfigurasi Terjaga**: File `.env` terabaikan di git, dan default credentials demo/development terdokumentasi dengan warning yang jelas.

### Test Yang Dilakukan

- Menjalankan `.venv\Scripts\pytest app/tests -q` di terminal backend.
- Menjalankan `npm.cmd run build` di terminal frontend.
- Memverifikasi output visual nominal currency outstanding pembayaran pada card.

### Risiko Tersisa

- Kredensial super admin demo (`admin@onespirit.asia`) bersifat hardcoded pada database seed awal untuk kemudahan demo local/evaluasi. Ini harus dinonaktifkan/diubah ketika sistem dirilis ke production.
- Cetak laporan operasional dan komersial (ROS, PNL) masih mengandalkan fitur bawaan Ctrl+P dari web browser (belum export PDF native).

