# AGRI-DATA HARVESTER

**Agri-Data Harvester Standard 1100** adalah modul *data ingestion & synchronization engine* berkinerja tinggi yang dirancang untuk menarik, membersihkan, dan menstandarisasi data **Poktan (Kelompok Tani)** dari portal SIMLUH Kementan secara otomatis.

Sistem ini didesain sebagai pipeline data yang stabil, *repeatable*, dan *scalable* untuk mengumpulkan data ke seluruh provinsi di Indonesia dengan mekanisme *production hardened* yang amat kokoh. Output berwujud CSV yang telah terdeduplikasi dan siap untuk diintegrasikan (ingest) langsung ke dalam ekosistem *backend* aplikasi generasi selanjutnya seperti Jiwakaya, WorkISM, maupun AI Data Infrastructure.

## 🚀 Fitur Utama

- **Autonomous Discovery**: Scraping bertingkat otomatis membaca dan menelusuri dropdown wilayah mulai dari list Provinsi → Kabupaten → Kecamatan secara utuh dengan mapping sinkronisasi standar UUID Gov (Ex: ID `35` menjadi `3500`).
- **Resiliency & State Management System**: Sistem sanggup menyimpan rekam jejak progress hingga unit kecamatan terkecil melalui `state/progress.json` sehingga proses ekstraksi bisa dilanjutkan (`--resume`) kapanpun tanpa memulai proses crawling dari awal apabila skrip mengalami error/terhenti.
- **Production Hardening Mechanism**: 
  - File *logging matrix* mendetail melalui `logs/harvester.log`.
  - Memory guard dengan proteksi *garbage collection* agresif untuk konsumsi memori `< 500MB`.
  - Filter empty DataFrame & rotasi User-Agent.
  - Timeout proteksi komplit: `(connect=10s, read=30s)` untuk *hanging server prevention*.
  - Menangkap `KeyboardInterrupt` / Terminasi Spontan (`Ctrl+C`) dengan penutupan log yang bersih tanpa *corrupt data*.
- **Data Integrity & Hash-Deduplication**: Pipeline dibekali hashing algoritma per-baris menggunakan standar `MD5(desa + id_poktan + nama_poktan)` yang menjamin tidak akan ada data duplikat (zero duplication). Junk row otomatis difilter habis (seperti header berulang & row kosong).
- **Telegram Monitoring**: Memberikan integrasi alert ke bot Telegram setiap batch provinsi, target kabupaten selesai, atau mendeteksi *HTTP Critical Blocking*.

## 🛠️ Prasyarat (Requirements)

Pastikan lingkungan eksekusi memiliki:
- **Python** versi `≥ 3.10`
- Memori Server / VM: Minimum `512MB`
- Package external requirement, instal menggunakan:
```bash
pip install -r requirements.txt
```

## ⚙️ Konfigurasi (`config.py`)

Atur variabel environment bot Telegram untuk mengaktifkan reporting otomatis:
```python
TELEGRAM_ENABLED = True
TELEGRAM_BOT_TOKEN = "YOUR_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
```
Konfigurasi jeda (delay) juga bisa disesuaikan apabila server sedang mengalami latensi (*throttle*).

## 🏃 Cara Menggunakan

Eksekusi engine secara utama ditangani melalui sistem `main.py` CLI interface.

**1. Scraping 1 Provinsi (Spesifik):**  
Masukkan ID standar Gov (Misal Jawa Timur dengan ID `3500`):
```bash
python main.py --province 3500
```

**2. Scraping Seluruh Wilayah Nasional.**  
(*Direkomendasikan dijalankan bertahap pada VM atau server pada waktu idle / malam hari*)
```bash
python main.py --all
```

**3. Melanjutkan Proses Scraping yang Terhenti (Resume):**  
Jika script crash (seperti karena HTTP 403 / 500), cukup langsung lanjutkan dengan argumen:
```bash
python main.py --resume
```
> Script otomatis meneruskan sisa ekstraksi tepat dari nama *Kecamatan* terakhir yang mengalami jeda atau *crash exception*.

## 📂 Struktur Data Output

Dataset output bersih (CSV) akan tersimpan di dalam folder `data/` dengan pengkategorian khusus hasil *auto-slugify*.

Contoh file:
```
data/
  ├── data_prov_jawatimur.csv
  └── data_prov_aceh.csv
```

**Kolom Data Terekstraksi (Scraped):**
`id_prov_gov`, `nama_prov`, `nama_kab`, `nama_kec`, `desa`, `id_poktan`, `nama_poktan`, `ketua`, `penyuluh`, `nik`, `scraped_at`, dan `row_hash`.

---
*Created per AGRI-DATA Architecture Blueprint 1100*
