# Panduan Logika & Bisnis — Source & Vendor Performance Center

Dokumen ini merinci definisi bisnis, rumus perhitungan, visualisasi metrik, fallback data, serta batasan teknis yang digunakan di dalam modul Source & Vendor Performance Center pada OneSpirit Workflow System.

---

## 1. Definisi Bisnis & Formula Metrik

Modul ini memantau kinerja komersial berdasarkan asal penawaran (Lead Source) dan pelaksana logistik lapangan (Vendor Partner) untuk mendukung pengambilan keputusan strategis oleh Management dan Program Owner (PO).

### A. Source Performance Metrics

1. **Total Projects (Total Proyek)**: Jumlah seluruh proyek yang terdaftar di dalam rentang filter yang aktif.
2. **Active Projects (Proyek Aktif)**: Jumlah proyek yang sedang berjalan (tidak berstatus Closed dan tidak berstatus Cancel/Canceled).
3. **Confirmed Projects (Deal Proyek)**: Jumlah proyek yang telah disepakati oleh klien (status quotation `Signed & Deal`).
4. **Cancelled Projects (Proyek Batal)**: Jumlah proyek yang dibatalkan oleh klien (status quotation `Cancel`, status program `Cancel`, atau status proyek `Canceled`).
5. **Pending Quotation (Proyek Menunggu Penawaran)**: Jumlah proyek yang berada dalam tahap negosiasi awal (status quotation `Draft`, `Sent`, `Follow Up`, atau `Revision`).
6. **Potential Revenue (Pendapatan Potensial)**: Akumulasi nilai anggaran (`budget`) dari seluruh proyek.
7. **Confirmed Revenue (Pendapatan Terkonfirmasi)**: Akumulasi anggaran dari proyek yang telah disepakati (status quotation `Signed & Deal` ATAU status program termasuk dalam kelompok Confirmed/Preparation/Ready/Running/Completed/Reporting/Closed).
8. **Outstanding Payment (Tagihan Tertunggak)**: Akumulasi selisih nominal dari seluruh invoice yang terbit dikurangi nominal payment yang telah disetujui (`status = 'approved'`).
9. **Average Project Value (Rata-rata Nilai Proyek)**: 
   $$\text{Average Value} = \frac{\text{Potential Revenue}}{\text{Total Projects}}$$
10. **Conversion Rate (Tingkat Konversi Proyek)**: Persentase tingkat keberhasilan penawaran menjadi kesepakatan komersial:
   $$\text{Conversion Rate (\%)} = \frac{\text{Confirmed Projects}}{\text{Total Projects}} \times 100$$
11. **Cancellation Rate (Tingkat Pembatalan)**: Persentase proyek yang dibatalkan:
   $$\text{Cancellation Rate (\%)} = \frac{\text{Cancelled Projects}}{\text{Total Projects}} \times 100$$
12. **Follow-up Needed (Beban Follow-up)**: Jumlah proyek yang memerlukan tindakan follow-up segera berdasarkan prioritas kritis atau overdue pembayaran.

### B. Vendor Performance Metrics

Vendor memantau kinerja hotel, tempat acara (venue), atau sub-kontraktor logistik lapangan:
1. **Usage Frequency (Frekuensi Penggunaan)**: Jumlah total proyek yang menggunakan jasa vendor tersebut.
2. **Average Project Value per Vendor**: Nilai rata-rata budget proyek yang diserahkan kepada vendor terkait.
3. **Confirmed Revenue per Vendor**: Nilai anggaran proyek terkonfirmasi yang melibatkan vendor tersebut.
4. **Risk Count per Vendor**: Jumlah proyek di bawah vendor terkait yang memicu peringatan risiko (seperti overdue payment atau pembatalan tanpa alasan).

---

## 2. Pemicu Peringatan Risiko (Risk Alert Triggers)

Sistem melakukan audit reaktif otomatis untuk memunculkan alert komersial:
* **High Cancellation Rate**: Dipicu jika suatu Source atau Vendor memiliki total proyek $\ge 2$ dan persentase pembatalan proyek (`cancel_rate`) $> 30\%$. (Level: `High`)
* **High Pending Quotation**: Dipicu jika suatu Source memiliki total proyek $\ge 2$ dan rasio proyek pending penawaran $> 50\%$. (Level: `Medium`)
* **High Outstanding Payment**: Dipicu jika outstanding tagihan kumulatif pada suatu Source $> \text{Rp } 50.000.000$. (Level: `High`)
* **Missing Source Mapping**: Dipicu jika proyek aktif terdaftar tanpa relasi `event_source_id`. (Level: `Medium`)
* **Missing Vendor Partners**: Dipicu jika proyek memiliki data source tetapi nama vendor kosong (`vendor_name` is null/empty/`"-"`). (Level: `Info`)

---

## 3. Fallback Data & Kualitas Data (Data Quality)

Karena data historis atau input operasional staff belum tentu lengkap, sistem menerapkan fallback aman berikut agar sistem tidak crash (division by zero / null pointer exceptions):
1. **Bila Event Source Kosong**: Proyek dikategorikan ke dalam Lead Source `"Direct"` dan nama vendor `"-"`.
2. **Bila Nilai Anggaran Kosong**: Dianggap bernilai `Rp 0`. Namun proyek dengan status `Signed & Deal` bernilai Rp 0 akan memicu alert prioritas kritis (`Critical`) agar PO segera melakukan revisi data.
3. **Data Vendor Tidak Terstruktur**: Dikarenakan belum tersedianya entitas database `Vendor` terpisah, grouping vendor dilakukan murni berdasarkan kesamaan string teks `vendor_name` pada tabel `EventSource`. Ini didokumentasikan di frontend sebagai limitasi MVP.
