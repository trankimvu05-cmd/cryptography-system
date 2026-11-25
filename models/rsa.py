"""
RSA — Mã hóa khóa công khai (Asymmetric Encryption)
Công thức: C = M^e mod n | M = C^d mod n
"""

import math


def is_prime(n):
    """Kiểm tra số nguyên tố."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def rsa_cipher(msg, p, q, e, decrypt=False):
    """
    Mã hóa / Giải mã RSA.

    Args:
        msg: Văn bản (plaintext) hoặc dãy số cipher cách nhau bằng dấu cách
        p: Số nguyên tố p
        q: Số nguyên tố q
        e: Khóa công khai e
        decrypt: True = giải mã, False = mã hóa

    Returns:
        (result, log, error):
        - result: Kết quả (None nếu lỗi)
        - log: Bảng phân tích chi tiết
        - error: Thông báo lỗi (None nếu thành công)
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        return None, None, (
            f"e={e} và phi={phi} không nguyên tố cùng nhau (ƯCLN != 1)!"
        )

    d = pow(e, -1, phi)
    log = "═══ THÔNG SỐ KHÓA RSA ═══\n"
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
            log += (
                f"  '{c}' (ASCII {m_val:3d}) ──> "
                f"C = {m_val}^{e} mod {n} = {c_val}\n"
            )
        return " ".join(map(str, ciphers)), log, None
