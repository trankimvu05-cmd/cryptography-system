import math
import tkinter as tk
from tkinter import filedialog as fd, messagebox as mb

# --- HÀM TẠO HIỆU ỨNG ĐỔ BÓNG 3D ---
def make_shadow(parent, w_class, offset=4, shadow_bg="#D1D5DB", border="#E5E7EB", **kwargs):
    # Khung chứa chính
    f = tk.Frame(parent, bg="#F3F4F6")
    
    # Khung mặt trước (đóng vai trò làm viền mỏng)
    front = tk.Frame(f, bg=border, padx=1, pady=1)
    front.pack(padx=(0, offset), pady=(0, offset), fill=tk.BOTH, expand=True)
    
    # Loại bỏ viền mặc định kỹ thuật số của Tkinter để tạo giao diện phẳng
    kwargs.setdefault('relief', 'flat')
    kwargs.setdefault('borderwidth', 0)
    kwargs.setdefault('highlightthickness', 0)
    
    # Tạo Widget thực tế (Nút bấm, Ô chữ...)
    w = w_class(front, **kwargs)
    w.pack(fill=tk.BOTH, expand=True)
    
    # Khung đổ bóng đặt lùi về sau
    s = tk.Frame(f, bg=shadow_bg)
    s.place(x=offset, y=offset, relwidth=1, relheight=1, width=-offset, height=-offset)
    s.lower() # Đẩy khung bóng xuống lớp dưới cùng
    
    return f, w

# --- XỬ LÝ THUẬT TOÁN ---
def process(decrypt=False):
    t = txt_in.get("1.0", tk.END).rstrip('\n')
    if not t: return mb.showwarning("Lỗi", "Chưa nhập văn bản!")
    
    try: 
        k = [int(x) for x in k_ent.get().replace(',', ' ').split()]
        if not k: raise ValueError
    except: 
        return mb.showerror("Lỗi", "Khóa phải là dãy số !")
    
    m = len(k)
    
    # Tiêu đề bảng phân tích
    analysis = f" BẢNG PHÂN TÍCH {'GIẢI MÃ' if decrypt else 'MÃ HÓA'}\n"
    analysis += "="*35 + "\n\n"
    analysis += "Khóa K (Cột):  " + "   ".join(map(str, k)) + "\n"
    analysis += "-" * (m * 4 + 13) + "\n"

    if decrypt:
        base_len = len(t) // m
        rem = len(t) % m
        lengths = [base_len + 1 if i < rem else base_len for i in range(m)]
        sorted_indices = [i for _, i in sorted(zip(k, range(m)))]
        
        cols = {}
        pos = 0
        for idx in sorted_indices:
            cols[idx] = t[pos : pos + lengths[idx]]
            pos += lengths[idx]
            
        r = ""
        rows = math.ceil(len(t) / m)
        for row in range(rows):
            row_str = "               "
            for i in range(m):
                if row < len(cols[i]):
                    char = cols[i][row]
                    r += char
                    row_str += char + "   "
                else:
                    row_str += "*   " 
            analysis += row_str + "\n"
            

    else:
        rows = math.ceil(len(t) / m)
        for row in range(rows):
            row_str = "               "
            for col in range(m):
                idx = row * m + col
                row_str += (t[idx] if idx < len(t) else "*") + "   "
            analysis += row_str + "\n"
            
        cols_str = [t[i::m] for i in range(m)]
        sorted_cols = [col for _, col in sorted(zip(k, cols_str))]
        r = "".join(sorted_cols)
        
        
    txt_out.delete("1.0", tk.END)
    txt_out.insert(tk.END, r)
    
    txt_analysis.delete("1.0", tk.END)
    txt_analysis.insert(tk.END, analysis)

def io_file(save=False):
    try:
        if save:
            p = fd.asksaveasfilename(defaultextension=".txt")
            if p: open(p, "w", encoding="utf-8").write(txt_out.get("1.0", tk.END).strip())
        else:
            p = fd.askopenfilename()
            if p: 
                txt_in.delete("1.0", tk.END)
                txt_in.insert(tk.END, open(p, "r", encoding="utf-8").read())
    except Exception as e: mb.showerror("Lỗi", str(e))

# --- GIAO DIỆN TKINTER HIỆN ĐẠI ---
root = tk.Tk()
root.title("Hệ Mã Hàng")
root.geometry("950x520")
root.configure(bg="#F3F4F6")

# Chia 2 cột layout
frame_left = tk.Frame(root, bg="#F3F4F6")
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

frame_right = tk.Frame(root, bg="#F3F4F6")
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=20)

# --- KHUNG BÊN TRÁI (THAO TÁC) ---
tk.Label(frame_left, text="Văn bản đầu vào:", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w")
f_in, txt_in = make_shadow(frame_left, tk.Text, height=4, width=45, font=("Consolas", 11), bg="#FFFFFF", fg="#000000")
f_in.pack(pady=(5, 5), fill=tk.X)

f_btn_open, btn_open = make_shadow(frame_left, tk.Button, offset=3, text="📂 Chọn File", bg="#FFFFFF", fg="#374151", activebackground="#F3F4F6", font=("Segoe UI", 9, "bold"), cursor="hand2", command=lambda: io_file(False))
f_btn_open.pack(anchor="e")

tk.Label(frame_left, text="Khóa K (Dãy số cách nhau bởi dấu phẩy):", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w", pady=(10,0))
f_k, k_ent = make_shadow(frame_left, tk.Entry, font=("Consolas", 12), bg="#FFFFFF", fg="#000000")
f_k.pack(pady=(5, 10), fill=tk.X)
k_ent.insert(0, "3, 6, 2, 1, 5, 4")

# Khu vực nút bấm có màu đổ bóng riêng
btn_frame = tk.Frame(frame_left, bg="#F3F4F6")
btn_frame.pack(pady=10)

f_enc, btn_enc = make_shadow(btn_frame, tk.Button, offset=4, shadow_bg="#047857", border="#059669", text="MÃ HÓA", bg="#10B981", fg="white", activebackground="#059669", activeforeground="white", font=("Segoe UI", 11, "bold"), cursor="hand2", padx=15, pady=4, command=lambda: process(False))
f_enc.pack(side=tk.LEFT, padx=10)

f_dec, btn_dec = make_shadow(btn_frame, tk.Button, offset=4, shadow_bg="#1D4ED8", border="#2563EB", text="GIẢI MÃ", bg="#3B82F6", fg="white", activebackground="#2563EB", activeforeground="white", font=("Segoe UI", 11, "bold"), cursor="hand2", padx=15, pady=4, command=lambda: process(True))
f_dec.pack(side=tk.LEFT, padx=10)

tk.Label(frame_left, text="Kết quả:", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w", pady=(5, 0))
f_out, txt_out = make_shadow(frame_left, tk.Text, height=4, width=45, font=("Consolas", 11), bg="#F9FAFB", fg="#000000")
f_out.pack(pady=(5, 5), fill=tk.X)

f_btn_save, btn_save = make_shadow(frame_left, tk.Button, offset=3, text="💾 Lưu Kết Quả", bg="#FFFFFF", fg="#374151", activebackground="#F3F4F6", font=("Segoe UI", 9, "bold"), cursor="hand2", command=lambda: io_file(True))
f_btn_save.pack(anchor="e")

# --- KHUNG BÊN PHẢI (BẢNG PHÂN TÍCH) ---
tk.Label(frame_right, text="Bảng Phân Tích (Hoán Vị Cột):", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w", pady=(0, 5))

# Ô phân tích nền trắng, viền mỏng xám và đổ bóng đậm hơn một chút
f_analysis, txt_analysis = make_shadow(frame_right, tk.Text, offset=6, shadow_bg="#CBD5E1", border="#9CA3AF", height=22, width=45, font=("Courier New", 11, "bold"), bg="#FFFFFF", fg="#1F2937", padx=15, pady=15)
f_analysis.pack(fill=tk.BOTH, expand=True)
txt_analysis.insert(tk.END, "Mã hóa/Giải mã")

root.mainloop()