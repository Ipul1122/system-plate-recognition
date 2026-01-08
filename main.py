import warnings
warnings.filterwarnings("ignore")

import cv2
import time
import easyocr
from ultralytics import YOLO

# Import Modul Kita
import image_utils
import ocr_utils

# --- DATABASE SIMULATION ---
def save_to_database_mockup(clean_text, raw_text):
    """
    Ini adalah simulasi fungsi save ke database.
    Nantinya di sini Anda coding koneksi ke MySQL/PostgreSQL.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n[DATABASE] === MENYIMPAN DATA ===")
    print(f"[DATABASE] Waktu   : {timestamp}")
    print(f"[DATABASE] INPUT   : {clean_text}  <-- INI YANG DISIMPAN")
    print(f"[DATABASE] (Debug) : {raw_text}")
    print("[DATABASE] ========================\n")
    # Disini nanti code: cursor.execute("INSERT INTO log (plat) VALUES (%s)", (clean_text,))

def main():
    print("--- SISTEM FINAL: DATABASE READY ---")
    
    print("[INIT] Loading EasyOCR...")
    reader = easyocr.Reader(['en'], gpu=False)
    
    print("[INIT] Loading YOLO...")
    try:
        model = YOLO('plat_model.pt')
    except:
        model = YOLO('yolov8n.pt')

    print("[INIT] Buka Kamera...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Config
    FRAME_SKIP = 5
    frame_count = 0
    
    # Variabel Display
    current_text = "WAITING..."
    current_color = (0, 255, 255)
    current_box = None
    debug_img = None 
    
    # Variabel Database Logic
    last_saved_text = ""
    last_save_time = 0
    DB_SAVE_DELAY = 5.0 # Jangan simpan plat yang sama sebelum 5 detik berlalu

    while True:
        success, frame = cap.read()
        if not success: break
        
        # --- AI PROCESS ---
        if frame_count % FRAME_SKIP == 0:
            results = model(frame, imgsz=320, conf=0.4, verbose=False)
            detected_now = False
            
            for result in results:
                if len(result.boxes) > 0:
                    box = result.boxes[0]
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    if (x2-x1) > 50 and (y2-y1) > 20:
                        detected_now = True
                        current_box = (x1, y1, x2, y2)
                        
                        h, w, _ = frame.shape
                        crop = frame[max(0, y1-10):min(h, y2+10), max(0, x1-10):min(w, x2+10)]
                        
                        try:
                            # 1. Preprocessing
                            processed_crop = image_utils.preprocess_for_ocr(crop)
                            debug_img = processed_crop 
                            
                            # 2. OCR Read
                            raw_results = reader.readtext(processed_crop)
                            
                            if raw_results:
                                # 3. Parsing & Cleaning (Ini Kuncinya)
                                final, raw = ocr_utils.parse_and_correct(raw_results)
                                
                                if final and len(final) > 3:
                                    current_text = final # Tampilkan yang bersih
                                    current_color = (0, 255, 0)
                                    
                                    # --- LOGIKA DATABASE ---
                                    # Simpan hanya jika teksnya BERBEDA dari yang terakhir disimpan
                                    # ATAU sudah lewat 5 detik
                                    if (final != last_saved_text) or ((time.time() - last_save_time) > DB_SAVE_DELAY):
                                        save_to_database_mockup(final, raw)
                                        last_saved_text = final
                                        last_save_time = time.time()

                        except Exception as e:
                            print(f"[ERR] {e}")
                        
                        break 
            
            if not detected_now:
                current_color = (0, 0, 255)

        # --- VISUALISASI ---
        if current_box:
            x1, y1, x2, y2 = current_box
            cv2.rectangle(frame, (x1, y1), (x2, y2), current_color, 2)
            cv2.rectangle(frame, (x1, y1-35), (x1+250, y1), current_color, -1)
            # Tampilkan text bersih di layar
            cv2.putText(frame, current_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        # Debug View (Pojok Kanan Bawah)
        if debug_img is not None:
            try:
                small_view = cv2.resize(debug_img, (150, 50))
                small_view_color = cv2.cvtColor(small_view, cv2.COLOR_GRAY2BGR)
                h, w, _ = frame.shape
                frame[h-60:h-10, w-160:w-10] = small_view_color
                cv2.rectangle(frame, (w-160, h-60), (w-10, h-10), (0,255,255), 1)
                cv2.putText(frame, "OCR EYE", (w-160, h-65), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
            except: pass

        cv2.putText(frame, "Tekan 'q' Exit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        cv2.imshow("Sistem Final", frame)
        frame_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()