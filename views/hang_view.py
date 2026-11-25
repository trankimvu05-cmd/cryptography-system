"""Hoán Vị Hàng View — Columnar Transposition"""
import customtkinter as ctk
from views.theme import *
from views.components import GlowEntry
from views.cipher_view_base import CipherViewBase
from models.hang import hang_cipher


class HangView(CipherViewBase):
    def __init__(self, master, **kw):
        super().__init__(
            master, "hang", "MÃ HÓA HOÁN VỊ HÀNG",
            "Hoán vị cột theo khóa dãy số",
            formula="Ghi hàng — đọc cột hoán vị",
            has_analysis=True, **kw
        )
        self.input_entry.insert(0, "DEFEND THE EAST WALL")

    def _build_key_area(self, parent):
        ctk.CTkLabel(
            parent, text="🔑 KHÓA K (Dãy số cách nhau bởi dấu phẩy):",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))
        self.key_entry = GlowEntry(parent, placeholder_text="Ví dụ: 3, 6, 2, 1, 5, 4")
        self.key_entry.pack(fill="x")
        self.key_entry.insert(0, "3, 6, 2, 1, 5, 4")

    def _parse_key(self):
        k = [int(x) for x in self.key_entry.get().replace(',', ' ').split()]
        if not k:
            raise ValueError
        return k

    def _on_encrypt(self):
        t = self._get_input()
        if not t:
            self.status.show_error("Vui lòng nhập văn bản!"); return
        try:
            k = self._parse_key()
        except (ValueError, TypeError):
            self.status.show_error("Khóa K phải là dãy số!"); return
        r, log = hang_cipher(t, k, False)
        self._set_output(r)
        self._set_analysis(log)
        self.status.show_success("Mã hóa Hoán vị hàng thành công!")

    def _on_decrypt(self):
        t = self._get_input()
        if not t:
            self.status.show_error("Vui lòng nhập văn bản!"); return
        try:
            k = self._parse_key()
        except (ValueError, TypeError):
            self.status.show_error("Khóa K phải là dãy số!"); return
        r, log = hang_cipher(t, k, True)
        self._set_output(r)
        self._set_analysis(log)
        self.status.show_success("Giải mã Hoán vị hàng thành công!")

    def _on_clear(self):
        self.key_entry.delete(0, "end")
