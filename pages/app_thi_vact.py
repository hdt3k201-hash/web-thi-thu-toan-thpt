# -*- coding: utf-8 -*-
"""
=======================================================================
  ỨNG DỤNG THI THỬ VACT (ĐHQG-HCM) - HOÀN CHỈNH TẤT CẢ CÁC PHẦN
  Tác giả: Toán Thầy Tùng
  Hướng dẫn chạy:
    1. pip install flask
    2. python app.py
    3. Truy cập http://localhost:5000
=======================================================================
"""
import copy
import os
import random
import time
import uuid

from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session
)

app = Flask(__name__)
# Đổi secret key này khi đưa lên server thực tế
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "vact-exam-secret-key-2026")

# Cấu hình thông số kỳ thi
EXAM_DURATION_MINUTES = 52.5                       # Thời gian làm bài: 52.5 phút
EXAM_DURATION_SECONDS = int(EXAM_DURATION_MINUTES * 60)  # 3150 giây
MATH_START_NUMBER = 61                             # Toán bắt đầu từ câu 61
LOGIC_START_NUMBER = 91                            # Logic bắt đầu từ câu 91
TOTAL_QUESTIONS = 42                               # 30 câu Toán + 12 câu Logic
TOTAL_POINTS = 42.0                                # 1 điểm / câu
EXAM_SUBJECT_NAME = "Toán học & Logic, Phân tích số liệu"

def format_minutes_vn(minutes):
    """Định dạng số phút kiểu Việt Nam (dùng dấu phẩy thay dấu chấm)."""
    return f"{minutes:g}".replace(".", ",")


# =======================================================================
# 1) DỮ LIỆU ĐỀ THI (CẤU TRÚC ĐỘC LẬP TỪNG ĐỀ NẰM TRONG DANH SÁCH)
# =======================================================================

EXAM_DEFS = [
    # -------------------------------------------------------------------
    # ĐỀ SỐ 1
    # -------------------------------------------------------------------
    {
        "id": "vact_de1",
        "title": "ĐỀ 1: ĐỀ THI THAM KHẢO VACT (ĐHQG-HCM)",
        "description": "Cấu trúc gồm 30 câu Toán học (Câu 61-90) & 12 câu Logic, Phân tích số liệu (Câu 91-102). Đề thi tích hợp dạng câu hỏi đơn lẻ và câu hỏi chùm dữ liệu dùng chung.",
        
        # --- PHẦN TOÁN HỌC ĐỀ 1 ---
        "math_blocks": [
            {
                "group_title": None,
                "group_text": None,
                "questions": [{
                    "id": "d1_m_61",
                    "content": "Giải phương trình \\( 2x + 7 = 23 \\). Nghiệm của phương trình là",
                    "options": {"A": "9", "B": "8", "C": "7", "D": "10"},
                    "correct": "B",
                    "explanation": "\\( 2x + 7 = 23 \\Leftrightarrow 2x = 16 \\Leftrightarrow x = 8 \\). Đáp án B."
                }]
            },
            {
                "group_title": None,
                "group_text": None,
                "questions": [{
                    "id": "d1_m_62",
                    "content": "Phương trình \\( x^2 - 6x + 8 = 0 \\) có hai nghiệm \\( x_1, x_2 \\). Tổng \\( x_1 + x_2 \\) bằng",
                    "options": {"A": "8", "B": "-6", "C": "-8", "D": "6"},
                    "correct": "D",
                    "explanation": "Theo định lí Vi-ét: \\( x_1 + x_2 = -b = 6 \\). Đáp án D."
                }]
            },
            {
                "group_title": None,
                "group_text": None,
                "questions": [{
                    "id": "d1_m_63",
                    "content": "Một lớp có 50 học sinh, trong đó số học sinh nữ chiếm 44% tổng số học sinh của lớp. Hỏi lớp đó có bao nhiêu học sinh nam?",
                    "options": {"A": "22", "B": "20", "C": "26", "D": "28"},
                    "correct": "D",
                    "explanation": "Số học sinh nữ là \\( 50 \\times 44\\% = 22 \\). Số học sinh nam là \\( 50 - 22 = 28 \\). Đáp án D."
                }]
            },
            {
                "group_title": "DỮ LIỆU DÙNG CHUNG TOÁN HỌC THỰC TẾ (ĐỀ 1)",
                "group_text": "Một doanh nghiệp sản xuất hai loại sản phẩm A và B. Chi phí nguyên vật liệu để sản xuất 1 đơn vị sản phẩm A là 100.000 đồng, 1 đơn vị sản phẩm B là 150.000 đồng. Tổng chi phí nguyên vật liệu tối đa cho phép là 15.000.000 đồng. Gọi \\( x, y \\) lần lượt là số sản phẩm A và B được sản xuất (với \\( x, y \\ge 0 \\)).",
                "questions": [
                    {
                        "id": "d1_m_grp_64",
                        "content": "Bất phương trình biểu diễn điều kiện giới hạn chi phí nguyên vật liệu là:",
                        "options": {
                            "A": "\\( 2x + 3y \\le 300 \\)",
                            "B": "\\( 3x + 2y \\le 300 \\)",
                            "C": "\\( x + y \\le 150 \\)",
                            "D": "\\( 2x + 3y \\ge 300 \\)"
                        },
                        "correct": "A",
                        "explanation": "Ta có: \\( 100.000x + 150.000y \\le 15.000.000 \\Leftrightarrow 2x + 3y \\le 300 \\). Đáp án A."
                    },
                    {
                        "id": "d1_m_grp_65",
                        "content": "Nếu doanh nghiệp đã sản xuất 60 sản phẩm A thì số sản phẩm B tối đa có thể sản xuất thêm là bao nhiêu?",
                        "options": {"A": "50", "B": "60", "C": "40", "D": "30"},
                        "correct": "B",
                        "explanation": "Thay \\( x = 60 \\) vào bất phương trình: \\( 2(60) + 3y \\le 300 \\Leftrightarrow 3y \\le 180 \\Leftrightarrow y \\le 60 \\). Đáp án B."
                    }
                ]
            }
        ],

        # --- PHẦN LOGIC & PHÂN TÍCH SỐ LIỆU ĐỀ 1 ---
        "logic_blocks": [
            {
                "group_title": "BÀI TOÁN LOGIC SUY LUẬN VỊ TRÍ (ĐỀ 1)",
                "group_text": "Có 5 bạn sinh viên A, B, C, D, E xếp thành một hàng ngang từ trái sang phải. Biết rằng:<br>- C không đứng ở hai đầu hàng.<br>- A đứng ngay bên trái của B.<br>- E đứng ở vị trí ngoài cùng bên phải.<br>- D đứng ngay bên phải của C.",
                "questions": [
                    {
                        "id": "d1_l_91",
                        "content": "Thứ tự sắp xếp của 5 bạn từ trái sang phải là:",
                        "options": {
                            "A": "A, B, C, D, E",
                            "B": "A, C, D, B, E",
                            "C": "C, D, A, B, E",
                            "D": "B, A, C, D, E"
                        },
                        "correct": "A",
                        "explanation": "E ở ngoài cùng bên phải (vị trí 5). A liền trái B. D liền phải C. C không ở đầu. Suy ra thứ tự: A, B, C, D, E. Đáp án A."
                    },
                    {
                        "id": "d1_l_92",
                        "content": "Bạn nào là người đứng ở vị trí chính giữa hàng?",
                        "options": {"A": "A", "B": "B", "C": "C", "D": "D"},
                        "correct": "C",
                        "explanation": "Thứ tự là A (1), B (2), C (3), D (4), E (5). Người đứng chính giữa là C. Đáp án C."
                    }
                ]
            },
            {
                "group_title": None,
                "group_text": None,
                "questions": [{
                    "id": "d1_l_93",
                    "content": "Tìm số tiếp theo trong dãy số: 2, 4, 8, 16, 32, ...",
                    "options": {"A": "64", "B": "48", "C": "50", "D": "128"},
                    "correct": "A",
                    "explanation": "Quy luật: Số sau gấp đôi số trước. \\( 32 \\times 2 = 64 \\). Đáp án A."
                }]
            }
        ]
    },

    # -------------------------------------------------------------------
    # ĐỀ SỐ 2
    # -------------------------------------------------------------------
    {
        "id": "vact_de2",
        "title": "ĐỀ 2: ĐỀ THI LUYỆN TẬP VACT NÂNG CAO",
        "description": "Nội dung đề thi thiết kế chuẩn hóa giúp thí sinh rèn luyện kĩ năng phản xạ nhanh, tính toán tối ưu và phân tích biểu đồ số liệu thực tế.",
        
        # --- PHẦN TOÁN HỌC ĐỀ 2 ---
        "math_blocks": [
            {
                "group_title": None,
                "group_text": None,
                "questions": [{
                    "id": "d2_m_61",
                    "content": "Đạo hàm của hàm số \\( y = x^3 - 3x + 1 \\) tại điểm \\( x = 2 \\) bằng",
                    "options": {"A": "9", "B": "6", "C": "12", "D": "3"},
                    "correct": "A",
                    "explanation": "\\( y' = 3x^2 - 3 \\Rightarrow y'(2) = 3(2^2) - 3 = 9 \\). Đáp án A."
                }]
            },
            {
                "group_title": None,
                "group_text": None,
                "questions": [{
                    "id": "d2_m_62",
                    "content": "Giá trị nhỏ nhất của hàm số \\( f(x) = x + \\dfrac{4}{x} \\) trên khoảng \\( (0; +\\infty) \\) là",
                    "options": {"A": "2", "B": "4", "C": "5", "D": "3"},
                    "correct": "B",
                    "explanation": "Theo BĐT Bất đẳng thức Cô-si: \\( x + \\dfrac{4}{x} \\ge 2\\sqrt{x \\cdot \\dfrac{4}{x}} = 4 \\). Dấu '=' xảy ra khi \\( x = 2 \\). Đáp án B."
                }]
            }
        ],

        # --- PHẦN LOGIC & PHÂN TÍCH SỐ LIỆU ĐỀ 2 ---
        "logic_blocks": [
            {
                "group_title": "BẢNG SỐ LIỆU DOANH SỐ CÔNG TY (ĐỀ 2)",
                "group_text": "Doanh số bán hàng (đơn vị: tỷ đồng) của công ty X trong 4 quý năm 2025:<br>- Quý 1: 120 tỷ<br>- Quý 2: 150 tỷ<br>- Quý 3: 180 tỷ<br>- Quý 4: 250 tỷ",
                "questions": [
                    {
                        "id": "d2_l_91",
                        "content": "Tổng doanh số bán hàng cả năm 2025 của công ty X là bao nhiêu?",
                        "options": {"A": "650 tỷ", "B": "700 tỷ", "C": "600 tỷ", "D": "750 tỷ"},
                        "correct": "B",
                        "explanation": "Tổng doanh số = 120 + 150 + 180 + 250 = 700 tỷ đồng. Đáp án B."
                    },
                    {
                        "id": "d2_l_92",
                        "content": "Doanh số Quý 4 tăng khoảng bao nhiêu phần trăm so với Quý 3?",
                        "options": {"A": "38,89%", "B": "35,50%", "C": "40,00%", "D": "28,00%"},
                        "correct": "A",
                        "explanation": "Tỉ lệ tăng = \\( \\dfrac{250 - 180}{180} \\times 100\\% \\approx 38,89\\% \\). Đáp án A."
                    }
                ]
            }
        ]
    }
]


# Tự động bổ sung đủ 30 câu Toán và 12 câu Logic cho mỗi đề nếu thiếu dữ liệu demo
for exam in EXAM_DEFS:
    # 1. Bổ sung Toán cho đủ 30 câu
    cur_m = sum(len(b["questions"]) for b in exam["math_blocks"])
    for i in range(cur_m + 1, 31):
        exam["math_blocks"].append({
            "group_title": None,
            "group_text": None,
            "questions": [{
                "id": f"{exam['id']}_m_auto_{i}",
                "content": f"[Câu {i + 60}] Cho hàm số \\( f(x) = {i}x + 5 \\). Giá trị của \\( f(1) \\) bằng",
                "options": {"A": str(i + 5), "B": str(i + 4), "C": str(i + 6), "D": str(i)},
                "correct": "A",
                "explanation": f"Thay \\( x = 1 \\) vào ta được \\( f(1) = {i}(1) + 5 = {i + 5} \\). Đáp án A."
            }]
        })
    # 2. Bổ sung Logic cho đủ 12 câu
    cur_l = sum(len(b["questions"]) for b in exam["logic_blocks"])
    for i in range(cur_l + 1, 13):
        exam["logic_blocks"].append({
            "group_title": None,
            "group_text": None,
            "questions": [{
                "id": f"{exam['id']}_l_auto_{i}",
                "content": f"[Câu {i + 90}] Số tiếp theo trong dãy số \\( {i}, {i*2}, {i*3}, \\dots \\) là",
                "options": {"A": str(i*4), "B": str(i*4 + 1), "C": str(i*3 + 1), "D": str(i*5)},
                "correct": "A",
                "explanation": f"Dãy số là cấp số cộng công sai \\( d = {i} \\). Số tiếp theo là \\( {i*4} \\). Đáp án A."
            }]
        })


# =======================================================================
# 2) HÀM XỬ LÝ ĐỀ THI & CHẤM ĐIỂM
# =======================================================================

def get_exam_by_id(exam_id):
    for e in EXAM_DEFS:
        if e["id"] == exam_id:
            return e
    return None

def build_shuffled_exam_session(exam, math_indices, logic_indices):
    """Tái tạo đề thi theo thứ tự khối đã xáo trộn và đánh số câu chuẩn xác."""
    shuffled_math_blocks = [copy.deepcopy(exam["math_blocks"][idx]) for idx in math_indices]
    shuffled_logic_blocks = [copy.deepcopy(exam["logic_blocks"][idx]) for idx in logic_indices]

    flat_questions = []

    # Đánh số Toán từ 61 đến 90
    q_num = MATH_START_NUMBER
    for block in shuffled_math_blocks:
        block_start = q_num
        for q in block["questions"]:
            q["number"] = q_num
            q["part"] = "math"
            flat_questions.append(q)
            q_num += 1
        block["start_num"] = block_start
        block["end_num"] = q_num - 1

    # Đánh số Logic từ 91 đến 102
    q_num = LOGIC_START_NUMBER
    for block in shuffled_logic_blocks:
        block_start = q_num
        for q in block["questions"]:
            q["number"] = q_num
            q["part"] = "logic"
            flat_questions.append(q)
            q_num += 1
        block["start_num"] = block_start
        block["end_num"] = q_num - 1

    return {
        "math_blocks": shuffled_math_blocks,
        "logic_blocks": shuffled_logic_blocks,
        "flat_questions": flat_questions,
    }

def score_exam_session(flat_questions, answers):
    total_points = 0.0
    answered_count = 0
    details = []

    for q in flat_questions:
        qid = q["id"]
        ans = answers.get(qid)
        is_correct = (ans == q["correct"])
        pts = 1.0 if is_correct else 0.0
        if ans:
            answered_count += 1
        details.append({
            "question": q,
            "user_answer": ans,
            "is_correct": is_correct,
            "points": round(pts, 2),
        })
        total_points += pts

    return round(total_points, 2), answered_count, details


# =======================================================================
# 3) GIAO DIỆN HTML, CSS & MATHJAX
# =======================================================================

BASE_CSS = """
:root{
  --blue-dark:#0a2a6b;
  --blue:#1560bd;
  --blue-mid:#2f7fe0;
  --blue-light:#eaf3fc;
  --blue-border:#bcdcf5;
  --red:#c0392b;
  --green:#0a6b2c;
}
*{box-sizing:border-box;}
body{background:#eef6fd;font-family:"Segoe UI",Roboto,Arial,sans-serif;color:#152238;margin:0;}
.topbar{background:linear-gradient(90deg,var(--blue-dark),var(--blue-mid));color:#fff;padding:16px 0;text-align:center;}
.topbar h1{font-size:1.4rem;font-weight:800;margin:0;letter-spacing:.4px;}
.topbar .subtitle{font-size:.85rem;opacity:.9;}
.wrap{max-width:1000px;margin:0 auto;padding:24px 16px 60px;}
.panel{background:#fff;border-radius:14px;box-shadow:0 4px 18px rgba(10,42,107,.12);padding:24px;}
.panel-title{text-align:center;font-weight:800;color:var(--blue-dark);font-size:1.25rem;margin-bottom:18px;}
.btn-blue{background:var(--blue);border:none;color:#fff;padding:10px 22px;border-radius:8px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;font-size:.95rem;}
.btn-blue:hover{background:var(--blue-dark);color:#fff;}
.btn-outline-blue{background:#fff;border:1.5px solid var(--blue);color:var(--blue-dark);padding:9px 20px;border-radius:8px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block;}
.btn-outline-blue:hover{background:var(--blue-light);}
.exam-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:22px;align-items:stretch;}
.exam-card{background:#fff;border-radius:14px;border-top:5px solid var(--blue-dark);box-shadow:0 4px 14px rgba(10,42,107,.12);padding:18px 18px 20px;display:flex;flex-direction:column;}
.exam-card-title{font-size:1.1rem;font-weight:800;color:var(--blue-dark);line-height:1.35;margin:0 0 10px;}
.exam-card-desc{color:#4d5c6e;font-size:.93rem;line-height:1.55;margin:0 0 16px;}
.exam-card-meta{margin-top:auto;padding-bottom:12px;color:#556;font-size:.85rem;}
.exam-card-btn{width:100%;text-align:center;padding:10px 0;}
label.form-label{font-weight:600;font-size:.92rem;}
.form-control{width:100%;padding:9px 12px;border:1px solid var(--blue-border);border-radius:8px;margin-bottom:14px;font-size:.95rem;}

.hero-topstrip{background:#fff;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 6px rgba(10,42,107,.08);}
.hero-topstrip .org-name{display:flex;align-items:center;gap:10px;color:var(--blue-dark);font-weight:800;font-size:1.05rem;line-height:1.15;}
.hero-topstrip .org-mark{width:38px;height:38px;border-radius:8px;background:linear-gradient(135deg,var(--blue),var(--blue-dark));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;}
.hero-banner{position:relative;overflow:hidden;min-height:140px;display:flex;align-items:center;justify-content:center;text-align:center;background:linear-gradient(180deg,#dbeeff 0%,#a9d3fb 45%,#6fb1ef 100%);}
.hero-banner .hero-text{position:relative;z-index:2;padding:18px;}
.hero-banner h2{margin:0;color:var(--blue-dark);font-weight:900;font-size:1.8rem;letter-spacing:.5px;text-shadow:2px 2px 0 #fff,-2px -2px 0 #fff,2px -2px 0 #fff,-2px 2px 0 #fff;}

.exam-header{background:var(--blue-dark);color:#fff;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;border-radius:10px 10px 0 0;position:sticky;top:0;z-index:20;}
.exam-header .name{font-weight:700;}
.exam-header .meta{font-size:.8rem;opacity:.85;}
.timer-pill{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.35);border-radius:20px;padding:6px 16px;font-weight:800;white-space:nowrap;}
.timer-pill.warning{background:var(--red);animation:blink 1s infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.5;}}

.part-section-title{background:var(--blue-dark);color:#fff;font-weight:800;padding:10px 16px;border-radius:8px;font-size:1.05rem;margin:24px 0 14px;display:flex;align-items:center;gap:8px;}
.group-stimulus{background:#f0f7ff;border:1.5px solid var(--blue-mid);border-radius:10px;padding:16px 18px;margin-bottom:16px;margin-top:16px;}
.group-title{font-weight:800;color:var(--blue-dark);margin-bottom:8px;font-size:1rem;text-transform:uppercase;border-bottom:1px solid var(--blue-border);padding-bottom:6px;}
.group-content{font-size:.95rem;line-height:1.5;color:#1d2d42;}

.qnav-strip{display:flex;flex-wrap:wrap;gap:5px;padding:10px 16px;background:#fff;border-bottom:1px solid var(--blue-border);position:sticky;top:52px;z-index:19;box-shadow:0 2px 5px rgba(0,0,0,.05);}
.qnav-cell{width:32px;height:28px;border:1px solid var(--blue-border);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:.74rem;font-weight:700;color:#333;cursor:pointer;background:#fff;}
.qnav-cell.answered{background:var(--blue);color:#fff;border-color:var(--blue-dark);}

.exam-main{background:#fff;padding:20px;border-radius:0 0 10px 10px;}
.q-block{border:1px solid var(--blue-border);border-radius:10px;padding:16px;margin-bottom:16px;scroll-margin-top:120px;}
.q-num{display:inline-block;background:var(--blue);color:#fff;font-weight:700;border-radius:50%;width:30px;height:30px;text-align:center;line-height:30px;font-size:.8rem;margin-right:8px;}
.q-content{font-size:.97rem;margin-bottom:12px;}
.opt-row{display:block;padding:8px 12px;border-radius:8px;margin-bottom:6px;cursor:pointer;border:1px solid transparent;}
.opt-row:hover{background:var(--blue-light);border-color:var(--blue-border);}

.submit-bar{position:sticky;bottom:0;background:#fff;border-top:1px solid var(--blue-border);padding:10px 16px;text-align:right;z-index:20;box-shadow:0 -2px 10px rgba(0,0,0,.05);}
.modal-overlay{position:fixed;inset:0;background:rgba(10,42,107,.55);display:none;align-items:center;justify-content:center;z-index:50;padding:16px;}
.modal-overlay.show{display:flex;}
.modal-box{background:#fff;border-radius:14px;max-width:520px;width:100%;padding:24px;text-align:center;}
.modal-box h4{color:var(--blue-dark);font-weight:800;margin-bottom:10px;}
.unanswered-list{color:var(--red);font-weight:700;}
.modal-actions{display:flex;gap:12px;justify-content:center;margin-top:16px;}
.result-score{font-size:1.8rem;font-weight:900;color:var(--blue);margin:14px 0;}
"""

MATHJAX_HEAD = """
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
"""

BASE_HEAD = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<style>""" + BASE_CSS + """</style>""" + MATHJAX_HEAD + """
</head>
<body>
<div class="topbar">
  <h1>KỲ THI ĐÁNH GIÁ NĂNG LỰC VACT - ÔN LẠI THI THỬ</h1>
  <div class="subtitle">""" + EXAM_SUBJECT_NAME + f" &middot; {TOTAL_QUESTIONS} câu (Câu 61 - 102) &middot; {format_minutes_vn(EXAM_DURATION_MINUTES)} phút</div>" + """
</div>
<div class="wrap">
"""

HERO_HEAD = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<style>""" + BASE_CSS + """</style>
</head>
<body>
<div class="hero-topstrip">
  <div class="org-name"><div class="org-mark">V</div> ĐẠI HỌC QUỐC GIA </div>
  <div class="org-name" style="font-size:.82rem;">TOÁN THẦY TÙNG - THI THỬ ONLINE</div>
</div>
<div class="hero-banner">
  <div class="hero-text">
    <h2>THI ĐÁNH GIÁ NĂNG LỰC VACT</h2>
  </div>
</div>
<div class="wrap">
"""

FOOTER = "</div></body></html>"


# --- HTML TEMPLATES ---

TPL_INFO = HERO_HEAD + """
<div class="panel" style="max-width:500px;margin:0 auto;">
  <div class="panel-title">NHẬP THÔNG TIN THÍ SINH</div>
  <form method="POST" action="{{ url_for('info') }}">
    <label class="form-label">Họ và tên thí sinh *</label>
    <input class="form-control" type="text" name="full_name" required placeholder="Ví dụ: Nguyễn Văn A" value="{{ student.get('full_name','') }}">
    <label class="form-label">Số báo danh *</label>
    <input class="form-control" type="text" name="sbd" required placeholder="Ví dụ: VACT001" value="{{ student.get('sbd','') }}">
    <div style="text-align:center;margin-top:10px;">
      <button type="submit" class="btn-blue">Tiếp tục &rarr;</button>
    </div>
  </form>
</div>
""" + FOOTER


TPL_EXAM_LIST = HERO_HEAD + """
<div class="panel">
  <div class="panel-title">DANH SÁCH ĐỀ THI VACT</div>
  <p style="text-align:center;color:#4d5c6e;margin-bottom:28px;">Xin chào <strong>{{ student.full_name }}</strong> (SBD: {{ student.sbd }}) - Chọn đề thi dưới đây để bắt đầu làm bài:</p>
  
  <div class="exam-grid">
    {% for exam in exams %}
    <div class="exam-card">
      <h3 class="exam-card-title">{{ exam.title }}</h3>
      <p class="exam-card-desc">{{ exam.description }}</p>
      <div class="exam-card-meta">{{ total_questions }} câu &middot; {{ duration }} phút &middot; {{ total_points }} điểm</div>
      <form method="POST" action="{{ url_for('start_exam', exam_id=exam.id) }}" style="margin:0;">
        <button type="submit" class="btn-blue exam-card-btn">Bắt đầu làm bài</button>
      </form>
    </div>
    {% endfor %}
  </div>
</div>
""" + FOOTER


TPL_TAKE_EXAM = BASE_HEAD + """
<div class="exam-header">
  <div>
    <div class="name">{{ student.full_name }} (SBD: {{ student.sbd }})</div>
    <div class="meta">{{ exam.title }}</div>
  </div>
  <div class="timer-pill" id="timerPill">&#9201; --:--</div>
</div>

<form method="POST" action="{{ url_for('submit_exam') }}" id="examForm">
  <!-- Thanh bấm nhảy tới câu hỏi -->
  <div class="qnav-strip">
    {% for q in exam_data.flat_questions %}
    <div class="qnav-cell" id="nav-{{ q.id }}" onclick="scrollToQ('{{ q.id }}')">{{ q.number }}</div>
    {% endfor %}
  </div>

  <div class="exam-main">
    <!-- PHẦN 1: TOÁN HỌC -->
    <div class="part-section-title">PHẦN 1: TOÁN HỌC (CÂU 61 - CÂU 90)</div>
    {% for block in exam_data.math_blocks %}
      {% if block.group_text %}
      <div class="group-stimulus">
        <div class="group-title">📌 {{ block.group_title or 'DỮ LIỆU DÙNG CHUNG' }} (CÂU {{ block.start_num }} - {{ block.end_num }})</div>
        <div class="group-content">{{ block.group_text|safe }}</div>
      </div>
      {% endif %}

      {% for q in block.questions %}
      <div class="q-block" id="q-{{ q.id }}">
        <div class="q-content">
          <span class="q-num">{{ q.number }}</span>{{ q.content|safe }}
        </div>
        {% for k in ['A','B','C','D'] %}
        <label class="opt-row">
          <input type="radio" name="mc_{{ q.id }}" value="{{ k }}"> <strong>{{ k }}.</strong> {{ q.options[k]|safe }}
        </label>
        {% endfor %}
      </div>
      {% endfor %}
    {% endfor %}

    <!-- PHẦN 2: LOGIC, PHÂN TÍCH SỐ LIỆU -->
    <div class="part-section-title" style="margin-top:36px;">PHẦN 2: LOGIC; PHÂN TÍCH SỐ LIỆU (CÂU 91 - CÂU 102)</div>
    {% for block in exam_data.logic_blocks %}
      {% if block.group_text %}
      <div class="group-stimulus">
        <div class="group-title">📌 {{ block.group_title or 'DỮ LIỆU DÙNG CHUNG' }} (CÂU {{ block.start_num }} - {{ block.end_num }})</div>
        <div class="group-content">{{ block.group_text|safe }}</div>
      </div>
      {% endif %}

      {% for q in block.questions %}
      <div class="q-block" id="q-{{ q.id }}">
        <div class="q-content">
          <span class="q-num">{{ q.number }}</span>{{ q.content|safe }}
        </div>
        {% for k in ['A','B','C','D'] %}
        <label class="opt-row">
          <input type="radio" name="mc_{{ q.id }}" value="{{ k }}"> <strong>{{ k }}.</strong> {{ q.options[k]|safe }}
        </label>
        {% endfor %}
      </div>
      {% endfor %}
    {% endfor %}
  </div>

  <div class="submit-bar">
    <span id="progressText" style="float:left;color:#556;line-height:36px;">Đã trả lời: 0/{{ exam_data.flat_questions|length }}</span>
    <button type="button" class="btn-blue" onclick="tryOpenSubmit()">NỘP BÀI</button>
  </div>
</form>

<!-- Modal Xác nhận nộp bài -->
<div class="modal-overlay" id="reminderModal">
  <div class="modal-box">
    <h4>NHẮC NHỞ TRƯỚC KHI NỘP BÀI</h4>
    <div id="reminderMsg" style="font-size:.95rem;"></div>
    <p style="color:#556;margin-top:14px;">Bạn có chắc chắn muốn <b>KẾT THÚC</b> phần thi này không?</p>
    <div class="modal-actions">
      <button class="btn-blue" onclick="doSubmit()">Có, nộp bài</button>
      <button class="btn-outline-blue" onclick="closeModal()">Xem lại bài</button>
    </div>
  </div>
</div>

<script>
var QUESTIONS = [
  {% for q in exam_data.flat_questions %}{ id: "{{ q.id }}", number: {{ q.number }} }{{ "," if not loop.last }}{% endfor %}
];
var totalSeconds = {{ remaining_seconds }};
var autoSubmitting = false;
window.__unanswered = [];

function scrollToQ(id) {
  var el = document.getElementById('q-' + id);
  if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
}

function isAnswered(q) {
  var els = document.getElementsByName('mc_' + q.id);
  for (var i = 0; i < els.length; i++) if (els[i].checked) return true;
  return false;
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
updateProgress();

function tryOpenSubmit() {
  updateProgress();
  var msg = document.getElementById('reminderMsg');
  if (window.__unanswered.length > 0) {
    msg.innerHTML = 'Hệ thống nhắc nhở: Bạn chưa làm câu <span class="unanswered-list">' +
      window.__unanswered.join(', ') + '</span>';
  } else {
    msg.innerHTML = '<span style="color:#0a2a6b;font-weight:700;">Bạn đã hoàn thành tất cả các câu hỏi.</span>';
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
""" + FOOTER


TPL_RESULT = BASE_HEAD + """
<div class="panel" style="max-width:480px;margin:0 auto;text-align:center;">
  <div class="panel-title">KẾT QUẢ THI VACT</div>
  <p style="color:#0a2a6b;font-weight:700;">Bạn đã nộp bài thành công!</p>
  <p>Số câu đã trả lời: <strong>{{ answered_count }}/{{ total_q }}</strong></p>
  <div class="result-score">Điểm: {{ score }}/{{ total_points }}</div>
  <div style="display:flex;gap:10px;justify-content:center;margin-top:18px;flex-wrap:wrap;">
    <a class="btn-blue" href="{{ url_for('answer_detail') }}">Xem đáp án &amp; lời giải</a>
    <a class="btn-outline-blue" href="{{ url_for('exam_list') }}">Chọn đề khác</a>
  </div>
</div>
""" + FOOTER


TPL_ANSWER_DETAIL = BASE_HEAD + """
<div class="panel">
  <div class="panel-title">ĐÁP ÁN &amp; LỜI GIẢI CHI TIẾT</div>
  <h3 style="text-align:center;color:var(--blue-dark);margin-top:-10px;">{{ exam.title }}</h3>
  <p style="text-align:center;color:#4d5c6e;">Điểm đạt được: <strong style="color:var(--blue-dark);">{{ score }}/{{ total_points }}</strong></p>

  <!-- PHẦN 1: TOÁN HỌC -->
  <div class="part-section-title">PHẦN 1: TOÁN HỌC (CÂU 61 - CÂU 90)</div>
  {% for block in exam_data.math_blocks %}
    {% if block.group_text %}
    <div class="group-stimulus">
      <div class="group-title">📌 {{ block.group_title or 'DỮ LIỆU DÙNG CHUNG' }} (CÂU {{ block.start_num }} - {{ block.end_num }})</div>
      <div class="group-content">{{ block.group_text|safe }}</div>
    </div>
    {% endif %}

    {% for q in block.questions %}
      {% set d = details_map[q.id] %}
      <div class="q-block" style="border-left:5px solid {{ '#0a6b2c' if d.is_correct else '#c0392b' }};">
        <div class="q-content"><span class="q-num">{{ q.number }}</span>{{ q.content|safe }}
          <span style="float:right;font-weight:700;">{{ d.points }} điểm</span>
        </div>

        {% for k in ['A','B','C','D'] %}
        <div class="opt-row" style="{% if k==q.correct %}color:#0a6b2c;font-weight:700;{% elif k==d.user_answer and k!=q.correct %}color:#c0392b;font-weight:700;{% endif %}">
          <strong>{{ k }}.</strong> {{ q.options[k]|safe }}
          {% if k==q.correct %} ✔ Đáp án đúng{% endif %}
          {% if k==d.user_answer and k!=q.correct %} ✘ Bạn đã chọn{% endif %}
        </div>
        {% endfor %}
        {% if not d.user_answer %}<div style="color:#c0392b;margin-top:6px;font-weight:600;">Bạn chưa chọn đáp án cho câu này.</div>{% endif %}

        <div style="background:#eef6ff;border-left:4px solid var(--blue);padding:10px 14px;border-radius:8px;font-size:.9rem;margin-top:10px;">
          <strong>Lời giải:</strong> {{ q.explanation|safe }}
        </div>
      </div>
    {% endfor %}
  {% endfor %}

  <!-- PHẦN 2: LOGIC; PHÂN TÍCH SỐ LIỆU -->
  <div class="part-section-title" style="margin-top:36px;">PHẦN 2: LOGIC; PHÂN TÍCH SỐ LIỆU (CÂU 91 - CÂU 102)</div>
  {% for block in exam_data.logic_blocks %}
    {% if block.group_text %}
    <div class="group-stimulus">
      <div class="group-title">📌 {{ block.group_title or 'DỮ LIỆU DÙNG CHUNG' }} (CÂU {{ block.start_num }} - {{ block.end_num }})</div>
      <div class="group-content">{{ block.group_text|safe }}</div>
    </div>
    {% endif %}

    {% for q in block.questions %}
      {% set d = details_map[q.id] %}
      <div class="q-block" style="border-left:5px solid {{ '#0a6b2c' if d.is_correct else '#c0392b' }};">
        <div class="q-content"><span class="q-num">{{ q.number }}</span>{{ q.content|safe }}
          <span style="float:right;font-weight:700;">{{ d.points }} điểm</span>
        </div>

        {% for k in ['A','B','C','D'] %}
        <div class="opt-row" style="{% if k==q.correct %}color:#0a6b2c;font-weight:700;{% elif k==d.user_answer and k!=q.correct %}color:#c0392b;font-weight:700;{% endif %}">
          <strong>{{ k }}.</strong> {{ q.options[k]|safe }}
          {% if k==q.correct %} ✔ Đáp án đúng{% endif %}
          {% if k==d.user_answer and k!=q.correct %} ✘ Bạn đã chọn{% endif %}
        </div>
        {% endfor %}
        {% if not d.user_answer %}<div style="color:#c0392b;margin-top:6px;font-weight:600;">Bạn chưa chọn đáp án cho câu này.</div>{% endif %}

        <div style="background:#eef6ff;border-left:4px solid var(--blue);padding:10px 14px;border-radius:8px;font-size:.9rem;margin-top:10px;">
          <strong>Lời giải:</strong> {{ q.explanation|safe }}
        </div>
      </div>
    {% endfor %}
  {% endfor %}

  <div style="text-align:center;margin-top:20px;">
    <a class="btn-blue" href="{{ url_for('exam_list') }}">Hoàn thành</a>
  </div>
</div>
""" + FOOTER


# =======================================================================
# 4) ĐIỀU HƯỚNG CÁC TRANG (ROUTES)
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
        student=student, exams=EXAM_DEFS, duration=format_minutes_vn(EXAM_DURATION_MINUTES),
        total_questions=TOTAL_QUESTIONS, total_points=TOTAL_POINTS
    )


@app.route("/bat-dau/<exam_id>", methods=["POST"])
def start_exam(exam_id):
    student = session.get("student")
    if not student:
        return redirect(url_for("info"))
    exam = get_exam_by_id(exam_id)
    if not exam:
        return redirect(url_for("exam_list"))

    # Xáo trộn danh sách khối câu hỏi
    math_indices = list(range(len(exam["math_blocks"])))
    random.shuffle(math_indices)

    logic_indices = list(range(len(exam["logic_blocks"])))
    random.shuffle(logic_indices)

    session["attempt"] = {
        "attempt_id": uuid.uuid4().hex[:10],
        "exam_id": exam_id,
        "math_indices": math_indices,
        "logic_indices": logic_indices,
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

    exam_data = build_shuffled_exam_session(
        exam, attempt["math_indices"], attempt["logic_indices"]
    )

    elapsed = time.time() - attempt["start_ts"]
    remaining = max(0, int(EXAM_DURATION_SECONDS - elapsed))

    return render_template_string(
        TPL_TAKE_EXAM, title="Làm bài thi VACT",
        student=student, exam=exam, exam_data=exam_data,
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

    exam_data = build_shuffled_exam_session(
        exam, attempt["math_indices"], attempt["logic_indices"]
    )

    answers = {q["id"]: request.form.get(f"mc_{q['id']}") for q in exam_data["flat_questions"]}
    score, answered_count, _ = score_exam_session(exam_data["flat_questions"], answers)

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

    return render_template_string(
        TPL_RESULT, title="Kết quả thi VACT",
        student=student, score=attempt["score"],
        answered_count=attempt["answered_count"],
        total_q=TOTAL_QUESTIONS, total_points=TOTAL_POINTS,
    )


@app.route("/ket-qua/dap-an")
def answer_detail():
    student = session.get("student")
    attempt = session.get("attempt")
    if not student or not attempt or not attempt.get("submitted"):
        return redirect(url_for("info"))

    exam = get_exam_by_id(attempt["exam_id"])
    exam_data = build_shuffled_exam_session(
        exam, attempt["math_indices"], attempt["logic_indices"]
    )

    _, _, details = score_exam_session(exam_data["flat_questions"], attempt["answers"])
    details_map = {d["question"]["id"]: d for d in details}

    return render_template_string(
        TPL_ANSWER_DETAIL, title="Đáp án chi tiết VACT",
        student=student, exam=exam, exam_data=exam_data,
        score=attempt["score"], details_map=details_map,
        total_points=TOTAL_POINTS,
    )


# =======================================================================
# 5) CHẠY ỨNG DỤNG
# =======================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)