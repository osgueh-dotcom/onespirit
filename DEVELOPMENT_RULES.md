# DEVELOPMENT RULES

Dokumen ini berisi aturan wajib untuk semua proses pengembangan project, baik dilakukan oleh manusia maupun AI agent seperti Codex, Gemini, Continue Dev, Ollama lokal, atau agent lain di Antigravity IDE / VS Code.

## 1. Peran Utama

### Product Owner

Product owner adalah pemilik sistem, pengambil keputusan, dan penguji utama.

Tanggung jawab product owner:

- Menjelaskan kebutuhan bisnis.
- Menentukan prioritas fitur.
- Menguji hasil pengembangan.
- Menyetujui perubahan besar.
- Menjaga agar sistem tetap sesuai kebutuhan operasional.

### AI Agent

AI agent berperan sebagai technical assistant, bukan pengambil keputusan final.

Tanggung jawab AI agent:

- Membaca konteks project sebelum coding.
- Melakukan audit sebelum implementasi.
- Memberi rencana kerja yang jelas.
- Mengubah kode secara bertahap dan aman.
- Menjelaskan setiap perubahan.
- Menjalankan test/build/dev run setelah pengembangan.
- Membantu dokumentasi dan commit.

## 2. Prinsip Utama Pengembangan

Setiap pengembangan harus mengikuti prinsip berikut:

1. Audit sebelum coding.
2. Sprint kecil dan terukur.
3. Jangan rewrite total tanpa alasan kuat.
4. Jangan hapus fitur lama tanpa konfirmasi.
5. Jangan ubah schema database secara destruktif tanpa rencana migrasi.
6. Jangan menambahkan dependency besar tanpa alasan teknis.
7. Prioritaskan maintainability, security, dan readability.
8. Setiap perubahan harus bisa dijelaskan.
9. Setiap perubahan harus bisa dites.
10. Setiap sprint harus diakhiri dengan dokumentasi dan commit.

## 3. Alur Kerja Wajib

Gunakan alur berikut untuk setiap sprint:

```text
1. Baca PROJECT_CONTEXT.md
2. Baca SPRINT_LOG.md
3. Baca CHANGELOG.md
4. Audit kondisi project saat ini
5. Identifikasi masalah utama
6. Buat rencana sprint kecil
7. Implementasikan perubahan
8. Jalankan test/build/dev run
9. Perbaiki error yang muncul
10. Update dokumentasi
11. Buat commit git
12. Laporkan hasil akhir
```

## 4. Aturan Untuk AI Agent Sebelum Coding

AI agent wajib melakukan ini sebelum coding:

- Memahami struktur folder.
- Mengecek package/dependency.
- Mengecek konfigurasi database.
- Mengecek command untuk menjalankan project.
- Mengecek apakah ada dokumentasi sebelumnya.
- Mengecek risiko terhadap fitur yang sudah berjalan.

AI agent tidak boleh langsung mengubah kode hanya berdasarkan asumsi.

## 5. Batasan Perubahan

AI agent tidak boleh melakukan hal berikut tanpa instruksi eksplisit:

- Rewrite total project.
- Menghapus modul lama.
- Menghapus database atau migration.
- Mengubah struktur utama secara besar-besaran.
- Mengubah autentikasi/security flow.
- Menghapus file konfigurasi.
- Menghapus dokumentasi project.
- Menambahkan dependency besar.
- Mengubah environment production.
- Melakukan push ke remote repository jika build/test gagal.

## 6. Aturan Database

Perubahan database harus hati-hati.

Wajib dilakukan:

- Jelaskan alasan perubahan schema.
- Buat migration jika tech stack mendukung.
- Hindari perubahan destruktif.
- Jangan hapus kolom/tabel tanpa backup atau konfirmasi.
- Jangan gunakan data production untuk testing sembarangan.
- Jangan commit file database sensitif.

Perubahan berisiko tinggi:

- Drop table.
- Rename table.
- Delete column.
- Change column type.
- Reset migration.
- Seed ulang database production.

Semua perubahan di atas wajib dikonfirmasi terlebih dahulu.

## 7. Aturan Security

Dilarang commit:

- `.env`
- API key
- password
- token
- private key
- credential database
- file backup database berisi data asli
- data pribadi client/user

Wajib diperhatikan:

- Validasi input user.
- Proteksi route yang membutuhkan login.
- Jangan tampilkan error sensitif ke user.
- Jangan simpan password dalam bentuk plain text.
- Gunakan environment variable untuk konfigurasi sensitif.

## 8. Aturan Git

Setiap sprint harus menghasilkan commit yang jelas.

Format commit disarankan:

```text
type(scope): ringkasan perubahan
```

Contoh:

```text
feat(invoice): add invoice status filter
fix(auth): resolve login redirect issue
docs(project): update sprint log and context
refactor(ui): simplify dashboard layout
chore(deps): update minor dependencies
```

Jenis commit:

- `feat` untuk fitur baru.
- `fix` untuk bug fix.
- `docs` untuk dokumentasi.
- `refactor` untuk perubahan struktur tanpa mengubah behavior.
- `test` untuk penambahan/perbaikan test.
- `chore` untuk maintenance.
- `security` untuk perbaikan keamanan.

## 9. Aturan Branch

Jika project sudah menggunakan branch, gunakan pola:

```text
main
develop
sprint/{{SPRINT_NAME}}
feature/{{FEATURE_NAME}}
fix/{{BUG_NAME}}
```

Contoh:

```text
sprint/10-1-dashboard-stabilization
feature/invoice-export
fix/login-session-timeout
```

## 10. Aturan Testing

Setelah implementasi, wajib jalankan command yang tersedia:

```bash
{{TEST_COMMAND}}
{{BUILD_COMMAND}}
{{DEV_COMMAND}}
```

Jika tidak ada test otomatis, minimal lakukan:

- Jalankan aplikasi mode dev.
- Buka halaman utama.
- Cek error terminal.
- Cek error browser console.
- Cek fitur yang baru diubah.
- Cek fitur lama yang terkait.

## 11. Aturan Dokumentasi

Setelah perubahan selesai, update dokumen yang relevan:

- `README.md` jika cara install/run berubah.
- `PROJECT_CONTEXT.md` jika workflow/istilah/batasan berubah.
- `SPRINT_LOG.md` untuk catatan sprint.
- `CHANGELOG.md` untuk perubahan versi.
- Dokumentasi teknis tambahan jika diperlukan.

## 12. Format Laporan Akhir AI Agent

Setelah selesai, AI agent wajib melaporkan:

```text
Ringkasan:
- ...

File yang diubah:
- ...

Perubahan utama:
- ...

Cara test:
- ...

Hasil test:
- ...

Risiko tersisa:
- ...

Commit yang dibuat:
- ...

Saran sprint berikutnya:
- ...
```

## 13. Prompt Standar Untuk AI Agent

Gunakan prompt ini saat mulai sprint baru:

```text
Anda adalah senior software engineer, system architect, dan AI development assistant.

Baca terlebih dahulu:
1. PROJECT_CONTEXT.md
2. DEVELOPMENT_RULES.md
3. SPRINT_LOG.md
4. CHANGELOG.md
5. README.md

Saya bukan programmer utama. Saya adalah product owner dan operator bisnis yang menggunakan AI agent untuk membangun sistem secara bertahap.

Tugas Anda:
1. Audit project terlebih dahulu.
2. Jangan langsung coding sebelum memahami struktur.
3. Identifikasi risiko teknis, bug, duplikasi, struktur folder, database, dependency, dan dokumentasi.
4. Buat rencana sprint kecil.
5. Implementasikan perubahan secara bertahap.
6. Jalankan test/build/dev run.
7. Perbaiki error yang muncul.
8. Update dokumentasi.
9. Buat commit git yang jelas.
10. Jika saya perintahkan, lakukan push setelah test minimal lolos.

Batasan:
- Jangan rewrite total tanpa alasan kuat.
- Jangan hapus fitur lama tanpa konfirmasi.
- Jangan ubah database secara destruktif tanpa rencana.
- Jangan commit credential, .env, token, atau data sensitif.
- Prioritaskan maintainability, security, dan struktur jangka panjang.

Output akhir wajib berisi:
1. Ringkasan hasil.
2. File yang diubah.
3. Alasan perubahan.
4. Cara menjalankan/test.
5. Risiko yang masih tersisa.
6. Commit message yang digunakan.
7. Saran sprint berikutnya.
```
