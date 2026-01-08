import cv2
import numpy as np

def improve_lighting(image):
    """
    Mengatasi masalah pencahayaan (Gelap/Bayangan) menggunakan CLAHE.
    (Contrast Limited Adaptive Histogram Equalization)
    """
    # Ubah ke YUV color space
    img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    
    # Ambil channel Y (Luma/Kecerahan)
    y, u, v = cv2.split(img_yuv)
    
    # Terapkan CLAHE (Perbaikan kontras cerdas)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    y_eq = clahe.apply(y)
    
    # Gabungkan kembali
    img_yuv_eq = cv2.merge((y_eq, u, v))
    
    # Kembalikan ke BGR
    result = cv2.cvtColor(img_yuv_eq, cv2.COLOR_YUV2BGR)
    return result

def preprocess_for_ocr(img_crop):
    """
    Pipeline utama pengolahan gambar sebelum masuk OCR.
    1. Improve Lighting
    2. Grayscale
    3. Auto Invert (Plat Hitam -> Putih)
    """
    # 1. Perbaiki Cahaya dulu
    enhanced_img = improve_lighting(img_crop)
    
    # 2. Ubah ke Grayscale
    gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)
    
    # 3. Cek Dominasi Warna (Untuk Auto-Invert)
    # Kita pakai Thresholding Otsu untuk memisahkan background & teks
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Hitung jumlah pixel putih
    total_pixels = binary.size
    white_pixels = cv2.countNonZero(binary)
    
    # Jika pixel putih sedikit (< 50%), berarti background hitam (teks putih)
    # Kita harus INVERT agar jadi Background Putih (teks hitam) yang disukai OCR
    if (white_pixels / total_pixels) < 0.5:
        gray = cv2.bitwise_not(gray)
        
    # Tambahkan sedikit Gaussian Blur untuk hilangkan noise bintik-bintik
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    
    return gray