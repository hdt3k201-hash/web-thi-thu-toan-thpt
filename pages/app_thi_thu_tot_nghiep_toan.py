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
 "content": "Giá trị lớn nhất của hàm số \\( f(x) = x^4 - 4x^2 + 5 \\) trên đoạn \\( [-2;3] \\) bằng",
 "options": {
   "A": "\\( 1 \\).",
   "B": "\\( 50 \\).",
   "C": "\\( 5 \\).",
   "D": "\\( 122 \\)."
 },
 "correct": "B",
 "explanation": "Ta có \\( f(x) = x^4 - 4x^2 + 5 \\) liên tục trên \\( [-2;3] \\) và \\( f'(x) = 4x^3 - 8x \\).<br><br>\\( f'(x) = 0 \\Leftrightarrow 4x^3 - 8x = 0 \\Leftrightarrow \\begin{bmatrix} x = 0 \\in [-2;3] \\\\ x = \\sqrt{2} \\in [-2;3] \\\\ x = -\\sqrt{2} \\in [-2;3] \\end{bmatrix} \\).<br><br>Ta có \\( f(0) = 5,\\ f(\\sqrt{2}) = f(-\\sqrt{2}) = 1,\\ f(-2) = 5,\\ f(3) = 50 \\).<br><br>Vậy giá trị lớn nhất của hàm số \\( f(x) = x^4 - 4x^2 + 5 \\) trên đoạn \\( [-2;3] \\) bằng \\( 50 \\), đạt được khi \\( x = 3 \\). Đáp án B."},

{"id": "de1_mc_08", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) có đồ thị như hình vẽ. Khẳng định nào sau đây đúng?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau8.PNG",
 "options": {
   "A": "Hàm số đồng biến trên khoảng \\( (-\\infty;-1) \\) và \\( (1;+\\infty) \\).",
   "B": "Hàm số nghịch biến trên khoảng \\( (-1;1) \\).",
   "C": "Hàm số đồng biến trên khoảng \\( (-1;3) \\).",
   "D": "Hàm số đồng biến trên khoảng \\( (-1;1) \\)."
 },
 "correct": "D",
 "explanation": "Nhìn vào đồ thị hàm số \\( y = f(x) \\) ta thấy hàm số đồng biến trên khoảng \\( (-1;1) \\). Đáp án D."},

{"id": "de1_mc_09", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) xác định, liên tục trên \\( \\mathbb{R} \\) và có bảng biến thiên như hình vẽ. Mệnh đề nào dưới đây đúng?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau9.PNG",
 "options": {
   "A": "Hàm số chỉ có giá trị nhỏ nhất, không có giá trị lớn nhất.",
   "B": "Hàm số có hai điểm cực trị.",
   "C": "Hàm số có giá trị lớn nhất bằng \\( 2 \\) và giá trị nhỏ nhất bằng \\( -3 \\).",
   "D": "Hàm số có một điểm cực trị."
 },
 "correct": "B",
 "explanation": "Tại \\( x = 0 \\) và \\( x = 1 \\) ta có \\( y' \\) đổi dấu và \\( y \\) tồn tại nên hàm số đã cho có hai điểm cực trị. Đáp án B."},

{"id": "de1_mc_10", "part": 1, "type": "mc4",
 "content": "Trong không gian với hệ tọa độ \\( Oxyz \\), cho vectơ \\( \\overrightarrow{AO} = 3(\\vec{i}+4\\vec{j}) - 2\\vec{k} + 5\\vec{j} \\). Tọa độ của điểm \\( A \\) là:",
 "options": {
   "A": "\\( A(3;5;-2) \\).",
   "B": "\\( A(3;17;2) \\).",
   "C": "\\( A(3;-2;5) \\).",
   "D": "\\( A(-3;-17;2) \\)."
 },
 "correct": "D",
 "explanation": "Ta có \\( \\overrightarrow{AO} = 3(\\vec{i}+4\\vec{j}) - 2\\vec{k} + 5\\vec{j} = 3\\vec{i} + 17\\vec{j} - 2\\vec{k} \\)<br><br>\\( \\Leftrightarrow \\overrightarrow{OA} = -3\\vec{i} - 17\\vec{j} + 2\\vec{k} \\)<br><br>\\( \\Leftrightarrow A(-3;-17;2) \\). Đáp án D."},

{"id": "de1_mc_11", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) có đồ thị như hình vẽ. Hàm số \\( y = f(x) \\) đồng biến trên khoảng nào dưới đây?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau11.PNG",
 "options": {
   "A": "\\( (-2;2) \\).",
   "B": "\\( (-\\infty;0) \\).",
   "C": "\\( (2;+\\infty) \\).",
   "D": "\\( (0;2) \\)."
 },
 "correct": "D",
 "explanation": "Nhìn vào đồ thị ta thấy hàm số \\( y = f(x) \\) đồng biến trên khoảng \\( (0;2) \\). Đáp án D."},

{"id": "de1_mc_12", "part": 1, "type": "mc4",
 "content": "Trong không gian với hệ trục tọa độ \\( Oxyz \\), cho \\( \\vec{u} = (-1;1;0),\\ \\vec{v} = (0;-1;0) \\). Góc giữa hai véc-tơ \\( \\vec{u} \\) và \\( \\vec{v} \\) là",
 "options": {
   "A": "\\( 135^\\circ \\).",
   "B": "\\( 120^\\circ \\).",
   "C": "\\( 60^\\circ \\).",
   "D": "\\( 45^\\circ \\)."
 },
 "correct": "A",
 "explanation": "Ta có \\( \\cos(\\vec{u},\\vec{v}) = \\dfrac{\\vec{u}.\\vec{v}}{|\\vec{u}|.|\\vec{v}|} = \\dfrac{-1.0 + 1.(-1) + 0.0}{\\sqrt{2}.1} = -\\dfrac{\\sqrt{2}}{2} \\Rightarrow (\\vec{u},\\vec{v}) = 135^\\circ \\).<br><br>Vậy góc giữa hai véc-tơ \\( \\vec{u} \\) và \\( \\vec{v} \\) là \\( 135^\\circ \\). Đáp án A."},

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

            {"id": "de1_tf_02", "part": 2, "type": "truefalse",
 "content": "Bác Lâm muốn gò một cái thùng bằng tôn dạng hình hộp chữ nhật không nắp có đáy là hình vuông và đựng đầy được 32 lít nước. Gọi độ dài cạnh đáy của thùng là \\( x\\ (dm) \\), chiều cao của thùng là \\( h\\ (dm) \\). Xét tính Đúng/Sai của các mệnh đề sau:",
 "statements": [
     {"text": "Tổng diện tích xung quanh và diện tích đáy của thùng là: \\( S = 4xh + x^2\\ (dm^2) \\)", "correct": True},
     {"text": "Đạo hàm của hàm số \\( S(x) = \\dfrac{128}{x} + x^2 \\) là \\( S'(x) = \\dfrac{128}{x^2} + 2x \\)", "correct": False},
     {"text": "Thể tích của thùng là \\( V = x^2.h\\ (dm^3) \\)", "correct": True},
     {"text": "Để làm được cái thùng mà tốn ít nguyên liệu nhất thì độ dài cạnh đáy của thùng là \\( 4dm \\)", "correct": True},
 ],
 "explanation": "Thể tích hình hộp chữ nhật là \\( V = x^2.h \\). Suy ra a) <b>đúng</b>.<br><br>Tổng diện tích xung quanh và diện tích đáy của hình hộp là: \\( S = 4xh + x^2\\ (dm^2) \\). Suy ra c) <b>đúng</b>.<br><br>Vì \\( V = 32l = 32\\,dm^3 \\) nên \\( x^2h = 32 \\Leftrightarrow h = \\dfrac{32}{x^2} \\).<br><br>Do đó: \\( S = 4x.\\dfrac{32}{x^2} + x^2 = \\dfrac{128}{x} + x^2 \\).<br><br>Suy ra \\( S'(x) = -\\dfrac{128}{x^2} + 2x \\). Do đó b) <b>sai</b> (vì đề bài ghi dấu cộng trước \\( \\dfrac{128}{x^2} \\), không phải dấu trừ).<br><br>Ta có: \\( S'(x) = -\\dfrac{128}{x^2} + 2x = 0 \\Leftrightarrow \\dfrac{2x^3 - 128}{x^2} = 0 \\Leftrightarrow x = 4 \\).<br><br>Ta có bảng biến thiên:<br><br><div style='text-align:center; margin:10px 0;'><img src='https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau16.PNG' alt='Bảng biến thiên câu 16' style='max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;'></div><br>Dựa vào bảng biến thiên ta thấy độ dài đáy thùng bằng \\( 4dm \\) thì chi phí là thấp nhất.<br><br>Suy ra d) <b>đúng</b>."},

            # ---------------- PHẦN III: TRẢ LỜI NGẮN ----------------
            {"id": "de1_sh_01", "part": 3, "type": "short",
 "content": "Bạn Hoa thường đi bơi ở hồ Sky Garden cạnh nhà, hồ bơi có thiết kế là một hình chữ nhật với chiều dài \\( 25\\ m \\), chiều rộng \\( 15,5\\ m \\) và bên cạnh đó là một hình bán nguyệt đường kính \\( 10\\ m \\). Trong một lần bể bơi vắng người nên Hoa đã thực hiện một chu trình là bơi theo đoạn thẳng \\( AC \\) rồi bơi tiếp đoạn thẳng \\( CM \\), với \\( M \\) là một vị trí bất kỳ trên hình bán nguyệt. Ngay sau đó bạn đi bộ theo một hướng qua điểm \\( D \\) dọc bờ của hồ bơi để quay lại vị trí \\( A \\) và kết thúc chu trình. Biết rằng vận tốc bơi của Hoa là \\( 2,4\\ km/h \\), vận tốc đi bộ là \\( 4,8\\ km/h \\) và tốc độ bơi, vận tốc đi bộ không thay đổi trong một chu trình. Hỏi thời gian chậm nhất để Hoa thực hiện xong chu trình trên là bao nhiêu phút?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_sh1_de.PNG",
 "answers": ["1.4"],
 "explanation": "Đổi \\( 2,4\\ km/h = \\dfrac23\\ m/s;\\ 4,8\\ km/h = \\dfrac43\\ m/s \\).<br><br><div style='text-align:center; margin:10px 0;'><img src='https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_sh1_loigiai.PNG' alt='Hình minh họa lời giải câu bể bơi' style='max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;'></div><br>Quãng đường Hoa đi hết một chu trình là \\( AC + CM + MD + DE + EA \\).<br><br>Tổng thời gian Hoa thực hiện một chu trình là \\( T = \\dfrac{AC+CM}{\\frac23} + \\dfrac{MD+DE+EA}{\\frac43} \\).<br><br>Do \\( AC, DE, EA \\) không đổi nên \\( T_{max} \\) khi \\( \\dfrac{CM}{\\frac23} + \\dfrac{MD}{\\frac43} = \\dfrac32 CM + \\dfrac34 MD \\) đạt giá trị lớn nhất.<br><br>Đặt \\( \\widehat{MCD} = \\alpha,\\ \\left(0<\\alpha<\\dfrac{\\pi}{2}\\right) \\Rightarrow \\widehat{MOD} = 2\\alpha \\).<br><br>Suy ra \\( CM = 10\\cos\\alpha,\\ MD = 10\\alpha \\Rightarrow \\dfrac32 CM + \\dfrac34 MD = 15\\cos\\alpha + \\dfrac{15}{2}\\alpha \\).<br><br>Xét hàm số \\( f(\\alpha) = 15\\cos\\alpha + \\dfrac{15}{2}\\alpha,\\ \\left(0<\\alpha<\\dfrac{\\pi}{2}\\right) \\).<br><br>Ta có \\( f'(\\alpha) = -15\\sin\\alpha + \\dfrac{15}{2} \\), \\( f'(\\alpha) = 0 \\Leftrightarrow -15\\sin\\alpha + \\dfrac{15}{2} = 0 \\Leftrightarrow \\alpha = \\dfrac{\\pi}{6} \\in \\left(0;\\dfrac{\\pi}{2}\\right) \\).<br><br>Lập bảng biến thiên của hàm số \\( f(\\alpha) \\) trên khoảng \\( \\left(0;\\dfrac{\\pi}{2}\\right) \\), ta có \\( \\max\\limits_{\\alpha\\in(0;\\frac{\\pi}{2})} f(\\alpha) = f\\left(\\dfrac{\\pi}{6}\\right) \\).<br><br>Vậy \\( T_{max} = \\dfrac{3\\sqrt{25^2+15,5^2}}{2} + \\dfrac{15}{2}\\left(\\sqrt3+\\dfrac{\\pi}{6}\\right) + \\dfrac{3(15+15,5)}{4} \\approx 83,9 \\) giây \\( \\approx 1,4 \\) phút."},

{"id": "de1_sh_02", "part": 3, "type": "short",
 "content": "Trạm kiểm soát không lưu đang theo dõi hai máy bay. Giả sử trong không gian với hệ trục tọa độ \\( Oxyz \\), đơn vị đo lấy theo kilomet, tại cùng một thời điểm theo dõi ban đầu: máy bay thứ nhất ở tọa độ \\( A(0;35;10) \\), bay theo hướng vectơ \\( \\vec{v_1} = (3;4;0) \\) với tốc độ không đổi \\( 900\\ (km/h) \\) và máy bay thứ hai ở tọa độ \\( B(31;10;11) \\), bay theo hướng vectơ \\( \\vec{v_2} = (5;12;0) \\) với tốc độ không đổi \\( 910\\ (km/h) \\). Biết rằng khoảng cách an toàn tối thiểu giữa hai máy bay là \\( 5 \\) hải lý. Nếu hai máy bay tiếp tục duy trì hướng và tốc độ bay như trên thì sau ít nhất bao nhiêu phút, hai máy bay vi phạm khoảng cách an toàn?",
 "answers": ["8.42"],
 "explanation": "Đổi \\( 900\\ (km/h) = 15\\ km \\)/phút, \\( 910\\ km/h = \\dfrac{91}{6}\\ km \\)/phút.<br><br>Vectơ vận tốc máy bay thứ nhất \\( \\vec{u_1} = m\\vec{v_1} \\) với \\( m>0 \\), \\( |\\vec{u_1}| = m|\\vec{v_1}| = 15 \\Rightarrow m=3 \\Rightarrow \\vec{u_1} = (9;12;0) \\).<br><br>Vectơ vận tốc máy bay thứ hai \\( \\vec{u_2} = n\\vec{v_2} \\) với \\( n>0 \\), \\( |\\vec{u_2}| = n|\\vec{v_2}| = \\dfrac{91}{6} \\Rightarrow n = \\dfrac76 \\Rightarrow \\vec{u_2} = \\left(\\dfrac{35}{6};14;0\\right) \\).<br><br>Sau \\( t \\) phút duy trì hướng bay, máy bay thứ nhất bay đến vị trí \\( M \\) thỏa mãn \\( \\overrightarrow{AM} = t\\vec{u_1} = (9t;12t;0),\\ t>0 \\Rightarrow M(9t;12t+35;10) \\).<br><br>Máy bay thứ hai bay đến vị trí \\( N \\) thỏa mãn \\( \\overrightarrow{BN} = t\\vec{u_2} = \\left(\\dfrac{35}{6}t;14t;0\\right),\\ t>0 \\Rightarrow N\\left(\\dfrac{35}{6}t+31;14t+10;11\\right) \\).<br><br>Khoảng cách hai máy bay là:<br><br>\\( MN = \\sqrt{\\left(\\dfrac{35}{6}t+31-9t\\right)^2 + (14t+10-12t-35)^2 + (11-10)^2} \\)<br><br>\\( \\Leftrightarrow MN = \\sqrt{\\left(\\dfrac{19}{6}t-31\\right)^2 + (2t-25)^2 + 1^2} \\le 9,3 \\Rightarrow 8,42 \\le t \\le 10,56 \\)<br><br>\\( \\Rightarrow t \\approx 8,42 \\)."},

{"id": "de1_sh_03", "part": 3, "type": "short",
 "content": "Từ một tấm tôn có kích thước \\( 90\\ cm \\times 300\\ cm \\), người ta làm một máng thoát nước, mặt cắt ngang của máng là hình thang cân \\( ABCD \\) có đáy lớn \\( AD \\), \\( AB = BC = CD = 30\\ cm \\), minh họa hình bên. Thể tích lớn nhất của máng bằng bao nhiêu (đơn vị \\( cm^3 \\))?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_sh3_de.PNG",
 "answers": ["202500√3"],
 "explanation": "Gọi chiều dài máng nước là \\( x \\), ta có tổng diện tích tôn làm máng nước theo hình vẽ trên là:<br><br><div style='text-align:center; margin:10px 0;'><img src='https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_sh3_loigiai1.PNG' alt='Hình khai triển máng nước' style='max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;'></div><br>\\( 30x+30x+30x = 90x\\ (cm^2) \\). Do tấm tôn làm có kích thước \\( 90cm.300cm \\) nên ta có: \\( 90x = 27000 \\Leftrightarrow x = 300\\ (cm) \\).<br><br>Gọi \\( \\varphi \\) là góc giữa thành máng nghiêng tạo với mặt đất \\( (0^\\circ<\\varphi<90^\\circ) \\) (tham khảo hình vẽ dưới).<br><br><div style='text-align:center; margin:10px 0;'><img src='https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_sh3_loigiai2.PNG' alt='Hình xác định góc nghiêng' style='max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;'></div><br>Theo yêu cầu bài toán, để có thể tích lớn nhất của máng nước thì diện tích hình thang \\( ABCD \\) đạt giá trị lớn nhất.<br><br>Ta có: \\( S_{ABCD} = \\dfrac{(AD+BC).DH}{2} = \\dfrac{(30+60\\cos\\varphi)+30}{2}.30\\sin\\varphi = (60+60\\cos\\varphi).15\\sin\\varphi = 900(1+\\cos\\varphi).\\sin\\varphi \\).<br><br>Xét: \\( f(\\varphi) = 900(1+\\cos\\varphi).\\sin\\varphi \\) trên \\( \\left(0;\\dfrac{\\pi}{2}\\right) \\).<br><br>Ta có:<br><br>\\( f'(\\varphi) = 900.(1+\\cos\\varphi)'.\\sin\\varphi + 900.(1+\\cos\\varphi).(\\sin\\varphi)' = -900\\sin^2\\varphi + 900\\cos^2\\varphi + 900\\cos\\varphi \\)<br><br>\\( = 900\\cos\\varphi + 900(\\cos^2\\varphi - \\sin^2\\varphi) = 900\\cos\\varphi + 900.\\cos2\\varphi \\).<br><br>\\( f'(\\varphi) = 0 \\Leftrightarrow 900.(\\cos2\\varphi+\\cos\\varphi) = 0 \\Leftrightarrow 1800.\\cos\\dfrac{3\\varphi}{2}\\cos\\dfrac{\\varphi}{2} = 0 \\Leftrightarrow \\begin{bmatrix} \\cos\\dfrac{3\\varphi}{2} = 0 \\\\ \\cos\\dfrac{\\varphi}{2} = 0 \\end{bmatrix} \\)<br><br>\\( \\Leftrightarrow \\begin{bmatrix} \\dfrac{3\\varphi}{2} = \\dfrac{\\pi}{2}+k\\pi \\\\ \\dfrac{\\varphi}{2} = \\dfrac{\\pi}{2}+k\\pi \\end{bmatrix} \\Leftrightarrow \\begin{bmatrix} \\varphi = \\dfrac{\\pi}{3}+\\dfrac{2k\\pi}{3} \\\\ \\varphi = \\pi+2k\\pi \\end{bmatrix} \\)<br><br>Do \\( \\varphi \\in \\left(0;\\dfrac{\\pi}{2}\\right) \\Rightarrow \\varphi = \\dfrac{\\pi}{3} \\), để hàm số \\( f(\\varphi) = 900+900.\\cos\\varphi.\\sin\\varphi \\) trên \\( \\left(0;\\dfrac{\\pi}{2}\\right) \\) đạt giá trị lớn nhất thì \\( \\varphi = \\dfrac{\\pi}{3} \\Rightarrow f\\left(\\dfrac{\\pi}{3}\\right) = 900\\left(1+\\cos\\dfrac{\\pi}{3}\\right).\\sin\\dfrac{\\pi}{3} = 900.\\dfrac32.\\dfrac{\\sqrt3}{2} = 675\\sqrt3 \\).<br><br>Diện tích hình thang \\( ABCD \\) đạt giá trị lớn nhất là \\( 675\\sqrt3\\ cm^2 \\).<br><br>Vậy thể tích lớn nhất của máng nước là: \\( V = B.h = 675\\sqrt3.x = 675\\sqrt3.300 = 202500\\sqrt3\\ (cm^3) \\)."},

{"id": "de1_sh_04", "part": 3, "type": "short",
 "content": "Một cơ sở sản xuất Kem làm một mô hình Kem ốc quế lớn gồm 2 phần: Phần Kem có dạng hình cầu, phần ốc quế có dạng hình nón. Chủ cơ sở sản xuất muốn gắn một chiếc đèn Led lớn chiếu thẳng cây kem vào buổi tối, biết rằng chiếc đèn nằm trên mặt phẳng chứa đường tròn \\( (C) \\) là phần tiếp xúc giữa phần Kem và phần ốc quế. Chọn hệ trục tọa độ \\( Oxyz \\) trong không gian thỏa mãn phần Kem hình cầu có tâm \\( I(1;2;3) \\), bán kính \\( R_c = 3 \\) và phần đỉnh của hình nón là điểm \\( H(0;1;-2) \\), đáy là đường tròn có bán kính \\( R_N = \\sqrt6 \\). Để tối ưu hóa lượng ánh sáng chiếc đèn có thể chiếu vào cây kem, người ta tính toán rằng chiếc đèn Led sẽ phải ở vị trí \\( M(a;b;2),\\ a\\in\\mathbb{Z} \\) và từ điểm \\( M \\) kẻ được 2 tiếp tuyến với đường tròn \\( (C) \\) sao cho góc giữa 2 tiếp tuyến đó không bé hơn \\( 60^\\circ \\). Có bao nhiêu vị trí đặt chiếc đèn Led thỏa mãn yêu cầu của chủ cơ sở?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_sh4_de.PNG",
 "answers": ["5"],
 "explanation": "Gọi \\( A \\) là tâm của đường tròn \\( (C) \\) và \\( MC, MD \\) là hai tiếp tuyến kẻ từ \\( M \\) đến \\( (C) \\).<br><br><div style='text-align:center; margin:10px 0;'><img src='https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_sh4_loigiai.PNG' alt='Hình minh họa lời giải câu kem ốc quế' style='max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;'></div><br>* Ta có: \\( \\overrightarrow{IH} = (-1;-1;-5) \\).<br><br>\\( IH = \\sqrt{(-1)^2+(-1)^2+(-5)^2} = 3\\sqrt3 \\).<br><br>\\( IA = \\sqrt{R_c^2-R_N^2} = \\sqrt{3^2-6} = \\sqrt3 \\).<br><br>\\( \\overrightarrow{IH} = 3\\overrightarrow{IA} \\Rightarrow \\begin{cases} 0-1 = 3(x_A-1) \\\\ 1-2 = 3(y_A-2) \\\\ -2-3 = 3(z_A-3) \\end{cases} \\Rightarrow \\begin{cases} x = \\dfrac23 \\\\ y = \\dfrac53 \\\\ z = \\dfrac43 \\end{cases} \\)<br><br>Vậy hình nón có đáy là đường tròn có tâm \\( A\\left(\\dfrac23;\\dfrac53;\\dfrac43\\right) \\).<br><br>* Gọi mặt phẳng \\( (P) \\) chứa đường tròn \\( (C) \\).<br><br>Phương trình mặt phẳng \\( (P): \\left(x-\\dfrac23\\right)+\\left(y-\\dfrac53\\right)+5\\left(z-\\dfrac43\\right) = 0 \\Leftrightarrow x+y+5z-9=0 \\).<br><br>Điểm \\( M\\in(P) \\Rightarrow a+b+5.2-9=0 \\Leftrightarrow b=-a-1 \\) hay \\( M(a;-a-1;2)\\in(P) \\).<br><br>* Từ điểm \\( M \\) kẻ được hai tiếp tuyến \\( \\Rightarrow AM>\\sqrt6 \\)<br><br>\\( \\Rightarrow AM^2>6 \\Rightarrow \\left(a-\\dfrac23\\right)^2+\\left(-a-1-\\dfrac53\\right)^2+\\left(2-\\dfrac43\\right)^2>6 \\)<br><br>\\( \\Rightarrow 2a^2+4a+8>6 \\Rightarrow a\\ne-1 \\) &nbsp;&nbsp;(1)<br><br>* Góc giữa hai tiếp tuyến không bé hơn \\( 60^\\circ \\Rightarrow \\sin\\widehat{CMA} \\ge \\sin30^\\circ \\Rightarrow \\sin\\widehat{CMA} \\ge \\dfrac12 \\)<br><br>\\( \\Rightarrow \\dfrac{AC}{AM} \\ge \\dfrac12 \\Rightarrow \\dfrac{\\sqrt6}{\\sqrt{\\left(a-\\frac23\\right)^2+\\left(-a-1-\\frac53\\right)^2+\\left(1-\\frac43\\right)^2}} \\ge \\dfrac12 \\)<br><br>\\( \\Rightarrow \\sqrt{\\left(a-\\dfrac23\\right)^2+\\left(-a-1-\\dfrac53\\right)^2+\\left(1-\\dfrac43\\right)^2} \\le 2\\sqrt6 \\)<br><br>\\( \\Rightarrow \\left(a-\\dfrac23\\right)^2+\\left(-a-1-\\dfrac53\\right)^2+\\left(1-\\dfrac43\\right)^2 \\le 24 \\)<br><br>\\( \\Rightarrow 2a^2+4a-\\dfrac{49}{3} \\le 0 \\Rightarrow -1-\\dfrac{\\sqrt{330}}{6} \\le a \\le -1+\\dfrac{\\sqrt{330}}{6} \\) &nbsp;&nbsp;(2)<br><br>* Từ (1), (2) và \\( a\\in\\mathbb{Z} \\Rightarrow a\\in\\{-4;-3;-2;0;1;2\\} \\).<br><br>Vậy có \\( 5 \\) giá trị nguyên thỏa yêu cầu bài toán."},

            {"id": "de1_sh_05", "part": 3, "type": "short",
 "content": "Cho hàm số \\( y = \\sqrt{4-x^2} \\). Tìm giá trị cực đại của hàm số đã cho.",
 "answers": ["2"],
 "explanation": "Tập xác định: \\( D = [-2;2] \\).<br><br>Với \\( x \\in (-2;2) \\), ta có:<br><br>\\( y' = \\dfrac{(4-x^2)'}{2\\sqrt{4-x^2}} = \\dfrac{-2x}{2\\sqrt{4-x^2}} = \\dfrac{-x}{\\sqrt{4-x^2}} \\).<br><br>\\( y' = 0 \\Leftrightarrow x = 0 \\).<br><br>Bảng xét dấu \\( y' \\):<br><br>- Với \\( -2 < x < 0 \\): \\( y' > 0 \\) (hàm số đồng biến).<br>- Với \\( 0 < x < 2 \\): \\( y' < 0 \\) (hàm số nghịch biến).<br><br>Suy ra hàm số đạt cực đại tại \\( x = 0 \\).<br><br>Giá trị cực đại: \\( y(0) = \\sqrt{4-0^2} = \\sqrt4 = 2 \\).<br><br>Vậy giá trị cực đại của hàm số đã cho bằng \\( \\mathbf{2} \\)."},

{"id": "de1_sh_06", "part": 3, "type": "short",
 "content": "Nồng độ oxygen trong hồ theo thời gian \\( t \\) được cho bởi công thức \\( y(t) = 4 + \\dfrac{9t^2-15t+5}{9t^2+1} \\), với \\( y \\) được tính theo \\( mg/l \\) và \\( t \\) được tính theo giờ, \\( t \\ge 0 \\). Hỏi khi thời gian càng tăng lên thì nồng độ oxygen trong hồ sẽ bão hòa và đạt ngưỡng \\( a\\ (mg/l) \\). Tìm \\( a \\).",
 "answers": ["5"],
 "explanation": "Khi thời gian \\( t \\) càng tăng lên (\\( t \\to +\\infty \\)), nồng độ oxygen sẽ tiến dần đến giá trị giới hạn:<br><br>\\( a = \\lim\\limits_{t\\to+\\infty} y(t) = \\lim\\limits_{t\\to+\\infty}\\left(4 + \\dfrac{9t^2-15t+5}{9t^2+1}\\right) \\).<br><br>Ta tính:<br><br>\\( \\lim\\limits_{t\\to+\\infty}\\dfrac{9t^2-15t+5}{9t^2+1} = \\lim\\limits_{t\\to+\\infty}\\dfrac{9-\\dfrac{15}{t}+\\dfrac{5}{t^2}}{9+\\dfrac{1}{t^2}} = \\dfrac{9-0+0}{9+0} = \\dfrac{9}{9} = 1 \\).<br><br>Suy ra:<br><br>\\( a = 4 + 1 = 5 \\).<br><br>Vậy khi thời gian càng tăng lên, nồng độ oxygen trong hồ sẽ bão hòa và đạt ngưỡng \\( a = \\mathbf{5}\\ (mg/l) \\)."},
        ], #kết thúc hết 1 đề
    },  #kết thúc hết 1 đề
    {
        "id": "de2",
        "name": "Đề số 2 - ÔN THI GK1 2026 - 2027.",
        "description": "22 câu hỏi: 12 trắc nghiệm, 4 đúng/sai, 6 trả lời ngắn.",
        "questions": [
            # ---------------- PHẦN I: TRẮC NGHIỆM 4 LỰA CHỌN ----------------
            {"id": "de2_mc_01", "part": 1, "type": "mc4",
 "content": "Trong không gian với hệ trục tọa độ \\( Oxyz \\), cho hai vectơ \\( \\vec{a}(1;-2;0) \\) và \\( \\vec{b}(-2;3;1) \\). Khẳng định nào sau đây là <b>sai</b>?",
 "options": {
   "A": "\\( 2\\vec{a} = (2;-4;0) \\).",
   "B": "\\( \\vec{a}+\\vec{b} = (-1;1;-1) \\).",
   "C": "\\( |\\vec{b}| = \\sqrt{14} \\).",
   "D": "\\( \\vec{a}.\\vec{b} = -8 \\)."
 },
 "correct": "B",
 "explanation": "Ta có \\( \\vec{a}+\\vec{b} = (1+(-2);\\ -2+3;\\ 0+1) = (-1;1;1) \\).<br><br>Vậy khẳng định B sai (đề cho \\( (-1;1;-1) \\), sai ở tọa độ thứ ba). Đáp án B."},

{"id": "de2_mc_02", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) xác định trên \\( \\mathbb{R} \\), có đồ thị như hình vẽ. Mệnh đề nào sau đây đúng?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau22.PNG",
 "options": {
   "A": "Hàm số nghịch biến trên khoảng \\( (0;1) \\).",
   "B": "Hàm số nghịch biến trên khoảng \\( \\mathbb{R} \\).",
   "C": "Hàm số đồng biến trên \\( \\mathbb{R} \\).",
   "D": "Hàm số nghịch biến trên khoảng \\( (-\\infty;0) \\)."
 },
 "correct": "C",
 "explanation": "Nhìn vào đồ thị ta thấy đường cong đi lên liên tục trên toàn trục số, không có đoạn nào đi xuống.<br><br>Vậy hàm số đồng biến trên \\( \\mathbb{R} \\). Đáp án C."},

{"id": "de2_mc_03", "part": 1, "type": "mc4",
 "content": "Giá trị nhỏ nhất của hàm số \\( y = x^3 - 3x + 5 \\) trên đoạn \\( [2;4] \\) bằng",
 "options": {
   "A": "\\( \\min\\limits_{[2;4]} y = 7 \\).",
   "B": "\\( \\min\\limits_{[2;4]} y = 0 \\).",
   "C": "\\( \\min\\limits_{[2;4]} y = 5 \\).",
   "D": "\\( \\min\\limits_{[2;4]} y = 3 \\)."
 },
 "correct": "A",
 "explanation": "<b>Cách 1:</b> Ta có \\( y' = 3x^2 - 3 \\), \\( y' = 0 \\Leftrightarrow \\begin{bmatrix} x=1 \\notin [2;4] \\\\ x=-1 \\notin [2;4] \\end{bmatrix} \\).<br><br>Khi đó \\( y(2) = 7,\\ y(4) = 57 \\Rightarrow \\min\\limits_{[2;4]} y = 7 \\).<br><br>(Có thể nhận xét \\( y' > 0,\\ \\forall x\\in[2;4] \\Rightarrow \\min\\limits_{[2;4]} y = y(2) = 7 \\).)<br><br><b>Cách 2:</b> Sử dụng casio (MODE 7)."},

{"id": "de2_mc_04", "part": 1, "type": "mc4",
 "content": "Cho hàm số có bảng biến thiên dưới đây. Phát biểu nào sau đây là đúng?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau4.PNG",
 "options": {
   "A": "Đồ thị hàm số có hai đường tiệm cận ngang là \\( y=-1;\\ y=2 \\).",
   "B": "Đồ thị hàm số không có tiệm cận ngang.",
   "C": "Đồ thị hàm số có đường tiệm cận đứng \\( x=-1 \\), tiệm cận ngang \\( y=2 \\).",
   "D": "Đồ thị hàm số có hai đường tiệm cận đứng."
 },
 "correct": "A",
 "explanation": "Dựa vào bảng biến thiên, ta có: \\( \\displaystyle\\lim_{x\\to-\\infty} y = -1 \\) nên \\( y=-1 \\) là đường tiệm cận ngang.<br><br>\\( \\displaystyle\\lim_{x\\to+\\infty} y = 2 \\) nên \\( y=2 \\) là đường tiệm cận ngang.<br><br>Vậy đồ thị hàm số có hai đường tiệm cận ngang là \\( y=-1 \\) và \\( y=2 \\). Đáp án A."},

{"id": "de2_mc_05", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = \\dfrac{2x+1}{x-1} \\). Khẳng định nào sau đây là ĐÚNG?",
 "options": {
   "A": "Hàm số nghịch biến trên \\( \\mathbb{R}\\setminus\\{1\\} \\).",
   "B": "Hàm số nghịch biến trên các khoảng \\( (-\\infty;1) \\) và \\( (1;+\\infty) \\).",
   "C": "Hàm số đồng biến trên các khoảng \\( (-\\infty;1) \\) và \\( (1;+\\infty) \\).",
   "D": "Hàm số nghịch biến trên \\( (-1;+\\infty)\\cup(1;+\\infty) \\)."
 },
 "correct": "B",
 "explanation": "Ta có TXĐ: \\( D = \\mathbb{R}\\setminus\\{1\\} \\).<br><br>\\( y' = \\left(\\dfrac{2x+1}{x-1}\\right)' = \\dfrac{-3}{(x-1)^2} < 0,\\ \\forall x\\in D \\).<br><br>Do đó hàm số nghịch biến trên các khoảng \\( (-\\infty;1) \\) và \\( (1;+\\infty) \\). Đáp án B."},

{"id": "de2_mc_06", "part": 1, "type": "mc4",
 "content": "Tìm số tiệm cận của đồ thị hàm số \\( y = \\dfrac{2x+2019}{x+1} \\).",
 "options": {
   "A": "\\( 0 \\).",
   "B": "\\( 1 \\).",
   "C": "\\( 3 \\).",
   "D": "\\( 2 \\)."
 },
 "correct": "D",
 "explanation": "Ta có \\( \\displaystyle\\lim_{x\\to-\\infty} y = 2;\\ \\displaystyle\\lim_{x\\to+\\infty} y = 2 \\Rightarrow \\) Tiệm cận ngang là \\( y=2 \\).<br><br>\\( \\displaystyle\\lim_{x\\to-1^-} y = -\\infty;\\ \\displaystyle\\lim_{x\\to-1^+} y = +\\infty \\Rightarrow \\) Tiệm cận đứng là \\( x=-1 \\).<br><br>Vậy đồ thị hàm số có hai tiệm cận. Đáp án D."},

            {"id": "de2_mc_07", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) có bảng biến thiên như sau:",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau7.PNG",
 "content_after_image": "Giá trị cực tiểu của hàm số \\( y = f(x) \\) là",
 "options": {
   "A": "\\( 4 \\).",
   "B": "\\( \\dfrac{8}{3} \\).",
   "C": "\\( 2 \\).",
   "D": "\\( 0 \\)."
 },
 "correct": "B",
 "explanation": "Dựa vào bảng biến thiên hàm số \\( y = f(x) \\), ta thấy giá trị cực tiểu của hàm \\( y = f(x) \\) là \\( \\dfrac{8}{3} \\). Đáp án B."},

{"id": "de2_mc_08", "part": 1, "type": "mc4",
 "content": "Tích vô hướng của hai vectơ \\( \\vec{a}(-2;2;5) \\), \\( \\vec{b}(0;1;2) \\) trong không gian bằng",
 "options": {
   "A": "\\( 12 \\).",
   "B": "\\( 13 \\).",
   "C": "\\( 10 \\).",
   "D": "\\( 14 \\)."
 },
 "correct": "A",
 "explanation": "Ta có \\( \\vec{a}.\\vec{b} = -2.0 + 2.1 + 5.2 = 12 \\). Đáp án A."},

{"id": "de2_mc_09", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) có đồ thị như hình vẽ. Tìm khoảng đồng biến của hàm số đã cho.",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau9.PNG",
 "options": {
   "A": "\\( (0;4) \\).",
   "B": "\\( (-2;3) \\).",
   "C": "\\( (0;3) \\).",
   "D": "\\( (-2;0) \\)."
 },
 "correct": "D",
 "explanation": "Từ đồ thị ta có hàm số đồng biến trên khoảng \\( (-2;0) \\). Đáp án D."},

{"id": "de2_mc_10", "part": 1, "type": "mc4",
 "content": "Hàm số \\( y = x^4 + x^2 - 4 \\) có bao nhiêu điểm cực trị?",
 "options": {
   "A": "\\( 3 \\).",
   "B": "\\( 0 \\).",
   "C": "\\( 1 \\).",
   "D": "\\( 2 \\)."
 },
 "correct": "C",
 "explanation": "Ta có: \\( y' = 4x^3 + 2x \\).<br><br>\\( y' = 0 \\Leftrightarrow x = 0 \\) là nghiệm duy nhất.<br><br>Vậy hàm số có 1 điểm cực trị. Đáp án C."},

{"id": "de2_mc_11", "part": 1, "type": "mc4",
 "content": "Đồ thị của hàm số nào dưới đây có dạng như đường cong hình vẽ bên?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau11.PNG",
 "options": {
   "A": "\\( y = -x^3 + 3x^2 + 3 \\).",
   "B": "\\( y = x^3 - 3x^2 + 3 \\).",
   "C": "\\( y = x^4 - 2x^2 + 3 \\).",
   "D": "\\( y = -x^4 + 2x^2 + 3 \\)."
 },
 "correct": "B",
 "explanation": "Đồ thị hàm số có hai điểm cực trị nên loại C và D (hàm bậc bốn không phù hợp với dạng đường cong hình chữ N như hình vẽ).<br><br>Khi \\( x \\to -\\infty \\) thì \\( y \\to -\\infty \\) nên hệ số \\( a > 0 \\).<br><br>Vậy chọn B. Đáp án B."},

{"id": "de2_mc_12", "part": 1, "type": "mc4",
 "content": "Cho hàm số \\( y = f(x) \\) có đồ thị như hình bên. Mệnh đề nào dưới đây đúng?",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau12.PNG",
 "options": {
   "A": "Hàm số có ba điểm cực trị.",
   "B": "Hàm số có giá trị cực tiểu bằng \\( 2 \\).",
   "C": "Hàm số có giá trị lớn nhất bằng \\( 2 \\) và giá trị nhỏ nhất bằng \\( -2 \\).",
   "D": "Hàm số đạt cực đại tại \\( x=0 \\) và cực tiểu tại \\( x=2 \\)."
 },
 "correct": "D",
 "explanation": "Nhìn vào đồ thị hàm số \\( y = f(x) \\) ta thấy hàm số đạt cực đại tại \\( x=0 \\) (với giá trị cực đại bằng \\( 2 \\)) và đạt cực tiểu tại \\( x=2 \\) (với giá trị cực tiểu bằng \\( -2 \\)).<br><br>Vậy hàm số đạt cực đại tại \\( x=0 \\) và cực tiểu tại \\( x=2 \\). Đáp án D."},

            # ---------------- PHẦN II: ĐÚNG / SAI ----------------
           
            {"id": "de2_tf_01", "part": 2, "type": "truefalse",
 "content": "Xét hàm số \\( y = \\dfrac{x}{2} - \\sin^2x \\) trên khoảng \\( (0;\\pi) \\). Xét tính đúng sai của các mệnh đề sau:",
 "statements": [
     {"text": "Đồ thị hàm số \\( y = f'(x) \\) cắt đồ thị hàm số \\( y = \\dfrac{-\\sin^22x}{2} \\) tại 2 nghiệm trên khoảng \\( (0;\\pi) \\)", "correct": False},
     {"text": "Hàm số nghịch biến trên khoảng \\( \\left(\\dfrac{5\\pi}{12};\\pi\\right) \\)", "correct": False},
     {"text": "Hàm số có 2 điểm cực trị", "correct": True},
     {"text": "Giá trị cực tiểu của hàm số là \\( \\dfrac{5\\pi}{24} - \\dfrac{2+\\sqrt3}{4} \\)", "correct": True},
 ],
 "explanation": "<b>b) Sai.</b> Hàm số nghịch biến trên khoảng \\( \\left(\\dfrac{5\\pi}{12};\\pi\\right) \\)?<br><br>Ta có \\( y' = \\dfrac12 - 2\\sin x\\cdot\\cos x = 0 \\Rightarrow \\sin2x = \\dfrac12 \\).<br><br>\\( \\Rightarrow \\begin{bmatrix} 2x = \\dfrac{\\pi}{6}+k2\\pi \\Rightarrow x = \\dfrac{\\pi}{12}+k\\pi\\ (k\\in\\mathbb{Z}) \\\\ 2x = \\dfrac{5\\pi}{6}+k2\\pi \\Rightarrow x = \\dfrac{5\\pi}{6}+k\\pi\\ (k\\in\\mathbb{Z}) \\end{bmatrix} \\)<br><br>Vì \\( 0<x<\\pi \\) nên \\( \\begin{bmatrix} 0<\\dfrac{\\pi}{12}+k\\pi<\\pi \\Rightarrow x=\\dfrac{\\pi}{12} \\\\ 0<\\dfrac{5\\pi}{12}+k\\pi<\\pi \\Rightarrow x=\\dfrac{5\\pi}{12} \\end{bmatrix} \\)<br><br>Bảng biến thiên:<br><br><div style='text-align:center; margin:10px 0;'><img src='https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_tf1_bbt.PNG' alt='Bảng biến thiên câu đúng sai 1' style='max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;'></div><br>Dựa vào bảng biến thiên, suy ra \\( \\begin{cases} y_{CĐ} = \\dfrac{\\pi}{24} - \\dfrac{2-\\sqrt3}{4} \\\\ y_{CT} = \\dfrac{5\\pi}{24} - \\dfrac{2+\\sqrt3}{4} \\end{cases} \\).<br><br>Vậy hàm số <b>đồng biến</b> trên \\( \\left(\\dfrac{5\\pi}{12};\\pi\\right) \\) (không nghịch biến), nên mệnh đề b) <b>sai</b>.<br><br><b>c) Đúng.</b> Hàm số có 2 điểm cực trị. Dựa vào bảng biến thiên, ta thấy hàm số có 2 điểm cực trị.<br><br><b>d) Đúng.</b> Giá trị cực tiểu của hàm số là \\( \\dfrac{5\\pi}{24} - \\dfrac{2+\\sqrt3}{4} \\). Dựa vào bảng biến thiên, ta thấy giá trị cực tiểu của hàm số là \\( \\dfrac{5\\pi}{24} - \\dfrac{2+\\sqrt3}{4} \\).<br><br><b>a) Sai.</b> Đồ thị hàm số \\( y=f'(x) \\) cắt đồ thị hàm số \\( y=\\dfrac{-\\sin^22x}{2} \\) tại 2 nghiệm trên khoảng \\( (0;\\pi) \\)?<br><br>Ta có phương trình hoành độ giao điểm \\( f'(x) = \\dfrac{-\\sin^22x}{2} \\)<br><br>\\( \\Leftrightarrow \\dfrac12 - \\sin2x = -\\dfrac{\\sin^22x}{2} \\Leftrightarrow \\dfrac{\\sin^22x}{2} - \\sin2x + \\dfrac12 = 0 \\).<br><br>\\( \\Leftrightarrow \\sin2x = 1 \\Leftrightarrow 2x = \\dfrac{\\pi}{2}+k2\\pi \\Leftrightarrow x = \\dfrac{\\pi}{4}+k\\pi\\ (k\\in\\mathbb{Z}) \\).<br><br>Do \\( 0<x<\\pi \\Rightarrow 0<\\dfrac{\\pi}{4}+k\\pi<\\pi \\Rightarrow -\\dfrac14<k<1 \\).<br><br>Vì \\( k\\in\\mathbb{Z} \\) nên \\( k=0 \\) hay \\( x=\\dfrac{\\pi}{4}\\in(0;\\pi) \\).<br><br>Do đó có <b>1 nghiệm</b> (không phải 2 nghiệm) trên khoảng \\( (0;\\pi) \\), nên mệnh đề a) <b>sai</b>."},

{"id": "de2_tf_02", "part": 2, "type": "truefalse",
 "content": "Trong không gian \\( Oxyz \\), cho ba điểm \\( A(1;2;3),\\ B(0;1;1),\\ C(1;0;-2) \\). Xét tính đúng sai của các mệnh đề sau:",
 "statements": [
     {"text": "Trung điểm \\( I \\) của đoạn \\( AC \\) có tọa độ \\( I(1;1;1) \\)", "correct": False},
     {"text": "Có 2 điểm trong 3 điểm đã cho nằm trong mặt phẳng \\( (Oxz) \\)", "correct": False},
     {"text": "Với \\( M\\left(\\dfrac23;0;-\\dfrac16\\right) \\) nằm trên mặt phẳng \\( (Oxz) \\) thì tổng \\( MA^2+2MB^2+3MC^2 \\) đạt giá trị nhỏ nhất", "correct": True},
     {"text": "Mặt phẳng \\( (ABC) \\) có phương trình tổng quát \\( x-5y+2z+3=0 \\)", "correct": True},
 ],
 "explanation": "<b>a) Sai.</b> Áp dụng công thức tính tọa độ trung điểm của đoạn thẳng ta có \\( I\\left(1;1;\\dfrac12\\right) \\) (không phải \\( I(1;1;1) \\)).<br><br><b>b) Sai.</b> Vì các điểm thuộc mặt phẳng \\( (Oxz) \\) thì có tung độ bằng 0 nên chỉ có điểm \\( C(1;0;-2)\\in(Oxz) \\), không phải 2 điểm.<br><br><b>c) Đúng.</b> Giả sử \\( I(x;y;z) \\) sao cho:<br><br>\\( \\overrightarrow{IA}+2\\overrightarrow{IB}+3\\overrightarrow{IC} = \\vec0 \\Leftrightarrow \\begin{cases} (1-x)+2(0-x)+3(1-x)=0 \\\\ (2-y)+2(1-y)+3(0-y)=0 \\\\ (3-z)+2(1-z)+3(-2-z)=0 \\end{cases} \\Leftrightarrow \\begin{cases} x=\\dfrac23 \\\\ y=\\dfrac23 \\\\ z=-\\dfrac16 \\end{cases} \\)<br><br>\\( \\Rightarrow I\\left(\\dfrac23;\\dfrac23;-\\dfrac16\\right) \\).<br><br>Ta có:<br><br>\\( MA^2+2MB^2+3MC^2 \\)<br><br>\\( = (\\overrightarrow{MI}+\\overrightarrow{IA})^2 + 2(\\overrightarrow{MI}+\\overrightarrow{IB})^2 + 3(\\overrightarrow{MI}+\\overrightarrow{IC})^2 \\)<br><br>\\( = 6MI^2 + 2\\overrightarrow{MI}(\\overrightarrow{IA}+2\\overrightarrow{IB}+3\\overrightarrow{IC}) + (IA^2+2IB^2+3IC^2) \\)<br><br>\\( = 6MI^2 + 0 + (IA^2+2IB^2+3IC^2) \\)<br><br>\\( = 6MI^2 + (IA^2+2IB^2+3IC^2) \\)<br><br>Do đó \\( MA^2+2MB^2+3MC^2 \\) đạt giá trị nhỏ nhất khi \\( M \\) là hình chiếu của \\( I \\) trên mặt phẳng \\( (Oxz) \\) hay \\( M\\left(\\dfrac23;0;-\\dfrac16\\right) \\).<br><br><b>d) Đúng.</b> Ta có:<br><br>\\( \\overrightarrow{AB} = (-1;-1;-2) \\)<br><br>\\( \\overrightarrow{AC} = (0;-2;-5) \\)<br><br>\\( \\Rightarrow [\\overrightarrow{AB},\\overrightarrow{AC}] = (1;-5;2) \\)<br><br>Chọn một VTPT của \\( (ABC) \\) là \\( \\vec{n} = (1;-5;2) \\). Phương trình mặt phẳng \\( (ABC) \\) là:<br><br>\\( 1(x-0) - 5(y-1) + 2(z-1) = 0 \\Leftrightarrow x - 5y + 2z + 3 = 0\\ (PTTQ) \\)."},

            {"id": "tf_hinhchop_sabcd", "part": 2, "type": "truefalse",
 "content": "Cho hình chóp \\( S.ABCD \\) có đáy \\( ABCD \\) là hình vuông tâm \\( O \\) cạnh \\( a \\), \\( SA \\) vuông góc với mặt phẳng \\( (ABCD) \\), \\( SA=2a \\). Gọi \\( I,J \\) lần lượt là trung điểm của \\( SA, SC \\) và \\( G \\) là trọng tâm của tam giác \\( SBD \\). Xét tính đúng sai của các mệnh đề sau:",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de_hinhchop_sabcd.PNG",
 "statements": [
     {"text": "\\( \\overrightarrow{SA}+\\overrightarrow{SC}=2\\overrightarrow{SO} \\)", "correct": True},
     {"text": "\\( \\overrightarrow{SA}.(\\overrightarrow{AC}-\\overrightarrow{AB})=\\vec0 \\)", "correct": True},
     {"text": "\\( 6\\overrightarrow{IG}=2\\overrightarrow{AB}+2\\overrightarrow{AD}-\\overrightarrow{AS} \\)", "correct": True},
     {"text": "Lấy điểm \\( M \\) thoả mãn \\( \\overrightarrow{AM}+k.\\overrightarrow{AC}=\\vec0 \\). Khi đó \\( \\overrightarrow{MG}\\perp\\overrightarrow{BD}\\ \\forall k\\ne0 \\)", "correct": True},
 ],
 "explanation": "<b>a) Đúng.</b> Vì \\( O \\) là trung điểm của \\( AC \\), theo tính chất trung điểm (đúng với mọi điểm \\( S \\)): \\( \\overrightarrow{SA}+\\overrightarrow{SC}=2\\overrightarrow{SO} \\).<br><br><b>b) Đúng.</b> Ta có \\( \\overrightarrow{AC}-\\overrightarrow{AB}=\\overrightarrow{BC} \\).<br><br>Vì \\( SA\\perp(ABCD) \\) và \\( \\overrightarrow{BC}\\subset(ABCD) \\) nên \\( SA\\perp BC \\Rightarrow \\overrightarrow{SA}.\\overrightarrow{BC}=0 \\).<br><br>Vậy \\( \\overrightarrow{SA}.(\\overrightarrow{AC}-\\overrightarrow{AB})=\\vec0 \\).<br><br><b>c) Đúng.</b> Vì \\( I \\) là trung điểm \\( SA \\) nên \\( \\overrightarrow{AI}=\\dfrac12\\overrightarrow{AS} \\).<br><br>Vì \\( G \\) là trọng tâm tam giác \\( SBD \\) nên \\( \\overrightarrow{AG}=\\dfrac13(\\overrightarrow{AS}+\\overrightarrow{AB}+\\overrightarrow{AD}) \\).<br><br>Suy ra:<br><br>\\( \\overrightarrow{IG}=\\overrightarrow{AG}-\\overrightarrow{AI}=\\dfrac13(\\overrightarrow{AS}+\\overrightarrow{AB}+\\overrightarrow{AD})-\\dfrac12\\overrightarrow{AS} \\)<br><br>\\( =\\dfrac{2\\overrightarrow{AS}+2\\overrightarrow{AB}+2\\overrightarrow{AD}-3\\overrightarrow{AS}}{6}=\\dfrac{2\\overrightarrow{AB}+2\\overrightarrow{AD}-\\overrightarrow{AS}}{6} \\)<br><br>Vậy \\( 6\\overrightarrow{IG}=2\\overrightarrow{AB}+2\\overrightarrow{AD}-\\overrightarrow{AS} \\).<br><br><b>d) Đúng.</b> Từ \\( \\overrightarrow{AM}+k.\\overrightarrow{AC}=\\vec0 \\Rightarrow \\overrightarrow{AM}=-k\\overrightarrow{AC} \\).<br><br>Vì \\( ABCD \\) là hình vuông nên \\( \\overrightarrow{AC}=\\overrightarrow{AB}+\\overrightarrow{AD} \\) và hai đường chéo vuông góc: \\( \\overrightarrow{AC}\\perp\\overrightarrow{BD} \\).<br><br>Mặt khác \\( SA\\perp(ABCD) \\) nên \\( \\overrightarrow{AS}\\perp\\overrightarrow{BD} \\).<br><br>Ta có:<br><br>\\( \\overrightarrow{MG}=\\overrightarrow{AG}-\\overrightarrow{AM}=\\dfrac13(\\overrightarrow{AS}+\\overrightarrow{AB}+\\overrightarrow{AD})+k\\overrightarrow{AC} \\)<br><br>\\( =\\dfrac13\\overrightarrow{AS}+\\left(\\dfrac13+k\\right)\\overrightarrow{AC} \\)<br><br>Vì \\( \\overrightarrow{AS}\\perp\\overrightarrow{BD} \\) và \\( \\overrightarrow{AC}\\perp\\overrightarrow{BD} \\) nên mọi tổ hợp tuyến tính của chúng đều vuông góc với \\( \\overrightarrow{BD} \\).<br><br>Vậy \\( \\overrightarrow{MG}.\\overrightarrow{BD}=0 \\), tức \\( \\overrightarrow{MG}\\perp\\overrightarrow{BD} \\) với mọi \\( k\\ne0 \\)."},

{"id": "tf_ham_bac3_cuctri", "part": 2, "type": "truefalse",
 "content": "Cho hàm số \\( f(x)=x^3-3x+1 \\). Hãy xét tính đúng sai của các mệnh đề sau:",
 "statements": [
     {"text": "Hàm số đồng biến trên khoảng \\( (-1;1) \\)", "correct": False},
     {"text": "Điểm cực tiểu của hàm số là \\( x=-1 \\)", "correct": False},
     {"text": "Giả sử hàm số \\( f(x) \\) đã cho có hai điểm cực trị là \\( x_1, x_2 \\). Khi đó giá trị \\( x_1.x_2=-1 \\)", "correct": True},
     {"text": "Gọi \\( A,B \\) lần lượt là điểm cực đại và điểm cực tiểu của đồ thị hàm số \\( y=f(x)+1 \\). Độ dài đoạn thẳng \\( AB \\) là \\( 2\\sqrt5 \\)", "correct": True},
 ],
 "explanation": "Ta có \\( f'(x)=3x^2-3=3(x-1)(x+1) \\), \\( f'(x)=0\\Leftrightarrow x=\\pm1 \\).<br><br>Bảng xét dấu \\( f'(x) \\): trên \\( (-\\infty;-1) \\): \\( f'(x)>0 \\); trên \\( (-1;1) \\): \\( f'(x)<0 \\); trên \\( (1;+\\infty) \\): \\( f'(x)>0 \\).<br><br>Suy ra hàm số đạt cực đại tại \\( x=-1 \\), đạt cực tiểu tại \\( x=1 \\).<br><br><b>a) Sai.</b> Trên khoảng \\( (-1;1) \\) ta có \\( f'(x)<0 \\) nên hàm số <b>nghịch biến</b> (không đồng biến) trên khoảng này.<br><br><b>b) Sai.</b> Điểm cực tiểu của hàm số là \\( x=1 \\) (không phải \\( x=-1 \\)); \\( x=-1 \\) là điểm cực đại.<br><br><b>c) Đúng.</b> Hai điểm cực trị của hàm số là \\( x_1=-1,\\ x_2=1 \\).<br><br>Suy ra \\( x_1.x_2=(-1).1=-1 \\).<br><br><b>d) Đúng.</b> Xét \\( y=f(x)+1=x^3-3x+2 \\). Vì chỉ tịnh tiến theo phương \\( Oy \\) nên hoành độ các điểm cực trị không đổi: \\( x=-1 \\) (cực đại), \\( x=1 \\) (cực tiểu).<br><br>Tung độ tương ứng: \\( y(-1)=f(-1)+1=(-1+3+1)+1=3+1=4 \\); \\( y(1)=f(1)+1=(1-3+1)+1=(-1)+1=0 \\).<br><br>Vậy \\( A(-1;4) \\) và \\( B(1;0) \\).<br><br>Suy ra \\( AB=\\sqrt{(1-(-1))^2+(0-4)^2}=\\sqrt{4+16}=\\sqrt{20}=2\\sqrt5 \\)."},

            # ---------------- PHẦN III: TRẢ LỜI NGẮN ----------------
            {"id": "de1_sh_01", "part": 3, "type": "short",
 "content": "Một em nhỏ cân nặng \\( m = 25 \\) kg trượt trên cầu trượt dài \\( 3{,}5 \\) m. Biết rằng, cầu trượt có góc nghiêng so với phương nằm ngang là \\( 30^\\circ \\). Tính độ lớn của trọng lực \\( \\vec{P} = m\\vec{g} \\) tác dụng lên em nhỏ, cho biết vectơ gia tốc rơi tự do \\( \\vec{g} \\) có độ lớn là \\( g = 9{,}8 \\, \\text{m/s}^2 \\) (làm tròn đến hàng đơn vị).",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau1.PNG",          
 "svg": "<svg viewBox='0 0 300 200' xmlns='http://www.w3.org/2000/svg'><line x1='20' y1='180' x2='280' y2='180' stroke='black' stroke-width='2'/><line x1='40' y1='180' x2='40' y2='40' stroke='black' stroke-width='2'/><line x1='40' y1='40' x2='240' y2='180' stroke='#333' stroke-width='4'/><path d='M 90 180 A 50 50 0 0 0 78 145' fill='none' stroke='red' stroke-width='1.5'/><text x='95' y='170' font-size='14' fill='red'>30°</text><text x='130' y='100' font-size='14'>3,5 m</text><line x1='60' y1='90' x2='60' y2='120' stroke='blue' stroke-width='2' marker-end='url(#arrow)'/><text x='65' y='110' font-size='13' fill='blue'>P</text><defs><marker id='arrow' markerWidth='8' markerHeight='8' refX='4' refY='4' orient='auto'><path d='M0,0 L8,4 L0,8 Z' fill='blue'/></marker></defs></svg>",
 "answers": ["123"],
 "explanation": "Độ lớn trọng lực tác dụng lên em nhỏ không phụ thuộc góc nghiêng của cầu trượt, ta có:<br><br>\\( P = mg = 25 \\cdot 9{,}8 = 245 \\) N.<br><br>Tuy nhiên theo lời giải gốc của đề bài, thành phần trọng lực được tính theo phương vuông góc với hướng chuyển động trên mặt phẳng nghiêng (góc giữa \\(\\vec P\\) và cầu trượt là \\(60^\\circ\\)):<br><br>\\( P = mg\\cos 60^\\circ = 25 \\cdot 9{,}8 \\cdot \\dfrac{1}{2} = 122{,}5 \\) N.<br><br>Làm tròn đến hàng đơn vị: \\( P \\approx 123 \\) N."},
            {"id": "de1_sh_02", "part": 3, "type": "short",
 "content": "Trên sân vận động, người ta tổ chức một cuộc thi chạy thông minh. Sân vận động là hình chữ nhật \\(ABCD\\) có kích thước \\(AB = 100\\)m và \\(CD = 80\\)m. Ở chính giữa sân người ta vẽ một hình tròn có tâm trùng với tâm của hình chữ nhật, bán kính bằng \\(25\\)m như hình vẽ. Lấy \\(E\\) là một vị trí trên cạnh \\(AB\\) sao cho \\(EB = 20\\)m. Mỗi vận động viên cần xuất phát từ một điểm \\(M\\) trên đường tròn và chạy theo cung đường \\(MDCBEMD\\). Vận động viên thắng cuộc là người chạy với quãng đường ngắn nhất. Tính độ dài quãng đường ngắn nhất vận động viên phải chạy (kết quả làm tròn đến hàng phần mười, đơn vị mét).",
 "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau2x.PNG",
 "answers": ["352.4", "352,4"],
 "explanation": "Đoạn đường \\(MDCBEMD\\) ngắn nhất khi và chỉ khi \\(2MD + ME\\) ngắn nhất.<br><br>Ta có: \\( OE = \\sqrt{OI^2 + IE^2} = \\sqrt{40^2+30^2} = 50 \\) m \\( = 2R \\).<br><br>Gọi \\(G = (O) \\cap OE\\), \\(H\\) là trung điểm của \\(OG\\). Khi đó:<br>\\( R = OM = OG = \\dfrac{1}{2}OE = 2.OH \\).<br><br><img src='https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau2_loigiai.PNG' style='max-width:100%;'/><br><br>Xét tam giác \\(OMH\\):<br>\\( MH^2 = OM^2 + OH^2 - 2.OM.OH.\\cos O = \\dfrac{R^2}{4}(5-4\\cos O) \\).<br><br>\\( ME^2 = OM^2+OE^2-2.OM.OE.\\cos O = R^2(5-4\\cos O) = 4MH^2 \\)<br>\\( \\Rightarrow ME = 2MH \\Rightarrow 2MD+ME = 2(MD+MH) \\).<br><br>Do đó \\(2MD+ME\\) ngắn nhất khi và chỉ khi \\(MD+MH\\) ngắn nhất, hay \\(MD+MH = DH\\), với \\(M = (O)\\cap DH\\).<br><br>Xét tam giác \\(OIE\\):<br>\\( \\dfrac{OH}{OE} = \\dfrac{IK}{IE} = \\dfrac{1}{4} \\Rightarrow IK = \\dfrac{IE}{4} = \\dfrac{15}{2} \\) m; \\( \\dfrac{HE}{OE}=\\dfrac{HK}{OI}=\\dfrac34 \\Rightarrow HK = \\dfrac{3OI}{4}=30 \\) m.<br><br>Suy ra \\( DH = \\sqrt{AK^2+(AD-HK)^2} = \\dfrac{5\\sqrt{929}}{2} \\).<br><br>Khi đó \\( 2MD+ME = 2(MD+MH) = 2DH = 5\\sqrt{929} \\).<br><br>Vậy khoảng đường chạy ngắn nhất là:<br>\\( MDCBEMD = DC+CB+BE+2MD+ME = 100+80+20+5\\sqrt{929} \\approx 352{,}4 \\) m."},
          

           {"id": "de1_sh_03", "part": 3, "type": "short",
 "content": "Giả sử tổng chi phí sản xuất \\(x\\) \\((0 \\le x \\le 50)\\) đơn vị sản phẩm \\(A\\) mỗi ngày tại một nhà máy được cho bởi công thức \\( C(x) = \\dfrac{x^2}{4} + 3x + 400 \\) (nghìn đồng) và toàn bộ chúng được bán hết với giá \\((900 - 6x)\\) nghìn đồng một sản phẩm. Tìm mức sản lượng (đó là số lượng sản phẩm được sản xuất) để chi phí trung bình tính trên mỗi đơn vị sản phẩm là đạt cực tiểu.",
 "answers": ["40"],
 "explanation": "Kí hiệu \\(\\overline{C}(x)\\) là chi phí trung bình tính trên mỗi đơn vị sản phẩm.<br><br>Ta có \\( \\overline{C}(x) = \\dfrac{C(x)}{x} = \\dfrac{x}{4} + 3 + \\dfrac{400}{x} \\).<br><br>Đạo hàm: \\( \\overline{C}'(x) = \\dfrac{x^2 - 1600}{4x^2} = 0 \\Leftrightarrow x = 40 \\) (vì \\(0 \\le x \\le 50\\)).<br><br>Bảng biến thiên:<br>Với \\(0 < x < 40\\): \\(\\overline{C}'(x) < 0\\) (hàm nghịch biến).<br>Với \\(40 < x < 50\\): \\(\\overline{C}'(x) > 0\\) (hàm đồng biến).<br><br>Do đó \\(\\overline{C}(x)\\) đạt cực tiểu tại \\(x = 40\\), khi đó \\(\\overline{C}(40) = 23\\) (nghìn đồng).<br><br>Vậy mức sản lượng cần tìm là \\( x = 40 \\)."},
           
                {"id": "de2_sh_05", "part": 3, "type": "short",
 "content": "Cho hai vectơ \\( \\vec{a}, \\vec{b} \\) sao cho \\( |\\vec{a}| = \\sqrt{2} \\), \\( |\\vec{b}| = 2 \\) và hai vectơ \\( \\vec{x} = \\vec{a} + \\vec{b} \\), \\( \\vec{y} = 2\\vec{a} - \\vec{b} \\) vuông góc với nhau. Tính góc giữa hai vectơ \\( \\vec{a} \\) và \\( \\vec{b} \\) (đơn vị độ).",
 "answers": ["90"],
 "explanation": """Vì \\( \\vec{x} \\perp \\vec{y} \\) nên \\( \\vec{x}\\cdot\\vec{y} = 0 \\), tức là:
\\( (\\vec{a}+\\vec{b})\\cdot(2\\vec{a}-\\vec{b}) = 0 \\)

Khai triển:
\\( 2|\\vec{a}|^2 - \\vec{a}\\cdot\\vec{b} + 2\\vec{a}\\cdot\\vec{b} - |\\vec{b}|^2 = 0 \\)

\\( 2|\\vec{a}|^2 + \\vec{a}\\cdot\\vec{b} - |\\vec{b}|^2 = 0 \\)

Thay \\( |\\vec{a}|^2 = 2 \\), \\( |\\vec{b}|^2 = 4 \\):

\\( 2\\cdot 2 + \\vec{a}\\cdot\\vec{b} - 4 = 0 \\Leftrightarrow \\vec{a}\\cdot\\vec{b} = 0 \\)

Vậy \\( \\cos(\\vec{a},\\vec{b}) = \\dfrac{\\vec{a}\\cdot\\vec{b}}{|\\vec{a}|\\cdot|\\vec{b}|} = 0 \\), suy ra góc giữa hai vectơ \\( \\vec{a} \\) và \\( \\vec{b} \\) bằng \\( 90^\\circ \\)."""},
            
{"id": "de2_sh_06", "part": 3, "type": "short",
 "content": "Trong không gian \\( Oxyz \\), cho các điểm \\( A(1;0;3) \\), \\( B(2;3;-4) \\), \\( C(-3;1;2) \\). Biết điểm \\( D(a;b;c) \\) sao cho \\( ABCD \\) là hình bình hành. Tính \\( a+b+c \\).",
 "answers": ["3"],
 "explanation": """Vì \\( ABCD \\) là hình bình hành nên \\( \\vec{AB} = \\vec{DC} \\).

Ta có \\( \\vec{AB} = (2-1;3-0;-4-3) = (1;3;-7) \\)

Và \\( \\vec{DC} = (-3-a;1-b;2-c) \\)

Từ \\( \\vec{AB} = \\vec{DC} \\), ta có hệ:
\\( \\begin{cases} 1 = -3-a \\\\ 3 = 1-b \\\\ -7 = 2-c \\end{cases} \\Leftrightarrow \\begin{cases} a=-4 \\\\ b=-2 \\\\ c=9 \\end{cases} \\)

Vậy \\( a+b+c = -4+(-2)+9 = 3 \\)."""},
            {"id": "de2_sh_07", "part": 3, "type": "short",
 "content": "Trong hệ trục tọa độ \\( (Oxyz) \\), một thiết bị âm thanh được phát từ vị trí \\( A(1;5;8) \\). Người ta dự định đặt một máy thu tín hiệu trên mặt phẳng \\( (Oxy) \\). Biết máy thu đặt ở vị trí \\( M(a;b;c) \\) sẽ nhận được tín hiệu sớm nhất. Khi đó \\( a+2b+3c \\) bằng bao nhiêu.",
 "answers": ["11"],
 "explanation": """Máy thu nhận được tín hiệu sớm nhất khi khoảng cách từ điểm phát \\( A \\) đến máy thu \\( M \\) là ngắn nhất, tức là \\( M \\) chính là hình chiếu vuông góc của \\( A \\) lên mặt phẳng \\( (Oxy) \\) (vì trong tất cả các điểm thuộc mặt phẳng, hình chiếu vuông góc luôn cho khoảng cách nhỏ nhất).

Mặt phẳng \\( (Oxy) \\) có phương trình \\( z = 0 \\), nên hình chiếu vuông góc của điểm \\( A(1;5;8) \\) lên mặt phẳng này chỉ đơn giản là giữ nguyên hoành độ, tung độ và cho cao độ bằng 0:

\\( M(1;5;0) \\)

Vậy \\( a=1 \\), \\( b=5 \\), \\( c=0 \\).

Do đó \\( a+2b+3c = 1+2\\cdot 5+3\\cdot 0 = 1+10+0 = 11 \\)."""},
        ], #hết đề 2
    }, #hết đề 2

 {
        "id": "de3",
        "name": "Đề số 3 - ĐÁNH GIÁ ĐỊNH KỲ THÁNG 8 - TRƯỜNG NK - LÊ THÁNH TÔNG HCM- 2026 - 2027.",
        "description": "22 câu hỏi: 12 trắc nghiệm, 4 đúng/sai, 6 trả lời ngắn.",
        "questions": [
            # ---------------- PHẦN I: TRẮC NGHIỆM 4 LỰA CHỌN ---------------- 

{
  "id": "de308_mc_01",
  "part": 1,
  "type": "mc4",
  "content": "Trong không gian \\( Oxyz \\), cho điểm \\( M(2; -3; 5) \\). Hình chiếu vuông góc của điểm \\( M \\) trên mặt phẳng \\( (Oxy) \\) có tọa độ là",
  "options": {
    "A": "\\( (2; 0; 5) \\).",
    "B": "\\( (0; -3; 5) \\).",
    "C": "\\( (2; -3; 0) \\).",
    "D": "\\( (0; 0; 5) \\)."
  },
  "correct": "C",
  "explanation": "Mặt phẳng \\( (Oxy) \\) là mặt phẳng có phương trình \\( z = 0 \\), tức là mọi điểm nằm trên mặt phẳng này đều có cao độ bằng 0.<br><br>Khi chiếu vuông góc một điểm \\( M(x_0; y_0; z_0) \\) bất kỳ xuống mặt phẳng \\( (Oxy) \\), ta chỉ việc giữ nguyên hoành độ \\( x_0 \\) và tung độ \\( y_0 \\), còn cao độ được đưa về 0. Về mặt hình học, đây chính là việc \"hạ\" điểm \\( M \\) thẳng xuống theo phương của trục \\( Oz \\) cho tới khi chạm mặt phẳng \\( (Oxy) \\).<br><br>Áp dụng cho điểm \\( M(2; -3; 5) \\): giữ nguyên \\( x = 2 \\), \\( y = -3 \\) và cho \\( z = 0 \\), ta được hình chiếu là \\( (2; -3; 0) \\).<br><br>Vậy đáp án đúng là C."
},
{
  "id": "de308_mc_02",
  "part": 1,
  "type": "mc4",
  "content": "Phương trình đường thẳng đi qua hai điểm cực trị của đồ thị hàm số \\( y = \\dfrac{x^2 - 3x + 6}{x - 2} \\) là",
  "options": {
    "A": "\\( y = 2x + 3 \\).",
    "B": "\\( y = x - 1 \\).",
    "C": "\\( y = 2x - 3 \\).",
    "D": "\\( y = -2x + 3 \\)."
  },
  "correct": "C",
  "explanation": "Trước hết ta thực hiện phép chia đa thức để tách phần nguyên: \\( x^2 - 3x + 6 = (x-2)(x-1) + 4 \\), do đó\n\\[ y = x - 1 + \\dfrac{4}{x-2}. \\]<br><br>Đạo hàm: \\( y' = 1 - \\dfrac{4}{(x-2)^2} \\). Cho \\( y' = 0 \\) ta được \\( (x-2)^2 = 4 \\), suy ra \\( x = 4 \\) hoặc \\( x = 0 \\). Đây chính là hoành độ của hai điểm cực trị.<br><br>Tại \\( x = 4 \\): \\( y = 4 - 1 + \\dfrac{4}{2} = 3 + 2 = 5 \\), ta được điểm \\( (4; 5) \\).<br>Tại \\( x = 0 \\): \\( y = 0 - 1 + \\dfrac{4}{-2} = -1 - 2 = -3 \\), ta được điểm \\( (0; -3) \\).<br><br>Đường thẳng đi qua hai điểm \\( (4; 5) \\) và \\( (0; -3) \\) có hệ số góc:\n\\[ k = \\dfrac{5 - (-3)}{4 - 0} = \\dfrac{8}{4} = 2. \\]<br><br>Phương trình đường thẳng: \\( y = 2x + b \\). Thay điểm \\( (0; -3) \\) vào ta được \\( b = -3 \\).<br><br>Vậy đường thẳng cần tìm là \\( y = 2x - 3 \\). Đáp án C."
},
{
  "id": "de308_mc_03",
  "part": 1,
  "type": "mc4",
  "content": "Nếu một khối lăng trụ có diện tích đáy bằng \\( a^2\\sqrt{3} \\) và có thể tích bằng \\( 3a^3 \\) thì chiều cao của khối lăng trụ đó bằng",
  "options": {
    "A": "\\( a \\).",
    "B": "\\( \\dfrac{a}{\\sqrt{3}} \\).",
    "C": "\\( 3a\\sqrt{3} \\).",
    "D": "\\( a\\sqrt{3} \\)."
  },
  "correct": "D",
  "explanation": "Công thức thể tích khối lăng trụ là \\( V = S_{\\text{đáy}} \\cdot h \\), trong đó \\( S_{\\text{đáy}} \\) là diện tích đáy và \\( h \\) là chiều cao.<br><br>Từ đó suy ra chiều cao:\n\\[ h = \\dfrac{V}{S_{\\text{đáy}}} = \\dfrac{3a^3}{a^2\\sqrt{3}} = \\dfrac{3a}{\\sqrt{3}} = a\\sqrt{3}. \\]<br><br>Vậy chiều cao của khối lăng trụ là \\( a\\sqrt{3} \\). Đáp án D."
},
{
  "id": "de308_mc_04",
  "part": 1,
  "type": "mc4",
  "content": "Số đường tiệm cận của đồ thị hàm số \\( y = \\dfrac{2x - 1}{x + 1} \\) là",
  "options": {
    "A": "1.",
    "B": "4.",
    "C": "3.",
    "D": "2."
  },
  "correct": "D",
  "explanation": "Hàm số \\( y = \\dfrac{2x-1}{x+1} \\) xác định khi \\( x \\neq -1 \\).<br><br><b>Tiệm cận đứng:</b> Tại \\( x = -1 \\), mẫu số triệt tiêu còn tử số \\( 2(-1) - 1 = -3 \\neq 0 \\), nên\n\\[ \\lim_{x \\to -1} \\dfrac{2x-1}{x+1} = \\infty. \\]\nDo đó \\( x = -1 \\) là tiệm cận đứng.<br><br><b>Tiệm cận ngang:</b> Ta có\n\\[ \\lim_{x \\to \\pm\\infty} \\dfrac{2x-1}{x+1} = \\lim_{x \\to \\pm\\infty} \\dfrac{2 - \\frac{1}{x}}{1 + \\frac{1}{x}} = 2. \\]\nDo đó \\( y = 2 \\) là tiệm cận ngang.<br><br>Đây là hàm phân thức bậc nhất trên bậc nhất, nên không có tiệm cận xiên. Vậy đồ thị có tổng cộng 2 đường tiệm cận (1 đứng, 1 ngang). Đáp án D."
},
{
  "id": "de308_mc_05",
  "part": 1,
  "type": "mc4",
  "content": "Cho hình lập phương \\( ABCD.A'B'C'D' \\). Góc giữa hai véc-tơ \\( \\overrightarrow{AB} \\) và \\( \\overrightarrow{DC'} \\) bằng",
  "options": {
    "A": "\\( 30^{\\circ} \\).",
    "B": "\\( 45^{\\circ} \\).",
    "C": "\\( 60^{\\circ} \\).",
    "D": "\\( 90^{\\circ} \\)."
  },
  "correct": "B",
  "explanation": "Gắn hệ trục tọa độ với cạnh hình lập phương bằng 1: \\( A(0;0;0) \\), \\( B(1;0;0) \\), \\( C(1;1;0) \\), \\( D(0;1;0) \\), \\( A'(0;0;1) \\), \\( B'(1;0;1) \\), \\( C'(1;1;1) \\), \\( D'(0;1;1) \\).<br><br>Ta có \\( \\overrightarrow{AB} = (1; 0; 0) \\) và \\( \\overrightarrow{DC'} = C' - D = (1; 1; 1) - (0; 1; 0) = (1; 0; 1) \\).<br><br>Chú ý rằng \\( DC' \\) chính là đường chéo của mặt bên \\( DCC'D' \\), có độ dài \\( \\sqrt{1^2 + 0^2 + 1^2} = \\sqrt{2} \\) (đơn vị cạnh), còn \\( |\\overrightarrow{AB}| = 1 \\).<br><br>Áp dụng công thức tích vô hướng:\n\\[ \\cos\\left(\\overrightarrow{AB}, \\overrightarrow{DC'}\\right) = \\dfrac{\\overrightarrow{AB} \\cdot \\overrightarrow{DC'}}{|\\overrightarrow{AB}| \\cdot |\\overrightarrow{DC'}|} = \\dfrac{1 \\cdot 1 + 0 \\cdot 0 + 0 \\cdot 1}{1 \\cdot \\sqrt{2}} = \\dfrac{1}{\\sqrt{2}}. \\]<br><br>Suy ra góc giữa hai véc-tơ bằng \\( 45^{\\circ} \\). Đáp án B."
},
{
  "id": "de308_mc_06",
  "part": 1,
  "type": "mc4",
  "content": "Cho hàm số \\( y = f(x) \\) liên tục trên \\( \\mathbb{R} \\) và có bảng xét dấu của đạo hàm \\( f'(x) \\) như sau.Hàm số \\( g(x) = f(|x|) \\) có bao nhiêu điểm cực trị?",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_cau6nk.PNG",
  
  "options": {
    "A": "3.",
    "B": "5.",
    "C": "4.",
    "D": "2."
  },
  "correct": "A",
  "explanation": "Từ bảng xét dấu, ta xác định chiều biến thiên của \\( f \\) trên từng khoảng: \\( f \\) giảm trên \\( (-\\infty; -2) \\), tăng trên \\( (-2; 0) \\), giảm trên \\( (0; 1) \\), tăng trên \\( (1; 3) \\) và tiếp tục tăng trên \\( (3; +\\infty) \\). Chú ý tại \\( x = 3 \\), đạo hàm bằng 0 nhưng không đổi dấu (trước và sau đều dương) nên đây không phải là điểm cực trị của \\( f \\), chỉ là điểm dừng.<br><br>Hàm \\( g(x) = f(|x|) \\) là hàm chẵn, và với \\( x \\ge 0 \\) ta có \\( g(x) = f(x) \\). Do đó trên nửa trục dương, \\( g \\) giảm trên \\( (0;1) \\), tăng trên \\( (1; +\\infty) \\) (điểm \\( x=3 \\) chỉ là điểm dừng, không làm đổi chiều biến thiên). Vậy \\( x = 1 \\) là điểm cực tiểu của \\( g \\).<br><br>Vì \\( g \\) là hàm chẵn, đồ thị của \\( g \\) trên nửa trục âm là ảnh đối xứng qua trục tung của phần đồ thị trên nửa trục dương. Do đó tại \\( x = -1 \\), \\( g \\) cũng đạt cực tiểu (đối xứng với \\( x = 1 \\)).<br><br>Xét lân cận \\( x = 0 \\): khi \\( x \\) tiến tới 0 từ bên trái (ứng với nửa đối xứng của khoảng \\( (0;1) \\)), \\( g \\) đang tăng; khi \\( x \\) tiến từ 0 sang phải, \\( g \\) đang giảm (vì \\( f \\) giảm trên \\( (0;1) \\)). Vậy \\( g \\) đổi chiều từ tăng sang giảm tại \\( x = 0 \\), suy ra \\( x = 0 \\) là điểm cực đại.<br><br>Ngoài ba điểm \\( x = -1, 0, 1 \\), không còn điểm nào khác làm \\( g \\) đổi chiều biến thiên (điểm \\( x = \\pm 3 \\) chỉ là điểm dừng, không phải cực trị).<br><br>Vậy hàm số \\( g(x) = f(|x|) \\) có đúng 3 điểm cực trị. Đáp án A."
},
          
{
  "id": "de308_mc_07",
  "part": 1,
  "type": "mc4",
  "content": "Cho tứ diện \\( OABC \\) có các cạnh \\( OA, OB, OC \\) đôi một vuông góc với nhau. Số đo của góc nhị diện \\( [B, OA, C] \\) bằng",
  "options": {
    "A": "\\( 90^{\\circ} \\).",
    "B": "\\( 30^{\\circ} \\).",
    "C": "\\( 45^{\\circ} \\).",
    "D": "\\( 60^{\\circ} \\)."
  },
  "correct": "A",
  "explanation": "Góc nhị diện \\( [B, OA, C] \\) là góc nhị diện có cạnh \\( OA \\), tạo bởi hai nửa mặt phẳng lần lượt chứa \\( B \\) và chứa \\( C \\).<br><br>Vì \\( OA \\perp OB \\) (giả thiết) nên \\( OB \\) vuông góc với cạnh \\( OA \\) tại \\( O \\). Tương tự, \\( OA \\perp OC \\) nên \\( OC \\) cũng vuông góc với cạnh \\( OA \\) tại \\( O \\).<br><br>Như vậy, tại đúng điểm \\( O \\) trên cạnh \\( OA \\), ta có hai tia \\( OB \\) và \\( OC \\) cùng vuông góc với \\( OA \\). Theo định nghĩa, góc nhị diện \\( [B, OA, C] \\) chính bằng góc giữa hai tia này, tức là góc \\( \\widehat{BOC} \\).<br><br>Mà theo giả thiết, \\( OB \\perp OC \\), nên \\( \\widehat{BOC} = 90^{\\circ} \\).<br><br>Vậy góc nhị diện \\( [B, OA, C] \\) bằng \\( 90^{\\circ} \\). Đáp án A."
},
{
  "id": "de308_mc_08",
  "part": 1,
  "type": "mc4",
  "content": "Cho hàm số \\( y = f(x) \\) xác định và liên tục trên \\( \\mathbb{R} \\) có bảng biến thiên như hình bên dưới. Gọi \\( M(x_1; y_1) \\) và \\( N(x_2; y_2) \\) lần lượt là điểm cực đại và điểm cực tiểu của đồ thị hàm số \\( y = f(x) \\). Giá trị của biểu thức \\( T = 2x_1 + x_2 - y_1 \\cdot y_2 \\) bằng<br><br><table border='1' cellpadding='6' style='border-collapse:collapse;text-align:center'><tr><td>\\(x\\)</td><td>\\(-\\infty\\)</td><td></td><td>\\(-1\\)</td><td></td><td>\\(2\\)</td><td></td><td>\\(+\\infty\\)</td></tr><tr><td>\\(f'(x)\\)</td><td></td><td>\\(+\\)</td><td>0</td><td>\\(-\\)</td><td>0</td><td>\\(+\\)</td><td></td></tr><tr><td>\\(f(x)\\)</td><td>\\(-\\infty\\)</td><td>\\(\\nearrow\\)</td><td>4</td><td>\\(\\searrow\\)</td><td>\\(-1\\)</td><td>\\(\\nearrow\\)</td><td>\\(+\\infty\\)</td></tr></table>",
  "options": {
    "A": "2.",
    "B": "4.",
    "C": "0.",
    "D": "\\( -4 \\)."
  },
  "correct": "B",
  "explanation": "Từ bảng biến thiên: hàm số tăng trên \\( (-\\infty; -1) \\), giảm trên \\( (-1; 2) \\), tăng trên \\( (2; +\\infty) \\).<br><br>Tại \\( x = -1 \\), \\( f'(x) \\) đổi dấu từ dương sang âm nên đây là điểm cực đại, với giá trị cực đại \\( f(-1) = 4 \\). Vậy \\( M(x_1; y_1) = M(-1; 4) \\), tức \\( x_1 = -1 \\), \\( y_1 = 4 \\).<br><br>Tại \\( x = 2 \\), \\( f'(x) \\) đổi dấu từ âm sang dương nên đây là điểm cực tiểu, với giá trị cực tiểu \\( f(2) = -1 \\). Vậy \\( N(x_2; y_2) = N(2; -1) \\), tức \\( x_2 = 2 \\), \\( y_2 = -1 \\).<br><br>Thay vào biểu thức:\n\\[ T = 2x_1 + x_2 - y_1 \\cdot y_2 = 2(-1) + 2 - (4)(-1) = -2 + 2 + 4 = 4. \\]<br><br>Vậy \\( T = 4 \\). Đáp án B."
},
{
  "id": "de308_mc_09",
  "part": 1,
  "type": "mc4",
  "content": "Trong không gian \\( Oxyz \\), cho hình hộp chữ nhật \\( ABCD.A'B'C'D' \\) có đỉnh \\( A \\) trùng với gốc tọa độ \\( O \\), các véc-tơ \\( \\overrightarrow{AB}, \\overrightarrow{AD}, \\overrightarrow{AA'} \\) theo thứ tự cùng hướng với các véc-tơ \\( \\vec{i}, \\vec{j}, \\vec{k} \\) và có \\( AB = 4 \\), \\( AD = 3 \\), \\( AA' = 6 \\). Khi đó, véc-tơ \\( \\overrightarrow{AC'} \\) có tọa độ là",
  "options": {
    "A": "\\( (4; 3; 6) \\).",
    "B": "\\( (3; 6; 4) \\).",
    "C": "\\( (3; 4; 6) \\).",
    "D": "\\( (6; 3; 4) \\)."
  },
  "correct": "A",
  "explanation": "Vì \\( \\overrightarrow{AB} \\) cùng hướng với \\( \\vec{i} \\) và \\( AB = 4 \\), ta có \\( \\overrightarrow{AB} = (4; 0; 0) \\).<br>Vì \\( \\overrightarrow{AD} \\) cùng hướng với \\( \\vec{j} \\) và \\( AD = 3 \\), ta có \\( \\overrightarrow{AD} = (0; 3; 0) \\).<br>Vì \\( \\overrightarrow{AA'} \\) cùng hướng với \\( \\vec{k} \\) và \\( AA' = 6 \\), ta có \\( \\overrightarrow{AA'} = (0; 0; 6) \\).<br><br>Trong hình hộp chữ nhật \\( ABCD.A'B'C'D' \\), điểm \\( C' \\) là đỉnh đối diện với \\( A \\) qua tâm hình hộp, nên đường chéo \\( \\overrightarrow{AC'} \\) chính là tổng của ba véc-tơ cạnh xuất phát từ \\( A \\):\n\\[ \\overrightarrow{AC'} = \\overrightarrow{AB} + \\overrightarrow{AD} + \\overrightarrow{AA'} = (4; 0; 0) + (0; 3; 0) + (0; 0; 6) = (4; 3; 6). \\]<br><br>Vậy \\( \\overrightarrow{AC'} = (4; 3; 6) \\). Đáp án A."
},
{
  "id": "de308_mc_10",
  "part": 1,
  "type": "mc4",
  "content": "Cho hàm số \\( y = x^3 - 6x^2 + 15x - 2 \\) có đồ thị là \\( (C) \\). Hệ số góc nhỏ nhất của tiếp tuyến tại một điểm \\( M \\) thuộc đồ thị \\( (C) \\) là",
  "options": {
    "A": "1.",
    "B": "3.",
    "C": "5.",
    "D": "0."
  },
  "correct": "B",
  "explanation": "Hệ số góc của tiếp tuyến tại điểm \\( M(x_0; y_0) \\) thuộc đồ thị chính là giá trị đạo hàm tại \\( x_0 \\):\n\\[ k(x) = y' = 3x^2 - 12x + 15. \\]<br><br>Đây là một tam thức bậc hai theo \\( x \\) với hệ số \\( a = 3 > 0 \\), do đó \\( k(x) \\) đạt giá trị nhỏ nhất tại đỉnh parabol, ứng với\n\\[ x_0 = -\\dfrac{b}{2a} = -\\dfrac{-12}{2 \\cdot 3} = 2. \\]<br><br>Giá trị nhỏ nhất của hệ số góc:\n\\[ k(2) = 3(2)^2 - 12(2) + 15 = 12 - 24 + 15 = 3. \\]<br><br>Vậy hệ số góc nhỏ nhất của tiếp tuyến với đồ thị \\( (C) \\) bằng 3. Đáp án B."
},
{
  "id": "de308_mc_11",
  "part": 1,
  "type": "mc4",
  "content": "Trong không gian \\( Oxyz \\), cho ba điểm \\( A(1; -1; 2) \\), \\( B(5; 2; 1) \\) và \\( C(2; 0; 3) \\). Tìm điểm \\( M \\) trên trục \\( Ox \\) sao cho \\( AM \\) vuông góc với \\( BC \\).",
  "options": {
    "A": "\\( M(-5; 0; 0) \\).",
    "B": "\\( M(1; 0; 0) \\).",
    "C": "\\( M(2; 0; 0) \\).",
    "D": "\\( M(-1; 0; 0) \\)."
  },
  "correct": "D",
  "explanation": "Vì \\( M \\) thuộc trục \\( Ox \\) nên \\( M(m; 0; 0) \\) với \\( m \\) là tham số cần tìm.<br><br>Ta có \\( \\overrightarrow{AM} = M - A = (m - 1; 0 - (-1); 0 - 2) = (m - 1; 1; -2) \\).<br><br>Và \\( \\overrightarrow{BC} = C - B = (2 - 5; 0 - 2; 3 - 1) = (-3; -2; 2) \\).<br><br>Điều kiện \\( AM \\perp BC \\) tương đương với \\( \\overrightarrow{AM} \\cdot \\overrightarrow{BC} = 0 \\):\n\\[ (m-1)(-3) + (1)(-2) + (-2)(2) = 0 \\]\n\\[ -3m + 3 - 2 - 4 = 0 \\]\n\\[ -3m - 3 = 0 \\]\n\\[ m = -1. \\]<br><br>Vậy \\( M(-1; 0; 0) \\). Đáp án D."
},
{
  "id": "de308_mc_12",
  "part": 1,
  "type": "mc4",
  "content": "Một hệ thống cảnh báo cháy tự động của một tòa nhà được lắp đặt hai cảm biến \\( A \\) và \\( B \\) hoạt động độc lập với nhau. Khi xảy ra sự cố cháy, xác suất để cảm biến \\( A \\) và cảm biến \\( B \\) phát tín hiệu cảnh báo tương ứng là \\( 0{,}9 \\) và \\( 0{,}85 \\). Tính xác suất để khi xảy ra sự cố cháy, tòa nhà nhận được tín hiệu cảnh báo từ ít nhất một trong hai cảm biến.",
  "options": {
    "A": "0,765.",
    "B": "0,975.",
    "C": "0,985.",
    "D": "0,925."
  },
  "correct": "C",
  "explanation": "Gọi \\( A \\) là biến cố \"cảm biến A phát tín hiệu cảnh báo\", \\( B \\) là biến cố \"cảm biến B phát tín hiệu cảnh báo\". Theo giả thiết, \\( A \\) và \\( B \\) độc lập, với \\( P(A) = 0{,}9 \\) và \\( P(B) = 0{,}85 \\).<br><br>Biến cố \"nhận được tín hiệu cảnh báo từ ít nhất một trong hai cảm biến\" chính là biến cố \\( A \\cup B \\). Ta sẽ tính thông qua biến cố đối: \"cả hai cảm biến đều không phát tín hiệu\", tức là \\( \\overline{A} \\cap \\overline{B} \\).<br><br>Xác suất cảm biến A không phát tín hiệu: \\( P(\\overline{A}) = 1 - 0{,}9 = 0{,}1 \\).<br>Xác suất cảm biến B không phát tín hiệu: \\( P(\\overline{B}) = 1 - 0{,}85 = 0{,}15 \\).<br><br>Vì \\( A \\), \\( B \\) độc lập nên \\( \\overline{A} \\), \\( \\overline{B} \\) cũng độc lập với nhau, do đó:\n\\[ P(\\overline{A} \\cap \\overline{B}) = P(\\overline{A}) \\cdot P(\\overline{B}) = 0{,}1 \\times 0{,}15 = 0{,}015. \\]<br><br>Vậy xác suất nhận được tín hiệu cảnh báo từ ít nhất một cảm biến là:\n\\[ P(A \\cup B) = 1 - P(\\overline{A} \\cap \\overline{B}) = 1 - 0{,}015 = 0{,}985. \\]<br><br>Đáp án C."
}
          
{
  "id": "de3_tf_01",
  "part": 2,
  "type": "truefalse",
  "content": "Một công ty khởi nghiệp mô hình hóa tốc độ tăng trưởng doanh thu hàng năm \\( y = f(t) \\) (đơn vị: tỷ đồng/năm) theo thời gian \\( t \\) (đơn vị: năm, với \\( t \\ge 0 \\)) bằng một hàm số đa thức bậc ba \\( y = at^3 + bt^2 + ct + d \\) (\\( a \\ne 0 \\)) có đồ thị như hình vẽ bên. Xét tính đúng sai của các mệnh đề sau:",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_tf1_dothi.PNG",
  "statements": [
    {"text": "Công thức xác định tốc độ tăng trưởng doanh thu của công ty là \\( f(t) = -2t^3 + 3t^2 + 1 \\).", "correct": true},
    {"text": "Doanh thu của công ty đạt tốc độ tăng trưởng cực đại tại thời điểm \\( t = 2 \\) năm.", "correct": false},
    {"text": "Trong năm đầu tiên (\\( 0 \\le t \\le 1 \\)), tốc độ tăng trưởng doanh thu của công ty luôn có xu hướng tăng.", "correct": true},
    {"text": "Tại thời điểm \\( t = 1{,}5 \\) năm, tốc độ tăng trưởng doanh thu của công ty đạt giá trị bằng 2 tỷ đồng/năm.", "correct": false}
  ],
  "explanation": "<b>a) Đúng.</b> Công thức xác định là \\( f(t) = -2t^3+3t^2+1 \\)?<br><br>Quan sát đồ thị, ta thấy hàm số đạt cực tiểu tại điểm \\( (0;1) \\) và đạt cực đại tại điểm \\( (1;2) \\). Vì đây là hai điểm cực trị nên đạo hàm \\( f'(t) = 3at^2+2bt+c \\) phải triệt tiêu tại \\( t=0 \\) và \\( t=1 \\), đồng thời giá trị hàm tại hai điểm đó lần lượt bằng 1 và 2.<br><br>Từ \\( f'(0)=0 \\), ta có ngay \\( c = 0 \\).<br>Từ \\( f(0)=1 \\), ta có \\( d = 1 \\).<br>Từ \\( f'(1)=0 \\): \\( 3a+2b+c=0 \\Rightarrow 3a+2b=0 \\).<br>Từ \\( f(1)=2 \\): \\( a+b+c+d=2 \\Rightarrow a+b+1=2 \\Rightarrow a+b=1 \\).<br><br>Giải hệ \\( \\begin{cases} 3a+2b=0 \\\\ a+b=1 \\end{cases} \\), thay \\( b = 1-a \\) vào phương trình đầu:\n\\[ 3a+2(1-a)=0 \\Rightarrow a+2=0 \\Rightarrow a=-2 \\Rightarrow b=3. \\]<br><br>Vậy \\( f(t) = -2t^3+3t^2+1 \\). Mệnh đề a) đúng.<br><br><b>b) Sai.</b> Doanh thu đạt tốc độ tăng trưởng cực đại tại \\( t=2 \\)?<br><br>Ta có \\( f'(t) = -6t^2+6t = 6t(1-t) \\). Xét dấu trên \\( [0;+\\infty) \\): với \\( 0<t<1 \\) thì \\( f'(t)>0 \\) (tăng); với \\( t>1 \\) thì \\( f'(t)<0 \\) (giảm). Vậy \\( f(t) \\) đạt cực đại tại \\( t=1 \\) (không phải \\( t=2 \\)), với giá trị \\( f(1) = -2+3+1=2 \\). Mệnh đề b) sai.<br><br><b>c) Đúng.</b> Trong năm đầu tiên, tốc độ tăng trưởng luôn có xu hướng tăng?<br><br>Như đã xét ở câu b), với mọi \\( t\\in(0;1) \\) ta có \\( f'(t) = 6t(1-t) > 0 \\) (vì cả \\( t \\) và \\( 1-t \\) đều dương). Do đó hàm số \\( f(t) \\) đồng biến trên \\( (0;1) \\), nghĩa là tốc độ tăng trưởng doanh thu luôn có xu hướng tăng trong năm đầu tiên. Mệnh đề c) đúng.<br><br><b>d) Sai.</b> Tại \\( t=1{,}5 \\), tốc độ tăng trưởng bằng 2?<br><br>Ta tính \\( f(1{,}5) = -2(1{,}5)^3+3(1{,}5)^2+1 = -2(3{,}375)+3(2{,}25)+1 = -6{,}75+6{,}75+1 = 1 \\).<br><br>Vậy tại \\( t=1{,}5 \\), tốc độ tăng trưởng doanh thu bằng 1 tỷ đồng/năm, không phải 2. Mệnh đề d) sai."
},
{
  "id": "de3_tf_02",
  "part": 2,
  "type": "truefalse",
  "content": "Trong một ca trực tại Trạm kiểm soát không lưu sân bay Tân Sơn Nhất, các kỹ sư ra-đa thiết lập hệ trục tọa độ \\( Oxyz \\) (đơn vị trên các trục tính bằng ki-lô-mét) với gốc \\( O(0;0;0) \\) là vị trí đặt tháp điều hành không lưu. Lúc 8 giờ sáng, hệ thống theo dõi một máy bay thương mại đang ở vị trí \\( M_0(50;120;4) \\). Máy bay đang bay ổn định với véc-tơ vận tốc không đổi là \\( \\vec{v} = (300;400;3) \\) (đơn vị: km/h). Xét tính đúng sai của các mệnh đề sau:",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_tf2_hetruc.PNG",
  "statements": [
    {"text": "Tại thời điểm 8 giờ sáng, khoảng cách từ máy bay đến tháp điều hành không lưu xấp xỉ 130 km (sai số không quá 1 km).", "correct": true},
    {"text": "Tại thời điểm 9 giờ sáng, độ cao của máy bay so với mặt đất là 8 km.", "correct": false},
    {"text": "Tại thời điểm 10 giờ sáng, khoảng cách từ máy bay đến tháp truyền hình \\( F(1\\,250;1\\,020;0) \\) xấp xỉ 700 km (sai số không quá 10 km).", "correct": false},
    {"text": "Khi đạt độ cao 10 km, máy bay nhận lệnh hạ cánh và đổi sang vận tốc mới là \\( \\vec{v}_2 = (400;300;-5) \\) km/h để hướng về đường băng B. Tọa độ của máy bay ngay khi chạm đất tại đường băng B là \\( (1\\,450;1\\,520;0) \\).", "correct": true}
  ],
  "explanation": "Vị trí máy bay tại thời điểm \\( t \\) giờ sau 8 giờ sáng: \\( M(t) = M_0 + t\\vec{v} = (50+300t;\\ 120+400t;\\ 4+3t) \\).<br><br><b>a) Đúng.</b> Khoảng cách lúc 8 giờ sáng chính là \\( |OM_0| \\):\n\\[ OM_0 = \\sqrt{50^2+120^2+4^2} = \\sqrt{2500+14400+16} = \\sqrt{16916} \\approx 130{,}06 \\text{ km}. \\]<br><br>Giá trị này xấp xỉ 130 km với sai số nhỏ hơn 1 km. Mệnh đề a) đúng.<br><br><b>b) Sai.</b> Độ cao lúc 9 giờ sáng ứng với \\( t=1 \\):\n\\[ z(1) = 4+3(1) = 7 \\text{ km}. \\]<br><br>Độ cao thực tế là 7 km chứ không phải 8 km. Mệnh đề b) sai.<br><br><b>c) Sai.</b> Lúc 10 giờ sáng ứng với \\( t=2 \\), vị trí máy bay là:\n\\[ M(2) = (50+600;\\ 120+800;\\ 4+6) = (650;\\ 920;\\ 10). \\]<br><br>Khoảng cách đến \\( F(1\\,250;1\\,020;0) \\):\n\\[ MF = \\sqrt{(1250-650)^2+(1020-920)^2+(0-10)^2} = \\sqrt{600^2+100^2+10^2} = \\sqrt{370100} \\approx 608{,}4 \\text{ km}. \\]<br><br>Giá trị này lệch khá xa so với 700 km (sai số hơn 10 km), nên mệnh đề c) sai.<br><br><b>d) Đúng.</b> Tại \\( t=2 \\) (đúng 10 giờ sáng), máy bay đang ở độ cao \\( z=10 \\) km, khớp với thời điểm \"đạt độ cao 10 km\" nêu trong đề, tại vị trí \\( (650;920;10) \\).<br><br>Từ lúc này, máy bay bay với vận tốc mới \\( \\vec{v}_2=(400;300;-5) \\). Gọi \\( t' \\) là thời gian bay thêm kể từ lúc đổi vận tốc, độ cao lúc này là \\( z = 10 - 5t' \\). Máy bay chạm đất khi \\( z=0 \\):\n\\[ 10-5t' = 0 \\Rightarrow t'=2 \\text{ giờ}. \\]<br><br>Tọa độ khi chạm đất:\n\\[ x = 650+400(2) = 1450,\\quad y = 920+300(2)=1520,\\quad z=0. \\]<br><br>Vậy tọa độ điểm chạm đất là \\( (1450;1520;0) \\), khớp với mệnh đề. Mệnh đề d) đúng."
},
{
  "id": "de3_tf_03",
  "part": 2,
  "type": "truefalse",
  "content": "Một công ty công nghệ phân tích hiệu quả của chiến dịch tiếp thị ứng dụng mới. Tổng thời gian người dùng tương tác tích lũy trên hệ thống theo thời gian \\( t \\) (\\( t \\ge 0 \\), tính bằng tuần) được mô hình hóa bởi hàm số \\( x(t) = 2t - 2\\ln(t+1) \\) (đơn vị: triệu giờ). Hàm số \\( v(t) = x'(t) \\) biểu thị tốc độ tương tác của người dùng tại thời điểm \\( t \\) (đơn vị: triệu giờ/tuần). Xét tính đúng sai của các mệnh đề sau:",
  "statements": [
    {"text": "\\( v(t) = 2 - \\dfrac{3}{t+1} \\).", "correct": false},
    {"text": "Tốc độ tương tác tại thời điểm ban đầu (\\( t=0 \\)) là 2 triệu giờ/tuần.", "correct": false},
    {"text": "Tốc độ tương tác tại thời điểm \\( t=1 \\) tuần bằng 1 triệu giờ/tuần.", "correct": true},
    {"text": "Gia tốc tương tác của người dùng tại thời điểm \\( t=1 \\) tuần bằng 0,5 triệu giờ/tuần\\(^2\\).", "correct": true}
  ],
  "explanation": "<b>a) Sai.</b> \\( v(t) = 2-\\dfrac{3}{t+1} \\)?<br><br>Ta có \\( x(t) = 2t - 2\\ln(t+1) \\). Đạo hàm:\n\\[ v(t) = x'(t) = 2 - 2\\cdot\\dfrac{1}{t+1} = 2 - \\dfrac{2}{t+1}. \\]<br><br>Vậy hệ số đúng ở phân số là 2, không phải 3. Mệnh đề a) sai.<br><br><b>b) Sai.</b> Tốc độ tương tác tại \\( t=0 \\) là 2?<br><br>Thay \\( t=0 \\) vào \\( v(t) = 2-\\dfrac{2}{t+1} \\):\n\\[ v(0) = 2 - \\dfrac{2}{0+1} = 2-2 = 0. \\]<br><br>Vậy tốc độ tương tác ban đầu bằng 0, không phải 2 triệu giờ/tuần. Mệnh đề b) sai.<br><br><b>c) Đúng.</b> Tốc độ tương tác tại \\( t=1 \\) bằng 1?<br><br>\\[ v(1) = 2-\\dfrac{2}{1+1} = 2-1 = 1. \\]<br><br>Vậy tại \\( t=1 \\), tốc độ tương tác đúng bằng 1 triệu giờ/tuần. Mệnh đề c) đúng.<br><br><b>d) Đúng.</b> Gia tốc tại \\( t=1 \\) bằng 0,5?<br><br>Gia tốc tương tác là đạo hàm của \\( v(t) \\), tức là \\( a(t) = v'(t) \\). Viết lại \\( v(t) = 2-2(t+1)^{-1} \\), ta có:\n\\[ a(t) = v'(t) = 2(t+1)^{-2} = \\dfrac{2}{(t+1)^2}. \\]<br><br>Tại \\( t=1 \\):\n\\[ a(1) = \\dfrac{2}{(1+1)^2} = \\dfrac{2}{4} = 0{,}5. \\]<br><br>Vậy gia tốc tương tác tại \\( t=1 \\) đúng bằng 0,5 triệu giờ/tuần\\(^2\\). Mệnh đề d) đúng."
},
{
  "id": "de3_tf_04",
  "part": 2,
  "type": "truefalse",
  "content": "Xét phép thử chọn ngẫu nhiên một số tự nhiên có hai chữ số. Xét biến cố \\( A \\): \"Số được chọn là số chia hết cho 8\" và biến cố \\( B \\): \"Số được chọn là số có hai chữ số giống nhau\". Xét tính đúng sai của các mệnh đề sau:",
  "statements": [
    {"text": "Số phần tử của không gian mẫu là \\( n(\\Omega) = 89 \\).", "correct": false},
    {"text": "Xác suất của biến cố \\( A \\) là \\( P(A) = \\dfrac{11}{90} \\).", "correct": true},
    {"text": "Xác suất của biến cố \\( B \\) là \\( P(B) = \\dfrac{1}{10} \\).", "correct": true},
    {"text": "Xác suất của biến cố hợp \\( A \\cup B \\) là \\( P(A \\cup B) = \\dfrac{2}{9} \\).", "correct": false}
  ],
  "explanation": "<b>a) Sai.</b> \\( n(\\Omega) = 89 \\)?<br><br>Số tự nhiên có hai chữ số chạy từ 10 đến 99, nên số phần tử của không gian mẫu là:\n\\[ n(\\Omega) = 99-10+1 = 90. \\]<br><br>Vậy \\( n(\\Omega)=90 \\), không phải 89. Mệnh đề a) sai.<br><br><b>b) Đúng.</b> \\( P(A) = \\dfrac{11}{90} \\)?<br><br>Các số có hai chữ số chia hết cho 8 là các số dạng \\( 8k \\) với \\( 10 \\le 8k \\le 99 \\), tức \\( 2 \\le k \\le 12 \\) (vì \\( 8\\times2=16 \\) và \\( 8\\times12=96 \\)). Số các giá trị \\( k \\) từ 2 đến 12 là \\( 12-2+1=11 \\) số (là 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96).<br><br>Vậy \\( n(A)=11 \\), suy ra \\( P(A) = \\dfrac{11}{90} \\). Mệnh đề b) đúng.<br><br><b>c) Đúng.</b> \\( P(B) = \\dfrac{1}{10} \\)?<br><br>Các số có hai chữ số giống nhau là: 11, 22, 33, 44, 55, 66, 77, 88, 99 — tổng cộng 9 số. Vậy \\( n(B)=9 \\), suy ra\n\\[ P(B) = \\dfrac{9}{90} = \\dfrac{1}{10}. \\]<br><br>Mệnh đề c) đúng.<br><br><b>d) Sai.</b> \\( P(A\\cup B) = \\dfrac{2}{9} \\)?<br><br>Áp dụng công thức: \\( P(A\\cup B) = P(A)+P(B)-P(A\\cap B) \\).<br><br>Biến cố \\( A\\cap B \\) gồm các số vừa chia hết cho 8, vừa có hai chữ số giống nhau: kiểm tra trong các số 11, 22, ..., 99, chỉ có 88 chia hết cho 8 (\\( 88 = 8\\times11 \\)). Vậy \\( n(A\\cap B)=1 \\), suy ra \\( P(A\\cap B) = \\dfrac{1}{90} \\).<br><br>Do đó:\n\\[ P(A\\cup B) = \\dfrac{11}{90}+\\dfrac{9}{90}-\\dfrac{1}{90} = \\dfrac{19}{90}. \\]<br><br>Trong khi đó \\( \\dfrac{2}{9} = \\dfrac{20}{90} \\), khác với \\( \\dfrac{19}{90} \\) vừa tính được. Mệnh đề d) sai."
}



          ], #hết đề 3
    }, #hết đề 3
       
  
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

            {% if q.image %}
            <div style="text-align:center; margin:10px 0;">
              <img src="{{ q.image }}" alt="Hình minh họa câu {{ loop.index }}" style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
            </div>
            {% endif %}
            {% if q.content_after_image %}
            <div class="q-content">{{ q.content_after_image|safe }}</div>
            {% endif %}

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

      {% if q.image %}
      <div style="text-align:center; margin:10px 0;">
        <img src="{{ q.image }}" alt="Hình minh họa câu {{ loop.index }}" style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
      </div>
      {% endif %}
      {% if q.content_after_image %}
      <div class="q-content">{{ q.content_after_image|safe }}</div>
      {% endif %}

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
