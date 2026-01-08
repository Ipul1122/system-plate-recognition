# 🇮🇩 Indonesian License Plate Recognition (ALPR) - Low Spec Optimized

Sistem pengenalan plat nomor kendaraan Indonesia secara *real-time* berbasis Python. Proyek ini dirancang khusus dengan pendekatan **Modular & Efisien** agar dapat berjalan lancar pada perangkat dengan spesifikasi rendah (Low-End PC/Laptop) tanpa memerlukan GPU diskrit.

## 💻 Spesifikasi Perangkat Pengujian
Sistem ini telah diuji dan berjalan stabil pada perangkat dengan spesifikasi minimum berikut:
* **Processor:** Intel® Celeron® N5100 @ 1.10GHz (4 CPUs)
* **RAM:** 4GB
* **GPU:** Intel® UHD Graphics (Integrated)
* **OS:** Windows 10/11
* **Camera:** Webcam Laptop Standard / IP Webcam (Android)

*Meskipun spesifikasi terbatas, sistem mampu mempertahankan FPS yang layak (>20 FPS) berkat teknik Frame Skipping dan optimasi algoritma.*

## 🚀 Fitur Utama
* **Ringan & Cepat:** Menggunakan strategi *Frame Skipping* dan *Asynchronous Logic* untuk menjaga performa pada CPU.
* **Deteksi Akurat:** Menggunakan model **YOLOv8** yang dikhususkan untuk plat nomor.
* **Smart OCR:** Menggunakan **EasyOCR** dengan *Auto-Correct Logic* untuk memperbaiki kesalahan baca (misal: Angka `5` dikoreksi jadi Huruf `S` sesuai posisi).
* **Auto-Reconnect:** Fitur otomatis menyambung ulang jika koneksi CCTV/IP Camera terputus.
* **Visual Persistence:** Tampilan GUI stabil dan tidak berkedip meskipun proses deteksi berjalan di latar belakang.

## 🛠️ Teknologi yang Digunakan
* **Python 3.11**
* **OpenCV** (Image Processing & Webcam)
* **Ultralytics YOLOv8** (Object Detection)
* **EasyOCR** (Optical Character Recognition)

## ⚙️ Cara Instalasi (Step-by-Step)

Pastikan Python 3.10 atau 3.11 sudah terinstall di komputer Anda.

1.  **Clone Repository ini**
    ```bash
    git clone [https://github.com/username-anda/nama-repo-anda.git](https://github.com/username-anda/nama-repo-anda.git)
    cd nama-repo-anda
    ```

2.  **Buat Virtual Environment (Wajib)**
    Sangat disarankan menggunakan venv agar library tidak bentrok.
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependensi**
    Copy dan jalankan perintah ini untuk menginstall semua library yang dibutuhkan sekaligus:
    ```bash
    pip install opencv-python ultralytics easyocr numpy
    ```
    *Catatan: EasyOCR akan otomatis mendownload model bahasa saat pertama kali program dijalankan. Pastikan internet aktif.*

4.  **Cek Model**
    Pastikan file `plat_model.pt` sudah ada di dalam folder utama.

## ▶️ Cara Menjalankan
Pastikan venv sudah aktif (muncul tulisan `(venv)` di terminal), lalu jalankan:

```bash
python main.py
