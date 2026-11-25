import tkinter as tk
from tkinter import messagebox as mb, filedialog as fd
import math

# ==========================================
# CÁC HÀM TOÁN HỌC RSA CƠ BẢN
# ==========================================
def is_prime(num):
    """Kiểm tra số nguyên tố"""
    if num <= 1: return False
    if num <= 3: return True
    if num % 2 == 0 or num % 3 == 0: return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Tìm khóa bí mật d sao cho (e * d) % phi == 1 bằng thuật toán Euclid mở rộng"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y

    _, x, _ = extended_gcd(e, phi)
    return (x % phi + phi) % phi

# ==========================================
# BIẾN TOÀN CỤC & HÀM ĐIỀU HƯỚNG PHÂN TÍCH
# ==========================================
rsa_log = {"GEN": "", "ENC": "", "DEC": ""}
current_tab = "GEN"
is_analysis_visible = False

def toggle_analysis():
    global is_analysis_visible
    if not is_analysis_visible:
        root.geometry("1150x680")
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)
        btn_analyze.config(text="ẨN PHÂN TÍCH")
        is_analysis_visible = True
    else:
        frame_right.pack_forget()
        root.geometry("560x680")
        btn_analyze.config(text="PHÂN TÍCH")
        is_analysis_visible = False

def switch_tab(tab_name):
    global current_tab
    current_tab = tab_name
    for btn, name in zip([btn_tab_gen, btn_tab_enc, btn_tab_dec], ["GEN", "ENC", "DEC"]):
        if name == tab_name:
            btn.config(bg="#3B82F6", fg="white") 
        else:
            btn.config(bg="#E5E7EB", fg="#374151") 
            
    txt_analysis.delete("1.0", tk.END)
    txt_analysis.insert(tk.END, rsa_log.get(tab_name, "Chưa có dữ liệu.\nVui lòng thực hiện thao tác Mã Hóa / Giải Mã trước."))

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
# THỰC THI THUẬT TOÁN RSA
# ==========================================
def process_rsa(is_decrypt=False):
    try:
        p = int(p_ent.get().strip())
        q = int(q_ent.get().strip())
        e = int(e_ent.get().strip())
    except ValueError:
        return mb.showerror("Lỗi", "Các tham số p, q, e phải là số nguyên!")

    # KIỂM TRA ĐIỀU KIỆN SỐ NGUYÊN TỐ CỦA P VÀ Q
    if not is_prime(p) or not is_prime(q):
        return mb.showerror("Lỗi Toán Học", "p và q bắt buộc phải là các số nguyên tố!")
    
    if p == q:
        return mb.showerror("Lỗi Toán Học", "p và q phải là hai số nguyên tố phân biệt (khác nhau)!")

    msg = txt_in.get("1.0", tk.END).strip()
    if not msg:
        return mb.showerror("Lỗi", "Vui lòng nhập nội dung văn bản.")

    # 1. TẠO KHÓA RSA
    n = p * q 
    phi = (p - 1) * (q - 1) 
    
    if gcd(e, phi) != 1: 
        return mb.showerror("Lỗi Toán Học", f"Khóa e = {e} không nguyên tố cùng nhau với phi(n) = {phi} (gcd != 1).")

    d = mod_inverse(e, phi) 

    log_gen = " BƯỚC 1: TẠO KHÓA RSA\n" + "="*45 + "\n"
    log_gen += f"- Chọn 2 số nguyên tố p = {p}, q = {q}\n" 
    log_gen += f"- Tính n = p * q = {n}\n" 
    log_gen += f"- Tính Phi(n) = (p-1)*(q-1) = {phi}\n" 
    log_gen += f"- Chọn e = {e} (thỏa mãn 1 < e < Phi và gcd(e, Phi) = 1)\n" 
    log_gen += f"- Tính khóa bí mật d: (e * d) mod Phi = 1 => d = {d}\n\n" 
    log_gen += f" >> Khóa công khai KU = {{e: {e}, n: {n}}}\n" 
    log_gen += f" >> Khóa riêng tư KR = {{d: {d}, n: {n}}}\n" 
    rsa_log["GEN"] = log_gen

    try:
        if is_decrypt:
            # Giải mã: C gom thành mảng số nguyên phân cách bằng dấu cách
            cipher_vals = [int(x) for x in msg.split()]
            plain_chars = [chr(pow(c, d, n)) for c in cipher_vals]
            out_final = "".join(plain_chars)
            
            rsa_log["DEC"] = f" BƯỚC GIẢI MÃ RSA\n" + "="*45 + f"\nCông thức: M = C^d mod n\nKhóa giải mã riêng tư d = {d}, n = {n}\nGiải mã thành công chuỗi ký tự."
        else:
            # Mã hóa từng ký tự
            plain_nums = [ord(char) for char in msg]
            cipher_nums = [pow(m, e, n) for m in plain_nums]
            out_final = " ".join(map(str, cipher_nums))
            
            log_enc = f" BƯỚC MÃ HÓA RSA\n" + "="*45 + f"\nCông thức: C = M^e mod n\nKhóa mã hóa công khai e = {e}, n = {n}\n\nChi tiết chuyển đổi từng ký tự:\n"
            for char, m, c in zip(msg, plain_nums, cipher_nums):
                log_enc += f" Ký tự '{char}' (ASCII: {m}) -> C = {m}^{e} mod {n} = {c}\n"
            rsa_log["ENC"] = log_enc
            
    except Exception as ex:
        return mb.showerror("Lỗi Xử Lý", f"Lỗi tính toán mã hóa/giải mã: {str(ex)}")

    txt_out.delete("1.0", tk.END)
    txt_out.insert(tk.END, out_final)
    switch_tab(current_tab)

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
root.title("Hệ Mã Hóa Công Khai RSA")
root.geometry("560x680")
root.configure(bg="#F3F4F6")

frame_left = tk.Frame(root, bg="#F3F4F6")
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

frame_right = tk.Frame(root, bg="#F3F4F6")

# --- LOGO RSA ---
header_logo = tk.Frame(frame_left, bg="#F3F4F6")
header_logo.pack(anchor="w", fill=tk.X, pady=(0, 15))
f_logo, _ = make_shadow(header_logo, tk.Label, offset=4, shadow_bg="#1E40AF", border="#1D4ED8", text=" RSA ", font=("Arial Black", 24, "bold"), bg="#3B82F6", fg="white", padx=8, pady=2)
f_logo.pack(side=tk.LEFT)
tk.Label(header_logo, text="Hệ mã hóa khóa công khai (Asymmetric)", font=("Segoe UI", 9, "italic"), fg="#6B7280", bg="#F3F4F6").pack(side=tk.LEFT, padx=10, pady=6)

# --- THAM SỐ KHÓA P, Q, E ---
param_frame = tk.Frame(frame_left, bg="#F3F4F6")
param_frame.pack(fill=tk.X, pady=(0, 10))

def add_param_input(parent, label_text, default_val):
    f = tk.Frame(parent, bg="#F3F4F6")
    f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
    tk.Label(f, text=label_text, bg="#F3F4F6", font=("Segoe UI", 9, "bold"), fg="#374151").pack(anchor="w")
    box, ent = make_shadow(f, tk.Entry, offset=2, font=("Consolas", 11, "bold"), bg="#FFFFFF", fg="#1D4ED8", justify="center")
    box.pack(fill=tk.X, pady=2)
    ent.insert(0, default_val)
    return ent

p_ent = add_param_input(param_frame, "Số nguyên tố p:", "61")
q_ent = add_param_input(param_frame, "Số nguyên tố q:", "53")
e_ent = add_param_input(param_frame, "Khóa e:", "17")

# --- KHU VỰC NHẬP VĂN BẢN ---
header_in = tk.Frame(frame_left, bg="#F3F4F6")
header_in.pack(fill=tk.X, pady=(5, 0))
tk.Label(header_in, text="Văn bản (Plaintext / Cipher int):", bg="#F3F4F6", font=("Segoe UI", 9, "bold"), fg="#374151").pack(side=tk.LEFT)
f_btn_open, _ = make_shadow(header_in, tk.Button, offset=2, text="📂 Chọn File", bg="#FFFFFF", fg="#374151", font=("Segoe UI", 8, "bold"), cursor="hand2", command=lambda: io_file(False))
f_btn_open.pack(side=tk.RIGHT)

f_in, txt_in = make_shadow(frame_left, tk.Text, height=4, font=("Consolas", 10), bg="#FFFFFF")
f_in.pack(pady=(3, 8), fill=tk.X)
txt_in.insert(tk.END, "HI")

# --- NÚT THỰC THI ---
btn_frame = tk.Frame(frame_left, bg="#F3F4F6")
btn_frame.pack(pady=5)

f_enc, _ = make_shadow(btn_frame, tk.Button, shadow_bg="#047857", border="#059669", text="MÃ HÓA", bg="#10B981", fg="white", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=10, pady=4, command=lambda: process_rsa(False))
f_enc.pack(side=tk.LEFT, padx=4)

f_dec, _ = make_shadow(btn_frame, tk.Button, shadow_bg="#1D4ED8", border="#2563EB", text="GIẢI MÃ", bg="#3B82F6", fg="white", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=10, pady=4, command=lambda: process_rsa(True))
f_dec.pack(side=tk.LEFT, padx=4)

f_analyze, btn_analyze = make_shadow(btn_frame, tk.Button, shadow_bg="#5B21B6", border="#6D28D9", text="PHÂN TÍCH", bg="#8B5CF6", fg="white", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=10, pady=4, command=toggle_analysis)
f_analyze.pack(side=tk.LEFT, padx=4)

# --- KHU VỰC KẾT QUẢ ---
header_out = tk.Frame(frame_left, bg="#F3F4F6")
header_out.pack(fill=tk.X, pady=(5, 0))
tk.Label(header_out, text="Kết quả đầu ra:", bg="#F3F4F6", font=("Segoe UI", 9, "bold"), fg="#374151").pack(side=tk.LEFT)
f_btn_save, _ = make_shadow(header_out, tk.Button, offset=2, text="💾 Lưu File", bg="#FFFFFF", fg="#374151", font=("Segoe UI", 8, "bold"), cursor="hand2", command=lambda: io_file(True))
f_btn_save.pack(side=tk.RIGHT)

f_out, txt_out = make_shadow(frame_left, tk.Text, height=4, font=("Consolas", 10), bg="#F9FAFB")
f_out.pack(pady=3, fill=tk.X)

# --- KHUNG PHẢI: THANH ĐIỀU HƯỚNG & PHÂN TÍCH ---
tk.Label(frame_right, text="Theo dõi chi tiết thuật toán RSA:", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w", pady=(0, 5))

nav_frame = tk.Frame(frame_right, bg="#F3F4F6")
nav_frame.pack(fill=tk.X, pady=(0, 10))

btn_tab_gen = tk.Button(nav_frame, text="1. Tạo Khóa", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("GEN"))
btn_tab_gen.pack(side=tk.LEFT, padx=2)
btn_tab_enc = tk.Button(nav_frame, text="2. Mã Hóa", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("ENC"))
btn_tab_enc.pack(side=tk.LEFT, padx=2)
btn_tab_dec = tk.Button(nav_frame, text="3. Giải Mã", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("DEC"))
btn_tab_dec.pack(side=tk.LEFT, padx=2)

f_analysis, txt_analysis = make_shadow(frame_right, tk.Text, offset=6, width=58, font=("Courier New", 10, "bold"), bg="#FFFFFF", fg="#1F2937", padx=15, pady=15)
f_analysis.pack(fill=tk.BOTH, expand=True)

switch_tab("GEN")

root.mainloop()