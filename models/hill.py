"""
Hill Cipher — Mã hóa ma trận đa bảng chữ cái
Công thức: C = P × K mod 26 | P = C × K⁻¹ mod 26
"""

import math


def hill_minor(m, i, j):
    """Tính minor của ma trận m tại vị trí (i, j)."""
    return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]


def hill_det(m):
    """Tính định thức ma trận m (đệ quy)."""
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = 0
    for c in range(len(m)):
        det += ((-1) ** c) * m[0][c] * hill_det(hill_minor(m, 0, c))
    return det


def hill_adjugate(m):
    """Tính ma trận phụ hợp (adjugate) của m."""
    if len(m) == 1:
        return [[1]]
    adj = []
    for i in range(len(m)):
        row = []
        for j in range(len(m)):
            sign = (-1) ** (i + j)
            row.append(sign * hill_det(hill_minor(m, j, i)))
        adj.append(row)
    return adj


def hill_cipher(text, K, decrypt=False):
    """
    Mã hóa / Giải mã Hill.

    Args:
        text: Văn bản đầu vào (chỉ lấy chữ cái)
        K: Ma trận khóa NxN (danh sách 2D)
        decrypt: True = giải mã, False = mã hóa

    Returns:
        (result, log, error):
        - result: Chuỗi kết quả (None nếu lỗi)
        - log: Bảng phân tích chi tiết (None nếu lỗi)
        - error: Thông báo lỗi (None nếu thành công)
    """
    t = "".join([c.upper() for c in text if c.isalpha()])
    m = len(K)
    det_K = hill_det(K) % 26
    if math.gcd(det_K, 26) != 1:
        return None, None, (
            f"Định thức Det(K) = {det_K} không nguyên tố "
            f"cùng nhau với 26 (ƯCLN != 1)!"
        )

    log = f"═══ BẢNG PHÂN TÍCH MA TRẬN HILL "
    log += f"({'GIẢI MÃ' if decrypt else 'MÃ HÓA'}) ═══\n"
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
        block = [ord(c) - 65 for c in t[i:i + m]]
        res_block = []
        for col in range(m):
            val = sum(block[row] * K_work[row][col] for row in range(m)) % 26
            res_block.append(val)
            res += chr(val + 65)
        log += (
            f"  [{', '.join(t[i:i + m])}] ──> "
            f"[{', '.join([chr(v + 65) for v in res_block])}]\n"
        )

    if decrypt:
        res = res.rstrip('X')
    return res, log, None
