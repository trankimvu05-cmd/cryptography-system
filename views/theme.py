"""
═══════════════════════════════════════════════════════
CYBER SECURITY DASHBOARD — Theme Configuration
Bảng màu, font, kích thước, thông tin 9 hệ mật mã
═══════════════════════════════════════════════════════
"""

# ─── BẢNG MÀU NỀN ───
BG_DARKEST   = "#080b1e"   # Nền chính cửa sổ
BG_DARK      = "#0d1137"   # Sidebar
BG_CARD      = "#111638"   # Card / Panel
BG_CARD_HOVER = "#181f52"  # Card khi hover
BG_INPUT     = "#0f1435"   # Nền ô nhập liệu
BG_INPUT_FOCUS = "#151b45" # Ô nhập khi focus
BG_HEADER    = "#0e1340"   # Header bar

# ─── MÀU NEON ACCENT ───
NEON_CYAN    = "#00d4ff"   # Accent chính (nổi bật nhất)
NEON_PURPLE  = "#7c3aed"   # Accent phụ
NEON_GREEN   = "#00ff88"   # Thành công / Encrypt
NEON_BLUE    = "#3b82f6"   # Decrypt
NEON_PINK    = "#ff006e"   # Lỗi / Cảnh báo
NEON_ORANGE  = "#ff8c00"   # Warning nhẹ
NEON_GOLD    = "#ffd700"   # Điểm nhấn đặc biệt

# ─── MÀU HOVER (sáng hơn accent) ───
HOVER_CYAN   = "#33dfff"
HOVER_PURPLE = "#9b59ff"
HOVER_GREEN  = "#33ff99"
HOVER_BLUE   = "#5b9bff"
HOVER_PINK   = "#ff3388"

# ─── MÀU TEXT ───
TEXT_PRIMARY   = "#e2e8f0"  # Chữ chính (trắng xám sáng)
TEXT_SECONDARY = "#94a3b8"  # Chữ phụ
TEXT_DIM       = "#475569"  # Chữ mờ nhạt
TEXT_TITLE     = "#f1f5f9"  # Tiêu đề lớn
TEXT_CODE      = "#67e8f9"  # Chữ code / kết quả

# ─── VIỀN ───
BORDER_DEFAULT = "#1e293b"  # Viền mặc định
BORDER_ACTIVE  = "#00d4ff"  # Viền khi active / focus
BORDER_SUBTLE  = "#162040"  # Viền rất nhẹ
BORDER_CARD    = "#1a2555"  # Viền card

# ─── GRADIENT TƯƠNG TỰ (dùng cho các lớp chồng) ───
GRADIENT_START = "#0d1137"
GRADIENT_END   = "#1a1f5e"

# ─── SIDEBAR ───
SIDEBAR_BG        = "#0a0f2e"
SIDEBAR_ACTIVE    = "#0c1a4a"
SIDEBAR_HOVER     = "#111b45"
SIDEBAR_ACCENT    = NEON_CYAN
SIDEBAR_TEXT       = "#94a3b8"
SIDEBAR_TEXT_ACTIVE = "#ffffff"

# ═══════════════════════════════════════════════════════
# FONTS
# ═══════════════════════════════════════════════════════
FONT_FAMILY     = "Segoe UI"
FONT_MONO       = "Consolas"
FONT_TITLE_SIZE = 22
FONT_SUBTITLE   = 14
FONT_BODY       = 13
FONT_SMALL      = 11
FONT_CODE       = 12
FONT_NAV        = 13
FONT_BUTTON     = 13

# ═══════════════════════════════════════════════════════
# KÍCH THƯỚC
# ═══════════════════════════════════════════════════════
WINDOW_WIDTH     = 1280
WINDOW_HEIGHT    = 800
WINDOW_MIN_W     = 1100
WINDOW_MIN_H     = 700
SIDEBAR_WIDTH    = 260
CARD_RADIUS      = 14
BUTTON_RADIUS    = 10
INPUT_HEIGHT     = 42
BUTTON_HEIGHT    = 42
NAV_BUTTON_H     = 44

# ═══════════════════════════════════════════════════════
# THÔNG TIN 9 HỆ MẬT MÃ + ĐIỀU HƯỚNG
# ═══════════════════════════════════════════════════════
CIPHER_INFO = {
    "dashboard": {
        "name": "Trang Chủ",
        "icon": "🏠",
        "desc": "Dashboard tổng quan hệ thống",
        "color": NEON_CYAN,
    },
    "caesar": {
        "name": "Caesar Cipher",
        "icon": "🅰",
        "desc": "Mã hóa dịch chuyển vòng tròn",
        "formula": "C = (P + K) mod 26",
        "color": "#06b6d4",
        "category": "Cổ điển",
    },
    "affine": {
        "name": "Affine Cipher",
        "icon": "🔣",
        "desc": "Kết hợp phép nhân và dịch chuyển",
        "formula": "C = (aP + b) mod 26",
        "color": "#8b5cf6",
        "category": "Cổ điển",
    },
    "hill": {
        "name": "Hill Cipher",
        "icon": "📊",
        "desc": "Mã hóa ma trận đa bảng chữ cái",
        "formula": "C = P × K mod 26",
        "color": "#f59e0b",
        "category": "Cổ điển",
    },
    "vigenere": {
        "name": "Vigenère Cipher",
        "icon": "🔤",
        "desc": "Khóa tuần hoàn đa bảng chữ cái",
        "formula": "Cᵢ = (Pᵢ + Kᵢ) mod 26",
        "color": "#10b981",
        "category": "Cổ điển",
    },
    "playfair": {
        "name": "Playfair Cipher",
        "icon": "🔲",
        "desc": "Ma trận khóa 5×5 mã hóa theo cặp",
        "formula": "Mã hóa cặp 2 chữ cái",
        "color": "#ec4899",
        "category": "Cổ điển",
    },
    "hang": {
        "name": "Hoán Vị Hàng",
        "icon": "📋",
        "desc": "Hoán vị cột theo khóa dãy số",
        "formula": "Ghi hàng — đọc cột hoán vị",
        "color": "#14b8a6",
        "category": "Hoán vị",
    },
    "des": {
        "name": "DES",
        "icon": "🔒",
        "desc": "Mã khối Feistel 64-bit tiêu chuẩn",
        "formula": "16 vòng Feistel + S-Box",
        "color": "#ef4444",
        "category": "Hiện đại",
    },
    "rsa": {
        "name": "RSA",
        "icon": "🔑",
        "desc": "Mã hóa khóa công khai bất đối xứng",
        "formula": "C = Mᵉ mod n",
        "color": "#3b82f6",
        "category": "Hiện đại",
    },
    "dh": {
        "name": "Diffie-Hellman",
        "icon": "🤝",
        "desc": "Trao đổi khóa bí mật qua kênh công khai",
        "formula": "K = Yˣ mod q",
        "color": "#22c55e",
        "category": "Hiện đại",
    },
    "about": {
        "name": "Giới Thiệu",
        "icon": "ℹ️",
        "desc": "Thông tin phần mềm",
        "color": NEON_PURPLE,
    },
}

# Thứ tự hiển thị trên sidebar
NAV_ORDER = [
    "dashboard",
    "caesar", "affine", "hill", "vigenere", "playfair",
    "hang", "des", "rsa", "dh",
    "about",
]
