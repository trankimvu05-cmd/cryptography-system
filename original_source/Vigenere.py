import os
import tkinter as tk
from tkinter import filedialog, messagebox

# ==========================================
# THUẬT TOÁN MÃ HÓA VIGENÈRE
# ==========================================
def ma_hoa_vigenere(text, khoa):
    ket_qua = []
    khoa = khoa.upper()
    khoa_idx = 0
    
    for c in text:
        if c.isalpha():
            ascii_offset = ord('A') if c.isupper() else ord('a')
            k_char = khoa[khoa_idx % len(khoa)]
            k_shift = ord(k_char) - ord('A')
            
            # Công thức mã hóa: C = (P + K) mod 26
            ma_hoa_char = chr((ord(c) - ascii_offset + k_shift) % 26 + ascii_offset)
            ket_qua.append(ma_hoa_char)
            khoa_idx += 1
        else:
            ket_qua.append(c)
            
    return "".join(ket_qua)

def giai_ma_vigenere(text, khoa):
    ket_qua = []
    khoa = khoa.upper()
    khoa_idx = 0
    
    for c in text:
        if c.isalpha():
            ascii_offset = ord('A') if c.isupper() else ord('a')
            k_char = khoa[khoa_idx % len(khoa)]
            k_shift = ord(k_char) - ord('A')
            
            # Công thức giải mã: P = (C - K) mod 26
            giai_ma_char = chr((ord(c) - ascii_offset - k_shift) % 26 + ascii_offset)
            ket_qua.append(giai_ma_char)
            khoa_idx += 1
        else:
            ket_qua.append(c)
            
    return "".join(ket_qua)

# ==========================================
# GIAO DIỆN GUI (TKINTER) GIỐNG MẪU CAESAR
# ==========================================
class AppVigenereGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MA HOA Vigenere")
        self.root.geometry("600x420")
        self.root.resizable(False, False)

        # Tiêu đề lớn
        lbl_title = tk.Label(root, text="CHƯƠNG TRÌNH MÃ HÓA VIGENÈRE", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=15)

        # Nhập Văn Bản
        tk.Label(root, text="NHẬP VĂN BẢN:", font=("Arial", 9)).pack(pady=(5, 2))
        self.txt_input = tk.Entry(root, width=70, font=("Arial", 10))
        self.txt_input.pack(pady=2)

        # Khóa K (Vigenère dùng khóa chữ nên ô nhập rộng hơn mẫu Caesar một chút cho dễ nhìn)
        tk.Label(root, text="KHÓA K:", font=("Arial", 9)).pack(pady=(8, 2))
        self.txt_key = tk.Entry(root, width=30, font=("Arial", 10), justify="center")
        self.txt_key.pack(pady=2)

        # Hàng nút chức năng 1: Mở File, Mã Hóa, Giải Mã
        f1 = tk.Frame(root)
        f1.pack(pady=12)
        tk.Button(f1, text="MỞ FILE", width=12, command=self.mo_file).grid(row=0, column=0, padx=10)
        tk.Button(f1, text="MÃ HÓA", width=12, command=self.xu_ly_ma_hoa).grid(row=0, column=1, padx=10)
        tk.Button(f1, text="GIẢI MÃ", width=12, command=self.xu_ly_giai_ma).grid(row=0, column=2, padx=10)

        # Kết Quả
        tk.Label(root, text="KẾT QUẢ:", font=("Arial", 9)).pack(pady=(5, 2))
        self.txt_output = tk.Entry(root, width=70, font=("Arial", 10))
        self.txt_output.pack(pady=2)

        # Hàng nút chức năng 2: Lưu File, Sao Chép, Xóa, Thoát
        f2 = tk.Frame(root)
        f2.pack(pady=12)
        tk.Button(f2, text="LƯU FILE", width=10, command=self.luu_file).grid(row=0, column=0, padx=8)
        tk.Button(f2, text="SAO CHÉP", width=10, command=self.sao_chep).grid(row=0, column=1, padx=8)
        tk.Button(f2, text="XÓA", width=10, command=self.xoa).grid(row=0, column=2, padx=8)
        tk.Button(f2, text="THOÁT", width=10, command=root.quit).grid(row=0, column=3, padx=8)

        # Dòng thống kê ở dưới cùng
        self.lbl_thong_ke = tk.Label(root, text="Thống kê: Chưa có dữ liệu", font=("Arial", 9))
        self.lbl_thong_ke.pack(pady=5)

    def xoa(self):
        self.txt_input.delete(0, tk.END)
        self.txt_key.delete(0, tk.END)
        self.txt_output.delete(0, tk.END)
        self.lbl_thong_ke.config(text="Thống kê: Chưa có dữ liệu")

    def sao_chep(self):
        res = self.txt_output.get()
        if res:
            self.root.clipboard_clear()
            self.root.clipboard_append(res)
            messagebox.showinfo("Thông báo", "Đã sao chép kết quả vào bộ nhớ tạm!")
        else:
            messagebox.showwarning("Cảnh báo", "Không có kết quả để sao chép!")

    def mo_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.txt_input.delete(0, tk.END)
                    self.txt_input.insert(0, f.read())
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở file: {e}")

    def luu_file(self):
        res = self.txt_output.get()
        if res:
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if path:
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(res)
                    messagebox.showinfo("Thông báo", "Lưu file thành công!")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Không có nội dung kết quả để lưu!")

    def xu_ly_ma_hoa(self):
        text = self.txt_input.get()
        key = self.txt_key.get()
        if not text or not key:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ văn bản và khóa K!")
            return
        if not key.isalpha():
            messagebox.showwarning("Lỗi", "Khóa K của Vigenère phải là các ký tự chữ cái (A-Z)!")
            return

        res = ma_hoa_vigenere(text, key)
        self.txt_output.delete(0, tk.END)
        self.txt_output.insert(0, res)
        self.lbl_thong_ke.config(text=f"Thống kê: Đã mã hóa thành công ({len(text)} ký tự).")

    def xu_ly_giai_ma(self):
        text = self.txt_input.get()
        key = self.txt_key.get()
        if not text or not key:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ văn bản và khóa K!")
            return
        if not key.isalpha():
            messagebox.showwarning("Lỗi", "Khóa K của Vigenère phải là các ký tự chữ cái (A-Z)!")
            return

        res = giai_ma_vigenere(text, key)
        self.txt_output.delete(0, tk.END)
        self.txt_output.insert(0, res)
        self.lbl_thong_ke.config(text=f"Thống kê: Giải mã hoàn tất ({len(text)} ký tự).")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppVigenereGUI(root)
    root.mainloop()

