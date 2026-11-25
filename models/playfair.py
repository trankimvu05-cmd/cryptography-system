"""
Playfair Cipher — Mã hóa cặp 2 chữ cái với ma trận khóa 5×5
Kết hợp I/J, chèn X giữa cặp trùng
"""


def playfair_matrix(kw):
    """
    Tạo ma trận khóa 5×5 Playfair từ từ khóa.

    Args:
        kw: Từ khóa (keyword)

    Returns:
        Chuỗi 25 ký tự đại diện ma trận 5×5
    """
    kw = kw.upper().replace('J', 'I')
    m = ""
    for c in kw + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c.isalpha() and c not in m:
            m += c
    return m


def playfair_cipher(text, kw, decrypt=False):
    """
    Mã hóa / Giải mã Playfair.

    Args:
        text: Văn bản đầu vào
        kw: Từ khóa (keyword)
        decrypt: True = giải mã, False = mã hóa

    Returns:
        (result, matrix): Kết quả và ma trận khóa 5×5
    """
    m = playfair_matrix(kw)
    t = "".join([c.upper() for c in text if c.isalpha()]).replace('J', 'I')

    if not decrypt:
        res, i = "", 0
        while i < len(t):
            a = t[i]
            if i + 1 < len(t):
                b = t[i + 1]
                if a == b:
                    res += a + 'X'
                    i += 1
                else:
                    res += a + b
                    i += 2
            else:
                res += a + 'X'
                i += 1
        t = res
    else:
        if len(t) % 2 != 0:
            t += 'X'

    out = ""
    d = -1 if decrypt else 1
    for i in range(0, len(t), 2):
        r1, c1 = m.index(t[i]) // 5, m.index(t[i]) % 5
        r2, c2 = m.index(t[i + 1]) // 5, m.index(t[i + 1]) % 5

        if r1 == r2:
            out += m[r1 * 5 + (c1 + d) % 5] + m[r2 * 5 + (c2 + d) % 5]
        elif c1 == c2:
            out += m[((r1 + d) % 5) * 5 + c1] + m[((r2 + d) % 5) * 5 + c2]
        else:
            out += m[r1 * 5 + c2] + m[r2 * 5 + c1]
    return out, m
