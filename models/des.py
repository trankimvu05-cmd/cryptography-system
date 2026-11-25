"""
DES (Data Encryption Standard) — Mã hóa khối 64-bit
Cấu trúc Feistel 16 vòng lặp với S-Box, P-Box
"""

# ═══════════════════════════════════════════════
# CÁC BẢNG HẰNG SỐ TIÊU CHUẨN DES
# ═══════════════════════════════════════════════

PC1 = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

DES_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

IP_T = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]

FP_T = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
]

E_BOX = [
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]

P_BOX = [
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26,
    5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

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


# ═══════════════════════════════════════════════
# HÀM XỬ LÝ NHỊ PHÂN
# ═══════════════════════════════════════════════

def des_p(b, tbl):
    """Hoán vị bit theo bảng."""
    return "".join(b[i - 1] for i in tbl)


def des_sh(b, n):
    """Dịch vòng trái n bit."""
    return b[n:] + b[:n]


def des_x(b1, b2):
    """XOR hai chuỗi bit."""
    return "".join("1" if b1[i] != b2[i] else "0" for i in range(len(b1)))


def des_to_hex(b):
    """Chuyển chuỗi bit sang hex."""
    return hex(int(b, 2))[2:].upper().zfill(len(b) // 4)


# ═══════════════════════════════════════════════
# THUẬT TOÁN DES CHÍNH
# ═══════════════════════════════════════════════

def des_cipher(msg, key_hex, decrypt=False):
    """
    Mã hóa / Giải mã DES.

    Args:
        msg: Văn bản (plaintext) hoặc chuỗi Hex (ciphertext)
        key_hex: Khóa 16 ký tự Hex (64-bit)
        decrypt: True = giải mã, False = mã hóa

    Returns:
        (result, log, error):
        - result: Kết quả (None nếu lỗi)
        - log: Bảng phân tích chi tiết
        - error: Thông báo lỗi (None nếu thành công)
    """
    try:
        key_bin = bin(int(key_hex, 16))[2:].zfill(64)
    except Exception:
        return None, None, "Khóa K chỉ gồm ký tự Hex (0-9, A-F)!"

    # Sinh 16 khóa con
    pc1_res = des_p(key_bin, PC1)
    C, D = pc1_res[:28], pc1_res[28:]
    subkeys = []
    log_key = "═══ BƯỚC 1: SINH 16 KHÓA CON (SUBKEYS) ═══\n"
    for i in range(16):
        C, D = des_sh(C, DES_SHIFTS[i]), des_sh(D, DES_SHIFTS[i])
        sk = des_p(C + D, PC2)
        subkeys.append(sk)
        log_key += f"  K{i + 1:02d}: {des_to_hex(sk)}\n"

    if decrypt:
        try:
            msg_bin = bin(int(msg, 16))[2:].zfill(len(msg) * 4)
        except Exception:
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
        blk = msg_bin[block_idx:block_idx + 64]
        ip_r = des_p(blk, IP_T)
        L, R = ip_r[:32], ip_r[32:]
        for i in range(16):
            L_prev, R_prev = L, R
            e_r = des_p(R_prev, E_BOX)
            xor_r = des_x(e_r, work_keys[i])
            s_r = ""
            for j in range(8):
                chunk = xor_r[j * 6:(j + 1) * 6]
                row = int(chunk[0] + chunk[5], 2)
                col = int(chunk[1:5], 2)
                s_r += bin(S_BOX[j][row][col])[2:].zfill(4)
            f_r = des_p(s_r, P_BOX)
            L = R_prev
            R = des_x(L_prev, f_r)
            if block_idx == 0:
                log_detail += (
                    f"  [Vòng {i + 1:2d}] "
                    f"L = {des_to_hex(L)} │ R = {des_to_hex(R)}\n"
                )
        out_bin += des_p(R + L, FP_T)

    if decrypt:
        try:
            out_bytes = int(out_bin, 2).to_bytes(
                len(out_bin) // 8, byteorder='big'
            )
            pad = out_bytes[-1]
            return (
                out_bytes[:-pad].decode('utf-8', errors='ignore'),
                log_detail,
                None
            )
        except Exception as e:
            return None, None, f"Lỗi giải mã DES: {e}"
    else:
        return des_to_hex(out_bin), log_detail, None
