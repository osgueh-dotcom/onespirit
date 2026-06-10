# Public Demo Architecture - OneSpirit Workflow System

Dokumen ini menjelaskan arsitektur deployment hibrida yang dirancang khusus untuk demo klien, validasi MVP, dan sesi presentasi interaktif tanpa menggunakan infrastruktur cloud produksi yang mahal.

---

## 1. Diagram Arsitektur

```mermaid
graph TD
    subgraph Public Internet
        Client[Client Browser]
        GH_Pages[GitHub Pages Frontend]
        Tunnel[Backend Tunnel (VS Code / ngrok)]
    end

    subgraph Local PC / Docker Environment
        FastAPI[FastAPI Backend]
        PostgreSQL[(PostgreSQL Local Docker)]
    end

    Client -->|1. Akses UI via HTTPS| GH_Pages
    Client -->|2. Request API via HTTPS| Tunnel
    Tunnel -->|3. Forward ke Port 8000| FastAPI
    FastAPI -->|4. Query (Internal Network)| PostgreSQL
```

---

## 2. Deskripsi Komponen Arsitektur

Sistem demo ini memisahkan komponen berdasarkan aksesibilitas dan tingkat keamanannya:

### A. Frontend (Public)
* **Hosting**: GitHub Pages ([https://osgueh-dotcom.github.io/onespirit/](https://osgueh-dotcom.github.io/onespirit/)).
* **Aksesibilitas**: Publik secara permanen.
* **Perilaku**: Memuat aset statis HTML, CSS, dan Javascript ke dalam browser klien. Pengalihan halaman ditangani oleh routing hash klien (`#/`).

### B. Backend (Temporary Public)
* **Hosting**: Komputer lokal pengembang/demonstrator.
* **Aksesibilitas**: Publik hanya selama sesi demo melalui port forwarding / temporary tunnel secure (HTTPS).
* **Perilaku**: Menerima request API dari browser klien, memproses otentikasi JWT, validasi bisnis, dan manipulasi data.

### C. Database (Strictly Private)
* **Hosting**: Container PostgreSQL di dalam network internal Docker lokal.
* **Aksesibilitas**: **Sama sekali tidak dapat diakses dari publik**.
* **Perilaku**: Hanya terhubung secara internal dengan kontainer backend FastAPI. Tidak ada port database (`5432`/`5433`) yang diekspos ke publik luar melalui tunnel.

---

## 3. Catatan Keamanan (Security Notes)

1. **Isolation**: Database PostgreSQL tetap berada di belakang firewall PC lokal dan hanya dapat diakses melalui kontainer backend.
2. **Short-Lived Tunnel**: Tunnel backend (ngrok atau VS Code Port Forwarding) hanya boleh diaktifkan selama sesi demo dan harus dimatikan setelah sesi selesai.
3. **No Frontend Secrets**: Tidak ada rahasia produksi seperti `JWT_SECRET`, database password, atau credential backend yang di-hardcode ke dalam bundel JavaScript frontend yang di-deploy ke GitHub Pages.
4. **Data Dummy**: Database demo harus diisi 100% dengan data tiruan operasional. Informasi komersial asli PT One Spirit Asia tidak boleh dimasukkan ke dalam database ini.

---

## 4. Batasan Sistem (Known Limitations)

1. **Ketergantungan Aktivitas PC Lokal**: Jika PC lokal mati atau koneksi internet terputus, backend API tidak akan merespons, menyebabkan frontend GitHub Pages menampilkan error loading.
2. **Perubahan URL Tunnel**: Setiap kali tunnel diaktifkan kembali, URL base API (`VITE_API_BASE_URL`) kemungkinan akan berubah. Klien harus memperbarui nilai GitHub Repository Secret dan melakukan build ulang untuk menerapkan perubahan tersebut.
3. **Kecepatan Jaringan**: Karena request API melewati jalur tunnel publik ke komputer lokal, latency request mungkin sedikit lebih tinggi dibandingkan deployment cloud production langsung.
