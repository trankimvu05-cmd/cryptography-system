import tkinter as tk
from tkinter import filedialog, messagebox
import math


def lay_khoa():
    try:
        a = int(nhap_a.get())
        b = int(nhap_b.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Khóa a và b phải là số nguyên!")
        return None, None

    if math.gcd(a, 26) != 1:
        messagebox.showerror(
            "Lỗi",
            "Khóa a không hợp lệ!\n"
            "Phải có UCLN(a, 26) = 1."
        )
        return None, None

    a = a % 26
    b = b % 26

    return a, b


def tim_nghich_dao(a):
    for i in range(26):
        if (a * i) % 26 == 1:
            return i
    return None


def ma_hoa():
    text = nhap_text.get()
    a, b = lay_khoa()

    if text == "":
        messagebox.showwarning("Thông báo", "Vui lòng nhập văn bản!")
        return

    if a is None:
        return

    ket_qua = ""

    for c in text:
        if c.isupper():
            x = ord(c) - ord('A')
            y = (a * x + b) % 26
            ket_qua += chr(y + ord('A'))

        elif c.islower():
            x = ord(c) - ord('a')
            y = (a * x + b) % 26
            ket_qua += chr(y + ord('a'))

        else:
            ket_qua += c

    hien_thi(ket_qua)
    thong_ke(ket_qua)


def giai_ma():
    text = nhap_text.get()
    a, b = lay_khoa()

    if text == "":
        messagebox.showwarning("Thông báo", "Vui lòng nhập văn bản!")
        return

    if a is None:
        return

    a_nghich_dao = tim_nghich_dao(a)

    if a_nghich_dao is None:
        messagebox.showerror("Lỗi", "Không tìm được nghịch đảo của a!")
        return

    ket_qua = ""

    for c in text:
        if c.isupper():
            y = ord(c) - ord('A')
            x = (a_nghich_dao * (y - b)) % 26
            ket_qua += chr(x + ord('A'))

        elif c.islower():
            y = ord(c) - ord('a')
            x = (a_nghich_dao * (y - b)) % 26
            ket_qua += chr(x + ord('a'))

        else:
            ket_qua += c

    hien_thi(ket_qua)
    thong_ke(ket_qua)


def hien_thi(text):
    ket_qua_text.delete(0, tk.END)
    ket_qua_text.insert(0, text)


def xoa():
    nhap_text.delete(0, tk.END)
    nhap_a.delete(0, tk.END)
    nhap_b.delete(0, tk.END)
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
        messagebox.showerror(
            "Lỗi",
            "Không thể đọc file!\n" + str(e)
        )


def luu_file():
    text = ket_qua_text.get()

    if text == "":
        messagebox.showwarning(
            "Thông báo",
            "Chưa có kết quả để lưu!"
        )
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

        messagebox.showinfo(
            "Thông báo",
            "Đã lưu file thành công!"
        )

    except Exception as e:
        messagebox.showerror(
            "Lỗi",
            "Không thể lưu file!\n" + str(e)
        )


def sao_chep():
    text = ket_qua_text.get()

    if text == "":
        messagebox.showwarning(
            "Thông báo",
            "Chưa có kết quả để sao chép!"
        )
        return

    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()

    messagebox.showinfo(
        "Thông báo",
        "Đã sao chép kết quả!"
    )


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
window.title("MÃ HÓA Affine")
window.geometry("650x450")
window.resizable(False, False)


tk.Label(
    window,
    text="CHƯƠNG TRÌNH MÃ HÓA AFFINE",
    font=("Arial", 16, "bold")
).pack(pady=12)


tk.Label(
    window,
    text="NHẬP VĂN BẢN:"
).pack()

nhap_text = tk.Entry(window, width=75)
nhap_text.pack(pady=5)


frame_khoa = tk.Frame(window)
frame_khoa.pack(pady=5)

tk.Label(
    frame_khoa,
    text="KHÓA a:"
).pack(side=tk.LEFT, padx=5)

nhap_a = tk.Entry(
    frame_khoa,
    width=10,
    justify="center"
)
nhap_a.pack(side=tk.LEFT, padx=5)

tk.Label(
    frame_khoa,
    text="KHÓA b:"
).pack(side=tk.LEFT, padx=5)

nhap_b = tk.Entry(
    frame_khoa,
    width=10,
    justify="center"
)
nhap_b.pack(side=tk.LEFT, padx=5)


tk.Label(
    window,
    text="Điều kiện: UCLN(a, 26) = 1"
).pack(pady=3)


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
