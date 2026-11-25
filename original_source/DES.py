import tkinter as tk
from tkinter import messagebox as mb, filedialog as fd

# ==========================================
# CÁC BẢNG HẰNG SỐ TIÊU CHUẨN CỦA HỆ MÃ DES
# ==========================================
PC1 = [
    57, 49, 41, 33, 25, 17, 9,  1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27, 19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29, 21, 13, 5,  28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,  16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

IP = [
    58, 50, 42, 34, 26, 18, 10, 2,  60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,  64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,  59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,  63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41,  9, 49, 17, 57, 25
]

E_BOX = [
    32, 1,  2,  3,  4,  5,  4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]

P_BOX = [
    16, 7,  20, 21, 29, 12, 28, 17, 1,  15, 23, 26, 5,  18, 31, 10,
    2,  8,  24, 14, 32, 27, 3,  9,  19, 13, 30, 6,  22, 11, 4,  25
]

S_BOX = [
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7], [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8], [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0], [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10], [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5], [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15], [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8], [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1], [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7], [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15], [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9], [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4], [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9], [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6], [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14], [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11], [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8], [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6], [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1], [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6], [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2], [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7], [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2], [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8], [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

# ==========================================
# CÁC HÀM XỬ LÝ NHỊ PHÂN CỐT LÕI
# ==========================================
def permute(bits, table): return "".join(bits[i - 1] for i in table)
def left_shift(bits, n): return bits[n:] + bits[:n]
def xor(b1, b2): return "".join("1" if b1[i] != b2[i] else "0" for i in range(len(b1)))
def format_bits(bits, chunk): return "  ".join(bits[i:i+chunk] for i in range(0, len(bits), chunk))
def bin_to_hex(b): return hex(int(b, 2))[2:].upper().zfill(len(b)//4)

# ==========================================
# BIẾN TOÀN CỤC & HÀM ĐIỀU HƯỚNG
# ==========================================
step_data = {"KEY": "", "IP": "", "ROUNDS": "", "FP": ""}
current_tab = "KEY"
is_analysis_visible = False # Trạng thái bảng phân tích

def toggle_analysis():
    global is_analysis_visible
    if not is_analysis_visible:
        root.geometry("1150x660")
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)
        btn_analyze.config(text="ẨN PHÂN TÍCH")
        is_analysis_visible = True
    else:
        frame_right.pack_forget()
        root.geometry("560x660")
        btn_analyze.config(text="PHÂN TÍCH")
        is_analysis_visible = False

def switch_tab(tab_name):
    global current_tab
    current_tab = tab_name
    for btn, name in zip([btn_tab_key, btn_tab_ip, btn_tab_round, btn_tab_fp], ["KEY", "IP", "ROUNDS", "FP"]):
        if name == tab_name:
            btn.config(bg="#3B82F6", fg="white") 
        else:
            btn.config(bg="#E5E7EB", fg="#374151") 
            
    txt_analysis.delete("1.0", tk.END)
    txt_analysis.insert(tk.END, step_data.get(tab_name, "Chưa có dữ liệu.\nVui lòng nhấn MÃ HÓA hoặc GIẢI MÃ trước."))

# ==========================================
# HÀM XỬ LÝ FILE (NHẬP / XUẤT)
# ==========================================
def io_file(is_save=False):
    try:
        if is_save:
            p = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if p: 
                with open(p, "w", encoding="utf-8") as f:
                    f.write(txt_out.get("1.0", tk.END).strip())
                mb.showinfo("Thành công", "Đã lưu kết quả thành công!")
        else:
            p = fd.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if p: 
                with open(p, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                txt_in.delete("1.0", tk.END)
                txt_in.insert(tk.END, content)
    except Exception as e:
        mb.showerror("Lỗi", f"Không thể xử lý file: {str(e)}")

# ==========================================
# HÀM THUẬT TOÁN DES CHÍNH
# ==========================================
def run_des(is_decrypt=False):
    key_hex = k_ent.get().strip().upper()
    msg = txt_in.get("1.0", tk.END).strip()
    
    if len(key_hex) != 16: return mb.showerror("Lỗi", "Khóa K phải đúng 16 ký tự Hex (64-bit).")
    if not msg: return mb.showerror("Lỗi", "Vui lòng nhập văn bản.")
    
    try:
        key_bin = bin(int(key_hex, 16))[2:].zfill(64)
    except:
        return mb.showerror("Lỗi", "Khóa K chỉ được chứa ký tự thập lục phân (0-9, A-F).")

    # 1. SINH KHÓA
    pc1_res = permute(key_bin, PC1)
    C, D = pc1_res[:28], pc1_res[28:]
    subkeys = []
    
    log_key = " BƯỚC 1: SINH 16 KHÓA CON\n" + "="*50 + "\n"
    log_key += f"Khóa K (64-bit):\n{format_bits(key_bin, 8)}\n\n"
    for i in range(16):
        shift = SHIFTS[i]
        C, D = left_shift(C, shift), left_shift(D, shift)
        subkeys.append(permute(C + D, PC2))
        log_key += f"K{i+1:<2} (48-bit): {format_bits(subkeys[-1], 6)}\n"
    step_data["KEY"] = log_key

    # Tiền xử lý dữ liệu
    if is_decrypt:
        try: msg_bin = bin(int(msg, 16))[2:].zfill(len(msg)*4)
        except: return mb.showerror("Lỗi", "Giải mã yêu cầu văn bản đầu vào là chuỗi Hex!")
        work_keys = subkeys[::-1] 
    else:
        msg_bytes = msg.encode('utf-8')
        pad_len = 8 - (len(msg_bytes) % 8)
        msg_bytes += bytes([pad_len] * pad_len)
        msg_bin = "".join(format(b, '08b') for b in msg_bytes)
        work_keys = subkeys

    out_bin = ""
    log_ip = log_rounds = log_fp = ""

    # Duyệt từng khối
    for block_idx in range(0, len(msg_bin), 64):
        block = msg_bin[block_idx:block_idx+64]
        
        # 2. BƯỚC IP
        ip_res = permute(block, IP)
        L, R = ip_res[:32], ip_res[32:]
        
        if block_idx == 0:
            log_ip = f" BƯỚC 2: HOÁN VỊ KHỞI ĐẦU IP (Khối 1)\n" + "="*50 + "\n"
            log_ip += f"Đầu vào 64-bit:\n{format_bits(block, 8)}\n\n"
            log_ip += f"Sau IP -> Chia L0, R0:\n"
            log_ip += f"L0: {format_bits(L, 8)}\nR0: {format_bits(R, 8)}\n"
            step_data["IP"] = log_ip
            log_rounds = f" BƯỚC 3: CHI TIẾT 16 VÒNG LẶP (Khối 1)\n" + "="*50 + "\n"

        # 3. BƯỚC 16 VÒNG LẶP
        for i in range(16):
            L_prev, R_prev = L, R
            e_res = permute(R_prev, E_BOX)
            xor_res = xor(e_res, work_keys[i])
            s_res = ""
            for j in range(8):
                chunk = xor_res[j*6 : (j+1)*6]
                row = int(chunk[0] + chunk[5], 2)
                col = int(chunk[1:5], 2)
                val = bin(S_BOX[j][row][col])[2:].zfill(4)
                s_res += val
            f_res = permute(s_res, P_BOX)
            
            L = R_prev
            R = xor(L_prev, f_res)
            
            if block_idx == 0:
                log_rounds += f"[Vòng {i+1}] Dùng Khóa K{16-i if is_decrypt else i+1}\n"
                log_rounds += f"L{i+1}: {bin_to_hex(L)} | R{i+1}: {bin_to_hex(R)}\n"
                log_rounds += "-"*30 + "\n"
                
        if block_idx == 0: step_data["ROUNDS"] = log_rounds

        # 4. BƯỚC FP
        rl_res = R + L
        fp_res = permute(rl_res, FP)
        out_bin += fp_res
        
        if block_idx == 0:
            log_fp = f" BƯỚC 4: HOÁN VỊ KẾT THÚC FP (Khối 1)\n" + "="*50 + "\n"
            log_fp += f"Ghép R16 L16 (Lưu ý bị đảo ngược vị trí):\n{format_bits(rl_res, 8)}\n\n"
            log_fp += f"Sau hoán vị FP (Kết quả khối):\n{format_bits(fp_res, 8)}\n"
            log_fp += f"Dạng Hex: {bin_to_hex(fp_res)}\n"
            step_data["FP"] = log_fp

    # Xuất kết quả
    if is_decrypt:
        out_bytes = int(out_bin, 2).to_bytes(len(out_bin) // 8, byteorder='big')
        pad = out_bytes[-1]
        out_final = out_bytes[:-pad].decode('utf-8', errors='ignore')
    else:
        out_final = bin_to_hex(out_bin)

    txt_out.delete("1.0", tk.END)
    txt_out.insert(tk.END, out_final)
    switch_tab(current_tab) # Cập nhật dữ liệu ngầm cho Bảng Phân Tích

# ==========================================
# UI NEO-BRUTALISM CƠ BẢN
# ==========================================
def make_shadow(parent, w_class, offset=4, shadow_bg="#D1D5DB", border="#E5E7EB", **kwargs):
    f = tk.Frame(parent, bg="#F3F4F6")
    front = tk.Frame(f, bg=border, padx=1, pady=1)
    front.pack(padx=(0, offset), pady=(0, offset), fill=tk.BOTH, expand=True)
    kwargs.setdefault('relief', 'flat')
    kwargs.setdefault('borderwidth', 0)
    kwargs.setdefault('highlightthickness', 0)
    w = w_class(front, **kwargs)
    w.pack(fill=tk.BOTH, expand=True)
    s = tk.Frame(f, bg=shadow_bg)
    s.place(x=offset, y=offset, relwidth=1, relheight=1, width=-offset, height=-offset)
    s.lower()
    return f, w

root = tk.Tk()
root.title("Hệ Mã Hóa Tiêu Chuẩn DES (Có Ẩn/Hiện Phân Tích)")
# Cửa sổ khởi tạo thu gọn (chỉ hiện bên trái)
root.geometry("560x660")
root.configure(bg="#F3F4F6")

frame_left = tk.Frame(root, bg="#F3F4F6")
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Khởi tạo frame_right nhưng chưa pack
frame_right = tk.Frame(root, bg="#F3F4F6")

# --- KHUNG TRÁI: NHẬP XUẤT ---
tk.Label(frame_left, text="Khóa K (16 ký tự Hex = 64-bit):", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w")
f_k, k_ent = make_shadow(frame_left, tk.Entry, offset=3, font=("Consolas", 12, "bold"), bg="#FFFFFF", fg="#1D4ED8")
f_k.pack(pady=(5, 10), fill=tk.X)
k_ent.insert(0, "133457799BBCDFF1")

# Khu vực Nhập file
header_in = tk.Frame(frame_left, bg="#F3F4F6")
header_in.pack(fill=tk.X, pady=(5, 0))
tk.Label(header_in, text="Văn bản (Plaintext / Ciphertext Hex):", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(side=tk.LEFT)
f_btn_open, btn_open = make_shadow(header_in, tk.Button, offset=2, text="📂 Chọn File Text", bg="#FFFFFF", fg="#374151", activebackground="#E5E7EB", font=("Segoe UI", 8, "bold"), cursor="hand2", command=lambda: io_file(False))
f_btn_open.pack(side=tk.RIGHT)

f_in, txt_in = make_shadow(frame_left, tk.Text, height=5, font=("Consolas", 11), bg="#FFFFFF")
f_in.pack(pady=(5, 10), fill=tk.X)
txt_in.insert(tk.END, "VIETNAM")

# Cụm Nút Thao Tác (Có thêm nút PHÂN TÍCH)
btn_frame = tk.Frame(frame_left, bg="#F3F4F6")
btn_frame.pack(pady=10)

f_enc, btn_enc = make_shadow(btn_frame, tk.Button, shadow_bg="#047857", border="#059669", text="MÃ HÓA", bg="#10B981", fg="white", activebackground="#059669", activeforeground="white", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=12, pady=4, command=lambda: run_des(False))
f_enc.pack(side=tk.LEFT, padx=5)

f_dec, btn_dec = make_shadow(btn_frame, tk.Button, shadow_bg="#1D4ED8", border="#2563EB", text="GIẢI MÃ", bg="#3B82F6", fg="white", activebackground="#2563EB", activeforeground="white", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=12, pady=4, command=lambda: run_des(True))
f_dec.pack(side=tk.LEFT, padx=5)

f_analyze, btn_analyze = make_shadow(btn_frame, tk.Button, shadow_bg="#5B21B6", border="#6D28D9", text="PHÂN TÍCH", bg="#8B5CF6", fg="white", activebackground="#6D28D9", activeforeground="white", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=12, pady=4, command=toggle_analysis)
f_analyze.pack(side=tk.LEFT, padx=5)

# Khu vực Lưu file
header_out = tk.Frame(frame_left, bg="#F3F4F6")
header_out.pack(fill=tk.X, pady=(5, 0))
tk.Label(header_out, text="Kết quả đầu ra:", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(side=tk.LEFT)
f_btn_save, btn_save = make_shadow(header_out, tk.Button, offset=2, text="💾 Lưu Kết Quả", bg="#FFFFFF", fg="#374151", activebackground="#E5E7EB", font=("Segoe UI", 8, "bold"), cursor="hand2", command=lambda: io_file(True))
f_btn_save.pack(side=tk.RIGHT)

f_out, txt_out = make_shadow(frame_left, tk.Text, height=5, font=("Consolas", 11), bg="#F9FAFB")
f_out.pack(pady=5, fill=tk.X)

# --- KHUNG PHẢI: THANH ĐIỀU HƯỚNG VÀ PHÂN TÍCH ---
tk.Label(frame_right, text="Theo dõi thuật toán mã hóa khối (Block 1):", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w", pady=(0, 5))

nav_frame = tk.Frame(frame_right, bg="#F3F4F6")
nav_frame.pack(fill=tk.X, pady=(0, 10))

btn_tab_key = tk.Button(nav_frame, text="1. Sinh Khóa", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("KEY"))
btn_tab_key.pack(side=tk.LEFT, padx=2)
btn_tab_ip = tk.Button(nav_frame, text="2. Bước IP", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("IP"))
btn_tab_ip.pack(side=tk.LEFT, padx=2)
btn_tab_round = tk.Button(nav_frame, text="3. 16 Vòng Lặp", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("ROUNDS"))
btn_tab_round.pack(side=tk.LEFT, padx=2)
btn_tab_fp = tk.Button(nav_frame, text="4. Bước FP", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("FP"))
btn_tab_fp.pack(side=tk.LEFT, padx=2)

f_analysis, txt_analysis = make_shadow(frame_right, tk.Text, offset=6, width=58, font=("Courier New", 10, "bold"), bg="#FFFFFF", fg="#1F2937", padx=15, pady=15)
f_analysis.pack(fill=tk.BOTH, expand=True)

# Gắn sẵn dữ liệu rỗng cho tab đầu tiên
switch_tab("KEY")

root.mainloop()