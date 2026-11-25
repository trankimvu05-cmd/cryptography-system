"""
Vigenère Cipher — Mã hóa đa bảng chữ cái dùng khóa tuần hoàn
Công thức: Cᵢ = (Pᵢ + Kᵢ) mod 26 | Pᵢ = (Cᵢ - Kᵢ) mod 26
"""


def vigenere_cipher(text, key, decrypt=False):
    """
    Mã hóa / Giải mã Vigenère.

    Args:
        text: Văn bản đầu vào
        key: Khóa (chuỗi chữ cái)
        decrypt: True = giải mã, False = mã hóa

    Returns:
        Chuỗi kết quả
    """
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
