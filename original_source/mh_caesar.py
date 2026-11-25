import tkinter as tk
from tkinter import filedialog, messagebox


def lay_khoa():
    try:
        return int(nhap_khoa.get()) % 26
    except ValueError:
        messagebox.showerror("Lỗi", "Khóa K phải là số nguyên!")
        return None


def ma_hoa():
    text = nhap_text.get()
    k = lay_khoa()

    if text == "":
        messagebox.showwarning("Thông báo", "Vui lòng nhập văn bản!")
        return

    if k is None:
        return

    ket_qua = ""

    for c in text:
        if c.isupper():
            ket_qua += chr((ord(c) - ord("A") + k) % 26 + ord("A"))
        elif c.islower():
            ket_qua += chr((ord(c) - ord("a") + k) % 26 + ord("a"))
        else:
            ket_qua += c

    hien_thi(ket_qua)
    thong_ke(ket_qua)


def giai_ma():
    text = nhap_text.get()
    k = lay_khoa()

    if text == "":
        messagebox.showwarning("Thông báo", "Vui lòng nhập văn bản!")
        return

    if k is None:
        return

    ket_qua = ""

    for c in text:
        if c.isupper():
            ket_qua += chr((ord(c) - ord("A") - k) % 26 + ord("A"))
        elif c.islower():
            ket_qua += chr((ord(c) - ord("a") - k) % 26 + ord("a"))
        else:
            ket_qua += c

    hien_thi(ket_qua)
    thong_ke(ket_qua)


def hien_thi(text):
    ket_qua_text.delete(0, tk.END)
    ket_qua_text.insert(0, text)


def xoa():
    nhap_text.delete(0, tk.END)
    nhap_khoa.delete(0, tk.END)
    ket_qua_text.delete(0, tk.END)
    thong_ke_label.config(text="Thống kê: Chưa có dữ liệu")


def mo_file():
    file_path = filedialog.askopenfilename(
        title="Chọn file văn bản",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path == "":
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        nhap_text.delete(0, tk.END)
        nhap_text.insert(0, text)

    except Exception as e:
        messagebox.showerror("Lỗi", "Không thể đọc file!\n" + str(e))


def luu_file():
    text = ket_qua_text.get()

    if text == "":
        messagebox.showwarning("Thông báo", "Chưa có kết quả để lưu!")
        return

    file_path = filedialog.asksaveasfilename(
        title="Lưu kết quả",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path == "":
        return

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

        messagebox.showinfo("Thông báo", "Đã lưu file thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", "Không thể lưu file!\n" + str(e))


def sao_chep():
    text = ket_qua_text.get()

    if text == "":
        messagebox.showwarning("Thông báo", "Chưa có kết quả để sao chép!")
        return

    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()
    messagebox.showinfo("Thông báo", "Đã sao chép kết quả!")


def thong_ke(text):
    chu_cai = 0
    chu_hoa = 0
    chu_thuong = 0
    chu_so = 0
    khoang_trang = 0
    ky_tu_dac_biet = 0

    for c in text:
        if c.isalpha():
            chu_cai += 1
            if c.isupper():
                chu_hoa += 1
            else:
                chu_thuong += 1
        elif c.isdigit():
            chu_so += 1
        elif c.isspace():
            khoang_trang += 1
        else:
            ky_tu_dac_biet += 1

    thong_ke_label.config(
        text="Thống kê: Độ dài = " + str(len(text))
        + " | Chữ cái = " + str(chu_cai)
        + " | Hoa = " + str(chu_hoa)
        + " | Thường = " + str(chu_thuong)
        + " | Số = " + str(chu_so)
        + " | Khoảng trắng = " + str(khoang_trang)
        + " | Ký tự đặc biệt = " + str(ky_tu_dac_biet)
    )


window = tk.Tk()
window.title("MA HOA Caesar")
window.geometry("650x420")
window.resizable(False, False)

tk.Label(
    window,
    text="CHƯƠNG TRÌNH MÃ HÓA CAESAR",
    font=("Arial", 16, "bold")
).pack(pady=12)


tk.Label(
    window,
    text="NHẬP VĂN BẢN:"
).pack()

nhap_text = tk.Entry(window, width=75)
nhap_text.pack(pady=5)


tk.Label(
    window,
    text="KHÓA K:"
).pack()

nhap_khoa = tk.Entry(
    window,
    width=15,
    justify="center"
)
nhap_khoa.pack(pady=5)


frame1 = tk.Frame(window)
frame1.pack(pady=8)

tk.Button(
    frame1,
    text="MỞ FILE",
    width=12,
    command=mo_file
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frame1,
    text="MÃ HÓA",
    width=12,
    command=ma_hoa
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frame1,
    text="GIẢI MÃ",
    width=12,
    command=giai_ma
).pack(side=tk.LEFT, padx=5)


tk.Label(
    window,
    text="KẾT QUẢ:"
).pack()

ket_qua_text = tk.Entry(window, width=75)
ket_qua_text.pack(pady=5)


frame2 = tk.Frame(window)
frame2.pack(pady=8)

tk.Button(
    frame2,
    text="LƯU FILE",
    width=12,
    command=luu_file
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frame2,
    text="SAO CHÉP",
    width=12,
    command=sao_chep
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frame2,
    text="XÓA",
    width=12,
    command=xoa
).pack(side=tk.LEFT, padx=5)

tk.Button(
    frame2,
    text="THOÁT",
    width=12,
    command=window.destroy
).pack(side=tk.LEFT, padx=5)


thong_ke_label = tk.Label(
    window,
    text="Thống kê: Chưa có dữ liệu",
    wraplength=600
)
thong_ke_label.pack(pady=10)


window.mainloop()
