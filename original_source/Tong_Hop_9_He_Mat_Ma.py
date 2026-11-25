"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                     CHƯƠNG TRÌNH TỔNG HỢP 9 HỆ MẬT MÃ                          ║
║               GIAO DIỆN HIỆN ĐẠI BẰNG CUSTOMTKINTER (ULTRA-PRO UI)             ║
║   Caesar | Affine | Hill | Vigenère | Playfair | Hàng | DES | RSA | D-H        ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import math
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Thiết lập theme hiện đại
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ═════════════════════════════════════════════════════════════
# THUẬT TOÁN 9 HỆ MẬT MÃ
# ═════════════════════════════════════════════════════════════

# --- 1. CAESAR ---
def caesar_cipher(text, k, decrypt=False):
    shift = (-k if decrypt else k) % 26
    r = []
    for c in text:
        if c.isupper():
            r.append(chr((ord(c) - 65 + shift) % 26 + 65))
        elif c.islower():
            r.append(chr((ord(c) - 97 + shift) % 26 + 97))
        else:
            r.append(c)
    return "".join(r)

# --- 2. AFFINE ---
def affine_mod_inv(a, m=26):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None

def affine_cipher(text, a, b, decrypt=False):
    a = a % 26
    b = b % 26
    if math.gcd(a, 26) != 1:
        return None, "ƯCLN(a, 26) != 1. Khóa 'a' không hợp lệ!"
    if decrypt:
        a_inv = affine_mod_inv(a, 26)
        if a_inv is None:
            return None, "Không tìm thấy nghịch đảo của a mod 26!"
        r = []
        for c in text:
            if c.isupper():
                r.append(chr((a_inv * (ord(c) - 65 - b)) % 26 + 65))
            elif c.islower():
                r.append(chr((a_inv * (ord(c) - 97 - b)) % 26 + 97))
            else:
                r.append(c)
        return "".join(r), None
    else:
        r = []
        for c in text:
            if c.isupper():
                r.append(chr((a * (ord(c) - 65) + b) % 26 + 65))
            elif c.islower():
                r.append(chr((a * (ord(c) - 97) + b) % 26 + 97))
            else:
                r.append(c)
        return "".join(r), None

# --- 3. HILL ---
def hill_minor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

def hill_det(m):
    if len(m) == 1: return m[0][0]
    if len(m) == 2: return m[0][0]*m[1][1] - m[0][1]*m[1][0]
    det = 0
    for c in range(len(m)):
        det += ((-1)**c) * m[0][c] * hill_det(hill_minor(m, 0, c))
    return det

def hill_adjugate(m):
    if len(m) == 1: return [[1]]
    adj = []
    for i in range(len(m)):
        row = []
        for j in range(len(m)):
            sign = (-1)**(i+j)
            row.append(sign * hill_det(hill_minor(m, j, i)))
        adj.append(row)
    return adj

def hill_cipher(text, K, decrypt=False):
    t = "".join([c.upper() for c in text if c.isalpha()])
    m = len(K)
    det_K = hill_det(K) % 26
    if math.gcd(det_K, 26) != 1:
        return None, None, f"Định thức Det(K) = {det_K} không nguyên tố cùng nhau với 26 (ƯCLN != 1)!"

    log = f"═══ BẢNG PHÂN TÍCH MA TRẬN HILL ({'GIẢI MÃ' if decrypt else 'MÃ HÓA'}) ═══\n"
    log += f"• Cấp ma trận: {m}x{m}\n"
    log += f"• Det(K) = {det_K} (Hợp lệ trên Z26)\n"

    if decrypt:
        det_inv = pow(det_K, -1, 26)
        adj_K = hill_adjugate(K)
        K_work = [[(det_inv * val) % 26 for val in row] for row in adj_K]
        log += f"• Det(K)^-1 mod 26 = {det_inv}\n"
        log += "• Ma trận giải mã K^-1 mod 26:\n"
    else:
        K_work = [[val % 26 for val in row] for row in K]
        log += "• Ma trận mã hóa K mod 26:\n"

    for row in K_work:
        log += "  │ " + "  ".join([f"{x:3d}" for x in row]) + " │\n"
    log += "──────────────────────────────────────────────\n"

    if len(t) % m != 0:
        pad = m - (len(t) % m)
        t += 'X' * pad
        log += f"• Đã thêm {pad} ký tự 'X' đệm để chia hết cho cấp {m}.\n"

    res = ""
    for i in range(0, len(t), m):
        block = [ord(c) - 65 for c in t[i:i+m]]
        res_block = []
        for col in range(m):
            val = sum(block[row] * K_work[row][col] for row in range(m)) % 26
            res_block.append(val)
            res += chr(val + 65)
        log += f"  [{', '.join(t[i:i+m])}] ──> [{', '.join([chr(v+65) for v in res_block])}]\n"

    if decrypt:
        res = res.rstrip('X')
    return res, log, None

# --- 4. VIGENÈRE ---
def vigenere_cipher(text, key, decrypt=False):
    key = key.upper()
    r = []
    k_idx = 0
    for c in text:
        if c.isalpha():
            offset = 65 if c.isupper() else 97
            shift = ord(key[k_idx % len(key)]) - 65
            if decrypt:
                r.append(chr((ord(c) - offset - shift) % 26 + offset))
            else:
                r.append(chr((ord(c) - offset + shift) % 26 + offset))
            k_idx += 1
        else:
            r.append(c)
    return "".join(r)

# --- 5. PLAYFAIR ---
def playfair_matrix(kw):
    kw = kw.upper().replace('J', 'I')
    m = ""
    for c in kw + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c.isalpha() and c not in m:
            m += c
    return m

def playfair_cipher(text, kw, decrypt=False):
    m = playfair_matrix(kw)
    t = "".join([c.upper() for c in text if c.isalpha()]).replace('J', 'I')

    if not decrypt:
        res, i = "", 0
        while i < len(t):
            a = t[i]
            if i + 1 < len(t):
                b = t[i + 1]
                if a == b:
                    res += a + 'X'; i += 1
                else:
                    res += a + b; i += 2
            else:
                res += a + 'X'; i += 1
        t = res
    else:
        if len(t) % 2 != 0:
            t += 'X'

    out = ""
    d = -1 if decrypt else 1
    for i in range(0, len(t), 2):
        r1, c1 = m.index(t[i]) // 5, m.index(t[i]) % 5
        r2, c2 = m.index(t[i+1]) // 5, m.index(t[i+1]) % 5

        if r1 == r2:
            out += m[r1 * 5 + (c1 + d) % 5] + m[r2 * 5 + (c2 + d) % 5]
        elif c1 == c2:
            out += m[((r1 + d) % 5) * 5 + c1] + m[((r2 + d) % 5) * 5 + c2]
        else:
            out += m[r1 * 5 + c2] + m[r2 * 5 + c1]
    return out, m

# --- 6. HOÁN VỊ HÀNG ---
def hang_cipher(text, key, decrypt=False):
    m = len(key)
    rows = math.ceil(len(text) / m)
    log = f"═══ BẢNG PHÂN TÍCH HOÁN VỊ CỘT ({'GIẢI MÃ' if decrypt else 'MÃ HÓA'}) ═══\n"
    log += f"• Khóa K: {' '.join(f'[{x}]' for x in key)}\n"
    log += f"• Số cột: {m} | Số hàng: {rows}\n"
    log += "──────────────────────────────────────────────\n"

    if decrypt:
        base_len = len(text) // m
        rem = len(text) % m
        lengths = [base_len + 1 if i < rem else base_len for i in range(m)]
        sorted_indices = [i for _, i in sorted(zip(key, range(m)))]

        cols = {}
        pos = 0
        for idx in sorted_indices:
            cols[idx] = text[pos : pos + lengths[idx]]
            pos += lengths[idx]

        r = ""
        for row in range(rows):
            row_chars = []
            for i in range(m):
                if row < len(cols[i]):
                    char = cols[i][row]
                    r += char
                    row_chars.append(char)
                else:
                    row_chars.append("*")
            log += "  Hàng " + f"{row+1:2d}:  " + "   ".join(row_chars) + "\n"
        return r, log
    else:
        for row in range(rows):
            row_chars = []
            for col in range(m):
                idx = row * m + col
                row_chars.append(text[idx] if idx < len(text) else "*")
            log += "  Hàng " + f"{row+1:2d}:  " + "   ".join(row_chars) + "\n"

        cols_str = [text[i::m] for i in range(m)]
        sorted_cols = [col for _, col in sorted(zip(key, cols_str))]
        return "".join(sorted_cols), log

# --- 7. DES TIÊU CHUẨN ---
PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
DES_SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
IP_T = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
FP_T = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
E_BOX = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
P_BOX = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
S_BOX = [
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

def des_p(b, tbl): return "".join(b[i - 1] for i in tbl)
def des_sh(b, n): return b[n:] + b[:n]
def des_x(b1, b2): return "".join("1" if b1[i] != b2[i] else "0" for i in range(len(b1)))
def des_to_hex(b): return hex(int(b, 2))[2:].upper().zfill(len(b)//4)

def des_cipher(msg, key_hex, decrypt=False):
    try:
        key_bin = bin(int(key_hex, 16))[2:].zfill(64)
    except:
        return None, None, "Khóa K chỉ gồm ký tự Hex (0-9, A-F)!"

    # Sinh khóa
    pc1_res = des_p(key_bin, PC1)
    C, D = pc1_res[:28], pc1_res[28:]
    subkeys = []
    log_key = "═══ BƯỚC 1: SINH 16 KHÓA CON (SUBKEYS) ═══\n"
    for i in range(16):
        C, D = des_sh(C, DES_SHIFTS[i]), des_sh(D, DES_SHIFTS[i])
        sk = des_p(C + D, PC2)
        subkeys.append(sk)
        log_key += f"  K{i+1:02d}: {des_to_hex(sk)}\n"

    if decrypt:
        try:
            msg_bin = bin(int(msg, 16))[2:].zfill(len(msg)*4)
        except:
            return None, None, "Giải mã DES yêu cầu Ciphertext là chuỗi Hex!"
        work_keys = subkeys[::-1]
    else:
        raw_b = msg.encode('utf-8')
        pad_len = 8 - (len(raw_b) % 8)
        raw_b += bytes([pad_len] * pad_len)
        msg_bin = "".join(format(b, '08b') for b in raw_b)
        work_keys = subkeys

    out_bin = ""
    log_detail = log_key + "\n═══ CHI TIẾT 16 VÒNG LẶP FEISTEL (KHỐI 1) ═══\n"
    for block_idx in range(0, len(msg_bin), 64):
        blk = msg_bin[block_idx:block_idx+64]
        ip_r = des_p(blk, IP_T)
        L, R = ip_r[:32], ip_r[32:]
        for i in range(16):
            L_prev, R_prev = L, R
            e_r = des_p(R_prev, E_BOX)
            xor_r = des_x(e_r, work_keys[i])
            s_r = ""
            for j in range(8):
                chunk = xor_r[j*6:(j+1)*6]
                row = int(chunk[0] + chunk[5], 2)
                col = int(chunk[1:5], 2)
                s_r += bin(S_BOX[j][row][col])[2:].zfill(4)
            f_r = des_p(s_r, P_BOX)
            L = R_prev
            R = des_x(L_prev, f_r)
            if block_idx == 0:
                log_detail += f"  [Vòng {i+1:2d}] L = {des_to_hex(L)} │ R = {des_to_hex(R)}\n"
        out_bin += des_p(R + L, FP_T)

    if decrypt:
        try:
            out_bytes = int(out_bin, 2).to_bytes(len(out_bin) // 8, byteorder='big')
            pad = out_bytes[-1]
            return out_bytes[:-pad].decode('utf-8', errors='ignore'), log_detail, None
        except Exception as e:
            return None, None, f"Lỗi giải mã DES: {e}"
    else:
        return des_to_hex(out_bin), log_detail, None

# --- 8. RSA ---
def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def rsa_cipher(msg, p, q, e, decrypt=False):
    n = p * q
    phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        return None, None, f"e={e} và phi={phi} không nguyên tố cùng nhau (ƯCLN != 1)!"

    d = pow(e, -1, phi)
    log = f"═══ THÔNG SỐ KHÓA RSA ═══\n"
    log += f"• p = {p}, q = {q}\n"
    log += f"• Modulus n = p * q = {n}\n"
    log += f"• Phi(n) = (p-1)*(q-1) = {phi}\n"
    log += f"• Khóa công khai KU = {{e: {e}, n: {n}}}\n"
    log += f"• Khóa riêng tư KR = {{d: {d}, n: {n}}}\n"
    log += "──────────────────────────────────────────────\n"

    if decrypt:
        try:
            ciphers = [int(x) for x in msg.split()]
            plain = "".join(chr(pow(c, d, n)) for c in ciphers)
            log += "• Chi tiết giải mã từng khối M = C^d mod n:\n"
            for c in ciphers:
                m_val = pow(c, d, n)
                log += f"  C = {c:4d} ──> M = {m_val:4d} ('{chr(m_val)}')\n"
            return plain, log, None
        except Exception as ex:
            return None, None, f"Lỗi giải mã RSA: {ex}"
    else:
        log += "• Chi tiết mã hóa từng ký tự C = M^e mod n:\n"
        nums = [ord(c) for c in msg]
        ciphers = []
        for c, m_val in zip(msg, nums):
            c_val = pow(m_val, e, n)
            ciphers.append(c_val)
            log += f"  '{c}' (ASCII {m_val:3d}) ──> C = {m_val}^{e} mod {n} = {c_val}\n"
        return " ".join(map(str, ciphers)), log, None

# --- 9. DIFFIE-HELLMAN ---
def is_primitive_root(alpha, q):
    if alpha <= 1 or alpha >= q: return False
    phi = q - 1
    factors = set()
    n = phi
    while n % 2 == 0: factors.add(2); n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0: factors.add(i); n //= i
        i += 2
    if n > 2: factors.add(n)
    for p in factors:
        if pow(alpha, phi // p, q) == 1: return False
    return True


# ═════════════════════════════════════════════════════════════
# GIAO DIỆN HIỆN ĐẠI CUSTOMTKINTER
# ═════════════════════════════════════════════════════════════
class ModernCryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ HỆ THỐNG MẬT MÃ TOÀN DIỆN - 9 THUẬT TOÁN")
        self.geometry("1200x780")
        self.minsize(1050, 700)

        # Layout chính: 2 cột (Sidebar bên trái, Workspace bên phải)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ─── SIDEBAR TRÁI ───
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(11, weight=1)

        # Logo Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="🛡️ CRYPTO SUITE",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#38bdf8"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 5), sticky="w")

        self.sub_logo = ctk.CTkLabel(
            self.sidebar, text="Hệ thống phân tích 9 thuật toán",
            font=ctk.CTkFont(size=12), text_color="#94a3b8"
        )
        self.sub_logo.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Nút chuyển đổi giao diện 9 hệ mật mã
        self.ciphers = [
            ("🅰  Mã Caesar", "caesar"),
            ("🔣  Mã Affine", "affine"),
            ("📊  Mã Hill (Ma Trận)", "hill"),
            ("🔤  Mã Vigenère", "vigenere"),
            ("🔲  Mã Playfair (5x5)", "playfair"),
            ("📋  Mã Hoán Vị Hàng", "hang"),
            ("🔒  Mã Khối DES", "des"),
            ("🔑  Mã Khóa RSA", "rsa"),
            ("🤝  Trao Đổi Khóa D-H", "dh"),
        ]

        self.nav_buttons = {}
        for idx, (label, key) in enumerate(self.ciphers, start=2):
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                font=ctk.CTkFont(size=13, weight="bold"),
                height=40, corner_radius=8,
                fg_color="transparent", text_color="#cbd5e1",
                hover_color="#1e293b",
                command=lambda k=key: self.select_cipher(k)
            )
            btn.grid(row=idx, column=0, padx=12, pady=3, sticky="ew")
            self.nav_buttons[key] = btn

        # Chế độ sáng / tối ở góc dưới sidebar
        self.theme_label = ctk.CTkLabel(self.sidebar, text="Chế độ hiển thị:", font=ctk.CTkFont(size=11), text_color="#64748b")
        self.theme_label.grid(row=12, column=0, padx=20, pady=(10, 0), sticky="w")
        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar, values=["Dark", "Light", "System"],
            command=self.change_theme, height=32, corner_radius=6
        )
        self.theme_menu.grid(row=13, column=0, padx=15, pady=(2, 20), sticky="ew")

        # ─── VÙNG LÀM VIỆC CHÍNH (WORKSPACE) ───
        self.frames = {}

        # Khởi tạo từng trang giải thuật
        self._init_caesar_view()
        self._init_affine_view()
        self._init_hill_view()
        self._init_vigenere_view()
        self._init_playfair_view()
        self._init_hang_view()
        self._init_des_view()
        self._init_rsa_view()
        self._init_dh_view()

        # Mở tab mặc định
        self.select_cipher("caesar")

    def change_theme(self, new_theme):
        ctk.set_appearance_mode(new_theme)

    def select_cipher(self, key):
        for k, frame in self.frames.items():
            if k == key:
                frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            else:
                frame.grid_forget()

        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color="#0284c7", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color="#cbd5e1")

    # ─── HELPER TẠO KHUNG BỐ CỤC ───
    def _create_base_view(self, key, title, desc):
        view = ctk.CTkFrame(self, corner_radius=12, fg_color="transparent")
        self.frames[key] = view

        # Header card
        header = ctk.CTkFrame(view, corner_radius=10, fg_color=("#f1f5f9", "#1e293b"))
        header.pack(fill="x", pady=(0, 15), ipady=8)
        
        lbl_t = ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=18, weight="bold"), text_color=("#0284c7", "#38bdf8"))
        lbl_t.pack(anchor="w", padx=15, pady=(5, 0))
        lbl_d = ctk.CTkLabel(header, text=desc, font=ctk.CTkFont(size=12), text_color=("#64748b", "#94a3b8"))
        lbl_d.pack(anchor="w", padx=15, pady=(0, 5))

        return view

    def _file_open_to(self, target_widget):
        p = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if p:
            try:
                with open(p, "r", encoding="utf-8") as f: data = f.read()
                if isinstance(target_widget, ctk.CTkEntry):
                    target_widget.delete(0, "end"); target_widget.insert(0, data)
                else:
                    target_widget.delete("1.0", "end"); target_widget.insert("1.0", data)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def _file_save_from(self, target_widget):
        val = target_widget.get() if isinstance(target_widget, ctk.CTkEntry) else target_widget.get("1.0", "end").strip()
        if not val: return messagebox.showwarning("Cảnh báo", "Không có nội dung để lưu!")
        p = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if p:
            with open(p, "w", encoding="utf-8") as f: f.write(val)
            messagebox.showinfo("Thành công", "Đã lưu kết quả thành công!")

    def _copy_from(self, target_widget):
        val = target_widget.get() if isinstance(target_widget, ctk.CTkEntry) else target_widget.get("1.0", "end").strip()
        if val:
            self.clipboard_clear()
            self.clipboard_append(val)
            messagebox.showinfo("Sao chép", "Đã chép nội dung vào Clipboard!")

    # ═════════════════════════════════════════════════════════
    # 1. VIEW CAESAR
    # ═════════════════════════════════════════════════════════
    def _init_caesar_view(self):
        v = self._create_base_view("caesar", "MÃ HÓA CAESAR", "Thuật toán thay thế vòng tròn: C = (P + k) mod 26")
        
        card = ctk.CTkFrame(v, corner_radius=10)
        card.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(card, text="Văn bản đầu vào (Plaintext / Ciphertext):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.caesar_in = ctk.CTkEntry(card, height=40, placeholder_text="Nhập văn bản cần xử lý...")
        self.caesar_in.pack(fill="x", padx=15, pady=5)
        self.caesar_in.insert(0, "HELLO CAESAR CIPHER")

        ctk.CTkLabel(card, text="Khóa dịch chuyển K (Số nguyên):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.caesar_k = ctk.CTkEntry(card, height=40, placeholder_text="Ví dụ: 3")
        self.caesar_k.pack(fill="x", padx=15, pady=5)
        self.caesar_k.insert(0, "3")

        # Nút thao tác
        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(fill="x", padx=15, pady=12)
        ctk.CTkButton(btn_bar, text="🔒 Mã Hóa", fg_color="#10b981", hover_color="#059669", height=38, width=120, command=self._run_caesar_enc).pack(side="left", padx=5)
        ctk.CTkButton(btn_bar, text="🔓 Giải Mã", fg_color="#3b82f6", hover_color="#2563eb", height=38, width=120, command=self._run_caesar_dec).pack(side="left", padx=5)
        ctk.CTkButton(btn_bar, text="📂 Mở File", fg_color="#64748b", hover_color="#475569", height=38, width=100, command=lambda: self._file_open_to(self.caesar_in)).pack(side="left", padx=5)

        ctk.CTkLabel(card, text="Kết quả đầu ra:", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(10, 2))
        self.caesar_out = ctk.CTkTextbox(card, height=120, font=ctk.CTkFont(family="Consolas", size=13))
        self.caesar_out.pack(fill="both", expand=True, padx=15, pady=5)

        action_bar = ctk.CTkFrame(card, fg_color="transparent")
        action_bar.pack(fill="x", padx=15, pady=(5, 15))
        ctk.CTkButton(action_bar, text="📋 Sao Chép", height=34, width=110, command=lambda: self._copy_from(self.caesar_out)).pack(side="left", padx=5)
        ctk.CTkButton(action_bar, text="💾 Lưu File", height=34, width=110, command=lambda: self._file_save_from(self.caesar_out)).pack(side="left", padx=5)

    def _run_caesar_enc(self):
        t = self.caesar_in.get().strip()
        try: k = int(self.caesar_k.get().strip())
        except: return messagebox.showerror("Lỗi", "Khóa K phải là số nguyên!")
        res = caesar_cipher(t, k, False)
        self.caesar_out.delete("1.0", "end"); self.caesar_out.insert("1.0", res)

    def _run_caesar_dec(self):
        t = self.caesar_in.get().strip()
        try: k = int(self.caesar_k.get().strip())
        except: return messagebox.showerror("Lỗi", "Khóa K phải là số nguyên!")
        res = caesar_cipher(t, k, True)
        self.caesar_out.delete("1.0", "end"); self.caesar_out.insert("1.0", res)

    # ═════════════════════════════════════════════════════════
    # 2. VIEW AFFINE
    # ═════════════════════════════════════════════════════════
    def _init_affine_view(self):
        v = self._create_base_view("affine", "MÃ HÓA AFFINE", "Hệ mật mã kết hợp phép nhân và dịch chuyển: C = (a*P + b) mod 26")
        card = ctk.CTkFrame(v, corner_radius=10)
        card.pack(fill="both", expand=True)

        ctk.CTkLabel(card, text="Văn bản đầu vào:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.affine_in = ctk.CTkEntry(card, height=40)
        self.affine_in.pack(fill="x", padx=15, pady=5)
        self.affine_in.insert(0, "AFFINE CIPHER EXAMPLE")

        k_row = ctk.CTkFrame(card, fg_color="transparent")
        k_row.pack(fill="x", padx=15, pady=5)
        
        k1 = ctk.CTkFrame(k_row, fg_color="transparent"); k1.pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkLabel(k1, text="Khóa a (ƯCLN(a, 26) = 1):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.affine_a = ctk.CTkEntry(k1, height=38); self.affine_a.pack(fill="x", pady=3); self.affine_a.insert(0, "7")

        k2 = ctk.CTkFrame(k_row, fg_color="transparent"); k2.pack(side="left", expand=True, fill="x", padx=(10, 0))
        ctk.CTkLabel(k2, text="Khóa b (Dịch chuyển):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.affine_b = ctk.CTkEntry(k2, height=38); self.affine_b.pack(fill="x", pady=3); self.affine_b.insert(0, "3")

        btn_bar = ctk.CTkFrame(card, fg_color="transparent")
        btn_bar.pack(fill="x", padx=15, pady=12)
        ctk.CTkButton(btn_bar, text="🔒 Mã Hóa", fg_color="#10b981", hover_color="#059669", height=38, width=120, command=self._run_affine_enc).pack(side="left", padx=5)
        ctk.CTkButton(btn_bar, text="🔓 Giải Mã", fg_color="#3b82f6", hover_color="#2563eb", height=38, width=120, command=self._run_affine_dec).pack(side="left", padx=5)
        ctk.CTkButton(btn_bar, text="📂 Mở File", fg_color="#64748b", hover_color="#475569", height=38, width=100, command=lambda: self._file_open_to(self.affine_in)).pack(side="left", padx=5)

        ctk.CTkLabel(card, text="Kết quả đầu ra:", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(10, 2))
        self.affine_out = ctk.CTkTextbox(card, height=120, font=ctk.CTkFont(family="Consolas", size=13))
        self.affine_out.pack(fill="both", expand=True, padx=15, pady=5)

        action_bar = ctk.CTkFrame(card, fg_color="transparent")
        action_bar.pack(fill="x", padx=15, pady=(5, 15))
        ctk.CTkButton(action_bar, text="📋 Sao Chép", height=34, width=110, command=lambda: self._copy_from(self.affine_out)).pack(side="left", padx=5)
        ctk.CTkButton(action_bar, text="💾 Lưu File", height=34, width=110, command=lambda: self._file_save_from(self.affine_out)).pack(side="left", padx=5)

    def _run_affine_enc(self):
        t = self.affine_in.get().strip()
        try: a, b = int(self.affine_a.get().strip()), int(self.affine_b.get().strip())
        except: return messagebox.showerror("Lỗi", "Khóa a và b phải là số nguyên!")
        r, err = affine_cipher(t, a, b, False)
        if err: return messagebox.showerror("Lỗi", err)
        self.affine_out.delete("1.0", "end"); self.affine_out.insert("1.0", r)

    def _run_affine_dec(self):
        t = self.affine_in.get().strip()
        try: a, b = int(self.affine_a.get().strip()), int(self.affine_b.get().strip())
        except: return messagebox.showerror("Lỗi", "Khóa a và b phải là số nguyên!")
        r, err = affine_cipher(t, a, b, True)
        if err: return messagebox.showerror("Lỗi", err)
        self.affine_out.delete("1.0", "end"); self.affine_out.insert("1.0", r)

    # ═════════════════════════════════════════════════════════
    # 3. VIEW HILL (KÈM PHÂN TÍCH MA TRẬN)
    # ═════════════════════════════════════════════════════════
    def _init_hill_view(self):
        v = self._create_base_view("hill", "MÃ HÓA HILL (NHẬP MA TRẬN TỰ DO)", "Mã hóa ma trận đa bảng chữ cái: C = P * K mod 26")
        split_box = ctk.CTkFrame(v, fg_color="transparent")
        split_box.pack(fill="both", expand=True)

        # Cột trái
        left = ctk.CTkFrame(split_box, corner_radius=10)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(left, text="Văn bản đầu vào (Chỉ chữ cái):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.hill_in = ctk.CTkEntry(left, height=38); self.hill_in.pack(fill="x", padx=15, pady=5); self.hill_in.insert(0, "ACT")

        sz_row = ctk.CTkFrame(left, fg_color="transparent"); sz_row.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(sz_row, text="Cấp ma trận n:", font=ctk.CTkFont(weight="bold")).pack(side="left")
        self.hill_n = ctk.CTkEntry(sz_row, width=50, height=32, justify="center"); self.hill_n.pack(side="left", padx=8); self.hill_n.insert(0, "3")
        ctk.CTkButton(sz_row, text="Tạo Lưới", width=80, height=32, fg_color="#f59e0b", hover_color="#d97706", command=self._update_hill_grid).pack(side="left")

        self.hill_grid_frame = ctk.CTkFrame(left, fg_color="transparent")
        self.hill_grid_frame.pack(fill="x", padx=15, pady=5)
        self.hill_entries = []
        self._update_hill_grid()

        btn_bar = ctk.CTkFrame(left, fg_color="transparent"); btn_bar.pack(fill="x", padx=15, pady=8)
        ctk.CTkButton(btn_bar, text="🔒 Mã Hóa", fg_color="#10b981", hover_color="#059669", height=36, width=110, command=lambda: self._run_hill(False)).pack(side="left", padx=4)
        ctk.CTkButton(btn_bar, text="🔓 Giải Mã", fg_color="#3b82f6", hover_color="#2563eb", height=36, width=110, command=lambda: self._run_hill(True)).pack(side="left", padx=4)

        ctk.CTkLabel(left, text="Kết quả:", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(5, 2))
        self.hill_out = ctk.CTkTextbox(left, height=80, font=ctk.CTkFont(family="Consolas", size=13))
        self.hill_out.pack(fill="both", expand=True, padx=15, pady=(2, 15))

        # Cột phải (Phân tích)
        right = ctk.CTkFrame(split_box, corner_radius=10)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(right, text="Bảng Phân Tích Định Thức & Ma Trận Nghịch Đảo:", font=ctk.CTkFont(weight="bold"), text_color="#38bdf8").pack(anchor="w", padx=15, pady=(10, 5))
        self.hill_log = ctk.CTkTextbox(right, font=ctk.CTkFont(family="Consolas", size=12), text_color="#38bdf8")
        self.hill_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.hill_log.insert("1.0", "Nhấn Mã Hóa hoặc Giải Mã để theo dõi chi tiết ma trận K^-1 và từng khối ký tự.")

    def _update_hill_grid(self):
        for w in self.hill_grid_frame.winfo_children(): w.destroy()
        self.hill_entries.clear()
        try:
            n = int(self.hill_n.get().strip())
            if n < 2 or n > 6: raise ValueError
        except:
            return messagebox.showerror("Lỗi", "Cấp ma trận từ 2 đến 6!")
        
        default_3x3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
        for i in range(n):
            rf = ctk.CTkFrame(self.hill_grid_frame, fg_color="transparent")
            rf.pack(anchor="w", pady=2)
            row = []
            for j in range(n):
                e = ctk.CTkEntry(rf, width=50, height=32, justify="center", font=ctk.CTkFont(family="Consolas", weight="bold"))
                e.pack(side="left", padx=2)
                if n == 3: e.insert(0, str(default_3x3[i][j]))
                else: e.insert(0, "1" if i == j else "0")
                row.append(e)
            self.hill_entries.append(row)

    def _run_hill(self, is_dec):
        t = self.hill_in.get().strip()
        if not t: return messagebox.showwarning("Cảnh báo", "Nhập văn bản!")
        try:
            K = []
            for r in self.hill_entries:
                row_vals = []
                for e in r:
                    val = e.get().strip()
                    if not val: raise ValueError
                    row_vals.append(int(val))
                K.append(row_vals)
        except:
            return messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ số nguyên vào ma trận!")

        res, log, err = hill_cipher(t, K, is_dec)
        if err: return messagebox.showerror("Lỗi Toán Học", err)
        self.hill_out.delete("1.0", "end"); self.hill_out.insert("1.0", res)
        self.hill_log.delete("1.0", "end"); self.hill_log.insert("1.0", log)

    # ═════════════════════════════════════════════════════════
    # 4. VIEW VIGENÈRE
    # ═════════════════════════════════════════════════════════
    def _init_vigenere_view(self):
        v = self._create_base_view("vigenere", "MÃ HÓA VIGENÈRE", "Mã hóa đa bảng chữ cái dùng từ khóa tuần hoàn: C_i = (P_i + K_i) mod 26")
        card = ctk.CTkFrame(v, corner_radius=10); card.pack(fill="both", expand=True)

        ctk.CTkLabel(card, text="Văn bản đầu vào:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.vig_in = ctk.CTkEntry(card, height=40); self.vig_in.pack(fill="x", padx=15, pady=5); self.vig_in.insert(0, "ATTACK AT DAWN")

        ctk.CTkLabel(card, text="Khóa K (Chuỗi chữ cái):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.vig_k = ctk.CTkEntry(card, height=40); self.vig_k.pack(fill="x", padx=15, pady=5); self.vig_k.insert(0, "LEMON")

        btn_bar = ctk.CTkFrame(card, fg_color="transparent"); btn_bar.pack(fill="x", padx=15, pady=12)
        ctk.CTkButton(btn_bar, text="🔒 Mã Hóa", fg_color="#10b981", hover_color="#059669", height=38, width=120, command=lambda: self._run_vig(False)).pack(side="left", padx=5)
        ctk.CTkButton(btn_bar, text="🔓 Giải Mã", fg_color="#3b82f6", hover_color="#2563eb", height=38, width=120, command=lambda: self._run_vig(True)).pack(side="left", padx=5)

        ctk.CTkLabel(card, text="Kết quả đầu ra:", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(10, 2))
        self.vig_out = ctk.CTkTextbox(card, height=120, font=ctk.CTkFont(family="Consolas", size=13))
        self.vig_out.pack(fill="both", expand=True, padx=15, pady=5)

        action_bar = ctk.CTkFrame(card, fg_color="transparent"); action_bar.pack(fill="x", padx=15, pady=(5, 15))
        ctk.CTkButton(action_bar, text="📋 Sao Chép", height=34, width=110, command=lambda: self._copy_from(self.vig_out)).pack(side="left", padx=5)
        ctk.CTkButton(action_bar, text="💾 Lưu File", height=34, width=110, command=lambda: self._file_save_from(self.vig_out)).pack(side="left", padx=5)

    def _run_vig(self, is_dec):
        t = self.vig_in.get().strip(); k = self.vig_k.get().strip()
        if not t or not k: return messagebox.showwarning("Cảnh báo", "Nhập đủ văn bản và khóa!")
        if not k.isalpha(): return messagebox.showerror("Lỗi", "Khóa Vigenère chỉ gồm chữ cái!")
        r = vigenere_cipher(t, k, is_dec)
        self.vig_out.delete("1.0", "end"); self.vig_out.insert("1.0", r)

    # ═════════════════════════════════════════════════════════
    # 5. VIEW PLAYFAIR
    # ═════════════════════════════════════════════════════════
    def _init_playfair_view(self):
        v = self._create_base_view("playfair", "MÃ HÓA PLAYFAIR (5x5)", "Mã hóa cặp 2 chữ cái với ma trận khóa 5x5 kết hợp I/J")
        split_box = ctk.CTkFrame(v, fg_color="transparent"); split_box.pack(fill="both", expand=True)

        left = ctk.CTkFrame(split_box, corner_radius=10); left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(left, text="Văn bản đầu vào:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.pf_in = ctk.CTkEntry(left, height=40); self.pf_in.pack(fill="x", padx=15, pady=5); self.pf_in.insert(0, "BALLOON")

        ctk.CTkLabel(left, text="Từ khóa K (Keyword):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.pf_kw = ctk.CTkEntry(left, height=40); self.pf_kw.pack(fill="x", padx=15, pady=5); self.pf_kw.insert(0, "MONARCHY")

        btn_bar = ctk.CTkFrame(left, fg_color="transparent"); btn_bar.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(btn_bar, text="🔒 Mã Hóa", fg_color="#10b981", hover_color="#059669", height=38, width=110, command=lambda: self._run_pf(False)).pack(side="left", padx=4)
        ctk.CTkButton(btn_bar, text="🔓 Giải Mã", fg_color="#3b82f6", hover_color="#2563eb", height=38, width=110, command=lambda: self._run_pf(True)).pack(side="left", padx=4)

        ctk.CTkLabel(left, text="Kết quả:", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(5, 2))
        self.pf_out = ctk.CTkTextbox(left, height=100, font=ctk.CTkFont(family="Consolas", size=13))
        self.pf_out.pack(fill="both", expand=True, padx=15, pady=(2, 15))

        right = ctk.CTkFrame(split_box, corner_radius=10); right.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(right, text="Ma Trận Khóa 5x5 Playfair:", font=ctk.CTkFont(weight="bold"), text_color="#38bdf8").pack(anchor="w", padx=15, pady=(10, 5))
        self.pf_grid_lbl = ctk.CTkLabel(right, text="", font=ctk.CTkFont(family="Courier New", size=18, weight="bold"), text_color="#4ade80")
        self.pf_grid_lbl.pack(fill="both", expand=True, padx=15, pady=15)
        self._refresh_pf_preview()

    def _refresh_pf_preview(self):
        kw = self.pf_kw.get().strip() or "KEYWORD"
        m = playfair_matrix(kw)
        grid = "\n\n".join(["     ".join(m[i:i+5]) for i in range(0, 25, 5)])
        self.pf_grid_lbl.configure(text=grid)

    def _run_pf(self, is_dec):
        t = self.pf_in.get().strip(); kw = self.pf_kw.get().strip()
        if not t or not kw: return messagebox.showwarning("Cảnh báo", "Nhập đủ thông tin!")
        r, m = playfair_cipher(t, kw, is_dec)
        self.pf_out.delete("1.0", "end"); self.pf_out.insert("1.0", r)
        self._refresh_pf_preview()

    # ═════════════════════════════════════════════════════════
    # 6. VIEW HOÁN VỊ HÀNG
    # ═════════════════════════════════════════════════════════
    def _init_hang_view(self):
        v = self._create_base_view("hang", "MÃ HÓA HOÁN VỊ HÀNG", "Ghi văn bản theo hàng và trích xuất theo thứ tự cột hoán vị")
        split_box = ctk.CTkFrame(v, fg_color="transparent"); split_box.pack(fill="both", expand=True)

        left = ctk.CTkFrame(split_box, corner_radius=10); left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(left, text="Văn bản đầu vào:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.hang_in = ctk.CTkEntry(left, height=40); self.hang_in.pack(fill="x", padx=15, pady=5); self.hang_in.insert(0, "DEFEND THE EAST WALL")

        ctk.CTkLabel(left, text="Khóa K (Dãy số cách nhau bởi dấu phẩy):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.hang_k = ctk.CTkEntry(left, height=40); self.hang_k.pack(fill="x", padx=15, pady=5); self.hang_k.insert(0, "3, 6, 2, 1, 5, 4")

        btn_bar = ctk.CTkFrame(left, fg_color="transparent"); btn_bar.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(btn_bar, text="🔒 Mã Hóa", fg_color="#10b981", hover_color="#059669", height=38, width=110, command=lambda: self._run_hang(False)).pack(side="left", padx=4)
        ctk.CTkButton(btn_bar, text="🔓 Giải Mã", fg_color="#3b82f6", hover_color="#2563eb", height=38, width=110, command=lambda: self._run_hang(True)).pack(side="left", padx=4)

        ctk.CTkLabel(left, text="Kết quả:", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(5, 2))
        self.hang_out = ctk.CTkTextbox(left, height=100, font=ctk.CTkFont(family="Consolas", size=13))
        self.hang_out.pack(fill="both", expand=True, padx=15, pady=(2, 15))

        right = ctk.CTkFrame(split_box, corner_radius=10); right.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(right, text="Bảng Phân Tích Cột và Hàng:", font=ctk.CTkFont(weight="bold"), text_color="#38bdf8").pack(anchor="w", padx=15, pady=(10, 5))
        self.hang_log = ctk.CTkTextbox(right, font=ctk.CTkFont(family="Consolas", size=12), text_color="#38bdf8")
        self.hang_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _run_hang(self, is_dec):
        t = self.hang_in.get().strip()
        try:
            k = [int(x) for x in self.hang_k.get().replace(',', ' ').split()]
            if not k: raise ValueError
        except:
            return messagebox.showerror("Lỗi", "Khóa K phải là dãy số phân tách bởi dấu phẩy!")
        r, log = hang_cipher(t, k, is_dec)
        self.hang_out.delete("1.0", "end"); self.hang_out.insert("1.0", r)
        self.hang_log.delete("1.0", "end"); self.hang_log.insert("1.0", log)

    # ═════════════════════════════════════════════════════════
    # 7. VIEW DES
    # ═════════════════════════════════════════════════════════
    def _init_des_view(self):
        v = self._create_base_view("des", "MÃ HÓA KHỐI DES (DATA ENCRYPTION STANDARD)", "Mã hóa khối 64-bit qua cấu trúc Feistel 16 vòng lặp với các hộp S-Box")
        split_box = ctk.CTkFrame(v, fg_color="transparent"); split_box.pack(fill="both", expand=True)

        left = ctk.CTkFrame(split_box, corner_radius=10); left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(left, text="Khóa K (16 ký tự Hex = 64-bit):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.des_k = ctk.CTkEntry(left, height=40, font=ctk.CTkFont(family="Consolas", weight="bold")); self.des_k.pack(fill="x", padx=15, pady=5); self.des_k.insert(0, "133457799BBCDFF1")

        ctk.CTkLabel(left, text="Văn bản (Plaintext / Hex):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.des_in = ctk.CTkEntry(left, height=40); self.des_in.pack(fill="x", padx=15, pady=5); self.des_in.insert(0, "VIETNAM")

        btn_bar = ctk.CTkFrame(left, fg_color="transparent"); btn_bar.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(btn_bar, text="🔒 Mã Hóa", fg_color="#10b981", hover_color="#059669", height=38, width=110, command=lambda: self._run_des(False)).pack(side="left", padx=4)
        ctk.CTkButton(btn_bar, text="🔓 Giải Mã", fg_color="#3b82f6", hover_color="#2563eb", height=38, width=110, command=lambda: self._run_des(True)).pack(side="left", padx=4)

        ctk.CTkLabel(left, text="Kết quả đầu ra (Hex / Text):", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(5, 2))
        self.des_out = ctk.CTkTextbox(left, height=100, font=ctk.CTkFont(family="Consolas", size=13))
        self.des_out.pack(fill="both", expand=True, padx=15, pady=(2, 15))

        right = ctk.CTkFrame(split_box, corner_radius=10); right.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(right, text="Theo Dõi 16 Khóa Con & 16 Vòng Lặp Feistel:", font=ctk.CTkFont(weight="bold"), text_color="#38bdf8").pack(anchor="w", padx=15, pady=(10, 5))
        self.des_log = ctk.CTkTextbox(right, font=ctk.CTkFont(family="Consolas", size=11), text_color="#38bdf8")
        self.des_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.des_log.insert("1.0", "Nhấn Mã Hóa hoặc Giải Mã để xem bảng sinh khóa PC1/PC2 và giá trị L_i, R_i từng vòng.")

    def _run_des(self, is_dec):
        msg = self.des_in.get().strip(); k_hex = self.des_k.get().strip().upper()
        if len(k_hex) != 16: return messagebox.showerror("Lỗi", "Khóa K phải đúng 16 ký tự Hex (64-bit)!")
        if not msg: return messagebox.showwarning("Cảnh báo", "Nhập văn bản!")
        r, log, err = des_cipher(msg, k_hex, is_dec)
        if err: return messagebox.showerror("Lỗi", err)
        self.des_out.delete("1.0", "end"); self.des_out.insert("1.0", r)
        self.des_log.delete("1.0", "end"); self.des_log.insert("1.0", log)

    # ═════════════════════════════════════════════════════════
    # 8. VIEW RSA
    # ═════════════════════════════════════════════════════════
    def _init_rsa_view(self):
        v = self._create_base_view("rsa", "MÃ HÓA KHÓA CÔNG KHAI RSA", "Mã hóa bất đối xứng: C = M^e mod n, M = C^d mod n")
        split_box = ctk.CTkFrame(v, fg_color="transparent"); split_box.pack(fill="both", expand=True)

        left = ctk.CTkFrame(split_box, corner_radius=10); left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Tham số p, q, e
        p_row = ctk.CTkFrame(left, fg_color="transparent"); p_row.pack(fill="x", padx=15, pady=5)
        
        f1 = ctk.CTkFrame(p_row, fg_color="transparent"); f1.pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkLabel(f1, text="Số nguyên tố p:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.rsa_p = ctk.CTkEntry(f1, height=34, justify="center"); self.rsa_p.pack(fill="x"); self.rsa_p.insert(0, "61")

        f2 = ctk.CTkFrame(p_row, fg_color="transparent"); f2.pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkLabel(f2, text="Số nguyên tố q:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.rsa_q = ctk.CTkEntry(f2, height=34, justify="center"); self.rsa_q.pack(fill="x"); self.rsa_q.insert(0, "53")

        f3 = ctk.CTkFrame(p_row, fg_color="transparent"); f3.pack(side="left", expand=True, fill="x", padx=2)
        ctk.CTkLabel(f3, text="Khóa e:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.rsa_e = ctk.CTkEntry(f3, height=34, justify="center"); self.rsa_e.pack(fill="x"); self.rsa_e.insert(0, "17")

        ctk.CTkLabel(left, text="Văn bản (Plaintext / Dãy số Cipher cách nhau bằng dấu cách):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.rsa_in = ctk.CTkEntry(left, height=40); self.rsa_in.pack(fill="x", padx=15, pady=5); self.rsa_in.insert(0, "HI")

        btn_bar = ctk.CTkFrame(left, fg_color="transparent"); btn_bar.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(btn_bar, text="🔒 Mã Hóa", fg_color="#10b981", hover_color="#059669", height=38, width=110, command=lambda: self._run_rsa(False)).pack(side="left", padx=4)
        ctk.CTkButton(btn_bar, text="🔓 Giải Mã", fg_color="#3b82f6", hover_color="#2563eb", height=38, width=110, command=lambda: self._run_rsa(True)).pack(side="left", padx=4)

        ctk.CTkLabel(left, text="Kết quả:", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(5, 2))
        self.rsa_out = ctk.CTkTextbox(left, height=100, font=ctk.CTkFont(family="Consolas", size=13))
        self.rsa_out.pack(fill="both", expand=True, padx=15, pady=(2, 15))

        right = ctk.CTkFrame(split_box, corner_radius=10); right.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(right, text="Phân Tích Toán Học Khóa RSA & Lũy Thừa Modulo:", font=ctk.CTkFont(weight="bold"), text_color="#38bdf8").pack(anchor="w", padx=15, pady=(10, 5))
        self.rsa_log = ctk.CTkTextbox(right, font=ctk.CTkFont(family="Consolas", size=12), text_color="#38bdf8")
        self.rsa_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _run_rsa(self, is_dec):
        try:
            p = int(self.rsa_p.get().strip())
            q = int(self.rsa_q.get().strip())
            e = int(self.rsa_e.get().strip())
        except:
            return messagebox.showerror("Lỗi", "p, q, e phải là số nguyên!")
        if not is_prime(p) or not is_prime(q):
            return messagebox.showerror("Lỗi", "p và q bắt buộc phải là số nguyên tố!")
        if p == q:
            return messagebox.showerror("Lỗi", "p và q phải là 2 số nguyên tố phân biệt!")

        msg = self.rsa_in.get().strip()
        if not msg: return messagebox.showwarning("Cảnh báo", "Nhập văn bản!")
        r, log, err = rsa_cipher(msg, p, q, e, is_dec)
        if err: return messagebox.showerror("Lỗi", err)
        self.rsa_out.delete("1.0", "end"); self.rsa_out.insert("1.0", r)
        self.rsa_log.delete("1.0", "end"); self.rsa_log.insert("1.0", log)

    # ═════════════════════════════════════════════════════════
    # 9. VIEW DIFFIE-HELLMAN
    # ═════════════════════════════════════════════════════════
    def _init_dh_view(self):
        v = self._create_base_view("dh", "TRAO ĐỔI KHÓA DIFFIE-HELLMAN", "Thỏa thuận khóa bí mật chung K qua kênh truyền thông khai")
        split_box = ctk.CTkFrame(v, fg_color="transparent"); split_box.pack(fill="both", expand=True)

        left = ctk.CTkFrame(split_box, corner_radius=10); left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Tham số chung q, alpha
        p1 = ctk.CTkFrame(left, fg_color="transparent"); p1.pack(fill="x", padx=15, pady=5)
        f1 = ctk.CTkFrame(p1, fg_color="transparent"); f1.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkLabel(f1, text="Số nguyên tố chung (q):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.dh_q = ctk.CTkEntry(f1, height=34, justify="center"); self.dh_q.pack(fill="x"); self.dh_q.insert(0, "353")

        f2 = ctk.CTkFrame(p1, fg_color="transparent"); f2.pack(side="left", expand=True, fill="x", padx=(5, 0))
        ctk.CTkLabel(f2, text="Nguyên căn chung (α):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.dh_alpha = ctk.CTkEntry(f2, height=34, justify="center"); self.dh_alpha.pack(fill="x"); self.dh_alpha.insert(0, "3")

        # Khóa riêng XA, XB
        p2 = ctk.CTkFrame(left, fg_color="transparent"); p2.pack(fill="x", padx=15, pady=5)
        f3 = ctk.CTkFrame(p2, fg_color="transparent"); f3.pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkLabel(f3, text="Khóa riêng Bên A (XA):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.dh_xa = ctk.CTkEntry(f3, height=34, justify="center"); self.dh_xa.pack(fill="x"); self.dh_xa.insert(0, "97")

        f4 = ctk.CTkFrame(p2, fg_color="transparent"); f4.pack(side="left", expand=True, fill="x", padx=(5, 0))
        ctk.CTkLabel(f4, text="Khóa riêng Bên B (XB):", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.dh_xb = ctk.CTkEntry(f4, height=34, justify="center"); self.dh_xb.pack(fill="x"); self.dh_xb.insert(0, "233")

        btn_bar = ctk.CTkFrame(left, fg_color="transparent"); btn_bar.pack(fill="x", padx=15, pady=12)
        ctk.CTkButton(btn_bar, text="⚡ TÍNH TOÁN & ĐỒNG THUẬN KHÓA", fg_color="#38bdf8", hover_color="#0284c7", text_color="#000000", font=ctk.CTkFont(weight="bold"), height=40, command=self._run_dh).pack(fill="x")

        ctk.CTkLabel(left, text="Khóa Bí Mật Chung (K):", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(anchor="w", padx=15, pady=(5, 2))
        self.dh_out = ctk.CTkTextbox(left, height=110, font=ctk.CTkFont(family="Consolas", size=13))
        self.dh_out.pack(fill="both", expand=True, padx=15, pady=(2, 15))

        right = ctk.CTkFrame(split_box, corner_radius=10); right.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(right, text="Theo Dõi Trao Đổi Khóa Công Khai & Bí Mật:", font=ctk.CTkFont(weight="bold"), text_color="#38bdf8").pack(anchor="w", padx=15, pady=(10, 5))
        self.dh_log = ctk.CTkTextbox(right, font=ctk.CTkFont(family="Consolas", size=12), text_color="#38bdf8")
        self.dh_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _run_dh(self):
        try:
            q = int(self.dh_q.get().strip())
            alpha = int(self.dh_alpha.get().strip())
            xa = int(self.dh_xa.get().strip())
            xb = int(self.dh_xb.get().strip())
        except:
            return messagebox.showerror("Lỗi", "Tất cả các tham số phải là số nguyên!")

        if not is_prime(q):
            return messagebox.showerror("Lỗi Toán Học", f"q={q} không phải là số nguyên tố!")
        if not is_primitive_root(alpha, q):
            return messagebox.showerror("Lỗi Toán Học", f"α={alpha} không phải là nguyên căn của {q}!")
        if xa >= q or xb >= q:
            return messagebox.showerror("Lỗi Toán Học", "Khóa riêng XA và XB phải nhỏ hơn q!")

        ya = pow(alpha, xa, q)
        yb = pow(alpha, xb, q)
        ka = pow(yb, xa, q)
        kb = pow(ya, xb, q)

        out_res = f"• Khóa công khai Bên A (YA) = {ya}\n• Khóa công khai Bên B (YB) = {yb}\n"
        out_res += f"──────────────────────────────────────\n"
        out_res += f"➔ KHÓA BÍ MẬT ĐỒNG THUẬN CHUNG: K = {ka}"
        self.dh_out.delete("1.0", "end"); self.dh_out.insert("1.0", out_res)

        log = "═══ QUÁ TRÌNH TRAO ĐỔI KHÓA DIFFIE-HELLMAN ═══\n\n"
        log += f"[1. BÊN A]\n"
        log += f"• Khóa riêng: XA = {xa}\n"
        log += f"• Tính khóa công khai: YA = α^XA mod q = {alpha}^{xa} mod {q} = {ya}\n"
        log += f"• Gửi công khai YA = {ya} qua mạng cho B\n\n"
        log += f"[2. BÊN B]\n"
        log += f"• Khóa riêng: XB = {xb}\n"
        log += f"• Tính khóa công khai: YB = α^XB mod q = {alpha}^{xb} mod {q} = {yb}\n"
        log += f"• Gửi công khai YB = {yb} qua mạng cho A\n\n"
        log += f"[3. TÍNH KHÓA CHUNG K]\n"
        log += f"• A nhận YB ({yb}) ──> K = YB^XA mod q = {yb}^{xa} mod {q} = {ka}\n"
        log += f"• B nhận YA ({ya}) ──> K = YA^XB mod q = {ya}^{xb} mod {q} = {kb}\n\n"
        if ka == kb:
            log += f"✅ KẾT QUẢ: Đồng thuận thành công! Khóa bí mật chung an toàn K = {ka}"
        else:
            log += f"❌ LỖI: Hai khóa không trùng khớp!"
        self.dh_log.delete("1.0", "end"); self.dh_log.insert("1.0", log)


if __name__ == "__main__":
    app = ModernCryptoApp()
    app.mainloop()
