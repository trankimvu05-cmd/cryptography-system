"""
Caesar Cipher — Mã hóa thay thế vòng tròn
Công thức: C = (P + K) mod 26 | P = (C - K) mod 26
"""


def caesar_cipher(text, k, decrypt=False):
    """
    Mã hóa / Giải mã Caesar.

    Args:
        text: Văn bản đầu vào
        k: Khóa dịch chuyển (số nguyên)
        decrypt: True = giải mã, False = mã hóa

    Returns:
        Chuỗi kết quả
    """
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
