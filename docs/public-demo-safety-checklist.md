# Public Demo Safety Checklist

Dokumen ini panduan kepatuhan keamanan operasional ketika mempublikasikan aplikasi OneSpirit Workflow System menggunakan public tunnel (seperti ngrok, cloudflared, localtunnel) untuk demo/presentasi klien sementara.

---

## ⚠️ Prinsip Utama Keamanan Demo

1. **Hanya Frontend & Backend yang Publik**: Hanya port frontend (`5173` / `80`) dan backend (`8000` / `443`) yang boleh diekspos keluar melalui tunnel.
2. **Database Harus Privat**: Jangan pernah mempublikasikan port database PostgreSQL (`5432` / `5433`). Database hanya boleh diakses secara internal oleh container backend.
3. **Data Dummy 100%**: Dilarang keras menggunakan data klien asli, dokumen CL/kontrak asli, nomor rekening asli, atau nama orang asli dalam database demo.
4. **Gunakan Akun Demo**: Tunjukkan demo menggunakan akun `demo@onespirit.asia`, bukan akun super admin pribadi.
5. **Ganti Password Setelah Demo**: Jika tunnel dibagikan secara luas, segera reset password akun demo setelah sesi selesai.
6. **Sembunyikan Swagger /docs**: Tidak perlu membagikan link Swagger backend `/docs` atau `/redoc` kepada perwakilan klien.
7. **Matikan Tunnel Segera**: Stop proses port forwarding segera setelah sesi Q&A demo berakhir. Jangan tinggalkan tunnel berjalan semalaman.

---

## 📋 Checklist Demo Kesiapan Keamanan

### Sebelum Demo Mulai

- [ ] **Layanan Internal Berjalan**: Pastikan PostgreSQL, Backend, dan Frontend berjalan normal di Docker Compose.
- [ ] **Data Dummy Siap**: Verifikasi database terisi data dummy yang bersih tanpa informasi sensitif.
- [ ] **Konfigurasi Akun Demo**: Pastikan email `demo@onespirit.asia` bisa masuk dengan password yang sudah dikonfigurasi di `.env` (Default: `OneSpiritDemo2026!`).
- [ ] **Aktifkan Tunnel**: Jalankan tunnel ke port frontend (`5173`) dan backend (`8000`).
- [ ] **Verifikasi CORS**: Pastikan domain tunnel frontend diizinkan masuk ke CORS setting backend jika diperlukan.
- [ ] **Test Akses Terisolasi**: Akses link tunnel dari mode browser Samaran (Incognito) untuk memverifikasi halaman login berjalan mulus.
- [ ] **Siapkan Dokumen PDF**: Siapkan Panduan Demo Client PDF di desktop untuk dibagikan ke klien.

### Selama Demo Berjalan

- [ ] **Bagi Hanya Link Frontend**: Hanya berikan link tunnel frontend kepada klien/audiens.
- [ ] **Presentasikan Narasi Terstruktur**: Ikuti alur demo 15-25 menit yang terdokumentasi di [client-demo-rehearsal.md](file:///e:/GVsys Project/One Spirit/docs/client-demo-rehearsal.md).
- [ ] **Hindari Ekspos Konsol**: Jangan memperlihatkan terminal server atau window Docker desktop selama screen-sharing.
- [ ] **Catat Feedback**: Gunakan [client-feedback-form.md](file:///e:/GVsys Project/One Spirit/docs/client-feedback-form.md) untuk mencatat semua masukan klien langsung.

### Sesudah Demo Selesai

- [ ] **Matikan Tunnel**: Tekan `Ctrl + C` pada semua proses terminal tunnel (ngrok / cloudflared).
- [ ] **Turunkan Docker Compose**: Jalankan `docker compose down` jika server demo tidak digunakan lagi untuk menghemat resource dan menutup port lokal.
- [ ] **Reset Password Demo (Opsional)**: Ubah nilai `DEMO_PASSWORD` di file `.env` jika link demo sempat terekspos ke publik tidak dikenal.
- [ ] **Arsipkan Catatan Masukan**: Pindahkan catatan feedback klien ke repositori internal untuk bahan evaluasi sprint berikutnya.
