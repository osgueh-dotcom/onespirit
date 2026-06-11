# Public Demo Safety Checklist

Dokumen ini berisi panduan keamanan operasional ketika aplikasi OneSpirit Workflow System dipublikasikan melalui public tunnel untuk sesi demo sementara.

---

## Peringatan Penting

> [!WARNING]
> Jangan mengekspos informasi berikut ke publik:
> - **PostgreSQL**: jangan mempublikasikan port database `5432` atau `5433`.
> - **DB Password**: jangan menyimpan `DB_PASSWORD` di frontend, GitHub Actions log, atau dokumen publik.
> - **JWT Secret**: `JWT_SECRET` hanya boleh berada di backend environment.
> - **Data asli klien**: gunakan data dummy untuk presentasi publik.

---

## Checklist Sebelum Demo

- [ ] Backend FastAPI berjalan normal di port `8000`.
- [ ] Database lokal aktif dan hanya dapat diakses oleh backend.
- [ ] Temporary tunnel hanya membuka backend port `8000`, bukan database.
- [ ] Frontend GitHub Pages aktif di [https://osgueh-dotcom.github.io/onespirit/](https://osgueh-dotcom.github.io/onespirit/).
- [ ] Login demo berhasil menggunakan akun demo yang sudah disiapkan.
- [ ] Password demo tidak ditulis di dokumen publik dan diberikan langsung saat sesi.
- [ ] Data dummy sudah bersih dari informasi sensitif PT One Spirit Asia atau klien asli.
- [ ] `BACKEND_CORS_ORIGINS` menyertakan `https://osgueh-dotcom.github.io`.
- [ ] `JWT_SECRET`, `ADMIN_PASSWORD`, dan `DEMO_USER_PASSWORD` berbeda dari default jika environment bukan development/demo lokal.
- [ ] User Management tidak terlihat dan tidak dapat diakses oleh role non-admin.

---

## Checklist Sesudah Demo

- [ ] Matikan tunnel atau ubah visibility VS Code port menjadi private.
- [ ] Hentikan backend/Docker Compose jika tidak diperlukan.
- [ ] Catat feedback klien menggunakan [client-feedback-form.md](client-feedback-form.md).
- [ ] Ganti `DEMO_USER_PASSWORD` jika link tunnel atau credential demo sempat tersebar terlalu luas.
- [ ] Nonaktifkan user demo jika akun tidak diperlukan setelah sesi.
- [ ] Jangan commit file `.env`, database lokal, file upload, atau data demo sensitif.
