"""Diffie-Hellman Key Exchange View"""
import customtkinter as ctk
from views.theme import *
from views.components import (
    CyberCard, NeonButton, GlowEntry, GlowTextbox, StatusBar
)
from models.diffie_hellman import dh_compute, is_prime, is_primitive_root


class DHView(ctk.CTkFrame):
    """
    Giao diện riêng cho Diffie-Hellman.
    Không kế thừa CipherViewBase vì DH không có encrypt/decrypt mà chỉ tính khóa.
    """

    def __init__(self, master, **kw):
        super().__init__(master, fg_color="transparent", **kw)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ─── HEADER ───
        header = CyberCard(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        ctk.CTkLabel(
            header, text="TRAO ĐỔI KHÓA DIFFIE-HELLMAN",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_TITLE_SIZE, weight="bold"),
            text_color=NEON_CYAN
        ).pack(anchor="w", padx=18, pady=(12, 0))
        ctk.CTkLabel(
            header,
            text="Thỏa thuận khóa bí mật chung K qua kênh truyền thông công khai  •  K = Yˣ mod q",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_SMALL),
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", padx=18, pady=(2, 12))

        # ─── LEFT: PARAMS + RESULT ───
        left = CyberCard(self)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
        left.grid_rowconfigure(5, weight=1)
        left.grid_columnconfigure(0, weight=1)

        # Tham số chung
        ctk.CTkLabel(
            left, text="⚙️ THAM SỐ CHUNG:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(15, 4))

        p1 = ctk.CTkFrame(left, fg_color="transparent")
        p1.grid(row=1, column=0, sticky="ew", padx=18)

        fq = ctk.CTkFrame(p1, fg_color="transparent")
        fq.pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkLabel(fq, text="Số nguyên tố q:",
                     font=ctk.CTkFont(size=FONT_SMALL), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.q_ent = GlowEntry(fq)
        self.q_ent.pack(fill="x")
        self.q_ent.insert(0, "353")

        fa = ctk.CTkFrame(p1, fg_color="transparent")
        fa.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(fa, text="Nguyên căn α:",
                     font=ctk.CTkFont(size=FONT_SMALL), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.alpha_ent = GlowEntry(fa)
        self.alpha_ent.pack(fill="x")
        self.alpha_ent.insert(0, "3")

        # Khóa riêng
        ctk.CTkLabel(
            left, text="🔐 KHÓA RIÊNG:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=TEXT_PRIMARY
        ).grid(row=2, column=0, sticky="w", padx=18, pady=(12, 4))

        p2 = ctk.CTkFrame(left, fg_color="transparent")
        p2.grid(row=3, column=0, sticky="ew", padx=18)

        fxa = ctk.CTkFrame(p2, fg_color="transparent")
        fxa.pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkLabel(fxa, text="Khóa riêng XA (Bên A):",
                     font=ctk.CTkFont(size=FONT_SMALL), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.xa_ent = GlowEntry(fxa)
        self.xa_ent.pack(fill="x")
        self.xa_ent.insert(0, "97")

        fxb = ctk.CTkFrame(p2, fg_color="transparent")
        fxb.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(fxb, text="Khóa riêng XB (Bên B):",
                     font=ctk.CTkFont(size=FONT_SMALL), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.xb_ent = GlowEntry(fxb)
        self.xb_ent.pack(fill="x")
        self.xb_ent.insert(0, "233")

        # Button
        NeonButton(
            left, text="⚡  TÍNH TOÁN & ĐỒNG THUẬN KHÓA",
            neon_color=NEON_CYAN, hover=HOVER_CYAN,
            text_color="#000000",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BUTTON, weight="bold"),
            command=self._run
        ).grid(row=4, column=0, sticky="ew", padx=18, pady=12)

        # Result
        ctk.CTkLabel(
            left, text="📤 KẾT QUẢ:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=NEON_GREEN
        ).grid(row=5, column=0, sticky="nw", padx=18, pady=(0, 4))

        self.out_box = GlowTextbox(left, height=140)
        self.out_box.grid(row=5, column=0, sticky="nsew", padx=18, pady=(25, 8))

        self.status = StatusBar(left)
        self.status.grid(row=6, column=0, sticky="ew", padx=18, pady=(0, 12))

        # ─── RIGHT: ANALYSIS ───
        right = CyberCard(self)
        right.grid(row=1, column=1, sticky="nsew", padx=(6, 0))
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            right, text="📊 PHÂN TÍCH TRAO ĐỔI KHÓA:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=FONT_BODY, weight="bold"),
            text_color=NEON_CYAN
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 5))

        self.log_box = GlowTextbox(
            right, text_color=NEON_CYAN,
            font=ctk.CTkFont(family=FONT_MONO, size=FONT_SMALL)
        )
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 12))
        self.log_box.insert("1.0", "Nhấn TÍNH TOÁN để xem quá trình trao đổi khóa chi tiết.")

    def _run(self):
        try:
            q = int(self.q_ent.get().strip())
            alpha = int(self.alpha_ent.get().strip())
            xa = int(self.xa_ent.get().strip())
            xb = int(self.xb_ent.get().strip())
        except ValueError:
            self.status.show_error("Tất cả tham số phải là số nguyên!")
            return

        if not is_prime(q):
            self.status.show_error(f"q={q} không phải là số nguyên tố!")
            return
        if not is_primitive_root(alpha, q):
            self.status.show_error(f"α={alpha} không phải là nguyên căn của {q}!")
            return
        if xa >= q or xb >= q:
            self.status.show_error("Khóa riêng XA và XB phải nhỏ hơn q!")
            return

        ya, yb, ka, kb, log = dh_compute(q, alpha, xa, xb)

        out = f"• Khóa công khai Bên A (YA) = {ya}\n"
        out += f"• Khóa công khai Bên B (YB) = {yb}\n"
        out += "──────────────────────────────────────\n"
        out += f"➔ KHÓA BÍ MẬT ĐỒNG THUẬN CHUNG: K = {ka}"

        self.out_box.delete("1.0", "end")
        self.out_box.insert("1.0", out)
        self.log_box.delete("1.0", "end")
        self.log_box.insert("1.0", log)
        self.status.show_success(f"Đồng thuận khóa thành công! K = {ka}")
