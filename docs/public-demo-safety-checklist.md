# Public Demo Safety Checklist

Dokumen ini berisi panduan kepatuhan keamanan operasional ketika mempublikasikan aplikasi OneSpirit Workflow System menggunakan public tunnel untuk sesi demo/presentasi klien sementara.

---

## ⚠️ Peringatan Penting (Jangan Expose!)

> [!WARNING]
> **DILARANG KERAS mengekspos informasi berikut ke publik:**
> - **PostgreSQL**: Jangan pernah mempublikasikan port database (`5432` / `5433`). Database harus tetap privat di jaringan internal.
> - **DB Password**: Jangan menyimpan password database (`DB_PASSWORD`) dalam konfigurasi frontend atau log publik.
> - **JWT Secret**: `JWT_SECRET` harus dijaga kerahasiaannya di backend saja dan tidak boleh dimasukkan ke dalam kode frontend.

---

## 📋 Checklist Kesiapan Demo

### Sebelum Demo Mulai

- [ ] **Backend running**: Pastikan FastAPI backend berjalan normal di port `8000`.
- [ ] **Database running**: Pastikan database PostgreSQL (atau SQLite) lokal aktif dan dapat diakses backend.
- [ ] **Tunnel aktif**: Jalankan temporary tunnel (ngrok / VS Code Port Forwarding) untuk mempublikasikan backend port `8000`.
- [ ] **Frontend GitHub Pages aktif**: Pastikan halaman [https://osgueh-dotcom.github.io/onespirit/](https://osgueh-dotcom.github.io/onespirit/) dapat diakses.
- [ ] **Login demo berhasil**: Uji login menggunakan akun demo `demo@onespirit.asia` di browser mode Incognito.
- [ ] **Data dummy siap**: Verifikasi database terisi data dummy operasional yang bersih tanpa informasi sensitif.
- [ ] **Database tidak public**: Pastikan port database PostgreSQL tidak diekspos melalui tunnel luar.
- [ ] **Verifikasi CORS**: Pastikan origin `https://osgueh-dotcom.github.io` sudah terdaftar di setting `CORS_ORIGINS` backend.

### Sesudah Demo Selesai

- [ ] **Tunnel dimatikan**: Hentikan proses tunnel (tekan `Ctrl + C` pada ngrok / ubah port VS Code visibility menjadi private).
- [ ] **Backend dihentikan jika perlu**: Hentikan service backend uvicorn / Docker compose jika tidak diperlukan lagi.
- [ ] **Feedback client dicatat**: Gunakan [client-feedback-form.md](file:///e:/GVsys Project/One Spirit/docs/client-feedback-form.md) untuk mencatat masukan dari klien.
- [ ] **Password demo diganti jika perlu**: Ganti `DEMO_PASSWORD` di file `.env` jika link tunnel sempat terekspos secara tidak terkontrol.
