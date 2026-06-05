# Batasan Sistem Fase MVP (Known Limitations)

Dokumen ini mencantumkan batasan teknis dan fungsional sistem **One Spirit Workflow & Business Analytics System** saat ini (fase MVP awal). 

Tujuan dokumen ini adalah membantu tim presenter menyajikan keterbatasan sistem dengan bahasa bisnis yang profesional kepada manajemen **PT. One Spirit Asia** serta mengarahkan pembicaraan ke pengembangan fase berikutnya.

---

## 1. Lingkungan Kerja Lokal (Local Running Environment)
- **Kondisi Saat Ini**: Aplikasi saat ini berjalan secara lokal di laptop presentasi (*local host/Docker desktop*).
- **Penjelasan Klien**: Sistem saat ini berada dalam fase uji coba purwarupa (*development prototype*). Pemasangan di server awan (*cloud server*) resmi milik PT. One Spirit Asia agar dapat diakses oleh seluruh staf dari luar kantor dijadwalkan pada **fase penyebaran produksi (production deployment)** setelah MVP disetujui.

## 2. Validasi Impor Data Excel Manual
- **Kondisi Saat Ini**: Pengunggahan file Excel operasional lama memberikan pratinjau validasi kesalahan, namun perbaikan data yang salah masih harus dilakukan manual pada file Excel sebelum diunggah kembali.
- **Penjelasan Klien**: Untuk fase MVP awal, fokus sistem adalah memastikan tidak ada data rusak yang masuk ke database. Pengembangan fitur perbaikan data langsung di web (*live inline editor*) diusulkan untuk **fase kemudahan operasional berikutnya**.

## 3. Akurasi Nominal Pembayaran Keuangan (Payment Tracking Refinement)
- **Kondisi Saat Ini**: Nominal dana masuk (*Received Cash*) dihitung berdasarkan jumlah pembayaran faktur penagihan yang disetujui. Namun, sistem belum menangani pencatatan termin pembayaran terperinci (seperti DP, termin 2, pelunasan) beserta tanggal jatuh temponya masing-masing.
- **Penjelasan Klien**: Perhitungan rasio kolektibilitas keuangan (*Collection Rate*) saat ini menggunakan basis penagihan sederhana. Mekanisme pencatatan termin pembayaran parsial secara terperinci direkomendasikan masuk pada **fase penyempurnaan keuangan (finance refinement phase)**.

## 4. Ekspor PDF Formal Otomatis (Server-side PDF Generation)
- **Kondisi Saat Ini**: Ekspor laporan eksekutif dan proyek menggunakan fitur cetak browser (*Print to PDF* via browser print).
- **Penjelasan Klien**: Fitur ini sangat praktis untuk laporan internal cepat. Pembuatan berkas PDF formal secara otomatis oleh server dengan kop surat resmi perusahaan untuk dikirimkan kepada klien eksternal direkomendasikan untuk **fase integrasi dokumen**.

## 5. Integrasi Dokumen & Notifikasi Eksternal
- **Kondisi Saat Ini**: Tautan Google Drive pada proyek diisi secara manual berupa link URL teks. Notifikasi pengingat tugas belum tersedia.
- **Penjelasan Klien**: Integrasi otomatis dengan folder Google Drive serta pengiriman notifikasi pengingat via WhatsApp atau Email (seperti alarm pengingat termin pembayaran) dijadwalkan untuk **fase integrasi pihak ketiga**.

## 6. Pembatasan Hak Akses Granular (Granular Permission Matrix)
- **Kondisi Saat Ini**: Hak akses pengguna sistem masih bersifat dasar (Administrator dapat mengakses semua menu, sementara staf internal memiliki hak akses pengeditan umum).
- **Penjelasan Klien**: Sistem keamanan saat ini menjamin perlindungan data utama. Matriks izin hak akses yang sangat granular (misalnya melarang PM tertentu melihat anggaran uang proyek) dapat disempurnakan pada **fase audit keamanan & manajemen pengguna**.
