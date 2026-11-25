"""RSA Cipher View — Mã hóa khóa công khai"""
import customtkinter as ctk
from views.theme import *
from views.components import GlowEntry
from views.cipher_view_base import CipherViewBase
from models.rsa import rsa_cipher, is_prime


class RSAView(CipherViewBase):
    def __init__(self, master, **kw):
        super().__init__(
            master, "rsa", "MÃ HÓA RSA",
            "Mã hóa khóa công khai bất đối xứng",
            formula="C = Mᵉ mod n  |  M = Cᵈ mod n",
            has_analysis=True, **kw
        )
        self.input_entry.insert(0, "HI")

    def _build_key_area(self, parent):
        ctk.CTkLabel(
            parent, text="🔑 THAM SỐ KHÓA RSA:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x")

        # p
        fp = ctk.CTkFrame(row, fg_color="transparent")
        fp.pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkLabel(fp, text="Số nguyên tố p:",
                     font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
                     text_color=TEXT_SECONDARY).pack(anchor="w")
        self.rsa_p = GlowEntry(fp, placeholder_text="p")
        self.rsa_p.pack(fill="x")
        self.rsa_p.insert(0, "61")

        # q
        fq = ctk.CTkFrame(row, fg_color="transparent")
        fq.pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkLabel(fq, text="Số nguyên tố q:",
                     font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
                     text_color=TEXT_SECONDARY).pack(anchor="w")
        self.rsa_q = GlowEntry(fq, placeholder_text="q")
        self.rsa_q.pack(fill="x")
        self.rsa_q.insert(0, "53")

        # e
        fe = ctk.CTkFrame(row, fg_color="transparent")
        fe.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(fe, text="Khóa e:",
                     font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
                     text_color=TEXT_SECONDARY).pack(anchor="w")
        self.rsa_e = GlowEntry(fe, placeholder_text="e")
        self.rsa_e.pack(fill="x")
        self.rsa_e.insert(0, "17")

        ctk.CTkLabel(
            parent,
            text="⚠️ Mã hóa: nhập text  |  Giải mã: nhập dãy số cipher cách nhau bằng dấu cách",
            font=ctk.CTkFont(family=FONT_FAMILY, size=10),
            text_color=TEXT_DIM
        ).pack(anchor="w", pady=(6, 0))

    def _validate_params(self):
        try:
            p = int(self.rsa_p.get().strip())
            q = int(self.rsa_q.get().strip())
            e = int(self.rsa_e.get().strip())
        except ValueError:
            self.status.show_error("p, q, e phải là số nguyên!")
            return None
        if not is_prime(p) or not is_prime(q):
            self.status.show_error("p và q bắt buộc phải là số nguyên tố!")
            return None
        if p == q:
            self.status.show_error("p và q phải là 2 số nguyên tố phân biệt!")
            return None
        return p, q, e

    def _on_encrypt(self):
        params = self._validate_params()
        if not params: return
        p, q, e = params
        msg = self._get_input()
        if not msg:
            self.status.show_error("Vui lòng nhập văn bản!"); return
        r, log, err = rsa_cipher(msg, p, q, e, False)
        if err:
            self.status.show_error(err); return
        self._set_output(r)
        self._set_analysis(log)
        self.status.show_success("Mã hóa RSA thành công!")

    def _on_decrypt(self):
        params = self._validate_params()
        if not params: return
        p, q, e = params
        msg = self._get_input()
        if not msg:
            self.status.show_error("Vui lòng nhập ciphertext!"); return
        r, log, err = rsa_cipher(msg, p, q, e, True)
        if err:
            self.status.show_error(err); return
        self._set_output(r)
        self._set_analysis(log)
        self.status.show_success("Giải mã RSA thành công!")

    def _on_clear(self):
        self.rsa_p.delete(0, "end")
        self.rsa_q.delete(0, "end")
        self.rsa_e.delete(0, "end")
