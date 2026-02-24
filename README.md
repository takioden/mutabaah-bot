# mutabaah-bot
# 🌙 Mutabaah Habit & Hadits Discord Bot

Bot Discord berbasis Python untuk membantu pengelolaan ibadah harian (Mutabaah Yaumiyah) secara otomatis dengan fitur checklist habit, leaderboard mingguan, dan hadits harian.

## 🚀 Fitur Utama
*   **Checklist Habit Harian**: Interaksi menggunakan Discord Buttons yang aman (Ephemeral) dan memiliki deadline pukul 23:59 WIB.
*   **Leaderboard Mingguan**: Klasemen otomatis berdasarkan persentase kepatuhan, reset setiap hari Ahad (Minggu).
*   **One Day One Hadits**: Pengiriman hadits acak (pendek < 1000 char) setiap hari melalui MyQuran API.
*   **Admin Panel**: Perintah khusus admin untuk menambah, menghapus, atau menonaktifkan habit.
*   **Database Asinkron**: Menggunakan `aiosqlite` agar bot tetap responsif saat memproses data.

## 🛠️ Persyaratan Sistem
*   Python 3.9 atau lebih tinggi
*   Library: `discord.py`, `aiosqlite`, `pytz`, `aiohttp`, `tzdata` (untuk Windows)

## 📦 Instalasi

1.  **Clone Repositori:**
    ```bash
    git clone https://github.com
    cd mutabaah-dcbot
    ```

2.  **Buat Virtual Environment:**
    ```bash
    python -m venv bot_env
    source bot_env/bin/activate  # Linux/macOS
    .\bot_env\Scripts\activate     # Windows
    ```

3.  **Instal Dependensi:**
    ```bash
    pip install discord.py aiosqlite aiohttp pytz tzdata
    ```

4.  **Konfigurasi:**
    Buat file `config.py` dan masukkan token bot kamu:
    ```python
    TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
    ```

## 🗄️ Struktur Database
Bot menggunakan SQLite yang disimpan di `data/mutabaah.db`. Tabel akan otomatis dibuat saat pertama kali dijalankan:
*   `users`: Menyimpan data Discord ID dan username.
*   `habits`: Daftar habit yang dikelola admin.
*   `daily_logs`: Catatan checklist harian user.


## ⏰ Scheduler (Tugas Otomatis)
*   **Daily Checklist**: Dikirim setiap pukul 19:30 WIB.
*   **One Day One Hadits**: Dikirim setiap pukul 05:00 WIB.
*   **Weekly Leaderboard**: Dikirim setiap hari Ahad pukul 21:00 WIB.

## 📄 Lisensi
Distribusi di bawah lisensi MIT. Lihat `LICENSE` untuk informasi lebih lanjut.
