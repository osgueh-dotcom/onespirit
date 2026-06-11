# Zoom Demo Safety Checklist

Dokumen ini adalah checklist utama untuk presentasi OneSpirit Workflow melalui Zoom Meeting.

## Mode Utama: Zoom Screen Share

- Aplikasi berjalan di PC presenter.
- Client melihat aplikasi melalui screen share Zoom.
- Tidak perlu public link jika client hanya melihat presentasi.
- Gunakan akun demo dan data dummy.
- Tutup tab, notifikasi, terminal, `.env`, database tool, dan aplikasi lain yang tidak perlu terlihat.

## Mode Fallback: VS Code Port Forwarding

Gunakan hanya jika client perlu mencoba aplikasi secara langsung.

- Forward frontend port `5173`.
- Forward backend port `8000` hanya jika arsitektur test memerlukannya.
- Jangan forward PostgreSQL `5432` atau host mapping `5433`.
- Gunakan visibility private atau organisasi jika tersedia.
- Hentikan forwarding segera setelah sesi.

## Sebelum Demo

- [ ] Docker Desktop berjalan.
- [ ] Backend berjalan dan `/health` mengembalikan status OK.
- [ ] Frontend berjalan.
- [ ] Database berjalan dan tidak public.
- [ ] Akun demo dapat login.
- [ ] Password demo bukan default dan diberikan terpisah.
- [ ] Data dummy siap dan tidak berisi data asli client.
- [ ] Dashboard, Projects, Project Detail, PM Control, PO Control, Source & Vendor, Finance, Import, dan Settings dapat dibuka.
- [ ] Browser console tidak memiliki error besar.
- [ ] Panduan demo/PDF presenter siap.
- [ ] Zoom screen share sudah diuji.
- [ ] Desktop notification dan password manager popup dimatikan.
- [ ] User Management hanya terlihat untuk Super Admin/Admin.
- [ ] Dev tunnel smoke test dijalankan jika VS Code Port Forwarding dipakai.

## Jika Memakai Port Forwarding

- [ ] Hanya port frontend/backend yang dibuka.
- [ ] PostgreSQL tidak di-forward.
- [ ] Backend URL tidak disebar jika tidak perlu.
- [ ] Swagger `/docs` tidak dibuka ke client.
- [ ] Link hanya aktif selama sesi demo.
- [ ] Password demo tidak dikirim melalui dokumen publik atau chat yang dapat diteruskan.
- [ ] `scripts/dev-tunnel-smoke.ps1` lulus untuk frontend load, API proxy, login, dan backend health.

## Setelah Demo

- [ ] Stop VS Code port forwarding/tunnel.
- [ ] Matikan Docker Compose jika tidak dipakai.
- [ ] Ganti password demo jika credential atau link sempat public.
- [ ] Nonaktifkan user demo bila tidak lagi diperlukan.
- [ ] Catat feedback client.
- [ ] Buat backlog dari feedback.
- [ ] Periksa log untuk login atau error yang tidak diharapkan.

## Demo Account

- Email: `demo@onespirit.asia`
- Password: diberikan secara terpisah saat sesi demo.

Password demo disediakan melalui `DEMO_USER_PASSWORD` atau env kompatibel `DEMO_PASSWORD`. Password tidak boleh ditulis di source code, README publik, screenshot, atau log.
