"""
Affine Cipher — Mã hóa kết hợp phép nhân và dịch chuyển
Công thức: C = (a*P + b) mod 26 | P = a⁻¹*(C - b) mod 26
"""

import math


def affine_mod_inv(a, m=26):
    """Tìm nghịch đảo modular của a trong Zm."""
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None


def affine_cipher(text, a, b, decrypt=False):
    """
    Mã hóa / Giải mã Affine.

    Args:
        text: Văn bản đầu vào
        a: Khóa nhân (ƯCLN(a, 26) = 1)
        b: Khóa dịch chuyển
        decrypt: True = giải mã, False = mã hóa

    Returns:
        (result, error): Kết quả và thông báo lỗi (None nếu thành công)
    """
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
