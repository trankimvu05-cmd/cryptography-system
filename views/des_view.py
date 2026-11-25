"""DES Cipher View — 16 vòng Feistel với bảng phân tích"""
import customtkinter as ctk
from views.theme import *
from views.components import GlowEntry
from views.cipher_view_base import CipherViewBase
from models.des import des_cipher


class DESView(CipherViewBase):
    def __init__(self, master, **kw):
        super().__init__(
            master, "des", "MÃ HÓA DES",
            "Mã khối Feistel 64-bit tiêu chuẩn",
            formula="16 vòng Feistel + S-Box",
            has_analysis=True, **kw
        )
        self.input_entry.insert(0, "VIETNAM")

    def _build_key_area(self, parent):
        ctk.CTkLabel(
            parent, text="🔑 KHÓA K (16 ký tự Hex = 64-bit):",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))
        self.key_entry = GlowEntry(
            parent,
            placeholder_text="Ví dụ: 133457799BBCDFF1",
            font=ctk.CTkFont(family=FONT_MONO, size=FONT_BODY, weight="bold")
        )
        self.key_entry.pack(fill="x")
        self.key_entry.insert(0, "133457799BBCDFF1")

        ctk.CTkLabel(
            parent,
            text="⚠️ Mã hóa: nhập Plaintext văn bản  |  Giải mã: nhập Ciphertext Hex",
            font=ctk.CTkFont(family=FONT_FAMILY, size=10),
            text_color=TEXT_DIM
        ).pack(anchor="w", pady=(4, 0))

    def _on_encrypt(self):
        msg = self._get_input()
        k_hex = self.key_entry.get().strip().upper()
        if len(k_hex) != 16:
            self.status.show_error("Khóa K phải đúng 16 ký tự Hex (64-bit)!"); return
        if not msg:
            self.status.show_error("Vui lòng nhập văn bản!"); return
        r, log, err = des_cipher(msg, k_hex, False)
        if err:
            self.status.show_error(err); return
        self._set_output(r)
        self._set_analysis(log)
        self.status.show_success("Mã hóa DES thành công!")

    def _on_decrypt(self):
        msg = self._get_input()
        k_hex = self.key_entry.get().strip().upper()
        if len(k_hex) != 16:
            self.status.show_error("Khóa K phải đúng 16 ký tự Hex (64-bit)!"); return
        if not msg:
            self.status.show_error("Vui lòng nhập ciphertext Hex!"); return
        r, log, err = des_cipher(msg, k_hex, True)
        if err:
            self.status.show_error(err); return
        self._set_output(r)
        self._set_analysis(log)
        self.status.show_success("Giải mã DES thành công!")

    def _on_clear(self):
        self.key_entry.delete(0, "end")
