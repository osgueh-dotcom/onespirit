# Dokumentasi Sprint 9: Operational Dashboard & PM Control Center

Dokumen ini mendokumentasikan implementasi PM Control Center (Dashboard Operasional) dan Logika Prioritas Aksi untuk mempermudah Program Manager dan manajemen memantau persiapan event.

---

## 1. Tujuan Operasional (Objective)
Berbeda dengan Dashboard Eksekutif yang mengukur indikator bisnis tingkat tinggi (KPI, deal rates, financial conversion), **PM Control Center** dibangun sebagai alat bantu operasional harian/mingguan bagi Program Manager untuk:
*   Mendeteksi event-event terdekat berdasarkan sisa hari pengerjaan.
*   Mengidentifikasi proyek dengan tingkat kesiapan rendah (Readiness Score < 80%).
*   Memberikan alarm visual untuk instrumen checklist operasional yang melewati tenggat waktu (Overdue).
*   Menyorot instrumen yang membutuhkan perbaikan data (Need Revision).
*   Menyajikan **Priority Actions** (Daftar Aksi Prioritas) untuk menindaklanjuti risiko persiapan event secara cepat.

---

## 2. Logika Prioritas Aksi (Priority Actions Logic)
Tiap proyek/event diklasifikasikan ke dalam 4 tingkat prioritas berdasarkan kriteria kesiapan dan waktu:

1.  **Critical (Kritis)**:
    *   Event dilaksanakan hari ini (atau tanggal pelaksanaan event sudah terlewati) dengan skor kesiapan proyek < 80%.
    *   Terdapat kondisi tidak aman kritis (blocker) pada daur hidup status (misalnya status program Running tetapi status proyek Canceled).
2.  **High (Tinggi)**:
    *   Event dilaksanakan dalam waktu 7 hari ke depan dengan skor kesiapan proyek < 80%.
    *   Ada instrumen operasional proyek yang melewati tenggat waktu (Overdue).
    *   Ada instrumen proyek yang ditandai butuh perbaikan (Need Revision).
    *   Dokumen krusial ROS (Rundown) atau CK (Checklist) belum berstatus 'Done' untuk proyek aktif (Ready/Running).
3.  **Medium (Sedang)**:
    *   Event dilaksanakan dalam waktu 14 hari ke depan dengan skor kesiapan proyek < 90%.
    *   Dokumen CL (Contract Letter) atau PNL belum selesai ('Done') untuk proyek komersial Signed & Deal.
    *   Dokumen laporan pertanggungjawaban kosong untuk proyek yang programnya sudah selesai (Completed/Reporting).
4.  **Low (Rendah)**:
    *   Proyek aktif biasa yang tidak memenuhi kriteria di atas (tidak memiliki risiko urgensi waktu atau kesiapan checklist).

---

## 3. Spesifikasi API (API Specs)

*   **Endpoint**: `GET /api/v1/dashboard/pm-control-center`
*   **Query Parameters**:
    *   `pm_id`: Filter berdasarkan Program Manager (PM) yang ditugaskan.
    *   `po_id`: Filter berdasarkan Program Owner (PO) yang ditugaskan.
    *   `date_from` / `date_to`: Filter berdasarkan rentang tanggal event.
    *   `readiness_min` / `readiness_max`: Filter proyek berdasarkan rentang persentase kesiapan (0 s/d 100).
    *   `include_closed` (Default: `false`): Menyertakan proyek berstatus Closed.
    *   `include_canceled` (Default: `false`): Menyertakan proyek berstatus Canceled.
    *   `instrument_status`: Menyaring proyek yang memiliki instrumen dengan status tertentu (misal: 'Need Revision').
    *   `event_window` (Default: `all`): Menyaring rentang waktu pengerjaan event:
        *   `today`: Pelaksanaan event hari ini.
        *   `next_7_days`: Event dilaksanakan dalam 7 hari mendatang.
        *   `next_14_days`: Event dilaksanakan dalam 14 hari mendatang.
        *   `this_month`: Event dilaksanakan pada bulan berjalan.
        *   `overdue`: Event yang jadwal selesainya sudah lewat namun status belum selesai.
        *   `all`: Semua proyek aktif.

---

## 4. Antarmuka PM Control Center (Frontend Sections)

Halaman depan `/pm-control-center` menyajikan panel dashboard terintegrasi:
1.  **KPI Operasional Cards**:
    *   Jumlah event hari ini.
    *   Jumlah event mendatang (7 Hari).
    *   Jumlah proyek tidak siap (skor kesiapan < 80%).
    *   Jumlah instrumen checklist Overdue.
    *   Jumlah instrumen checklist Need Revision.
    *   Rata-rata skor kesiapan operasional proyek secara agregat.
2.  **Filter Panel**: Pilihan dropdown PM, PO, Periode Event Window, Tanggal Mulai/Selesai, dan toggle status Closed/Batal.
3.  **Tab Menu Kontrol**:
    *   **Tab Prioritas**: Berisi kartu Priority Actions dengan rincian masalah, rekomendasi solusi, dan tombol navigasi langsung ke detail proyek.
    *   **Tab Jadwal Event & Kesiapan**: Tabel event mendatang 14 hari beserta persentase kesiapan, status, PM, dan aksi terdekat. Dilengkapi tabel pendukung proyek belum siap (< 80%).
    *   **Tab Checklist & Revisi**: Tabel instrumen Overdue (lengkap dengan perhitungan hari keterlambatan) dan instrumen yang membutuhkan revisi (Need Revision).
    *   **Tab Beban Kerja PM**: Distribusi beban persiapan event aktif, keterlambatan checklist, dan rata-rata skor kesiapan per Program Manager.

---

## 5. Pengujian & Verifikasi (Verification)

### Tes Backend Otomatis
Jalankan pengujian unit terintegrasi:
```bash
docker exec onespirit_backend pytest app/tests/test_pm_control_center.py -p no:warnings
```

### Build Frontend
Jalankan kompilasi untuk memverifikasi kebersihan file Vue:
```bash
docker exec onespirit_frontend npm run build
```
