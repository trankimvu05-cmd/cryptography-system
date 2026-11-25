"""
═══════════════════════════════════════════════════════
CYBER SECURITY DASHBOARD — Controllers
Bộ điều khiển trung gian: Validate dữ liệu và gọi Model
═══════════════════════════════════════════════════════
"""

from models.caesar import caesar_cipher
from models.affine import affine_cipher
from models.hill import hill_cipher
from models.vigenere import vigenere_cipher
from models.playfair import playfair_cipher, playfair_matrix
from models.hang import hang_cipher
from models.des import des_cipher
from models.rsa import rsa_cipher, is_prime
from models.diffie_hellman import dh_compute, is_primitive_root


class CipherController:
    """Controller tập trung xử lý validate và gọi các hàm nghiệp vụ mật mã."""

    @staticmethod
    def run_caesar(text, key_str, decrypt=False):
        if not text:
            raise ValueError("Vui lòng nhập văn bản!")
        try:
            k = int(key_str.strip())
        except ValueError:
            raise ValueError("Khóa K phải là số nguyên!")
        return caesar_cipher(text, k, decrypt)

    @staticmethod
    def run_affine(text, a_str, b_str, decrypt=False):
        if not text:
            raise ValueError("Vui lòng nhập văn bản!")
        try:
            a = int(a_str.strip())
            b = int(b_str.strip())
        except ValueError:
            raise ValueError("Khóa a và b phải là số nguyên!")
        res, err = affine_cipher(text, a, b, decrypt)
        if err:
            raise ValueError(err)
        return res

    @staticmethod
    def run_hill(text, matrix_entries, decrypt=False):
        if not text:
            raise ValueError("Vui lòng nhập văn bản!")
        K = []
        for r in matrix_entries:
            row_vals = []
            for e in r:
                val = e.get().strip() if hasattr(e, 'get') else str(e).strip()
                if not val:
                    raise ValueError("Vui lòng nhập đầy đủ số nguyên vào tất cả các ô ma trận!")
                row_vals.append(int(val))
            K.append(row_vals)
        res, log, err = hill_cipher(text, K, decrypt)
        if err:
            raise ValueError(err)
        return res, log

    @staticmethod
    def run_vigenere(text, key_str, decrypt=False):
        if not text or not key_str:
            raise ValueError("Vui lòng nhập đủ văn bản và khóa K!")
        k = key_str.strip()
        if not k.isalpha():
            raise ValueError("Khóa Vigenère phải là các ký tự chữ cái (A-Z)!")
        return vigenere_cipher(text, k, decrypt)

    @staticmethod
    def run_playfair(text, kw_str, decrypt=False):
        if not text or not kw_str:
            raise ValueError("Vui lòng nhập đủ văn bản và từ khóa!")
        kw = kw_str.strip()
        if not kw.isalpha():
            raise ValueError("Từ khóa chỉ gồm các ký tự chữ cái!")
        return playfair_cipher(text, kw, decrypt)

    @staticmethod
    def run_hang(text, key_str, decrypt=False):
        if not text:
            raise ValueError("Vui lòng nhập văn bản!")
        try:
            k = [int(x) for x in key_str.replace(',', ' ').split()]
            if not k:
                raise ValueError
        except Exception:
            raise ValueError("Khóa K phải là dãy số phân tách bởi dấu phẩy hoặc khoảng trắng!")
        return hang_cipher(text, k, decrypt)

    @staticmethod
    def run_des(msg, key_hex, decrypt=False):
        if not msg:
            raise ValueError("Vui lòng nhập văn bản đầu vào!")
        k = key_hex.strip().upper()
        if len(k) != 16:
            raise ValueError("Khóa K phải đúng 16 ký tự Hex (64-bit)!")
        res, log, err = des_cipher(msg, k, decrypt)
        if err:
            raise ValueError(err)
        return res, log

    @staticmethod
    def run_rsa(msg, p_str, q_str, e_str, decrypt=False):
        try:
            p = int(p_str.strip())
            q = int(q_str.strip())
            e = int(e_str.strip())
        except ValueError:
            raise ValueError("Các tham số p, q, e phải là số nguyên!")
        if not is_prime(p) or not is_prime(q):
            raise ValueError("p và q bắt buộc phải là các số nguyên tố!")
        if p == q:
            raise ValueError("p và q phải là 2 số nguyên tố phân biệt!")
        if not msg:
            raise ValueError("Vui lòng nhập văn bản đầu vào!")
        res, log, err = rsa_cipher(msg, p, q, e, decrypt)
        if err:
            raise ValueError(err)
        return res, log

    @staticmethod
    def run_dh(q_str, alpha_str, xa_str, xb_str):
        try:
            q = int(q_str.strip())
            alpha = int(alpha_str.strip())
            xa = int(xa_str.strip())
            xb = int(xb_str.strip())
        except ValueError:
            raise ValueError("Tất cả tham số q, alpha, XA, XB phải là số nguyên!")
        if not is_prime(q):
            raise ValueError(f"q={q} không phải là số nguyên tố!")
        if not is_primitive_root(alpha, q):
            raise ValueError(f"alpha={alpha} không phải là nguyên căn của {q}!")
        if xa >= q or xb >= q:
            raise ValueError("Khóa riêng XA và XB bắt buộc phải nhỏ hơn q!")
        return dh_compute(q, alpha, xa, xb)
