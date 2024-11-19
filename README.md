# EventPass Backend API

EventPass adalah platform untuk mengelola dan menghadiri berbagai acara. Proyek ini menyediakan API backend yang dibangun dengan framework FASTAPI. Panduan ini menjelaskan cara menyiapkan lingkungan pengembangan, menjalankan server, dan melakukan migrasi database.

# Prasyarat
Sebelum memulai, pastikan Anda telah menginstal:
- Python (versi 3.10 atau lebih baru)
- pip (Python package installer)

# Instalasi

1. Clone repositori
```
git clone https://github.com/mazipan/eventpass-backend.git
cd eventpass-backend
```

2. Buat virtual environment
Di dalam direktori proyek, jalankan perintah berikut untuk membuat dan mengaktifkan virtual environment:
```
python -m venv venv
source venv/bin/activate # untuk linux
venv\Scripts\activate # untuk windows
```

3. Instal dependensi
Instal semua dependensi yang tercantum di requirements.txt:
```
pip install -r requirements.txt
```

# Konfigurasi

Buat file ```.env``` di root direktori proyek untuk menyimpan konfigurasi lingkungan. Contoh isi file ```.env```:
```
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=your_database
UPLOAD_DIR=uploads
```

# Menjalankan Project
1. Jalankan server
Gunakan perintah berikut untuk menjalankan server development:
```
uvicorn src.main:app --reload
```

2. Cek endpoint API
Buka browser atau gunakan aplikasi seperti Postman untuk memeriksa endpoint API pada ```http://127.0.0.1:8000/docs``` untuk dokumentasi interaktif.

# Migrasi Database

1. Inisialisasi database dengan Alembic (jangan di eksekusi apabila migration sudah ada dari upstream git)
```
alembic init migrations
```

2. Buat migrasi baru
```
alembic revision --autogenerate -m "Initial migration"
```

3. Terapkan migrasi
```
alembic upgrade head
```


# For NIX Users
1. Untuk pengguna NIX, gunakan perintah berikut untuk mengggunakan nix-shell:
    ```
    nix-shell .
    ```
2. Aktifkan virtual environment dengan perintah berikut:
    ```
    source venv/bin/activate
    ```
3. Install dependensi dengan perintah berikut:
    ```
    pip install -r requirements.txt
    ```
3. Jalankan server dengan perintah berikut:
    - apabila menginstall fastapi[standard] atau fastapi[full], gunakan perintah berikut:
        ```
        fastapi dev src/main.py --reload --port 8000
        ```
    - apabila belum maka gunakan perintah berikut:
        ```
        uvicorn src.main:app --reload --port 8000
        ```
