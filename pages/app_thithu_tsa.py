# -*- coding: utf-8 -*-
"""
=======================================================================
  ỨNG DỤNG THI THỬ TSA - 1 FILE PYTHON DUY NHẤT (app.py)
=======================================================================
Học sinh chọn đề thi -> làm bài -> nộp bài -> xem điểm & đáp án chi tiết.
Hỗ trợ đủ 4 dạng câu hỏi:
  1. mc4       : Trắc nghiệm 4 lựa chọn
  2. truefalse : Đúng/Sai (nhiều mệnh đề)
  3. short     : Trả lời ngắn
  4. dragdrop  : Kéo thả

ĐIỂM MỚI TRONG BẢN NÀY:
  - KHÔNG CẦN TÀI KHOẢN để vào thi: học sinh chỉ cần nhập họ tên là bắt đầu
    làm bài ngay (không có bước tạo/đăng nhập tài khoản, không quản lý
    tài khoản học sinh ở trang quản trị).
  - Giao diện chuyển sang tông màu ĐỎ theo đúng màu nhận diện kỳ thi TSA.
  - Công thức toán học được render đúng bằng MathJax: toàn bộ ngân hàng câu
    hỏi gốc đã được viết bằng LaTeX (phân số, căn, mũ, giới
    hạn, vector, góc...) để hiển thị đúng kiểu chữ Toán học thay vì ký tự
    Unicode thô. Câu hỏi thêm qua trang quản trị cũng gõ LaTeX theo cú pháp
    \\( ... \\) (inline) hoặc \\[ ... \\] / $$ ... $$ (hiển thị khối).
  - Đồng hồ đếm NGƯỢC 60 phút (giống thời gian làm bài thi TSA chính thức:
    40 câu / 60 phút), hết giờ sẽ tự động nộp bài; còn dưới 5 phút đồng hồ
    chuyển sang nhấp nháy cảnh báo.
  - Mỗi câu hỏi có thể gắn thêm 1 hình ảnh minh hoạ (ảnh vẽ hình học,
    biểu đồ, ...) bằng cách thêm trường "image" (đường dẫn/URL ảnh)
    trong khối "questions" của từng đề, hoặc dùng trang Quản trị để tải
    ảnh lên khi thêm câu hỏi mới.
  - MỖI ĐỀ THI CÓ NGÂN HÀNG CÂU HỎI RIÊNG, ĐỘC LẬP: câu hỏi của từng đề
    được viết trực tiếp trong khối "questions" của đề đó (biến EXAMS),
    không còn dùng chung 1 ngân hàng QUESTIONS cho tất cả đề như trước.
    Muốn thêm/sửa/bớt câu hỏi của đề nào, chỉ sửa đúng khối của đề đó.
  - Có trang QUẢN TRỊ (/admin) cho phép giáo viên thêm câu hỏi mới vào
    NGAY SAU đề thi đã có (không cần sửa code, không cần deploy lại).
    Câu hỏi thêm qua trang quản trị được lưu vào file JSON:
        data/extra_questions.json   (mỗi câu có kèm exam_id thuộc đề nào)
    File này (và thư mục static/uploads) KHÔNG nên đưa lên GitHub
    (đã có gợi ý .gitignore ở cuối file) vì đây là dữ liệu sinh ra khi
    vận hành trên VPS, tương tự database.db.

CHẠY THỬ TRÊN MÁY:
    pip install Flask gunicorn
    python app.py
    -> mở http://127.0.0.1:5000
    -> trang quản trị: http://127.0.0.1:5000/admin  (mật khẩu mặc định: tsa2026,
       đổi bằng biến môi trường ADMIN_PASSWORD khi deploy thật)

DEPLOY LÊN VPS: xem hướng dẫn ở cuối file (phần "HƯỚNG DẪN DEPLOY").

Toàn bộ ngân hàng câu hỏi GỐC nằm trong biến EXAMS bên dưới, mỗi đề tự
chứa câu hỏi riêng trong khoá "questions" của đề đó.
Muốn thêm câu hỏi/đề mới vĩnh viễn (đưa vào code): sửa biến EXAMS.
Muốn thêm nhanh câu hỏi vào cuối 1 đề đang chạy trên VPS: dùng /admin.
=======================================================================
"""
import json
import os
import sqlite3
import uuid
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template_string, request, redirect,
    url_for, abort, g, session, flash
)
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

DATA_DIR = os.path.join(BASE_DIR, "data")
EXTRA_Q_PATH = os.path.join(DATA_DIR, "extra_questions.json")
OVERRIDES_PATH = os.path.join(DATA_DIR, "question_overrides.json")
EXAM_REMOVED_PATH = os.path.join(DATA_DIR, "exam_removed.json")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "webp", "svg"}

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "doi-key-nay-khi-deploy-that")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8MB / request

# Đổi mật khẩu quản trị bằng biến môi trường ADMIN_PASSWORD khi deploy thật.
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "tsa2026")

# =======================================================================
# SSO VỚI WORDPRESS: chỉ học sinh ĐÃ ĐĂNG NHẬP trên web chính (WordPress)
# mới được vào thi. WordPress tạo 1 "vé" (token) đã ký bằng mã bí mật dùng
# chung (WP_SSO_SECRET), gắn vào URL nhúng iframe dạng ?wp_token=...
# App này giải mã + kiểm tra chữ ký token đó để xác nhận chính WordPress
# đã tạo ra (không ai giả mạo được nếu không biết mã bí mật).
# Đổi WP_SSO_SECRET bằng biến môi trường khi deploy thật, và PHẢI dùng
# ĐÚNG chuỗi bí mật giống hệt bên WordPress (functions.php).
# =======================================================================
import hmac
import hashlib
import base64
import time
import os
WP_SSO_SECRET = "FocusEdu2026-Sso-Xk9mQp3vLr7z"
WP_TOKEN_MAX_AGE = 900  # token chỉ có hiệu lực 15 phút kể từ lúc WordPress tạo ra


def verify_wp_token(token):
    """Giải mã & kiểm tra chữ ký token do WordPress tạo. Trả về họ tên học sinh
    nếu token hợp lệ và chưa hết hạn, trả về None nếu token sai/giả mạo/hết hạn."""
    if not token:
        print("DEBUG FLASK: Không nhận được token trong URL (token rỗng)")
        return None
    try:
        padded_token = token + '=' * (-len(token) % 4)
        raw = base64.urlsafe_b64decode(padded_token.encode("utf-8")).decode("utf-8")
        name, ts_str, sig = raw.rsplit("|", 2)
    except Exception as e:
        print(f"DEBUG FLASK: Lỗi decode Base64: {e}")
        return None

    expected_sig = hmac.new(
        WP_SSO_SECRET.encode("utf-8"), f"{name}|{ts_str}".encode("utf-8"), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(sig, expected_sig):
        print("DEBUG FLASK: Sai chữ ký HMAC (Mã secret không khớp giữa WP và Flask)")
        return None

    try:
        if time.time() - int(ts_str) > WP_TOKEN_MAX_AGE:
            print(f"DEBUG FLASK: Token hết hạn! Giờ server: {time.time()}, Giờ token: {ts_str}")
            return None
    except Exception as e:
        print(f"DEBUG FLASK: Lỗi kiểm tra thời gian: {e}")
        return None

    return name


# =======================================================================
# 1) NGÂN HÀNG ĐỀ THI - MỖI ĐỀ CÓ CÂU HỎI RIÊNG, ĐỘC LẬP HOÀN TOÀN
#    -> Mỗi đề (EXAMS[i]) tự chứa danh sách câu hỏi của chính nó trong
#       khoá "questions". KHÔNG còn ngân hàng câu hỏi dùng chung giữa
#       các đề nữa: muốn thêm/sửa/xoá câu hỏi của đề nào, chỉ cần sửa
#       ngay trong khối "questions" của đề đó - không ảnh hưởng đề khác.
#    -> Có thể thêm trường "image": "/static/uploads/ten_anh.png" hoặc
#       "image": "https://duong-dan-anh-ngoai.jpg" cho câu hỏi nào có
#       hình vẽ minh hoạ.
#    -> id của mỗi câu hỏi được đặt tiền tố theo đề (vd "de1_mc_01") để
#       không bao giờ trùng với câu hỏi của đề khác.
# =======================================================================
EXAMS = [
    {
        "id": 'de_tsa11_tungthay',
        "name": 'Đề ôn tập TSA Toán 11 ',
        "description": '4 câu hỏi đầu của đề, đủ 4 dạng: trắc nghiệm, đúng/sai, trả lời ngắn, kéo thả.',
        "questions": [

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de_tsa11_mc_01',
                "type": 'mc4',
                "content": ' Cho hàm số \\( y = \\dfrac{\\sin x + 2\\cos x + m}{\\cos x - 2\\sin x + 3} \\). Có bao nhiêu giá trị nguyên của tham số \\( m \\) để tập giá trị của hàm số này chứa đoạn \\( [-1; 1] \\)?',
                "options": {
                    'A': '0',
                    'B': '1',
                    'C': '2',
                    'D': '3',
                },
                "correct": 'B',
                "points": 1,
                "explanation": 'Biến đổi: \\( y(\\cos x - 2\\sin x + 3) = \\sin x + 2\\cos x + m \\Leftrightarrow (y-2)\\cos x - (2y+1)\\sin x = m - 3y \\). Phương trình này có nghiệm \\( x \\) khi và chỉ khi \\( (m-3y)^2 \\le (y-2)^2+(2y+1)^2 = 5y^2+5 \\). Để \\( [-1;1] \\subset \\) tập giá trị, cần bất đẳng thức trên đúng với mọi \\( y\\in[-1,1] \\), tức \\( f(y)=4y^2-6my+m^2-5\\le0,\\ \\forall y\\in[-1,1] \\). Do \\( f(y) \\) là parabol quay bề lõm lên trên nên chỉ cần xét 2 đầu mút: \\( f(1)=m^2-6m-1\\le0 \\Rightarrow m\\in[3-\\sqrt{10};\\,3+\\sqrt{10}] \\) và \\( f(-1)=m^2+6m-1\\le0 \\Rightarrow m\\in[-3-\\sqrt{10};\\,-3+\\sqrt{10}] \\). Giao 2 khoảng: \\( m\\in[\\sqrt{10}-3;\\,3-\\sqrt{10}] \\approx [-0.162;\\,0.162] \\). Chỉ có \\( m=0 \\) nguyên thoả mãn \\( \\Rightarrow \\) có đúng 1 giá trị. Đáp án B.',
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": 'de_tsa11_tf_01',
                "type": 'truefalse',
                "content": " Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh \\( a \\). Tam giác SAB đều và nằm trong mặt phẳng vuông góc với đáy. Gọi M, N lần lượt là trung điểm của SC và SD. Xét tính Đúng/Sai của các mệnh đề sau:",
                "statements": [
                    {"text": 'Góc tạo bởi mặt phẳng (SCD) và mặt đáy bằng \\( 60^\\circ \\)', "correct": False},
                    {"text": 'Khoảng cách giữa hai đường thẳng AM và SB bằng \\( \\dfrac{a\\sqrt3}{4} \\)', "correct": True},
                    {"text": 'Thể tích khối tứ diện S.AMN bằng \\( \\dfrac{a^3\\sqrt3}{48} \\)', "correct": True},
                    {"text": 'Bán kính mặt cầu ngoại tiếp hình chóp S.ABCD bằng \\( \\dfrac{a\\sqrt{21}}{6} \\)', "correct": True},
                ],
                "points": 1,
                "explanation": "Chọn hệ trục: A(0,0,0), B(a,0,0), C(a,a,0), D(0,a,0), trung điểm AB là (a/2,0,0), do (SAB) vuông góc đáy nên S(a/2, 0, a√3/2). (a) Gọi H là trung điểm CD(a/2,a,0): S'H (S' là hình chiếu S) = a, SS' = a√3/2 ⇒ tan(góc) = √3/2 ⇒ góc ≈ 40.9° ≠ 60° ⇒ Sai. (b) M = trung điểm SC = (3a/4, a/2, a√3/4). Dùng công thức khoảng cách 2 đường chéo nhau AM, SB (tích có hướng 2 vtcp và vectơ AS) ⇒ d = a√3/4 ⇒ Đúng. (c) Với M,N là trung điểm SC,SD: V(S.AMN) = (SM/SC)(SN/SD)·V(S.ACD) = (1/2)(1/2)·(1/2)V(S.ABCD) = (1/8)V(S.ABCD). Mà V(S.ABCD) = (1/3)·a²·(a√3/2) = a³√3/6 ⇒ V(S.AMN) = a³√3/48 ⇒ Đúng. (d) Tâm mặt cầu ngoại tiếp có dạng O(a/2, a/2, z₀) do cách đều 4 đỉnh đáy; cho OA = OS giải được z₀ = a√3/6, suy ra R² = a²/2 + z₀² = 7a²/12 ⇒ R = a√21/6 ⇒ Đúng.",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de_tsa11_sh_01',
                "type": 'short',
                "content": ' Xếp 10 học sinh gồm 5 nam và 5 nữ vào 10 chiếc ghế được xếp thành một vòng tròn. Tính xác suất để không có bất kỳ 2 học sinh cùng giới tính nào ngồi cạnh nhau, đồng thời học sinh nam tên A và học sinh nữ tên B (là 2 lớp trưởng) bắt buộc phải ngồi đối diện nhau. Biết xác suất là phân số tối giản \\( \\dfrac{p}{q} \\). Tính giá trị của biểu thức \\( S = p + q \\).',
                "blanks": [
                    {"label": 'S = p + q =', "answers": ['631']},
                ],
                "points": 1,
                "explanation": 'Không gian mẫu: \\( n(\\Omega)=10! \\) (10 ghế phân biệt). Điều kiện không có 2 người cùng giới ngồi cạnh nhau ⇒ ghế phải xếp xen kẽ nam-nữ: 5 ghế lẻ 1 nhóm, 5 ghế chẵn 1 nhóm (2 cách chọn nhóm nào là nam). Với mỗi cách chia, ghế đối diện của 1 ghế lẻ luôn là ghế chẵn, nên điều kiện A-B đối diện tự động phù hợp giới tính. Số cách chọn ghế cho A trong 5 ghế nam: 5 cách, ghế của B (đối diện A) bị xác định duy nhất. Xếp 4 nam còn lại vào 4 ghế nam còn trống: \\(4!\\); xếp 4 nữ còn lại vào 4 ghế nữ còn trống: \\(4!\\). Số cách thuận lợi: \\( 2\\cdot5\\cdot4!\\cdot4! = 5760 \\). Xác suất \\( = \\dfrac{5760}{10!} = \\dfrac{1}{630} \\Rightarrow p=1,\\ q=630 \\Rightarrow S = 631 \\).',
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": 'de_tsa11_dd_01',
                "type": 'dragdrop',
                "content": ' Một con robot xuất phát từ gốc tọa độ O(0, 0) trên mặt phẳng Oxy, hướng theo chiều dương của trục Ox. Lập trình di chuyển của robot được thiết lập như sau: Bước 1: Tiến thẳng về phía trước 12 cm đến điểm A₁. Bước n (với n ≥ 2): Quay trái một góc 90°, sau đó tiến thẳng một đoạn bằng \\( \\dfrac{2}{3} \\) độ dài của đoạn đường di chuyển ngay trước đó để tới điểm Aₙ. Quá trình này lặp lại vô hạn lần và robot tiến dần đến một điểm tới hạn M(X; Y). Kéo và thả các kết quả sau vào ô tương ứng:',
                "image": 'https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/images/de_tsa11_cau4_robot.PNG',
                "options_pool": ['36', '108/13', '72/13', '24', '36/13'],
                "blanks": [
                    {"label": 'Tổng quãng đường robot di chuyển được sau vô hạn bước là (cm):', "answer": '36'},
                    {"label": 'Hoành độ X của điểm tới hạn M là:', "answer": '108/13'},
                    {"label": 'Tung độ Y của điểm tới hạn M là:', "answer": '72/13'},
                ],
                "points": 1,
                "explanation": "Độ dài các đoạn lập thành cấp số nhân \\( L_n = 12\\cdot(2/3)^{n-1} \\). Tổng quãng đường: \\( \\sum L_n = \\dfrac{12}{1-2/3} = 36 \\) cm. Hướng di chuyển lặp chu kỳ 4 (Đông, Bắc, Tây, Nam) do mỗi bước quay trái 90°. Hoành độ: \\( X = L_1 - L_3 + L_5 - \\cdots = 12\\left[1-(2/3)^2+(2/3)^4-\\cdots\\right] = 12\\cdot\\dfrac{1}{1+4/9} = 12\\cdot\\dfrac{9}{13} = \\dfrac{108}{13} \\). Tung độ: \\( Y = L_2 - L_4 + L_6 - \\cdots = 12\\cdot\\dfrac23\\cdot\\dfrac{9}{13} = \\dfrac{72}{13} \\).",
            },
        ],
    },
    {
        "id": 'de2',
        "name": 'Đề số 2 - Hình học & Xác suất',
        "description": '10 câu hỏi thiên về hình học không gian và xác suất thống kê.',
        "questions": [

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": 'de2_tf_03',
                "type": 'truefalse',
                "content": 'Cho hình chóp đều S.ABCD có \\( SA = 2 \\), \\( AB = 1 \\). Các nhận định sau đúng hay sai?',
                "statements": [
                    {"text": 'SA và CD không vuông góc nhau', "correct": True},
                    {"text": 'Góc giữa SA và CD là \\( 30^\\circ \\)', "correct": False},
                    {"text": 'Khoảng cách giữa SA và CD bằng 1', "correct": False},
                ],
                "points": 1,
                "explanation": 'CD ∥ AB nên góc(SA,CD) = góc(SA,AB) = \\( \\widehat{SAB} \\). Tam giác SAB có \\( SA=SB=2 \\), \\( AB=1 \\), \\( \\cos\\widehat{SAB}=\\dfrac{4+1-4}{2\\cdot2\\cdot1}=\\dfrac{1}{4}>0 \\) nên \\( \\widehat{SAB}\\ne90^\\circ \\) (mệnh đề 1 Đúng), \\( \\widehat{SAB}\\approx75.5^\\circ\\ne30^\\circ \\) (mệnh đề 2 Sai). \\( d(SA,CD)=\\sqrt{\\dfrac{14}{15}}\\approx0.966\\ne1 \\) (mệnh đề 3 Sai).',
            },
            {
                "id": 'de2_tf_04',
                "type": 'truefalse',
                "content": 'Trong không gian Oxyz, cho ba điểm \\( A(1;2;3) \\), \\( B(3;4;5) \\), \\( C(6;7;9) \\). Xét tính đúng/sai của các mệnh đề sau:',
                "statements": [
                    {"text": '\\( \\overrightarrow{AB} = (2; 2; 2) \\)', "correct": True},
                    {"text": 'Ba điểm A, B, C thẳng hàng', "correct": False},
                ],
                "points": 1,
                "explanation": '\\( \\overrightarrow{AB}=(2;2;2) \\) đúng theo định nghĩa toạ độ vector. \\( \\overrightarrow{AC}=(5;5;6) \\); tỉ lệ \\( \\dfrac{5}{2}=\\dfrac{5}{2}\\ne\\dfrac{6}{2} \\) nên \\( \\overrightarrow{AB}, \\overrightarrow{AC} \\) không cùng phương \\( \\Rightarrow \\) A, B, C không thẳng hàng.',
            },
            {
                "id": 'de2_tf_05',
                "type": 'truefalse',
                "content": 'Kim tự tháp Louvre có dạng hình chóp tứ giác đều, cao 20.6 mét, đáy mỗi cạnh 35 mét. Xét tính đúng/sai của các mệnh đề sau:',
                "statements": [
                    {"text": 'Khoảng cách giữa đỉnh và mặt đất bằng 20.6 m', "correct": True},
                    {"text": 'Cạnh bên của kim tự tháp vuông góc với mặt đất', "correct": False},
                    {"text": 'Đáy của kim tự tháp là hình vuông', "correct": True},
                ],
                "points": 1,
                "explanation": 'Khoảng cách đỉnh-đáy chính là chiều cao hình chóp = 20.6m (Đúng). Cạnh bên hình chóp đều tạo góc nhọn với đáy, không vuông góc (Sai). Đáy hình chóp tứ giác đều luôn là hình vuông (Đúng).',
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_06',
                "type": 'short',
                "content": 'Một hàng học sinh gồm 3 nam và 7 nữ được xếp thành 1 hàng ngang. Xác suất để không có bất kì 2 bạn nam nào đứng cạnh nhau (dạng phân số a/b):',
                "blanks": [
                    {"label": 'Xác suất =', "answers": ['7/15', '7 / 15']},
                ],
                "points": 1,
                "explanation": 'Xếp 7 nữ: 7! cách, tạo 8 khoảng trống. Xếp 3 nam vào 8 khoảng: A(8,3) cách. P = 7!·A(8,3)/10! = 7/15.',
            },
            {
                "id": 'de2_sh_07',
                "type": 'short',
                "content": 'Cho hình (H) giới hạn bởi \\( y = \\sqrt{4k^2-x^2} \\) \\( (k\\ge0) \\) và trục hoành. Thể tích khối tròn xoay khi quay (H) quanh Ox là V. Có bao nhiêu giá trị nguyên của k thoả \\( V < 6400\\pi \\)?',
                "blanks": [
                    {"label": 'Số giá trị nguyên', "answers": ['9']},
                ],
                "points": 1,
                "explanation": '(H) là nửa hình tròn bán kính \\( 2k \\), quay quanh Ox tạo khối cầu: \\( V=\\dfrac{4}{3}\\pi(2k)^3 \\). \\( V<6400\\pi \\Leftrightarrow k^3<600 \\Leftrightarrow k<8.43 \\). Với k nguyên, \\( k\\ge0 \\): \\( k\\in\\{0,...,8\\} \\Rightarrow \\) 9 giá trị.',
            },
            {
                "id": 'de2_sh_08',
                "type": 'short',
                "content": 'Cho tập A gồm các số có 3 chữ số tạo bởi {0,1,2,3,5}. Xác suất lấy được số có tổng các chữ số bằng 8 là a/b (tối giản). Tính 10a - b = ?',
                "blanks": [
                    {"label": '10a - b =', "answers": ['30']},
                ],
                "points": 1,
                "explanation": 'n(Ω)=4·5·5=100. Bộ tổng 8: (5,3,0)→4 số, (5,2,1)→6 số, (3,3,2)→3 số ⇒ 13 số. P=13/100 ⇒ a=13,b=100 ⇒ 10a-b=30.',
            },
            {
                "id": 'de2_sh_09',
                "type": 'short',
                "content": 'Cho tứ diện ABCD có AB, AC, AD đôi một vuông góc. Biết BD=BC=5, AC=4. M, N, P lần lượt là trung điểm BC, CD, BD. Thể tích tứ diện A.MNP bằng?',
                "blanks": [
                    {"label": 'Thể tích', "answers": ['2']},
                ],
                "points": 1,
                "explanation": 'AB=3, AD=4 (Pytago). V(ABCD)=(1/6)·3·4·4=8. (MNP) đồng dạng (BCD) tỉ số 1/2 nên diện tích bằng 1/4, chiều cao từ A không đổi ⇒ V(A.MNP)=8/4=2.',
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_02',
                "type": 'mc4',
                "content": 'Trong không gian Oxyz, có điểm \\( A(a,b,c) \\) và điểm \\( B(m,n,p) \\) di chuyển nhưng luôn thoả mãn: \\( a^2+b^2+c^2 = 9 \\) và \\( m^2+n^2+p^2 = 36 \\). Nhận định nào sau đây là SAI?',
                "options": {
                    'A': 'Điểm A thuộc một mặt cầu cố định.',
                    'B': 'Độ dài ngắn nhất của AB là 3.',
                    'C': 'Độ dài AB đạt cực tiểu \\( \\Leftrightarrow \\overrightarrow{OA} \\cdot \\overrightarrow{OB} = 36 \\).',
                    'D': 'Độ dài AB đạt cực tiểu \\( \\Leftrightarrow \\) A là trung điểm OB.',
                },
                "correct": 'C',
                "points": 1,
                "explanation": 'A thuộc mặt cầu tâm O bán kính \\( R_1=3 \\); B thuộc mặt cầu tâm O bán kính \\( R_2=6 \\). AB nhỏ nhất khi O, A, B thẳng hàng cùng chiều: \\( AB_{min} = R_2-R_1 = 3 \\) (B đúng), khi đó A là trung điểm OB (D đúng), A thuộc mặt cầu cố định (A đúng). \\( \\overrightarrow{OA} \\cdot \\overrightarrow{OB} = |OA||OB|\\cos 0^\\circ = 3\\cdot6 = 18 \\ne 36 \\) nên C sai.',
            },
            {
                "id": 'de2_mc_03',
                "type": 'mc4',
                "content": 'Cho mẫu A có phần tử lớn nhất là 378, nhỏ nhất là 310, trung bình 344, độ lệch chuẩn 12. Nếu mẫu B được tạo từ mẫu A bỏ đi 2 phần tử 378 và 310 thì nhận định nào sau đây đúng?',
                "options": {
                    'A': 'Mẫu B có trung bình lớn hơn A, độ lệch chuẩn lớn hơn A.',
                    'B': 'Mẫu B có trung bình bé hơn A, độ lệch chuẩn lớn hơn A.',
                    'C': 'Mẫu B có trung bình lớn hơn A, độ lệch chuẩn bé hơn A.',
                    'D': 'Mẫu B có trung bình bằng A, độ lệch chuẩn bé hơn A.',
                },
                "correct": 'D',
                "points": 1,
                "explanation": '\\( 378+310=688=2\\cdot344 \\) nên trung bình mẫu B vẫn bằng 344. Hai giá trị bị loại cách xa trung bình (34 đơn vị, lớn hơn nhiều so với độ lệch chuẩn gốc 12) nên loại chúng làm giảm độ phân tán \\( \\Rightarrow \\) độ lệch chuẩn mẫu B bé hơn. Đáp án D.',
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": 'de2_dd_01',
                "type": 'dragdrop',
                "content": "Cho lăng trụ đều ABC.A'B'C' có \\( AB = 4 \\), \\( AA' = 3 \\). Kéo và thả các phương án lựa chọn thích hợp vào từng ô trống.",
                "options_pool": ['12√3', '8√3', '4√3'],
                "blanks": [
                    {"label": "V(ABC.A'B'C') =", "answer": '12√3'},
                    {"label": "V(A.BCC'B') =", "answer": '8√3'},
                ],
                "points": 1,
                "explanation": "\\( S_{đáy}=\\dfrac{4^2\\sqrt3}{4}=4\\sqrt3 \\). \\( V_{lăng trụ}=4\\sqrt3\\cdot3=12\\sqrt3 \\). \\( V_{A.A'B'C'}=\\dfrac{1}{3}V_{lăng trụ}=4\\sqrt3 \\Rightarrow V_{A.BCC'B'}=12\\sqrt3-4\\sqrt3=8\\sqrt3 \\).",
            },
        ],
    },
    {
        "id": 'de3',
        "name": 'Đề số 3 - Giải tích & Đại số',
        "description": '10 câu hỏi thiên về hàm số, giới hạn, mũ-logarit.',
        "questions": [

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de3_mc_01',
                "type": 'mc4',
                "content": 'Cho hàm số \\( y = \\dfrac{1+x}{1-x} \\). Nhận xét nào sau đây đúng?',
                "options": {
                    'A': 'Đồ thị hàm có TCN \\( y = 1 \\), TCĐ \\( x = 1 \\)',
                    'B': 'Đồ thị hàm có TCN \\( y = -1 \\), TCĐ \\( x = 1 \\)',
                    'C': 'Đồ thị hàm có TCN \\( y = 1 \\), TCĐ \\( x = -1 \\)',
                    'D': 'Đồ thị hàm có TCN \\( y = -1 \\), TCĐ \\( x = -1 \\)',
                },
                "correct": 'B',
                "points": 1,
                "explanation": 'Viết lại \\( y = \\dfrac{x+1}{-x+1} \\). TCN: \\( \\lim_{x\\to\\pm\\infty} y = \\dfrac{1}{-1} = -1 \\) \\( \\Rightarrow \\) TCN: \\( y = -1 \\). TCĐ: mẫu \\( = 0 \\Leftrightarrow x = 1 \\) (tử tại \\( x=1 \\) khác 0) \\( \\Rightarrow \\) TCĐ: \\( x = 1 \\). Đáp án B.',
            },
            {
                "id": 'de3_mc_05',
                "type": 'mc4',
                "content": 'Tập xác định D của hàm số \\( y = \\dfrac{1}{\\sqrt{\\cos^2 x - \\sin^2 x}} \\) là?',
                "options": {
                    'A': '\\( D = \\mathbb{R} \\setminus \\left\\{ \\dfrac{\\pi}{4} + \\dfrac{k\\pi}{2}, k\\in\\mathbb{Z} \\right\\} \\)',
                    'B': '\\( D = \\mathbb{R} \\setminus \\left\\{ \\dfrac{\\pi}{4} + k\\pi, k\\in\\mathbb{Z} \\right\\} \\)',
                    'C': '\\( D = \\mathbb{R} \\setminus \\left\\{ \\dfrac{\\pi}{2} + \\dfrac{k\\pi}{2}, k\\in\\mathbb{Z} \\right\\} \\)',
                    'D': '\\( D = \\mathbb{R} \\setminus \\left\\{ \\dfrac{\\pi}{2} + k\\pi, k\\in\\mathbb{Z} \\right\\} \\)',
                },
                "correct": 'A',
                "points": 1,
                "explanation": '\\( \\cos^2 x - \\sin^2 x = \\cos 2x \\). Điều kiện: \\( \\cos 2x \\ne 0 \\Leftrightarrow 2x \\ne \\dfrac{\\pi}{2} + k\\pi \\Leftrightarrow x \\ne \\dfrac{\\pi}{4} + \\dfrac{k\\pi}{2} \\). Đáp án A.',
            },
            {
                "id": 'de3_mc_06',
                "type": 'mc4',
                "content": 'Với giá trị nào của m thì hàm số \\( y = mx^3 + x^2 + (m^2-6)x + 1 \\) đạt cực tiểu tại \\( x = 1 \\)?',
                "options": {
                    'A': '\\( m = -4 \\)',
                    'B': '\\( m = -2 \\)',
                    'C': '\\( m = 2 \\)',
                    'D': '\\( m = 1 \\)',
                },
                "correct": 'D',
                "points": 1,
                "explanation": "\\( y'=3mx^2+2x+m^2-6 \\); \\( y'(1)=0 \\Leftrightarrow m^2+3m-4=0 \\Leftrightarrow m=1 \\) hoặc \\( m=-4 \\). \\( y''=6mx+2 \\). Với \\( m=1 \\): \\( y''(1)=8>0 \\) (cực tiểu, thoả). Với \\( m=-4 \\): \\( y''(1)=-22<0 \\) (cực đại, loại). Đáp án D.",
            },
            {
                "id": 'de3_mc_04',
                "type": 'mc4',
                "content": 'Hệ số của số hạng có số mũ của x bằng số mũ của y trong khai triển \\( \\left(x^2 + \\dfrac{3y}{x}\\right)^{14} \\) là?',
                "options": {
                    'A': '\\( 14! \\times C_{14}^{7} \\)',
                    'B': '\\( 3^7 \\times C_{14}^{7} \\)',
                    'C': '\\( 3^{14} \\times C_{14}^{7} \\)',
                    'D': '\\( C_{14}^{7} \\)',
                },
                "correct": 'B',
                "points": 1,
                "explanation": 'Số hạng tổng quát: \\( T = C_{14}^{k}\\cdot3^k\\cdot x^{28-3k}\\cdot y^k \\). Cần \\( 28-3k=k \\Leftrightarrow k=7 \\). Hệ số cần tìm là \\( C_{14}^{7}\\cdot3^7 \\). Đáp án B.',
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": 'de3_tf_01',
                "type": 'truefalse',
                "content": 'Cho hàm số \\( y = f(x) = \\sqrt{1 + \\cos x} \\). Khi xét \\( x \\in (0, \\pi) \\), các mệnh đề dưới đây đúng hay sai?',
                "statements": [
                    {"text": 'Phương trình \\( \\sqrt{1+\\cos x} = \\cos\\dfrac{x}{2} \\) có nghiệm', "correct": False},
                    {"text": 'Phương trình \\( \\sqrt{1+\\cos x} = \\cos\\dfrac{x}{4} \\) có nghiệm', "correct": True},
                    {"text": 'Phương trình \\( \\sqrt{1+\\cos x} = \\cos\\dfrac{\\pi}{8} \\) có đúng 1 nghiệm', "correct": True},
                ],
                "points": 1,
                "explanation": '\\( 1+\\cos x = 2\\cos^2\\dfrac{x}{2} \\Rightarrow \\sqrt{1+\\cos x} = \\sqrt{2}\\cdot\\cos\\dfrac{x}{2} \\) (do \\( \\dfrac{x}{2}\\in(0,\\dfrac{\\pi}{2}) \\) nên \\( \\cos\\dfrac{x}{2}>0 \\)). (1) \\( \\sqrt{2}\\cos\\dfrac{x}{2}=\\cos\\dfrac{x}{2} \\Leftrightarrow \\cos\\dfrac{x}{2}=0 \\): vô nghiệm trên \\( (0,\\pi) \\Rightarrow \\) Sai. (2) Đặt \\( t=\\cos\\dfrac{x}{4}\\in(\\dfrac{\\sqrt2}{2},1) \\): \\( 2\\sqrt{2}t^2-t-\\sqrt{2}=0 \\) có nghiệm \\( t\\approx0.905 \\) thoả \\( \\Rightarrow \\) Đúng. (3) \\( \\cos\\dfrac{x}{2}=\\dfrac{\\cos(\\pi/8)}{\\sqrt2}\\approx0.653\\in(0,1) \\); \\( \\cos\\dfrac{x}{2} \\) nghịch biến toàn ánh trên \\( (0,\\pi) \\) nên có đúng 1 nghiệm \\( \\Rightarrow \\) Đúng.',
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de3_sh_01',
                "type": 'short',
                "content": 'Bất phương trình \\( (\\log_2 x)^2 + \\log_3\\dfrac{36}{x} \\le \\left(1 + \\log_3\\dfrac{36}{x}\\right)\\cdot\\log_2 x \\) có tập nghiệm \\( x \\in [a, b] \\). Giá trị của \\( a + \\dfrac{b}{2} \\) = ?',
                "blanks": [
                    {"label": 'a + b/2 =', "answers": ['4']},
                ],
                "points": 1,
                "explanation": 'Đặt \\( u=\\log_2 x, v=\\log_3\\dfrac{36}{x} \\). BPT \\( \\Leftrightarrow (u-1)(u-v)\\le0 \\). Giải 2 trường hợp được tập nghiệm \\( [2,4] \\Rightarrow a=2, b=4 \\Rightarrow a+\\dfrac{b}{2} = 2+2 = 4 \\).',
            },
            {
                "id": 'de3_sh_03',
                "type": 'short',
                "content": 'Cho hàm số \\( y = 4\\sin(x)\\cdot\\sin\\left(x + \\dfrac{\\pi}{2}\\right) \\). Giá trị lớn nhất và nhỏ nhất của y là:',
                "blanks": [
                    {"label": 'Giá trị lớn nhất', "answers": ['2']},
                    {"label": 'Giá trị nhỏ nhất', "answers": ['-2']},
                ],
                "points": 1,
                "explanation": '\\( \\sin\\left(x+\\dfrac{\\pi}{2}\\right)=\\cos x \\) nên \\( y=4\\sin x\\cdot\\cos x=2\\sin 2x \\). Vì \\( -1\\le\\sin 2x\\le1 \\) nên \\( -2\\le y\\le2 \\).',
            },
            {
                "id": 'de3_sh_04',
                "type": 'short',
                "content": "Cho hàm số \\( f(x) = (x + 10)^6 \\). Tính \\( f''(2) \\) = ?",
                "blanks": [
                    {"label": "f''(2) =", "answers": ['622080']},
                ],
                "points": 1,
                "explanation": "\\( f'(x)=6(x+10)^5 \\); \\( f''(x)=30(x+10)^4 \\). \\( f''(2)=30\\cdot12^4=30\\cdot20736=622080 \\).",
            },
            {
                "id": 'de3_sh_05',
                "type": 'short',
                "content": 'Tính giới hạn: \\( \\displaystyle\\lim_{x\\to0} \\dfrac{1 - \\cos 2x}{x} \\) = ?',
                "blanks": [
                    {"label": 'Kết quả', "answers": ['0']},
                ],
                "points": 1,
                "explanation": '\\( 1-\\cos 2x=2\\sin^2 x \\). Giới hạn \\( = \\lim \\dfrac{2\\sin^2 x}{x} = \\lim\\left(2\\sin x\\cdot\\dfrac{\\sin x}{x}\\right) = 2\\cdot0\\cdot1 = 0 \\).',
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": 'de3_dd_02',
                "type": 'dragdrop',
                "content": 'Cho các số thực \\( x, y, z \\ge 0 \\) thoả \\( 3^x + 9^y + 27^z = 11 \\). Kéo thả để hoàn thành kết luận về khoảng giá trị của z và giá trị nhỏ nhất của \\( x+2y+3z \\).',
                "options_pool": ['0', '2/3', '2', '9'],
                "blanks": [
                    {"label": 'Giá trị z thuộc đoạn [___ ;', "answer": '0'},
                    {"label": '___ ] (cận trên của z)', "answer": '2/3'},
                    {"label": 'min(x + 2y + 3z) =', "answer": '2'},
                ],
                "points": 1,
                "explanation": 'Với \\( A=3^x, B=9^y, C=27^z \\ge 1 \\), \\( A+B+C=11 \\): \\( C\\le9 \\Rightarrow z\\le\\dfrac{2}{3} \\), kết hợp \\( z\\ge0 \\Rightarrow z\\in\\left[0;\\dfrac{2}{3}\\right] \\). \\( 3^{x+2y+3z}=A\\cdot B\\cdot C \\), tích nhỏ nhất khi 2 trong 3 biến bằng 1: \\( \\min(ABC)=9 \\Rightarrow \\min P=2 \\).',
            },
        ],
    },
]


# 1b) CÂU HỎI THÊM QUA TRANG QUẢN TRỊ (/admin)
#     Mỗi câu hỏi thêm qua /admin được lưu kèm "exam_id" để biết nó
#     thuộc đề nào, trong data/extra_questions.json (chỉ 1 file, không
#     còn cần file map riêng nữa vì mỗi đề đã độc lập).
# =======================================================================
def _load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_extra_questions():
    """list các câu hỏi được thêm qua /admin, mỗi câu có kèm 'exam_id'."""
    return _load_json(EXTRA_Q_PATH, [])


def save_extra_questions(data):
    _save_json(EXTRA_Q_PATH, data)


def load_question_overrides():
    """dict: id câu hỏi -> nội dung câu hỏi đã được SỬA qua /admin (đè lên bản gốc/bản thêm)."""
    return _load_json(OVERRIDES_PATH, {})


def save_question_overrides(data):
    _save_json(OVERRIDES_PATH, data)


def load_exam_removed():
    """dict: exam_id -> list id câu hỏi GỐC (đã viết trong code của đề đó) bị ẩn khỏi đề
    (không xoá khỏi code, chỉ ẩn khi hiển thị)."""
    return _load_json(EXAM_REMOVED_PATH, {})


def save_exam_removed(data):
    _save_json(EXAM_REMOVED_PATH, data)


def is_extra_question(qid):
    """True nếu câu hỏi này được thêm qua /admin (không nằm sẵn trong code của đề)."""
    return any(q["id"] == qid for q in load_extra_questions())


def get_question_by_id(qid):
    overrides = load_question_overrides()
    if qid in overrides:
        return overrides[qid]
    for exam in EXAMS:
        for q in exam["questions"]:
            if q["id"] == qid:
                return q
    for q in load_extra_questions():
        if q["id"] == qid:
            return q
    return None


def get_exam_by_id(exam_id):
    for e in EXAMS:
        if e["id"] == exam_id:
            return e
    return None


def get_exam_questions(exam_id):
    """Câu hỏi của 1 đề = câu hỏi viết sẵn trong code CỦA RIÊNG ĐỀ ĐÓ
    (exam["questions"]) + câu hỏi thêm qua /admin cho đề đó - câu hỏi đã bị ẩn."""
    exam = get_exam_by_id(exam_id)
    if not exam:
        return []
    removed_ids = set(load_exam_removed().get(exam_id, []))
    base_ids = [q["id"] for q in exam["questions"] if q["id"] not in removed_ids]
    extra_ids = [q["id"] for q in load_extra_questions() if q.get("exam_id") == exam_id]
    all_ids = base_ids + extra_ids
    return [get_question_by_id(qid) for qid in all_ids if get_question_by_id(qid)]


# 2) DATABASE (SQLite) - lưu kết quả bài làm
# =======================================================================
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id TEXT PRIMARY KEY,
            exam_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            answers_json TEXT NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def student_required(view_func):
    """Chỉ yêu cầu học sinh đã NHẬP HỌ TÊN (không cần tài khoản/mật khẩu)."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("student_name"):
            return redirect(url_for("student_login"))
        return view_func(*args, **kwargs)
    return wrapper


# =======================================================================
# 3) CHẤM ĐIỂM
# =======================================================================
def normalize(s):
    if s is None:
        return ""
    return str(s).strip().lower().replace(" ", "")


def grade_question(question, submitted):
    qtype = question["type"]
    max_points = question.get("points", 1)

    if qtype == "mc4":
        chosen = submitted.get("choice") if submitted else None
        correct = question["correct"]
        is_correct = chosen == correct
        earned = max_points if is_correct else 0
        return earned, max_points, {"chosen": chosen, "correct": correct, "is_correct": is_correct}

    if qtype == "truefalse":
        statements = question["statements"]
        n = len(statements)
        per_stmt = max_points / n if n else 0
        earned = 0
        detail_statements = []
        for i, st in enumerate(statements):
            key = str(i)
            student_val = None
            if submitted and key in submitted:
                student_val = submitted[key] == "true"
            correct_val = st["correct"]
            is_correct = (student_val == correct_val) if student_val is not None else False
            if is_correct:
                earned += per_stmt
            detail_statements.append({
                "text": st["text"], "student": student_val,
                "correct": correct_val, "is_correct": is_correct,
            })
        return round(earned, 3), max_points, {"statements": detail_statements}

    if qtype in ("short", "dragdrop"):
        blanks = question["blanks"]
        n = len(blanks)
        per_blank = max_points / n if n else 0
        earned = 0
        detail_blanks = []
        for i, bl in enumerate(blanks):
            key = str(i)
            student_val = submitted.get(key, "") if submitted else ""
            if qtype == "short":
                accepted = [normalize(a) for a in bl.get("answers", [])]
                is_correct = normalize(student_val) in accepted
                correct_display = " / ".join(bl.get("answers", []))
            else:
                accepted = [normalize(bl.get("answer", ""))]
                is_correct = normalize(student_val) in accepted
                correct_display = bl.get("answer", "")
            if is_correct:
                earned += per_blank
            detail_blanks.append({
                "label": bl.get("label", ""), "student": student_val,
                "correct": correct_display, "is_correct": is_correct,
            })
        return round(earned, 3), max_points, {"blanks": detail_blanks}

    return 0, max_points, {}


def grade_exam(exam_id, form):
    questions = get_exam_questions(exam_id)
    total_earned = 0
    total_max = 0
    details = []
    answers_to_store = {}

    for q in questions:
        qid = q["id"]
        qtype = q["type"]

        if qtype == "mc4":
            submitted = {"choice": form.get(f"{qid}__choice")}
        elif qtype == "truefalse":
            submitted = {}
            for i in range(len(q["statements"])):
                val = form.get(f"{qid}__stmt_{i}")
                if val is not None:
                    submitted[str(i)] = val
        elif qtype in ("short", "dragdrop"):
            submitted = {}
            for i in range(len(q["blanks"])):
                val = form.get(f"{qid}__blank_{i}")
                if val is not None:
                    submitted[str(i)] = val
        else:
            submitted = {}

        earned, max_points, detail = grade_question(q, submitted)
        total_earned += earned
        total_max += max_points
        details.append({
            "id": qid, "type": qtype, "content": q["content"], "explanation": q["explanation"],
            "image": q.get("image"),
            "earned": round(earned, 2), "max": max_points, "detail": detail,
        })
        answers_to_store[qid] = submitted

    return total_earned, total_max, details, answers_to_store


# =======================================================================
# 4) GIAO DIỆN (HTML nhúng trong Python, dùng render_template_string)
#    Tông màu ĐỎ theo nhận diện kỳ thi TSA.
# =======================================================================
BASE_CSS = """
:root {
  --tsa-red: #c8102e;
  --tsa-red-dark: #8b0000;
  --tsa-red-darker: #5c0011;
  --tsa-red-light: #fdecec;
  --tsa-red-soft: #fbd5d8;
}
body { background-color:#fdf5f5; font-family:"Segoe UI",Roboto,Arial,sans-serif; }
.navbar-custom { background: linear-gradient(90deg,var(--tsa-red-darker),var(--tsa-red)); }
.navbar-custom .navbar-brand { color:#fff !important; }

/* Nút & huy hiệu chuyển sang màu đỏ chủ đạo TSA */
.btn-primary, .btn-tsa {
  background-color: var(--tsa-red) !important;
  border-color: var(--tsa-red) !important;
  color:#fff !important;
}
.btn-primary:hover, .btn-primary:focus, .btn-tsa:hover {
  background-color: var(--tsa-red-dark) !important;
  border-color: var(--tsa-red-dark) !important;
}
.btn-outline-primary {
  color: var(--tsa-red) !important; border-color: var(--tsa-red) !important;
}
.btn-outline-primary:hover { background-color: var(--tsa-red) !important; color:#fff !important; }
.text-primary { color: var(--tsa-red) !important; }
.bg-primary { background-color: var(--tsa-red) !important; }

.exam-card { border:none; border-top:4px solid var(--tsa-red); border-radius:14px; transition:transform .15s ease; }
.exam-card:hover { transform: translateY(-4px); box-shadow:0 10px 24px rgba(200,16,46,.18); }
.question-card { border-radius:14px; border-left:5px solid var(--tsa-red); }
.question-content { white-space: pre-line; font-size:1.02rem; }
.question-image { max-width:100%; border-radius:10px; border:1px solid #f1c3c8; margin:12px 0; }
.option-row { padding:8px 12px; border-radius:8px; margin-bottom:6px; }
.option-row:hover { background-color: var(--tsa-red-light); }
.dragdrop-pool { display:flex; flex-wrap:wrap; gap:8px; padding:10px; background:#fff5f5; border-radius:10px; }
.chip { display:inline-block; padding:6px 14px; background: var(--tsa-red-soft); border:1px solid #f0a3ac;
        border-radius:20px; cursor:pointer; user-select:none; font-weight:600; color:var(--tsa-red-darker); }
.chip-selected { background: var(--tsa-red); color:#fff; border-color: var(--tsa-red-dark); }
.drop-zone { display:inline-block; min-width:100px; padding:6px 14px; border:2px dashed #d68a91;
             border-radius:8px; cursor:pointer; color:#94636a; font-style:italic; }
.drop-zone-filled { border-style:solid; border-color: var(--tsa-red); background: var(--tsa-red-light);
                     color: var(--tsa-red-darker); font-style:normal; font-weight:600; }
.score-card { border-radius:18px; border:none; background:linear-gradient(135deg,var(--tsa-red-darker),var(--tsa-red)); color:#fff; }
.score-big { font-size:3.5rem; font-weight:800; }
.explanation-box { background:#fffbeb; border-left:4px solid #f59e0b; padding:12px 16px;
                    border-radius:8px; font-size:.95rem; }
.admin-box { border-radius:14px; border-top:4px solid var(--tsa-red); }
.badge-tsa { background-color: var(--tsa-red) !important; }
.timer-warning { background-color: var(--tsa-red-darker) !important; animation: tsa-blink 1s infinite; }
@keyframes tsa-blink { 0%,100% { opacity:1; } 50% { opacity:.55; } }
/* MathJax: căn giữa công thức khối, không phá dòng chữ thường */
mjx-container[display="true"] { margin: 8px 0 !important; }
nav.navbar a.nav-link { color:#ffe3e5 !important; }
nav.navbar a.nav-link:hover { color:#fff !important; }
"""

BASE_HEAD = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>""" + BASE_CSS + """</style>
<!-- MathJax: cho phép gõ công thức Toán bằng LaTeX trong nội dung câu hỏi,
     dùng \\( ... \\) hoặc $...$ cho công thức trên dòng, \\[ ... \\] hoặc $$...$$ cho công thức khối -->
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
<nav class="navbar navbar-dark navbar-custom mb-4">
  <div class="container">
    <a class="navbar-brand fw-bold" href="{{ url_for('index') }}">📕 Thi thử TSA - Toán Thầy Tùng</a>
    {% if session.get('student_name') %}
    <span class="navbar-text small text-white-50 me-3">Xin chào, {{ session.get('student_name') }}</span>
    <a class="nav-link small" href="{{ url_for('student_logout') }}">Đổi tên khác</a>
    {% endif %}
  </div>
</nav>
<div class="container pb-5">
"""

BASE_FOOT = """
</div>
<footer class="text-center text-muted py-4 small">
  Ứng dụng luyện thi TSA
</footer>
</body>
</html>
"""

TPL_INDEX = BASE_HEAD + """
<div class="row justify-content-center">
  <div class="col-lg-9">
    <div class="text-center mb-4">
      <h2 class="fw-bold" style="color:var(--tsa-red-darker);">Chọn đề thi để bắt đầu</h2>
      <p class="text-muted">Xin chào <strong>{{ student_name }}</strong> - chọn một đề bên dưới rồi bấm "Bắt đầu làm bài".</p>
    </div>

    <div class="row g-4">
      {% for exam in exams %}
      <div class="col-md-4">
        <div class="card h-100 shadow-sm exam-card">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title fw-bold">{{ exam.name }}</h5>
            <p class="card-text text-muted flex-grow-1">{{ exam.description }}</p>
            <p class="text-muted small mb-3">{{ exam.total_questions }} câu hỏi</p>
            <a href="{{ url_for('exam_page', exam_id=exam.id) }}" class="btn btn-tsa">Bắt đầu làm bài</a>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</div>
""" + BASE_FOOT

TPL_EXAM = BASE_HEAD + """
<div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
  <div>
    <h3 class="fw-bold mb-0">{{ exam.name }}</h3>
    <div class="text-muted">Học sinh: <strong>{{ student_name }}</strong> &middot; {{ questions|length }} câu hỏi</div>
  </div>
  <div id="timer" class="badge badge-tsa fs-6 px-3 py-2">⏱ 60:00</div>
</div>

<form id="exam-form" method="POST" action="{{ url_for('submit_exam', exam_id=exam.id) }}">

{% for q in questions %}
<div class="card question-card shadow-sm mb-4">
  <div class="card-body">
    <h6 class="fw-bold mb-3">Câu {{ loop.index }}
      <span class="badge bg-secondary-subtle text-dark ms-2">
        {% if q.type == 'mc4' %}Trắc nghiệm 4 lựa chọn
        {% elif q.type == 'truefalse' %}Đúng / Sai
        {% elif q.type == 'short' %}Trả lời ngắn
        {% elif q.type == 'dragdrop' %}Kéo thả
        {% endif %}
      </span>
    </h6>
    <p class="question-content">{{ q.content }}</p>
    {% if q.image %}
      <img src="{{ q.image }}" alt="Hình minh hoạ câu {{ loop.index }}" class="question-image">
    {% endif %}

    {% if q.type == 'mc4' %}
      {% for key, opt in q.options.items() %}
      <div class="form-check option-row">
        <input class="form-check-input" type="radio" name="{{ q.id }}__choice" id="{{ q.id }}_{{ key }}" value="{{ key }}">
        <label class="form-check-label" for="{{ q.id }}_{{ key }}"><strong>{{ key }}.</strong> {{ opt }}</label>
      </div>
      {% endfor %}
    {% endif %}

    {% if q.type == 'truefalse' %}
      <table class="table table-bordered align-middle">
        <thead class="table-light">
          <tr><th>Mệnh đề</th><th class="text-center" style="width:90px;">Đúng</th><th class="text-center" style="width:90px;">Sai</th></tr>
        </thead>
        <tbody>
        {% for st in q.statements %}
          <tr>
            <td>{{ loop.index }}. {{ st.text }}</td>
            <td class="text-center"><input type="radio" name="{{ q.id }}__stmt_{{ loop.index0 }}" value="true"></td>
            <td class="text-center"><input type="radio" name="{{ q.id }}__stmt_{{ loop.index0 }}" value="false"></td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    {% endif %}

    {% if q.type == 'short' %}
      <div class="row g-3">
        {% for bl in q.blanks %}
        <div class="col-md-6">
          <label class="form-label small text-muted">{{ bl.label }}</label>
          <input type="text" class="form-control" name="{{ q.id }}__blank_{{ loop.index0 }}" placeholder="Nhập câu trả lời">
        </div>
        {% endfor %}
      </div>
    {% endif %}

    {% if q.type == 'dragdrop' %}
      <div class="dragdrop-pool mb-3" data-qid="{{ q.id }}">
        {% for opt in q.options_pool %}
        <span class="chip" draggable="true" data-value="{{ opt }}">{{ opt }}</span>
        {% endfor %}
      </div>
      <div class="dragdrop-blanks">
        {% for bl in q.blanks %}
        <div class="dd-blank-row mb-2">
          <span class="me-2">{{ bl.label }}</span>
          <span class="drop-zone" data-qid="{{ q.id }}" data-index="{{ loop.index0 }}">Thả đáp án vào đây</span>
          <input type="hidden" name="{{ q.id }}__blank_{{ loop.index0 }}" class="dd-hidden-input">
        </div>
        {% endfor %}
      </div>
      <div class="form-text">Bấm chọn 1 đáp án ở trên rồi bấm vào ô trống để điền (hoặc kéo thả trên máy tính).</div>
    {% endif %}

  </div>
</div>
{% endfor %}

<div class="text-center mb-5">
  <button type="submit" class="btn btn-tsa btn-lg px-5" onclick="return confirm('Bạn có chắc chắn muốn nộp bài không?');">Nộp bài</button>
</div>
</form>

<script>
// Đồng hồ đếm NGƯỢC 60 phút theo đúng thời gian làm bài thi chính thức TSA
// (đề thi thật gồm 40 câu / 60 phút; đề luyện ở đây có thể ít câu hơn nhưng
// vẫn giữ đúng 60 phút để học sinh quen áp lực thời gian thật).
let secondsLeft = 60 * 60;
const timerEl = document.getElementById('timer');
let timerInterval = null;

function renderTimer() {
  const m = String(Math.floor(secondsLeft / 60)).padStart(2, '0');
  const s = String(secondsLeft % 60).padStart(2, '0');
  timerEl.textContent = `⏱ ${m}:${s}`;
  if (secondsLeft <= 300) {
    timerEl.classList.add('timer-warning');
  }
}
renderTimer();

timerInterval = setInterval(() => {
  secondsLeft--;
  if (secondsLeft <= 0) {
    clearInterval(timerInterval);
    secondsLeft = 0;
    renderTimer();
    alert('Đã hết 60 phút làm bài! Hệ thống sẽ tự động nộp bài của bạn.');
    document.getElementById('exam-form').submit();
    return;
  }
  renderTimer();
}, 1000);

let selectedChip = null;
document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    document.querySelectorAll('.chip').forEach(c => c.classList.remove('chip-selected'));
    if (selectedChip === chip) { selectedChip = null; return; }
    selectedChip = chip;
    chip.classList.add('chip-selected');
  });
  chip.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('text/plain', chip.getAttribute('data-value'));
  });
});

document.querySelectorAll('.drop-zone').forEach(zone => {
  zone.addEventListener('click', () => {
    if (!selectedChip) return;
    fillBlank(zone, selectedChip.getAttribute('data-value'));
    selectedChip.classList.remove('chip-selected');
    selectedChip = null;
  });
  zone.addEventListener('dragover', (e) => e.preventDefault());
  zone.addEventListener('drop', (e) => {
    e.preventDefault();
    const value = e.dataTransfer.getData('text/plain');
    fillBlank(zone, value);
  });
});

function fillBlank(zone, value) {
  zone.textContent = value;
  zone.classList.add('drop-zone-filled');
  const hiddenInput = zone.nextElementSibling;
  if (hiddenInput && hiddenInput.classList.contains('dd-hidden-input')) {
    hiddenInput.value = value;
  }
}
</script>
""" + BASE_FOOT

TPL_RESULT = BASE_HEAD + """
<div class="text-center mb-4">
  <h3 class="fw-bold">Kết quả bài thi</h3>
  <div class="text-muted">{{ exam.name }} &middot; Học sinh: <strong>{{ student_name }}</strong></div>
</div>

<div class="row justify-content-center mb-5">
  <div class="col-md-5">
    <div class="card score-card shadow-sm text-center">
      <div class="card-body">
        <div class="score-big">{{ score_10 }}</div>
        <div class="text-muted-light">/ 10 điểm</div>
        <div class="mt-2 small">({{ score }} / {{ max_score }} điểm thô)</div>
      </div>
    </div>
  </div>
</div>

<h5 class="fw-bold mb-3">Đáp án chi tiết từng câu</h5>

{% for d in details %}
<div class="card question-card shadow-sm mb-4 {{ 'border-success' if d.earned == d.max else ('border-warning' if d.earned > 0 else 'border-danger') }}">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-start flex-wrap gap-2">
      <h6 class="fw-bold">Câu {{ loop.index }}</h6>
      <span class="badge {{ 'bg-success' if d.earned == d.max else ('bg-warning text-dark' if d.earned > 0 else 'bg-danger') }}">
        {{ d.earned }} / {{ d.max }} điểm
      </span>
    </div>
    <p class="question-content">{{ d.content }}</p>
    {% if d.image %}
      <img src="{{ d.image }}" alt="Hình minh hoạ câu {{ loop.index }}" class="question-image">
    {% endif %}

    {% if d.type == 'mc4' %}
      <p class="mb-1">
        Bạn chọn: <strong>{{ d.detail.chosen or '(không chọn)' }}</strong>
        &middot; Đáp án đúng: <strong class="text-success">{{ d.detail.correct }}</strong>
      </p>
    {% endif %}

    {% if d.type == 'truefalse' %}
      <table class="table table-sm table-bordered">
        <thead class="table-light"><tr><th>Mệnh đề</th><th>Bạn chọn</th><th>Đáp án đúng</th><th></th></tr></thead>
        <tbody>
        {% for st in d.detail.statements %}
          <tr class="{{ 'table-success' if st.is_correct else 'table-danger' }}">
            <td>{{ st.text }}</td>
            <td>{{ 'Đúng' if st.student == true else ('Sai' if st.student == false else '(bỏ trống)') }}</td>
            <td>{{ 'Đúng' if st.correct else 'Sai' }}</td>
            <td>{{ '✅' if st.is_correct else '❌' }}</td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    {% endif %}

    {% if d.type in ('short', 'dragdrop') %}
      <table class="table table-sm table-bordered">
        <thead class="table-light"><tr><th>Ô trống</th><th>Bạn trả lời</th><th>Đáp án đúng</th><th></th></tr></thead>
        <tbody>
        {% for bl in d.detail.blanks %}
          <tr class="{{ 'table-success' if bl.is_correct else 'table-danger' }}">
            <td>{{ bl.label }}</td>
            <td>{{ bl.student or '(bỏ trống)' }}</td>
            <td>{{ bl.correct }}</td>
            <td>{{ '✅' if bl.is_correct else '❌' }}</td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
    {% endif %}

    <div class="explanation-box mt-3">
      <strong>Lời giải chi tiết:</strong>
      <p class="mb-0">{{ d.explanation }}</p>
    </div>
  </div>
</div>
{% endfor %}

<div class="text-center mb-5">
  <a href="{{ url_for('index') }}" class="btn btn-outline-primary">← Quay về trang chọn đề</a>
</div>
""" + BASE_FOOT

TPL_LOGIN = BASE_HEAD + """
<div class="row justify-content-center">
  <div class="col-md-5">
    <div class="card shadow-sm admin-box">
      <div class="card-body">
        <h5 class="fw-bold mb-3">Nhập họ tên để bắt đầu làm bài</h5>
        <p class="text-muted small">Không cần tài khoản - chỉ cần nhập họ tên là có thể vào thi ngay.</p>
        {% if error %}<div class="alert alert-danger py-2">{{ error }}</div>{% endif %}
        <form method="POST">
          <label class="form-label">Họ và tên</label>
          <input type="text" name="full_name" class="form-control mb-3" autofocus required>
          <button type="submit" class="btn btn-tsa w-100">Bắt đầu</button>
        </form>
      </div>
    </div>
  </div>
</div>
""" + BASE_FOOT

TPL_LOGIN_BLOCKED = BASE_HEAD + """
<div class="row justify-content-center">
  <div class="col-md-5">
    <div class="card shadow-sm admin-box">
      <div class="card-body text-center">
        <h5 class="fw-bold mb-3">Cần đăng nhập trên focusedu.com.vn</h5>
        <p class="text-muted small">
          Bạn cần đăng nhập tài khoản trên website chính trước, sau đó vào lại
          mục "Thi thử TSA" để bắt đầu làm bài.
        </p>
        <a href="https://focusedu.com.vn/wp-login.php" class="btn btn-tsa w-100 mt-2">
          Đăng nhập ngay
        </a>
      </div>
    </div>
  </div>
</div>
""" + BASE_FOOT

TPL_ADMIN_LOGIN = BASE_HEAD + """
<div class="row justify-content-center">
  <div class="col-md-5">
    <div class="card shadow-sm admin-box">
      <div class="card-body">
        <h5 class="fw-bold mb-3">Đăng nhập quản trị</h5>
        {% if error %}<div class="alert alert-danger py-2">{{ error }}</div>{% endif %}
        <form method="POST">
          <label class="form-label">Mật khẩu quản trị</label>
          <input type="password" name="password" class="form-control mb-3" autofocus required>
          <button type="submit" class="btn btn-tsa w-100">Đăng nhập</button>
        </form>
      </div>
    </div>
  </div>
</div>
""" + BASE_FOOT

TPL_ADMIN_PANEL = BASE_HEAD + """
<div class="d-flex justify-content-between align-items-center mb-4">
  <h3 class="fw-bold mb-0">Quản trị đề thi</h3>
  <div>
    <a href="{{ url_for('admin_logout') }}" class="btn btn-outline-secondary btn-sm">Đăng xuất</a>
  </div>
</div>

{% if success %}<div class="alert alert-success">{{ success }}</div>{% endif %}
{% if error %}<div class="alert alert-danger">{{ error }}</div>{% endif %}

<div class="card shadow-sm admin-box mb-4">
  <div class="card-body">
    <h5 class="fw-bold mb-3">Thêm câu hỏi mới vào cuối một đề</h5>
    <p class="text-muted small">
      Nội dung câu hỏi và lời giải hỗ trợ công thức Toán LaTeX: dùng
      <code>\\( ... \\)</code> cho công thức trên dòng hoặc <code>\\[ ... \\]</code> cho công thức khối.
      Có thể tải ảnh minh hoạ (hình vẽ, biểu đồ) hoặc dán link ảnh ngoài.
    </p>
    <form method="POST" action="{{ url_for('admin_add_question') }}" enctype="multipart/form-data">
      <div class="row g-3 mb-2">
        <div class="col-md-6">
          <label class="form-label fw-semibold">Thêm vào đề</label>
          <select name="exam_id" class="form-select" required>
            {% for exam in exams %}
            <option value="{{ exam.id }}">{{ exam.name }} ({{ exam.total_questions }} câu hiện tại)</option>
            {% endfor %}
          </select>
        </div>
        <div class="col-md-6">
          <label class="form-label fw-semibold">Dạng câu hỏi</label>
          <select name="qtype" id="qtype-select" class="form-select" required>
            <option value="mc4">Trắc nghiệm 4 lựa chọn</option>
            <option value="truefalse">Đúng / Sai (nhiều mệnh đề)</option>
            <option value="short">Trả lời ngắn</option>
            <option value="dragdrop">Kéo thả</option>
          </select>
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Nội dung câu hỏi</label>
        <textarea name="content" class="form-control" rows="3" required
          placeholder="Ví dụ: Tính đạo hàm của hàm số \\( y = x^3 + 2x \\)"></textarea>
      </div>

      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <label class="form-label fw-semibold">Ảnh minh hoạ - tải lên (không bắt buộc)</label>
          <input type="file" name="image_file" class="form-control" accept="image/*">
        </div>
        <div class="col-md-6">
          <label class="form-label fw-semibold">... hoặc dán link ảnh ngoài</label>
          <input type="url" name="image_url" class="form-control" placeholder="https://...">
        </div>
      </div>

      <!-- mc4 -->
      <div class="qtype-block" data-type="mc4">
        <label class="form-label fw-semibold">4 phương án</label>
        <div class="row g-2 mb-2">
          <div class="col-md-6"><div class="input-group"><span class="input-group-text">A</span>
            <input type="text" name="opt_A" class="form-control"></div></div>
          <div class="col-md-6"><div class="input-group"><span class="input-group-text">B</span>
            <input type="text" name="opt_B" class="form-control"></div></div>
          <div class="col-md-6"><div class="input-group"><span class="input-group-text">C</span>
            <input type="text" name="opt_C" class="form-control"></div></div>
          <div class="col-md-6"><div class="input-group"><span class="input-group-text">D</span>
            <input type="text" name="opt_D" class="form-control"></div></div>
        </div>
        <label class="form-label fw-semibold">Đáp án đúng</label>
        <select name="mc4_correct" class="form-select" style="max-width:150px;">
          <option value="A">A</option><option value="B">B</option>
          <option value="C">C</option><option value="D">D</option>
        </select>
      </div>

      <!-- truefalse -->
      <div class="qtype-block" data-type="truefalse" style="display:none;">
        <label class="form-label fw-semibold">Các mệnh đề (bỏ trống dòng nào không dùng, tối đa 5)</label>
        {% for i in range(5) %}
        <div class="row g-2 mb-2 align-items-center">
          <div class="col-md-9"><input type="text" name="tf_text_{{ i }}" class="form-control" placeholder="Mệnh đề {{ i+1 }}"></div>
          <div class="col-md-3">
            <select name="tf_correct_{{ i }}" class="form-select">
              <option value="">-- chưa dùng --</option>
              <option value="true">Đúng</option>
              <option value="false">Sai</option>
            </select>
          </div>
        </div>
        {% endfor %}
      </div>

      <!-- short -->
      <div class="qtype-block" data-type="short" style="display:none;">
        <label class="form-label fw-semibold">Các ô trả lời ngắn (bỏ trống dòng nào không dùng, tối đa 4)</label>
        {% for i in range(4) %}
        <div class="row g-2 mb-2">
          <div class="col-md-5"><input type="text" name="sh_label_{{ i }}" class="form-control" placeholder="Nhãn ô {{ i+1 }}, ví dụ: Kết quả ="></div>
          <div class="col-md-7"><input type="text" name="sh_answers_{{ i }}" class="form-control" placeholder="Đáp án đúng (nếu có nhiều cách viết, cách nhau bằng dấu ;)"></div>
        </div>
        {% endfor %}
      </div>

      <!-- dragdrop -->
      <div class="qtype-block" data-type="dragdrop" style="display:none;">
        <label class="form-label fw-semibold">Danh sách đáp án để kéo thả (cách nhau bằng dấu ;)</label>
        <input type="text" name="dd_pool" class="form-control mb-2" placeholder="12√3; 8√3; 4√3">
        <label class="form-label fw-semibold">Các ô trống (bỏ trống dòng nào không dùng, tối đa 4)</label>
        {% for i in range(4) %}
        <div class="row g-2 mb-2">
          <div class="col-md-5"><input type="text" name="dd_label_{{ i }}" class="form-control" placeholder="Nhãn ô {{ i+1 }}"></div>
          <div class="col-md-7"><input type="text" name="dd_answer_{{ i }}" class="form-control" placeholder="Đáp án đúng của ô này"></div>
        </div>
        {% endfor %}
      </div>

      <div class="row g-3 my-2">
        <div class="col-md-3">
          <label class="form-label fw-semibold">Điểm câu này</label>
          <input type="number" name="points" class="form-control" value="1" min="1" step="1">
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Lời giải chi tiết</label>
        <textarea name="explanation" class="form-control" rows="3" required></textarea>
      </div>

      <button type="submit" class="btn btn-tsa px-4">Thêm câu hỏi vào đề</button>
    </form>
  </div>
</div>

<div class="card shadow-sm admin-box">
  <div class="card-body">
    <h5 class="fw-bold mb-3">Các đề hiện có</h5>
    <table class="table table-bordered align-middle">
      <thead class="table-light"><tr><th>Đề</th><th>Số câu gốc</th><th>Số câu thêm qua quản trị</th><th>Tổng</th><th>Câu hỏi</th></tr></thead>
      <tbody>
      {% for exam in exams %}
        <tr>
          <td>{{ exam.name }}</td>
          <td>{{ exam.base_count }}</td>
          <td>{{ exam.extra_count }}</td>
          <td class="fw-bold">{{ exam.total_questions }}</td>
          <td><a href="{{ url_for('admin_exam_questions', exam_id=exam.id) }}" class="btn btn-sm btn-outline-primary">Sửa / Xoá câu hỏi</a></td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<script>
const qtypeSelect = document.getElementById('qtype-select');
function refreshBlocks() {
  document.querySelectorAll('.qtype-block').forEach(block => {
    block.style.display = (block.getAttribute('data-type') === qtypeSelect.value) ? 'block' : 'none';
  });
}
qtypeSelect.addEventListener('change', refreshBlocks);
refreshBlocks();
</script>
""" + BASE_FOOT

TPL_ADMIN_EXAM_QUESTIONS = BASE_HEAD + """
<div class="d-flex justify-content-between align-items-center mb-4">
  <h3 class="fw-bold mb-0">Câu hỏi trong "{{ exam.name }}"</h3>
  <a href="{{ url_for('admin_panel') }}" class="btn btn-outline-secondary btn-sm">← Về trang quản trị</a>
</div>

{% if success %}<div class="alert alert-success">{{ success }}</div>{% endif %}
{% if error %}<div class="alert alert-danger">{{ error }}</div>{% endif %}

<div class="card shadow-sm admin-box">
  <div class="card-body">
    <p class="text-muted small">
      Câu hỏi <strong>Gốc</strong> (có sẵn trong code) khi bấm Xoá sẽ chỉ bị <strong>ẩn khỏi riêng đề này</strong>
      (không ảnh hưởng tới các đề khác đang dùng chung câu đó, và không đụng tới code).
      Câu hỏi <strong>Thêm qua QT</strong> khi bấm Xoá sẽ bị xoá hẳn khỏi hệ thống.
    </p>
    <table class="table table-bordered align-middle">
      <thead class="table-light">
        <tr>
          <th style="width:40px;">STT</th>
          <th>Nội dung</th>
          <th style="width:120px;">Dạng</th>
          <th style="width:110px;">Nguồn</th>
          <th style="width:190px;">Hành động</th>
        </tr>
      </thead>
      <tbody>
      {% for q in questions %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>
            {{ q.content|truncate(110) }}
            {% if q.is_edited %}<span class="badge bg-warning text-dark ms-1">đã sửa</span>{% endif %}
          </td>
          <td>{{ {"mc4": "Trắc nghiệm", "truefalse": "Đúng/Sai", "short": "Trả lời ngắn", "dragdrop": "Kéo thả"}[q.type] }}</td>
          <td>{{ "Thêm qua QT" if q.is_extra else "Gốc" }}</td>
          <td>
            <a href="{{ url_for('admin_edit_question', qid=q.id, exam_id=exam.id) }}" class="btn btn-sm btn-outline-primary">Sửa</a>
            <form method="POST" action="{{ url_for('admin_remove_question', exam_id=exam.id, qid=q.id) }}"
                  class="d-inline" onsubmit="return confirm('Xoá câu hỏi này khỏi đề?');">
              <button type="submit" class="btn btn-sm btn-outline-danger">Xoá</button>
            </form>
          </td>
        </tr>
      {% else %}
        <tr><td colspan="5" class="text-center text-muted">Đề này chưa có câu hỏi nào.</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>
""" + BASE_FOOT

TPL_EDIT_QUESTION = BASE_HEAD + """
<div class="d-flex justify-content-between align-items-center mb-4">
  <h3 class="fw-bold mb-0">Sửa câu hỏi</h3>
  <a href="{{ url_for('admin_exam_questions', exam_id=exam_id) }}" class="btn btn-outline-secondary btn-sm">← Quay lại danh sách</a>
</div>

{% if error %}<div class="alert alert-danger">{{ error }}</div>{% endif %}

<div class="card shadow-sm admin-box">
  <div class="card-body">
    <p class="text-muted small">
      Dạng câu hỏi hiện tại: <strong>{{ {"mc4": "Trắc nghiệm 4 lựa chọn", "truefalse": "Đúng/Sai", "short": "Trả lời ngắn", "dragdrop": "Kéo thả"}[question.type] }}</strong>
      (không thể đổi dạng khi sửa - nếu muốn đổi dạng, hãy xoá câu này rồi thêm câu mới).
      Hỗ trợ công thức LaTeX <code>\\( ... \\)</code> (trên dòng) hoặc <code>\\[ ... \\]</code> (khối).
    </p>
    <form method="POST" enctype="multipart/form-data">
      <input type="hidden" name="qtype" value="{{ question.type }}">

      <div class="mb-3">
        <label class="form-label fw-semibold">Nội dung câu hỏi</label>
        <textarea name="content" class="form-control" rows="3" required>{{ question.content }}</textarea>
      </div>

      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <label class="form-label fw-semibold">Đổi ảnh minh hoạ - tải ảnh khác lên (không bắt buộc)</label>
          <input type="file" name="image_file" class="form-control" accept="image/*">
          {% if question.image %}
          <div class="form-text">Ảnh hiện tại: <a href="{{ question.image }}" target="_blank">xem ảnh</a> (bỏ trống để giữ nguyên)</div>
          {% endif %}
        </div>
        <div class="col-md-6">
          <label class="form-label fw-semibold">... hoặc sửa link ảnh ngoài</label>
          <input type="url" name="image_url" class="form-control" value="{{ question.image or '' }}">
        </div>
      </div>

      {% if question.type == "mc4" %}
      <label class="form-label fw-semibold">4 phương án</label>
      <div class="row g-2 mb-2">
        <div class="col-md-6"><div class="input-group"><span class="input-group-text">A</span>
          <input type="text" name="opt_A" class="form-control" value="{{ question.options.A }}"></div></div>
        <div class="col-md-6"><div class="input-group"><span class="input-group-text">B</span>
          <input type="text" name="opt_B" class="form-control" value="{{ question.options.B }}"></div></div>
        <div class="col-md-6"><div class="input-group"><span class="input-group-text">C</span>
          <input type="text" name="opt_C" class="form-control" value="{{ question.options.C }}"></div></div>
        <div class="col-md-6"><div class="input-group"><span class="input-group-text">D</span>
          <input type="text" name="opt_D" class="form-control" value="{{ question.options.D }}"></div></div>
      </div>
      <label class="form-label fw-semibold">Đáp án đúng</label>
      <select name="mc4_correct" class="form-select" style="max-width:150px;">
        {% for letter in ["A", "B", "C", "D"] %}
        <option value="{{ letter }}" {{ "selected" if question.correct == letter else "" }}>{{ letter }}</option>
        {% endfor %}
      </select>

      {% elif question.type == "truefalse" %}
      <label class="form-label fw-semibold">Các mệnh đề (bỏ trống dòng nào không dùng, tối đa 5)</label>
      {% for i in range(5) %}
      {% set st = question.statements[i] if i < question.statements|length else None %}
      <div class="row g-2 mb-2 align-items-center">
        <div class="col-md-9"><input type="text" name="tf_text_{{ i }}" class="form-control" value="{{ st.text if st else '' }}"></div>
        <div class="col-md-3">
          <select name="tf_correct_{{ i }}" class="form-select">
            <option value="" {{ "selected" if not st else "" }}>-- chưa dùng --</option>
            <option value="true" {{ "selected" if st and st.correct == true else "" }}>Đúng</option>
            <option value="false" {{ "selected" if st and st.correct == false else "" }}>Sai</option>
          </select>
        </div>
      </div>
      {% endfor %}

      {% elif question.type == "short" %}
      <label class="form-label fw-semibold">Các ô trả lời ngắn (bỏ trống dòng nào không dùng, tối đa 4)</label>
      {% for i in range(4) %}
      {% set bl = question.blanks[i] if i < question.blanks|length else None %}
      <div class="row g-2 mb-2">
        <div class="col-md-5"><input type="text" name="sh_label_{{ i }}" class="form-control" value="{{ bl.label if bl else '' }}"></div>
        <div class="col-md-7"><input type="text" name="sh_answers_{{ i }}" class="form-control" value="{{ bl.answers|join('; ') if bl else '' }}"></div>
      </div>
      {% endfor %}

      {% elif question.type == "dragdrop" %}
      <label class="form-label fw-semibold">Danh sách đáp án để kéo thả (cách nhau bằng dấu ;)</label>
      <input type="text" name="dd_pool" class="form-control mb-2" value="{{ question.options_pool|join('; ') }}">
      <label class="form-label fw-semibold">Các ô trống (bỏ trống dòng nào không dùng, tối đa 4)</label>
      {% for i in range(4) %}
      {% set bl = question.blanks[i] if i < question.blanks|length else None %}
      <div class="row g-2 mb-2">
        <div class="col-md-5"><input type="text" name="dd_label_{{ i }}" class="form-control" value="{{ bl.label if bl else '' }}"></div>
        <div class="col-md-7"><input type="text" name="dd_answer_{{ i }}" class="form-control" value="{{ bl.answer if bl else '' }}"></div>
      </div>
      {% endfor %}
      {% endif %}

      <div class="row g-3 my-2">
        <div class="col-md-3">
          <label class="form-label fw-semibold">Điểm câu này</label>
          <input type="number" name="points" class="form-control" value="{{ question.points }}" min="1" step="1">
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Lời giải chi tiết</label>
        <textarea name="explanation" class="form-control" rows="3" required>{{ question.explanation }}</textarea>
      </div>

      <button type="submit" class="btn btn-tsa px-4">Lưu chỉnh sửa</button>
    </form>
  </div>
</div>
""" + BASE_FOOT

# =======================================================================
# 5) ROUTES
# =======================================================================
def exams_with_counts():
    """Danh sách đề kèm số câu hỏi (viết sẵn trong code của đề + thêm qua admin) để hiển thị."""
    extra_qs = load_extra_questions()
    removed_map = load_exam_removed()
    result = []
    for e in EXAMS:
        removed_ids = set(removed_map.get(e["id"], []))
        base_count = len([q for q in e["questions"] if q["id"] not in removed_ids])
        extra_count = len([q for q in extra_qs if q.get("exam_id") == e["id"]])
        result.append({
            **e,
            "base_count": base_count,
            "extra_count": extra_count,
            "total_questions": base_count + extra_count,
        })
    return result


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return view_func(*args, **kwargs)
    return wrapper


@app.route("/")
@student_required
def index():
    return render_template_string(
        TPL_INDEX, title="Chọn đề thi", exams=exams_with_counts(),
        student_name=session.get("student_name"),
    )


@app.route("/login", methods=["GET"])
def student_login():
    """BẮT BUỘC ĐĂNG NHẬP WORDPRESS: chỉ vào thi được khi có token hợp lệ
    (?wp_token=...) do WordPress tạo ra khi học sinh đã đăng nhập trên web
    chính. Không có/token sai/hết hạn -> chặn, không cho nhập tên tay nữa."""
    if session.get("student_name"):
        return redirect(url_for("index"))

    wp_token = request.args.get("wp_token")
    name = verify_wp_token(wp_token)
    if name:
        session["student_name"] = name
        return redirect(url_for("index"))

    return render_template_string(TPL_LOGIN_BLOCKED, title="Cần đăng nhập")


@app.route("/logout")
def student_logout():
    session.pop("student_name", None)
    return redirect(url_for("student_login"))


@app.route("/exam/<exam_id>")
@student_required
def exam_page(exam_id):
    exam = get_exam_by_id(exam_id)
    if not exam:
        abort(404)
    student_name = session.get("student_name", "Học sinh")
    questions = get_exam_questions(exam_id)
    return render_template_string(
        TPL_EXAM, title=exam["name"], exam=exam, questions=questions, student_name=student_name
    )


@app.route("/submit/<exam_id>", methods=["POST"])
@student_required
def submit_exam(exam_id):
    exam = get_exam_by_id(exam_id)
    if not exam:
        abort(404)

    student_name = session.get("student_name", "Học sinh")
    total_earned, total_max, details, answers = grade_exam(exam_id, request.form)

    submission_id = str(uuid.uuid4())
    db = get_db()
    db.execute(
        """
        INSERT INTO submissions (id, exam_id, student_name, answers_json, score, max_score, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            submission_id, exam_id, student_name,
            json.dumps(answers, ensure_ascii=False),
            total_earned, total_max, datetime.utcnow().isoformat(),
        ),
    )
    db.commit()

    return redirect(url_for("result_page", submission_id=submission_id))


@app.route("/result/<submission_id>")
@student_required
def result_page(submission_id):
    db = get_db()
    row = db.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,)).fetchone()
    if not row:
        abort(404)

    exam = get_exam_by_id(row["exam_id"])
    stored_answers = json.loads(row["answers_json"])

    questions = get_exam_questions(row["exam_id"])
    details = []
    for q in questions:
        submitted = stored_answers.get(q["id"], {})
        earned, max_points, detail = grade_question(q, submitted)
        details.append({
            "id": q["id"], "type": q["type"], "content": q["content"], "explanation": q["explanation"],
            "image": q.get("image"),
            "earned": round(earned, 2), "max": max_points, "detail": detail,
        })

    score_10 = round((row["score"] / row["max_score"]) * 10, 2) if row["max_score"] else 0

    return render_template_string(
        TPL_RESULT, title="Kết quả bài thi", exam=exam, student_name=row["student_name"],
        score=row["score"], max_score=row["max_score"], score_10=score_10, details=details,
    )


# ---------------- QUẢN TRỊ: thêm câu hỏi vào cuối mỗi đề ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if session.get("is_admin"):
        return redirect(url_for("admin_panel"))
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        error = "Sai mật khẩu, vui lòng thử lại."
    return render_template_string(TPL_ADMIN_LOGIN, title="Đăng nhập quản trị", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/panel")
@admin_required
def admin_panel():
    return render_template_string(
        TPL_ADMIN_PANEL, title="Quản trị đề thi",
        exams=exams_with_counts(), success=request.args.get("success"), error=request.args.get("error"),
    )


def _save_uploaded_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    ext = file_storage.filename.rsplit(".", 1)[-1].lower() if "." in file_storage.filename else ""
    if ext not in ALLOWED_IMAGE_EXT:
        return None
    filename = f"{uuid.uuid4().hex}.{ext}"
    filename = secure_filename(filename)
    file_storage.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return f"/static/uploads/{filename}"


def _parse_question_form(qtype, form, files, existing_image=None):
    """Đọc dữ liệu form thành 1 dict câu hỏi (chưa có 'id'). Dùng chung cho thêm mới và sửa.
    Trả về (question_dict, error_message). Nếu lỗi thì question_dict = None."""
    content = (form.get("content") or "").strip()
    explanation = (form.get("explanation") or "").strip()
    try:
        points = int(form.get("points") or 1)
    except ValueError:
        points = 10

    if not content or not explanation or qtype not in ("mc4", "truefalse", "short", "dragdrop"):
        return None, "Vui lòng nhập đủ nội dung câu hỏi và lời giải."

    # Ảnh minh hoạ: ưu tiên file tải lên mới, sau đó tới link ngoài, cuối cùng giữ ảnh cũ (khi sửa)
    image = _save_uploaded_image(files.get("image_file"))
    if not image:
        image_url = (form.get("image_url") or "").strip()
        image = image_url or existing_image

    question = {
        "type": qtype, "content": content,
        "explanation": explanation, "points": points, "image": image,
    }

    if qtype == "mc4":
        options = {
            "A": (form.get("opt_A") or "").strip(),
            "B": (form.get("opt_B") or "").strip(),
            "C": (form.get("opt_C") or "").strip(),
            "D": (form.get("opt_D") or "").strip(),
        }
        if not all(options.values()):
            return None, "Vui lòng nhập đủ 4 phương án A/B/C/D."
        question["options"] = options
        question["correct"] = form.get("mc4_correct", "A")

    elif qtype == "truefalse":
        statements = []
        for i in range(5):
            text = (form.get(f"tf_text_{i}") or "").strip()
            correct_raw = form.get(f"tf_correct_{i}") or ""
            if text and correct_raw in ("true", "false"):
                statements.append({"text": text, "correct": correct_raw == "true"})
        if not statements:
            return None, "Vui lòng nhập ít nhất 1 mệnh đề Đúng/Sai."
        question["statements"] = statements

    elif qtype == "short":
        blanks = []
        for i in range(4):
            label = (form.get(f"sh_label_{i}") or "").strip()
            answers_raw = (form.get(f"sh_answers_{i}") or "").strip()
            if label and answers_raw:
                answers = [a.strip() for a in answers_raw.split(";") if a.strip()]
                blanks.append({"label": label, "answers": answers})
        if not blanks:
            return None, "Vui lòng nhập ít nhất 1 ô trả lời ngắn."
        question["blanks"] = blanks

    elif qtype == "dragdrop":
        pool_raw = (form.get("dd_pool") or "").strip()
        options_pool = [a.strip() for a in pool_raw.split(";") if a.strip()]
        blanks = []
        for i in range(4):
            label = (form.get(f"dd_label_{i}") or "").strip()
            answer = (form.get(f"dd_answer_{i}") or "").strip()
            if label and answer:
                blanks.append({"label": label, "answer": answer})
        if not options_pool or not blanks:
            return None, "Vui lòng nhập danh sách đáp án kéo thả và ít nhất 1 ô trống."
        question["options_pool"] = options_pool
        question["blanks"] = blanks

    return question, None


@app.route("/admin/add-question", methods=["POST"])
@admin_required
def admin_add_question():
    exam_id = request.form.get("exam_id")
    exam = get_exam_by_id(exam_id)
    if not exam:
        return redirect(url_for("admin_panel", error="Đề thi không hợp lệ."))

    qtype = request.form.get("qtype")
    question, err = _parse_question_form(qtype, request.form, request.files)
    if err:
        return redirect(url_for("admin_panel", error=err))

    new_id = f"{exam_id}_x" + uuid.uuid4().hex[:8]
    question["id"] = new_id
    question["exam_id"] = exam_id

    extra_questions = load_extra_questions()
    extra_questions.append(question)
    save_extra_questions(extra_questions)

    return redirect(url_for("admin_panel", success=f"Đã thêm câu hỏi vào cuối \"{exam['name']}\"."))


@app.route("/admin/exam/<exam_id>/questions")
@admin_required
def admin_exam_questions(exam_id):
    """Trang liệt kê toàn bộ câu hỏi đang có trong 1 đề, có nút Sửa / Xoá cho từng câu."""
    exam = get_exam_by_id(exam_id)
    if not exam:
        abort(404)
    overrides = load_question_overrides()
    rows = []
    for q in get_exam_questions(exam_id):
        rows.append({**q, "is_extra": is_extra_question(q["id"]), "is_edited": q["id"] in overrides})
    return render_template_string(
        TPL_ADMIN_EXAM_QUESTIONS, title=f"Câu hỏi - {exam['name']}", exam=exam, questions=rows,
        success=request.args.get("success"), error=request.args.get("error"),
    )


@app.route("/admin/question/<qid>/edit", methods=["GET", "POST"])
@admin_required
def admin_edit_question(qid):
    """Sửa nội dung 1 câu hỏi (gốc hoặc thêm qua quản trị). Lưu đè qua data/question_overrides.json,
    không bao giờ chỉnh sửa trực tiếp biến EXAMS trong code."""
    exam_id = request.values.get("exam_id", "")
    question = get_question_by_id(qid)
    if not question:
        abort(404)

    if request.method == "POST":
        updated, err = _parse_question_form(
            question["type"], request.form, request.files, existing_image=question.get("image")
        )
        if err:
            return redirect(url_for("admin_edit_question", qid=qid, exam_id=exam_id, error=err))
        updated["id"] = qid
        overrides = load_question_overrides()
        overrides[qid] = updated
        save_question_overrides(overrides)
        return redirect(url_for("admin_exam_questions", exam_id=exam_id, success="Đã lưu chỉnh sửa câu hỏi."))

    return render_template_string(
        TPL_EDIT_QUESTION, title="Sửa câu hỏi", question=question, exam_id=exam_id,
        error=request.args.get("error"),
    )


@app.route("/admin/exam/<exam_id>/remove-question/<qid>", methods=["POST"])
@admin_required
def admin_remove_question(exam_id, qid):
    """Xoá 1 câu hỏi khỏi đề. Câu thêm qua quản trị -> xoá hẳn. Câu gốc trong code -> chỉ ẩn khỏi
    riêng đề này (ngân hàng câu hỏi gốc trong code không bị đụng tới, đề khác dùng câu đó vẫn còn)."""
    exam = get_exam_by_id(exam_id)
    if not exam:
        abort(404)

    if is_extra_question(qid):
        extra_questions = [q for q in load_extra_questions() if q["id"] != qid]
        save_extra_questions(extra_questions)

        overrides = load_question_overrides()
        if qid in overrides:
            del overrides[qid]
            save_question_overrides(overrides)
    else:
        removed_map = load_exam_removed()
        removed_map.setdefault(exam_id, [])
        if qid not in removed_map[exam_id]:
            removed_map[exam_id].append(qid)
        save_exam_removed(removed_map)

    return redirect(url_for("admin_exam_questions", exam_id=exam_id, success="Đã xoá câu hỏi khỏi đề."))


# =======================================================================
# 6) CHẠY APP
# =======================================================================
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
else:
    # Khi chạy qua gunicorn trên VPS (gunicorn app:app), đảm bảo DB được khởi tạo
    init_db()

# =======================================================================
# HƯỚNG DẪN DEPLOY LÊN VPS (Ubuntu/Debian, Gunicorn + Nginx)
# =======================================================================
# 0) File .gitignore nên có (để không đưa dữ liệu sinh ra khi chạy lên Git):
#      database.db
#      data/
#      static/uploads/
#
# 1) Đưa code lên GitHub:
#      git init && git add app.py .gitignore && git commit -m "TSA exam app (theme do, mathjax, admin)"
#      git branch -M main
#      git remote add origin https://github.com/<user>/<repo>.git
#      git push -u origin main
#
# 2) Trên VPS:
#      sudo apt update && sudo apt install -y python3-pip python3-venv nginx git
#      cd /var/www && sudo git clone https://github.com/<user>/<repo>.git tsa_exam_app
#      cd tsa_exam_app
#      python3 -m venv venv && source venv/bin/activate
#      pip install flask gunicorn
#
# 3) Test:
#      venv/bin/gunicorn --bind 0.0.0.0:8000 app:app
#      -> mở http://<ip-vps>:8000 để kiểm tra
#      -> mở http://<ip-vps>:8000/admin để thêm câu hỏi (đổi ADMIN_PASSWORD!)
#
# 4) Chạy nền bằng systemd - tạo /etc/systemd/system/tsa_exam.service:
#      [Unit]
#      Description=Gunicorn TSA exam app
#      After=network.target
#
#      [Service]
#      User=www-data
#      WorkingDirectory=/var/www/tsa_exam_app
#      Environment="SECRET_KEY=doi-thanh-chuoi-bi-mat"
#      Environment="ADMIN_PASSWORD=doi-mat-khau-quan-tri-that-manh"
#      ExecStart=/var/www/tsa_exam_app/venv/bin/gunicorn --workers 3 --bind unix:tsa_exam.sock -m 007 app:app
#
#      [Install]
#      WantedBy=multi-user.target
#
#      sudo chown -R www-data:www-data /var/www/tsa_exam_app
#      sudo systemctl start tsa_exam && sudo systemctl enable tsa_exam
#
# 5) Nginx reverse proxy - /etc/nginx/sites-available/tsa_exam:
#      server {
#          listen 80;
#          server_name your-domain.com;
#          client_max_body_size 10M;   # cho phép tải ảnh minh hoạ lên trang quản trị
#          location / {
#              include proxy_params;
#              proxy_pass http://unix:/var/www/tsa_exam_app/tsa_exam.sock;
#          }
#      }
#      sudo ln -s /etc/nginx/sites-available/tsa_exam /etc/nginx/sites-enabled
#      sudo nginx -t && sudo systemctl restart nginx
#
# 6) HTTPS miễn phí:
#      sudo apt install -y certbot python3-certbot-nginx
#      sudo certbot --nginx -d your-domain.com
#
# 7) Cập nhật code sau này (dữ liệu trong data/ và static/uploads/ không bị mất
#    vì đã gitignore, không nằm trong repo):
#      cd /var/www/tsa_exam_app && sudo git pull && sudo systemctl restart tsa_exam
# =======================================================================
