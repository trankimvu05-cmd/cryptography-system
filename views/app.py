"""
═══════════════════════════════════════════════════════
CYBER SECURITY DASHBOARD — Main Window & Navigation
Quản lý Sidebar, Topbar, chuyển đổi các View
═══════════════════════════════════════════════════════
"""

import customtkinter as ctk
from views.theme import *
from views.dashboard import DashboardView
from views.about_view import AboutView
from views.caesar_view import CaesarView
from views.affine_view import AffineView
from views.hill_view import HillView
from views.vigenere_view import VigenereView
from views.playfair_view import PlayfairView
from views.hang_view import HangView
from views.des_view import DESView
from views.rsa_view import RSAView
from views.dh_view import DHView


class MainApp(ctk.CTk):
    """Cửa sổ ứng dụng chính với Sidebar Cyber Security và Router điều hướng."""

    def __init__(self):
        super().__init__()

        # Cấu hình cửa sổ
        self.title("🛡️ CRYPTOGRAPHY SYSTEM — CYBER SECURITY DASHBOARD")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_W, WINDOW_MIN_H)
        self.configure(fg_color=BG_DARKEST)

        # Layout chính: Cột 0 là Sidebar, Cột 1 là Workspace chính
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._active_cipher = None
        self._nav_buttons = {}
        self._views = {}

        self._build_sidebar()
        self._build_workspace()

        # Hiển thị Dashboard mặc định
        self.navigate_to("dashboard")

    def _build_sidebar(self):
        """Tạo sidebar bên trái mang phong cách Cyberpunk / Cyber Security."""
        sidebar = ctk.CTkFrame(
            self, width=SIDEBAR_WIDTH, corner_radius=0,
            fg_color=SIDEBAR_BG, border_color=BORDER_SUBTLE, border_width=1
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(2, weight=1)
        sidebar.grid_columnconfigure(0, weight=1)

        # ─── LOGO & BRANDING ───
        brand_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand_frame.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="ew")

        brand_top = ctk.CTkFrame(brand_frame, fg_color="transparent")
        brand_top.pack(anchor="w")

        ctk.CTkLabel(
            brand_top, text="⚡",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            brand_top, text="CRYPTOSYS",
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=NEON_CYAN
        ).pack(side="left")

        ctk.CTkLabel(
            brand_frame, text="Cyber Security Lab v2.0",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=TEXT_DIM
        ).pack(anchor="w", padx=(30, 0))

        # Đường phân cách
        sep = ctk.CTkFrame(sidebar, height=1, fg_color=BORDER_SUBTLE)
        sep.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")

        # ─── NAVIGATION BUTTONS LIST ───
        nav_scroll = ctk.CTkScrollableFrame(
            sidebar, fg_color="transparent",
            scrollbar_button_color=BORDER_DEFAULT,
            scrollbar_button_hover_color=NEON_CYAN
        )
        nav_scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        nav_scroll.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            nav_scroll, text="MENU ĐIỀU HƯỚNG",
            font=ctk.CTkFont(family=FONT_FAMILY, size=10, weight="bold"),
            text_color=TEXT_DIM
        ).pack(anchor="w", padx=10, pady=(4, 8))

        for key in NAV_ORDER:
            info = CIPHER_INFO.get(key, {})
            icon = info.get("icon", "🔹")
            name = info.get("name", key.capitalize())

            btn = ctk.CTkButton(
                nav_scroll,
                text=f"  {icon}   {name}",
                anchor="w",
                font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_NAV),
                height=NAV_BUTTON_H,
                corner_radius=8,
                fg_color="transparent",
                text_color=SIDEBAR_TEXT,
                hover_color=SIDEBAR_HOVER,
                command=lambda k=key: self.navigate_to(k)
            )
            btn.pack(fill="x", pady=2)
            self._nav_buttons[key] = btn

        # ─── FOOTER & SYSTEM STATUS ───
        footer = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer.grid(row=3, column=0, padx=15, pady=15, sticky="ew")

        status_card = ctk.CTkFrame(
            footer, fg_color=BG_CARD, corner_radius=10,
            border_color=BORDER_CARD, border_width=1
        )
        status_card.pack(fill="x", pady=(0, 10), ipady=4)

        sc_inner = ctk.CTkFrame(status_card, fg_color="transparent")
        sc_inner.pack(fill="x", padx=12, pady=6)

        ctk.CTkLabel(
            sc_inner, text="🟢 Hệ thống sẵn sàng",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=NEON_GREEN
        ).pack(anchor="w")

        ctk.CTkLabel(
            sc_inner, text="9/9 Thuật toán bảo toàn",
            font=ctk.CTkFont(family=FONT_FAMILY, size=10),
            text_color=TEXT_DIM
        ).pack(anchor="w")

        # Nút về Dashboard nhanh
        self.btn_home = ctk.CTkButton(
            footer, text="🏠 Trang Chủ",
            height=34, corner_radius=8,
            fg_color="#1e293b", hover_color="#334155",
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL, weight="bold"),
            command=lambda: self.navigate_to("dashboard")
        )
        self.btn_home.pack(fill="x")

    def _build_workspace(self):
        """Tạo vùng làm việc chính bên phải."""
        self.workspace = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.workspace.grid_rowconfigure(0, weight=1)
        self.workspace.grid_columnconfigure(0, weight=1)

        # Khởi tạo trước tất cả các Views
        self._views["dashboard"] = DashboardView(self.workspace, on_select_cipher=self.navigate_to)
        self._views["about"] = AboutView(self.workspace)
        self._views["caesar"] = CaesarView(self.workspace)
        self._views["affine"] = AffineView(self.workspace)
        self._views["hill"] = HillView(self.workspace)
        self._views["vigenere"] = VigenereView(self.workspace)
        self._views["playfair"] = PlayfairView(self.workspace)
        self._views["hang"] = HangView(self.workspace)
        self._views["des"] = DESView(self.workspace)
        self._views["rsa"] = RSAView(self.workspace)
        self._views["dh"] = DHView(self.workspace)

    def navigate_to(self, key):
        """Chuyển đổi view hiện tại sang key mong muốn."""
        if key not in self._views:
            return

        # Ẩn view cũ
        if self._active_cipher and self._active_cipher in self._views:
            self._views[self._active_cipher].grid_forget()

        # Hiện view mới
        self._views[key].grid(row=0, column=0, sticky="nsew")
        self._active_cipher = key

        # Cập nhật style cho Sidebar button
        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=SIDEBAR_ACTIVE,
                    text_color=SIDEBAR_TEXT_ACTIVE,
                    border_color=NEON_CYAN,
                    border_width=1
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=SIDEBAR_TEXT,
                    border_width=0
                )
