# Dashboard Analytics Visualization - OneSpirit Workflow

Dokumen ini menjelaskan rancangan, formula data, perilaku visual, dan batasan teknis dari komponen visualisasi data (charts) yang diimplementasikan pada Executive Dashboard dalam **Sprint 12.3**.

---

## 1. Tujuan Visualisasi
Visualisasi ini bertujuan untuk memberikan gambaran cepat (executive summary) kepada tim manajemen PT One Spirit Asia mengenai performa komersial dan operasional perusahaan. Dengan adanya representasi grafis (charts) berbasis SVG, analisis konversi, perbandingan pendapatan, dan sebaran status proyek dapat dievaluasi secara intuitif saat presentasi klien (client validation).

---

## 2. Definisi dan Formula Setiap Chart

### A. Flow Inquiry ke Deal (DashboardFunnelChart)
* **Deskripsi**: Menampilkan alur konversi dari inquiry awal yang masuk menjadi proyek deal dan proyek yang dibatalkan.
* **Data Source**: `analyticsData.executive` (`total_inquiry`, `total_deal`, `total_cancel`).
* **Formula**:
  - **Inquiry Rate**: Selalu dianggap basis $100\%$.
  - **Deal Conversion Rate**: $\min(100, (\text{total\_deal} / \text{total\_inquiry}) \times 100)$
  - **Cancellation Rate**: $\min(100, (\text{total\_cancel} / \text{total\_inquiry}) \times 100)$

### B. Perbandingan Deal dan Cancel (DashboardRateComparison)
* **Deskripsi**: Visualisasi radial gauge membandingkan persentase rasio deal dengan persentase rasio pembatalan secara berdampingan.
* **Data Source**: `analyticsData.executive` (`deal_rate`, `cancel_rate`).
* **Formula**:
  - **Deal Rate**: Diambil langsung dari nilai agregat `deal_rate` di database (persentase total deal terhadap total proyek).
  - **Cancel Rate**: Diambil langsung dari nilai agregat `cancel_rate` di database (persentase total batal terhadap total proyek).
  - **SVG Circumference Offset**: $251,2 - (251,2 \times \text{rate}) / 100$ (menggunakan radius lingkaran 40).

### C. Perbandingan Pendapatan (DashboardRevenueChart)
* **Deskripsi**: Bar perbandingan antara nilai anggaran yang diproyeksikan, nilai anggaran yang sudah terkonfirmasi melalui kontrak, dan target pendapatan tahunan.
* **Data Source**: 
  - `potential_revenue` (Estimasi Pipeline) dari `analyticsData.executive`.
  - `confirmed_revenue` (Revenue Terkonfirmasi) dari `analyticsData.executive`.
  - `revenue_target` (Target Revenue) dari `analyticsData.target` (Default: Rp 9,2 Miliar).
* **Formula**:
  - Batas skala bar dihitung relatif terhadap nilai maksimum dari ketiga variabel di atas:
    $$\text{Scale Percent} = (\text{Nilai Variabel} / \max(\text{Potential}, \text{Confirmed}, \text{Target})) \times 100$$

### D. Komposisi Status Project (DashboardStatusDistribution)
* **Deskripsi**: Menampilkan persentase jumlah proyek berdasarkan masing-masing status operasional yang aktif (Inquiry, Penawaran, Terkonfirmasi, Persiapan, Berjalan, Selesai, Batal, Ditutup).
* **Data Source**: `analyticsData.project.count_by_status` (Katalog hitungan per status).
* **Formula**:
  - **Persentase Share**: $(\text{Jumlah Proyek Status} / \text{Total Proyek}) \times 100$
  - Diurutkan dari jumlah proyek terbanyak ke terkecil.

### E. Kontribusi Source (DashboardSourceContribution)
* **Deskripsi**: Menampilkan share kontribusi nilai proyek (confirmed revenue) berdasarkan kategori rujukan hotel atau partner rujukan lainnya.
* **Data Source**: `analyticsData.source_analytics` (list data referensi rujukan).
* **Formula**:
  - **Persentase Share**: $(\text{Confirmed Revenue Source} / \text{Total Confirmed Revenue Semua Source}) \times 100$
  - Hanya menampilkan source yang memiliki `confirmed_revenue > 0`, diurutkan secara descending.

---

## 3. Perilaku Empty State (Empty State Behavior)

Untuk menjaga ketahanan antarmuka pengguna (UI durability):
1. **Pencegahan Error Pembagian Nol (Zero Division Guard)**: Jika total inquiry atau total proyek bernilai 0, sistem secara otomatis mengeset persentase ke `0%` daripada menghasilkan `NaN` atau `Infinity`.
2. **Ketiadaan Data**: Jika `totalInquiry` adalah 0 (atau list `sourceAnalytics` kosong), panel visualisasi akan merender ikon SVG abu-abu dengan deskripsi pesan informatif seperti:
   - *"Belum ada data flow inquiry."*
   - *"Data source belum cukup untuk divisualisasikan."*
3. **Null/Undefined Checks**: Seluruh props di dalam komponen chart memiliki default value (`0`, `0.0`, atau array kosong `[]`) untuk mencegah crash jika backend mengembalikan nilai kosong.

---

## 4. Batasan Teknis (Known Limitations)

1. **Static Rendering**: Charts ini menggunakan SVG statis interaktif dengan efek transisi CSS murni. Tidak mendukung interaksi kursor tingkat lanjut (seperti zoom-in chart atau click-to-drilldown data) yang biasa ada pada library berat seperti Chart.js.
2. **Target Pendapatan Keras (Hardcoded Target Fallback)**: Jika tabel target revenue di database kosong, Target Revenue di-fallback secara hardcoded ke nilai Rp 9.200.000.000 (Rp 9,2M) sesuai rencana anggaran direksi tahun 2025.
