"""
Diffie-Hellman Key Exchange — Trao đổi khóa bí mật chung
Thỏa thuận khóa K qua kênh truyền thông công khai
"""


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


def is_primitive_root(alpha, q):
    """
    Kiểm tra alpha có phải nguyên căn (primitive root) của q hay không.

    Args:
        alpha: Giá trị cần kiểm tra
        q: Số nguyên tố

    Returns:
        True nếu alpha là nguyên căn của q
    """
    if alpha <= 1 or alpha >= q:
        return False
    phi = q - 1
    factors = set()
    n = phi
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 2
    if n > 2:
        factors.add(n)
    for p in factors:
        if pow(alpha, phi // p, q) == 1:
            return False
    return True


def dh_compute(q, alpha, xa, xb):
    """
    Tính toán trao đổi khóa Diffie-Hellman.

    Args:
        q: Số nguyên tố chung
        alpha: Nguyên căn chung
        xa: Khóa riêng bên A
        xb: Khóa riêng bên B

    Returns:
        (ya, yb, ka, kb, log):
        - ya: Khóa công khai bên A
        - yb: Khóa công khai bên B
        - ka: Khóa bí mật tính bởi A
        - kb: Khóa bí mật tính bởi B
        - log: Bảng phân tích chi tiết
    """
    # Bên A: Tính YA = alpha^XA mod q
    ya = pow(alpha, xa, q)
    # Bên B: Tính YB = alpha^XB mod q
    yb = pow(alpha, xb, q)
    # Bên A: Tính K = YB^XA mod q
    ka = pow(yb, xa, q)
    # Bên B: Tính K = YA^XB mod q
    kb = pow(ya, xb, q)

    # Tạo bảng phân tích
    log = "═══ QUÁ TRÌNH TRAO ĐỔI KHÓA DIFFIE-HELLMAN ═══\n\n"
    log += "[1. BÊN A]\n"
    log += f"• Khóa riêng: XA = {xa}\n"
    log += (
        f"• Tính khóa công khai: YA = α^XA mod q "
        f"= {alpha}^{xa} mod {q} = {ya}\n"
    )
    log += f"• Gửi công khai YA = {ya} qua mạng cho B\n\n"
    log += "[2. BÊN B]\n"
    log += f"• Khóa riêng: XB = {xb}\n"
    log += (
        f"• Tính khóa công khai: YB = α^XB mod q "
        f"= {alpha}^{xb} mod {q} = {yb}\n"
    )
    log += f"• Gửi công khai YB = {yb} qua mạng cho A\n\n"
    log += "[3. TÍNH KHÓA CHUNG K]\n"
    log += (
        f"• A nhận YB ({yb}) ──> K = YB^XA mod q "
        f"= {yb}^{xa} mod {q} = {ka}\n"
    )
    log += (
        f"• B nhận YA ({ya}) ──> K = YA^XB mod q "
        f"= {ya}^{xb} mod {q} = {kb}\n\n"
    )
    if ka == kb:
        log += (
            f"✅ KẾT QUẢ: Đồng thuận thành công! "
            f"Khóa bí mật chung an toàn K = {ka}"
        )
    else:
        log += "❌ LỖI: Hai khóa không trùng khớp!"

    return ya, yb, ka, kb, log
