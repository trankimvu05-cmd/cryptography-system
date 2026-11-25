"""
Flask Web Application — CRYPTOGRAPHY SYSTEM
Chuyển đổi từ CustomTkinter desktop sang Web App
"""

from flask import Flask, render_template, request, jsonify
import sys, os

# Thêm thư mục gốc vào path để import models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from models.caesar import caesar_cipher
from models.affine import affine_cipher
from models.hill import hill_cipher
from models.vigenere import vigenere_cipher
from models.playfair import playfair_cipher, playfair_matrix
from models.hang import hang_cipher
from models.des import des_cipher
from models.rsa import rsa_cipher, is_prime
from models.diffie_hellman import dh_compute, is_prime as dh_is_prime, is_primitive_root

app = Flask(__name__)


# ═══════════════════════════════
# ROUTES — PAGES
# ═══════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


# ═══════════════════════════════
# API ROUTES — CIPHERS
# ═══════════════════════════════

@app.route("/api/caesar", methods=["POST"])
def api_caesar():
    data = request.get_json()
    text = data.get("text", "")
    decrypt = data.get("decrypt", False)
    try:
        k = int(data.get("key", 3))
    except (ValueError, TypeError):
        return jsonify({"error": "Khóa K phải là số nguyên!"}), 400
    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản!"}), 400
    result = caesar_cipher(text, k, decrypt)
    return jsonify({"result": result})


@app.route("/api/affine", methods=["POST"])
def api_affine():
    data = request.get_json()
    text = data.get("text", "")
    decrypt = data.get("decrypt", False)
    try:
        a = int(data.get("a", 5))
        b = int(data.get("b", 8))
    except (ValueError, TypeError):
        return jsonify({"error": "a và b phải là số nguyên!"}), 400
    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản!"}), 400
    result, err = affine_cipher(text, a, b, decrypt)
    if err:
        return jsonify({"error": err}), 400
    return jsonify({"result": result})


@app.route("/api/hill", methods=["POST"])
def api_hill():
    data = request.get_json()
    text = data.get("text", "")
    decrypt = data.get("decrypt", False)
    matrix_raw = data.get("matrix", [[3, 3], [2, 5]])
    try:
        K = [[int(v) for v in row] for row in matrix_raw]
    except (ValueError, TypeError):
        return jsonify({"error": "Ma trận khóa phải gồm các số nguyên!"}), 400
    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản!"}), 400
    result, log, err = hill_cipher(text, K, decrypt)
    if err:
        return jsonify({"error": err}), 400
    return jsonify({"result": result, "log": log})


@app.route("/api/vigenere", methods=["POST"])
def api_vigenere():
    data = request.get_json()
    text = data.get("text", "")
    key = data.get("key", "KEY")
    decrypt = data.get("decrypt", False)
    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản!"}), 400
    if not key or not key.isalpha():
        return jsonify({"error": "Khóa chỉ được chứa chữ cái!"}), 400
    result = vigenere_cipher(text, key, decrypt)
    return jsonify({"result": result})


@app.route("/api/playfair", methods=["POST"])
def api_playfair():
    data = request.get_json()
    text = data.get("text", "")
    key = data.get("key", "KEYWORD")
    decrypt = data.get("decrypt", False)
    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản!"}), 400
    if not key:
        return jsonify({"error": "Vui lòng nhập từ khóa!"}), 400
    result, matrix = playfair_cipher(text, key, decrypt)
    # Format matrix 5x5
    matrix_grid = [matrix[i*5:(i+1)*5] for i in range(5)]
    return jsonify({"result": result, "matrix": matrix_grid})


@app.route("/api/hang", methods=["POST"])
def api_hang():
    data = request.get_json()
    text = data.get("text", "")
    decrypt = data.get("decrypt", False)
    key_raw = data.get("key", [3, 1, 4, 2])
    try:
        key = [int(x) for x in key_raw]
    except (ValueError, TypeError):
        return jsonify({"error": "Khóa phải là dãy số nguyên!"}), 400
    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản!"}), 400
    if len(key) < 2:
        return jsonify({"error": "Khóa cần ít nhất 2 cột!"}), 400
    result, log = hang_cipher(text, key, decrypt)
    return jsonify({"result": result, "log": log})


@app.route("/api/des", methods=["POST"])
def api_des():
    data = request.get_json()
    text = data.get("text", "")
    key_hex = data.get("key", "133457799BBCDFF1")
    decrypt = data.get("decrypt", False)
    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản!"}), 400
    if len(key_hex) != 16:
        return jsonify({"error": "Khóa DES phải là 16 ký tự Hex (64-bit)!"}), 400
    result, log, err = des_cipher(text, key_hex.upper(), decrypt)
    if err:
        return jsonify({"error": err}), 400
    return jsonify({"result": result, "log": log})


@app.route("/api/rsa", methods=["POST"])
def api_rsa():
    data = request.get_json()
    text = data.get("text", "")
    decrypt = data.get("decrypt", False)
    try:
        p = int(data.get("p", 61))
        q = int(data.get("q", 53))
        e = int(data.get("e", 17))
    except (ValueError, TypeError):
        return jsonify({"error": "p, q, e phải là số nguyên!"}), 400
    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản!"}), 400
    if not is_prime(p) or not is_prime(q):
        return jsonify({"error": "p và q bắt buộc phải là số nguyên tố!"}), 400
    if p == q:
        return jsonify({"error": "p và q phải là 2 số nguyên tố phân biệt!"}), 400
    result, log, err = rsa_cipher(text, p, q, e, decrypt)
    if err:
        return jsonify({"error": err}), 400
    return jsonify({"result": result, "log": log})


@app.route("/api/dh", methods=["POST"])
def api_dh():
    data = request.get_json()
    try:
        q = int(data.get("q", 353))
        alpha = int(data.get("alpha", 3))
        xa = int(data.get("xa", 97))
        xb = int(data.get("xb", 233))
    except (ValueError, TypeError):
        return jsonify({"error": "Tất cả tham số phải là số nguyên!"}), 400
    if not dh_is_prime(q):
        return jsonify({"error": f"q={q} không phải số nguyên tố!"}), 400
    if not is_primitive_root(alpha, q):
        return jsonify({"error": f"α={alpha} không phải nguyên căn của {q}!"}), 400
    if xa >= q or xb >= q:
        return jsonify({"error": "Khóa riêng XA và XB phải nhỏ hơn q!"}), 400
    ya, yb, ka, kb, log = dh_compute(q, alpha, xa, xb)
    return jsonify({
        "ya": ya, "yb": yb, "k": ka, "log": log
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
