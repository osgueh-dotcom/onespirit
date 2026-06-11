# Sprint 13 - Full Sprint Audit & Hardening

Tanggal: 2026-06-11  
Status: Done  
Scope: evaluasi Sprint 0 sampai Sprint 12.3, hardening kecil, dan dokumentasi gap.

---

## Ringkasan Evaluasi Sprint

| Area Sprint | Hasil yang Sudah Kuat | Gap yang Ditemukan | Tindakan Sprint 13 |
|---|---|---|---|
| Sprint 0-2 | Fondasi FastAPI, Vue, domain workflow, CRM, projects, dan data quality sudah terbentuk. | Dokumentasi root masih memiliki artefak encoding dan link lokal absolut. | README diganti dengan versi portable dan status project disesuaikan ke Sprint 12.3. |
| Sprint 3-6 | Analytics foundation, readiness CL/ROS/CK/PNL, finance, dan import Excel sudah terhubung ke workflow utama. | Demo docs masih memuat link lokal absolut dan beberapa teks rusak. | Demo rehearsal dan safety checklist dibuat ulang dengan teks bersih dan link relatif. |
| Sprint 7-10 | PM Control, PO Control, commercial risk, test backend, dan MVP demo readiness sudah matang. | Dokumentasi CORS memakai nama env yang tidak sesuai kode (`CORS_ORIGINS` vs `BACKEND_CORS_ORIGINS`). | Panduan GitHub Pages diperbaiki agar sesuai dengan `Settings.BACKEND_CORS_ORIGINS`. |
| Sprint 11 | Source & Vendor Performance Center menambah analitik source/vendor yang relevan bagi management. | Vendor partner masih fallback field tekstual, belum entity relasional. | Dicatat sebagai limitation produk, belum diubah karena butuh schema migration khusus. |
| Sprint 12-12.3 | UI/UX responsive, light mode, dan charts SVG dashboard sudah meningkatkan kesiapan demo. | Default CORS backend belum menyertakan GitHub Pages walaupun deployment docs mengharuskannya. | Default CORS ditambah `https://osgueh-dotcom.github.io`. |

---

## Perbaikan yang Dikerjakan

1. **Backend CORS hardening**
   - Menambahkan `https://osgueh-dotcom.github.io` ke default `BACKEND_CORS_ORIGINS` agar demo GitHub Pages tidak bergantung penuh pada konfigurasi manual.
   - Mengganti anotasi validator dari built-in `any` ke `typing.Any`.

2. **Credential log safety**
   - Mengganti `print()` saat seed admin/demo/staff menjadi `logger.info()`.
   - Menghapus password dari output seeding runtime.

3. **Documentation portability**
   - Mengganti `README.md` dengan versi ringkas, portable, dan bebas karakter rusak.
   - Membersihkan link lokal absolut di dokumen demo.
   - Menyelaraskan endpoint health check menjadi `/health`.
   - Mengoreksi instruksi env CORS menjadi `BACKEND_CORS_ORIGINS`.

4. **Demo handover clarity**
   - Membuat ulang `docs/client-demo-rehearsal.md` agar alur demo 15-25 menit mudah diikuti.
   - Membuat ulang `docs/public-demo-safety-checklist.md` dengan checklist sebelum/sesudah demo.

5. **Backend test hardening**
   - Menambahkan helper `backend/app/tests/db_utils.py` untuk memakai SQLite named in-memory database per test module.
   - Menghapus ketergantungan test pada path `/tmp/*.db` yang tidak stabil di Windows/sandbox.

---

## Gap yang Masih Perlu Sprint Lanjutan

1. **Frontend quality scripts**
   - `frontend/package.json` belum memiliki script `lint`, `typecheck`, atau test UI. Saat ini validasi frontend bergantung pada `npm run build`.

2. **Role-aware UI visibility**
   - API permission gate sudah ada, tetapi UI masih perlu audit granular untuk memastikan setiap role hanya melihat aksi yang relevan.

3. **Vendor normalization**
   - Source & Vendor Performance masih menggunakan vendor textual fallback. Perlu entity vendor dan relasi project/vendor jika akan dipakai untuk evaluasi vendor produksi.

4. **Production deployment hardening**
   - Perlu deployment backend/database cloud, backup otomatis, HTTPS managed, secret rotation, dan observability.

5. **Report output**
   - Print CSS sudah ada, tetapi export PDF resmi untuk CL/ROS/CK/PNL/final report belum menjadi service backend/frontend yang terstruktur.

---

## Rekomendasi Sprint Berikutnya

Sprint 14 sebaiknya fokus pada **Production Readiness Foundation**:

1. Tambahkan frontend lint/test baseline.
2. Audit role-based UI actions.
3. Rancang schema vendor partner relasional.
4. Siapkan deployment backend cloud dan backup policy.
5. Definisikan format PDF resmi untuk CL, ROS, CK, PNL, dan final report.
