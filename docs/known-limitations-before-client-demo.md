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
- **Kondisi Saat Ini**: Sistem keamanan dasar telah diimplementasikan, termasuk penyembunyian tautan dokumen PNL sensitif untuk peran `Staff`. Namun, pembatasan hak akses menu atau tombol edit/view secara menyeluruh untuk halaman lain belum bersifat granular per divisi.
- **Penjelasan Klien**: Sistem keamanan saat ini telah menjamin perlindungan data keuangan utama (PNL). Matriks izin hak akses yang sangat mendalam (misalnya membatasi PM agar tidak bisa mengedit data customer) dijadwalkan untuk disempurnakan pada **fase audit keamanan & manajemen pengguna lanjut**.

## 7. Penyimpanan Berkas Langsung di Server (Direct Document Storage)
- **Kondisi Saat Ini**: Modul instrumen proyek (**CL, ROS, CK, PNL, PF, MATRIX**) telah memiliki pelacakan status operasional, tanggal jatuh tempo, dan skor kesiapan terintegrasi. Namun berkas-berkas tersebut masih dilampirkan menggunakan tautan (URL) Google Drive luar, bukan diunggah langsung ke database server sistem.
- **Penjelasan Klien**: Untuk tahap MVP saat ini, pencatatan berbasis tautan luar sangat praktis untuk fleksibilitas penyimpanan. Fitur unggah berkas PDF/Excel secara langsung ke server internal atau folder otomatis Google Drive terintegrasi direkomendasikan untuk **fase manajemen dokumen terintegrasi**.
## 8. Sifat Peringatan Gerbang Kesiapan (Readiness Warning Flexibility)
- **Kondisi Saat Ini**: Sebagian besar kondisi gerbang kesiapan (seperti dokumen CL/ROS/CK belum selesai saat masuk status Ready/Running) disajikan sebagai peringatan (*warnings*), bukan pemblokir keras (*hard blockers*) yang langsung menghentikan proses kerja. Hanya kondisi yang benar-benar tidak aman (seperti menjalankan proyek yang berstatus Canceled) yang diblok secara kritis dan memerlukan override pembaruan paksa (*force update*).
- **Penjelasan Klien**: Hal ini dirancang agar sistem tidak menghambat kelancaran operasional di lapangan jika terjadi kondisi mendesak. Sistem memberikan rekomendasi tindakan preventif tanpa mematikan fleksibilitas pengambilan keputusan PM/PO secara kaku.
## 9. Penjadwalan Kerja Kru dan Kalender Operasional (Crew Scheduling & Operational Calendar)
- **Kondisi Saat Ini**: PM Control Center merangkum event mendatang dalam daftar tabel linimasa periode (7 hari / 14 hari) berdasarkan tanggal proyek, namun belum terintegrasi dengan tampilan kalender visual bulanan interaktif atau modul penugasan jadwal kru per jam secara detail.
- **Penjelasan Klien**: Modul PM Control Center fokus pada pemantauan gerbang kesiapan berkas operasional dan instrumen event. Visualisasi kalender operasional interaktif (*interactive operational calendar*) dan manajemen jadwal tim Kru lapangan direncanakan untuk **fase manajemen penjadwalan & logistik lanjutan**.
## 10. Pendeteksian Aktivitas Komersial & Riwayat Follow-up
- **Kondisi Saat Ini**: PO Control Center merekomendasikan prioritas follow-up berdasarkan kondisi statis data (seperti budget, status, dan sisa hari event), namun belum melacak aktivitas komunikasi nyata (log telepon, histori chat WhatsApp, atau email terkirim).
- **Penjelasan Klien**: Fitur ini sangat krusial untuk melacak produktivitas. Sistem pencatatan log aktivitas komunikasi komersial secara dinamis dengan klien direncanakan untuk **fase penyempurnaan CRM & aktivitas penjualan**.
## 11. Pelacakan Jatuh Tempo Faktur Sederhana
- **Kondisi Saat Ini**: Peringatan tagihan overdue didasarkan pada perbandingan tanggal jatuh tempo faktur secara sederhana pada database, belum terintegrasi dengan sistem akuntansi eksternal resmi.
- **Penjelasan Klien**: Di MVP, pelacakan difokuskan untuk memberikan warning kepada PO agar segera melakukan follow-up. Rekonsiliasi mutasi bank otomatis dan sinkronisasi sistem akuntansi pihak ketiga direncanakan pada **fase modul keuangan terintegrasi**.

