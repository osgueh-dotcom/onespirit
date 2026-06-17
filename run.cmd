@echo off
title One Spirit Asia Operations Launcher
color 0B
cls
echo =====================================================================
echo       ___              ____             _      _  _    
echo      / _ \  _ __   ___/ ___|  _ __   (_) _ __(_)| |_  
echo     ^| ^| ^| ^|^| '_ \ / _ \___ \ ^| '_ \  ^| ^|^| '__^| ^|^| __^| 
echo     ^| ^|_^| ^|^| ^| ^| ^|^|  __/___) ^|^| ^|_) ^| ^| ^|^| ^|   ^| ^|^| ^|_  
echo      \___/ ^|_^| ^|_^| \___^|____/ ^| .__/  ^|_^|^|_^|   ^|_^| \__^| 
echo                             ^|_^|                          
echo                    ONE SPIRIT ASIA WORKFLOW SYSTEM
echo =====================================================================
echo.
if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
    set "PATH=C:\Program Files\Docker\Docker\resources\bin;%PATH%"
)
echo.
echo [1/4] Memeriksa status Docker Daemon...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Docker Daemon tidak terdeteksi!
    echo Silakan buka aplikasi Docker Desktop terlebih dahulu, lalu jalankan kembali launcher ini.
    echo Jika tetap gagal di Windows, aktifkan virtualization di BIOS/UEFI dan fitur WSL/Virtual Machine Platform.
    echo.
    pause
    exit /b
)
echo [OK] Docker aktif dan siap digunakan.
echo.
echo [2/4] Sinkronisasi kode: Menarik pengembangan terbaru dari GitHub...
git pull
if %errorlevel% neq 0 (
    echo.
    echo [Peringatan] Gagal menarik data terbaru dari GitHub (mungkin masalah jaringan / offline).
    echo Sistem akan tetap menggunakan kode lokal terakhir Anda.
) else (
    echo [OK] Sinkronisasi GitHub berhasil.
)
echo.
echo [3/4] Menjalankan container sistem (PostgreSQL, Backend, Frontend)...
docker compose up -d --build
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Gagal menjalankan Docker Compose! Periksa log kesalahan di atas.
    echo.
    pause
    exit /b
)
echo [OK] Semua container berjalan secara background (detached mode).
echo.
echo [4/4] Mempersiapkan browser untuk membuka aplikasi...
timeout /t 5 /nobreak >nul
start http://localhost:5173
echo.
echo =====================================================================
echo  SISTEM BERHASIL DILUNCURKAN!
echo.
echo  - Portal Operasional (Frontend) : http://localhost:5173
echo  - Dokumentasi API (FastAPI)     : http://localhost:8000/docs
echo  - Akun Default                  : admin@onespirit.asia
echo  - Password                      : lihat environment lokal atau launcher internal
echo.
echo  PENTING: Jika Anda tidak melihat perubahan visual terbaru pada UI:
echo  Lakukan HARD REFRESH di browser Anda dengan menekan Ctrl + F5!
echo =====================================================================
echo.
echo Tekan tombol apa saja untuk menutup jendela launcher ini...
pause >nul
