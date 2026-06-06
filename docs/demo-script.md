# Skrip Demonstrasi Sistem One Spirit

Skrip ini dirancang untuk memandu presenter dari **GVSys (Gueh Visual Systems)** saat melakukan presentasi langsung kepada jajaran manajemen **PT. One Spirit Asia**.

---

## 1. Pembukaan (Opening)
> **Presenter**: 
> "Selamat pagi/siang Bapak dan Ibu dari manajemen PT. One Spirit Asia. Terima kasih atas waktu yang diberikan. Saya perwakilan dari Gueh Visual Systems (GVSys) hari ini sangat senang bisa mendemonstrasikan **One Spirit Workflow & Business Analytics System**.
> 
> Seperti yang kita diskusikan sebelumnya bersama Bapak Abdul Patah, operasional One Spirit sangat padat dengan berbagai event. Selama ini, data penawaran, status persiapan program, penagihan invoice, hingga pembagian beban kerja tim dikelola secara manual menggunakan file-file Excel yang tersebar. Hal ini rawan memicu ketidakselarasan data.
>
> Hari ini, kami mempersembahkan solusi modernisasi sistem web terintegrasi yang akan memusatkan seluruh alur kerja operasional dan laporan analitik bisnis Anda secara terstruktur dan terpadu. Mari kita masuk ke aplikasinya."

---

## 2. Halaman Login & Konsep PO/PM
*(Presenter membuka halaman login, lalu masuk ke aplikasi)*
> **Presenter**:
> "Ini adalah halaman masuk utama sistem. Kita akan masuk menggunakan akun manajemen/administrator. 
> 
> Satu hal penting yang ingin kami sampaikan adalah fleksibilitas penugasan tim. Di sistem ini, staf internal Anda tidak dikunci pada satu jabatan kaku. Seorang staf bisa bertindak sebagai **Program Owner (PO)** di proyek A, namun di proyek B dia bisa bertindak sebagai **Program Manager (PM)**. Sistem mendukung penunjukan peran dinamis ini per proyek secara fleksibel."

---

## 3. Executive Dashboard & Analitik Target
*(Presenter menunjukkan halaman Dashboard)*
> **Presenter**:
> "Setelah sukses masuk, pengguna langsung disambut oleh **Executive Dashboard**. Dashboard ini dirancang khusus sebagai alat evaluasi performa bagi manajemen senior dan direksi One Spirit.
> 
> Di bagian atas, Bapak dan Ibu dapat melihat KPI Utama: **Total Inquiry**, **Total Deal**, **Deal Rate**, hingga **Cancel Rate** yang semuanya terbarui berdasarkan database terpusat.
> 
> Di sisi kanan, sistem menampilkan persentase pencapaian target penjualan tahunan secara dinamis dari database, membandingkan akumulasi *Confirmed Revenue* (nilai kontrak yang disepakati) dengan target pendapatan direksi. 
> 
> Kami juga menambahkan metrik penagihan keuangan seperti **Actually Received Cash**, **Collection Rate**, dan sisa piutang **Outstanding Amount**. Ini sangat membantu manajemen memantau efektivitas divisi billing."

---

## 4. Narasi Eksekutif & Catatan Evaluasi Otomatis
*(Presenter menunjuk bagian Executive Summary Narrative dan Management Review Notes)*
> **Presenter**:
> "Bagi manajemen yang membutuhkan ringkasan cepat untuk rapat mingguan, sistem menyediakan **Executive Summary Narrative** dalam bahasa Indonesia yang dibuat secara otomatis oleh sistem. Narasi ini langsung mengompilasi total inquiry, deal, konversi pendapatan, dan memberikan peringatan dini jika tingkat pembatalan terpantau tinggi.
> 
> Di bawahnya, terdapat **Catatan Evaluasi Manajemen**. Sistem secara cerdas mengelompokkan temuan data ke dalam tiga poin:
> 1. *Kekuatan / Indikasi Positif*: Misalnya pencapaian target penjualan berjalan baik.
> 2. *Risiko / Bottlenecks*: Misalnya adanya penumpukan antrean proyek di tahap Inquiry.
> 3. *Rekomendasi Tindakan*: Saran operasional konkret bagi manajemen, seperti segera menunjuk PO untuk memproses penawaran."

---

## 5. Alur Kerja Proyek & Filter Analitik
*(Presenter berpindah ke halaman Projects)*
> **Presenter**:
> "Sekarang kita beralih ke halaman alur kerja proyek. Di sini, manajemen dapat memantau seluruh status daur hidup proyek dari tahap awal penawaran (*Quotation Status*), tahapan persiapan program operasional (*Program Status*), status penagihan (*Payment Status*), hingga penutupan proyek (*Project Status*).
> 
> Untuk mempermudah navigasi di tengah ratusan proyek, kami menyediakan panel **Filter Analitik**. Kita bisa menyaring proyek berdasarkan nama PO tertentu untuk melihat beban kerjanya, menyaring berdasarkan kategori pelanggan seperti Corporate untuk melihat pangsa pasar utama, atau memantau proyek yang bersumber dari partner hotel."

---

## 6. Detail Proyek, Readiness Score, & Kontrol Eksekusi Event
*(Presenter membuka salah satu detail proyek contoh)*
> **Presenter**:
> "Mari kita buka salah satu detail proyek. Di halaman ini, semua informasi penting dikonsolidasikan dalam satu tempat: detail anggaran, penanggung jawab PO/PM, detail pembayaran, hingga instrumen kesiapan operasional proyek.
> 
> Pertama, perhatikan sidebar kanan. Di sini terdapat panel baru **Event Execution Control**. Panel ini menampilkan **Readiness Score** (Skor Kesiapan Proyek) dan **Instrument Completion Rate** yang terperinci. Selain itu, terdapat **Indikator Urgensi Tanggal Event** yang secara dinamis menghitung hari tersisa sebelum acara dimulai (misal: 'Event dalam X hari' atau 'Event sudah lewat').
> 
> Panel ini juga menyajikan **Rekomendasi Aksi Operasional** secara otomatis, seperti menyarankan pengisian CL, ROS, atau CK sebelum event berjalan.
> 
> Di bawahnya, terdapat panel **Project Status Timeline & Transition**. Jika kita mencoba mengubah status (misalnya mengubah status program dari Inquiry langsung ke Running), sistem tidak akan membiarkan perubahan konyol tanpa peringatan. Sistem akan memicu **Gerbang Kesiapan (Readiness Gate)**:
> 1. Sistem memeriksa kelengkapan berkas CL/ROS/CK/PNL.
> 2. Jika ada kekurangan, sistem memunculkan pop-up modal peringatan berisi daftar catatan kesiapan operasional yang belum terpenuhi dan meminta konfirmasi eksplisit dari user sebelum status diubah.
> 3. Jika terdapat kondisi tidak aman kritis (misalnya mencoba menjalankan proyek yang berstatus Canceled), sistem secara ketat memblokir transisi tersebut. Pengguna dengan otoritas khusus dapat memilih opsi **Force Update** untuk memaksakan pembaruan tersebut jika diperlukan dalam kondisi darurat.
> 
> Di bawah panel kontrol, terdapat daftar instrumen utama kita: **CL (Contract Letter)**, **ROS (Rundown of Show)**, **CK (Check List)**, **PNL (Profit & Loss)**, serta berkas client validation **PF** dan **MATRIX**.
> 
> Di panel ini, PM/PO dapat langsung mengubah status instrumen secara inline (*Not Started, In Progress, Done, Need Revision*), mengatur tanggal jatuh tempo, dan mengisi catatan. Jika status diubah ke **Done**, sistem secara otomatis mengunci tanggal selesai (*Completed Date*) hari ini. Jika ada dokumen yang melewati tanggal jatuh tempo, indikator **Overdue** berwarna merah akan menyala untuk memberikan alarm visual bagi tim.
> 
> Keamanan berkas keuangan sensitif seperti **PNL** juga telah kami proteksi di level database. Jika pengguna masuk sebagai peran `Staff` (staf biasa), tautan dokumen PNL akan disembunyikan secara otomatis dengan label *Restricted*, sedangkan peran `Admin`, `Management`, dan `Finance` tetap dapat melihat dan membukanya.
> 
> Terakhir, semua riwayat pemblokiran gerbang kesiapan, perubahan status dengan peringatan, serta penggunaan force update terekam secara otomatis pada tabel **Activity Log** di bagian bawah, memberikan audit trail yang transparan bagi manajemen."

---

## 7. Dashboard Instrument Summary & Review Kualitas Data
*(Presenter kembali ke Dashboard utama)*
> **Presenter**:
> "Sebagai penutup demonstrasi fitur dashboard, kami ingin menunjukkan panel **Instrument Readiness Summary** dan **Review Kualitas Data** yang baru.
> 
> Pada dashboard utama, jajaran direksi dapat melihat rangkuman kesiapan operasional secara agregat untuk seluruh proyek aktif: jumlah proyek yang kehilangan dokumen CL, ROS, CK, atau PNL, jumlah instrumen yang butuh revisi (*Need Revision*), instrumen yang terlambat (*Overdue*), hingga rata-rata persentase kesiapan instrumen (*Average Completion Rate*).
> 
> Selain itu, jika ada proyek berstatus Quotation `Signed & Deal` tetapi belum melengkapi CL atau PNL, atau status Program sudah `Ready/Running` namun ROS belum `Done`, sistem secara cerdas akan langsung memunculkannya sebagai peringatan kualitas data di panel **Review Kualitas Data**."

---

## 8. PM Control Center & Operational Priorities
*(Presenter mengklik item menu 'PM Control Center' di sidebar)*
> **Presenter**:
> "Sekarang, mari kita lihat salah satu fitur terpenting bagi tim operasional Anda: **PM Control Center** (Pusat Kontrol Manajer Program). Berbeda dengan dashboard eksekutif sebelumnya yang berfokus pada KPI bisnis tingkat tinggi, PM Control Center dirancang khusus untuk memandu PM dan PO dalam memilah pekerjaan operasional harian.
> 
> Di bagian atas, kami menyediakan rangkuman operasional cepat: jumlah event hari ini, event mendatang dalam 7 hari, instrumen checklist yang terlewat atau butuh revisi, serta rata-rata tingkat kesiapan seluruh event aktif secara real-time.
> 
> Di bawahnya, sistem menyajikan panel **Priority Actions List** (Daftar Aksi Prioritas). Algoritma sistem secara cerdas menyaring dan mengelompokkan proyek-proyek bermasalah menjadi empat kategori urgensi: Critical, High, Medium, dan Low. Misalnya, jika ada event yang diadakan hari ini tetapi skor kesiapannya di bawah 80%, sistem akan langsung menaikkannya sebagai status **Critical** dengan rekomendasi tindakan nyata agar PM segera menindaklanjuti kelalaian berkas.
> 
> Kami juga menyediakan tab menu interaktif untuk melihat **Jadwal Event & Kesiapan**, **Checklist & Revisi**, serta **Beban Kerja PM**. Di dalam tab instrumen checklist, tim operasional dapat memantau dengan tepat berapa hari keterlambatan (*Days Overdue*) suatu berkas kontrak (CL) atau Rundown (ROS) yang jatuh tempo, lengkap dengan penanggung jawab PM-nya.
> 
> Tentu saja, PM dapat langsung menyaring data berdasarkan nama mereka sendiri atau periode waktu tertentu, dan mengklik tautan proyek untuk langsung membuka halaman detail proyek."

---

## 9. PO Control Center & Commercial follow-up
*(Presenter mengklik item menu 'PO Control Center' di sidebar)*
> **Presenter**:
> "Selanjutnya, mari kita masuk ke fitur terbaru yang kami bangun di Sprint 10: **PO Control Center** (Pusat Kontrol Pemilik Program). Jika PM Control Center berfokus pada kesiapan teknis operasional di lapangan, PO Control Center dirancang khusus untuk Program Owner memantau kesehatan aspek komersial dan keuangan proyek.
> 
> Di bagian atas, Bapak dan Ibu disuguhkan dengan KPI komersial tingkat tinggi: total proyek di bawah kepemilikan PO, rasio deal-to-cancel, potential vs confirmed revenue, outstanding tagihan klien, serta jumlah aksi follow-up yang mendesak.
> 
> Kami membagi workspace ini ke dalam beberapa tab:
> 1. **Prioritas Follow-up**: Menampilkan daftar aksi komersial mendesak secara otomatis, mulai dari status *Critical* (seperti proyek deal tetapi budget kosong, proyek batal tanpa alasan, atau piutang yang telah jatuh tempo), status *High* (penawaran yang belum deal padahal H-14 event), hingga status *Medium* dan *Low*. Ini membantu PO mengetahui klien mana yang harus dikontak pagi ini.
>    *(Catatan: Follow-up priority adalah indikator bantu untuk membantu PO melihat project yang membutuhkan perhatian. Prioritas ini bukan keputusan final otomatis dan tetap perlu divalidasi oleh tim One Spirit berdasarkan konteks operasional dan komersial)*
> 2. **Daftar Proyek PO**: Master data proyek dengan ringkasan status quotation, program, dan payment.
> 3. **Kinerja Komersial**: Grafik dan tabel detail mengenai struktur quotation, statistik nilai proyek, performa deal rate per PO, serta kontribusi lead source (melacak hotel atau partner mana yang menyumbang konversi revenue terbesar).
> 4. **Risiko Komersial**: Panel audit otomatis yang mengelompokkan proyek berdasarkan warning finansial, seperti proyek Signed & Deal Rp 0 atau piutang overdue.
> 
> Dengan PO Control Center, manajemen dapat meminimalisir piutang macet dan mempercepat konversi pipeline penawaran menjadi deal komersial secara efektif."

---

## 10. Cetak Laporan & Penutup
*(Presenter menekan tombol Print / Save Report)*
> **Presenter**:
> "Terakhir, laporan dashboard ini dapat langsung dicetak atau disimpan ke file PDF. Dengan menekan tombol **Print / Save Report**, sistem otomatis memicu cetak browser dengan tata letak khusus yang menghilangkan navigasi menu dan latar belakang gelap, menghasilkan dokumen cetak putih bersih yang rapi dan profesional.
> 
> Demikian demonstrasi dari sistem web One Spirit dengan instrumen proyek terintegrasi. Kami ingin menyelaraskan beberapa pertanyaan validasi dengan Bapak dan Ibu untuk memastikan alur status keuangan, penugasan PO/PM, dan detail instrumen operasional ini sudah tepat sebelum kita melangkah ke fase implementasi selanjutnya. Terima kasih."
