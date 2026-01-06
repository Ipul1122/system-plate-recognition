# 🇮🇩 Indonesian License Plate Recognition (ALPR) - Low Spec Optimized

Sistem pengenalan plat nomor kendaraan Indonesia secara real-time menggunakan webcam. Proyek ini dirancang khusus dan **dioptimalkan untuk berjalan lancar pada perangkat tanpa GPU (CPU Only)** seperti laptop Intel Celeron/i3 dengan RAM 4GB.

## 🚀 Fitur Utama
* **Ringan & Cepat:** Menggunakan strategi *Frame Skipping* dan *Asynchronous Logic* untuk menjaga FPS tetap tinggi (>20 FPS) pada hardware rendah.
* **Deteksi Akurat:** Menggunakan model **YOLOv8** yang dikhususkan untuk plat nomor.
* **OCR Terintegrasi:** Menggunakan **EasyOCR** dengan *Allowlist filtering* (Hanya huruf kapital & angka) untuk pembacaan teks yang presisi.
* **Visual Persistence:** Tampilan GUI stabil dan tidak berkedip meskipun proses deteksi berjalan di latar belakang.

## 🛠️ Teknologi yang Digunakan
* **Python 3.11.9**
* **OpenCV** (Image Processing & Webcam)
* **Ultralytics YOLOv8** (Object Detection)
* **EasyOCR** (Optical Character Recognition)

## ⚙️ Cara Instalasi (Step-by-Step)

Pastikan Python 3.11 sudah terinstall di komputer Anda.

1.  **Clone Repository ini**
    ```bash
    git clone [https://github.com/username-anda/nama-repo-anda.git](https://github.com/username-anda/nama-repo-anda.git)
    cd nama-repo-anda
    ```

2.  **Buat Virtual Environment (Wajib)**
    Sangat disarankan menggunakan venv untuk menghindari konflik library.
    ```bash
    python -m venv venv
    ```

3.  **Aktifkan Virtual Environment**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **Mac/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependensi**
    ```bash
    pip install -r requirements.txt
    ```
    *Catatan: Jika mengalami kendala pada OpenCV, uninstall dulu versi headless dengan `pip uninstall opencv-python-headless -y` lalu install ulang `pip install opencv-python`.*

5.  **Cek Model**
    Pastikan file `plat_model.pt` sudah ada di dalam folder utama.

## ▶️ Cara Menjalankan
Pastikan venv sudah aktif, lalu jalankan:

```bash
python main.py
