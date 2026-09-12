# -*- coding: utf-8 -*-
"""
=======================================================================
  ỨNG DỤNG THI THỬ ĐÁNH GIÁ NĂNG LỰC (HSA) - PHẦN TƯ DUY ĐỊNH LƯỢNG
  (1 FILE PYTHON DUY NHẤT - GIAO DIỆN TÔNG MÀU XANH LÁ THEO MẪU)
=======================================================================
Luồng sử dụng:
  1) Học sinh nhập họ tên, số báo danh.
  2) Chọn 1 trong các đề thi tham khảo.
  3) Vào "Màn hình chờ" (giống ảnh mẫu Map Study) - có 120 giây đếm
     ngược trước khi tự động bắt đầu, hoặc bấm <BẮT ĐẦU> để vào ngay.
  4) Làm bài: đề có đúng 50 câu:
       - 35 câu trắc nghiệm 4 lựa chọn (A/B/C/D)
       - 15 câu điền đáp án (trả lời ngắn)
     Đồng hồ đếm ngược 75 phút, có thanh câu hỏi 1..50 để chuyển câu.
  5) Khi bấm "NỘP BÀI" sẽ hiện màn hình nhắc nhở (giống ảnh mẫu) liệt kê
     các câu chưa làm và hỏi xác nhận "Có / Không" trước khi nộp thật.
  6) Nộp bài -> hiển thị điểm số (thang điểm 50) -> xem đáp án & lời
     giải chi tiết từng câu.

Chạy thử:
    pip install Flask
    python app_thi_hsa.py
    -> mở http://127.0.0.1:5000
=======================================================================
"""
import math
import os
import random
import time
import uuid
from fractions import Fraction

from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "doi-key-nay-khi-deploy-that")

EXAM_DURATION_MINUTES = 75   # thời gian làm bài (giống đề tham khảo HSA thật)
WAIT_SECONDS = 120           # thời gian màn hình chờ trước khi vào thi
MC4_COUNT_TARGET = 35         # số câu trắc nghiệm 4 lựa chọn MONG MUỐN cho 1 đề đầy đủ
SHORT_COUNT_TARGET = 15       # số câu điền đáp án MONG MUỐN cho 1 đề đầy đủ
TOTAL_POINTS = 50             # tổng điểm phần thi (giống ảnh mẫu)


# =======================================================================
# 1) NGÂN HÀNG CÂU HỎI "TOÁN HỌC VÀ XỬ LÝ SỐ LIỆU" - VIẾT TAY TỪNG CÂU
#    (theo đúng cách viết của app thi thử tốt nghiệp: mỗi câu là 1 dict
#    khai báo sẵn nội dung/đáp án/lời giải, KHÔNG sinh tự động bằng code)
#
#    -> MUỐN THÊM CÂU HỎI: chỉ cần copy 1 dict mẫu bên dưới, dán vào đúng
#       danh sách "mc4" (trắc nghiệm 4 lựa chọn) hoặc "short" (điền đáp án)
#       của đề tương ứng trong EXAM_DEFS, rồi sửa lại nội dung/đáp án.
#       KHÔNG cần sửa bất kỳ chỗ nào khác trong code.
#
#    Cấu trúc 1 câu TRẮC NGHIỆM (type sẽ tự được gán = "mc4"):
#        {
#            "content": "Nội dung câu hỏi (có thể dùng LaTeX \\( ... \\))",
#            "image": "https://.../hinh-ve.png",       # KHÔNG BẮT BUỘC
#            "content_after_image": "Câu hỏi sau ảnh",  # KHÔNG BẮT BUỘC
#            "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
#            "correct": "A",   # chữ cái đáp án đúng
#            "explanation": "Lời giải chi tiết",
#        }
#
#    Cấu trúc 1 câu ĐIỀN ĐÁP ÁN (type sẽ tự được gán = "short"):
#        {
#            "content": "Nội dung câu hỏi",
#            "answers": ["12", "12.0"],   # có thể liệt kê nhiều cách viết đúng
#            "explanation": "Lời giải chi tiết",
#        }
#
#    Công thức toán dùng LaTeX (giống app thi tốt nghiệp): đặt trong
#    \\( ... \\) cho công thức trên cùng dòng, MathJax sẽ tự render đẹp.
# =======================================================================

EXAM_DEFS = [
    # ------------------------------------------------------------------
    # ĐỀ 1
    # ------------------------------------------------------------------
    {
        "id": "de1",
        "name": "Đề thi tham khảo số 1 - Đánh giá năng lực học sinh THPT 2025",
        "seed": 2025101,   # để trộn thứ tự xen kẽ trắc nghiệm/điền đáp án cố định
        "mc4": [
            {
                "content": "Giải phương trình \\( 3x - 5 = 16 \\). Nghiệm của phương trình là",
                "options": {"A": "7", "B": "6", "C": "8", "D": "5"},
                "correct": "A",
                "explanation": "\\( 3x - 5 = 16 \\Leftrightarrow 3x = 21 \\Leftrightarrow x = 7 \\). Đáp án A.",
            },
            {
                "content": "Phương trình \\( x^2 - 5x + 6 = 0 \\) có hai nghiệm \\( x_1, x_2 \\). Tổng \\( x_1 + x_2 \\) bằng",
                "options": {"A": "6", "B": "-5", "C": "5", "D": "-6"},
                "correct": "C",
                "explanation": "Theo định lí Vi-ét: \\( x_1 + x_2 = -b = 5 \\). Đáp án C.",
            },
            {
                "content": "Một lớp học có 40 học sinh, trong đó số học sinh nữ chiếm 40% tổng số học sinh của lớp. Hỏi lớp đó có bao nhiêu học sinh nam?",
                "options": {"A": "16", "B": "20", "C": "26", "D": "24"},
                "correct": "D",
                "explanation": "Số học sinh nữ là \\( 40 \\times 40\\% = 16 \\). Số học sinh nam là \\( 40 - 16 = 24 \\). Đáp án D.",
            },
            {
                "content": "Cho cấp số cộng \\( (u_n) \\) có số hạng đầu \\( u_1 = 3 \\) và công sai \\( d = 4 \\). Giá trị của \\( u_{10} \\) bằng",
                "options": {"A": "36", "B": "43", "C": "39", "D": "35"},
                "correct": "C",
                "explanation": "\\( u_{10} = u_1 + 9d = 3 + 9 \\times 4 = 39 \\). Đáp án C.",
            },
            {
                "content": "Cho hàm số \\( f(x) = 3x - 2 \\). Giá trị \\( f(4) \\) bằng",
                "options": {"A": "10", "B": "12", "C": "9", "D": "8"},
                "correct": "A",
                "explanation": "\\( f(4) = 3 \\times 4 - 2 = 10 \\). Đáp án A.",
            },
            {
                "content": "Một hình chữ nhật có chiều dài 12 cm và chiều rộng 5 cm. Diện tích hình chữ nhật đó bằng",
                "options": {"A": "17 cm²", "B": "70 cm²", "C": "60 cm²", "D": "50 cm²"},
                "correct": "C",
                "explanation": "Diện tích \\( S = 12 \\times 5 = 60 \\) cm². Đáp án C.",
            },
            {
                "content": "Cho dãy số liệu: 5, 7, 9, 11, 13. Số trung bình cộng của dãy số liệu trên bằng",
                "options": {"A": "8", "B": "10", "C": "7", "D": "9"},
                "correct": "D",
                "explanation": "Trung bình cộng \\( = (5+7+9+11+13):5 = 45:5 = 9 \\). Đáp án D.",
            },
            {
                "content": "Một nhóm có 8 học sinh. Hỏi có bao nhiêu cách chọn ra 3 học sinh từ nhóm đó (không phân biệt thứ tự)?",
                "options": {"A": "336", "B": "24", "C": "28", "D": "56"},
                "correct": "D",
                "explanation": "Số cách chọn là tổ hợp \\( C_8^3 = 56 \\) (cách). Đáp án D.",
            },
            {
                # CÂU VÍ DỤ minh họa cách chèn ẢNH và văn bản SAU ẢNH.
                # Hãy thay link "image" bằng ảnh thật của bạn (upload lên
                # GitHub/Imgur... rồi dán link raw vào đây) và sửa lại nội
                # dung/đáp án cho đúng với hình vẽ thật.
                "content": "Cho đồ thị hàm số \\( y = f(x) \\) như hình vẽ bên.",
                "image": "https://via.placeholder.com/480x260.png?text=Anh+minh+hoa+do+thi",
                "content_after_image": "Hàm số đã cho đồng biến trên khoảng nào sau đây?",
                "options": {"A": "\\( (-\\infty;0) \\)", "B": "\\( (0;+\\infty) \\)",
                            "C": "\\( (-1;1) \\)", "D": "\\( (-2;2) \\)"},
                "correct": "B",
                "explanation": "(Câu ví dụ) Đây chỉ là mẫu minh họa cách khai báo trường \"image\" và "
                               "\"content_after_image\" - hãy thay bằng ảnh và lời giải thật của bạn.",
            },
        ],
        "short": [
            {
                "content": "Giải phương trình \\( 5x + 7 = 32 \\). Tìm nghiệm x (điền số nguyên).",
                "answers": ["5"],
                "explanation": "\\( 5x + 7 = 32 \\Leftrightarrow 5x = 25 \\Leftrightarrow x = 5 \\).",
            },
            {
                "content": "Phương trình \\( x^2 - 2x - 15 = 0 \\) có nghiệm dương bằng bao nhiêu?",
                "answers": ["5"],
                "explanation": "\\( x^2 - 2x - 15 = (x-5)(x+3) = 0 \\Rightarrow x = 5 \\) hoặc \\( x = -3 \\). Nghiệm dương là 5.",
            },
            {
                "content": "Một cửa hàng có 300 sản phẩm, trong đó 15% là hàng lỗi. Hỏi có bao nhiêu sản phẩm lỗi? (chỉ điền số)",
                "answers": ["45"],
                "explanation": "Số sản phẩm lỗi \\( = 300 \\times 15\\% = 45 \\).",
            },
            {
                "content": "Tìm ước chung lớn nhất (ƯCLN) của 36 và 48. (chỉ điền số)",
                "answers": ["12"],
                "explanation": "\\( 36 = 2^2 \\times 3^2,\\ 48 = 2^4 \\times 3 \\Rightarrow \\text{ƯCLN} = 2^2 \\times 3 = 12 \\).",
            },
        ],
    },

    # ------------------------------------------------------------------
    # ĐỀ 2
    # ------------------------------------------------------------------
    {
        "id": "de2",
        "name": "Đề thi tham khảo số 2 - Đánh giá năng lực học sinh THPT 2025",
        "seed": 2025202,
        "mc4": [
            {
                "content": "Giải phương trình \\( 4x - 9 = 15 \\). Nghiệm của phương trình là",
                "options": {"A": "5", "B": "7", "C": "6", "D": "8"},
                "correct": "C",
                "explanation": "\\( 4x - 9 = 15 \\Leftrightarrow 4x = 24 \\Leftrightarrow x = 6 \\). Đáp án C.",
            },
            {
                "content": "Phương trình \\( x^2 - 7x + 10 = 0 \\) có hai nghiệm \\( x_1, x_2 \\). Tổng \\( x_1 + x_2 \\) bằng",
                "options": {"A": "10", "B": "-7", "C": "-10", "D": "7"},
                "correct": "D",
                "explanation": "Theo định lí Vi-ét: \\( x_1 + x_2 = -b = 7 \\). Đáp án D.",
            },
            {
                "content": "Một lớp học có 45 học sinh, trong đó số học sinh nữ chiếm 60% tổng số học sinh của lớp. Hỏi lớp đó có bao nhiêu học sinh nam?",
                "options": {"A": "27", "B": "20", "C": "18", "D": "22"},
                "correct": "C",
                "explanation": "Số học sinh nữ là \\( 45 \\times 60\\% = 27 \\). Số học sinh nam là \\( 45 - 27 = 18 \\). Đáp án C.",
            },
            {
                "content": "Cho cấp số cộng \\( (u_n) \\) có số hạng đầu \\( u_1 = -2 \\) và công sai \\( d = 5 \\). Giá trị của \\( u_{12} \\) bằng",
                "options": {"A": "53", "B": "58", "C": "48", "D": "50"},
                "correct": "A",
                "explanation": "\\( u_{12} = u_1 + 11d = -2 + 11 \\times 5 = 53 \\). Đáp án A.",
            },
            {
                "content": "Cho hàm số \\( f(x) = -2x + 7 \\). Giá trị \\( f(3) \\) bằng",
                "options": {"A": "1", "B": "-1", "C": "13", "D": "4"},
                "correct": "A",
                "explanation": "\\( f(3) = -2 \\times 3 + 7 = 1 \\). Đáp án A.",
            },
            {
                "content": "Một hình chữ nhật có chiều dài 15 cm và chiều rộng 8 cm. Diện tích hình chữ nhật đó bằng",
                "options": {"A": "23 cm²", "B": "130 cm²", "C": "110 cm²", "D": "120 cm²"},
                "correct": "D",
                "explanation": "Diện tích \\( S = 15 \\times 8 = 120 \\) cm². Đáp án D.",
            },
            {
                "content": "Cho dãy số liệu: 4, 6, 8, 10, 12. Số trung bình cộng của dãy số liệu trên bằng",
                "options": {"A": "9", "B": "7", "C": "8", "D": "10"},
                "correct": "C",
                "explanation": "Trung bình cộng \\( = (4+6+8+10+12):5 = 40:5 = 8 \\). Đáp án C.",
            },
            {
                "content": "Một nhóm có 9 học sinh. Hỏi có bao nhiêu cách chọn ra 4 học sinh từ nhóm đó (không phân biệt thứ tự)?",
                "options": {"A": "36", "B": "126", "C": "3024", "D": "84"},
                "correct": "B",
                "explanation": "Số cách chọn là tổ hợp \\( C_9^4 = 126 \\) (cách). Đáp án B.",
            },
        ],
        "short": [
            {
                "content": "Giải phương trình \\( 6x + 4 = 34 \\). Tìm nghiệm x (điền số nguyên).",
                "answers": ["5"],
                "explanation": "\\( 6x + 4 = 34 \\Leftrightarrow 6x = 30 \\Leftrightarrow x = 5 \\).",
            },
            {
                "content": "Phương trình \\( x^2 - x - 12 = 0 \\) có nghiệm dương bằng bao nhiêu?",
                "answers": ["4"],
                "explanation": "\\( x^2 - x - 12 = (x-4)(x+3) = 0 \\Rightarrow x = 4 \\) hoặc \\( x = -3 \\). Nghiệm dương là 4.",
            },
            {
                "content": "Một cửa hàng có 250 sản phẩm, trong đó 20% là hàng lỗi. Hỏi có bao nhiêu sản phẩm lỗi? (chỉ điền số)",
                "answers": ["50"],
                "explanation": "Số sản phẩm lỗi \\( = 250 \\times 20\\% = 50 \\).",
            },
            {
                "content": "Tìm bội chung nhỏ nhất (BCNN) của 18 và 24. (chỉ điền số)",
                "answers": ["72"],
                "explanation": "\\( 18 = 2 \\times 3^2,\\ 24 = 2^3 \\times 3 \\Rightarrow \\text{BCNN} = 2^3 \\times 3^2 = 72 \\).",
            },
        ],
    },

    # ------------------------------------------------------------------
    # ĐỀ 3
    # ------------------------------------------------------------------
    {
        "id": "de3",
        "name": "Đề thi tham khảo số 3 - Đánh giá năng lực học sinh THPT 2025",
        "seed": 2025303,
        "mc4": [
            {
                "content": "Giải phương trình \\( 7x - 3 = 25 \\). Nghiệm của phương trình là",
                "options": {"A": "3", "B": "5", "C": "4", "D": "6"},
                "correct": "C",
                "explanation": "\\( 7x - 3 = 25 \\Leftrightarrow 7x = 28 \\Leftrightarrow x = 4 \\). Đáp án C.",
            },
            {
                "content": "Phương trình \\( x^2 - 9x + 20 = 0 \\) có hai nghiệm \\( x_1, x_2 \\). Tổng \\( x_1 + x_2 \\) bằng",
                "options": {"A": "-9", "B": "20", "C": "-20", "D": "9"},
                "correct": "D",
                "explanation": "Theo định lí Vi-ét: \\( x_1 + x_2 = -b = 9 \\). Đáp án D.",
            },
            {
                "content": "Một lớp học có 60 học sinh, trong đó số học sinh nữ chiếm 25% tổng số học sinh của lớp. Hỏi lớp đó có bao nhiêu học sinh nam?",
                "options": {"A": "15", "B": "40", "C": "50", "D": "45"},
                "correct": "D",
                "explanation": "Số học sinh nữ là \\( 60 \\times 25\\% = 15 \\). Số học sinh nam là \\( 60 - 15 = 45 \\). Đáp án D.",
            },
            {
                "content": "Cho cấp số cộng \\( (u_n) \\) có số hạng đầu \\( u_1 = 10 \\) và công sai \\( d = -3 \\). Giá trị của \\( u_8 \\) bằng",
                "options": {"A": "-11", "B": "31", "C": "11", "D": "-8"},
                "correct": "A",
                "explanation": "\\( u_8 = u_1 + 7d = 10 + 7 \\times (-3) = -11 \\). Đáp án A.",
            },
            {
                "content": "Cho hàm số \\( f(x) = 5x - 4 \\). Giá trị \\( f(2) \\) bằng",
                "options": {"A": "10", "B": "6", "C": "-6", "D": "14"},
                "correct": "B",
                "explanation": "\\( f(2) = 5 \\times 2 - 4 = 6 \\). Đáp án B.",
            },
            {
                "content": "Một hình chữ nhật có chiều dài 20 cm và chiều rộng 9 cm. Diện tích hình chữ nhật đó bằng",
                "options": {"A": "29 cm²", "B": "190 cm²", "C": "180 cm²", "D": "200 cm²"},
                "correct": "C",
                "explanation": "Diện tích \\( S = 20 \\times 9 = 180 \\) cm². Đáp án C.",
            },
            {
                "content": "Cho dãy số liệu: 10, 12, 14, 16, 18. Số trung bình cộng của dãy số liệu trên bằng",
                "options": {"A": "13", "B": "15", "C": "16", "D": "14"},
                "correct": "D",
                "explanation": "Trung bình cộng \\( = (10+12+14+16+18):5 = 70:5 = 14 \\). Đáp án D.",
            },
            {
                "content": "Một nhóm có 10 học sinh. Hỏi có bao nhiêu cách chọn ra 3 học sinh từ nhóm đó (không phân biệt thứ tự)?",
                "options": {"A": "720", "B": "30", "C": "120", "D": "45"},
                "correct": "C",
                "explanation": "Số cách chọn là tổ hợp \\( C_{10}^3 = 120 \\) (cách). Đáp án C.",
            },
        ],
        "short": [
            {
                "content": "Giải phương trình \\( 9x - 11 = 61 \\). Tìm nghiệm x (điền số nguyên).",
                "answers": ["8"],
                "explanation": "\\( 9x - 11 = 61 \\Leftrightarrow 9x = 72 \\Leftrightarrow x = 8 \\).",
            },
            {
                "content": "Phương trình \\( x^2 - 3x - 18 = 0 \\) có nghiệm dương bằng bao nhiêu?",
                "answers": ["6"],
                "explanation": "\\( x^2 - 3x - 18 = (x-6)(x+3) = 0 \\Rightarrow x = 6 \\) hoặc \\( x = -3 \\). Nghiệm dương là 6.",
            },
            {
                "content": "Một cửa hàng có 400 sản phẩm, trong đó 10% là hàng lỗi. Hỏi có bao nhiêu sản phẩm lỗi? (chỉ điền số)",
                "answers": ["40"],
                "explanation": "Số sản phẩm lỗi \\( = 400 \\times 10\\% = 40 \\).",
            },
            {
                "content": "Tìm ước chung lớn nhất (ƯCLN) của 60 và 84. (chỉ điền số)",
                "answers": ["12"],
                "explanation": "\\( 60 = 2^2 \\times 3 \\times 5,\\ 84 = 2^2 \\times 3 \\times 7 \\Rightarrow \\text{ƯCLN} = 2^2 \\times 3 = 12 \\).",
            },
        ],
    },
]


def build_exam(exam_def):
    """Ghép câu trắc nghiệm + điền đáp án của 1 đề (viết tay ở EXAM_DEFS),
    gán id/số thứ tự, rồi TRỘN XEN KẼ ngẫu nhiên (nhưng cố định theo seed
    riêng của từng đề) để thứ tự câu 1..N không tách khối như file gốc."""
    exam_id = exam_def["id"]
    rng = random.Random(exam_def["seed"])

    questions = []
    for q in exam_def["mc4"]:
        q2 = dict(q)
        q2["type"] = "mc4"
        questions.append(q2)
    for q in exam_def["short"]:
        q2 = dict(q)
        q2["type"] = "short"
        questions.append(q2)

    rng.shuffle(questions)
    for idx, q in enumerate(questions, start=1):
        q["id"] = f"{exam_id}_q{idx:02d}"
        q["number"] = idx

    n_mc4 = len(exam_def["mc4"])
    n_short = len(exam_def["short"])
    description = f"{n_mc4 + n_short} câu hỏi: {n_mc4} trắc nghiệm, {n_short} điền đáp án."

    return {
        "id": exam_id, "name": exam_def["name"],
        "description": description, "questions": questions,
    }


EXAMS = [build_exam(d) for d in EXAM_DEFS]


def get_exam_by_id(exam_id):
    for e in EXAMS:
        if e["id"] == exam_id:
            return e
    return None




# =======================================================================
# 2) CHẤM ĐIỂM - mỗi câu 1 điểm, 50 câu = 50 điểm
# =======================================================================
def normalize_short(s):
    if s is None:
        return ""
    return str(s).strip().lower().replace(" ", "").replace(",", ".")


def check_short_answer(given, accepted_list):
    g = normalize_short(given)
    if not g:
        return False
    for acc in accepted_list:
        a = normalize_short(acc)
        if g == a:
            return True
        # So khớp thêm theo giá trị số (chấp nhận cả dạng phân số như "1/2"
        # trùng với "0.5") để tiện khi tự soạn thêm câu có đáp án là số.
        gv = av = None
        try:
            gv = float(Fraction(g))
        except Exception:
            try:
                gv = float(g)
            except Exception:
                gv = None
        try:
            av = float(Fraction(a))
        except Exception:
            try:
                av = float(a)
            except Exception:
                av = None
        if gv is not None and av is not None and abs(gv - av) < 1e-6:
            return True
    return False


def score_exam(exam, answers):
    total_points = 0.0
    answered_count = 0
    details = []
    per_point = TOTAL_POINTS / len(exam["questions"])
    for q in exam["questions"]:
        qid = q["id"]
        ans = answers.get(qid)
        entry = {"question": q}
        if q["type"] == "mc4":
            is_correct = (ans == q["correct"])
            pts = per_point if is_correct else 0.0
            if ans:
                answered_count += 1
            entry.update({"user_answer": ans, "is_correct": is_correct})
        else:
            given = (ans or "").strip()
            is_correct = check_short_answer(given, q["answers"])
            pts = per_point if is_correct else 0.0
            if given:
                answered_count += 1
            entry.update({"user_answer": given, "is_correct": is_correct})
        entry["points"] = round(pts, 2)
        total_points += pts
        details.append(entry)
    return round(total_points, 2), answered_count, details


# =======================================================================
# 3) GIAO DIỆN - TÔNG MÀU XANH LÁ (theo mẫu ảnh HSA / Map Study)
# =======================================================================
BASE_CSS = """
:root{
  --green-dark:#0b5b2c;
  --green:#1c8a43;
  --green-mid:#2fa356;
  --green-light:#eaf7ee;
  --green-border:#bfe4cb;
  --red:#c0392b;
}
*{box-sizing:border-box;}
body{background:#eef8f0;font-family:"Segoe UI",Roboto,Arial,sans-serif;color:#1b2b22;margin:0;}
.bg-grid{
  background-color:var(--green);
  background-image:
    linear-gradient(rgba(255,255,255,.12) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.12) 1px, transparent 1px);
  background-size:34px 34px;
}
.topbar{background:linear-gradient(90deg,var(--green-dark),var(--green-mid));color:#fff;padding:16px 0;text-align:center;}
.topbar h1{font-size:1.4rem;font-weight:800;margin:0;letter-spacing:.4px;}
.topbar .subtitle{font-size:.85rem;opacity:.9;}
.wrap{max-width:1100px;margin:0 auto;padding:24px 16px 60px;}
.panel{background:#fff;border-radius:14px;box-shadow:0 4px 18px rgba(11,91,44,.1);padding:24px;}
.panel-title{text-align:center;font-weight:800;color:var(--green-dark);font-size:1.25rem;margin-bottom:18px;}
.btn-green{background:var(--green);border:none;color:#fff;padding:10px 22px;border-radius:8px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;font-size:.95rem;}
.btn-green:hover{background:var(--green-dark);color:#fff;}
.btn-outline-green{background:#fff;border:1.5px solid var(--green);color:var(--green-dark);padding:9px 20px;border-radius:8px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;}
.btn-outline-green:hover{background:var(--green-light);}
label.form-label{font-weight:600;font-size:.92rem;}
.form-control{width:100%;padding:9px 12px;border:1px solid var(--green-border);border-radius:8px;margin-bottom:14px;font-size:.95rem;}
.exam-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px;margin-top:10px;}
.exam-card{border:1.5px solid var(--green-border);border-radius:14px;padding:18px;background:#fbfffb;}
.exam-card h5{color:var(--green-dark);font-weight:700;margin:0 0 8px;}
.exam-card p{color:#4d5c52;font-size:.88rem;min-height:36px;}
.exam-card .meta{color:#6b8072;font-size:.82rem;margin-bottom:12px;}
/* Màn hình chờ */
.wait-wrap{min-height:100vh;padding:40px 16px;}
.wait-inner{max-width:900px;margin:0 auto;}
.brand{display:flex;align-items:center;justify-content:center;gap:10px;color:#fff;font-weight:800;font-size:1.3rem;margin-bottom:26px;}
.brand .logo-box{width:34px;height:34px;border:2px solid #fff;border-radius:6px;display:flex;align-items:center;justify-content:center;}
.title-box{background:#fff;border-radius:16px;padding:22px 26px;text-align:center;margin-bottom:20px;}
.title-box h2{color:var(--green-dark);font-weight:900;font-size:1.7rem;margin:0 0 4px;letter-spacing:.5px;}
.title-box h3{color:var(--green);font-weight:800;font-size:1.05rem;margin:0;}
.wait-sub{color:#fff;text-align:center;font-size:1.02rem;margin-bottom:22px;}
.wait-sub b{font-size:1.12rem;}
.device{background:#fff;border-radius:16px;overflow:hidden;}
.device-topbar{background:#f1f3f4;padding:10px 18px;font-size:.8rem;font-weight:700;color:#333;text-align:center;}
.device-body{padding:30px 24px;text-align:center;}
.part-names{color:#1a3fae;font-weight:700;line-height:1.9;margin:12px 0 18px;font-size:.92rem;}
.arrow-row{display:flex;justify-content:center;gap:8px;margin:22px 0;flex-wrap:wrap;}
.arrow{width:34px;height:28px;border:2px solid var(--green);color:var(--green);display:flex;align-items:center;justify-content:center;font-weight:900;border-radius:3px;}
.current-part{color:var(--green-dark);font-weight:800;font-size:1.15rem;margin:14px 0 8px;}
.hsa-logo{display:flex;justify-content:center;gap:0;margin:18px auto;width:240px;font-weight:900;font-size:1.6rem;color:#fff;border-radius:6px;overflow:hidden;}
.hsa-logo div{flex:1;padding:12px 0;}
.hsa-logo .h{background:#888;} .hsa-logo .s{background:#1a5c33;} .hsa-logo .a{background:#c0392b;}
.wait-count{font-size:2.1rem;font-weight:900;color:var(--red);margin:14px 0;}
/* Giao diện làm bài */
.exam-header{background:var(--green-dark);color:#fff;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;border-radius:10px 10px 0 0;}
.exam-header .name{font-weight:700;}
.exam-header .meta{font-size:.8rem;opacity:.85;}
.timer-pill{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.35);border-radius:20px;padding:6px 16px;font-weight:800;white-space:nowrap;}
.timer-pill.warning{background:var(--red);animation:blink 1s infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.5;}}
.part-tab{background:var(--green-light);color:var(--green-dark);font-weight:700;padding:6px 14px;border-radius:6px;font-size:.82rem;display:inline-block;margin:10px 0 4px 4px;border:1px solid var(--green-border);}
.qnav-strip{display:flex;flex-wrap:wrap;gap:5px;padding:8px 16px;background:#fff;border-bottom:1px solid var(--green-border);}
.qnav-cell{width:30px;height:30px;border:1px solid var(--green-border);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:.76rem;font-weight:700;color:#333;cursor:pointer;background:#fff;}
.qnav-cell.answered{background:var(--green);color:#fff;border-color:var(--green-dark);}
.exam-main{background:#fff;padding:20px;border-radius:0 0 10px 10px;}
.part-title{color:var(--green-dark);font-weight:800;margin:20px 0 10px;border-left:4px solid var(--green);padding-left:10px;}
.part-title:first-child{margin-top:0;}
.q-block{border:1px solid var(--green-border);border-radius:10px;padding:16px;margin-bottom:16px;scroll-margin-top:120px;}
.q-num{display:inline-block;background:var(--green);color:#fff;font-weight:700;border-radius:50%;width:26px;height:26px;text-align:center;line-height:26px;font-size:.85rem;margin-right:8px;}
.q-content{font-size:.97rem;margin-bottom:12px;}
.opt-row{display:block;padding:7px 10px;border-radius:8px;margin-bottom:5px;cursor:pointer;}
.opt-row:hover{background:var(--green-light);}
.short-input{width:220px;padding:8px 10px;border:1px solid var(--green-border);border-radius:8px;}
.submit-bar{position:sticky;bottom:0;background:#fff;border-top:1px solid var(--green-border);padding:10px 16px;text-align:right;}
/* Modal nhắc nhở trước khi nộp bài */
.modal-overlay{position:fixed;inset:0;background:rgba(11,91,44,.55);display:none;align-items:center;justify-content:center;z-index:50;padding:16px;}
.modal-overlay.show{display:flex;}
.modal-box{background:#fff;border-radius:14px;max-width:520px;width:100%;padding:24px;text-align:center;}
.modal-box h4{color:var(--green-dark);font-weight:800;margin-bottom:10px;}
.unanswered-list{color:var(--red);font-weight:700;}
.modal-actions{display:flex;gap:12px;justify-content:center;margin-top:16px;}
/* Kết quả & đáp án */
.result-score{font-size:1.6rem;font-weight:900;color:var(--green);margin:14px 0;}
"""

BASE_HEAD_GREEN = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<style>""" + BASE_CSS + """</style>
<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\\\(', '\\\\)'], ['$', '$']],
    displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']]
  },
  svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</head>
<body>
<div class="topbar">
  <h1>KỲ THI ĐÁNH GIÁ NĂNG LỰC HSA - LUYỆN TẬP</h1>
  <div class="subtitle">Phần thi Toán học và xử lý số liệu (Tư duy định lượng) &middot; 50 câu &middot; 75 phút</div>
</div>
<div class="wrap">
"""
BASE_FOOT_GREEN = "</div></body></html>"

# ---------- Trang 1: nhập thông tin thí sinh ----------
TPL_INFO = BASE_HEAD_GREEN + """
<div class="panel" style="max-width:520px;margin:0 auto;">
  <div class="panel-title">NHẬP THÔNG TIN THÍ SINH</div>
  <form method="POST" action="{{ url_for('info') }}">
    <label class="form-label">Họ và tên *</label>
    <input class="form-control" type="text" name="full_name" required value="{{ student.get('full_name','') }}">
    <label class="form-label">Số báo danh *</label>
    <input class="form-control" type="text" name="sbd" required value="{{ student.get('sbd','') }}">
    <div style="text-align:center;margin-top:10px;">
      <button type="submit" class="btn-green">Tiếp tục &rarr;</button>
    </div>
  </form>
</div>
""" + BASE_FOOT_GREEN

# ---------- Trang 2: chọn đề thi ----------
TPL_EXAM_LIST = BASE_HEAD_GREEN + """
<div class="panel">
  <div class="panel-title">CHỌN ĐỀ THI THAM KHẢO</div>
  <p style="text-align:center;color:#4d5c52;">Xin chào <strong>{{ student.full_name }}</strong> - chọn một đề bên dưới để vào màn hình chờ trước khi làm bài.</p>
  <div class="exam-grid">
    {% for exam in exams %}
    <div class="exam-card">
      <h5>{{ exam.name }}</h5>
      <p>{{ exam.description }}</p>
      <div class="meta">{{ exam.questions|length }} câu hỏi &middot; {{ duration }} phút &middot; {{ total_points }} điểm</div>
      <a class="btn-green" style="width:100%;text-align:center;display:block;" href="{{ url_for('wait_screen', exam_id=exam.id) }}">Vào màn hình chờ</a>
    </div>
    {% endfor %}
  </div>
</div>
""" + BASE_FOOT_GREEN

# ---------- Trang 3: màn hình chờ (theo mẫu ảnh) ----------
TPL_WAIT = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<style>""" + BASE_CSS + """</style>
</head>
<body class="bg-grid">
<div class="wait-wrap"><div class="wait-inner">
  <div class="brand"><span class="logo-box">F</span> FOCUS EDU</div>
  <div class="title-box">
    <h2>MÀN HÌNH CHỜ</h2>
    <h3>TRƯỚC PHẦN THI TOÁN HỌC VÀ XỬ LÝ SỐ LIỆU</h3>
  </div>
  <div class="wait-sub">Có <b>{{ wait_seconds }} giây</b> nghỉ trước khi vào làm bài</div>

  <div class="device">
    <div class="device-topbar">{{ exam.name|upper }}</div>
    <div class="device-body">
      <p style="color:#556;margin-bottom:4px;">Bài thi tham khảo gồm các phần:</p>
      <div class="part-names">
        TOÁN HỌC VÀ XỬ LÝ SỐ LIỆU (TƯ DUY ĐỊNH LƯỢNG)<br>
        NGÔN NGỮ - VĂN HỌC (TƯ DUY ĐỊNH TÍNH)<br>
        KHOA HỌC hoặc TIẾNG ANH
      </div>
      <p style="color:#8a998f;font-size:.82rem;">(Bản luyện tập này triển khai phần <b>Tư duy định lượng</b> - làm tuần tự, không quay lại)</p>

      <div class="arrow-row">
        {% for i in range(9) %}<div class="arrow">&raquo;</div>{% endfor %}
      </div>

      <div class="current-part">TOÁN HỌC VÀ XỬ LÝ SỐ LIỆU (TƯ DUY ĐỊNH LƯỢNG)</div>
      <p style="color:#556;">Thời gian hoàn thành phần thi: <b>{{ duration }} phút</b><br>
      Tổng điểm phần thi tư duy định lượng: <b>{{ total_points }} điểm</b> &middot; {{ total_q }} câu hỏi</p>

      <div class="hsa-logo"><div class="h">H</div><div class="s">S</div><div class="a">A</div></div>

      <p style="color:#556;">Phần thi tự động bắt đầu sau {{ wait_seconds }} giây.<br>
      Nếu đã sẵn sàng, bạn có thể bấm nút &lt;BẮT ĐẦU&gt; dưới đây để bắt đầu phần thi.</p>

      <div class="wait-count" id="cd">{{ wait_seconds }}</div>

      <form method="POST" action="{{ url_for('start_exam', exam_id=exam.id) }}">
        <button type="submit" class="btn-green">BẮT ĐẦU</button>
      </form>
    </div>
  </div>
</div></div>
<script>
var t = {{ wait_seconds }};
var el = document.getElementById('cd');
var timer = setInterval(function () {
  t--; if (t < 0) t = 0;
  el.innerText = t;
  if (t <= 0) { clearInterval(timer); document.forms[0].submit(); }
}, 1000);
</script>
</body>
</html>
"""

# ---------- Trang 4: làm bài ----------
TPL_TAKE_EXAM = BASE_HEAD_GREEN + """
<div class="exam-header">
  <div>
    <div class="name">{{ student.full_name or 'Thí sinh' }}</div>
    <div class="meta">SBD: {{ student.sbd or '---' }} &middot; {{ exam.name }}</div>
  </div>
  <div class="timer-pill" id="timerPill">&#9201; --:--</div>
</div>
<div class="part-tab">TOÁN HỌC VÀ XỬ LÝ SỐ LIỆU (TƯ DUY ĐỊNH LƯỢNG)</div>

<form method="POST" action="{{ url_for('submit_exam') }}" id="examForm">
  <div class="qnav-strip">
    {% for q in questions %}
    <div class="qnav-cell" id="nav-{{ q.id }}" onclick="scrollToQ('{{ q.id }}')">{{ q.number }}</div>
    {% endfor %}
  </div>

  <div class="exam-main">
    {% if questions %}<div class="part-title">TOÁN HỌC VÀ XỬ LÝ SỐ LIỆU - 50 CÂU TRẮC NGHIỆM &amp; ĐIỀN ĐÁP ÁN XEN KẼ (mỗi câu 1 điểm)</div>{% endif %}
    {% for q in questions %}
      <div class="q-block" id="q-{{ q.id }}">
        <div class="q-content">
          <span class="q-num">{{ q.number }}</span>{{ q.content|safe }}
          <span style="float:right;font-size:.75rem;font-weight:700;color:#4d5c52;background:#eef5ee;padding:2px 10px;border-radius:10px;">
            {{ 'Trắc nghiệm' if q.type == 'mc4' else 'Điền đáp án' }}
          </span>
          {% if q.image %}
          <div style="text-align:center;margin:10px 0;">
            <img src="{{ q.image }}" alt="Hình minh họa câu {{ q.number }}" style="max-width:100%;border-radius:8px;">
          </div>
          {% endif %}
          {% if q.content_after_image %}<div style="margin-top:6px;">{{ q.content_after_image|safe }}</div>{% endif %}
        </div>
        {% if q.type == 'mc4' %}
          {% for k in ['A','B','C','D'] %}
          <label class="opt-row">
            <input type="radio" name="mc_{{ q.id }}" value="{{ k }}"> <strong>{{ k }}.</strong> {{ q.options[k]|safe }}
          </label>
          {% endfor %}
        {% else %}
          <input type="text" class="short-input" name="sh_{{ q.id }}" placeholder="Nhập đáp án...">
        {% endif %}
      </div>
    {% endfor %}
  </div>

  <div class="submit-bar">
    <span id="progressText" style="float:left;color:#556;">Đã trả lời: 0/{{ questions|length }}</span>
    <button type="button" class="btn-green" onclick="tryOpenSubmit()">NỘP BÀI</button>
  </div>
</form>

<div class="modal-overlay" id="reminderModal">
  <div class="modal-box">
    <h4>NHẮC NHỞ TRƯỚC KHI NỘP BÀI</h4>
    <div id="reminderMsg" style="font-size:.95rem;"></div>
    <p style="color:#556;margin-top:14px;">Khi đã kết thúc phần thi, bạn sẽ không quay lại phần thi được nữa.<br>Bạn chắc chắn <b>KẾT THÚC</b> phần thi này?</p>
    <div class="modal-actions">
      <button class="btn-green" onclick="doSubmit()">Có</button>
      <button class="btn-outline-green" onclick="closeModal()">Không</button>
    </div>
  </div>
</div>

<script>
var QUESTIONS = [
  {% for q in questions %}{ id: "{{ q.id }}", number: {{ q.number }}, type: "{{ q.type }}" }{{ "," if not loop.last }}
  {% endfor %}
];
var totalSeconds = {{ remaining_seconds }};
var autoSubmitting = false;
window.__unanswered = [];

function scrollToQ(id) {
  var el = document.getElementById('q-' + id);
  if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
}

function isAnswered(q) {
  if (q.type === 'mc4') {
    var els = document.getElementsByName('mc_' + q.id);
    for (var i = 0; i < els.length; i++) if (els[i].checked) return true;
    return false;
  } else {
    var el = document.getElementsByName('sh_' + q.id)[0];
    return el && el.value.trim().length > 0;
  }
}

function updateProgress() {
  var count = 0;
  var unanswered = [];
  QUESTIONS.forEach(function (q) {
    var cell = document.getElementById('nav-' + q.id);
    if (isAnswered(q)) { count++; if (cell) cell.classList.add('answered'); }
    else { if (cell) cell.classList.remove('answered'); unanswered.push(q.number); }
  });
  document.getElementById('progressText').innerText = 'Đã trả lời: ' + count + '/' + QUESTIONS.length;
  window.__unanswered = unanswered;
}

document.getElementById('examForm').addEventListener('change', updateProgress);
document.getElementById('examForm').addEventListener('input', updateProgress);
updateProgress();

function tryOpenSubmit() {
  updateProgress();
  var msg = document.getElementById('reminderMsg');
  if (window.__unanswered.length > 0) {
    msg.innerHTML = 'Hệ thống nhắc nhở: Bạn chưa làm câu <span class="unanswered-list">' +
      window.__unanswered.join(', ') + '</span>';
  } else {
    msg.innerHTML = '<span style="color:#1a6635;font-weight:700;">Bạn đã hoàn thành tất cả các câu hỏi.</span>';
  }
  document.getElementById('reminderModal').classList.add('show');
}
function closeModal() { document.getElementById('reminderModal').classList.remove('show'); }
function doSubmit() { autoSubmitting = true; document.getElementById('examForm').submit(); }

function tick() {
  if (totalSeconds <= 0) {
    document.getElementById('timerPill').innerText = '⏱ 00:00';
    if (!autoSubmitting) { autoSubmitting = true; document.getElementById('examForm').submit(); }
    return;
  }
  var m = Math.floor(totalSeconds / 60), s = totalSeconds % 60;
  var pill = document.getElementById('timerPill');
  pill.innerText = '⏱ ' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
  if (totalSeconds <= 300) pill.classList.add('warning');
  totalSeconds--;
}
tick();
setInterval(tick, 1000);
</script>
""" + BASE_FOOT_GREEN

# ---------- Trang 5: kết quả ----------
TPL_RESULT = BASE_HEAD_GREEN + """
<div class="panel" style="max-width:480px;margin:0 auto;text-align:center;">
  <div class="panel-title">KẾT QUẢ PHẦN THI TƯ DUY ĐỊNH LƯỢNG</div>
  <p style="color:#1a6635;font-weight:700;">Bạn đã nộp bài thành công!</p>
  <p>Số câu đã trả lời: <strong>{{ answered_count }}/{{ total_q }}</strong></p>
  <div class="result-score">Điểm: {{ score }}/{{ total_points }}</div>
  <div style="display:flex;gap:10px;justify-content:center;margin-top:18px;flex-wrap:wrap;">
    <a class="btn-green" href="{{ url_for('answer_detail') }}">Xem đáp án chi tiết</a>
    <a class="btn-outline-green" href="{{ url_for('exam_list') }}">Chọn đề khác</a>
  </div>
</div>
""" + BASE_FOOT_GREEN

# ---------- Trang 6: đáp án chi tiết ----------
TPL_ANSWER_DETAIL = BASE_HEAD_GREEN + """
<div class="panel">
  <div class="panel-title">ĐÁP ÁN &amp; LỜI GIẢI CHI TIẾT - {{ exam.name }}</div>
  <p style="text-align:center;color:#4d5c52;">Điểm đạt được: <strong style="color:var(--green-dark);">{{ score }}/{{ total_points }}</strong></p>

  {% for d in details %}
    {% set q = d.question %}
    <div class="q-block" style="border-left:5px solid {{ '#1a6635' if d.is_correct else '#c0392b' }};">
      <div class="q-content"><span class="q-num">{{ q.number }}</span>{{ q.content|safe }}
        <span style="float:right;font-weight:700;">{{ d.points }} điểm</span>
        {% if q.image %}
        <div style="text-align:center;margin:10px 0;">
          <img src="{{ q.image }}" alt="Hình minh họa câu {{ q.number }}" style="max-width:100%;border-radius:8px;">
        </div>
        {% endif %}
        {% if q.content_after_image %}<div style="margin-top:6px;">{{ q.content_after_image|safe }}</div>{% endif %}
      </div>

      {% if q.type == 'mc4' %}
        {% for k in ['A','B','C','D'] %}
        <div class="opt-row" style="{% if k==q.correct %}color:#1a6635;font-weight:700;{% elif k==d.user_answer and k!=q.correct %}color:#c0392b;font-weight:700;{% endif %}">
          <strong>{{ k }}.</strong> {{ q.options[k]|safe }}
          {% if k==q.correct %} ✔ Đáp án đúng{% endif %}
          {% if k==d.user_answer and k!=q.correct %} ✘ Bạn đã chọn{% endif %}
        </div>
        {% endfor %}
        {% if not d.user_answer %}<div style="color:#c0392b;">Bạn chưa chọn đáp án cho câu này.</div>{% endif %}
      {% else %}
        <div>Đáp án đúng: <strong style="color:#1a6635;">{{ q.answers[0] }}</strong></div>
        <div>Bạn đã trả lời: <strong style="{{ 'color:#1a6635;' if d.is_correct else 'color:#c0392b;' }}">{{ d.user_answer or '(bỏ trống)' }}</strong></div>
      {% endif %}

      <div style="background:#fff8e6;border-left:4px solid #f0ad4e;padding:10px 14px;border-radius:8px;font-size:.9rem;margin-top:10px;">
        <strong>Lời giải:</strong> {{ q.explanation|safe }}
      </div>
    </div>
  {% endfor %}

  <div style="text-align:center;margin-top:20px;">
    <a class="btn-green" href="{{ url_for('exam_list') }}">Hoàn thành</a>
  </div>
</div>
""" + BASE_FOOT_GREEN


# =======================================================================
# 4) ROUTES
# =======================================================================
@app.route("/", methods=["GET", "POST"])
@app.route("/thong-tin", methods=["GET", "POST"])
def info():
    if request.method == "POST":
        session["student"] = {
            "full_name": request.form.get("full_name", "").strip(),
            "sbd": request.form.get("sbd", "").strip(),
        }
        return redirect(url_for("exam_list"))
    student = session.get("student", {})
    return render_template_string(TPL_INFO, title="Nhập thông tin thí sinh", student=student)


@app.route("/de-thi")
def exam_list():
    student = session.get("student")
    if not student:
        return redirect(url_for("info"))
    return render_template_string(
        TPL_EXAM_LIST, title="Chọn đề thi tham khảo",
        student=student, exams=EXAMS, duration=EXAM_DURATION_MINUTES,
        total_points=TOTAL_POINTS,
    )


@app.route("/cho/<exam_id>")
def wait_screen(exam_id):
    student = session.get("student")
    if not student:
        return redirect(url_for("info"))
    exam = get_exam_by_id(exam_id)
    if not exam:
        return redirect(url_for("exam_list"))
    return render_template_string(
        TPL_WAIT, title="Màn hình chờ", exam=exam,
        wait_seconds=WAIT_SECONDS, duration=EXAM_DURATION_MINUTES,
        total_points=TOTAL_POINTS, total_q=len(exam["questions"]),
    )


@app.route("/bat-dau/<exam_id>", methods=["POST"])
def start_exam(exam_id):
    student = session.get("student")
    if not student:
        return redirect(url_for("info"))
    exam = get_exam_by_id(exam_id)
    if not exam:
        return redirect(url_for("exam_list"))
    session["attempt"] = {
        "attempt_id": uuid.uuid4().hex[:10],
        "exam_id": exam_id,
        "start_ts": time.time(),
        "submitted": False,
    }
    return redirect(url_for("take_exam"))


@app.route("/lam-bai")
def take_exam():
    student = session.get("student")
    attempt = session.get("attempt")
    if not student or not attempt:
        return redirect(url_for("info"))
    if attempt.get("submitted"):
        return redirect(url_for("result"))
    exam = get_exam_by_id(attempt["exam_id"])
    if not exam:
        return redirect(url_for("exam_list"))
    elapsed = time.time() - attempt["start_ts"]
    remaining = max(0, int(EXAM_DURATION_MINUTES * 60 - elapsed))
    return render_template_string(
        TPL_TAKE_EXAM, title="Làm bài thi",
        student=student, exam=exam, questions=exam["questions"],
        remaining_seconds=remaining,
    )


@app.route("/nop-bai", methods=["POST"])
def submit_exam():
    student = session.get("student")
    attempt = session.get("attempt")
    if not student or not attempt:
        return redirect(url_for("info"))
    exam = get_exam_by_id(attempt["exam_id"])
    if not exam:
        return redirect(url_for("exam_list"))

    answers = {}
    for q in exam["questions"]:
        qid = q["id"]
        if q["type"] == "mc4":
            answers[qid] = request.form.get(f"mc_{qid}")
        else:
            answers[qid] = request.form.get(f"sh_{qid}", "")

    score, answered_count, details = score_exam(exam, answers)

    attempt["submitted"] = True
    attempt["answers"] = answers
    attempt["score"] = score
    attempt["answered_count"] = answered_count
    session["attempt"] = attempt

    return redirect(url_for("result"))


@app.route("/ket-qua")
def result():
    student = session.get("student")
    attempt = session.get("attempt")
    if not student or not attempt or not attempt.get("submitted"):
        return redirect(url_for("info"))
    exam = get_exam_by_id(attempt["exam_id"])
    return render_template_string(
        TPL_RESULT, title="Kết quả thi",
        student=student, score=attempt["score"],
        answered_count=attempt["answered_count"],
        total_q=len(exam["questions"]), total_points=TOTAL_POINTS,
    )


@app.route("/ket-qua/dap-an")
def answer_detail():
    student = session.get("student")
    attempt = session.get("attempt")
    if not student or not attempt or not attempt.get("submitted"):
        return redirect(url_for("info"))
    exam = get_exam_by_id(attempt["exam_id"])
    _, _, details = score_exam(exam, attempt["answers"])
    return render_template_string(
        TPL_ANSWER_DETAIL, title="Đáp án chi tiết",
        student=student, exam=exam, score=attempt["score"],
        details=details, total_points=TOTAL_POINTS,
    )


# =======================================================================
# 5) CHẠY APP
# =======================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
