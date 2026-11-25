"""Dashboard — Trang chủ với 9 thẻ chức năng"""

import customtkinter as ctk
from views.theme import *
from views.components import CyberCard, DashboardCipherCard


class DashboardView(ctk.CTkFrame):

    def __init__(self, master, on_select_cipher=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_select = on_select_cipher

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ─── HERO HEADER ───
        hero = CyberCard(self)
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        hero_inner = ctk.CTkFrame(hero, fg_color="transparent")
        hero_inner.pack(fill="x", padx=25, pady=20)

        ctk.CTkLabel(
            hero_inner, text="🛡️  CRYPTOGRAPHY SYSTEM",
            font=ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold"),
            text_color=NEON_CYAN
        ).pack(anchor="w")

        ctk.CTkLabel(
            hero_inner,
            text="Hệ thống mã hóa và giải mã 9 thuật toán mật mã",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SUBTITLE),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", pady=(4, 0))

        desc = (
            "Phần mềm tích hợp 9 hệ mật mã từ cổ điển đến hiện đại, "
            "bao gồm: Caesar, Affine, Hill, Vigenère, Playfair, Hoán Vị Hàng, "
            "DES, RSA và Diffie-Hellman. Hỗ trợ mã hóa, giải mã, phân tích "
            "thuật toán và trực quan hóa quá trình xử lý."
        )
        ctk.CTkLabel(
            hero_inner, text=desc,
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
            text_color=TEXT_DIM, wraplength=800, justify="left"
        ).pack(anchor="w", pady=(8, 0))

        # ─── STATS BAR ───
        stats = CyberCard(self)
        stats.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        stats_inner = ctk.CTkFrame(stats, fg_color="transparent")
        stats_inner.pack(fill="x", padx=25, pady=12)

        stat_data = [
            ("🔐", "9", "Thuật toán", NEON_CYAN),
            ("⚡", "5", "Mật mã cổ điển", NEON_PURPLE),
            ("🔒", "3", "Mật mã hiện đại", NEON_GREEN),
            ("🤝", "1", "Trao đổi khóa", NEON_GOLD),
            ("📊", "4", "Có bảng phân tích", NEON_BLUE),
        ]
        for icon, num, label, color in stat_data:
            sf = ctk.CTkFrame(stats_inner, fg_color="transparent")
            sf.pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(
                sf, text=f"{icon}  {num}",
                font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"),
                text_color=color
            ).pack()
            ctk.CTkLabel(
                sf, text=label,
                font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
                text_color=TEXT_SECONDARY
            ).pack()

        # ─── CIPHER GRID (3x3) ───
        grid_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=BORDER_DEFAULT,
            scrollbar_button_hover_color=NEON_CYAN
        )
        grid_frame.grid(row=2, column=0, sticky="nsew")

        cipher_keys = [
            "caesar", "affine", "hill",
            "vigenere", "playfair", "hang",
            "des", "rsa", "dh"
        ]

        for idx, key in enumerate(cipher_keys):
            row, col = divmod(idx, 3)
            info = CIPHER_INFO.get(key, {})
            card = DashboardCipherCard(
                grid_frame, key, info,
                on_click=self._on_select
            )
            card.grid(
                row=row, column=col,
                padx=8, pady=8, sticky="nsew"
            )
            grid_frame.grid_columnconfigure(col, weight=1)
        for r in range(3):
            grid_frame.grid_rowconfigure(r, weight=0)
