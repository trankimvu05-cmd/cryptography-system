"""Affine Cipher View"""
import customtkinter as ctk
from views.theme import *
from views.components import GlowEntry
from views.cipher_view_base import CipherViewBase
from models.affine import affine_cipher


class AffineView(CipherViewBase):
    def __init__(self, master, **kw):
        super().__init__(
            master, "affine", "MÃ HÓA AFFINE",
            "Kết hợp phép nhân và dịch chuyển",
            formula="C = (aP + b) mod 26", **kw
        )
        self.input_entry.insert(0, "AFFINE CIPHER EXAMPLE")

    def _build_key_area(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x")

        # Khóa a
        fa = ctk.CTkFrame(row, fg_color="transparent")
        fa.pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkLabel(
            fa, text="🔑 KHÓA a (ƯCLN(a,26)=1):",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))
        self.key_a = GlowEntry(fa, placeholder_text="Ví dụ: 7")
        self.key_a.pack(fill="x")
        self.key_a.insert(0, "7")

        # Khóa b
        fb = ctk.CTkFrame(row, fg_color="transparent")
        fb.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(
            fb, text="🔑 KHÓA b (Dịch chuyển):",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))
        self.key_b = GlowEntry(fb, placeholder_text="Ví dụ: 3")
        self.key_b.pack(fill="x")
        self.key_b.insert(0, "3")

    def _on_encrypt(self):
        t = self._get_input()
        if not t:
            self.status.show_error("Vui lòng nhập văn bản!"); return
        try:
            a = int(self.key_a.get().strip())
            b = int(self.key_b.get().strip())
        except ValueError:
            self.status.show_error("Khóa a và b phải là số nguyên!"); return
        r, err = affine_cipher(t, a, b, False)
        if err:
            self.status.show_error(err); return
        self._set_output(r)
        self.status.show_success(f"Đã mã hóa thành công ({len(t)} ký tự)")

    def _on_decrypt(self):
        t = self._get_input()
        if not t:
            self.status.show_error("Vui lòng nhập văn bản!"); return
        try:
            a = int(self.key_a.get().strip())
            b = int(self.key_b.get().strip())
        except ValueError:
            self.status.show_error("Khóa a và b phải là số nguyên!"); return
        r, err = affine_cipher(t, a, b, True)
        if err:
            self.status.show_error(err); return
        self._set_output(r)
        self.status.show_success(f"Đã giải mã thành công ({len(t)} ký tự)")

    def _on_clear(self):
        self.key_a.delete(0, "end")
        self.key_b.delete(0, "end")
