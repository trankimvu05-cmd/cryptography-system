import tkinter as tk
from tkinter import messagebox as mb

# ==========================================
# CÁC HÀM TOÁN HỌC DIFFIE-HELLMAN
# ==========================================
def is_prime(num):
    """Kiểm tra số nguyên tố (dành cho tham số q)"""
    if num <= 1: return False
    if num <= 3: return True
    if num % 2 == 0 or num % 3 == 0: return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def is_primitive_root(alpha, q):
    """Kiểm tra alpha có phải là nguyên căn (primitive root) của q hay không"""
    if alpha <= 1 or alpha >= q:
        return False
    phi = q - 1
    factors = set()
    n = phi
    # Tìm các thừa số nguyên tố của phi (q-1)
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 2
    if n > 2:
        factors.add(n)
    
    # Nếu alpha^(phi/p) mod q == 1 với bất kỳ thừa số nguyên tố p nào, alpha không phải nguyên căn
    for p in factors:
        if pow(alpha, phi // p, q) == 1:
            return False
    return True

# ==========================================
# BIẾN TOÀN CỤC & HÀM ĐIỀU HƯỚNG PHÂN TÍCH
# ==========================================
dh_log = {"PUB": "", "SEC": ""}
current_tab = "PUB"
is_analysis_visible = False

def toggle_analysis():
    global is_analysis_visible
    if not is_analysis_visible:
        root.geometry("1150x580")
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)
        btn_analyze.config(text="ẨN PHÂN TÍCH")
        is_analysis_visible = True
    else:
        frame_right.pack_forget()
        root.geometry("560x580")
        btn_analyze.config(text="PHÂN TÍCH")
        is_analysis_visible = False

def switch_tab(tab_name):
    global current_tab
    current_tab = tab_name
    tabs = {"PUB": btn_tab_pub, "SEC": btn_tab_sec}
    
    for name, btn in tabs.items():
        if name == tab_name:
            btn.config(bg="#3B82F6", fg="white") 
        else:
            btn.config(bg="#E5E7EB", fg="#374151") 
            
    txt_analysis.delete("1.0", tk.END)
    txt_analysis.insert(tk.END, dh_log.get(tab_name, "Chưa có dữ liệu.\nVui lòng nhấn nút TÍNH TOÁN."))

# ==========================================
# THỰC THI THUẬT TOÁN DIFFIE-HELLMAN
# ==========================================
def process_dh():
    try:
        q = int(q_ent.get().strip())
        alpha = int(alpha_ent.get().strip())
        xa = int(xa_ent.get().strip())
        xb = int(xb_ent.get().strip())
    except ValueError:
        return mb.showerror("Lỗi", "Các tham số q, alpha, XA, XB phải là số nguyên!")

    # Kiểm tra điều kiện toán học dựa theo quy luật của Diffie-Hellman
    if not is_prime(q):
        return mb.showerror("Lỗi Toán Học", f"q = {q} không phải là số nguyên tố!")
    
    if not is_primitive_root(alpha, q):
        return mb.showerror("Lỗi Toán Học", f"alpha = {alpha} không phải là nguyên căn của q = {q}!")
        
    if xa >= q or xb >= q: 
        return mb.showerror("Lỗi Toán Học", f"Khóa riêng XA và XB bắt buộc phải nhỏ hơn q ({q})!")

    # BÊN A: Tính YA = alpha^XA mod q
    ya = pow(alpha, xa, q)
    # BÊN B: Tính YB = alpha^XB mod q
    yb = pow(alpha, xb, q) 
    
    # BÊN A: Tính K = YB^XA mod q
    ka = pow(yb, xa, q)
    # BÊN B: Tính K = YA^XB mod q
    kb = pow(ya, xb, q) 

    # --- TẠO LOG PHÂN TÍCH ---
    log_pub = " BƯỚC 1: TẠO VÀ TRAO ĐỔI KHÓA CÔNG KHAI\n" + "="*50 + "\n"
    log_pub += f"- Tham số chung: Số nguyên tố q = {q}, Nguyên căn α = {alpha}\n\n" 
    log_pub += "[ BÊN A ]:\n"
    log_pub += f" - Khóa riêng: XA = {xa}\n" 
    log_pub += f" - Tính YA = α^XA mod q = {alpha}^{xa} mod {q} = {ya}\n" 
    log_pub += f" => A gửi khóa công khai YA ({ya}) cho B qua mạng.\n\n" 
    
    log_pub += "[ BÊN B ]:\n"
    log_pub += f" - Khóa riêng: XB = {xb}\n" 
    log_pub += f" - Tính YB = α^XB mod q = {alpha}^{xb} mod {q} = {yb}\n" 
    log_pub += f" => B gửi khóa công khai YB ({yb}) cho A qua mạng.\n" 
    dh_log["PUB"] = log_pub

    log_sec = " BƯỚC 2: TÍNH TOÁN KHÓA BÍ MẬT CHUNG (K)\n" + "="*50 + "\n"
    log_sec += "[ BÊN A ]:\n"
    log_sec += f" - Nhận YB = {yb} từ B.\n" 
    log_sec += f" - Tính K = YB^XA mod q = {yb}^{xa} mod {q} = {ka}\n\n" 
    
    log_sec += "[ BÊN B ]:\n"
    log_sec += f" - Nhận YA = {ya} từ A.\n" 
    log_sec += f" - Tính K = YA^XB mod q = {ya}^{xb} mod {q} = {kb}\n\n" 
    
    if ka == kb:
        log_sec += f">>> THÀNH CÔNG! Hai bên đã đồng thuận khóa chung K = {ka}"
    else:
        log_sec += f">>> LỖI: Khóa không khớp (KA={ka}, KB={kb}). Thuật toán thất bại."
    dh_log["SEC"] = log_sec

    # --- IN KẾT QUẢ RA MÀN HÌNH ---
    out_txt = f"Khóa công khai truyền trên mạng (Kẻ gian có thể thấy):\n"
    out_txt += f" ➔ YA (Bên A) = {ya}\n ➔ YB (Bên B) = {yb}\n\n"
    out_txt += "="*40 + "\n"
    out_txt += f"Khóa bí mật chung (Chỉ A và B có thể tính được):\n"
    out_txt += f" ➔ K = {ka}\n"
    
    txt_out.delete("1.0", tk.END)
    txt_out.insert(tk.END, out_txt)
    switch_tab("PUB")

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
root.title("Trao Đổi Khóa Diffie-Hellman")
root.geometry("560x580")
root.configure(bg="#F3F4F6")

frame_left = tk.Frame(root, bg="#F3F4F6")
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
frame_right = tk.Frame(root, bg="#F3F4F6")

# --- LOGO ---
header_logo = tk.Frame(frame_left, bg="#F3F4F6")
header_logo.pack(anchor="w", fill=tk.X, pady=(0, 15))
f_logo, _ = make_shadow(header_logo, tk.Label, offset=4, shadow_bg="#047857", border="#059669", text=" D-H ", font=("Arial Black", 24, "bold"), bg="#10B981", fg="white", padx=8, pady=2)
f_logo.pack(side=tk.LEFT)
tk.Label(header_logo, text="Thuật toán trao đổi khóa (Key Exchange)", font=("Segoe UI", 9, "italic"), fg="#6B7280", bg="#F3F4F6").pack(side=tk.LEFT, padx=10, pady=6)

def add_param_input(parent, label_text, default_val):
    f = tk.Frame(parent, bg="#F3F4F6")
    f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
    tk.Label(f, text=label_text, bg="#F3F4F6", font=("Segoe UI", 9, "bold"), fg="#374151").pack(anchor="w")
    box, ent = make_shadow(f, tk.Entry, offset=2, font=("Consolas", 11, "bold"), bg="#FFFFFF", fg="#1D4ED8", justify="center")
    box.pack(fill=tk.X, pady=2)
    ent.insert(0, default_val)
    return ent

# --- THAM SỐ CHUNG Q VÀ ALPHA ---
param_frame_1 = tk.Frame(frame_left, bg="#F3F4F6")
param_frame_1.pack(fill=tk.X, pady=(0, 10))
q_ent = add_param_input(param_frame_1, "Số nguyên tố chung (q):", "353")
alpha_ent = add_param_input(param_frame_1, "Nguyên căn chung (α):", "3")

# --- KHÓA RIÊNG XA VÀ XB ---
param_frame_2 = tk.Frame(frame_left, bg="#F3F4F6")
param_frame_2.pack(fill=tk.X, pady=(0, 15))
xa_ent = add_param_input(param_frame_2, "Khóa riêng (XA - Bên A):", "97")
xb_ent = add_param_input(param_frame_2, "Khóa riêng (XB - Bên B):", "233")

# --- NÚT THỰC THI ---
btn_frame = tk.Frame(frame_left, bg="#F3F4F6")
btn_frame.pack(pady=10)

f_calc, _ = make_shadow(btn_frame, tk.Button, shadow_bg="#1D4ED8", border="#2563EB", text="TÍNH TOÁN KHÓA", bg="#3B82F6", fg="white", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=15, pady=6, command=process_dh)
f_calc.pack(side=tk.LEFT, padx=5)

f_analyze, btn_analyze = make_shadow(btn_frame, tk.Button, shadow_bg="#5B21B6", border="#6D28D9", text="PHÂN TÍCH TOÁN HỌC", bg="#8B5CF6", fg="white", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=15, pady=6, command=toggle_analysis)
f_analyze.pack(side=tk.LEFT, padx=5)

# --- KHU VỰC KẾT QUẢ ---
header_out = tk.Frame(frame_left, bg="#F3F4F6")
header_out.pack(fill=tk.X, pady=(5, 0))
tk.Label(header_out, text="Bảng điều khiển kết quả:", bg="#F3F4F6", font=("Segoe UI", 9, "bold"), fg="#374151").pack(side=tk.LEFT)

f_out, txt_out = make_shadow(frame_left, tk.Text, height=8, font=("Consolas", 10), bg="#F9FAFB")
f_out.pack(pady=3, fill=tk.X)

# --- KHUNG PHẢI: THANH ĐIỀU HƯỚNG & PHÂN TÍCH ---
tk.Label(frame_right, text="Theo dõi chi tiết thuật toán Diffie-Hellman:", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w", pady=(0, 5))

nav_frame = tk.Frame(frame_right, bg="#F3F4F6")
nav_frame.pack(fill=tk.X, pady=(0, 10))

btn_tab_pub = tk.Button(nav_frame, text="1. Trao đổi khóa", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("PUB"))
btn_tab_pub.pack(side=tk.LEFT, padx=2)
btn_tab_sec = tk.Button(nav_frame, text="2. Tính khóa bí mật K", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=lambda: switch_tab("SEC"))
btn_tab_sec.pack(side=tk.LEFT, padx=2)

f_analysis, txt_analysis = make_shadow(frame_right, tk.Text, offset=6, width=58, font=("Courier New", 10, "bold"), bg="#FFFFFF", fg="#1F2937", padx=15, pady=15)
f_analysis.pack(fill=tk.BOTH, expand=True)

root.mainloop()