"""Caesar Cipher View"""
import customtkinter as ctk
from views.theme import *
from views.components import GlowEntry
from views.cipher_view_base import CipherViewBase
from models.caesar import caesar_cipher


class CaesarView(CipherViewBase):
    def __init__(self, master, **kw):
        super().__init__(
            master, "caesar", "MÃ HÓA CAESAR",
            "Thuật toán thay thế vòng tròn",
            formula="C = (P + K) mod 26", **kw
        )
        self.input_entry.insert(0, "HELLO CAESAR CIPHER")

    def _build_key_area(self, parent):
        ctk.CTkLabel(
            parent, text="🔑 KHÓA K (Số nguyên):",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))
        self.key_entry = GlowEntry(parent, placeholder_text="Ví dụ: 3", width=200)
        self.key_entry.pack(anchor="w")
        self.key_entry.insert(0, "3")

    def _on_encrypt(self):
        t = self._get_input()
        if not t:
            self.status.show_error("Vui lòng nhập văn bản!")
            return
        try:
            k = int(self.key_entry.get().strip())
        except ValueError:
            self.status.show_error("Khóa K phải là số nguyên!")
            return
        self._set_output(caesar_cipher(t, k, False))
        self.status.show_success(f"Đã mã hóa thành công ({len(t)} ký tự)")

    def _on_decrypt(self):
        t = self._get_input()
        if not t:
            self.status.show_error("Vui lòng nhập văn bản!")
            return
        try:
            k = int(self.key_entry.get().strip())
        except ValueError:
            self.status.show_error("Khóa K phải là số nguyên!")
            return
        self._set_output(caesar_cipher(t, k, True))
        self.status.show_success(f"Đã giải mã thành công ({len(t)} ký tự)")

    def _on_clear(self):
        self.key_entry.delete(0, "end")
