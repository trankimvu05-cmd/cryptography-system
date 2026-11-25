"""
═══════════════════════════════════════════════════════
CYBER SECURITY DASHBOARD — Reusable Components
Widget tái sử dụng cho giao diện Cyber Security
═══════════════════════════════════════════════════════
"""

import customtkinter as ctk
from views.theme import *


class CyberCard(ctk.CTkFrame):
    """Card bo góc với nền tối và viền tinh tế."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("corner_radius", CARD_RADIUS)
        kwargs.setdefault("fg_color", BG_CARD)
        kwargs.setdefault("border_color", BORDER_CARD)
        kwargs.setdefault("border_width", 1)
        super().__init__(master, **kwargs)


class NeonButton(ctk.CTkButton):
    """Nút bấm với hiệu ứng neon."""

    def __init__(self, master, neon_color=NEON_CYAN, hover=None, **kwargs):
        kwargs.setdefault("corner_radius", BUTTON_RADIUS)
        kwargs.setdefault("height", BUTTON_HEIGHT)
        kwargs.setdefault("fg_color", neon_color)
        kwargs.setdefault("hover_color", hover or _lighten(neon_color))
        kwargs.setdefault("text_color", "#ffffff")
        kwargs.setdefault("font", ctk.CTkFont(
            family=FONT_FAMILY, size=FONT_BUTTON, weight="bold"
        ))
        kwargs.setdefault("cursor", "hand2")
        super().__init__(master, **kwargs)


class GlowEntry(ctk.CTkEntry):
    """Ô nhập liệu với viền phát sáng khi focus."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("height", INPUT_HEIGHT)
        kwargs.setdefault("corner_radius", 8)
        kwargs.setdefault("fg_color", BG_INPUT)
        kwargs.setdefault("border_color", BORDER_DEFAULT)
        kwargs.setdefault("text_color", TEXT_PRIMARY)
        kwargs.setdefault("placeholder_text_color", TEXT_DIM)
        kwargs.setdefault("font", ctk.CTkFont(
            family=FONT_MONO, size=FONT_BODY
        ))
        super().__init__(master, **kwargs)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, _event=None):
        self.configure(border_color=NEON_CYAN)

    def _on_focus_out(self, _event=None):
        self.configure(border_color=BORDER_DEFAULT)


class GlowTextbox(ctk.CTkTextbox):
    """Textbox nhiều dòng với nền tối."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("corner_radius", 8)
        kwargs.setdefault("fg_color", BG_INPUT)
        kwargs.setdefault("border_color", BORDER_DEFAULT)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("text_color", TEXT_CODE)
        kwargs.setdefault("font", ctk.CTkFont(
            family=FONT_MONO, size=FONT_CODE
        ))
        super().__init__(master, **kwargs)


class SectionHeader(ctk.CTkFrame):
    """Header section với icon và tiêu đề."""

    def __init__(self, master, title, subtitle="", accent=NEON_CYAN, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.lbl_title = ctk.CTkLabel(
            self, text=title,
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=accent
        )
        self.lbl_title.pack(anchor="w")

        if subtitle:
            self.lbl_sub = ctk.CTkLabel(
                self, text=subtitle,
                font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
                text_color=TEXT_SECONDARY
            )
            self.lbl_sub.pack(anchor="w", pady=(2, 0))


class StatusBar(ctk.CTkLabel):
    """Thanh trạng thái hiển thị thông báo lỗi/thành công."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("text", "")
        kwargs.setdefault("font", ctk.CTkFont(
            family=FONT_FAMILY, size=FONT_SMALL
        ))
        kwargs.setdefault("text_color", TEXT_SECONDARY)
        kwargs.setdefault("anchor", "w")
        super().__init__(master, **kwargs)

    def show_success(self, msg):
        self.configure(text=f"✅ {msg}", text_color=NEON_GREEN)

    def show_error(self, msg):
        self.configure(text=f"❌ {msg}", text_color=NEON_PINK)

    def show_info(self, msg):
        self.configure(text=f"ℹ️ {msg}", text_color=NEON_CYAN)

    def clear(self):
        self.configure(text="", text_color=TEXT_SECONDARY)


class ActionBar(ctk.CTkFrame):
    """Thanh nút hành động ngang."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)


class DashboardCipherCard(ctk.CTkFrame):
    """Thẻ cipher cho trang Dashboard với hiệu ứng hover."""

    def __init__(self, master, cipher_key, cipher_info, on_click=None, **kwargs):
        super().__init__(
            master,
            corner_radius=CARD_RADIUS,
            fg_color=BG_CARD,
            border_color=BORDER_CARD,
            border_width=1,
            cursor="hand2",
            **kwargs
        )
        self._cipher_key = cipher_key
        self._on_click = on_click
        self._accent = cipher_info.get("color", NEON_CYAN)

        # Accent bar trên cùng
        accent_bar = ctk.CTkFrame(
            self, height=4, corner_radius=2,
            fg_color=self._accent
        )
        accent_bar.pack(fill="x", padx=15, pady=(12, 0))

        # Icon
        icon_lbl = ctk.CTkLabel(
            self, text=cipher_info.get("icon", "🔐"),
            font=ctk.CTkFont(size=32)
        )
        icon_lbl.pack(pady=(10, 5))

        # Tên thuật toán
        name_lbl = ctk.CTkLabel(
            self, text=cipher_info.get("name", ""),
            font=ctk.CTkFont(
                family=FONT_FAMILY, size=FONT_SUBTITLE, weight="bold"
            ),
            text_color=TEXT_TITLE
        )
        name_lbl.pack(pady=(0, 3))

        # Category badge
        cat = cipher_info.get("category", "")
        if cat:
            cat_lbl = ctk.CTkLabel(
                self, text=cat,
                font=ctk.CTkFont(family=FONT_FAMILY, size=10),
                text_color=self._accent,
                fg_color=_with_alpha(self._accent),
                corner_radius=4, padx=8, pady=2
            )
            cat_lbl.pack(pady=(0, 5))

        # Mô tả
        desc_lbl = ctk.CTkLabel(
            self, text=cipher_info.get("desc", ""),
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
            text_color=TEXT_SECONDARY,
            wraplength=180
        )
        desc_lbl.pack(pady=(0, 12), padx=10)

        # Bind click trên toàn bộ card
        for widget in [self, accent_bar, icon_lbl, name_lbl, desc_lbl]:
            widget.bind("<Button-1>", self._handle_click)

        # Hover effects
        for widget in [self, accent_bar, icon_lbl, name_lbl, desc_lbl]:
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

        if cat:
            cat_lbl.bind("<Button-1>", self._handle_click)
            cat_lbl.bind("<Enter>", self._on_enter)
            cat_lbl.bind("<Leave>", self._on_leave)

    def _handle_click(self, _event=None):
        if self._on_click:
            self._on_click(self._cipher_key)

    def _on_enter(self, _event=None):
        self.configure(
            fg_color=BG_CARD_HOVER,
            border_color=self._accent
        )

    def _on_leave(self, _event=None):
        self.configure(
            fg_color=BG_CARD,
            border_color=BORDER_CARD
        )


# ═══════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════

def _lighten(hex_color, amount=30):
    """Làm sáng một màu hex."""
    hex_color = hex_color.lstrip('#')
    r = min(255, int(hex_color[0:2], 16) + amount)
    g = min(255, int(hex_color[2:4], 16) + amount)
    b = min(255, int(hex_color[4:6], 16) + amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def _with_alpha(hex_color):
    """Tạo màu nền rất nhạt (giả lập alpha trên nền tối)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) // 6
    g = int(hex_color[2:4], 16) // 6
    b = int(hex_color[4:6], 16) // 6
    return f"#{r:02x}{g:02x}{b:02x}"
