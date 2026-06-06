# Dokumentasi Sprint 8: Project Readiness & Event Execution Control

Dokumen ini mendokumentasikan implementasi Gerbang Kesiapan Proyek (Project Readiness Gates) dan Kontrol Eksekusi Event yang dibangun pada Sprint 8.

---

## 1. Tujuan Operasional (Objective)
Tujuan utama Sprint 8 adalah membangun kontrol kesiapan operasional sebelum proyek/event berpindah ke status daur hidup yang lebih lanjut (seperti status program **Ready**, **Running**, **Completed**, atau **Closed**). 

Sistem mengevaluasi status instrumen, dokumen pendukung, kepemilikan proyek, tanggal pelaksanaan, dan pembayaran finansial untuk memberikan indikator visual, rekomendasi aksi operasional, serta peringatan sebelum status diubah.

---

## 2. Kebijakan Warning vs Blocker (Transition Policy)
Sistem membagi temuan menjadi dua kategori:
1. **Peringatan (Warnings / Non-Blocking)**: Masalah operasional yang tidak menghalangi proses bisnis secara keras. Transisi status tetap diizinkan, tetapi pengguna akan melihat konfirmasi peringatan dan sistem akan mencatat peringatan tersebut di log aktivitas. Contoh: CL belum siap, ROS belum Done, atau PNL belum diunggah.
2. **Pemblokir Kritis (Critical Blockers)**: Kondisi tidak aman yang secara keras menghalangi transisi status kecuali pengguna dengan otorisasi khusus menggunakan opsi **Force Update** (Pembaruan Paksa). Contoh: Mencoba menjalankan (status Program `Running`) proyek yang telah dibatalkan (status Project `Canceled`).

---

## 3. Aturan Gerbang Kesiapan (Readiness Gate Rules)

### A. Aturan Program Status
- **Target: "Ready"** (Siap Hari-H)
  - Peringatan jika: CL (Contract Letter), ROS (Rundown of Show), CK (Checklist) belum berstatus `Done` atau missing.
  - Peringatan jika: PNL belum `Done` untuk proyek dengan Quotation `Signed & Deal`.
  - Peringatan jika: Ada instrumen berstatus `Need Revision` atau telat (`Overdue`).
  - Peringatan jika: Tanggal pelaksanaan (`event_date_start`) kosong.
  - Peringatan jika: Program Owner (PO) atau Program Manager (PM) belum ditugaskan.
- **Target: "Running"** (Event Sedang Berjalan)
  - Peringatan jika: Skor kesiapan proyek (Readiness Score) kurang dari 80%.
  - Peringatan jika: ROS atau CK belum berstatus `Done`.
  - Peringatan jika: Ada instrumen wajib berstatus `Need Revision`.
  - Peringatan jika: Tanggal pelaksanaan kosong.
  - Pemblokir kritis jika: Proyek dalam status utama `Canceled`.
- **Target: "Completed"** (Event Selesai Lapangan)
  - Peringatan jika: Dokumen lampiran proyek kosong.
  - Peringatan jika: Masih ada instrumen yang telat (`Overdue`).
  - Peringatan jika: ROS atau CK belum berstatus `Done`.
  - Peringatan jika: Tanggal selesai event (`event_date_end`) kosong atau berada di masa depan.
- **Target: "Closed"** (Arsip Proyek Selesai)
  - Peringatan jika: Status pembayaran (`payment_status`) bukan `Paid`.
  - Peringatan jika: Dokumen lampiran proyek kosong.
  - Peringatan jika: PNL belum `Done` atau missing.

### B. Aturan Project Status
- **Target: "Closed"** (Proyek Ditutup Buku)
  - Peringatan jika: Status pembayaran bukan `Paid`.
  - Peringatan jika: Status program belum `Completed`, `Reporting`, atau `Closed`.
  - Peringatan jika: Dokumen lampiran proyek kosong.
  - Peringatan jika: PNL belum `Done` atau missing.
  - Peringatan jika: Ada instrumen berstatus `Need Revision`.
- **Target: "Canceled"** (Proyek Dibatalkan)
  - Peringatan jika: Catatan alasan pembatalan (`cancel_reason`) kosong.
  - Peringatan jika: Quotation sudah berstatus `Signed & Deal`.
  - Peringatan jika: Status pembayaran sudah masuk `Paid` atau `Partial Paid`.

---

## 4. Perubahan API (API Specs)

### A. Endpoint Pratinjau Kesiapan
*   **POST** `/api/v1/projects/{project_id}/readiness/check`
*   **Request Body**:
    ```json
    {
      "status_type": "program_status",
      "target_status": "Ready",
      "notes": "Optional remarks"
    }
    ```
*   **Response**:
    ```json
    {
      "project_id": "uuid-string",
      "status_type": "program_status",
      "target_status": "Ready",
      "allowed": true,
      "severity": "warning",
      "can_override": true,
      "readiness_score": 75.0,
      "instrument_completion_rate": 66.7,
      "warnings": [
        "Contract/Confirmation Letter (CL) is missing or not marked as 'Done'."
      ],
      "blockers": [],
      "recommendations": [
        "Lengkapi dan setujui Contract/Confirmation Letter (CL)."
      ]
    }
    ```

### B. Endpoint Transisi Status (Dengan Parameter Force)
*   **PATCH** `/api/v1/projects/{project_id}/status`
*   **Payload**:
    ```json
    {
      "status_type": "program_status",
      "new_status": "Running",
      "notes": "Forcing start of event",
      "force": true
    }
    ```
*   **Logika Backend**:
    *   Mengevaluasi gerbang kesiapan proyek.
    *   Jika `severity == "critical"` dan `force == false`, mengembalikan **HTTP 409 Conflict** beserta informasi detil blocker.
    *   Jika `severity == "critical"` dan `force == true`, mengizinkan transisi status dan mencatat log aktivitas dengan aksi `status_force_updated`.
    *   Jika hanya memiliki warning operasional biasa, transisi berjalan normal dan mencatat aksi `status_changed_with_readiness_warning`.

---

## 5. Komponen Frontend Baru & Pembaruan

1.  **ProjectExecutionControlPanel.vue**: Panel sidebar kanan di halaman detail proyek untuk memvisualisasikan data kesiapan, durasi hari tersisa sebelum event, rekomendasi aksi operasional, dan log ringkasan peringatan.
2.  **ReadinessSummary.vue**: Komponen visual gauge di dashboard utama yang menampilkan status agregat proyek operasional (*Ready Projects*, *Not Ready Projects*, *Upcoming 7 Days*, *Overdue Events*, dan ringkasan masalah instrumen).
3.  **ProjectDetail.vue (Pembaruan)**: Integrasi overlay modal konfirmasi status yang otomatis mengecek kesiapan via API sebelum menerapkan status baru.
4.  **Projects.vue (Pembaruan)**: Penambahan kolom **Readiness** pada tabel daftar proyek utama untuk melihat skor kesiapan dan persentase penyelesaian instrumen secara sekilas.
5.  **PmWorkloadTable.vue (Pembaruan)**: Penambahan metrik rata-rata kesiapan dan jumlah event mendadak per PM.

---

## 6. Penanganan Sensitivitas Keuangan (PNL Sensitivity)
Mekanisme pengamanan dokumen Profit & Loss (PNL) tetap terjaga secara konsisten:
- Pengguna dengan peran `Staff` hanya dapat melihat persentase kesiapan dan status instrumen PNL (misalnya 'Done' atau 'Need Revision'), namun tautan dokumen Google Drive-nya disensor secara otomatis demi menjaga kerahasiaan profit margin perusahaan.
- Catatan sensitivitas keamanan PNL dievaluasi sebagai peringatan informasional saja dan tidak mengurangi skor kesiapan (`project_readiness_score`) proyek.

---

## 7. Langkah Verifikasi (Verification Steps)

### Pengujian Backend
Jalankan tes backend terintegrasi:
```bash
docker exec onespirit_backend pytest app/tests/test_readiness_gates.py -p no:warnings
```

### Pengujian Frontend Build
Jalankan kompilasi aset produksi frontend untuk memastikan tidak ada kesalahan impor komponen:
```bash
docker exec onespirit_frontend npm run build
```

---

## 8. Rekomendasi Sprint Berikutnya (Sprint 9 Recommendation)
Untuk Sprint 9, direkomendasikan berfokus pada integrasi Google Drive API secara dinamis serta penyempurnaan sistem notifikasi WhatsApp/Email otomatis berdasarkan jatuh tempo instrumen atau pemicu gerbang kesiapan kritis.
