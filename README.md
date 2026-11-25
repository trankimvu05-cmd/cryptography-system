# 🛡️ CRYPTOGRAPHY SYSTEM — CYBER SECURITY DASHBOARD

Hệ thống mã hóa và giải mã 9 thuật toán mật mã bằng Python, được tái cấu trúc theo mô hình chuẩn **MVC (Model - View - Controller)** và giao diện hiện đại **Cyber Security Dashboard**.

---

## 🚀 Tính năng nổi bật

1. **Bảo toàn 100% Thuật toán**:
   - Caesar, Affine, Hill, Vigenère, Playfair, Hoán Vị Hàng, DES, RSA, Diffie-Hellman.
   - Giữ nguyên công thức, bước mã hóa, giải mã và hiển thị bảng phân tích.

2. **Kiến trúc MVC**:
   - `models/`: Chứa các hàm nghiệp vụ toán học thuần túy (pure functions).
   - `views/`: Giao diện CustomTkinter Cyber Security (Dark theme, Navy, Neon Cyan, Neon Purple, bo góc, hover button, gradient cards).
   - `controllers/`: Kiểm tra tính hợp lệ dữ liệu (validation) và điều hướng gọi Model.

3. **Giao diện Cyber Security Dashboard**:
   - **Dashboard (Trang chủ)**: Thống kê số lượng thuật toán, phân loại (Cổ điển, Hoán vị, Hiện đại), 9 Cyber Cards có hiệu ứng di chuột và chọn nhanh.
   - **Sidebar bên trái**: Điều hướng nhanh giữa các thuật toán và nút quay về Trang chủ.
   - **Trang chi tiết thuật toán**: Trường nhập khóa được thiết kế chuyên biệt cho từng thuật toán (Hill: lưới ma trận tùy chọn kích thước, RSA: p, q, e, DES: khóa 64-bit Hex, DH: q, alpha, XA, XB).
   - **Bảng phân tích (Analysis Panel)**: Hiển thị chi tiết các bước tính toán (Ma trận K^-1, 16 vòng DES, thông số khóa RSA, trao đổi khóa Diffie-Hellman).
   - **Tiện ích**: Đọc file văn bản, lưu file kết quả, sao chép kết quả một chạm (Clipboard), làm mới.

---

## 📁 Cấu trúc thư mục

```
CRYPTOGRAPHY_SYSTEM/
│
├── main.py                      # File khởi chạy ứng dụng
├── requirements.txt             # Thư viện phụ thuộc
│
├── models/                      # MODEL: Thuật toán mật mã thuần túy
│   ├── caesar.py
│   ├── affine.py
│   ├── hill.py
│   ├── vigenere.py
│   ├── playfair.py
│   ├── hang.py
│   ├── des.py
│   ├── rsa.py
│   └── diffie_hellman.py
│
├── views/                       # VIEW: Giao diện Cyber Security Dashboard
│   ├── app.py                   # Cửa sổ chính & điều hướng Sidebar
│   ├── theme.py                 # Hệ thống màu sắc, font chữ Cyber Security
│   ├── components.py            # CyberCard, NeonButton, GlowEntry...
│   ├── cipher_view_base.py      # Lớp cha chuẩn hóa cho giao diện cipher
│   ├── dashboard.py             # Trang chủ Dashboard
│   ├── about_view.py            # Trang giới thiệu hệ thống
│   ├── caesar_view.py
│   ├── affine_view.py
│   ├── hill_view.py
│   ├── vigenere_view.py
│   ├── playfair_view.py
│   ├── hang_view.py
│   ├── des_view.py
│   ├── rsa_view.py
│   └── dh_view.py
│
├── controllers/                 # CONTROLLER: Validate & cầu nối View - Model
│   └── cipher_controller.py
│
└── original_source/             # Source code gốc được backup an toàn
```

---

## 🛠️ Hướng dẫn cài đặt & khởi chạy

### 1. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```
*(Yêu cầu `customtkinter`)*

### 2. Khởi chạy phần mềm:
```bash
python main.py
```
Hoặc mở thư mục `CRYPTOGRAPHY_SYSTEM` trong Visual Studio Code và ấn F5 (Run `main.py`).
