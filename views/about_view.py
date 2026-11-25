"""About — Trang giới thiệu phần mềm"""

import customtkinter as ctk
from views.theme import *
from views.components import CyberCard


class AboutView(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = CyberCard(self)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ctk.CTkLabel(
            header, text="ℹ️  GIỚI THIỆU PHẦN MỀM",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_TITLE_SIZE, weight="bold"),
            text_color=NEON_PURPLE
        ).pack(anchor="w", padx=18, pady=(12, 2))
        ctk.CTkLabel(
            header, text="Cryptography System — Hệ thống mã hóa và giải mã 9 thuật toán mật mã",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", padx=18, pady=(0, 12))

        # Content
        content = CyberCard(self)
        content.grid(row=1, column=0, sticky="nsew")

        scroll = ctk.CTkScrollableFrame(
            content, fg_color="transparent",
            scrollbar_button_color=BORDER_DEFAULT,
            scrollbar_button_hover_color=NEON_CYAN
        )
        scroll.pack(fill="both", expand=True, padx=15, pady=15)

        sections = [
            ("🛡️ Tổng quan", (
                "Cryptography System là phần mềm tích hợp 9 hệ mật mã, "
                "từ cổ điển đến hiện đại. Giao diện được thiết kế theo phong cách "
                "Cyber Security Dashboard — hiện đại, chuyên nghiệp và trực quan."
            )),
            ("📚 9 Hệ Mật Mã", (
                "1. Caesar Cipher — Mã hóa dịch chuyển vòng tròn\n"
                "2. Affine Cipher — Kết hợp phép nhân và dịch chuyển\n"
                "3. Hill Cipher — Mã hóa bằng ma trận NxN\n"
                "4. Vigenère Cipher — Khóa tuần hoàn đa bảng chữ cái\n"
                "5. Playfair Cipher — Ma trận khóa 5×5 theo cặp\n"
                "6. Hoán Vị Hàng — Hoán vị cột theo khóa dãy số\n"
                "7. DES — Mã khối Feistel 64-bit tiêu chuẩn\n"
                "8. RSA — Mã hóa khóa công khai bất đối xứng\n"
                "9. Diffie-Hellman — Trao đổi khóa bí mật"
            )),
            ("⚙️ Kiến Trúc", (
                "Chương trình được tổ chức theo mô hình MVC:\n"
                "• Model — Thuật toán thuần túy của 9 hệ mật mã\n"
                "• View — Giao diện Cyber Security Dashboard (CustomTkinter)\n"
                "• Controller — Kết nối giao diện với thuật toán"
            )),
            ("🎨 Công Nghệ", (
                "• Ngôn ngữ: Python\n"
                "• GUI Framework: CustomTkinter\n"
                "• Phong cách: Cyber Security Dashboard\n"
                "• Tông màu: Navy, Tím, Cyan neon"
            )),
            ("👨‍💻 Tác Giả", (
                "Phần mềm được phát triển phục vụ mục đích học tập "
                "và nghiên cứu về Mật mã học (Cryptography)."
            )),
        ]

        for title, body in sections:
            ctk.CTkLabel(
                scroll, text=title,
                font=ctk.CTkFont(
                    family=FONT_FAMILY, size=FONT_SUBTITLE, weight="bold"
                ),
                text_color=NEON_CYAN
            ).pack(anchor="w", pady=(15, 5))

            ctk.CTkLabel(
                scroll, text=body,
                font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY),
                text_color=TEXT_PRIMARY,
                justify="left", wraplength=700
            ).pack(anchor="w", padx=10)
