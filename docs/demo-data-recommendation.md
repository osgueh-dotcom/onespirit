# Rekomendasi Data Demonstrasi (Demo Data Guide)

Dokumen ini memandu presenter dalam memilih dan menyajikan data proyek/event dari database lokal untuk memberikan demonstrasi yang meyakinkan kepada **PT. One Spirit Asia**. 

Sistem modern ini diisi oleh data awal dari proses pembacaan Excel (*seed data*) dan simulasi proyek. Untuk presentasi yang sukses, disarankan menunjukkan dua jenis data proyek dengan karakteristik kontras.

---

## 1. Proyek Model Utama (Good Data Profile)
*Tujuan: Menunjukkan tampilan sistem yang ideal saat seluruh staf disiplin mengisi data administrasi proyek dan seluruh instrumen operasional terpenuhi.*

### Karakteristik Proyek:
- **Status Program**: `Ready`, `Running`, atau `Completed`.
- **Status Project**: `Active` atau `Reporting`.
- **Status Quotation**: `Signed & Deal`.
- **Staf Ditugaskan**: PO (Program Owner) dan PM (Program Manager) terisi secara valid.
- **Data Keuangan**: Budget terisi nominal wajar (misal: > Rp50.000.000), status pembayaran terisi (misal: `Invoice Sent` atau `Partial Paid`).
- **Dokumen / Instrumen Proyek**: Seluruh instrumen proyek (**CL, ROS, CK, PNL, PF, MATRIX**) berstatus `Done` dengan tautan dokumen terisi.
- **Readiness Score**: Mendekati `100%` (hijau) karena completion rate instrumen tinggi dan tidak ada peringatan status.

### Poin Utama yang Harus Ditunjukkan:
- Tunjukkan kartu **Project Readiness Indicator** di sidebar kanan dengan skor kesiapan `100%`.
- Perlihatkan tabel **Project Instruments & Checklist** yang bersih tanpa ada badge merah Overdue atau oranye Need Revision.
- **PNL Access Demonstration**: 
  - Masuk/simulasikan login sebagai `Admin`/`Finance` -> tautan PNL aktif dan dapat diklik.
  - Masuk/simulasikan login sebagai `Staff` -> tautan PNL tersembunyi/sensor (*Restricted*), menjaga kerahasiaan profit margin perusahaan.
- Tunjukkan tabel **Activity Log** di bagian bawah yang mencatat riwayat perubahan status instrumen secara terperinci.

---

## 2. Proyek Bermasalah Administratif (Data Quality & Instrument Issue Profile)
*Tujuan: Menunjukkan kemampuan sistem dalam mendeteksi ketidaksiapan operasional proyek secara otomatis dan memberikan alarm visual kepada PM/PO.*

### Karakteristik Proyek:
- **Status Quotation**: `Signed & Deal` tetapi instrumen **CL** atau **PNL** berstatus `Not Started` / `Need Revision` (atau link kosong).
- **Status Program**: `Ready` atau `Running` tetapi instrumen **ROS** atau **CK** belum berstatus `Done`.
- **Tanggal Jatuh Tempo**: Salah satu instrumen memiliki tanggal jatuh tempo (`Due Date`) yang telah lewat hari ini tetapi status belum `Done`.
- **Readiness Score**: Rendah (misal: < `50%` berwarna merah/oranye).

### Poin Utama yang Harus Ditunjukkan:
- Buka detail proyek ini, tunjukkan penurunan drastis pada **Readiness Score** di kartu sidebar.
- Tunjukkan indikator **Overdue** merah yang menyala di sebelah instrumen yang telat.
- Tunjukkan kotak **Validation Warnings** (Peringatan Validasi) yang secara otomatis mencantumkan masalah instrumen (misalnya: *"CL missing for Signed & Deal project"*, *"Instrument [ROS] is overdue"*).
- Kembali ke Dashboard utama, tunjukkan bagaimana data proyek bermasalah ini secara agregat terakumulasi pada **Instrument Readiness Summary** (misalnya meningkatkan angka *Missing CL* atau *Instruments Overdue*).

---

## 3. Skenario Transisi Status & Gerbang Kesiapan (Status Transition & Readiness Gate Demo)
*Tujuan: Memperagakan kecerdasan sistem dalam memandu pengguna saat mengganti status program/proyek serta penanganan override.*

### Langkah Uji Coba Demo:
1. **Skenario Peringatan Non-Bloking**:
   - Buka proyek yang instrumennya belum lengkap (misal: CL/ROS belum 'Done').
   - Di panel status, coba ubah status Program ke `Ready`.
   - Sistem akan memicu gerbang kesiapan dan menampilkan **Modal Peringatan Kesiapan (Readiness Warning Modal)** yang menyajikan daftar berkas yang belum lengkap sebelum status berubah.
   - Klik **"Tetap Lanjutkan"** untuk memperagakan kelonggaran sistem (fleksibilitas bisnis) yang membolehkan transisi dengan catatan.
2. **Skenario Pemblokiran Kritis (Critical Blocker)**:
   - Pilih proyek yang dibatalkan (Project Status: `Canceled`).
   - Coba ubah status Program ke `Running`.
   - Gerbang kesiapan akan memblokir penuh secara kritis karena kondisi tidak aman (tidak boleh menjalankan event yang sudah batal).
   - Tunjukkan kotak peringatan merah yang mengunci tombol simpan biasa.
   - Aktifkan opsi **"Pembaruan Paksa (Force Update)"** untuk memperagakan kemampuan override administrator untuk melanjutkan perubahan status dalam kasus darurat, kemudian simpan.

---

## 4. Cara Mempersiapkan Data Demo di Database Lokal
Jika database dalam keadaan bersih (baru dideploy lokal), presenter dapat mempersiapkan data contoh langsung dari UI aplikasi atau melalui file impor:
1. **Membuat Data Bagus**:
   - Tambah atau edit proyek yang ada di menu **Projects**.
   - Isi seluruh input form secara lengkap. Hubungkan dengan Customer dan Event Source resmi.
   - Pada panel **Project Instruments**, ubah status seluruh dokumen (**CL, ROS, CK, PNL, PF, MATRIX**) menjadi `Done`, isi URL tautan dokumen dengan link dummy, dan set tanggal jatuh tempo di masa depan.
2. **Membuat Data Masalah**:
   - Buat satu proyek baru, set status Quotation menjadi `Signed & Deal` dan status Program menjadi `Ready`.
   - Di panel instrumen, set status **CL** ke `Need Revision`.
   - Set tanggal jatuh tempo instrumen **ROS** ke kemarin (lalu simpan statusnya tetap `In Progress`).
   - Verifikasi bahwa Readiness Score proyek langsung merosot dan dashboard utama memperbarui metrik instrumen yang terlewat secara real-time.
3. **Menguji Impor Excel**:
   - Unggah file Excel contoh. Isi kolom instrumen dengan nilai `"Revision"`, `"Ada"`, atau link URL.
   - Verifikasi bahwa sistem impor memetakan status instrumen dengan tepat ke database (`Need Revision`, `Done` dengan URL) dan menampilkan warning impor jika ada nilai ambigu.

