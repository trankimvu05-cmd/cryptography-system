import tkinter as tk
from tkinter import filedialog as fd, messagebox as mb

def get_matrix():
    kw = k_ent.get().strip().upper().replace('J', 'I')
    if not kw or not kw.isalpha(): 
        mb.showerror("Lỗi", "Khóa K phải là chữ cái!")
        return None
    m = ""
    for c in kw + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c.isalpha() and c not in m: m += c
    return m

def show_matrix():
    m = get_matrix()
    if m:
        # Cắt chuỗi thành 5 hàng, sử dụng khoảng trắng rộng để tạo thành lưới vuông vức
        grid = "\n".join(["   ".join(m[i:i+5]) for i in range(0, 25, 5)])
        # Đẩy kết quả lên nhãn hiển thị trực tiếp trên giao diện
        lbl_matrix.config(text=grid)

def process(decrypt=False):
    t = txt_in.get("1.0", tk.END).strip()
    m = get_matrix()
    if not m: return
    if not t: return mb.showwarning("Lỗi", "Chưa nhập văn bản!")

    # Tách chuỗi P theo cặp, xử lý trùng lặp và chữ J
    t = "".join([c.upper() for c in t if c.isalpha()]).replace('J', 'I')
    if not decrypt:
        res, i = "", 0
        while i < len(t):
            a = t[i]
            if i + 1 < len(t):
                b = t[i + 1]
                if a == b: res += a + 'X'; i += 1
                else: res += a + b; i += 2
            else: res += a + 'X'; i += 1
        t = res
    else:
        if len(t) % 2 != 0: t += 'X'

    # Áp dụng nguyên tắc Playfair
    r, d = "", -1 if decrypt else 1
    for i in range(0, len(t), 2):
        r1, c1 = m.index(t[i]) // 5, m.index(t[i]) % 5
        r2, c2 = m.index(t[i+1]) // 5, m.index(t[i+1]) % 5
        
        if r1 == r2: r += m[r1*5 + (c1+d)%5] + m[r2*5 + (c2+d)%5]
        elif c1 == c2: r += m[((r1+d)%5)*5 + c1] + m[((r2+d)%5)*5 + c2]
        else: r += m[r1*5 + c2] + m[r2*5 + c1]
            
    txt_out.delete("1.0", tk.END)
    txt_out.insert(tk.END, r)
    
    # Tự động cập nhật bảng mã lên màn hình mỗi khi mã hóa/giải mã
    show_matrix()

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

# Giao diện Tkinter
root = tk.Tk()
root.title("Mã Hóa Playfair (Hiển thị bảng mã trực tiếp)")

tk.Label(root, text="Văn bản đầu vào:").pack()
txt_in = tk.Text(root, height=5, width=70); txt_in.pack()
tk.Button(root, text="Chọn File", command=lambda: io_file(False)).pack(pady=5)

tk.Label(root, text="Từ khóa K (Keyword - VD: MINH):").pack()
k_ent = tk.Entry(root, width=30); k_ent.pack()
k_ent.insert(0, "MINH")

f = tk.Frame(root); f.pack(pady=10)
tk.Button(f, text="Mã Hóa", bg="#4CAF50", fg="white", command=lambda: process(False)).pack(side=tk.LEFT, padx=5)
tk.Button(f, text="Giải Mã", bg="#2196F3", fg="white", command=lambda: process(True)).pack(side=tk.LEFT, padx=5)
tk.Button(f, text="Cập nhật Bảng mã", bg="#FF9800", fg="white", command=show_matrix).pack(side=tk.LEFT, padx=5)

# Khu vực hiển thị bảng mã trực tiếp trên giao diện
tk.Label(root, text="Bảng mã 5x5:", font=("Arial", 10, "bold"), fg="#555").pack()
# Dùng font "Courier" (monospaced) để các cột chữ cái xếp thẳng hàng nhau
lbl_matrix = tk.Label(root, text="[Bảng mã trống]", font=("Courier", 14, "bold"), fg="#D32F2F")
lbl_matrix.pack(pady=5)

tk.Label(root, text="Kết quả:").pack()
txt_out = tk.Text(root, height=5, width=70); txt_out.pack()
tk.Button(root, text="Lưu Kết Quả", command=lambda: io_file(True)).pack(pady=5)

# Hiển thị sẵn bảng mã mặc định ngay khi mở app
show_matrix()

root.mainloop()