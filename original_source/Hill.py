import math
import tkinter as tk
from tkinter import filedialog as fd, messagebox as mb

# --- CÁC HÀM TOÁN HỌC MA TRẬN (Pure Python) ---
def get_minor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

def get_det(m):
    if len(m) == 1: return m[0][0]
    if len(m) == 2: return m[0][0]*m[1][1] - m[0][1]*m[1][0]
    det = 0
    for c in range(len(m)):
        det += ((-1)**c) * m[0][c] * get_det(get_minor(m, 0, c))
    return det

def get_adjugate(m):
    if len(m) == 1: return [[1]]
    adj = []
    for i in range(len(m)):
        row = []
        for j in range(len(m)):
            sign = (-1)**(i+j)
            row.append(sign * get_det(get_minor(m, j, i)))
        adj.append(row)
    return adj

# --- HÀM TẠO HIỆU ỨNG ĐỔ BÓNG 3D ---
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

# --- BIẾN TOÀN CỤC ---
matrix_entries = []
is_analysis_visible = False

# --- HÀM ẨN/HIỆN BẢNG PHÂN TÍCH ---
def toggle_analysis():
    global is_analysis_visible
    if not is_analysis_visible:
        root.geometry("980x620")
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20), pady=10)
        btn_analyze.config(text="ẨN PHÂN TÍCH")
        is_analysis_visible = True
    else:
        frame_right.pack_forget()
        root.geometry("520x620")
        btn_analyze.config(text="PHÂN TÍCH")
        is_analysis_visible = False

# --- HÀM CẬP NHẬT LƯỚI MA TRẬN ---
def update_matrix_grid(event=None):
    try:
        n = int(entry_size.get().strip())
        if n < 2:
            raise ValueError
    except:
        mb.showerror("Lỗi", "Cấp ma trận phải là một số nguyên dương >= 2!")
        return
        
    if n >= 7:
        if not mb.askyesno("Cảnh báo tính toán", f"Ma trận cấp {n}x{n} yêu cầu khối lượng tính toán cực kỳ lớn (O(n!)) khi tìm nghịch đảo.\nPhần mềm có thể bị treo (Not Responding) một lúc.\nBạn có chắc chắn muốn tạo?"):
            return

    for widget in frame_matrix_grid.winfo_children():
        widget.destroy()
    matrix_entries.clear()
    
    for i in range(n):
        row_entries = []
        for j in range(n):
            e = tk.Entry(frame_matrix_grid, width=4, font=("Consolas", 12, "bold"), justify="center", bg="#FFFFFF", fg="#000000", relief="solid", borderwidth=1)
            e.grid(row=i, column=j, padx=2, pady=2)
            row_entries.append(e)
        matrix_entries.append(row_entries)

# --- XỬ LÝ THUẬT TOÁN HILL ---
def process(decrypt=False):
    t_raw = txt_in.get("1.0", tk.END).rstrip('\n')
    if not t_raw: return mb.showwarning("Lỗi", "Chưa nhập văn bản!")
    t = "".join([c.upper() for c in t_raw if c.isalpha()])
    
    try:
        K = []
        for row_entries in matrix_entries:
            row_vals = []
            for entry in row_entries:
                val = entry.get().strip()
                if not val: raise ValueError
                row_vals.append(int(val))
            K.append(row_vals)
        m = len(K)
    except:
        return mb.showerror("Lỗi", "Vui lòng nhập đầy đủ SỐ NGUYÊN vào TẤT CẢ các ô của ma trận!")
    
    det_K = get_det(K) % 26
    if math.gcd(det_K, 26) != 1:
        return mb.showerror("Lỗi Toán Học", f"Định thức Det(K) = {det_K}.\nƯCLN({det_K}, 26) != 1. Ma trận không khả nghịch trên Z26!")
    
    analysis = f" BẢNG PHÂN TÍCH {'GIẢI MÃ' if decrypt else 'MÃ HÓA'} HILL \n"
    analysis += "="*35 + "\n\n"
    analysis += f"Cấp ma trận (m) = {m}\n"
    analysis += f"Định thức Det(K) = {det_K} (Hợp lệ)\n"
    
    if decrypt:
        det_inv = pow(det_K, -1, 26)
        adj_K = get_adjugate(K)
        K_work = [[(det_inv * val) % 26 for val in row] for row in adj_K]
        analysis += f"Nghịch đảo Det(K)^-1 = {det_inv}\n"
        analysis += "Ma trận giải mã K^-1:\n"
    else:
        K_work = [[val % 26 for val in row] for row in K]
        analysis += "Ma trận mã hóa K:\n"
        
    for row in K_work:
        analysis += "  | " + "  ".join([f"{x:3d}" for x in row]) + " |\n"
    analysis += "-"*35 + "\n\n"

    # Tự động thêm đệm 'X' nếu chuỗi không chia hết cho cấp ma trận m
    if len(t) % m != 0:
        t += 'X' * (m - (len(t) % m))
        
    r = ""
    for i in range(0, len(t), m):
        block = [ord(c) - 65 for c in t[i:i+m]]
        res_block = []
        
        block_str = "[" + ", ".join(t[i:i+m]) + "]"
        analysis += f"{block_str} -> "
        
        for col in range(m):
            val = sum(block[row] * K_work[row][col] for row in range(m)) % 26
            res_block.append(val)
            r += chr(val + 65)
            
        res_str = "[" + ", ".join([chr(v + 65) for v in res_block]) + "]"
        analysis += f"{res_str}\n"

    # LOẠI BỎ KÝ TỰ 'X' ĐỆM KHI GIẢI MÃ
    if decrypt:
        r = r.rstrip('X')

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

# --- GIAO DIỆN TKINTER ---
root = tk.Tk()
root.title("Hệ Mã Hóa Hill (Nhập Cấp Ma Trận Tự Do)")
root.geometry("520x620")
root.configure(bg="#F3F4F6")

frame_left = tk.Frame(root, bg="#F3F4F6")
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)

frame_right = tk.Frame(root, bg="#F3F4F6")

# Khung Trái: Đầu vào
tk.Label(frame_left, text="Văn bản đầu vào:", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w")
f_in, txt_in = make_shadow(frame_left, tk.Text, height=3, width=45, font=("Consolas", 11), bg="#FFFFFF", fg="#000000")
f_in.pack(pady=(5, 5), fill=tk.X)
f_btn_open, btn_open = make_shadow(frame_left, tk.Button, offset=3, text="📂 Chọn File", bg="#FFFFFF", fg="#374151", activebackground="#F3F4F6", font=("Segoe UI", 9, "bold"), cursor="hand2", command=lambda: io_file(False))
f_btn_open.pack(anchor="e")

# --- KHU VỰC NHẬP CẤP MA TRẬN MỚI ---
frame_matrix_ctrl = tk.Frame(frame_left, bg="#F3F4F6")
frame_matrix_ctrl.pack(fill=tk.X, pady=(10, 5))

tk.Label(frame_matrix_ctrl, text="Nhập cấp ma trận (n):", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(side=tk.LEFT)

f_size, entry_size = make_shadow(frame_matrix_ctrl, tk.Entry, offset=2, width=5, font=("Consolas", 12, "bold"), justify="center", bg="#FFFFFF")
f_size.pack(side=tk.LEFT, padx=(5, 10))
entry_size.insert(0, "3")
entry_size.bind("<Return>", update_matrix_grid)

f_btn_gen, btn_gen = make_shadow(frame_matrix_ctrl, tk.Button, offset=2, text="Tạo Lưới", bg="#F59E0B", fg="white", activebackground="#D97706", font=("Segoe UI", 9, "bold"), cursor="hand2", command=update_matrix_grid)
f_btn_gen.pack(side=tk.LEFT)

f_matrix_wrapper, frame_matrix_grid = make_shadow(frame_left, tk.Frame, offset=4, bg="#E5E7EB")
f_matrix_wrapper.pack(pady=5)
update_matrix_grid()

# Khung Trái: Nút bấm
btn_frame = tk.Frame(frame_left, bg="#F3F4F6")
btn_frame.pack(pady=10)

f_enc, btn_enc = make_shadow(btn_frame, tk.Button, offset=4, shadow_bg="#047857", border="#059669", text="MÃ HÓA", bg="#10B981", fg="white", activebackground="#059669", activeforeground="white", font=("Segoe UI", 10, "bold"), cursor="hand2", padx=10, pady=4, command=lambda: process(False))
f_enc.pack(side=tk.LEFT, padx=5)

f_dec, btn_dec = make_shadow(btn_frame, tk.Button, offset=4, shadow_bg="#1D4ED8", border="#2563EB", text="GIẢI MÃ", bg="#3B82F6", fg="white", activebackground="#2563EB", activeforeground="white", font=("Segoe UI", 10, "bold"), cursor="hand2", padx=10, pady=4, command=lambda: process(True))
f_dec.pack(side=tk.LEFT, padx=5)

f_analyze, btn_analyze = make_shadow(btn_frame, tk.Button, offset=4, shadow_bg="#5B21B6", border="#6D28D9", text="PHÂN TÍCH", bg="#8B5CF6", fg="white", activebackground="#6D28D9", activeforeground="white", font=("Segoe UI", 10, "bold"), cursor="hand2", padx=10, pady=4, command=toggle_analysis)
f_analyze.pack(side=tk.LEFT, padx=5)

# Khung Trái: Đầu ra
tk.Label(frame_left, text="Kết quả:", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w", pady=(5, 0))
f_out, txt_out = make_shadow(frame_left, tk.Text, height=3, width=45, font=("Consolas", 11), bg="#F9FAFB", fg="#000000")
f_out.pack(pady=(5, 5), fill=tk.X)
f_btn_save, btn_save = make_shadow(frame_left, tk.Button, offset=3, text="💾 Lưu Kết Quả", bg="#FFFFFF", fg="#374151", activebackground="#F3F4F6", font=("Segoe UI", 9, "bold"), cursor="hand2", command=lambda: io_file(True))
f_btn_save.pack(anchor="e")

# Khung Phải: Bảng Phân Tích
tk.Label(frame_right, text="Giám sát luồng ma trận:", bg="#F3F4F6", font=("Segoe UI", 10, "bold"), fg="#374151").pack(anchor="w", pady=(0, 5))
f_analysis, txt_analysis = make_shadow(frame_right, tk.Text, offset=6, shadow_bg="#CBD5E1", border="#9CA3AF", height=24, width=45, font=("Courier New", 11, "bold"), bg="#FFFFFF", fg="#1F2937", padx=15, pady=15)
f_analysis.pack(fill=tk.BOTH, expand=True)
txt_analysis.insert(tk.END, "Nhấn Mã hóa/Giải mã trước, sau đó bảng phân tích sẽ hiện tại đây.")

root.mainloop()