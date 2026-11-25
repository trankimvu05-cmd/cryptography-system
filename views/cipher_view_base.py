"""
═══════════════════════════════════════════════════════
Cipher View Base — Lớp cha chung cho tất cả cipher view
Cung cấp layout tiêu chuẩn: header, input, key, buttons, output, status
═══════════════════════════════════════════════════════
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from views.theme import *
from views.components import (
    CyberCard, NeonButton, GlowEntry, GlowTextbox,
    SectionHeader, StatusBar, ActionBar
)


class CipherViewBase(ctk.CTkFrame):
    """
    Lớp cha cho tất cả giao diện hệ mật mã.
    Subclass override: _build_key_area(), _on_encrypt(), _on_decrypt(), _on_clear()
    """

    def __init__(self, master, cipher_key, title, subtitle, formula="",
                 has_analysis=False, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._cipher_key = cipher_key
        self._has_analysis = has_analysis

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        if has_analysis:
            self.grid_columnconfigure(1, weight=1)

        # ─── HEADER ───
        header = CyberCard(self)
        header.grid(row=0, column=0,
                    columnspan=2 if has_analysis else 1,
                    sticky="ew", pady=(0, 12))

        title_lbl = ctk.CTkLabel(
            header, text=title,
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_TITLE_SIZE, weight="bold"),
            text_color=NEON_CYAN
        )
        title_lbl.pack(anchor="w", padx=18, pady=(12, 0))

        desc_text = subtitle
        if formula:
            desc_text += f"  •  {formula}"
        desc_lbl = ctk.CTkLabel(
            header, text=desc_text,
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
            text_color=TEXT_SECONDARY
        )
        desc_lbl.pack(anchor="w", padx=18, pady=(2, 12))

        # ─── MAIN CONTENT CARD ───
        main_card = CyberCard(self)
        main_card.grid(row=1, column=0, sticky="nsew", padx=(0, 6 if has_analysis else 0))
        main_card.grid_rowconfigure(5, weight=1)
        main_card.grid_columnconfigure(0, weight=1)

        # Input area
        ctk.CTkLabel(
            main_card, text="📝 VĂN BẢN ĐẦU VÀO:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(15, 4))

        self.input_entry = GlowEntry(
            main_card, placeholder_text="Nhập văn bản cần xử lý..."
        )
        self.input_entry.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 8))

        # Key area — subclass override
        self.key_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        self.key_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 8))
        self._build_key_area(self.key_frame)

        # Action buttons
        btn_bar = ActionBar(main_card)
        btn_bar.grid(row=3, column=0, sticky="ew", padx=18, pady=(4, 8))

        NeonButton(
            btn_bar, text="🔒  MÃ HÓA",
            neon_color=NEON_GREEN, hover="#059669",
            width=130, command=self._safe_encrypt
        ).pack(side="left", padx=(0, 6))

        NeonButton(
            btn_bar, text="🔓  GIẢI MÃ",
            neon_color=NEON_BLUE, hover="#2563eb",
            width=130, command=self._safe_decrypt
        ).pack(side="left", padx=(0, 6))

        NeonButton(
            btn_bar, text="📂 Mở File",
            neon_color="#475569", hover="#374151",
            width=100, command=self._open_file
        ).pack(side="left", padx=(0, 6))

        NeonButton(
            btn_bar, text="🔄 Làm mới",
            neon_color="#6b21a8", hover="#581c87",
            width=100, command=self._safe_clear
        ).pack(side="left")

        # Output area
        out_header = ctk.CTkFrame(main_card, fg_color="transparent")
        out_header.grid(row=4, column=0, sticky="ew", padx=18, pady=(4, 4))

        ctk.CTkLabel(
            out_header, text="📤 KẾT QUẢ:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=NEON_GREEN
        ).pack(side="left")

        NeonButton(
            out_header, text="📋 Sao chép",
            neon_color="#334155", hover="#1e293b",
            width=100, height=30,
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
            command=self._copy_result
        ).pack(side="right", padx=(4, 0))

        NeonButton(
            out_header, text="💾 Lưu file",
            neon_color="#334155", hover="#1e293b",
            width=100, height=30,
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
            command=self._save_file
        ).pack(side="right")

        self.output_box = GlowTextbox(main_card, height=120)
        self.output_box.grid(row=5, column=0, sticky="nsew", padx=18, pady=(0, 8))

        # Status bar
        self.status = StatusBar(main_card)
        self.status.grid(row=6, column=0, sticky="ew", padx=18, pady=(0, 12))

        # ─── ANALYSIS PANEL (optional) ───
        if has_analysis:
            analysis_card = CyberCard(self)
            analysis_card.grid(row=1, column=1, sticky="nsew", padx=(6, 0))
            analysis_card.grid_rowconfigure(1, weight=1)
            analysis_card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                analysis_card, text="📊 BẢNG PHÂN TÍCH CHI TIẾT:",
                font=ctk.CTkFont(
                    family=FONT_FAMILY, size=FONT_BODY, weight="bold"
                ),
                text_color=NEON_CYAN
            ).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 5))

            self.analysis_box = GlowTextbox(
                analysis_card,
                text_color=NEON_CYAN,
                font=ctk.CTkFont(family=FONT_MONO, size=FONT_SMALL)
            )
            self.analysis_box.grid(
                row=1, column=0, sticky="nsew", padx=15, pady=(0, 12)
            )
            self.analysis_box.insert(
                "1.0",
                "Nhấn MÃ HÓA hoặc GIẢI MÃ để xem bảng phân tích thuật toán."
            )

    # ─── METHODS TO OVERRIDE ───

    def _build_key_area(self, parent):
        """Override để xây dựng khu vực nhập khóa riêng cho từng cipher."""
        pass

    def _on_encrypt(self):
        """Override — Xử lý mã hóa."""
        raise NotImplementedError

    def _on_decrypt(self):
        """Override — Xử lý giải mã."""
        raise NotImplementedError

    def _on_clear(self):
        """Override — Xử lý xóa thêm (ngoài input/output)."""
        pass

    # ─── INTERNAL METHODS ───

    def _safe_encrypt(self):
        try:
            self.status.clear()
            self._on_encrypt()
        except Exception as e:
            self.status.show_error(str(e))

    def _safe_decrypt(self):
        try:
            self.status.clear()
            self._on_decrypt()
        except Exception as e:
            self.status.show_error(str(e))

    def _safe_clear(self):
        self.input_entry.delete(0, "end")
        self.output_box.delete("1.0", "end")
        self.status.clear()
        if self._has_analysis:
            self.analysis_box.delete("1.0", "end")
        self._on_clear()

    def _get_input(self):
        return self.input_entry.get().strip()

    def _set_output(self, text):
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", str(text))

    def _set_analysis(self, text):
        if self._has_analysis:
            self.analysis_box.delete("1.0", "end")
            self.analysis_box.insert("1.0", str(text))

    def _open_file(self):
        p = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if p:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = f.read()
                self.input_entry.delete(0, "end")
                self.input_entry.insert(0, data)
                self.status.show_success(f"Đã đọc file: {p.split('/')[-1]}")
            except Exception as e:
                self.status.show_error(f"Không thể đọc file: {e}")

    def _save_file(self):
        val = self.output_box.get("1.0", "end").strip()
        if not val:
            self.status.show_error("Chưa có kết quả để lưu!")
            return
        p = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if p:
            try:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(val)
                self.status.show_success("Đã lưu file thành công!")
            except Exception as e:
                self.status.show_error(f"Không thể lưu: {e}")

    def _copy_result(self):
        val = self.output_box.get("1.0", "end").strip()
        if not val:
            self.status.show_error("Chưa có kết quả để sao chép!")
            return
        self.winfo_toplevel().clipboard_clear()
        self.winfo_toplevel().clipboard_append(val)
        self.status.show_success("Đã sao chép kết quả!")
