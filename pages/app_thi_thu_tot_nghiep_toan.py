# -*- coding: utf-8 -*-
"""
=======================================================================
  ỨNG DỤNG THI THỬ TỐT NGHIỆP THPT - MÔN TOÁN (1 FILE PYTHON DUY NHẤT)
=======================================================================
Luồng sử dụng:
  1) Học sinh nhập thông tin cá nhân (họ tên, SBD, ngày sinh, ...).
  2) Chọn môn thi Toán (giao diện danh sách môn thi).
  3) Chọn 1 trong các đề thi Toán để bắt đầu làm bài.
  4) Làm bài: đề Toán có đúng 22 câu, gồm 3 dạng:
       - Phần I : 12 câu trắc nghiệm 4 lựa chọn      (0.25 điểm/câu)
       - Phần II: 4 câu Đúng/Sai (mỗi câu 4 ý nhỏ)   (theo số ý đúng)
       - Phần III: 6 câu trả lời ngắn                 (0.5 điểm/câu)
     (không có dạng kéo-thả) - đúng cấu trúc đề thi Toán THPT hiện hành,
     tổng điểm tối đa = 10.
  5) Nộp bài -> hiển thị kết quả (số câu đã làm, điểm đạt được).
  6) Xem đáp án & lời giải chi tiết từng câu.

Giao diện tông màu XANH DƯƠNG (không phải màu đỏ).
Chạy thử:
    pip install Flask
    python app.py
    -> mở http://127.0.0.1:5000
=======================================================================
"""
import os
import time
import uuid
from fractions import Fraction

from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "doi-key-nay-khi-deploy-that")

EXAM_DURATION_MINUTES = 90  # thời gian làm bài môn Toán (giống đề thi thật)

# =======================================================================
# 1) NGÂN HÀNG ĐỀ THI TOÁN - MỖI ĐỀ 22 CÂU (12 mc4 + 4 truefalse + 6 short)
# =======================================================================
EXAMS = [
    {
        "id": "de1",
        "name": "Đề số 1 - ÔN THI GK1 - 2026 - 2027.",
        "description": "22 câu hỏi: 12 trắc nghiệm, 4 đúng/sai, 6 trả lời ngắn.",
        "questions": [
            # ---------------- PHẦN I: TRẮC NGHIỆM 4 LỰA CHỌN ---------------

            {"id": "de1_mc_01", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = \\dfrac{x-1}{x} \\). Mệnh đề nào sau đây là đúng?",
 "options": {
   "A": "Hàm số đã cho đồng biến trên \\( \\mathbb{R}\\setminus\\{0\\} \\).",
   "B": "Hàm số đã cho chỉ đồng biến trên khoảng \\( (-\\infty;0) \\).",
   "C": "Hàm số đã cho đồng biến trên mỗi khoảng xác định.",
   "D": "Hàm số đã cho chỉ đồng biến trên khoảng \\( (0;+\\infty) \\)."
 },
 "correct": "C",
 "explanation": "Tập xác định \\( D = \\mathbb{R}\\setminus\\{0\\} \\).<br><br>Ta có \\( y' = \\dfrac{1}{x^2} > 0,\\ \\forall x \\neq 0 \\) nên hàm số đồng biến trên các khoảng \\( (-\\infty;0) \\) và \\( (0;+\\infty) \\).<br><br>Vậy hàm số đồng biến trên mỗi khoảng xác định. Đáp án C."},

{"id": "de1_mc_02", "part": 1, "type": "mc4",
 "content": "Tiệm cận ngang của đồ thị hàm số \\( y = \\dfrac{1-2x}{x+1} \\) là",
 "options": {
   "A": "\\( y = 1 \\).",
   "B": "\\( y = 2 \\).",
   "C": "\\( y = -2 \\).",
   "D": "\\( x = -1 \\)."
 },
 "correct": "C",
 "explanation": "Ta có:<br><br>\\( \\displaystyle\\lim_{x\\to+\\infty} y = \\lim_{x\\to+\\infty}\\dfrac{1-2x}{x+1} = -2 \\)<br><br>\\( \\displaystyle\\lim_{x\\to-\\infty} y = \\lim_{x\\to-\\infty}\\dfrac{1-2x}{x+1} = -2 \\)<br><br>Suy ra đồ thị hàm số có tiệm cận ngang \\( y = -2 \\). Đáp án C."},

{"id": "de1_mc_03", "part": 1, "type": "mc4",
 "content": "Hàm số \\( y = 2x^3 - x^2 + 5 \\) có điểm cực đại là",
 "options": {
   "A": "\\( y = 5 \\).",
   "B": "\\( x = 0 \\).",
   "C": "\\( M(0;5) \\).",
   "D": "\\( x = \\dfrac{1}{3} \\)."
 },
 "correct": "B",
 "explanation": "Ta có \\( y' = 6x^2 - 2x,\\ y'' = 12x - 2 \\).<br><br>\\( y' = 0 \\Leftrightarrow \\begin{bmatrix} x = 0 \\\\ x = \\dfrac{1}{3} \\end{bmatrix} \\)<br><br>\\( y''(0) = -2 < 0 \\Rightarrow x = 0 \\) là điểm cực đại của hàm số \\( y = 2x^3 - x^2 + 5 \\).<br><br><i>Chú ý: Phân biệt điểm cực đại của hàm số là \\( x_{cđ} \\), còn điểm cực đại của đồ thị hàm số là \\( (x_{cđ}; y_{cđ}) \\).</i> Đáp án B."},

{"id": "de1_mc_04", "part": 1, "type": "mc4",
 "content": "Đường cong trong hình dưới là đồ thị của một hàm số được liệt kê ở bốn phương án A, B, C, D dưới đây. Hỏi hàm số đó là hàm số nào?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau4.PNG",
 "options": {
   "A": "\\( y = x^4 - x^2 + 1 \\).",
   "B": "\\( y = -x^3 + 3x + 1 \\).",
   "C": "\\( y = -x^2 + x - 1 \\).",
   "D": "\\( y = x^3 - 3x + 1 \\)."
 },
 "correct": "D",
 "explanation": "Dựa vào hình dạng đồ thị: đây là đường cong bậc ba, có hệ số của \\( x^3 \\) dương (nhánh cuối đi lên), có hai điểm cực trị (một cực đại, một cực tiểu).<br><br>Loại phương án A vì đây là hàm bậc bốn (đồ thị dạng chữ W hoặc M, có trục đối xứng).<br><br>Loại phương án C vì đây là hàm bậc hai (đồ thị là parabol).<br><br>Loại phương án B vì hệ số của \\( x^3 \\) âm nên nhánh cuối của đồ thị phải đi xuống, không phù hợp với hình vẽ.<br><br>Vậy hàm số cần tìm là \\( y = x^3 - 3x + 1 \\). Đáp án D."},

{"id": "de1_mc_05", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) xác định trên nửa khoảng \\( [-1;3) \\) có bảng biến thiên như hình vẽ.",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau5.PNG",
 "content_after_image": "Khẳng định nào sau đây đúng?",
 "options": {
   "A": "\\( \\displaystyle\\min_{x\\in[-1;3)} f(x) = -2 \\).",
   "B": "\\( \\displaystyle\\max_{x\\in[-1;3)} f(x) = 2 \\).",
   "C": "\\( \\displaystyle\\min_{x\\in[-1;3)} f(x) = -1 \\).",
   "D": "\\( \\displaystyle\\max_{x\\in[-1;3)} f(x) = 1 \\)."
 },
 "correct": "A",
 "explanation": "Dựa vào bảng biến thiên ta thấy \\( f(x) \\geq -2\\ \\ \\forall x \\in [-1;3) \\) và \\( f(-1) = -2 \\).<br><br>Nên \\( \\displaystyle\\min_{x\\in[-1;3)} f(x) = -2 \\). Đáp án A."},

{"id": "de1_mc_06", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) xác định trên \\( \\mathbb{R}\\setminus\\{1\\} \\), liên tục trên mỗi khoảng xác định và có bảng biến thiên như hình bên. Hỏi đồ thị hàm số đã cho có bao nhiêu đường tiệm cận?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau6.PNG",
 "options": {
   "A": "\\( 2 \\).",
   "B": "\\( 3 \\).",
   "C": "\\( 4 \\).",
   "D": "\\( 1 \\)."
 },
 "correct": "B",
 "explanation": "Nhìn bảng biến thiên ta thấy:<br><br>\\( \\displaystyle\\lim_{x\\to+\\infty} f(x) = 5 \\)<br><br>\\( \\displaystyle\\lim_{x\\to-\\infty} f(x) = 3 \\)<br><br>\\( \\displaystyle\\lim_{x\\to 1^+} f(x) = +\\infty \\)<br><br>\\( \\displaystyle\\lim_{x\\to 1^-} f(x) = -\\infty \\)<br><br>Vì vậy đồ thị hàm số có ba đường tiệm cận: một tiệm cận đứng \\( x = 1 \\) và hai tiệm cận ngang \\( y = 3 \\) và \\( y = 5 \\). Đáp án B."},

            {"id": "de1_mc_07", "part": 1, "type": "mc4",
             "content": "Họ nguyên hàm của hàm số \\( f(x) = 3x^2 - 2x + 1 \\) là:",
             "options": {"A": "\\( x^3 - x^2 + x + C \\)", "B": "\\( 3x^3 - x^2 + x + C \\)", "C": "\\( x^3 - 2x^2 + x + C \\)", "D": "\\( x^3 - x^2 + C \\)"},
             "correct": "A",
             "explanation": "\\( \\int (3x^2-2x+1)\\,dx = x^3 - x^2 + x + C \\). Đáp án A."},

            {"id": "de1_mc_08", "part": 1, "type": "mc4",
             "content": "Cho hình chóp \\( S.ABCD \\) có đáy \\( ABCD \\) là hình vuông cạnh \\( a \\), \\( SA \\) vuông góc với đáy và \\( SA = a \\). Thể tích khối chóp \\( S.ABCD \\) bằng:",
             "options": {"A": "\\( \\dfrac{a^3}{3} \\)", "B": "\\( a^3 \\)", "C": "\\( \\dfrac{a^3}{6} \\)", "D": "\\( \\dfrac{a^3}{2} \\)"},
             "correct": "A",
             "explanation": "\\( V = \\dfrac{1}{3}\\cdot S_{ABCD}\\cdot SA = \\dfrac{1}{3}\\cdot a^2\\cdot a = \\dfrac{a^3}{3} \\). Đáp án A."},

            {"id": "de1_mc_09", "part": 1, "type": "mc4",
             "content": "Nghiệm của phương trình \\( 2^{x+1} = 32 \\) là:",
             "options": {"A": "4", "B": "3", "C": "5", "D": "16"},
             "correct": "A",
             "explanation": "\\( 2^{x+1}=2^5 \\Leftrightarrow x+1=5 \\Leftrightarrow x=4 \\). Đáp án A."},

            {"id": "de1_mc_10", "part": 1, "type": "mc4",
             "content": "Giá trị của \\( \\displaystyle\\lim_{x\\to 2}\\dfrac{x^2-4}{x-2} \\) bằng:",
             "options": {"A": "4", "B": "0", "C": "2", "D": "\\( +\\infty \\)"},
             "correct": "A",
             "explanation": "\\( \\dfrac{x^2-4}{x-2} = x+2 \\) (với \\( x\\ne2 \\)) \\( \\Rightarrow \\lim_{x\\to2}(x+2)=4 \\). Đáp án A."},

            {"id": "de1_mc_11", "part": 1, "type": "mc4",
             "content": "Đồ thị hàm số \\( y = \\dfrac{2x-1}{x+1} \\) có tiệm cận đứng là đường thẳng:",
             "options": {"A": "\\( x=-1 \\)", "B": "\\( x=1 \\)", "C": "\\( y=2 \\)", "D": "\\( y=-1 \\)"},
             "correct": "A",
             "explanation": "Mẫu số bằng 0 khi \\( x=-1 \\) (và tử số khác 0 tại đó) nên tiệm cận đứng là \\( x=-1 \\). Đáp án A."},

            {"id": "de1_mc_12", "part": 1, "type": "mc4",
             "content": "Trong mặt phẳng \\( Oxy \\), cho vectơ \\( \\vec{a} = (3;-4) \\). Độ dài vectơ \\( \\vec{a} \\) bằng:",
             "options": {"A": "5", "B": "7", "C": "25", "D": "1"},
             "correct": "A",
             "explanation": "\\( |\\vec{a}| = \\sqrt{3^2+(-4)^2} = \\sqrt{25} = 5 \\). Đáp án A."},

            # ---------------- PHẦN II: ĐÚNG / SAI ---------------
            {"id": "de1_tf_01", "part": 2, "type": "truefalse",
             "content": "Cho hàm số \\( y = x^3 - 3x^2 + 2 \\). Xét tính Đúng/Sai của các mệnh đề sau:",
             "statements": [
                 {"text": "\\( y' = 3x^2 - 6x \\)", "correct": True},
                 {"text": "Hàm số đạt cực đại tại \\( x=2 \\)", "correct": False},
                 {"text": "Giá trị cực tiểu của hàm số bằng \\( -2 \\)", "correct": True},
                 {"text": "Hàm số đồng biến trên khoảng \\( (0;2) \\)", "correct": False},
             ],
             "explanation": "\\( y'=3x^2-6x=3x(x-2)=0 \\Leftrightarrow x=0,x=2 \\). a) Đúng. b) \\( y''=6x-6,\\ y''(0)=-6<0 \\) nên cực đại tại \\( x=0 \\) (không phải \\( x=2 \\)) \\( \\Rightarrow \\) Sai. c) Cực tiểu tại \\( x=2 \\): \\( y(2)=8-12+2=-2 \\) \\( \\Rightarrow \\) Đúng. d) Trên \\( (0;2) \\), \\( y'=3x(x-2)<0 \\) nên hàm số nghịch biến (không đồng biến) \\( \\Rightarrow \\) Sai."},

            {"id": "de1_tf_02", "part": 2, "type": "truefalse",
             "content": "Cho hình lăng trụ đứng \\( ABC.A'B'C' \\) có đáy \\( ABC \\) là tam giác đều cạnh \\( a \\), chiều cao \\( AA' = 2a \\). Xét tính Đúng/Sai của các mệnh đề sau:",
             "statements": [
                 {"text": "Thể tích khối lăng trụ bằng \\( \\dfrac{a^3\\sqrt3}{2} \\)", "correct": True},
                 {"text": "\\( AA' \\) vuông góc với mặt phẳng \\( (ABC) \\)", "correct": True},
                 {"text": "Diện tích xung quanh của lăng trụ bằng \\( 6a^2 \\)", "correct": True},
                 {"text": "Diện tích toàn phần của lăng trụ bằng \\( 6a^2 \\)", "correct": False},
             ],
             "explanation": "Diện tích đáy \\( S=\\dfrac{a^2\\sqrt3}{4} \\). a) \\( V=S\\cdot AA' = \\dfrac{a^2\\sqrt3}{4}\\cdot2a=\\dfrac{a^3\\sqrt3}{2} \\) \\( \\Rightarrow \\) Đúng. b) Đúng theo tính chất lăng trụ đứng. c) \\( S_{xq}=3a\\cdot2a=6a^2 \\) \\( \\Rightarrow \\) Đúng. d) \\( S_{tp}=S_{xq}+2S=6a^2+\\dfrac{a^2\\sqrt3}{2}\\ne6a^2 \\) \\( \\Rightarrow \\) Sai."},

            {"id": "de1_tf_03", "part": 2, "type": "truefalse",
             "content": "Cho hàm số \\( y = \\log_3(x^2-1) \\). Xét tính Đúng/Sai của các mệnh đề sau:",
             "statements": [
                 {"text": "Tập xác định của hàm số là \\( D=(-\\infty;-1)\\cup(1;+\\infty) \\)", "correct": True},
                 {"text": "\\( y' = \\dfrac{2x}{(x^2-1)\\ln3} \\)", "correct": True},
                 {"text": "Hàm số xác định tại \\( x=0 \\)", "correct": False},
                 {"text": "Đồ thị hàm số đi qua điểm \\( (2;1) \\)", "correct": True},
             ],
             "explanation": "Điều kiện \\( x^2-1>0 \\Leftrightarrow x<-1 \\) hoặc \\( x>1 \\) \\( \\Rightarrow \\) a) Đúng. b) Áp dụng công thức đạo hàm \\( \\log \\) \\( \\Rightarrow \\) Đúng. c) Tại \\( x=0 \\): \\( x^2-1=-1<0 \\), không xác định \\( \\Rightarrow \\) Sai. d) Tại \\( x=2 \\): \\( y=\\log_3(3)=1 \\) \\( \\Rightarrow \\) Đúng."},

            {"id": "de1_tf_04", "part": 2, "type": "truefalse",
             "content": "Trong không gian \\( Oxyz \\), cho ba điểm \\( A(1;0;0) \\), \\( B(0;2;0) \\), \\( C(0;0;3) \\). Xét tính Đúng/Sai của các mệnh đề sau:",
             "statements": [
                 {"text": "\\( \\overrightarrow{AB} = (-1;2;0) \\)", "correct": True},
                 {"text": "Độ dài đoạn \\( AB \\) bằng \\( \\sqrt5 \\)", "correct": True},
                 {"text": "Mặt phẳng \\( (ABC) \\) có phương trình \\( \\dfrac{x}{1}+\\dfrac{y}{2}+\\dfrac{z}{3}=1 \\)", "correct": True},
                 {"text": "Trọng tâm tam giác \\( ABC \\) có tọa độ \\( (1;2;3) \\)", "correct": False},
             ],
             "explanation": "a) \\( \\overrightarrow{AB}=B-A=(-1;2;0) \\) \\( \\Rightarrow \\) Đúng. b) \\( AB=\\sqrt{1+4}=\\sqrt5 \\) \\( \\Rightarrow \\) Đúng. c) Đúng theo phương trình mặt phẳng đoạn chắn. d) Trọng tâm \\( G=\\left(\\dfrac13;\\dfrac23;1\\right) \\), không phải \\( (1;2;3) \\) \\( \\Rightarrow \\) Sai."},

            # ---------------- PHẦN III: TRẢ LỜI NGẮN ----------------
            {"id": "de1_sh_01", "part": 3, "type": "short",
             "content": "Tìm giá trị lớn nhất của hàm số \\( y = -x^2 + 4x - 1 \\) trên \\( \\mathbb{R} \\).",
             "answers": ["3"],
             "explanation": "\\( y=-(x-2)^2+3\\le3 \\), dấu bằng khi \\( x=2 \\). Vậy \\( \\max y = 3 \\)."},

            {"id": "de1_sh_02", "part": 3, "type": "short",
             "content": "Giải phương trình \\( \\log_2 x + \\log_2(x-2) = 3 \\) (với \\( x>2 \\)). Tìm \\( x \\).",
             "answers": ["4"],
             "explanation": "\\( \\log_2[x(x-2)]=3 \\Leftrightarrow x(x-2)=8 \\Leftrightarrow x^2-2x-8=0 \\Leftrightarrow x=4 \\) hoặc \\( x=-2 \\) (loại vì \\( x>2 \\)). Vậy \\( x=4 \\)."},

            {"id": "de1_sh_03", "part": 3, "type": "short",
             "content": "Cho hình chóp tứ giác đều \\( S.ABCD \\) có cạnh đáy \\( a=2 \\), cạnh bên bằng \\( \\sqrt6 \\). Tính chiều cao \\( h \\) của hình chóp.",
             "answers": ["2"],
             "explanation": "Nửa đường chéo đáy \\( = \\dfrac{2\\sqrt2}{2}=\\sqrt2 \\). \\( h=\\sqrt{(\\sqrt6)^2-(\\sqrt2)^2}=\\sqrt{6-2}=2 \\)."},

            {"id": "de1_sh_04", "part": 3, "type": "short",
             "content": "Một hộp có 10 viên bi đánh số từ 1 đến 10. Chọn ngẫu nhiên 3 viên. Tính xác suất để tổng 3 số ghi trên 3 viên là số chẵn (kết quả dạng phân số tối giản).",
             "answers": ["1/2"],
             "explanation": "Từ 1-10 có 5 số lẻ, 5 số chẵn. Tổng chẵn khi số lượng số lẻ được chọn là 0 hoặc 2. \\( C_5^3+C_5^2\\cdot C_5^1 = 10+50=60 \\). \\( n(\\Omega)=C_{10}^3=120 \\). Xác suất \\( =\\dfrac{60}{120}=\\dfrac12 \\)."},

            {"id": "de1_sh_05", "part": 3, "type": "short",
             "content": "Cho cấp số nhân \\( (u_n) \\) có \\( u_1=2 \\), công bội \\( q=3 \\). Tính tổng 5 số hạng đầu \\( S_5 \\).",
             "answers": ["242"],
             "explanation": "\\( S_5=u_1\\cdot\\dfrac{q^5-1}{q-1}=2\\cdot\\dfrac{243-1}{2}=242 \\)."},

            {"id": "de1_sh_06", "part": 3, "type": "short",
             "content": "Trong không gian \\( Oxyz \\), cho mặt cầu \\( (S): x^2+y^2+z^2-2x+4y-6z-2=0 \\). Tính bán kính \\( R \\) của mặt cầu.",
             "answers": ["4"],
             "explanation": "Tâm \\( I(1;-2;3) \\), \\( R=\\sqrt{1^2+(-2)^2+3^2+2}=\\sqrt{16}=4 \\)."},
        ],
    },
    {
        "id": "de2",
        "name": "Đề số 2 - Ôn tập Toán THPT",
        "description": "22 câu hỏi: 12 trắc nghiệm, 4 đúng/sai, 6 trả lời ngắn.",
        "questions": [
            # ---------------- PHẦN I: TRẮC NGHIỆM 4 LỰA CHỌN ----------------
            {"id": "de2_mc_01", "part": 1, "type": "mc4",
             "content": "Hàm số \\( y = -x^3 + 3x - 2 \\) nghịch biến trên khoảng nào sau đây?",
             "options": {"A": "\\( (-1;1) \\)", "B": "\\( (1;+\\infty) \\)", "C": "\\( (-2;0) \\)", "D": "\\( (0;2) \\)"},
             "correct": "B",
             "explanation": "\\( y'=-3x^2+3=-3(x-1)(x+1) \\). \\( y'<0 \\) khi \\( x<-1 \\) hoặc \\( x>1 \\), tức hàm số nghịch biến trên \\( (1;+\\infty) \\) (và \\( (-\\infty;-1) \\)). Đáp án B."},

            {"id": "de2_mc_02", "part": 1, "type": "mc4",
             "content": "Đạo hàm của hàm số \\( y = \\ln(3x+2) \\) là:",
             "options": {"A": "\\( \\dfrac{3}{3x+2} \\)", "B": "\\( \\dfrac{1}{3x+2} \\)", "C": "\\( \\dfrac{3}{x+2} \\)", "D": "\\( \\dfrac{\\ln3}{3x+2} \\)"},
             "correct": "A",
             "explanation": "\\( y'=\\dfrac{(3x+2)'}{3x+2}=\\dfrac{3}{3x+2} \\). Đáp án A."},

            {"id": "de2_mc_03", "part": 1, "type": "mc4",
             "content": "Tập nghiệm của bất phương trình \\( \\log_3(2x+1) > 2 \\) là:",
             "options": {"A": "\\( (4;+\\infty) \\)", "B": "\\( (-\\tfrac12;4) \\)", "C": "\\( (-\\infty;4) \\)", "D": "\\( (0;4) \\)"},
             "correct": "A",
             "explanation": "Điều kiện \\( x>-\\tfrac12 \\). \\( 2x+1>3^2=9 \\Leftrightarrow x>4 \\). Kết hợp điều kiện: \\( x\\in(4;+\\infty) \\). Đáp án A."},

            {"id": "de2_mc_04", "part": 1, "type": "mc4",
             "content": "Trong không gian \\( Oxyz \\), cho \\( A(2;-1;3) \\), \\( B(0;3;-1) \\). Vectơ \\( \\overrightarrow{AB} \\) có tọa độ là:",
             "options": {"A": "\\( (-2;4;-4) \\)", "B": "\\( (2;4;-4) \\)", "C": "\\( (-2;-4;-4) \\)", "D": "\\( (-2;4;4) \\)"},
             "correct": "A",
             "explanation": "\\( \\overrightarrow{AB}=B-A=(0-2;3-(-1);-1-3)=(-2;4;-4) \\). Đáp án A."},

            {"id": "de2_mc_05", "part": 1, "type": "mc4",
             "content": "Cho cấp số cộng \\( (u_n) \\) có \\( u_1=5 \\), công sai \\( d=-2 \\). Tổng 10 số hạng đầu \\( S_{10} \\) bằng:",
             "options": {"A": "-40", "B": "40", "C": "-30", "D": "-50"},
             "correct": "A",
             "explanation": "\\( S_{10}=\\dfrac{10}{2}\\left[2u_1+9d\\right]=5(10-18)=-40 \\). Đáp án A."},

            {"id": "de2_mc_06", "part": 1, "type": "mc4",
             "content": "Một túi có 4 viên bi đỏ, 6 viên bi xanh. Lấy ngẫu nhiên 2 viên. Xác suất để lấy được 2 viên khác màu là:",
             "options": {"A": "\\( \\dfrac{8}{15} \\)", "B": "\\( \\dfrac{2}{5} \\)", "C": "\\( \\dfrac{4}{15} \\)", "D": "\\( \\dfrac13 \\)"},
             "correct": "A",
             "explanation": "\\( n(\\Omega)=C_{10}^2=45 \\). Số cách chọn khác màu \\( =4\\times6=24 \\). Xác suất \\( =\\dfrac{24}{45}=\\dfrac{8}{15} \\). Đáp án A."},

            {"id": "de2_mc_07", "part": 1, "type": "mc4",
             "content": "Họ nguyên hàm của hàm số \\( f(x) = 4x^3 - 6x^2 + 2 \\) là:",
             "options": {"A": "\\( x^4 - 2x^3 + 2x + C \\)", "B": "\\( 4x^4 - 2x^3 + 2x + C \\)", "C": "\\( x^4 - 2x^3 + C \\)", "D": "\\( x^4 - 6x^3 + 2x + C \\)"},
             "correct": "A",
             "explanation": "\\( \\int(4x^3-6x^2+2)dx = x^4-2x^3+2x+C \\). Đáp án A."},

            {"id": "de2_mc_08", "part": 1, "type": "mc4",
             "content": "Cho hình chóp \\( S.ABC \\) có đáy \\( ABC \\) vuông tại \\( B \\), \\( AB=3 \\), \\( BC=4 \\), \\( SA \\) vuông góc với đáy và \\( SA=6 \\). Thể tích khối chóp bằng:",
             "options": {"A": "12", "B": "24", "C": "6", "D": "36"},
             "correct": "A",
             "explanation": "\\( S_{ABC}=\\dfrac12\\cdot3\\cdot4=6 \\). \\( V=\\dfrac13\\cdot6\\cdot6=12 \\). Đáp án A."},

            {"id": "de2_mc_09", "part": 1, "type": "mc4",
             "content": "Nghiệm của phương trình \\( 3^{2x-1} = 27 \\) là:",
             "options": {"A": "2", "B": "1", "C": "4", "D": "\\( \\tfrac52 \\)"},
             "correct": "A",
             "explanation": "\\( 3^{2x-1}=3^3\\Leftrightarrow2x-1=3\\Leftrightarrow x=2 \\). Đáp án A."},

            {"id": "de2_mc_10", "part": 1, "type": "mc4",
             "content": "Giá trị của \\( \\displaystyle\\lim_{x\\to3}\\dfrac{x^2-9}{x-3} \\) bằng:",
             "options": {"A": "6", "B": "0", "C": "3", "D": "9"},
             "correct": "A",
             "explanation": "\\( \\dfrac{x^2-9}{x-3}=x+3\\Rightarrow\\lim_{x\\to3}(x+3)=6 \\). Đáp án A."},

            {"id": "de2_mc_11", "part": 1, "type": "mc4",
             "content": "Đồ thị hàm số \\( y = \\dfrac{3x+2}{x-2} \\) có tiệm cận ngang là đường thẳng:",
             "options": {"A": "\\( y=3 \\)", "B": "\\( x=2 \\)", "C": "\\( y=2 \\)", "D": "\\( x=3 \\)"},
             "correct": "A",
             "explanation": "\\( \\lim_{x\\to\\pm\\infty} y = 3 \\) nên tiệm cận ngang là \\( y=3 \\). Đáp án A."},

            {"id": "de2_mc_12", "part": 1, "type": "mc4",
             "content": "Cho vectơ \\( \\vec{a}=(1;2;2) \\). Độ dài vectơ \\( \\vec{a} \\) bằng:",
             "options": {"A": "3", "B": "9", "C": "5", "D": "\\( \\sqrt5 \\)"},
             "correct": "A",
             "explanation": "\\( |\\vec a|=\\sqrt{1+4+4}=\\sqrt9=3 \\). Đáp án A."},

            # ---------------- PHẦN II: ĐÚNG / SAI ----------------
            {"id": "de2_tf_01", "part": 2, "type": "truefalse",
             "content": "Cho hàm số \\( y = x^3 - 6x^2 + 9x \\). Xét tính Đúng/Sai của các mệnh đề sau:",
             "statements": [
                 {"text": "\\( y' = 3x^2 - 12x + 9 \\)", "correct": True},
                 {"text": "Hàm số đạt cực đại tại \\( x=1 \\)", "correct": True},
                 {"text": "Giá trị cực tiểu của hàm số bằng \\( 0 \\)", "correct": True},
                 {"text": "Hàm số đồng biến trên khoảng \\( (1;3) \\)", "correct": False},
             ],
             "explanation": "\\( y'=3x^2-12x+9=3(x-1)(x-3) \\) \\( \\Rightarrow \\) a) Đúng. \\( y''=6x-12,\\ y''(1)=-6<0 \\) nên cực đại tại \\( x=1 \\) \\( \\Rightarrow \\) b) Đúng. Cực tiểu tại \\( x=3 \\): \\( y(3)=27-54+27=0 \\) \\( \\Rightarrow \\) c) Đúng. Trên \\( (1;3) \\), \\( y'<0 \\) (nghịch biến, không đồng biến) \\( \\Rightarrow \\) d) Sai."},

            {"id": "de2_tf_02", "part": 2, "type": "truefalse",
             "content": "Cho hình lăng trụ đứng \\( ABC.A'B'C' \\) có đáy \\( ABC \\) vuông tại \\( A \\), \\( AB=3 \\), \\( AC=4 \\), chiều cao \\( AA'=5 \\). Xét tính Đúng/Sai của các mệnh đề sau:",
             "statements": [
                 {"text": "Diện tích tam giác đáy \\( ABC \\) bằng \\( 6 \\)", "correct": True},
                 {"text": "Thể tích khối lăng trụ bằng \\( 30 \\)", "correct": True},
                 {"text": "Độ dài cạnh \\( BC \\) bằng \\( 7 \\)", "correct": False},
                 {"text": "Diện tích xung quanh của lăng trụ bằng \\( 60 \\)", "correct": True},
             ],
             "explanation": "a) \\( S_{ABC}=\\dfrac12\\cdot3\\cdot4=6 \\) \\( \\Rightarrow \\) Đúng. b) \\( V=6\\cdot5=30 \\) \\( \\Rightarrow \\) Đúng. c) \\( BC=\\sqrt{3^2+4^2}=5\\ne7 \\) \\( \\Rightarrow \\) Sai. d) \\( S_{xq}=(3+4+5)\\cdot5=60 \\) \\( \\Rightarrow \\) Đúng."},

            {"id": "de2_tf_03", "part": 2, "type": "truefalse",
             "content": "Cho hàm số \\( y = \\log_2(4-x^2) \\). Xét tính Đúng/Sai của các mệnh đề sau:",
             "statements": [
                 {"text": "Tập xác định của hàm số là \\( D=(-2;2) \\)", "correct": True},
                 {"text": "\\( y' = \\dfrac{-2x}{(4-x^2)\\ln2} \\)", "correct": True},
                 {"text": "Hàm số xác định tại \\( x=2 \\)", "correct": False},
                 {"text": "Đồ thị hàm số đi qua điểm \\( (0;2) \\)", "correct": True},
             ],
             "explanation": "Điều kiện \\( 4-x^2>0 \\Leftrightarrow -2<x<2 \\) \\( \\Rightarrow \\) a) Đúng. b) Đúng theo công thức đạo hàm. c) Tại \\( x=2 \\): \\( 4-x^2=0 \\), không xác định \\( \\Rightarrow \\) Sai. d) \\( y(0)=\\log_2 4=2 \\) \\( \\Rightarrow \\) Đúng."},

            {"id": "de2_tf_04", "part": 2, "type": "truefalse",
             "content": "Trong không gian \\( Oxyz \\), cho ba điểm \\( A(2;0;0) \\), \\( B(0;3;0) \\), \\( C(0;0;4) \\). Xét tính Đúng/Sai của các mệnh đề sau:",
             "statements": [
                 {"text": "\\( \\overrightarrow{AB} = (-2;3;0) \\)", "correct": True},
                 {"text": "Độ dài đoạn \\( AB \\) bằng \\( \\sqrt{13} \\)", "correct": True},
                 {"text": "Mặt phẳng \\( (ABC) \\) có phương trình \\( \\dfrac{x}{2}+\\dfrac{y}{3}+\\dfrac{z}{4}=1 \\)", "correct": True},
                 {"text": "Trọng tâm tam giác \\( ABC \\) có tọa độ \\( (2;3;4) \\)", "correct": False},
             ],
             "explanation": "a) \\( \\overrightarrow{AB}=(-2;3;0) \\) \\( \\Rightarrow \\) Đúng. b) \\( AB=\\sqrt{4+9}=\\sqrt{13} \\) \\( \\Rightarrow \\) Đúng. c) Đúng theo phương trình đoạn chắn. d) Trọng tâm \\( G=\\left(\\dfrac23;1;\\dfrac43\\right) \\), không phải \\( (2;3;4) \\) \\( \\Rightarrow \\) Sai."},

            # ---------------- PHẦN III: TRẢ LỜI NGẮN ----------------
            {"id": "de2_sh_01", "part": 3, "type": "short",
             "content": "Tìm giá trị nhỏ nhất của hàm số \\( y = x^2 - 6x + 5 \\) trên \\( \\mathbb{R} \\).",
             "answers": ["-4"],
             "explanation": "\\( y=(x-3)^2-4\\ge-4 \\), dấu bằng khi \\( x=3 \\). Vậy \\( \\min y=-4 \\)."},

            {"id": "de2_sh_02", "part": 3, "type": "short",
             "content": "Giải phương trình \\( \\log_3 x + \\log_3(x+6) = 3 \\) (với \\( x>0 \\)). Tìm \\( x \\).",
             "answers": ["3"],
             "explanation": "\\( \\log_3[x(x+6)]=3\\Leftrightarrow x^2+6x-27=0\\Leftrightarrow x=3 \\) hoặc \\( x=-9 \\) (loại vì \\( x>0 \\)). Vậy \\( x=3 \\)."},

            {"id": "de2_sh_03", "part": 3, "type": "short",
             "content": "Cho hình chóp tứ giác đều \\( S.ABCD \\) có cạnh đáy \\( a=2 \\), cạnh bên bằng \\( \\sqrt3 \\). Tính chiều cao \\( h \\) của hình chóp.",
             "answers": ["1"],
             "explanation": "Nửa đường chéo đáy \\( =\\sqrt2 \\). \\( h=\\sqrt{(\\sqrt3)^2-(\\sqrt2)^2}=\\sqrt{3-2}=1 \\)."},

            {"id": "de2_sh_04", "part": 3, "type": "short",
             "content": "Một hộp có 12 viên bi đánh số từ 1 đến 12. Chọn ngẫu nhiên 3 viên. Tính xác suất để tổng 3 số ghi trên 3 viên là số chẵn (kết quả dạng phân số tối giản).",
             "answers": ["1/2"],
             "explanation": "Từ 1-12 có 6 số lẻ, 6 số chẵn. Tổng chẵn khi số lượng số lẻ được chọn là 0 hoặc 2. \\( C_6^3+C_6^2\\cdot C_6^1=20+90=110 \\). \\( n(\\Omega)=C_{12}^3=220 \\). Xác suất \\( =\\dfrac{110}{220}=\\dfrac12 \\)."},

            {"id": "de2_sh_05", "part": 3, "type": "short",
             "content": "Cho cấp số nhân \\( (u_n) \\) có \\( u_1=3 \\), công bội \\( q=2 \\). Tính tổng 6 số hạng đầu \\( S_6 \\).",
             "answers": ["189"],
             "explanation": "\\( S_6=u_1\\cdot\\dfrac{q^6-1}{q-1}=3\\cdot\\dfrac{64-1}{1}=3\\cdot63=189 \\)."},

            {"id": "de2_sh_06", "part": 3, "type": "short",
             "content": "Trong không gian \\( Oxyz \\), cho mặt cầu \\( (S): x^2+y^2+z^2+4x-2y+6z-2=0 \\). Tính bán kính \\( R \\) của mặt cầu.",
             "answers": ["4"],
             "explanation": "Tâm \\( I(-2;1;-3) \\), \\( R=\\sqrt{(-2)^2+1^2+(-3)^2+2}=\\sqrt{16}=4 \\)."},
        ],
    },
]


def get_exam_by_id(exam_id):
    for e in EXAMS:
        if e["id"] == exam_id:
            return e
    return None


# =======================================================================
# 2) CHẤM ĐIỂM
#    - Trắc nghiệm 4 lựa chọn : 0.25 điểm / câu  (12 câu => 3 điểm)
#    - Đúng/Sai (4 ý/câu)     : 1 ý đúng=0.10 ; 2 ý=0.25 ; 3 ý=0.50 ; 4 ý=1.00
#      (4 câu => tối đa 4 điểm)
#    - Trả lời ngắn           : 0.5 điểm / câu (6 câu => 3 điểm)
#    Tổng tối đa = 10 điểm.
# =======================================================================
TF_POINTS_MAP = {0: 0.0, 1: 0.10, 2: 0.25, 3: 0.50, 4: 1.00}


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
    """answers: dict qid -> giá trị nộp (mc4: 'A'.. ; truefalse: {'0':'true'/'false',...}; short: chuỗi)"""
    total = 0.0
    answered_count = 0
    details = []
    for q in exam["questions"]:
        qid = q["id"]
        ans = answers.get(qid)
        pts = 0.0
        entry = {"question": q}

        if q["type"] == "mc4":
            is_correct = (ans == q["correct"])
            pts = 0.25 if is_correct else 0.0
            if ans:
                answered_count += 1
            entry.update({"user_answer": ans, "is_correct": is_correct})

        elif q["type"] == "truefalse":
            ans = ans or {}
            n_correct = 0
            stmt_detail = []
            for i, st in enumerate(q["statements"]):
                given = ans.get(str(i))
                is_ok = (given is not None) and ((given == "true") == st["correct"])
                if is_ok:
                    n_correct += 1
                stmt_detail.append({"text": st["text"], "correct": st["correct"], "given": given, "is_ok": is_ok})
            pts = TF_POINTS_MAP.get(n_correct, 0.0)
            if len(ans) == 4:
                answered_count += 1
            entry.update({"user_answer": ans, "stmt_detail": stmt_detail, "n_correct": n_correct})

        elif q["type"] == "short":
            given = (ans or "").strip()
            is_correct = check_short_answer(given, q["answers"])
            pts = 0.5 if is_correct else 0.0
            if given:
                answered_count += 1
            entry.update({"user_answer": given, "is_correct": is_correct})

        entry["points"] = round(pts, 2)
        total += pts
        details.append(entry)

    return round(total, 2), answered_count, details


# =======================================================================
# 3) GIAO DIỆN - TÔNG MÀU XANH DƯƠNG
# =======================================================================
BASE_CSS = """
:root {
  --xanh-dam: #0d3b7a;
  --xanh: #1565c0;
  --xanh-nhat: #1e88e5;
  --xanh-vien: #e3f0fd;
  --xanh-soft: #d3e6fb;
}
body { background-color:#eef4fb; font-family:"Segoe UI",Roboto,Arial,sans-serif; }
.topbar {
  background: linear-gradient(90deg,var(--xanh-dam),var(--xanh-nhat));
  color:#fff; padding:18px 0; text-align:center;
}
.topbar h1 { font-size:1.7rem; font-weight:800; letter-spacing:.5px; margin:0; }
.topbar .subtitle { font-size:.85rem; opacity:.9; }
.wrap { max-width:1100px; margin:0 auto; padding:24px 16px 60px; }
.panel { background:#fff; border-radius:14px; box-shadow:0 4px 18px rgba(13,59,122,.08); padding:24px; }
.panel-title { text-align:center; font-weight:800; color:var(--xanh-dam); font-size:1.35rem; margin-bottom:20px; }
.btn-xanh {
  background:var(--xanh); border:none; color:#fff; padding:10px 22px; border-radius:8px;
  font-weight:600; cursor:pointer; text-decoration:none; display:inline-block;
}
.btn-xanh:hover { background:var(--xanh-dam); color:#fff; }
.btn-outline-xanh {
  background:#fff; border:1.5px solid var(--xanh); color:var(--xanh); padding:9px 20px; border-radius:8px;
  font-weight:600; cursor:pointer; text-decoration:none; display:inline-block;
}
.btn-outline-xanh:hover { background:var(--xanh-vien); }
label.form-label { font-weight:600; color:#333; font-size:.92rem; }
.form-control, select.form-control {
  width:100%; padding:9px 12px; border:1px solid #c7d7ea; border-radius:8px; margin-bottom:14px; font-size:.95rem;
}
.info-box { background:var(--xanh-vien); border-radius:10px; padding:16px 18px; }
.info-box h6 { color:var(--xanh-dam); font-weight:700; margin-bottom:10px; }
.info-box .row-line { font-size:.9rem; margin-bottom:4px; color:#333; }
.subject-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:14px; margin-top:18px; }
.subject-card {
  border:1.5px solid #d3e6fb; border-radius:12px; padding:16px; text-align:center; background:#fbfdff;
}
.subject-card.active { border-color:var(--xanh); box-shadow:0 3px 10px rgba(21,101,192,.12); }
.subject-card .name { font-weight:700; color:var(--xanh-dam); margin-bottom:10px; }
.subject-card .disabled-tag { color:#94a3b8; font-size:.82rem; font-style:italic; }
.exam-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:18px; margin-top:10px; }
.exam-card { border:1.5px solid #d3e6fb; border-radius:14px; padding:18px; background:#fbfdff; }
.exam-card h5 { color:var(--xanh-dam); font-weight:700; }
.exam-card p { color:#556; font-size:.88rem; min-height:40px; }
.exam-card .meta { color:#789; font-size:.82rem; margin-bottom:12px; }
/* Giao diện làm bài */
.exam-topbar { background:var(--xanh-dam); color:#fff; padding:10px 18px; border-radius:10px 10px 0 0; }
.exam-topbar .name { font-weight:700; }
.exam-topbar .meta { font-size:.82rem; opacity:.85; }
.topbar-right { display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
.timer-pill {
  display:flex; align-items:center; gap:10px; background:rgba(255,255,255,.15);
  border:1px solid rgba(255,255,255,.35); border-radius:20px; padding:6px 16px;
}
.timer-text { font-weight:700; color:#fff; font-size:.95rem; white-space:nowrap; }
.timer-text.warning { color:#ffb4a8; animation: blink 1s infinite; }
.conn-status { display:flex; align-items:center; gap:6px; font-size:.78rem; color:#dff3e5; white-space:nowrap; }
.dot-green { width:8px; height:8px; border-radius:50%; background:#2ecc71; box-shadow:0 0 0 3px rgba(46,204,113,.25); flex:none; }
.btn-submit-white {
  background:#fff; color:var(--xanh-dam); font-weight:700; border:none;
  padding:9px 22px; border-radius:8px; cursor:pointer; font-size:.92rem;
}
.btn-submit-white:hover { background:var(--xanh-vien); }
.exam-toolbar {
  background:#fff; border-bottom:1px solid #e1eaf5; padding:8px 18px; display:flex;
  justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.5;} }
.exam-body { display:flex; gap:18px; align-items:flex-start; }
.exam-main { flex:1; background:#fff; border-radius:0 0 10px 10px; padding:20px; max-height:74vh; overflow-y:auto; }
.exam-side { width:230px; background:#fff; border-radius:10px; padding:14px; position:sticky; top:14px; }
.part-title { color:var(--xanh-dam); font-weight:800; font-size:1.02rem; margin:22px 0 12px; border-left:4px solid var(--xanh); padding-left:10px; }
.part-title:first-child { margin-top:0; }
.q-block { border:1px solid #e6edf7; border-radius:10px; padding:16px; margin-bottom:16px; scroll-margin-top:14px; }
.q-num { display:inline-block; background:var(--xanh); color:#fff; font-weight:700; border-radius:50%; width:26px; height:26px; text-align:center; line-height:26px; font-size:.85rem; margin-right:8px; }
.q-content { font-size:.98rem; margin-bottom:12px; }
.opt-row { display:block; padding:7px 10px; border-radius:8px; margin-bottom:5px; cursor:pointer; }
.opt-row:hover { background:var(--xanh-vien); }
.tf-table { width:100%; border-collapse:collapse; font-size:.92rem; }
.tf-table td { padding:7px 6px; border-bottom:1px solid #f0f3f8; }
.tf-table th { text-align:center; color:var(--xanh-dam); padding-bottom:6px; }
.short-input { width:220px; padding:8px 10px; border:1px solid #c7d7ea; border-radius:8px; }
.nav-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:6px; margin-top:10px; }
.nav-cell {
  width:100%; aspect-ratio:1; border:1px solid #c7d7ea; border-radius:6px; background:#fff; color:#333;
  font-size:.8rem; font-weight:600; cursor:pointer; display:flex; align-items:center; justify-content:center;
}
.nav-cell.answered { background:var(--xanh); color:#fff; border-color:var(--xanh-dam); }
.progress-text { font-size:.82rem; color:#556; margin-top:10px; text-align:center; }
/* Kết quả */
.result-card { max-width:480px; margin:40px auto; border:2px solid var(--xanh); border-radius:14px; padding:28px; text-align:center; background:#fff; }
.result-card h4 { color:var(--xanh-dam); font-weight:800; margin-bottom:18px; }
.result-line { font-size:1rem; margin-bottom:8px; }
.result-score { font-size:1.6rem; font-weight:800; color:var(--xanh); margin:14px 0; }
/* Đáp án chi tiết */
.review-block { border-radius:10px; padding:16px; margin-bottom:16px; border:1px solid #e6edf7; }
.review-block.ok { border-left:5px solid #2e7d32; }
.review-block.bad { border-left:5px solid #c0392b; }
.tag-ok { color:#2e7d32; font-weight:700; }
.tag-bad { color:#c0392b; font-weight:700; }
.explain-box { background:#fff8e6; border-left:4px solid #f0ad4e; padding:10px 14px; border-radius:8px; font-size:.9rem; margin-top:10px; }
.tf-review-row { display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px dashed #eee; font-size:.9rem; }
"""

BASE_HEAD = """
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
  <h1>GIAO DIỆN THI TRÊN MÁY TÍNH</h1>
  <div class="subtitle">Phần mềm luyện thi thử Tốt nghiệp THPT</div>
</div>
<div class="wrap">
"""

BASE_FOOT = """
</div>
</body>
</html>
"""

# ---------- Trang 1: nhập thông tin thí sinh ----------
TPL_INFO = BASE_HEAD + """
<div class="panel" style="max-width:640px;margin:0 auto;">
  <div class="panel-title">NHẬP THÔNG TIN THÍ SINH</div>
  <form method="POST" action="{{ url_for('info') }}">
    <label class="form-label">Họ và tên *</label>
    <input class="form-control" type="text" name="full_name" required value="{{ student.get('full_name','') }}">

    <div style="display:flex; gap:14px;">
      <div style="flex:1;">
        <label class="form-label">Số báo danh *</label>
        <input class="form-control" type="text" name="sbd" required value="{{ student.get('sbd','') }}">
      </div>
      <div style="flex:1;">
        <label class="form-label">Ngày sinh</label>
        <input class="form-control" type="text" name="dob" placeholder="dd/mm/yyyy" value="{{ student.get('dob','') }}">
      </div>
    </div>

    <div style="display:flex; gap:14px;">
      <div style="flex:1;">
        <label class="form-label">Giới tính</label>
        <select class="form-control" name="gender">
          <option value="Nam" {{ 'selected' if student.get('gender')=='Nam' else '' }}>Nam</option>
          <option value="Nữ" {{ 'selected' if student.get('gender')=='Nữ' else '' }}>Nữ</option>
        </select>
      </div>
      <div style="flex:1;">
        <label class="form-label">Ca thi</label>
        <input class="form-control" type="text" name="ca_thi" value="{{ student.get('ca_thi','1') }}">
      </div>
    </div>

    <div style="display:flex; gap:14px;">
      <div style="flex:1;">
        <label class="form-label">Hội đồng thi</label>
        <input class="form-control" type="text" name="hoi_dong" value="{{ student.get('hoi_dong','') }}">
      </div>
      <div style="flex:1;">
        <label class="form-label">Điểm thi</label>
        <input class="form-control" type="text" name="diem_thi" value="{{ student.get('diem_thi','') }}">
      </div>
      <div style="flex:1;">
        <label class="form-label">Phòng thi</label>
        <input class="form-control" type="text" name="phong_thi" value="{{ student.get('phong_thi','') }}">
      </div>
    </div>

    <div style="text-align:center; margin-top:16px;">
      <button type="submit" class="btn-xanh">Tiếp tục &rarr;</button>
    </div>
  </form>
</div>
""" + BASE_FOOT

# ---------- Trang 2: danh sách môn thi ----------
TPL_SUBJECTS = BASE_HEAD + """
<div class="panel">
  <div class="panel-title">KỲ THI  TỐT NGHIỆP THPT 2027</div>
  <div style="display:flex; gap:18px; flex-wrap:wrap;">
    <div class="info-box" style="flex:1; min-width:260px;">
      <h6>THÔNG TIN THÍ SINH</h6>
      <div class="row-line">Họ và tên: <strong>{{ student.full_name }}</strong></div>
      <div class="row-line">SBD: <strong>{{ student.sbd }}</strong></div>
      <div class="row-line">Ngày sinh: <strong>{{ student.dob or '—' }}</strong></div>
      <div class="row-line">Giới tính: <strong>{{ student.gender }}</strong></div>
      <div class="row-line">Ca thi: <strong>{{ student.ca_thi or '—' }}</strong></div>
    </div>
    <div class="info-box" style="flex:1; min-width:260px;">
      <h6>HỘI ĐỒNG THI</h6>
      <div class="row-line">Hội đồng thi: <strong>{{ student.hoi_dong or '—' }}</strong></div>
      <div class="row-line">Điểm thi: <strong>{{ student.diem_thi or '—' }}</strong></div>
      <div class="row-line">Phòng thi: <strong>{{ student.phong_thi or '—' }}</strong></div>
    </div>
  </div>

  <h5 style="color:var(--xanh-dam); font-weight:700; margin-top:26px;">DANH SÁCH MÔN THI</h5>
  <div class="subject-grid">
    <div class="subject-card active">
      <div class="name">Toán</div>
      <a class="btn-xanh" href="{{ url_for('exam_list') }}">Vào thi</a>
    </div>
    {% for mon in ['Ngữ văn','Tiếng Anh','Vật lí','Hóa học','Sinh học','Lịch sử','Địa lí','GDKT&PL','Tin học'] %}
    <div class="subject-card">
      <div class="name">{{ mon }}</div>
      <div class="disabled-tag">Sắp mở</div>
    </div>
    {% endfor %}
  </div>

  <div style="text-align:center; margin-top:24px;">
    <a class="btn-outline-xanh" href="{{ url_for('info') }}">&larr; Quay lại</a>
  </div>
</div>
""" + BASE_FOOT

# ---------- Trang 3: chọn đề thi Toán ----------
TPL_EXAM_LIST = BASE_HEAD + """
<div class="panel">
  <div class="panel-title">CHỌN ĐỀ THI ĐỂ BẮT ĐẦU - MÔN TOÁN</div>
  <p style="text-align:center; color:#556;">Xin chào <strong>{{ student.full_name }}</strong> - chọn một đề bên dưới rồi bấm "Bắt đầu làm bài".</p>

  <div class="exam-grid">
    {% for exam in exams %}
    <div class="exam-card">
      <h5>{{ exam.name }}</h5>
      <p>{{ exam.description }}</p>
      <div class="meta">{{ exam.questions|length }} câu hỏi &middot; {{ duration }} phút</div>
      <form method="POST" action="{{ url_for('start_exam', exam_id=exam.id) }}">
        <button type="submit" class="btn-xanh" style="width:100%;">Bắt đầu làm bài</button>
      </form>
    </div>
    {% endfor %}
  </div>

  <div style="text-align:center; margin-top:24px;">
    <a class="btn-outline-xanh" href="{{ url_for('subjects') }}">&larr; Quay lại</a>
  </div>
</div>
""" + BASE_FOOT

# ---------- Trang 4: làm bài ----------
TPL_TAKE_EXAM = BASE_HEAD + """
<div>
  <div class="exam-topbar" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
    <div>
      <div class="name">{{ student.full_name }}</div>
      <div class="meta">SBD: {{ student.sbd }} &middot; Môn thi: TOÁN &middot; Đề: {{ exam.name }}</div>
    </div>
    <div class="topbar-right">
      <div class="timer-pill">
        <span id="timer" class="timer-text">⏱ --:--</span>
        <span class="conn-status"><span class="dot-green"></span>Đang kết nối</span>
      </div>
      <button type="submit" form="examForm" class="btn-submit-white">NỘP BÀI</button>
    </div>
  </div>

  <!-- CHỈ MỘT FORM DUY NHẤT bao trọn toàn bộ câu hỏi + thanh công cụ,
       để tránh việc câu hỏi bị nhân đôi và cho phép nộp bài bất cứ lúc nào. -->
  <form method="POST" action="{{ url_for('submit_exam') }}" id="examForm" onsubmit="return confirmSubmit(event);">

    <div class="exam-toolbar">
      <div class="progress-text" id="progressText" style="margin:0;">Số câu đã trả lời: 0/{{ questions|length }}</div>
    </div>

    <div class="exam-body" style="margin-top:14px;">
      <div class="exam-main">
        {% set current_part = [0] %}
        {% for q in questions %}
          {% if q.part != current_part[0] %}
            {% if current_part.__setitem__(0, q.part) %}{% endif %}
            <div class="part-title">
              {% if q.part == 1 %}PHẦN I. Trắc nghiệm nhiều lựa chọn (mỗi câu 0.25 điểm)
              {% elif q.part == 2 %}PHẦN II. Đúng / Sai (mỗi ý đúng được tính điểm theo bảng quy đổi)
              {% else %}PHẦN III. Trả lời ngắn (mỗi câu 0.5 điểm)
              {% endif %}
            </div>
          {% endif %}

          <div class="q-block" id="q-{{ q.id }}">
            <div class="q-content"><span class="q-num">{{ loop.index }}</span>{{ q.content|safe }}</div>

            {% if q.type == 'mc4' %}
              {% for k in ['A','B','C','D'] %}
              <label class="opt-row">
                <input type="radio" name="mc_{{ q.id }}" value="{{ k }}"> <strong>{{ k }}.</strong> {{ q.options[k]|safe }}
              </label>
              {% endfor %}

            {% elif q.type == 'truefalse' %}
              <table class="tf-table">
                <tr><th style="text-align:left;">Mệnh đề</th><th>Đúng</th><th>Sai</th></tr>
                {% for st in q.statements %}
                <tr>
                  <td>{{ ['a) ','b) ','c) ','d) '][loop.index0] }}{{ st.text|safe }}</td>
                  <td style="text-align:center;"><input type="radio" name="tf_{{ q.id }}_{{ loop.index0 }}" value="true"></td>
                  <td style="text-align:center;"><input type="radio" name="tf_{{ q.id }}_{{ loop.index0 }}" value="false"></td>
                </tr>
                {% endfor %}
              </table>

            {% elif q.type == 'short' %}
              <input type="text" class="short-input" name="sh_{{ q.id }}" placeholder="Nhập đáp án...">
            {% endif %}
          </div>
        {% endfor %}
      </div>

      <div class="exam-side">
        <div style="font-weight:700; color:var(--xanh-dam); text-align:center;">Danh sách câu hỏi</div>
        <div class="nav-grid">
          {% for q in questions %}
          <div class="nav-cell" id="nav-{{ q.id }}" onclick="scrollToQ('{{ q.id }}')">{{ loop.index }}</div>
          {% endfor %}
        </div>
        <div class="progress-text" id="progressSide">Đã trả lời: 0/{{ questions|length }}</div>
      </div>
    </div>
  </form>
</div>

<script>
var QUESTIONS = [
  {% for q in questions %}{ id: "{{ q.id }}", type: "{{ q.type }}" }{{ "," if not loop.last }}
  {% endfor %}
];
var totalSeconds = {{ remaining_seconds }};
var autoSubmitting = false;

function scrollToQ(id) {
  var el = document.getElementById('q-' + id);
  if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
}

function isAnswered(q) {
  if (q.type === 'mc4') {
    var els = document.getElementsByName('mc_' + q.id);
    for (var i = 0; i < els.length; i++) if (els[i].checked) return true;
    return false;
  } else if (q.type === 'truefalse') {
    for (var i = 0; i < 4; i++) {
      var els = document.getElementsByName('tf_' + q.id + '_' + i);
      var ok = false;
      for (var j = 0; j < els.length; j++) if (els[j].checked) ok = true;
      if (!ok) return false;
    }
    return true;
  } else if (q.type === 'short') {
    var el = document.getElementsByName('sh_' + q.id)[0];
    return el && el.value.trim().length > 0;
  }
  return false;
}

function updateProgress() {
  var count = 0;
  QUESTIONS.forEach(function(q) {
    var cell = document.getElementById('nav-' + q.id);
    if (isAnswered(q)) {
      count++;
      if (cell) cell.classList.add('answered');
    } else {
      if (cell) cell.classList.remove('answered');
    }
  });
  var txt = 'Số câu đã trả lời: ' + count + '/' + QUESTIONS.length;
  document.getElementById('progressText').innerText = txt;
  document.getElementById('progressSide').innerText = 'Đã trả lời: ' + count + '/' + QUESTIONS.length;
}

document.getElementById('examForm').addEventListener('change', updateProgress);
document.getElementById('examForm').addEventListener('input', updateProgress);
updateProgress();

// Học sinh có thể bấm "NỘP BÀI" bất cứ lúc nào (kể cả chưa làm hết) - chỉ cần xác nhận.
function confirmSubmit(evt) {
  if (autoSubmitting) return true;
  var ok = confirm('Bạn có chắc chắn muốn nộp bài không? Sau khi nộp sẽ không thể chỉnh sửa đáp án.');
  if (!ok) { evt.preventDefault(); }
  return ok;
}

function tick() {
  if (totalSeconds <= 0) {
    document.getElementById('timer').innerText = '⏱ 00:00';
    autoSubmitting = true;
    document.getElementById('examForm').submit();
    return;
  }
  var m = Math.floor(totalSeconds / 60);
  var s = totalSeconds % 60;
  var label = '⏱ ' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
  var timerEl = document.getElementById('timer');
  timerEl.innerText = label;
  if (totalSeconds <= 300) timerEl.classList.add('warning');
  totalSeconds--;
}
tick();
setInterval(tick, 1000);
</script>
""" + BASE_FOOT

# ---------- Trang 5: kết quả ----------
TPL_RESULT = BASE_HEAD + """
<div class="result-card">
  <h4>GIAO DIỆN KẾT QUẢ THI</h4>
  <p style="color:#2e7d32; font-weight:600;">Bạn đã nộp bài thi thành công!</p>
  <div class="result-line">Số câu đã trả lời: <strong>{{ answered_count }}/{{ total_q }}</strong></div>
  <div class="result-score">Số điểm đạt được: {{ score }}/10</div>
  <div style="display:flex; gap:10px; justify-content:center; margin-top:18px;">
    <a class="btn-xanh" href="{{ url_for('answer_detail') }}">Xem đáp án chi tiết</a>
    <a class="btn-outline-xanh" href="{{ url_for('subjects') }}">Hoàn thành</a>
  </div>
</div>
""" + BASE_FOOT

# ---------- Trang 6: đáp án chi tiết ----------
TPL_ANSWER_DETAIL = BASE_HEAD + """
<div class="panel">
  <div class="panel-title">ĐÁP ÁN & LỜI GIẢI CHI TIẾT - {{ exam.name }}</div>
  <p style="text-align:center; color:#556;">Điểm đạt được: <strong style="color:var(--xanh);">{{ score }}/10</strong></p>

  {% for d in details %}
    {% set q = d.question %}
    <div class="review-block {{ 'ok' if (d.get('is_correct') or (q.type=='truefalse' and d.n_correct==4)) else 'bad' }}">
      <div class="q-content"><span class="q-num">{{ loop.index }}</span>{{ q.content|safe }}
        <span style="float:right; font-weight:700;">{{ d.points }} điểm</span>
      </div>

      {% if q.type == 'mc4' %}
        {% for k in ['A','B','C','D'] %}
          <div class="opt-row" style="{% if k==q.correct %}color:#2e7d32; font-weight:700;{% elif k==d.user_answer and k!=q.correct %}color:#c0392b; font-weight:700;{% endif %}">
            <strong>{{ k }}.</strong> {{ q.options[k]|safe }}
            {% if k==q.correct %} ✔ Đáp án đúng{% endif %}
            {% if k==d.user_answer and k!=q.correct %} ✘ Bạn đã chọn{% endif %}
          </div>
        {% endfor %}
        {% if not d.user_answer %}<div class="tag-bad">Bạn chưa chọn đáp án cho câu này.</div>{% endif %}

      {% elif q.type == 'truefalse' %}
        {% for sd in d.stmt_detail %}
        <div class="tf-review-row">
          <span>{{ ['a) ','b) ','c) ','d) '][loop.index0] }}{{ sd.text|safe }}</span>
          <span>
            Đáp án: <strong>{{ 'Đúng' if sd.correct else 'Sai' }}</strong>
            &middot; Bạn chọn: <strong class="{{ 'tag-ok' if sd.is_ok else 'tag-bad' }}">
              {% if sd.given == 'true' %}Đúng{% elif sd.given == 'false' %}Sai{% else %}(chưa chọn){% endif %}
            </strong>
          </span>
        </div>
        {% endfor %}
        <div style="margin-top:8px; font-size:.88rem; color:#556;">Số ý đúng: {{ d.n_correct }}/4</div>

      {% elif q.type == 'short' %}
        <div>Đáp án đúng: <strong style="color:#2e7d32;">{{ q.answers[0] }}</strong></div>
        <div>Bạn đã trả lời: <strong class="{{ 'tag-ok' if d.is_correct else 'tag-bad' }}">{{ d.user_answer or '(bỏ trống)' }}</strong></div>
      {% endif %}

      <div class="explain-box"><strong>Lời giải:</strong> {{ q.explanation|safe }}</div>
    </div>
  {% endfor %}

  <div style="text-align:center; margin-top:20px;">
    <a class="btn-xanh" href="{{ url_for('subjects') }}">Hoàn thành</a>
  </div>
</div>
""" + BASE_FOOT


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
            "dob": request.form.get("dob", "").strip(),
            "gender": request.form.get("gender", "Nam"),
            "ca_thi": request.form.get("ca_thi", "").strip(),
            "hoi_dong": request.form.get("hoi_dong", "").strip(),
            "diem_thi": request.form.get("diem_thi", "").strip(),
            "phong_thi": request.form.get("phong_thi", "").strip(),
        }
        return redirect(url_for("subjects"))

    student = session.get("student", {})
    return render_template_string(TPL_INFO, title="Nhập thông tin thí sinh", student=student)


@app.route("/mon-thi")
def subjects():
    student = session.get("student")
    if not student:
        return redirect(url_for("info"))
    return render_template_string(TPL_SUBJECTS, title="Danh sách môn thi", student=student)


@app.route("/toan/de-thi")
def exam_list():
    student = session.get("student")
    if not student:
        return redirect(url_for("info"))
    return render_template_string(
        TPL_EXAM_LIST, title="Chọn đề thi - Môn Toán",
        student=student, exams=EXAMS, duration=EXAM_DURATION_MINUTES
    )


@app.route("/toan/de-thi/<exam_id>/bat-dau", methods=["POST"])
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


@app.route("/thi")
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
        TPL_TAKE_EXAM, title="Làm bài thi - Môn Toán",
        student=student, exam=exam, questions=exam["questions"],
        remaining_seconds=remaining
    )


@app.route("/thi/nop-bai", methods=["POST"])
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
        elif q["type"] == "truefalse":
            d = {}
            for i in range(len(q["statements"])):
                val = request.form.get(f"tf_{qid}_{i}")
                if val is not None:
                    d[str(i)] = val
            answers[qid] = d
        elif q["type"] == "short":
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
        answered_count=attempt["answered_count"], total_q=len(exam["questions"])
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
        student=student, exam=exam, score=attempt["score"], details=details
    )


# =======================================================================
# 5) CHẠY APP
# =======================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
