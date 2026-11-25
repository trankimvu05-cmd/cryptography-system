"""Playfair Cipher View — Bảng mã 5×5"""
import customtkinter as ctk
from views.theme import *
from views.components import GlowEntry
from views.cipher_view_base import CipherViewBase
from models.playfair import playfair_cipher, playfair_matrix


class PlayfairView(CipherViewBase):
    def __init__(self, master, **kw):
        super().__init__(
            master, "playfair", "MÃ HÓA PLAYFAIR",
            "Ma trận khóa 5×5 mã hóa theo cặp",
            formula="Kết hợp I/J, chèn X giữa cặp trùng",
            has_analysis=True, **kw
        )
        self.input_entry.insert(0, "BALLOON")

    def _build_key_area(self, parent):
        ctk.CTkLabel(
            parent, text="🔑 TỪ KHÓA K (Keyword):",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))
        self.key_entry = GlowEntry(parent, placeholder_text="Ví dụ: MONARCHY")
        self.key_entry.pack(fill="x")
        self.key_entry.insert(0, "MONARCHY")

    def _refresh_matrix_display(self, kw):
        m = playfair_matrix(kw or "KEYWORD")
        grid = "BẢNG MÃ PLAYFAIR 5×5:\n\n"
        for i in range(0, 25, 5):
            grid += "     ".join(m[i:i + 5]) + "\n\n"
        self._set_analysis(grid)

    def _on_encrypt(self):
        t = self._get_input()
        kw = self.key_entry.get().strip()
        if not t or not kw:
            self.status.show_error("Vui lòng nhập đủ văn bản và từ khóa!"); return
        if not kw.isalpha():
            self.status.show_error("Từ khóa chỉ gồm chữ cái!"); return
        r, m = playfair_cipher(t, kw, False)
        self._set_output(r)
        self._refresh_matrix_display(kw)
        self.status.show_success("Mã hóa Playfair thành công!")

    def _on_decrypt(self):
        t = self._get_input()
        kw = self.key_entry.get().strip()
        if not t or not kw:
            self.status.show_error("Vui lòng nhập đủ văn bản và từ khóa!"); return
        if not kw.isalpha():
            self.status.show_error("Từ khóa chỉ gồm chữ cái!"); return
        r, m = playfair_cipher(t, kw, True)
        self._set_output(r)
        self._refresh_matrix_display(kw)
        self.status.show_success("Giải mã Playfair thành công!")

    def _on_clear(self):
        self.key_entry.delete(0, "end")
