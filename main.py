"""
═══════════════════════════════════════════════════════
CYBER SECURITY DASHBOARD — Main Entry Point
Khởi chạy hệ thống giao diện MVC 9 Hệ Mật Mã
═══════════════════════════════════════════════════════
"""

import sys
import os

# Thêm đường dẫn thư mục gốc vào sys.path để import tương đối/tuyệt đối chuẩn mực
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import customtkinter as ctk
from views.app import MainApp

def main():
    # Cấu hình theme CustomTkinter
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # Khởi tạo và chạy giao diện
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()
