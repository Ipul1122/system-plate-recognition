import re

# --- KAMUS KOREKSI ---
dict_int_to_char = {
    '0': 'O', '1': 'I', '2': 'Z', '3': 'E', '4': 'A', 
    '5': 'S', '6': 'G', '7': 'Z', '8': 'B'
}

dict_char_to_int = {
    'O': '0', 'Q': '0', 'D': '0', 'U': '0', 'Z': '2',
    'I': '1', 'L': '1', 'S': '5', 'B': '8', 'A': '4', 'G': '6'
}

def parse_and_correct(ocr_results):
    if not ocr_results: return None, ""

    # 1. Filter Tinggi (Buang tanggal/noise kecil)
    max_h = 0
    for bbox, text, conf in ocr_results:
        h = bbox[2][1] - bbox[0][1]
        if h > max_h: max_h = h
    
    valid_blocks = []
    for bbox, text, conf in ocr_results:
        h = bbox[2][1] - bbox[0][1]
        # Ambang batas 50% dari tinggi maks
        if h > (max_h * 0.5): 
            valid_blocks.append((bbox[0][0], text))
            
    if not valid_blocks: return None, ""

    # 2. Urutkan Kiri -> Kanan
    valid_blocks.sort(key=lambda x: x[0])
    
    # Gabung jadi string mentah
    raw_text_parts = [b[1] for b in valid_blocks]
    raw_full_string = " ".join(raw_text_parts).upper()
    
    # Bersihkan simbol (ambil alphanumeric saja)
    clean_str = "".join(e for e in raw_full_string if e.isalnum())

    # 3. Logika Pisah Wilayah - Nomor - Seri
    first_digit = -1
    last_digit = -1
    
    for i, char in enumerate(clean_str):
        if char.isdigit():
            if first_digit == -1: first_digit = i
            last_digit = i
            
    if first_digit == -1: return raw_full_string, raw_full_string

    # Potong
    part1 = list(clean_str[:first_digit])             # Wilayah
    part2 = list(clean_str[first_digit:last_digit+1]) # Nomor
    part3 = list(clean_str[last_digit+1:])            # Seri
    
    # --- AUTO-CORRECT ---
    
    # Bagian 1: Wilayah (Huruf)
    for i in range(len(part1)):
        if part1[i] in dict_int_to_char: part1[i] = dict_int_to_char[part1[i]]
        
    # Bagian 2: Nomor (Angka)
    for i in range(len(part2)):
        if part2[i] in dict_char_to_int: part2[i] = dict_char_to_int[part2[i]]
        
    # Bagian 3: Seri (Huruf)
    for i in range(len(part3)):
        if part3[i] in dict_int_to_char: part3[i] = dict_int_to_char[part3[i]]

    # --- FILTER KHUSUS (NOISE REMOVAL) ---
    # Jika Wilayah terdeteksi 'Z', 'I', atau 'O' sendirian, dan diikuti angka panjang
    # Kemungkinan itu noise (baut/garis), bukan plat Z sesungguhnya.
    # (Hapus blok ini jika Anda memang ingin mendeteksi Plat Z Sumedang)
    str_area = "".join(part1)
    if len(str_area) == 1 and str_area in ['Z', 'I', 'O', '1', '2']:
        # Anggap ini sampah, kosongkan wilayahnya
        # Jadi "Z 2234 DBF" menjadi "2234 DBF"
        # part1 = [] 
        pass 
        # Note: Saya pasifkan (pass) dulu. Kalau mau aktif, hapus tanda # di baris part1 = []

    final_text = f"{''.join(part1)} {''.join(part2)} {''.join(part3)}"
    
    # Trim spasi depan jika wilayah kosong
    final_text = final_text.strip()
    
    return final_text, raw_full_string