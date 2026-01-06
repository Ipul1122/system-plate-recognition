import cv2
import time
import easyocr
from ultralytics import YOLO

def main():
    print("--- SISTEM PLAT NOMOR: PERFORMANCE MODE ---")
    
    # 1. INISIALISASI (LOAD MODEL DI AWAL)
    print("[INFO] Loading EasyOCR (CPU Mode)...")
    reader = easyocr.Reader(['en'], gpu=False) 
    
    print("[INFO] Loading YOLO Model...")
    try:
        # Gunakan model plat yang sudah didownload
        model = YOLO('plat_model.pt') 
    except:
        print("[WARNING] 'plat_model.pt' tidak ada. Menggunakan 'yolov8n.pt' standar.")
        model = YOLO('yolov8n.pt')

    # 2. SETUP KAMERA (KUNCI PERFORMA)
    cap = cv2.VideoCapture(0)
    # Wajib 640x480. Resolusi HD (1280x720) akan membuat FPS drop ke 5.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 3. VARIABEL OPTIMASI
    FRAME_SKIP = 7      # AI hanya jalan tiap 7 frame sekali (Video tetap lancar)
    frame_count = 0
    
    # Memori untuk menyimpan hasil terakhir saat AI 'istirahat'
    last_box = None
    last_text = ""
    last_color = (0, 255, 0)
    
    # Variabel FPS
    prev_time = 0
    curr_fps = 0

    print("[INFO] Siap! Tekan 'q' untuk berhenti.")

    while True:
        start_time = time.time()
        success, frame = cap.read()
        
        if not success:
            break

        # --- OTAK AI (Hanya jalan sesekali) ---
        if frame_count % FRAME_SKIP == 0:
            # Reset sementara
            detected_in_this_frame = False
            
            # 1. Deteksi YOLO (Image Size 320 cukup untuk plat jarak dekat)
            results = model(frame, imgsz=320, conf=0.4, verbose=False)
            
            for result in results:
                if len(result.boxes) > 0:
                    # Ambil kotak dengan confidence tertinggi
                    box = result.boxes[0]
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Validasi ukuran kotak (filter error kecil)
                    if (x2-x1) > 50 and (y2-y1) > 20:
                        last_box = (x1, y1, x2, y2)
                        
                        # 2. Crop & OCR
                        # Crop dengan margin sedikit
                        h_img, w_img, _ = frame.shape
                        crop = frame[max(0, y1-5):min(h_img, y2+5), max(0, x1-5):min(w_img, x2+5)]
                        
                        try:
                            # OCR hanya membaca Alphanumeric
                            ocr_res = reader.readtext(crop, detail=0, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                            if ocr_res:
                                last_text = " ".join(ocr_res)
                                last_color = (0, 255, 0) # Hijau jika terbaca
                            else:
                                last_text = "Plat Terdeteksi..."
                                last_color = (0, 255, 255) # Kuning jika belum terbaca
                        except:
                            pass
                        
                        detected_in_this_frame = True
                        break # Ambil 1 plat saja
            
            # Jika frame ini YOLO jalan tapi tidak nemu apa-apa, reset memori lama
            if not detected_in_this_frame:
                last_box = None
                last_text = ""

        # --- VISUALISASI (Jalan di setiap frame) ---
        # Gambar ulang hasil terakhir (Persistence)
        if last_box:
            x1, y1, x2, y2 = last_box
            cv2.rectangle(frame, (x1, y1), (x2, y2), last_color, 2)
            # Background hitam untuk teks agar jelas
            cv2.rectangle(frame, (x1, y1-30), (x1 + 250, y1), last_color, -1)
            cv2.putText(frame, last_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # --- HITUNG FPS REAL-TIME ---
        # Moving Average sederhana agar angka tidak loncat-loncat
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        curr_fps = int(fps)

        # Tampilkan FPS Besar di Pojok Kiri
        color_fps = (0, 255, 0) if curr_fps > 20 else (0, 0, 255) # Hijau jika >20, Merah jika drop
        cv2.putText(frame, f"FPS: {curr_fps}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_fps, 2)
        
        # Tampilkan Status Engine
        status = "AI: Thinking..." if frame_count % FRAME_SKIP == 0 else "AI: Skipped"
        cv2.putText(frame, status, (10, 70), cv2.FONT_HERSHEY_PLAIN, 1, (200, 200, 200), 1)

        cv2.imshow("Plat Recognition System", frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()