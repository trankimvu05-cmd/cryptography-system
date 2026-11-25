"""Vigenère Cipher View"""
import customtkinter as ctk
from views.theme import *
from views.components import GlowEntry
from views.cipher_view_base import CipherViewBase
from models.vigenere import vigenere_cipher


class VigenereView(CipherViewBase):
    def __init__(self, master, **kw):
        super().__init__(
            master, "vigenere", "MÃ HÓA VIGENÈRE",
            "Khóa tuần hoàn đa bảng chữ cái",
            formula="Cᵢ = (Pᵢ + Kᵢ) mod 26", **kw
        )
        self.input_entry.insert(0, "ATTACK AT DAWN")

    def _build_key_area(self, parent):
        ctk.CTkLabel(
            parent, text="🔑 KHÓA K (Chuỗi chữ cái):",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))
        self.key_entry = GlowEntry(parent, placeholder_text="Ví dụ: LEMON")
        self.key_entry.pack(fill="x")
        self.key_entry.insert(0, "LEMON")

    def _on_encrypt(self):
        t = self._get_input()
        k = self.key_entry.get().strip()
        if not t or not k:
            self.status.show_error("Vui lòng nhập đủ văn bản và khóa!"); return
        if not k.isalpha():
            self.status.show_error("Khóa Vigenère chỉ gồm chữ cái!"); return
        self._set_output(vigenere_cipher(t, k, False))
        self.status.show_success(f"Đã mã hóa thành công ({len(t)} ký tự)")

    def _on_decrypt(self):
        t = self._get_input()
        k = self.key_entry.get().strip()
        if not t or not k:
            self.status.show_error("Vui lòng nhập đủ văn bản và khóa!"); return
        if not k.isalpha():
            self.status.show_error("Khóa Vigenère chỉ gồm chữ cái!"); return
        self._set_output(vigenere_cipher(t, k, True))
        self.status.show_success(f"Đã giải mã thành công ({len(t)} ký tự)")

    def _on_clear(self):
        self.key_entry.delete(0, "end")
