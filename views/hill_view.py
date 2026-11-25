"""Hill Cipher View — Ma trận khóa NxN với bảng phân tích"""
import customtkinter as ctk
from views.theme import *
from views.components import GlowEntry
from views.cipher_view_base import CipherViewBase
from models.hill import hill_cipher


class HillView(CipherViewBase):
    def __init__(self, master, **kw):
        self.hill_entries = []
        super().__init__(
            master, "hill", "MÃ HÓA HILL",
            "Mã hóa ma trận đa bảng chữ cái",
            formula="C = P × K mod 26", has_analysis=True, **kw
        )
        self.input_entry.insert(0, "ACT")

    def _build_key_area(self, parent):
        # Size control
        sz_row = ctk.CTkFrame(parent, fg_color="transparent")
        sz_row.pack(fill="x", pady=(0, 6))

        ctk.CTkLabel(
            sz_row, text="🔑 CẤP MA TRẬN n:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(side="left")

        self.size_entry = GlowEntry(sz_row, width=60, placeholder_text="n")
        self.size_entry.pack(side="left", padx=8)
        self.size_entry.insert(0, "3")

        from views.components import NeonButton
        NeonButton(
            sz_row, text="Tạo Lưới", neon_color="#f59e0b", hover="#d97706",
            width=90, height=34, command=self._update_grid
        ).pack(side="left")

        # Matrix grid
        self.grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.grid_frame.pack(fill="x", pady=(4, 0))
        self._update_grid()

    def _update_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.hill_entries.clear()
        try:
            n = int(self.size_entry.get().strip())
            if n < 2 or n > 6:
                raise ValueError
        except ValueError:
            self.status.show_error("Cấp ma trận từ 2 đến 6!")
            return

        default_3x3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
        for i in range(n):
            rf = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
            rf.pack(anchor="w", pady=2)
            row = []
            for j in range(n):
                e = ctk.CTkEntry(
                    rf, width=50, height=34, justify="center",
                    font=ctk.CTkFont(family=FONT_MONO, size=FONT_BODY, weight="bold"),
                    fg_color=BG_INPUT, border_color=BORDER_DEFAULT,
                    text_color=TEXT_PRIMARY, corner_radius=6
                )
                e.pack(side="left", padx=2)
                if n == 3:
                    e.insert(0, str(default_3x3[i][j]))
                else:
                    e.insert(0, "1" if i == j else "0")
                row.append(e)
            self.hill_entries.append(row)

    def _get_matrix(self):
        K = []
        for r in self.hill_entries:
            row_vals = []
            for e in r:
                val = e.get().strip()
                if not val:
                    raise ValueError("Vui lòng nhập đầy đủ số nguyên vào ma trận!")
                row_vals.append(int(val))
            K.append(row_vals)
        return K

    def _on_encrypt(self):
        t = self._get_input()
        if not t:
            self.status.show_error("Vui lòng nhập văn bản!"); return
        try:
            K = self._get_matrix()
        except (ValueError, TypeError) as e:
            self.status.show_error(str(e)); return
        res, log, err = hill_cipher(t, K, False)
        if err:
            self.status.show_error(err); return
        self._set_output(res)
        self._set_analysis(log)
        self.status.show_success("Mã hóa Hill thành công!")

    def _on_decrypt(self):
        t = self._get_input()
        if not t:
            self.status.show_error("Vui lòng nhập văn bản!"); return
        try:
            K = self._get_matrix()
        except (ValueError, TypeError) as e:
            self.status.show_error(str(e)); return
        res, log, err = hill_cipher(t, K, True)
        if err:
            self.status.show_error(err); return
        self._set_output(res)
        self._set_analysis(log)
        self.status.show_success("Giải mã Hill thành công!")
