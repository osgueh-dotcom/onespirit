# Rekomendasi Data Demonstrasi (Demo Data Guide)

Dokumen ini memandu presenter dalam memilih dan menyajikan data proyek/event dari database lokal untuk memberikan demonstrasi yang meyakinkan kepada **PT. One Spirit Asia**. 

Sistem modern ini diisi oleh data awal dari proses pembacaan Excel (*seed data*) dan simulasi proyek. Untuk presentasi yang sukses, disarankan menunjukkan dua jenis data proyek dengan karakteristik kontras.

---

## 1. Proyek Model Utama (Good Data Profile)
*Tujuan: Menunjukkan tampilan sistem yang ideal saat seluruh staf disiplin mengisi data administrasi proyek.*

### Karakteristik Proyek:
- **Status Program**: `Ready`, `Running`, atau `Completed`.
- **Status Project**: `Active` atau `Reporting`.
- **Status Quotation**: `Signed & Deal`.
- **Staf Ditugaskan**: PO (Program Owner) dan PM (Program Manager) terisi secara valid.
- **Data Keuangan**: Budget terisi nominal wajar (misal: > Rp50.000.000), status pembayaran terisi (misal: `Invoice Sent` atau `Partial Paid`).
- **Dokumen**: Tautan Google Drive dokumen penawaran/kontrak terisi.

### Poin Utama yang Harus Ditunjukkan:
- Tunjukkan panel **Status Timeline** di halaman detail proyek untuk memperlihatkan transisi alur progres yang teratur dari tahap Inquiry hingga Closed.
- Tunjukkan tabel **Activity Log** untuk melihat rekaman historis audit alur kerja (siapa staf yang mengubah status, kapan diubah).
- Tunjukkan tautan Google Drive dokumen yang dapat diklik langsung.

---

## 2. Proyek Bermasalah Administratif (Data Quality Issue Profile)
*Tujuan: Menunjukkan kecerdasan sistem dalam mendeteksi kesalahan input operasional secara otomatis tanpa audit manual.*

### Karakteristik Proyek:
- **Status Quotation**: `Cancel` (Batal) tetapi kolom **Alasan Pembatalan (Cancel Reason)** dibiarkan kosong oleh staf.
- ATAU
- **Staf Ditugaskan**: PO atau PM dibiarkan kosong (`None`) pada proyek aktif.
- ATAU
- **Data Keuangan**: Nilai budget diisi `0` atau dibiarkan kosong, atau proyek berstatus `Closed` tetapi status pembayaran masih `Invoice Sent` (belum bayar).

### Poin Utama yang Harus Ditunjukkan:
- Buka detail proyek ini, tunjukkan kotak **Validation Warnings** (Peringatan Validasi) berwarna kuning/merah yang secara instan menunjukkan apa saja berkas atau tugas yang kurang.
- Kembali ke Dashboard utama, tunjukkan bagaimana jumlah masalah di proyek ini terakumulasi secara akurat pada panel **Review Kualitas Data** (misalnya meningkatkan angka *Missing PO* atau *Cancel without Reason*).
- Jelaskan bahwa fitur audit otomatis ini membantu direksi One Spirit memastikan semua staf melengkapi data sebelum rapat koordinasi bulanan.

---

## 3. Cara Mempersiapkan Data Demo di Database Lokal
Jika database dalam keadaan bersih (baru dideploy lokal), presenter dapat mempersiapkan data contoh langsung dari UI aplikasi atau dengan mengecek database:
1. **Membuat Data Bagus**:
   - Masuk ke menu **Projects**, klik tombol tambah proyek atau edit proyek yang ada.
   - Isi seluruh input form secara lengkap. Tunjuk salah satu user sebagai PO dan user lainnya sebagai PM. Hubungkan dengan Customer resmi dan Event Source resmi.
2. **Membuat Data Masalah**:
   - Buat satu proyek baru. Kosongkan nilai budget (isi `0`).
   - Jangan tunjuk PO atau PM (biarkan kosong).
   - Ubah status quotation menjadi `Cancel`, namun biarkan text area alasan pembatalan kosong. Simpan proyek tersebut.
   - Verifikasi bahwa dashboard langsung menampilkan penambahan 1 isu baru di panel kualitas data.
