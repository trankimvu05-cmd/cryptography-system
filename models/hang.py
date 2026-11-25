"""
Hoán Vị Hàng (Columnar Transposition)
Ghi văn bản theo hàng, đọc theo thứ tự cột hoán vị
"""

import math


def hang_cipher(text, key, decrypt=False):
    """
    Mã hóa / Giải mã Hoán vị hàng.

    Args:
        text: Văn bản đầu vào
        key: Dãy số thứ tự cột (list[int])
        decrypt: True = giải mã, False = mã hóa

    Returns:
        (result, log): Kết quả và bảng phân tích
    """
    m = len(key)
    rows = math.ceil(len(text) / m)
    log = f"═══ BẢNG PHÂN TÍCH HOÁN VỊ CỘT "
    log += f"({'GIẢI MÃ' if decrypt else 'MÃ HÓA'}) ═══\n"
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
            cols[idx] = text[pos: pos + lengths[idx]]
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
            log += "  Hàng " + f"{row + 1:2d}:  " + "   ".join(row_chars) + "\n"
        return r, log
    else:
        for row in range(rows):
            row_chars = []
            for col in range(m):
                idx = row * m + col
                row_chars.append(text[idx] if idx < len(text) else "*")
            log += "  Hàng " + f"{row + 1:2d}:  " + "   ".join(row_chars) + "\n"

        cols_str = [text[i::m] for i in range(m)]
        sorted_cols = [col for _, col in sorted(zip(key, cols_str))]
        return "".join(sorted_cols), log
