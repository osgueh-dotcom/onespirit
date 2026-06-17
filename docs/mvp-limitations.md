# MVP Limitations - OneSpirit Workflow System

Status: Sprint 19 Backend Test Stack Cleanup

OneSpirit Workflow sudah demo-ready, tetapi belum production-ready.

## Current Limitations

1. **Security**
   - Production secret storage belum memakai managed secret service.
   - MFA, login rate limiting, dan account lockout belum tersedia.
   - `/docs` dan OpenAPI belum dibatasi untuk production.

2. **Authorization**
   - Role-aware UI visibility baseline sudah tersedia.
   - Role Admin, PO, dan PM belum formal di backend.
   - Project ownership belum menjadi authorization gate.
   - Import dan mutation instrumen PNL masih memakai permission broad.

3. **Deployment**
   - GitHub Pages dan backend tunnel adalah demo architecture.
   - Docker Compose memakai dev server dan database host port; image rebuild diperlukan setelah perubahan source.
   - Production reverse proxy, SSL, restart policy, dan monitoring belum final.

4. **Data Recovery**
   - Belum ada automated backup, off-site retention, atau encryption.
   - Restore drill belum dicatat.

5. **External Integration**
   - Belum ada SMTP/notifikasi otomatis.
   - PDF masih mengandalkan browser print; server-side PDF belum tersedia.

6. **Vendor Data**
   - Vendor partner masih berupa field tekstual pada EventSource.
   - Normalisasi vendor ditunda agar Sprint 14 tidak menjadi rewrite data model.

7. **Quality Debt**
   - Backend test stack sudah bersih dengan `36 passed` tanpa warning.
   - Frontend ESLint baseline sudah bersih dengan `0 errors` dan `0 warnings`.
   - Component test dan coverage threshold belum tersedia.

## Production Risk

Jangan menggunakan MVP ini langsung sebagai production system sebelum:

- secrets dirotasi;
- HTTPS dan reverse proxy siap;
- database tidak dipublish;
- role/ownership gate diperkuat;
- backup dan restore drill berhasil;
- monitoring dan rollback diuji.

## Sprint 20 Recommendation

`Sprint 20 - Authorization & Production Runtime Hardening`

1. Formalisasi Admin, PO, dan PM.
2. Tambahkan permission khusus imports dan PNL.
3. Terapkan project ownership gate.
4. Siapkan production Dockerfiles/Compose override.
5. Jalankan backup/restore drill.
6. Tambahkan monitoring dan rate limiting.
7. Tambahkan component test dan coverage threshold bertahap.
