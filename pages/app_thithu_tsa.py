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
        "name": 'Đề ôn tập TSA Toán 11 - Đề 1. ',
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
                "image": 'https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de_tsa11_cau4_robot.PNG',
                "options_pool": ['36', '108/13', '72/13', '24', '36/13'],
                "blanks": [
                    {"label": 'Tổng quãng đường robot di chuyển được sau vô hạn bước là (cm):', "answer": '36'},
                    {"label": 'Hoành độ X của điểm tới hạn M là:', "answer": '108/13'},
                    {"label": 'Tung độ Y của điểm tới hạn M là:', "answer": '72/13'},
                ],
                "points": 1,
                "explanation": "Độ dài các đoạn lập thành cấp số nhân \\( L_n = 12\\cdot(2/3)^{n-1} \\). Tổng quãng đường: \\( \\sum L_n = \\dfrac{12}{1-2/3} = 36 \\) cm. Hướng di chuyển lặp chu kỳ 4 (Đông, Bắc, Tây, Nam) do mỗi bước quay trái 90°. Hoành độ: \\( X = L_1 - L_3 + L_5 - \\cdots = 12\\left[1-(2/3)^2+(2/3)^4-\\cdots\\right] = 12\\cdot\\dfrac{1}{1+4/9} = 12\\cdot\\dfrac{9}{13} = \\dfrac{108}{13} \\). Tung độ: \\( Y = L_2 - L_4 + L_6 - \\cdots = 12\\cdot\\dfrac23\\cdot\\dfrac{9}{13} = \\dfrac{72}{13} \\).",
            },

            # ================== TRẮC NGHIỆM 4 LỰA CHỌN (mc4) - tiếp ==================
            {
                "id": 'de_tsa11_mc_02',
                "type": 'mc4',
                "content": ' Một bài thi trắc nghiệm Toán học có 10 câu hỏi khó, mỗi câu có 4 đáp án và chỉ có 1 đáp án đúng. Trả lời đúng được 1 điểm, trả lời sai bị trừ 0.25 điểm. Học sinh C tự tin làm chắc chắn đúng 6 câu đầu tiên. Trong 4 câu còn lại, có 2 câu C loại bỏ được 2 phương án chắc chắn sai (rồi chọn ngẫu nhiên trong 2 phương án còn lại); 2 câu C không biết gì nên khoanh bừa cả 4 phương án. Tính xác suất để C đạt từ 8 điểm trở lên.',
                "options": {
                    'A': '3/32',
                    'B': '9/64',
                    'C': '11/64',
                    'D': '5/32',
                },
                "correct": 'B',
                "points": 1,
                "explanation": 'Điểm chắc chắn từ 6 câu đầu = 6. Cần điểm của 4 câu còn lại \\( \\ge 2 \\). Gọi \\(c_A\\) = số câu đúng trong 2 câu "loại 2 phương án" (mỗi câu đúng với xác suất 1/2), \\(c_B\\) = số câu đúng trong 2 câu "khoanh bừa 4 phương án" (mỗi câu đúng với xác suất 1/4). Điểm 4 câu này \\( = 1{,}25(c_A+c_B) - 1 \\ge 2 \\Leftrightarrow c_A+c_B \\ge 2{,}4 \\Leftrightarrow c_A+c_B \\ge 3\\). Với \\(c_A\\sim B(2;1/2)\\): \\(P(0)=1/4, P(1)=1/2, P(2)=1/4\\). Với \\(c_B\\sim B(2;1/4)\\): \\(P(0)=9/16, P(1)=3/8, P(2)=1/16\\). \\(P(c_A+c_B=4) = P(2,2)=\\frac14\\cdot\\frac1{16}=\\frac1{64}\\). \\(P(c_A+c_B=3)=P(1,2)+P(2,1)=\\frac12\\cdot\\frac1{16}+\\frac14\\cdot\\frac38=\\frac1{32}+\\frac3{32}=\\frac4{32}=\\frac{8}{64}\\). Tổng \\( = \\frac1{64}+\\frac8{64}=\\frac9{64}\\). Đáp án B.',
            },

            # ================== ĐÚNG / SAI (truefalse) - tiếp ==================
            {
                "id": 'de_tsa11_tf_02',
                "type": 'truefalse',
                "content": ' Một bệnh nhân được tiêm một liều thuốc 100 mg vào lúc 8h00 sáng. Biết rằng cứ sau mỗi giờ, lượng thuốc trong cơ thể bị đào thải 20% so với giờ trước đó. Để duy trì nồng độ thuốc, bắt đầu từ 9h00 sáng, cứ mỗi giờ bệnh nhân lại được tiêm bổ sung thêm 10 mg thuốc. Gọi \\( u_n \\) là lượng thuốc trong cơ thể bệnh nhân ngay sau lần tiêm thứ \\( n \\) (với \\( n=1 \\) tương ứng lúc 8h00 sáng). Xét tính Đúng/Sai của các mệnh đề sau:',
                "statements": [
                    {"text": 'Lượng thuốc trong cơ thể ngay sau lần tiêm thứ 3 (lúc 10h00 sáng) là 82 mg', "correct": True},
                    {"text": 'Công thức tổng quát của lượng thuốc sau lần tiêm thứ n là \\( u_n = 50\\cdot(0.8)^{n-1}+50 \\)', "correct": True},
                    {"text": 'Kể từ sau 24 giờ, lượng thuốc trong cơ thể sẽ tụt xuống dưới mức 50 mg', "correct": False},
                    {"text": 'Nếu quá trình tiêm này kéo dài vô hạn, lượng thuốc trong cơ thể bệnh nhân sẽ tiến dần về mức 0 mg', "correct": False},
                ],
                "points": 1,
                "explanation": 'Đệ quy: \\( u_{n+1}=0.8u_n+10,\\ u_1=100 \\). Điểm cân bằng \\( L=0.8L+10\\Rightarrow L=50 \\). Đặt \\( v_n=u_n-50\\Rightarrow v_n=v_1\\cdot0.8^{n-1}=50\\cdot0.8^{n-1}\\Rightarrow u_n=50\\cdot0.8^{n-1}+50\\). (a) \\( u_1=100,u_2=0.8\\cdot100+10=90,u_3=0.8\\cdot90+10=82\\) mg \\(\\Rightarrow\\) Đúng. (b) Đúng công thức vừa suy ra \\(\\Rightarrow\\) Đúng. (c) Vì \\(50\\cdot0.8^{n-1}>0\\) với mọi \\(n\\), nên \\(u_n>50\\) luôn đúng, không bao giờ tụt dưới 50 mg \\(\\Rightarrow\\) Sai. (d) Giới hạn \\( \\lim u_n = 50 \\ne 0 \\Rightarrow\\) Sai.',
            },

            # ================== TRẢ LỜI NGẮN (short) - tiếp ==================
            {
                "id": 'de_tsa11_sh_02',
                "type": 'short',
                "content": ' Cho hàm số \\( f(x) = x^3 - 3x^2 + 2 \\) có đồ thị (C). Qua điểm \\( M(m; 2) \\) có thể kẻ được đúng 3 tiếp tuyến đến đồ thị (C), trong đó có đúng 2 tiếp tuyến vuông góc với nhau. Giá trị của tham số m bằng bao nhiêu? (Điền đáp án dưới dạng phân số tối giản).',
                "blanks": [
                    {"label": 'm =', "answers": ['-1/27']},
                ],
                "points": 1,
                "explanation": 'Tiếp tuyến tại \\(t\\): \\(y=f(t)+f\'(t)(x-t)\\), với \\(f\'(t)=3t^2-6t\\). Qua M(m;2): \\(2=f(t)+f\'(t)(m-t)\\), rút gọn được \\(t\\big[2t^2-3(1+m)t+6m\\big]=0\\). Vậy \\(t=0\\) (tiếp tuyến ngang \\(y=2\\)) và 2 nghiệm \\(t_1,t_2\\) của \\(2t^2-3(1+m)t+6m=0\\) (tổng \\(s=t_1+t_2=\\frac{3(1+m)}{2}\\), tích \\(p=t_1t_2=3m\\)) cho đủ 3 tiếp tuyến phân biệt. Vì tiếp tuyến tại \\(t=0\\) có hệ số góc 0 nên không thể vuông góc với tiếp tuyến nào khác (cần hệ số góc kia là vô cực) \\(\\Rightarrow\\) cặp vuông góc duy nhất phải là \\((t_1,t_2)\\): \\(f\'(t_1)f\'(t_2)=-1\\). Có \\(f\'(t)=3t(t-2)\\Rightarrow f\'(t_1)f\'(t_2)=9p(p-2s+4)\\). Thay \\(p=3m,\\ s=\\frac{3(1+m)}2\\) được \\(p-2s+4=3m-3(1+m)+4=1\\) (hằng số!) \\(\\Rightarrow f\'(t_1)f\'(t_2)=9p=27m=-1\\Rightarrow m=-\\dfrac1{27}\\). Kiểm tra \\(\\Delta=9(1+m)^2-48m=\\dfrac{820}{81}>0\\) (2 nghiệm phân biệt, khác 0) \\(\\Rightarrow\\) thỏa mãn.',
            },
            {
                "id": 'de_tsa11_sh_03',
                "type": 'short',
                "content": ' Lấy ngẫu nhiên một ước số nguyên dương của số \\( M = 2^{10}\\cdot 3^{15}\\cdot 5^{20} \\). Xác suất để ước số được chọn là lập phương của một số tự nhiên (tức là có dạng \\( k^3 \\) với \\( k \\in \\mathbb{N} \\)) có thể viết dưới dạng phân số tối giản là \\( \\dfrac{a}{b} \\). Tính giá trị của biểu thức \\( S = a + b \\).',
                "blanks": [
                    {"label": 'S = a + b =', "answers": ['23']},
                ],
                "points": 1,
                "explanation": 'Tổng số ước của M: \\((10+1)(15+1)(20+1)=11\\cdot16\\cdot21=3696\\). Ước dạng \\(2^a3^b5^c\\) là lập phương \\(\\Leftrightarrow a,b,c\\) đều chia hết cho 3: \\(a\\in\\{0,3,6,9\\}\\) (4 giá trị, do \\(a\\le10\\)); \\(b\\in\\{0,3,...,15\\}\\) (6 giá trị); \\(c\\in\\{0,3,...,18\\}\\) (7 giá trị, do \\(c\\le20\\)). Số ước lập phương \\(=4\\cdot6\\cdot7=168\\). Xác suất \\(=\\dfrac{168}{3696}=\\dfrac{1}{22}\\Rightarrow a=1,b=22\\Rightarrow S=23\\).',
            },
            {
                "id": 'de_tsa11_sh_04',
                "type": 'short',
                "content": ' Cho phương trình lượng giác: \\( \\sqrt{1-\\sin 2x} + \\sqrt{1+\\sin 2x} = 2\\sqrt{2}\\cos x \\). Hỏi trên đoạn \\( [-100\\pi; 100\\pi] \\), phương trình đã cho có tất cả bao nhiêu nghiệm phân biệt?',
                "blanks": [
                    {"label": 'Số nghiệm =', "answers": ['200']},
                ],
                "points": 1,
                "explanation": 'Do \\(1\\mp\\sin2x=(\\sin x\\mp\\cos x)^2\\) nên VT \\(=|\\sin x-\\cos x|+|\\sin x+\\cos x|=2\\max(|\\sin x|,|\\cos x|)\\) (đẳng thức \\(|a-b|+|a+b|=2\\max(|a|,|b|)\\)). PT trở thành \\(\\max(|\\sin x|,|\\cos x|)=\\sqrt2\\cos x\\), suy ra cần \\(\\cos x\\ge0\\). Nếu \\(|\\cos x|\\ge|\\sin x|\\): \\(\\cos x=\\sqrt2\\cos x\\Rightarrow\\cos x=0\\), vô lý (mâu thuẫn giả thiết). Nếu \\(|\\sin x|\\ge|\\cos x|\\): \\(|\\sin x|=\\sqrt2\\cos x\\), kết hợp \\(\\sin^2x+\\cos^2x=1\\Rightarrow3\\cos^2x=1\\Rightarrow\\cos x=\\dfrac1{\\sqrt3}\\) (nhận vì \\(\\ge0\\)), \\(|\\sin x|=\\dfrac{\\sqrt6}{3}\\) (thỏa điều kiện \\(|\\sin x|\\ge|\\cos x|\\)). Vậy nghiệm: \\(x=\\pm\\alpha+2k\\pi\\) với \\(\\alpha=\\arccos\\dfrac1{\\sqrt3}\\in(0;\\frac\\pi2)\\) — đúng 2 nghiệm mỗi chu kỳ \\(2\\pi\\). Đoạn \\([-100\\pi;100\\pi]\\) có độ dài \\(200\\pi=100\\) chu kỳ trọn vẹn \\(\\Rightarrow\\) tổng số nghiệm \\(=100\\times2=200\\).',
            },

            # ================== KÉO THẢ (dragdrop) - tiếp ==================
            {
                "id": 'de_tsa11_dd_02',
                "type": 'dragdrop',
                "content": " Cho hình chóp S.ABC có đáy ABC là tam giác vuông cân tại B, với cạnh AB = a. Cạnh bên SA vuông góc với mặt phẳng đáy (ABC) và SA = a√2. Kéo và thả các kết quả sau vào các ô tương ứng:",
                "options_pool": ['a√6/3', '60°', 'a√3/3', '1/3', 'arccos(√3/3)'],
                "blanks": [
                    {"label": 'Số đo góc tạo bởi hai mặt phẳng (SBC) và (SAC) là:', "answer": 'arccos(√3/3)'},
                    {"label": 'Khoảng cách từ đỉnh A đến mặt phẳng (SBC) bằng:', "answer": 'a√6/3'},
                    {"label": 'Số đo góc tạo bởi hai đường thẳng chéo nhau SC và AB là:', "answer": '60°'},
                ],
                "points": 1,
                "explanation": "Chọn hệ trục: B(0,0,0), A(a,0,0), C(0,a,0) (vuông cân tại B), S(a,0,a√2) (do SA⊥đáy). \\(\\bullet\\) Góc 2 mp (SAC),(SBC): pháp tuyến \\((SAC)\\): \\(\\vec{n_1}=\\vec{AS}\\times\\vec{AC}=(0,0,a\\sqrt2)\\times(-a,a,0) \\propto(1,1,0)\\); pháp tuyến \\((SBC)\\): \\(\\vec{n_2}=\\vec{BS}\\times\\vec{BC}=(a,0,a\\sqrt2)\\times(0,a,0)\\propto(-\\sqrt2,0,1)\\). \\(\\cos\\varphi=\\dfrac{|\\vec{n_1}\\cdot\\vec{n_2}|}{|\\vec{n_1}||\\vec{n_2}|}=\\dfrac{\\sqrt2}{\\sqrt2\\cdot\\sqrt3}=\\dfrac1{\\sqrt3}=\\dfrac{\\sqrt3}{3}\\Rightarrow\\varphi=\\arccos\\dfrac{\\sqrt3}{3}\\). \\(\\bullet\\) Mặt (SBC) qua B với pháp tuyến \\((-\\sqrt2,0,1)\\): \\(-\\sqrt2x+z=0\\). \\(d(A,(SBC))=\\dfrac{|-\\sqrt2\\cdot a|}{\\sqrt3}=\\dfrac{a\\sqrt2}{\\sqrt3}=\\dfrac{a\\sqrt6}{3}\\). \\(\\bullet\\) \\(\\vec{SC}=(-a,a,-a\\sqrt2)\\), \\(\\vec{AB}=(-a,0,0)\\): \\(\\cos\\theta=\\dfrac{|\\vec{SC}\\cdot\\vec{AB}|}{|\\vec{SC}||\\vec{AB}|}=\\dfrac{a^2}{2a\\cdot a}=\\dfrac12\\Rightarrow\\theta=60^\\circ\\).",
            },

            # ================== TRẢ LỜI NGẮN (short) - tiếp ==================
            # ================== TRẢ LỜI NGẮN (short) - tiếp ==================
    {
        "id": "de_tsa11_sh_05",
        "type": "short",
        "content": ' Một chiếc xe chạy trong sa mạc có quỹ đạo là một đường cong bậc ba với phương trình \\( y = \\dfrac{1}{3}x^3 - 2x^2 + 5x \\) (trên hệ trục tọa độ với đơn vị là km). Tại mọi thời điểm, đèn pha của xe luôn chiếu sáng theo một tia sáng thẳng trùng với phương của tiếp tuyến quỹ đạo xe chạy tại điểm đó. Tại thời điểm xe đi ngang qua vị trí có hoành độ \\( x = 4 \\) thì đèn pha chiếu sáng trúng một cột mốc M nằm trên trục tung Oy. Hãy xác định tung độ của cột mốc M. (Điền đáp án dưới dạng phân số tối giản).',
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau11-de1.PNG",
        "blanks": [
            {"label": "Tung độ của M =", "answers": ["-32/3"]}
        ],
        "points": 1,
        "explanation": "Tại \\(x=4\\): \\(y(4)=\\dfrac13(4)^3-2(4)^2+5(4)=\\dfrac{64}{3}-32+20=\\dfrac{64}{3}-12=\\dfrac{28}{3}\\). Đạo hàm \\(y'=x^2-4x+5\\Rightarrow y'(4)=16-16+5=5\\) (hệ số góc tiếp tuyến). Phương trình tiếp tuyến tại \\(x=4\\): \\(y=5(x-4)+\\dfrac{28}{3}=5x-20+\\dfrac{28}{3}=5x-\\dfrac{32}{3}\\). Cột mốc M nằm trên Oy \\(\\Rightarrow x=0\\Rightarrow y_M=-\\dfrac{32}{3}\\)."
    },
    {
        "id": "de_tsa11_sh_06",
        "type": "short",
        "content": "Một số tự nhiên X có 2026 chữ số, trong đó có đúng 2025 chữ số 9 và chữ số tận cùng là 8 (nghĩa là X = \\(\\underbrace{99\\ldots9}_{2025\\text{ chữ số}}8\\)). Đặt \\( Y = X^2 \\). Hỏi tổng tất cả các chữ số của số Y bằng bao nhiêu?",
        "blanks": [
            {"label": "Tổng các chữ số của Y =", "answers": ["18235"]}
        ],
        "points": 1,
        "explanation": "Viết \\(X=10^n-2\\) với \\(n=2026\\) (kiểm tra: \\(n=1\\Rightarrow10-2=8\\); \\(n=2\\Rightarrow100-2=98\\); tổng quát \\(10^n-2\\) có dạng \\((n-1)\\) chữ số 9 rồi đến 8 — đúng với X có 2025 chữ số 9 rồi đến 8, \\(n=2026\\)). Khi đó \\(Y=X^2=10^{2n}-4\\cdot10^n+4=10^n(10^n-4)+4\\). Vì \\(10^n-4\\) có dạng \\((n-1)\\) chữ số 9 rồi đến 6 (thử \\(n=1{:}\\,6\\); \\(n=2{:}\\,96\\); \\(n=3{:}\\,996\\)), nên \\(10^n(10^n-4)\\) là số đó theo sau bởi \\(n\\) chữ số 0. Cộng thêm 4 vào chữ số cuối (đang là 0) được: \\(Y=\\underbrace{9\\ldots9}_{n-1}6\\underbrace{0\\ldots0}_{n-1}4\\) (tổng cộng \\(2n\\) chữ số). Tổng chữ số của Y \\(=9(n-1)+6+4=9n+1\\). Với \\(n=2026\\): tổng \\(=9\\times2026+1=18234+1=18235\\).\n\nKiểm tra với n nhỏ: \\(n=3\\): X=998, \\(X^2=996004\\), tổng chữ số \\(=9+9+6+0+0+4=28=9\\times3+1\\) ✓ khớp công thức."
    },

    # ---------------- ĐÚNG / SAI (truefalse) ----------------
   {
        "id": "de1_tf_13",
        "type": "truefalse",
        "content": """Một trạm ra-đa của cảnh sát giao thông đã ghi lại tốc độ (đơn vị: km/h) của 50 chiếc ô tô đi qua một đoạn đường cao tốc được giới hạn tốc độ. Số liệu được ghép nhóm như sau:
        
       Biết rằng đoạn đường này quy định tốc độ tối đa là 100 km/h. Xét tính Đúng/Sai của các mệnh đề sau:""",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau13-de1.PNG",
        "statements": [
            {"text": "Mốt của mẫu số liệu trên thuộc nhóm [80; 100).", "correct": True},
            {"text": "Tứ phân vị thứ nhất \\( (Q_1) \\) của mẫu số liệu bằng 65 km/h.", "correct": False},
            {"text": "Tốc độ trung bình của 50 chiếc xe bị ghi nhận là 91.2 km/h.", "correct": False},
            {"text": "Số xe vi phạm tốc độ tối đa chiếm hơn 35% tổng số xe bị ghi nhận.", "correct": False}
        ],
        "points": 1,
        "explanation": """a) Nhóm chứa mốt là nhóm có tần số lớn nhất (18 xe), đó là nhóm \\( [80; 100) \\) \\( \\Rightarrow \\) Đúng.

b) Cỡ mẫu \\( N = 50 \\), vị trí tứ phân vị thứ nhất là \\( \\dfrac{N}{4} = 12.5 \\).
Tần số tích lũy của nhóm 1 là 5; nhóm 2 là \\( 5+12=17 \\). Do đó \\( Q_1 \\) thuộc nhóm \\( [60; 80) \\).
\\( Q_1 = 60 + \\dfrac{12.5 - 5}{12} \\cdot 20 = 72.5 \\) (km/h) \\( \\Rightarrow \\) Sai.

c) Chọn giá trị đại diện cho các nhóm là 50, 70, 90, 110, 130.
Tốc độ trung bình: \\( \\bar{x} = \\dfrac{5\\cdot 50 + 12\\cdot 70 + 18\\cdot 90 + 10\\cdot 110 + 5\\cdot 130}{50} = 89.2 \\) (km/h) \\( \\Rightarrow \\) Sai.

d) Số xe vi phạm tốc độ tối đa (tốc độ \\( \\ge 100 \\) km/h) thuộc nhóm \\( [100; 120) \\) và \\( [120; 140) \\).
Số lượng là: \\( 10 + 5 = 15 \\) (xe).
Tỉ lệ xe vi phạm là: \\( \\dfrac{15}{50} = 30\\% < 35\\% \\) \\( \\Rightarrow \\) Sai."""
    },

    # ---------------- KÉO THẢ (dragdrop) ----------------
    {
        "id": "de1_dd_14",
        "type": "dragdrop",
        "content": "Anh A mua trả góp một căn hộ và cần vay ngân hàng đúng 1 tỷ VNĐ (tức là \\( 10^9 \\) đồng). Ngân hàng áp dụng mức lãi suất cố định là 0.8%/tháng. Thỏa thuận thanh toán như sau: đúng một tháng sau khi nhận tiền vay, anh A bắt đầu trả nợ; mỗi tháng anh A trả một số tiền cố định là X (đồng) và liên tục trong n tháng cho đến khi hết nợ (tháng cuối cùng có thể làm tròn). Kéo và thả các biểu thức phù hợp vào ô trống:",
        "options_pool": [
            "\\( 8\\cdot 10^6 \\)", 
            "\\( X\\dfrac{1.008^n-1}{0.008} \\)", 
            "\\( 10^9(1.008)^n - X\\dfrac{1.008^n-1}{0.008} \\)", 
            "\\( \\dfrac{8\\cdot 10^6\\cdot 1.008^{60}}{1.008^{60}-1} \\)", 
            "\\( 8\\cdot 10^7 \\)"
        ],
        "blanks": [
            {"label": "Riêng trong tháng đầu tiên, số tiền lãi phát sinh từ khoản vay mà anh A phải chịu là (đồng):", "answer": "8\\cdot 10^6"},
            {"label": "Công thức tính số tiền anh A còn nợ ngân hàng ngay sau khi đóng tiền ở tháng thứ n là:", "answer": "10^9(1.008)^n - X\\dfrac{1.008^n-1}{0.008}"},
            {"label": "Nếu anh A muốn tất toán (trả hết nợ) trong vòng đúng 5 năm (60 tháng), thì số tiền cố định X phải trả mỗi tháng là:", "answer": "\\dfrac{8\\cdot 10^6\\cdot 1.008^{60}}{1.008^{60}-1}"}
        ],
        "points": 1,
        "explanation": """Kí hiệu số tiền vay ban đầu là \\( P = 10^9 \\), lãi suất \\( r = 0.008 \\).

- Tiền lãi riêng tháng đầu tiên anh A phải chịu là: \\( P \\cdot r = 10^9 \\cdot 0.008 = 8,000,000 = 8\\cdot 10^6 \\) (đồng).

- Sau \\( n \\) tháng, số tiền anh A còn nợ là:
\\( T_n = P(1+r)^n - X\\dfrac{(1+r)^n - 1}{r} = 10^9(1.008)^n - X\\dfrac{1.008^n-1}{0.008} \\).

- Để tất toán sau 5 năm (60 tháng), thì \\( T_{60} = 0 \\):
\\( \\Rightarrow 10^9(1.008)^{60} = X\\dfrac{1.008^{60}-1}{0.008} \\)
\\( \\Rightarrow X = \\dfrac{10^9 \\cdot 0.008 \\cdot 1.008^{60}}{1.008^{60}-1} = \\dfrac{8\\cdot 10^6\\cdot 1.008^{60}}{1.008^{60}-1} \\)."""
    },

    # ---------------- TRẢ LỜI NGẮN (short) ----------------
    {
        "id": "de1_sh_15",
        "type": "short",
        "content": "Cho hình chóp S.ABCD có đáy ABCD là hình vuông cạnh a, cạnh bên SA vuông góc với mặt phẳng đáy và \\( SA=a \\). Điểm M di động trên đoạn thẳng BC, điểm N di động trên đoạn thẳng CD sao cho góc \\( \\widehat{MAN}=45^{\\circ} \\). Biết thể tích nhỏ nhất của khối chóp S.AMN có dạng \\( V=\\dfrac{a^3(\\sqrt{p}-q)}{r} \\) với p, q, r là các số nguyên dương phân biệt và phân số tối giản. Tính giá trị biểu thức \\( T=p+q+r \\).",
        "blanks": [
            {"label": "T =", "answers": ["6"]}
        ],
        "points": 1,
        "explanation": """Đặt \\( \\widehat{BAM} = \\alpha, \\widehat{DAN} = \\beta \\). Vì \\( \\widehat{MAN} = 45^\\circ \\) và \\( \\widehat{BAD} = 90^\\circ \\) nên \\( \\alpha + \\beta = 45^\\circ \\).
Ta có: \\( BM = a\\tan\\alpha, DN = a\\tan\\beta \\).
Diện tích tam giác AMN:
\\( S_{AMN} = S_{ABCD} - S_{ABM} - S_{ADN} - S_{MCN} \\)
\\( = a^2 - \\dfrac{a^2}{2}\\tan\\alpha - \\dfrac{a^2}{2}\\tan\\beta - \\dfrac{a^2}{2}(1-\\tan\\alpha)(1-\\tan\\beta) \\)
\\( = \\dfrac{a^2}{2}(1 - \\tan\\alpha\\tan\\beta) \\).
Mà \\( \\tan(\\alpha+\\beta) = 1 \\Leftrightarrow \\dfrac{\\tan\\alpha + \\tan\\beta}{1 - \\tan\\alpha\\tan\\beta} = 1 \\Leftrightarrow \\tan\\alpha + \\tan\\beta = 1 - \\tan\\alpha\\tan\\beta \\).
Áp dụng BĐT Cô-si:
\\( 1 - \\tan\\alpha\\tan\\beta = \\tan\\alpha + \\tan\\beta \\ge 2\\sqrt{\\tan\\alpha\\tan\\beta} \\)
Đặt \\( t = \\sqrt{\\tan\\alpha\\tan\\beta} \\ge 0 \\), ta có \\( t^2 + 2t - 1 \\le 0 \\Rightarrow t \\le \\sqrt{2}-1 \\).
Do đó \\( \\tan\\alpha\\tan\\beta \\le (\\sqrt{2}-1)^2 = 3 - 2\\sqrt{2} \\).
Suy ra: \\( S_{AMN} = \\dfrac{a^2}{2}(1 - \\tan\\alpha\\tan\\beta) \\ge \\dfrac{a^2}{2}(1 - (3 - 2\\sqrt{2})) = a^2(\\sqrt{2}-1) \\).
Thể tích khối chóp:
\\( V = \\dfrac{1}{3}SA \\cdot S_{AMN} \\ge \\dfrac{1}{3}a \\cdot a^2(\\sqrt{2}-1) = \\dfrac{a^3(\\sqrt{2}-1)}{3} \\).
Dấu "=" xảy ra khi \\( \\alpha = \\beta = 22.5^\\circ \\).
Đồng nhất hệ số với \\( V = \\dfrac{a^3(\\sqrt{p}-q)}{r} \\), ta được \\( p=2, q=1, r=3 \\).
Vậy \\( T = p + q + r = 2 + 1 + 3 = 6 \\)."""
    },

    # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
    {
        "id": "de1_mc_16",
        "type": "mc4",
        "content": "Gọi \\( x_1, x_2 \\) là các nghiệm thực của phương trình \\( \\log_2\\dfrac{x^2+2x+3}{2x^2-x+2} = x^2-3x-1 \\). Tính giá trị của biểu thức \\( P=x_1^2+x_2^2 \\).",
        "options": {
            "A": "P = 7",
            "B": "P = 9",
            "C": "P = 11",
            "D": "P = 13"
        },
        "correct": "C",
        "points": 1,
        "explanation": """Điều kiện: \\( \\dfrac{x^2+2x+3}{2x^2-x+2} > 0 \\) (luôn đúng do tử số và mẫu số đều dương với mọi \\( x \\)).
Phương trình tương đương:
\\( \\log_2(x^2+2x+3) - \\log_2(2x^2-x+2) = (2x^2-x+2) - (x^2+2x+3) \\)
\\( \\Leftrightarrow \\log_2(x^2+2x+3) + (x^2+2x+3) = \\log_2(2x^2-x+2) + (2x^2-x+2) \\) (*)
Xét hàm số \\( f(t) = \\log_2 t + t \\) trên \\( (0; +\\infty) \\). Ta có \\( f'(t) = \\dfrac{1}{t\\ln 2} + 1 > 0 \\), nên hàm số đồng biến.
Từ (*) suy ra \\( f(x^2+2x+3) = f(2x^2-x+2) \\)
\\( \\Leftrightarrow x^2+2x+3 = 2x^2-x+2 \\)
\\( \\Leftrightarrow x^2 - 3x - 1 = 0 \\).
Phương trình có 2 nghiệm phân biệt \\( x_1, x_2 \\) (do \\( \\Delta = 13 > 0 \\)).
Theo định lí Vi-ét: \\( x_1 + x_2 = 3 \\) và \\( x_1 x_2 = -1 \\).
Giá trị biểu thức: \\( P = x_1^2 + x_2^2 = (x_1+x_2)^2 - 2x_1 x_2 = 3^2 - 2(-1) = 11 \\).
Vậy đáp án đúng là C."""
    },

    # ---------------- TRẢ LỜI NGẮN (short) - CÂU 17 ----------------
            {
                "id": "de1_sh_17",
                "type": "short",
                "content": "Cho hình chóp S.ABC có độ dài ba cạnh bên bằng nhau \\( SA=SB=SC=a \\). Các góc ở đỉnh S lần lượt được cho bởi: \\( \\widehat{ASB}=60^\\circ \\), \\( \\widehat{BSC}=90^\\circ \\) và \\( \\widehat{CSA}=120^\\circ \\). Gọi \\( \\alpha \\) là góc tạo bởi hai mặt phẳng (SAB) và (SAC). Tính giá trị của \\( \\cos\\alpha \\). (Điền đáp án dưới dạng phân số tối giản).",
                "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau17-de1.PNG",
                "blanks": [
                    {"label": "\\( \\cos\\alpha = \\)", "answers": ["1/3"]}
                ],
                "points": 1,
                "explanation": """Dựa vào các góc ở đỉnh S, ta tính được các cạnh đáy:
- Xét \\( \\Delta SAB \\) có \\( SA=SB=a \\) và \\( \\widehat{ASB}=60^\\circ \\) nên là tam giác đều \\( \\Rightarrow AB = a \\).
- Xét \\( \\Delta SBC \\) vuông cân tại S do \\( \\widehat{BSC}=90^\\circ \\) \\( \\Rightarrow BC = a\\sqrt{2} \\).
- Xét \\( \\Delta SAC \\) có \\( AC^2 = SA^2 + SC^2 - 2SA\\cdot SC\\cos 120^\\circ = 3a^2 \\Rightarrow AC = a\\sqrt{3} \\).

Ta thấy \\( AB^2 + BC^2 = a^2 + 2a^2 = 3a^2 = AC^2 \\), nên \\( \\Delta ABC \\) là tam giác vuông tại B.
Gọi H là hình chiếu vuông góc của S xuống mặt phẳng (ABC). Vì \\( SA=SB=SC \\) nên H là tâm đường tròn ngoại tiếp \\( \\Delta ABC \\). Do \\( \\Delta ABC \\) vuông tại B nên H chính là trung điểm của cạnh huyền AC.

Tính thể tích khối chóp S.ABC theo công thức góc ở đỉnh:
\\( V = \\dfrac{1}{6}SA\\cdot SB\\cdot SC\\sqrt{1+2\\cos 60^\\circ\\cos 90^\\circ\\cos 120^\\circ - \\cos^2 60^\\circ - \\cos^2 90^\\circ - \\cos^2 120^\\circ} = \\dfrac{a^3\\sqrt{2}}{12} \\).

Khoảng cách từ B đến mặt phẳng (SAC) là: 
\\( d(B, (SAC)) = \\dfrac{3V}{S_{\\Delta SAC}} = \\dfrac{3\\cdot \\frac{a^3\\sqrt{2}}{12}}{\\frac{a^2\\sqrt{3}}{4}} = \\dfrac{a\\sqrt{6}}{3} \\).

Trong \\( \\Delta SAB \\) đều, đường cao kẻ từ B xuống giao tuyến SA là \\( BH = \\dfrac{a\\sqrt{3}}{2} \\).
Góc \\( \\alpha \\) tạo bởi (SAB) và (SAC) được tính qua hệ thức: 
\\( \\sin\\alpha = \\dfrac{d(B, (SAC))}{BH} = \\dfrac{\\frac{a\\sqrt{6}}{3}}{\\frac{a\\sqrt{3}}{2}} = \\dfrac{2\\sqrt{2}}{3} \\).
Suy ra \\( \\cos\\alpha = \\sqrt{1 - \\sin^2\\alpha} = \\sqrt{1 - \\dfrac{8}{9}} = \\dfrac{1}{3} \\)."""
            },

            # ---------------- ĐÚNG / SAI (truefalse) - CÂU 18 ----------------
            {
                "id": "de1_tf_18",
                "type": "truefalse",
                "content": "Trong không gian, xét tính Đúng/Sai của các mệnh đề sau về quan hệ song song:",
                "statements": [
                    {"text": "Nếu hai mặt phẳng phân biệt cùng song song với một đường thẳng thì chúng song song với nhau.", "correct": False},
                    {"text": "Cho hai đường thẳng chéo nhau. Luôn tồn tại duy nhất một mặt phẳng chứa đường thẳng này và song song với đường thẳng kia.", "correct": True},
                    {"text": "Nếu mặt phẳng \\( (\\alpha) \\) chứa hai đường thẳng phân biệt cùng song song với mặt phẳng \\( (\\beta) \\) thì \\( (\\alpha) \\) song song với \\( (\\beta) \\).", "correct": False},
                    {"text": "Hình chiếu song song của hai đường thẳng chéo nhau lên một mặt phẳng (theo phương chiếu không song song với hai đường thẳng đó) có thể là hai đường thẳng song song.", "correct": True}
                ],
                "points": 1,
                "explanation": """a) Sai. Hai mặt phẳng đó có thể cắt nhau. Khi đó giao tuyến của chúng sẽ song song với đường thẳng đã cho.

b) Đúng. Đây là tính chất và hệ quả cơ bản trong SGK Hình học 11 về đường thẳng và mặt phẳng song song.

c) Sai. Hai đường thẳng phân biệt đó phải **cắt nhau** thì mới đủ điều kiện kết luận hai mặt phẳng song song. Nếu hai đường thẳng đó song song thì hai mặt phẳng vẫn có thể cắt nhau.

d) Đúng. Nếu mặt phẳng chiếu song song với một mặt phẳng đang chứa cả hai đường thẳng đó thì hình chiếu của chúng sẽ là hai đường thẳng song song."""
            },

            # ---------------- TRẢ LỜI NGẮN (short) - CÂU 19 ----------------
            {
                "id": "de1_sh_19",
                "type": "short",
                "content": "Cho hàm số \\( f(x) = \\sqrt{1+2x}\\sqrt[3]{1+3x}\\dots\\sqrt[2026]{1+2026x} \\). Tính giới hạn \\( L = \\lim_{x\\to 0}\\dfrac{f(x)-1}{x} \\).",
                "blanks": [
                    {"label": "L =", "answers": ["2025"]}
                ],
                "points": 1,
                "explanation": """Ta có dạng của giới hạn này chính là đạo hàm của hàm số tại \\( x=0 \\):
\\( L = \\lim_{x\\to 0}\\dfrac{f(x)-f(0)}{x-0} = f'(0) \\) (do dễ dàng nhận thấy \\( f(0) = 1 \\)).

Lấy logarith tự nhiên (ln) hai vế của hàm số, ta được: 
\\( \\ln f(x) = \\sum_{k=2}^{2026} \\dfrac{1}{k} \\ln(1+kx) \\).

Đạo hàm hai vế: 
\\( \\dfrac{f'(x)}{f(x)} = \\sum_{k=2}^{2026} \\dfrac{1}{k} \\cdot \\dfrac{k}{1+kx} = \\sum_{k=2}^{2026} \\dfrac{1}{1+kx} \\).

Thay \\( x = 0 \\) vào hệ thức trên, ta có:
\\( \\dfrac{f'(0)}{f(0)} = \\sum_{k=2}^{2026} 1 = (2026 - 2) + 1 = 2025 \\).
Do \\( f(0) = 1 \\) nên \\( f'(0) = 2025 \\). Vậy \\( L = 2025 \\)."""
            },

            # ---------------- KÉO THẢ (dragdrop) - CÂU 20 ----------------
           {
        "id": "de1_dd_20",
        "type": "dragdrop",
        "content": "Một chiếc xe đẩy chở một thanh thép cứng dài (đặt nằm ngang) đi qua một góc cua vuông góc nối giữa hai hành lang. Hành lang thứ nhất rộng 2.7 (m), hành lang thứ hai rộng 6.4 (m). Để thanh thép có thể lọt qua góc cua này mà không bị kẹt, chiều dài L của thanh thép phải thỏa mãn một giới hạn tối đa (Bỏ qua bề dày của thanh thép). Giả sử khi thanh thép bị kẹt cứng nhất, nó tạo với vách của hành lang thứ hai một góc là \\( \\theta \\). Kéo thả các kết quả sau vào các ô trống tương ứng:",
        "options_pool": [
            "\\( 12.5 \\)", 
            "\\( \\dfrac{3}{4} \\)", 
            "\\( 10.0 \\)", 
            "\\( \\dfrac{4}{3} \\)", 
            "\\( 8.0 \\)"
        ],
        "blanks": [
            {
                "label": "Tang của góc \\( \\theta \\) tại vị trí thanh thép bị kẹt hẹp nhất bằng:", 
                "answer": "\\( \\dfrac{4}{3} \\)"
            },
            {
                "label": "Tại vị trí kẹt, độ dài đoạn thanh thép tính từ mép góc cua đến vách hành lang thứ hai là: (m).", 
                "answer": "\\( 8.0 \\)"
            },
            {
                "label": "Chiều dài lớn nhất của thanh thép để có thể lọt qua được góc cua là: (m).", 
                "answer": "\\( 12.5 \\)"
            }
        ],
        "points": 1,
        "explanation": """Gọi \\( L \\) là chiều dài thanh thép khi đi qua góc cua và bị vướng sát vào cả mép góc cua bên trong và 2 vách hành lang bên ngoài. Khi đó chiều dài thanh thép được biểu diễn bằng hàm số theo góc \\( \\theta \\) là:
\\( L(\\theta) = \\dfrac{2.7}{\\cos\\theta} + \\dfrac{6.4}{\\sin\\theta} \\) (với \\( 0 < \\theta < \\dfrac{\\pi}{2} \\)).

Để thanh thép lọt qua được ở mọi góc độ, chiều dài thực của thanh phải nhỏ hơn hoặc bằng giá trị nhỏ nhất của hàm \\( L(\\theta) \\).
Ta lấy đạo hàm để tìm cực trị: 
\\( L'(\\theta) = \\dfrac{2.7\\sin\\theta}{\\cos^2\\theta} - \\dfrac{6.4\\cos\\theta}{\\sin^2\\theta} = 0 \\)
\\( \\Leftrightarrow 2.7\\sin^3\\theta = 6.4\\cos^3\\theta \\Leftrightarrow \\tan^3\\theta = \\dfrac{6.4}{2.7} = \\dfrac{64}{27} \\Leftrightarrow \\tan\\theta = \\dfrac{4}{3} \\).

Từ \\( \\tan\\theta = \\dfrac{4}{3} \\), ta suy ra \\( \\sin\\theta = \\dfrac{4}{5} = 0.8 \\) và \\( \\cos\\theta = \\dfrac{3}{5} = 0.6 \\).
- Chiều dài đoạn thanh thép tính từ góc cua sang hành lang thứ hai là: \\( \\dfrac{6.4}{\\sin\\theta} = \\dfrac{6.4}{0.8} = 8.0 \\) (m).
- Chiều dài cực đại của thanh thép (giá trị min của \\( L(\\theta) \\)) là: 
\\( L_{max} = \\dfrac{2.7}{\\cos\\theta} + \\dfrac{6.4}{\\sin\\theta} = \\dfrac{2.7}{0.6} + \\dfrac{6.4}{0.8} = 4.5 + 8.0 = 12.5 \\) (m)."""
    },
            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de1_mc_21',
                "type": 'mc4',
                "content": 'Tìm tất cả các giá trị thực của tham số \\( m \\) để đa thức \\( P(x) = x^4 - 4x^3 + 4x^2 + m \\) có thể phân tích thành dạng \\( P(x) = (x - a)^2 \\cdot Q(x) \\), trong đó \\( Q(x) \\) là một đa thức bậc hai và \\( a \\) là một hằng số thực.',
                "options": {
                    'A': '\\( m \\in \\{0; -1\\} \\)',
                    'B': '\\( m \\in \\{0; 1\\} \\)',
                    'C': '\\( m \\in \\{1; 2\\} \\)',
                    'D': '\\( m \\in \\{-1; 1\\} \\)',
                },
                "correct": 'A',
                "points": 1,
                "explanation": """Ta viết lại: \\( P(x) - m = x^4 - 4x^3 + 4x^2 = x^2(x-2)^2 \\), tức là \\( P(x) = x^2(x-2)^2 + m \\).

Để \\( P(x) \\) có nhân tử \\( (x-a)^2 \\) (với \\( Q(x) \\) bậc hai bất kỳ), điều kiện cần và đủ là \\( a \\) phải là nghiệm kép của \\( P(x) \\), nghĩa là:
\\( P(a) = 0 \\) và \\( P'(a) = 0 \\).

Ta có \\( P'(x) = 4x^3 - 12x^2 + 8x = 4x(x-1)(x-2) \\), suy ra \\( P'(x) = 0 \\Leftrightarrow x \\in \\{0; 1; 2\\} \\).

Xét từng trường hợp:
- \\( a = 0 \\): \\( P(0) = m = 0 \\Rightarrow m = 0 \\).
- \\( a = 2 \\): \\( P(2) = m = 0 \\Rightarrow m = 0 \\).
- \\( a = 1 \\): \\( P(1) = 1 - 4 + 4 + m = 1 + m = 0 \\Rightarrow m = -1 \\).

Kiểm tra lại:
+ Với \\( m = 0 \\): \\( P(x) = x^2(x-2)^2 = (x-0)^2\\cdot(x-2)^2 \\) — thỏa mãn (a = 0, Q(x) = (x-2)^2).
+ Với \\( m = -1 \\): \\( P(x) = [x(x-2)]^2 - 1 = (x^2-2x-1)(x^2-2x+1) = (x-1)^2(x^2-2x-1) \\) — thỏa mãn (a = 1, Q(x) = x^2-2x-1).

Vậy \\( m \\in \\{0; -1\\} \\). Đáp án A.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de1_sh_22',
                "type": 'short',
                "content": 'Một khối tháp nghệ thuật được xếp từ các khối lập phương nhỏ bằng nhau. Tầng trên cùng (tầng 1) có \\( 1^2 \\) khối, tầng thứ 2 từ trên xuống có \\( 3^2 \\) khối, tầng thứ 3 có \\( 5^2 \\) khối... Tầng thứ \\( n \\) có \\( (2n-1)^2 \\) khối. Gọi \\( V_n \\) là tổng số khối lập phương cần dùng để xếp được tháp có \\( n \\) tầng. Người ta bao quanh toàn bộ tháp này bằng một khối hộp chữ nhật ngoại tiếp sát nhất, có diện tích đáy là \\( (2n-1)^2 \\) và chiều cao là \\( n \\) (với đơn vị là cạnh của khối lập phương nhỏ). Gọi \\( V_{h\\hat{o}p} \\) là thể tích của khối hộp này. Tính giới hạn \\( L = \\lim_{n\\to+\\infty} \\dfrac{V_n}{V_{h\\hat{o}p}} \\). (Điền đáp án dưới dạng phân số tối giản).',
                "blanks": [
                    {"label": 'L =', "answers": ['1/3']},
                ],
                "points": 1,
                "explanation": """Tổng số khối của tháp \\( n \\) tầng là tổng bình phương \\( n \\) số lẻ đầu tiên:
\\( V_n = 1^2 + 3^2 + 5^2 + \\cdots + (2n-1)^2 = \\dfrac{n(2n-1)(2n+1)}{3} \\).

Thể tích khối hộp ngoại tiếp: \\( V_{h\\hat{o}p} = (2n-1)^2 \\cdot n \\).

Do đó:
\\( \\dfrac{V_n}{V_{h\\hat{o}p}} = \\dfrac{n(2n-1)(2n+1)/3}{n(2n-1)^2} = \\dfrac{2n+1}{3(2n-1)} \\).

Lấy giới hạn khi \\( n \\to +\\infty \\):
\\( L = \\lim_{n\\to+\\infty} \\dfrac{2n+1}{6n-3} = \\dfrac{2}{6} = \\dfrac{1}{3} \\).""",
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de1_tf_23",
                "type": "truefalse",
                "content": "Một quản giáo có 5 chiếc chìa khóa và 5 ổ khóa tương ứng. Tuy nhiên, các chìa khóa đã bị tháo khỏi chùm và trộn lẫn ngẫu nhiên. Người quản giáo chọn ngẫu nhiên từng chiếc chìa khóa để cắm vào từng ổ khóa (mỗi ổ cắm đúng 1 chìa). Xét tính Đúng/Sai của các mệnh đề sau:",
                "statements": [
                    {"text": "Số cách ghép 5 chìa khóa vào 5 ổ khóa là 120 cách.", "correct": True},
                    {"text": "Xác suất để có ĐÚNG 4 ổ khóa được mở thành công là \\( \\dfrac{1}{120} \\).", "correct": False},
                    {"text": "Xác suất để KHÔNG CÓ bất kỳ ổ khóa nào được mở thành công là \\( \\dfrac{11}{30} \\).", "correct": True},
                    {"text": "Xác suất để có ÍT NHẤT 1 ổ khóa được mở thành công là \\( \\dfrac{19}{30} \\).", "correct": True}
                ],
                "points": 1,
                "explanation": """a) Mỗi cách ghép chìa vào ổ là một hoán vị của 5 phần tử, nên số cách là \\( 5! = 120 \\) cách \\( \\Rightarrow \\) Đúng.

b) Vì phép ghép là một song ánh (hoán vị), nếu có đúng 4 ổ khóa được mở đúng thì ổ còn lại bắt buộc cũng phải đúng (do chỉ còn duy nhất 1 chìa cho 1 ổ). Vậy KHÔNG THỂ có đúng 4 ổ đúng — xác suất này bằng 0, không phải \\( \\dfrac{1}{120} \\) \\( \\Rightarrow \\) Sai.

c) Xác suất không có ổ khóa nào đúng chính là xác suất của một "mất thứ tự toàn phần" (derangement):
\\( D_5 = 5!\\left(1 - \\dfrac{1}{1!} + \\dfrac{1}{2!} - \\dfrac{1}{3!} + \\dfrac{1}{4!} - \\dfrac{1}{5!}\\right) = 44 \\).
Xác suất \\( = \\dfrac{44}{120} = \\dfrac{11}{30} \\) \\( \\Rightarrow \\) Đúng.

d) Xác suất có ít nhất 1 ổ đúng \\( = 1 - \\dfrac{11}{30} = \\dfrac{19}{30} \\) \\( \\Rightarrow \\) Đúng.""",
            },
            {
                "id": "de1_tf_24",
                "type": "truefalse",
                "content": "Định luật làm nguội của Newton phát biểu rằng: Tốc độ thay đổi nhiệt độ của một vật tỷ lệ thuận với chênh lệch nhiệt độ giữa vật đó và môi trường xung quanh. Công thức mô hình hóa nhiệt độ \\( T(t) \\) của vật sau thời gian \\( t \\) (phút) là \\( T(t) = T_{env} + (T_0 - T_{env})e^{-kt} \\), trong đó \\( T_{env} \\) là nhiệt độ môi trường, \\( T_0 \\) là nhiệt độ ban đầu của vật, và \\( k \\) là hằng số làm nguội. Một cốc cà phê vừa được pha xong có nhiệt độ 90°C được đặt trong phòng có nhiệt độ không đổi là 20°C. Sau đúng 10 phút, nhiệt độ của cốc cà phê giảm xuống còn 60°C. Xét tính Đúng/Sai của các mệnh đề sau:",
                "statements": [
                    {"text": "Giá trị của hằng số làm nguội \\( k \\) xấp xỉ bằng 0.056.", "correct": True},
                    {"text": "Sau 20 phút kể từ lúc pha, nhiệt độ của cốc cà phê là 40°C.", "correct": False},
                    {"text": "Cần nhiều hơn 30 phút để cốc cà phê nguội xuống mức 30°C.", "correct": True},
                    {"text": "Tốc độ giảm nhiệt độ của cốc cà phê trong quá trình làm nguội là một hằng số.", "correct": False}
                ],
                "points": 1,
                "explanation": """Ta có \\( T(t) = 20 + 70e^{-kt} \\) (vì \\( T_0 - T_{env} = 90-20=70 \\)).

a) Tại \\( t=10 \\): \\( 60 = 20 + 70e^{-10k} \\Rightarrow e^{-10k} = \\dfrac{4}{7} \\Rightarrow k = \\dfrac{\\ln(7/4)}{10} \\approx 0.0560 \\) \\( \\Rightarrow \\) Đúng.

b) Tại \\( t=20 \\): \\( T(20) = 20 + 70\\left(\\dfrac{4}{7}\\right)^2 = 20 + 70\\cdot\\dfrac{16}{49} \\approx 20+22.86 = 42.86°C \\), không phải 40°C \\( \\Rightarrow \\) Sai.

c) Giải \\( 30 = 20+70e^{-kt} \\Rightarrow e^{-kt} = \\dfrac{1}{7} \\Rightarrow t = \\dfrac{\\ln 7}{k} \\approx \\dfrac{1.9459}{0.0560} \\approx 34.8 \\) phút \\( > 30 \\) phút \\( \\Rightarrow \\) Đúng.

d) Tốc độ giảm nhiệt \\( T'(t) = -70k\\,e^{-kt} \\) phụ thuộc vào \\( t \\) (giảm dần theo thời gian), không phải hằng số \\( \\Rightarrow \\) Sai.""",
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de1_dd_25",
                "type": "dragdrop",
                "content": "Trên màn hình radar trạm kiểm soát không lưu, quỹ đạo bay của một máy bay trực thăng (H) được mô phỏng bởi đường cong \\( (C): y = x^2 - 4x + 5 \\). Cùng lúc đó, một tàu hỏa (T) di chuyển thẳng tắp theo đường ray có phương trình \\( d: y = 2x - 5 \\). Biết đơn vị tọa độ tính bằng kilômét. Để thực hiện nhiệm vụ thả hàng tiếp tế, máy bay (H) cần tiến đến vị trí M trên quỹ đạo sao cho khoảng cách từ máy bay đến tàu hỏa là ngắn nhất. Kéo và thả các phương án sau vào vị trí thích hợp:",
              
                "options_pool": [
                    "\\( 3 \\)",
                    "\\( 2 \\)",
                    "\\( \\sqrt{5} \\)",
                    "\\( \\dfrac{\\sqrt{5}}{5} \\)",
                    "\\( \\dfrac{1}{5} \\)"
                ],
                "blanks": [
                    {"label": "Hoành độ của vị trí M là:", "answer": "3"},
                    {"label": "Tung độ của vị trí M là:", "answer": "2"},
                    {"label": "Khoảng cách ngắn nhất giữa máy bay và tàu hỏa là: (km)", "answer": "\\dfrac{\\sqrt{5}}{5}"}
                ],
                "points": 1,
                "explanation": """Khoảng cách từ một điểm trên (C) đến đường thẳng d ngắn nhất khi tiếp tuyến của (C) tại điểm đó song song với d.

Đường thẳng d có hệ số góc bằng 2. Ta cần tìm điểm M trên (C) sao cho \\( y'(x) = 2 \\).

Ta có \\( y' = 2x - 4 \\). Giải \\( 2x - 4 = 2 \\Rightarrow x = 3 \\).

Khi đó \\( y = 3^2 - 4\\cdot 3 + 5 = 9 - 12 + 5 = 2 \\).

Vậy \\( M(3; 2) \\) — hoành độ \\( X = 3 \\), tung độ \\( Y = 2 \\).

Viết lại d dưới dạng tổng quát: \\( 2x - y - 5 = 0 \\).

Khoảng cách ngắn nhất:
\\( d(M, d) = \\dfrac{|2\\cdot 3 - 2 - 5|}{\\sqrt{2^2+(-1)^2}} = \\dfrac{|6-2-5|}{\\sqrt{5}} = \\dfrac{1}{\\sqrt{5}} = \\dfrac{\\sqrt{5}}{5} \\) (km).""",
            },


                      # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de1_sh_26',
                "type": 'short',
                "content": 'Một trường mầm non có 20 phần quà giống hệt nhau cần chia cho 4 lớp học: lớp Gấu, lớp Thỏ, lớp Mèo và lớp Cún. Cô giáo có quy định chia quà như sau: Lớp Gấu (lớp lớn tuổi nhất) nhận được ít nhất 2 phần quà; ba lớp còn lại (Thỏ, Mèo, Cún) yêu cầu số phần quà nhận được của mỗi lớp bắt buộc phải là một số lẻ (có thể nhận 1, 3, 5, . . . phần quà). Hỏi cô giáo có tất cả bao nhiêu cách chia quà thỏa mãn yêu cầu trên?',
                "blanks": [
                    {"label": 'Số cách chia =', "answers": ['120']},
                ],
                "points": 1,
                "explanation": """Gọi số quà của lớp Gấu, Thỏ, Mèo, Cún lần lượt là \\( g, t, m, c \\), với \\( g \\ge 2 \\) và \\( t, m, c \\) là các số lẻ dương.

Đặt \\( t = 2a+1, m = 2b+1, c = 2c'+1 \\) với \\( a, b, c' \\ge 0 \\).

Phương trình: \\( g + t + m + c = 20 \\Leftrightarrow g + 2(a+b+c') + 3 = 20 \\Leftrightarrow g = 17 - 2(a+b+c') \\).

Vì \\( 2(a+b+c') \\) luôn chẵn nên \\( g \\) phải lẻ. Kết hợp \\( g \\ge 2 \\), ta có \\( g \\in \\{3, 5, 7, 9, 11, 13, 15, 17\\} \\).

Với mỗi \\( g \\), đặt \\( s = \\dfrac{17-g}{2} = a+b+c' \\), số nghiệm nguyên không âm của \\( a+b+c'=s \\) là \\( \\binom{s+2}{2} \\).

\\( g=3 \\Rightarrow s=7 \\Rightarrow \\binom{9}{2}=36 \\)
\\( g=5 \\Rightarrow s=6 \\Rightarrow \\binom{8}{2}=28 \\)
\\( g=7 \\Rightarrow s=5 \\Rightarrow \\binom{7}{2}=21 \\)
\\( g=9 \\Rightarrow s=4 \\Rightarrow \\binom{6}{2}=15 \\)
\\( g=11 \\Rightarrow s=3 \\Rightarrow \\binom{5}{2}=10 \\)
\\( g=13 \\Rightarrow s=2 \\Rightarrow \\binom{4}{2}=6 \\)
\\( g=15 \\Rightarrow s=1 \\Rightarrow \\binom{3}{2}=3 \\)
\\( g=17 \\Rightarrow s=0 \\Rightarrow \\binom{2}{2}=1 \\)

Tổng số cách: \\( 36+28+21+15+10+6+3+1 = 120 \\) cách.""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de1_mc_27',
                "type": 'mc4',
                "content": 'Với mỗi số nguyên \\( n \\ge 2 \\), xét phương trình \\( x^n + nx - 1 = 0 \\). Phương trình này luôn có một nghiệm dương duy nhất, kí hiệu là \\( x_n \\). Tính giới hạn \\( L = \\lim_{n\\to+\\infty}(n \\cdot x_n) \\).',
                "options": {
                    'A': '\\( L = 0 \\)',
                    'B': '\\( L = \\dfrac{1}{2} \\)',
                    'C': '\\( L = 1 \\)',
                    'D': '\\( L = e \\)',
                },
                "correct": 'C',
                "points": 1,
                "explanation": """Xét hàm \\( f(x) = x^n + nx - 1 \\) trên \\( (0; +\\infty) \\). Ta có \\( f(0) = -1 < 0 \\) và \\( f(1) = n > 0 \\), nên \\( x_n \\in (0; 1) \\) và duy nhất do \\( f \\) đồng biến trên \\( (0;+\\infty) \\).

Ta chứng minh \\( x_n \\to 0 \\) khi \\( n \\to \\infty \\): giả sử \\( x_n \\to c \\in [0;1] \\). Nếu \\( c > 0 \\) và \\( c < 1 \\) thì \\( x_n^n \\to 0 \\), khi đó từ phương trình \\( x_n^n + nx_n = 1 \\), ta cần \\( nx_n \\to 1 \\), suy ra \\( x_n \\to 0 \\) (mâu thuẫn với \\( c>0 \\) trừ khi ta xét đúng tốc độ hội tụ). Điều này cho thấy \\( x_n \\sim \\dfrac{1}{n} \\).

Cụ thể: vì \\( x_n \\to 0 \\), ta có \\( x_n^n \\to 0 \\) rất nhanh (do \\( x_n \\) nhỏ hơn 1 và giảm về 0 khi \\( n\\to\\infty \\)) — thực tế \\( x_n^n = \\left(\\dfrac{1+o(1)}{n}\\right)^n \\to 0 \\).

Từ phương trình gốc: \\( n x_n = 1 - x_n^n \\to 1 - 0 = 1 \\).

Vậy \\( L = \\lim_{n\\to+\\infty} n x_n = 1 \\). Đáp án C.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de1_sh_28',
                "type": 'short',
                "content": 'Từ một tấm bìa hình tròn bán kính \\( R \\), người ta cắt bỏ đi một hình quạt tròn và cuộn phần còn lại thành một chiếc phễu hình nón (khi cuộn, hai bán kính của hình quạt chập lại vào nhau). Để chiếc phễu hình nón chứa được thể tích lớn nhất, tỉ số giữa độ dài cung tròn bị cắt bỏ so với chu vi ban đầu của tấm bìa tròn phải có dạng \\( \\dfrac{p - \\sqrt{q}}{r} \\), trong đó \\( p, q, r \\) là các số nguyên dương phân biệt và phân số đã tối giản. Tính tổng \\( S = p + q + r \\).',
                "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau28-de1.PNG",
                "blanks": [
                    {"label": 'S =', "answers": ['12']},
                ],
                "points": 1,
                "explanation": """Sau khi cắt bỏ hình quạt, phần còn lại có bán kính (đường sinh của nón) \\( l = R \\) (không đổi khi cuộn).

Gọi \\( r \\) là bán kính đáy nón tạo thành, \\( h \\) là chiều cao: \\( h = \\sqrt{R^2 - r^2} \\).

Thể tích: \\( V = \\dfrac{1}{3}\\pi r^2 h = \\dfrac{1}{3}\\pi r^2\\sqrt{R^2-r^2} \\).

Xét \\( f(r) = r^4(R^2 - r^2) \\) (tỉ lệ với \\( V^2 \\)). Đạo hàm:
\\( f'(r) = 4r^3(R^2-r^2) - 2r^5 = 2r^3(2R^2 - 3r^2) = 0 \\Rightarrow r^2 = \\dfrac{2R^2}{3} \\Rightarrow r = R\\sqrt{\\dfrac{2}{3}} = \\dfrac{R\\sqrt6}{3} \\).

Vì cung tròn của phần giữ lại (chu vi đáy nón) bằng \\( 2\\pi r \\), trong khi chu vi ban đầu tấm bìa là \\( 2\\pi R \\), nên tỉ lệ phần GIỮ LẠI so với chu vi ban đầu là:
\\( \\dfrac{2\\pi r}{2\\pi R} = \\dfrac{r}{R} = \\dfrac{\\sqrt6}{3} \\).

Suy ra tỉ lệ phần BỊ CẮT BỎ so với chu vi ban đầu:
\\( 1 - \\dfrac{\\sqrt6}{3} = \\dfrac{3-\\sqrt6}{3} \\).

Vậy \\( p=3, q=6, r=3 \\Rightarrow S = 3+6+3 = 12 \\).""",
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de1_tf_29",
                "type": "truefalse",
                "content": "Trong một gian hàng hội chợ, người chơi gieo một con xúc xắc cân đối và đồng chất. Luật chơi như sau: - Nếu gieo ra mặt 6 chấm: Người chơi được thưởng ngay 100 nghìn đồng và được quyền gieo tiếp. - Nếu gieo ra mặt 4 hoặc 5 chấm: Người chơi được thưởng 50 nghìn đồng và trò chơi kết thúc. - Nếu gieo ra mặt 1, 2, 3 chấm: Người chơi bị phạt mất 20 nghìn đồng và trò chơi kết thúc. Trò chơi chỉ kết thúc khi người chơi gieo vào mặt yêu cầu dừng. Xét tính Đúng/Sai của các mệnh đề sau:",
                "statements": [
                    {"text": "Xác suất để trò chơi kết thúc ngay sau lần gieo đầu tiên là \\( \\dfrac{5}{6} \\).", "correct": True},
                    {"text": "Xác suất để một người chơi kiếm được chính xác 150 nghìn đồng từ trò chơi này là \\( \\dfrac{1}{36} \\).", "correct": False},
                    {"text": "Xác suất để một lượt chơi kéo dài từ 3 lần gieo trở lên là \\( \\dfrac{1}{36} \\).", "correct": True},
                    {"text": "Trung bình (kỳ vọng), mỗi lượt tham gia trò chơi này người chơi sẽ lãi 28 nghìn đồng.", "correct": True}
                ],
                "points": 1,
                "explanation": """a) Trò chơi kết thúc ngay sau lần gieo đầu \\( \\Leftrightarrow \\) không ra mặt 6 (mặt 6 mới được gieo tiếp). \\( P = \\dfrac{5}{6} \\Rightarrow \\) Đúng.

b) Vì trò chơi chỉ kết thúc bằng đúng 1 lần thắng (+50) hoặc 1 lần thua (−20) sau một chuỗi các lần ra mặt 6 (+100 mỗi lần), tổng tiền kiếm được sau \\( k \\) lần ra mặt 6 rồi kết thúc là \\( 100k + 50 \\) (nếu kết thúc bằng thắng) hoặc \\( 100k - 20 \\) (nếu kết thúc bằng thua).
Để tổng \\( =150 \\): \\( 100k+50=150 \\Rightarrow k=1 \\) (kết thúc bằng thắng, hợp lệ); \\( 100k-20=150 \\) không cho \\( k \\) nguyên.
Vậy chỉ có trường hợp: gieo 6 (1 lần) rồi gieo 4 hoặc 5.
\\( P = \\dfrac{1}{6}\\cdot\\dfrac{2}{6} = \\dfrac{1}{18} \\), không phải \\( \\dfrac{1}{36} \\Rightarrow \\) Sai.

c) Lượt chơi kéo dài từ 3 lần gieo trở lên \\( \\Leftrightarrow \\) hai lần gieo đầu đều ra mặt 6.
\\( P = \\left(\\dfrac{1}{6}\\right)^2 = \\dfrac{1}{36} \\Rightarrow \\) Đúng.

d) Gọi \\( E \\) là kỳ vọng tiền lãi mỗi lượt chơi. Ta có phương trình đệ quy:
\\( E = \\dfrac{1}{6}(100+E) + \\dfrac{1}{3}(50) + \\dfrac{1}{2}(-20) \\)
Nhân 6 vế: \\( 6E = (100+E) + 100 - 60 = 140 + E \\)
\\( \\Rightarrow 5E = 140 \\Rightarrow E = 28 \\) (nghìn đồng) \\( \\Rightarrow \\) Đúng.""",
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de1_dd_30",
                "type": "dragdrop",
                "content": "Trên một lưới tọa độ phẳng Oxy, một con kiến bắt đầu di chuyển từ gốc tọa độ O(0, 0) để tìm mồi tại điểm A(6, 6). Con kiến được lập trình sao cho ở mỗi bước, nó chỉ có thể đi sang phải 1 đơn vị hoặc đi lên trên 1 đơn vị. Đặc biệt, đường thẳng y = x là một bờ sông. Con kiến có thể bò sát mép bờ sông nhưng tuyệt đối không được vượt qua sông, nghĩa là tọa độ (x; y) của kiến tại mọi thời điểm phải luôn thỏa mãn x ≥ y. Kéo và thả các kết quả sau vào ô trống tương ứng:",
                "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau30-de1.PNG",
                "options_pool": [
                    "\\( 132 \\)",
                    "\\( \\dfrac{1}{14} \\)",
                    "\\( 924 \\)",
                    "\\( \\dfrac{1}{7} \\)",
                    "\\( 462 \\)"
                ],
                "blanks": [
                    {"label": "Tổng số đường đi ngắn nhất bất kì từ gốc O đến điểm A (không quan tâm bờ sông) là:", "answer": "924"},
                    {"label": "Số đường đi hợp lệ từ gốc O đến A mà con kiến không bị rơi xuống sông là:", "answer": "132"},
                    {"label": "Giả sử con kiến chọn ngẫu nhiên một con đường ngắn nhất từ O đến A, xác suất để nó đi đến đích an toàn là:", "answer": "\\dfrac{1}{7}"}
                ],
                "points": 1,
                "explanation": """Tổng số đường đi ngắn nhất từ O(0,0) đến A(6,6) (mỗi bước sang phải hoặc lên trên, tổng cộng 12 bước gồm 6 bước phải và 6 bước lên):
\\( \\binom{12}{6} = 924 \\) đường.

Số đường đi hợp lệ (luôn thỏa \\( x \\ge y \\), tức không vượt qua đường chéo \\( y=x \\)) chính là số đường đi Dyck, được tính bằng số Catalan:
\\( C_6 = \\dfrac{1}{7}\\binom{12}{6} = \\dfrac{924}{7} = 132 \\) đường.

Xác suất để con kiến chọn ngẫu nhiên một đường đi ngắn nhất và đến đích an toàn (không rơi xuống sông):
\\( P = \\dfrac{132}{924} = \\dfrac{1}{7} \\).""",
            },
                      # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de1_tf_31",
                "type": "truefalse",
                "content": "Cho khối tứ diện ABCD có thể tích bằng \\( V \\). Lấy các điểm M, N, P, Q lần lượt nằm trên các cạnh AB, BC, CD, DA sao cho các tỉ lệ đoạn thẳng thỏa mãn: \\( AM = 2MB \\), \\( BN = 2NC \\), \\( CP = 2PD \\), và \\( DQ = 2QA \\). Xét tính Đúng/Sai của các mệnh đề sau:",
                "statements": [
                    {"text": "Bốn điểm M, N, P, Q cùng nằm trên một mặt phẳng.", "correct": False},
                    {"text": "Hai đường thẳng MN và PQ là hai đường thẳng chéo nhau.", "correct": True},
                    {"text": "Thể tích của khối tứ diện M.BNP bằng \\( \\dfrac{4}{27} \\) thể tích khối tứ diện ABCD.", "correct": True},
                    {"text": "Tỉ số thể tích giữa khối chóp M.NCP và khối tứ diện ABCD bằng \\( \\dfrac{2}{27} \\).", "correct": True}
                ],
                "points": 1,
                "explanation": """Do tỉ số thể tích và quan hệ đồng phẳng bất biến qua phép biến đổi affine, ta chọn tứ diện chuẩn: \\( A(0,0,0), B(1,0,0), C(0,1,0), D(0,0,1) \\), khi đó \\( V_{ABCD} = \\dfrac{1}{6} \\).

Từ điều kiện tỉ lệ, ta có:
\\( M = A+\\dfrac{2}{3}(B-A) = \\left(\\dfrac{2}{3};0;0\\right) \\)
\\( N = B+\\dfrac{2}{3}(C-B) = \\left(\\dfrac{1}{3};\\dfrac{2}{3};0\\right) \\)
\\( P = C+\\dfrac{2}{3}(D-C) = \\left(0;\\dfrac{1}{3};\\dfrac{2}{3}\\right) \\)
\\( Q = D+\\dfrac{2}{3}(A-D) = \\left(0;0;\\dfrac{1}{3}\\right) \\)

a) Tính định thức \\( [\\vec{MN}, \\vec{MP}, \\vec{MQ}] \\), ta được kết quả khác 0 \\( \\Rightarrow \\) M, N, P, Q không đồng phẳng \\( \\Rightarrow \\) Sai.

b) Vì 4 điểm không đồng phẳng nên hai đường MN và PQ không thể cắt nhau (nếu cắt nhau thì 4 điểm phải đồng phẳng); đồng thời hai đường không song song (kiểm tra vectơ chỉ phương không cùng phương) \\( \\Rightarrow \\) MN và PQ chéo nhau \\( \\Rightarrow \\) Đúng.

c) Thể tích tứ diện M, B, N, P: 
\\( V_{MBNP} = \\dfrac{1}{6}\\left|\\det[\\vec{BM}',\\vec{NM}',\\vec{PM}']\\right| = \\dfrac{1}{6}\\cdot\\dfrac{4}{27} = \\dfrac{2}{81} \\)
Tỉ số: \\( \\dfrac{V_{MBNP}}{V_{ABCD}} = \\dfrac{2/81}{1/6} = \\dfrac{4}{27} \\Rightarrow \\) Đúng.

d) Thể tích tứ diện M, N, C, P:
\\( V_{MNCP} = \\dfrac{1}{6}\\cdot\\dfrac{2}{27} = \\dfrac{1}{81} \\)
Tỉ số: \\( \\dfrac{V_{MNCP}}{V_{ABCD}} = \\dfrac{1/81}{1/6} = \\dfrac{2}{27} \\Rightarrow \\) Đúng.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de1_sh_32',
                "type": 'short',
                "content": 'Một đội nghiên cứu lâm nghiệp đo chiều cao của 100 cây bạch đàn trong một khu rừng sinh thái. Số liệu được ghi chép và biểu diễn dưới dạng bảng phân bố tần số ghép nhóm như sau: Báo cáo cho biết trung vị của mẫu số liệu trên chính xác bằng 176 (cm). Biết x, y là các số nguyên dương. Tính hiệu số \\( S = y - x \\).',
                "image": 'https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau32-de1.PNG',
              "blanks": [
                    {"label": 'S =', "answers": ['3']},
                ],
                "points": 1,
                "explanation": """Tổng số cây: \\( 10+x+40+y+15=100 \\Rightarrow x+y=35 \\).

Vì trung vị \\( =176 \\in [170;180) \\), nên nhóm chứa trung vị là \\( [170;180) \\) với \\( L=170, f=40, h=10 \\), và tần số tích lũy trước nhóm này là \\( CF = 10+x \\).

Công thức trung vị:
\\( M_e = L + \\dfrac{\\frac{N}{2} - CF}{f}\\cdot h \\)
\\( 176 = 170 + \\dfrac{50-(10+x)}{40}\\cdot 10 \\)
\\( 6 = \\dfrac{40-x}{4} \\)
\\( 24 = 40 - x \\Rightarrow x = 16 \\)

Suy ra \\( y = 35 - 16 = 19 \\).

Kiểm tra: \\( CF=10+16=26 < 50 \\) và \\( CF+f=66\\ge 50 \\) — thỏa mãn nhóm chứa trung vị.

Vậy \\( S = y - x = 19 - 16 = 3 \\).""",
            },
            {
                "id": 'de1_sh_33',
                "type": 'short',
                "content": 'Cho dãy số \\( (u_n) \\) được xác định bởi điều kiện ban đầu \\( u_1 = 2026 \\) và hệ thức truy hồi \\( u_{n+1} = u_n^2 - u_n + 1 \\) với mọi số nguyên dương \\( n \\ge 1 \\). Đặt \\( S_n = \\dfrac{1}{u_1} + \\dfrac{1}{u_2} + \\cdots + \\dfrac{1}{u_n} \\) là tổng của n số hạng đầu tiên của dãy nghịch đảo. Tính giới hạn \\( L = \\lim_{n\\to+\\infty} S_n \\). (Điền đáp án dưới dạng phân số tối giản).',
                "blanks": [
                    {"label": 'L =', "answers": ['1/2025']},
                ],
                "points": 1,
                "explanation": """Từ hệ thức truy hồi: \\( u_{n+1} - 1 = u_n^2 - u_n = u_n(u_n-1) \\).

Suy ra: \\( \\dfrac{1}{u_{n+1}-1} = \\dfrac{1}{u_n(u_n-1)} = \\dfrac{1}{u_n-1} - \\dfrac{1}{u_n} \\) (phân tích thành phân thức đơn giản).

Do đó: \\( \\dfrac{1}{u_n} = \\dfrac{1}{u_n-1} - \\dfrac{1}{u_{n+1}-1} \\).

Tổng \\( S_n \\) là tổng viễn vọng (telescoping):
\\( S_n = \\sum_{k=1}^{n}\\left(\\dfrac{1}{u_k-1}-\\dfrac{1}{u_{k+1}-1}\\right) = \\dfrac{1}{u_1-1} - \\dfrac{1}{u_{n+1}-1} \\)

Vì \\( u_1=2026>2 \\), dãy \\( (u_n) \\) tăng rất nhanh và \\( u_n \\to +\\infty \\), nên \\( \\dfrac{1}{u_{n+1}-1}\\to 0 \\).

Vậy \\( L = \\dfrac{1}{u_1-1} = \\dfrac{1}{2025} \\).""",
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de1_dd_34",
                "type": "dragdrop",
                "content": "Một kĩ sư thiết kế cần chế tạo một chiếc bồn chứa nước hình trụ đứng có nắp đậy với thể tích sức chứa bắt buộc là \\( 32\\pi \\) (m³). Khảo sát giá thành vật liệu trên thị trường cho thấy: chi phí tấm kim loại dùng làm mặt đáy và nắp đậy là 200 nghìn đồng cho mỗi mét vuông; chi phí vật liệu làm mặt xung quanh bồn là 100 nghìn đồng cho mỗi mét vuông. Kéo thả các thông số kĩ thuật tối ưu vào ô trống sao cho chi phí chế tạo bồn chứa là thấp nhất có thể.",
                "options_pool": [
                    "\\( 4 \\)",
                    "\\( 4.8\\pi \\)",
                    "\\( 2 \\)",
                    "\\( 8 \\)",
                    "\\( 3.6\\pi \\)"
                ],
                "blanks": [
                    {"label": "Bán kính đáy tối ưu R của bồn chứa là: (m)", "answer": "2"},
                    {"label": "Chiều cao tối ưu h của bồn chứa là: (m)", "answer": "8"},
                    {"label": "Tổng chi phí thấp nhất để mua vật liệu là: (triệu đồng)", "answer": "4.8\\pi"}
                ],
                "points": 1,
                "explanation": """Gọi \\( R \\) (m) là bán kính đáy, \\( h \\) (m) là chiều cao bồn trụ.

Thể tích: \\( \\pi R^2 h = 32\\pi \\Rightarrow h = \\dfrac{32}{R^2} \\).

Chi phí (đơn vị nghìn đồng):
- Đáy và nắp: \\( 200\\cdot 2\\pi R^2 = 400\\pi R^2 \\)
- Xung quanh: \\( 100\\cdot 2\\pi R h = 200\\pi R h \\)

Tổng chi phí: \\( C(R) = 400\\pi R^2 + 200\\pi R\\cdot\\dfrac{32}{R^2} = 400\\pi R^2 + \\dfrac{6400\\pi}{R} \\).

Đạo hàm: \\( C'(R) = 800\\pi R - \\dfrac{6400\\pi}{R^2} \\).

Giải \\( C'(R)=0 \\Leftrightarrow 800R = \\dfrac{6400}{R^2} \\Leftrightarrow R^3 = 8 \\Leftrightarrow R = 2 \\) (m).

Suy ra \\( h = \\dfrac{32}{4} = 8 \\) (m).

Chi phí thấp nhất: \\( C(2) = 400\\pi\\cdot 4 + \\dfrac{6400\\pi}{2} = 1600\\pi + 3200\\pi = 4800\\pi \\) (nghìn đồng) \\( = 4.8\\pi \\) (triệu đồng).""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de1_mc_35',
                "type": 'mc4',
                "content": 'Cho ba số thực a, b, c lập thành một cấp số cộng theo thứ tự đó và có tổng bằng 15. Biết rằng dãy số đang xét là một dãy số tăng. Nếu người ta cộng thêm 1 vào số a, cộng thêm 1 vào số b và cộng thêm 4 vào số c, thì ba số mới nhận được sẽ lập thành một cấp số nhân. Tính giá trị biểu thức \\( P = a^2 + b^2 + c^2 \\).',
                "options": {
                    'A': '\\( P = 93 \\)',
                    'B': '\\( P = 147 \\)',
                    'C': '\\( P = 75 \\)',
                    'D': '\\( P = 83 \\)',
                },
                "correct": 'A',
                "points": 1,
                "explanation": """Vì a, b, c là cấp số cộng có tổng 15, nên \\( b \\) là số hạng giữa: \\( 3b = 15 \\Rightarrow b = 5 \\).

Đặt công sai \\( d > 0 \\) (do dãy tăng): \\( a = 5-d, \\; c = 5+d \\).

Ba số mới \\( a+1, b+1, c+4 \\) tức là \\( 6-d, \\; 6, \\; 9+d \\) lập thành cấp số nhân:
\\( 6^2 = (6-d)(9+d) \\)
\\( 36 = 54 + 6d - 9d - d^2 \\)
\\( 36 = 54 - 3d - d^2 \\)
\\( d^2 + 3d - 18 = 0 \\)

Giải: \\( \\Delta = 9+72=81, \\sqrt{\\Delta}=9 \\)
\\( d = \\dfrac{-3+9}{2} = 3 \\) hoặc \\( d = \\dfrac{-3-9}{2} = -6 \\) (loại vì \\( d>0 \\)).

Vậy \\( d = 3 \\Rightarrow a = 5-3=2, \\; b=5, \\; c=5+3=8 \\) (thỏa mãn tăng dần: 2 < 5 < 8).

\\( P = a^2+b^2+c^2 = 4+25+64 = 93 \\). Đáp án A.""",
            },
                      # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de1_dd_36",
                "type": "dragdrop",
                "content": "Trên một mặt phẳng, người ta đánh dấu 12 điểm phân biệt nằm trên một đường tròn. Nối tất cả các cặp điểm lại với nhau bằng các đoạn thẳng để tạo thành các dây cung. Giả sử các điểm được sắp xếp sao cho không có bất kỳ 3 dây cung nào đồng quy tại một điểm bên trong đường tròn. Kéo và thả các số liệu thích hợp vào ô trống:",
                "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau36-de1.PNG",
                "options_pool": [
                    "\\( 220 \\)",
                    "\\( 562 \\)",
                    "\\( 495 \\)",
                    "\\( 792 \\)",
                    "\\( 66 \\)"
                ],
                "blanks": [
                    {"label": "Tổng số dây cung được tạo ra là:", "answer": "66"},
                    {"label": "Số giao điểm của các dây cung nằm BÊN TRONG hình tròn là:", "answer": "495"},
                    {"label": "Số miền đa giác (số phần) mà hình tròn bị phân chia bởi các dây cung này là:", "answer": "562"}
                ],
                "points": 1,
                "explanation": """Tổng số dây cung: mỗi dây cung ứng với một cách chọn 2 điểm trong 12 điểm:
\\( \\binom{12}{2} = 66 \\) dây cung.

Số giao điểm bên trong: vì không có 3 dây cung nào đồng quy, mỗi giao điểm bên trong tương ứng duy nhất với một cách chọn 4 điểm trong 12 điểm (4 điểm tạo thành 1 tứ giác nội tiếp, hai đường chéo của nó cắt nhau tại đúng 1 điểm):
\\( \\binom{12}{4} = 495 \\) giao điểm.

Số miền: sử dụng công thức Euler cho bài toán chia hình tròn bởi các dây cung (không có 3 dây cung đồng quy):
\\( R = 1 + \\binom{n}{2} + \\binom{n}{4} \\)
\\( R = 1 + 66 + 495 = 562 \\) miền.""",
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de1_tf_37",
                "type": "truefalse",
                "content": "Một quả bóng cao su được thả rơi tự do theo phương thẳng đứng từ độ cao 10 m xuống mặt sàn cứng. Mỗi lần nảy lên, do ma sát và biến dạng, quả bóng bị mất đi 20% cơ năng so với trước khi chạm sàn (biết rằng cơ năng tỉ lệ thuận với độ cao tối đa đạt được). Gọi \\( h_n \\) là độ cao cực đại bóng đạt được sau lần chạm sàn thứ n (với \\( h_0=10 \\)). Giả sử gia tốc trọng trường \\( g=10 \\) m/s² và bỏ qua sức cản của không khí. Xét tính Đúng/Sai của các mệnh đề:",
                "statements": [
                    {"text": "Độ cao cực đại mà quả bóng đạt được ngay sau lần chạm sàn thứ 3 là 5.12 m.", "correct": True},
                    {"text": "Tổng quãng đường quả bóng di chuyển (lên và xuống) từ lúc thả đến khi dừng hẳn là 90 m.", "correct": True},
                    {"text": "Dãy số biểu diễn thời gian của mỗi lần bóng nảy lên rồi rơi xuống chạm sàn \\( (t_1, t_2, \\ldots) \\) là một cấp số nhân với công bội \\( q = 0.8 \\).", "correct": False},
                    {"text": "Tổng thời gian từ lúc thả bóng đến khi bóng hoàn toàn đứng yên trên mặt sàn nhỏ hơn 25 giây.", "correct": False}
                ],
                "points": 1,
                "explanation": """Vì cơ năng tỉ lệ thuận với độ cao, mất 20% cơ năng nghĩa là độ cao còn lại 80%, nên \\( h_n = 10\\cdot(0.8)^n \\).

a) \\( h_3 = 10\\cdot(0.8)^3 = 10\\cdot 0.512 = 5.12 \\) m \\( \\Rightarrow \\) Đúng.

b) Tổng quãng đường: \\( S = h_0 + 2\\sum_{n=1}^{\\infty}h_n = h_0 + \\dfrac{2h_0\\cdot 0.8}{1-0.8} = 10 + \\dfrac{16}{0.2} = 10+80=90 \\) m \\( \\Rightarrow \\) Đúng.

c) Thời gian rơi/nảy từ độ cao \\( h_n \\): \\( \\tau_n = \\sqrt{\\dfrac{2h_n}{g}} \\). Do đó thời gian mỗi lần nảy lên-rơi xuống là \\( t_n = 2\\sqrt{\\dfrac{2h_n}{g}} \\propto \\sqrt{h_n} \\propto \\sqrt{(0.8)^n} \\).
Công bội thực tế là \\( \\sqrt{0.8}\\approx 0.894 \\), không phải \\( 0.8 \\) \\( \\Rightarrow \\) Sai.

d) Thời gian rơi ban đầu: \\( t_0=\\sqrt{2\\cdot10/10}=\\sqrt2\\approx1.414 \\)s.
Tổng thời gian các lần nảy: \\( T_{bounce} = \\sum_{n=1}^\\infty 2\\sqrt{\\dfrac{2h_n}{g}} = 2\\sqrt2\\sum_{n=1}^\\infty(\\sqrt{0.8})^n = 2\\sqrt2\\cdot\\dfrac{\\sqrt{0.8}}{1-\\sqrt{0.8}}\\approx23.96 \\)s.
Tổng thời gian \\( T \\approx 1.414+23.96\\approx25.38 \\)s \\( > 25 \\)s \\( \\Rightarrow \\) Sai.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de1_sh_38',
                "type": 'short',
                "content": 'Một mảnh giấy hình chữ nhật ABCD có kích thước \\( AB=8 \\) (cm) và \\( BC=6 \\) (cm). Người ta gấp mảnh giấy dọc theo đường chéo AC sao cho mặt phẳng (DAC) vuông góc với mặt phẳng (BAC) tạo thành một khối tứ diện. Tính bình phương khoảng cách giữa hai đường thẳng chéo nhau AB và CD trong không gian (đơn vị: cm²). Biết đáp án là một phân số tối giản \\( \\dfrac{a}{b} \\) với \\( a,b\\in\\mathbb{N}^* \\), hãy tính tổng \\( S=a+b \\).',
                "blanks": [
                    {"label": 'S =', "answers": ['941']},
                ],
                "points": 1,
                "explanation": """Chọn hệ tọa độ với AC nằm trên trục Ox: \\( A(0,0,0), C(10,0,0) \\) (vì \\( AC=\\sqrt{8^2+6^2}=10 \\)).

Xác định B trong mặt phẳng đáy (z=0): \\( AB=8, CB=6 \\Rightarrow B\\left(\\dfrac{32}{5};\\dfrac{24}{5};0\\right) \\).

Xác định D: trước khi gấp, \\( AD=6, CD=8 \\Rightarrow \\) tọa độ (phẳng) là \\( \\left(\\dfrac{18}{5};-\\dfrac{24}{5}\\right) \\). Khi gấp sao cho (DAC) ⊥ (BAC), điểm D quay quanh trục AC (Ox) đến khi hình chiếu của D lên mặt phẳng đáy nằm trên chính trục AC (do đó thành phần y bằng 0):
\\( D\\left(\\dfrac{18}{5}; 0; \\dfrac{24}{5}\\right) \\).

Tính \\( \\vec{AB}=\\left(\\dfrac{32}{5};\\dfrac{24}{5};0\\right) \\), \\( \\vec{CD}=\\left(-\\dfrac{32}{5};0;\\dfrac{24}{5}\\right) \\).

\\( \\vec{AB}\\times\\vec{CD} = \\dfrac{1}{25}(576;-768;768) \\)

\\( \\vec{AC}=(10;0;0) \\), \\( \\vec{AC}\\cdot(\\vec{AB}\\times\\vec{CD}) = \\dfrac{5760}{25}=\\dfrac{1152}{5} \\)

Khoảng cách bình phương:
\\( d^2 = \\dfrac{\\left(\\dfrac{1152}{5}\\right)^2}{|\\vec{AB}\\times\\vec{CD}|^2} = \\dfrac{900}{41} \\) (cm²).

Vậy \\( a=900, b=41 \\Rightarrow S = 900+41 = 941 \\).""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de1_mc_39',
                "type": 'mc4',
                "content": 'Một công ty sản xuất ly giấy đựng nước giải khát có dạng hình nón. Để tiết kiệm chi phí nguyên vật liệu, kĩ sư thiết kế cần tối ưu hóa tỉ lệ giữa chiều cao h và bán kính đáy R của ly giấy sao cho diện tích mặt xung quanh của ly là nhỏ nhất nhưng vẫn chứa được đúng một thể tích \\( V_0 \\) cố định cho trước. Hỏi tỉ số \\( \\dfrac{h}{R} \\) đạt được khi tối ưu bằng bao nhiêu?',
                "options": {
                    'A': '\\( \\sqrt{2} \\)',
                    'B': '\\( 2\\sqrt{2} \\)',
                    'C': '\\( \\sqrt{3} \\)',
                    'D': '\\( \\dfrac{3}{2} \\)',
                },
                "correct": 'A',
                "points": 1,
                "explanation": """Thể tích: \\( V_0 = \\dfrac13\\pi R^2 h \\Rightarrow h = \\dfrac{3V_0}{\\pi R^2} \\).

Diện tích xung quanh: \\( S = \\pi R l \\) với \\( l=\\sqrt{R^2+h^2} \\).

Xét \\( f(R) = S^2/\\pi^2 = R^2(R^2+h^2) = R^4 + R^2h^2 \\). Thay \\( h^2 = \\dfrac{9V_0^2}{\\pi^2 R^4} \\):

\\( f(R) = R^4 + \\dfrac{9V_0^2}{\\pi^2 R^2} \\)

Đặt \\( x=R^2 \\): \\( g(x) = x^2 + \\dfrac{9V_0^2}{\\pi^2 x} \\)

\\( g'(x) = 2x - \\dfrac{9V_0^2}{\\pi^2 x^2} = 0 \\Rightarrow x^3 = \\dfrac{9V_0^2}{2\\pi^2} \\)

Tính tỉ số \\( \\dfrac{h}{R} = \\dfrac{3V_0}{\\pi R^3} = \\dfrac{3V_0}{\\pi x^{3/2}} \\).

Với \\( x^{3/2} = \\sqrt{x^3} = \\sqrt{\\dfrac{9V_0^2}{2\\pi^2}} = \\dfrac{3V_0}{\\pi\\sqrt2} \\), ta có:

\\( \\dfrac{h}{R} = \\dfrac{3V_0}{\\pi\\cdot\\dfrac{3V_0}{\\pi\\sqrt2}} = \\sqrt2 \\).

Đáp án A.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de1_sh_40',
                "type": 'short',
                "content": 'Cho hàm số \\( y = \\dfrac{m\\sin x + n\\cos x + 1}{\\sin x + 2\\cos x + 3} \\) (với m, n là các tham số nguyên). Biết rằng tập giá trị của hàm số này trên tập xác định là đoạn \\( [-1; 3] \\). Tính giá trị của biểu thức \\( T = m^2 + n^3 \\).',
                "blanks": [
                    {"label": 'T =', "answers": ['1']},
                ],
                "points": 1,
                "explanation": """Gọi \\( y_0 \\) là một giá trị của hàm số. Ta có:
\\( y_0(\\sin x+2\\cos x+3) = m\\sin x+n\\cos x+1 \\)
\\( \\Leftrightarrow (y_0-m)\\sin x + (2y_0-n)\\cos x = 1-3y_0 \\)

Phương trình có nghiệm x khi và chỉ khi:
\\( (y_0-m)^2+(2y_0-n)^2 \\ge (1-3y_0)^2 \\)

Khai triển và rút gọn, bất phương trình trở thành (theo biến \\( y_0 \\)):
\\( 4y_0^2 + (2m+4n-6)y_0 - (m^2+n^2-1) \\le 0 \\)

Vì tập giá trị đúng bằng \\( [-1;3] \\), nên -1 và 3 là hai nghiệm của phương trình bậc hai tương ứng (dấu bằng xảy ra ở biên). Theo Viète:

Tổng nghiệm: \\( -1+3=2 = \\dfrac{-(2m+4n-6)}{4} \\Rightarrow m+2n=-1 \\) (i)

Tích nghiệm: \\( -1\\cdot3=-3 = \\dfrac{-(m^2+n^2-1)}{4} \\Rightarrow m^2+n^2=13 \\) (ii)

Từ (i): \\( m=-1-2n \\). Thay vào (ii):
\\( (-1-2n)^2+n^2=13 \\Rightarrow 5n^2+4n-12=0 \\)
\\( \\Rightarrow n=1.2 \\) (loại, không nguyên) hoặc \\( n=-2 \\) (nhận).

Với \\( n=-2 \\Rightarrow m=-1-2(-2)=3 \\).

Kiểm tra: \\( m^2+n^2=9+4=13 \\) ✓ (thỏa (ii)).

Vậy \\( T = m^2+n^3 = 9 + (-8) = 1 \\).""",
            },
        ],   # kết thúc hết 1 đề
    },      # kết thúc hết 1 đề
    {
        "id": 'de2',
        "name": 'Đề số 2 - ÔN TẬP TSA ĐỢT 1 - 2027',
        "description": '40 câu hỏi ôn tập đợt 1.',
        "questions": [

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
                       # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_01',
                "type": 'short',
                "content": 'Một nhà máy sản xuất cần lắp đặt một đường ống dẫn nước từ trạm bơm A trên bờ biển (được coi là một đường thẳng) đến một giàn khoan B trên biển. Biết khoảng cách từ B đến bờ biển là \\( BH = 6 \\) km, và khoảng cách từ A đến H dọc theo bờ biển là \\( AH = 8 \\) km. Chi phí lắp đặt mỗi km đường ống trên bờ là 30.000 USD, và dưới biển là 50.000 USD. Người ta quyết định chọn một điểm M nằm trên đoạn AH để lắp đặt đường ống từ A đến M (trên bờ) và từ M đến B (dưới biển). Tính khoảng cách AM (theo km) để tổng chi phí lắp đặt là nhỏ nhất.',
                "blanks": [
                    {"label": 'AM =', "answers": ['3.5', '3,5', '7/2']},
                ],
                "points": 1,
                "explanation": """Đặt \\( HM = x \\) (với \\( 0 \\le x \\le 8 \\)). Suy ra \\( AM = 8-x \\).

Quãng đường ống dưới biển: \\( MB = \\sqrt{BH^2+HM^2} = \\sqrt{36+x^2} \\).

Hàm tổng chi phí (đơn vị: chục nghìn USD):
\\( f(x) = 3(8-x) + 5\\sqrt{36+x^2} \\)

Đạo hàm: \\( f'(x) = -3 + \\dfrac{5x}{\\sqrt{36+x^2}} \\)

Giải \\( f'(x)=0 \\):
\\( \\dfrac{5x}{\\sqrt{36+x^2}} = 3 \\Leftrightarrow 5x = 3\\sqrt{36+x^2} \\)
\\( \\Leftrightarrow 25x^2 = 9(36+x^2) \\Leftrightarrow 16x^2 = 324 \\)
\\( \\Rightarrow x^2 = \\dfrac{324}{16} \\Rightarrow x = 4.5 \\) (thỏa mãn \\( x\\in[0;8] \\))

Lập bảng biến thiên: tại \\( x=4.5 \\), hàm chi phí đạt cực tiểu.

Khi đó \\( AM = 8-4.5 = 3.5 \\) km.""",
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de2_dd_02",
                "type": "dragdrop",
                "content": "Cho khối nón \\( (N) \\) có bán kính đáy \\( R = 3 \\) cm và chiều cao \\( h = 4 \\) cm. Một mặt cầu \\( (S) \\) được gọi là nội tiếp khối nón nếu nó tiếp xúc với mặt đáy và tất cả các đường sinh của nón. Hãy kéo thả các giá trị số phù hợp vào các đại lượng tương ứng dưới đây:",
                "options_pool": [
                    "\\( 1.5 \\)",
                    "\\( 4.5\\pi \\)",
                    "\\( 5 \\)",
                    "\\( 15\\pi \\)",
                    "\\( 12\\pi \\)"
                ],
                "blanks": [
                    {"label": "Độ dài đường sinh l của khối nón bằng: (cm)", "answer": "5"},
                    {"label": "Diện tích xung quanh của khối nón bằng: (cm²)", "answer": "15\\pi"},
                    {"label": "Bán kính r của mặt cầu nội tiếp khối nón bằng: (cm)", "answer": "1.5"},
                    {"label": "Thể tích của khối cầu nội tiếp bằng: (cm³)", "answer": "4.5\\pi"}
                ],
                "points": 1,
                "explanation": """Đường sinh: \\( l = \\sqrt{R^2+h^2} = \\sqrt{3^2+4^2} = 5 \\).

Diện tích xung quanh nón: \\( S_{xq} = \\pi R l = \\pi\\cdot 3\\cdot 5 = 15\\pi \\).

Bán kính mặt cầu nội tiếp nón chính là bán kính đường tròn nội tiếp tam giác cân có đáy \\( 2R=6 \\) và cạnh bên \\( l=5 \\).

Nửa chu vi: \\( p = \\dfrac{5+5+6}{2} = 8 \\).

Diện tích tam giác cắt ngang: \\( S = \\dfrac{1}{2}\\cdot 2R\\cdot h = \\dfrac{1}{2}\\cdot 6\\cdot 4 = 12 \\).

Bán kính cầu: \\( r = \\dfrac{S}{p} = \\dfrac{12}{8} = 1.5 \\) (hoặc dùng công thức \\( r=\\dfrac{R\\cdot h}{R+l} \\)).

Thể tích khối cầu nội tiếp: \\( V = \\dfrac{4}{3}\\pi r^3 = \\dfrac{4}{3}\\pi(1.5)^3 = 4.5\\pi \\).""",
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de2_tf_03",
                "type": "truefalse",
                "content": "Một hộp chứa 10 quả cầu màu Đỏ, 8 quả cầu màu Xanh và 6 quả cầu màu Vàng. Các quả cầu chỉ khác nhau về màu sắc. Lấy ngẫu nhiên đồng thời 4 quả cầu từ hộp. Các nhận định sau đây là Đúng hay Sai?",
                "statements": [
                    {"text": "Không gian mẫu của phép thử có số phần tử là \\( C_{24}^4 = 10626 \\).", "correct": True},
                    {"text": "Số cách lấy được 4 quả cầu không có màu Vàng là 3060.", "correct": True},
                    {"text": "Xác suất để 4 quả cầu lấy ra có đúng 2 màu là \\( \\dfrac{5291}{10626} \\).", "correct": True},
                    {"text": "Xác suất để lấy được ít nhất 1 quả cầu Đỏ là \\( \\dfrac{9625}{10626} \\).", "correct": True}
                ],
                "points": 1,
                "explanation": """a) Tổng số quả cầu là \\( 10+8+6=24 \\). Lấy ngẫu nhiên 4 quả, số phần tử không gian mẫu \\( n(\\Omega) = C_{24}^4 = 10626 \\) \\( \\Rightarrow \\) Đúng.

b) Lấy 4 quả không có màu Vàng tức là chỉ lấy từ 18 quả Đỏ và Xanh. Số cách là \\( C_{18}^4 = 3060 \\) \\( \\Rightarrow \\) Đúng.

c) Dùng phần bù: \\( n(\\text{2 màu}) = n(\\Omega) - n(\\text{1 màu}) - n(\\text{3 màu}) \\).

Số cách lấy 4 quả cùng 1 màu: \\( C_{10}^4+C_8^4+C_6^4 = 210+70+15=295 \\).

Số cách lấy 4 quả có đủ 3 màu (dạng 2-1-1):
\\( C_{10}^2C_8^1C_6^1 + C_{10}^1C_8^2C_6^1 + C_{10}^1C_8^1C_6^2 = 45\\cdot48 + 10\\cdot28\\cdot6 + 10\\cdot8\\cdot15 = 5040 \\).

Số cách lấy 4 quả có đúng 2 màu: \\( 10626-295-5040=5291 \\). Xác suất \\( P=\\dfrac{5291}{10626} \\) \\( \\Rightarrow \\) Đúng.

d) Dùng biến cố đối "không lấy được quả Đỏ nào" (chỉ lấy trong 14 quả Xanh và Vàng). Số cách: \\( C_{14}^4 = 1001 \\). Số cách lấy ít nhất 1 Đỏ: \\( 10626-1001=9625 \\). \\( P=\\dfrac{9625}{10626} \\) \\( \\Rightarrow \\) Đúng.""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_04',
                "type": 'mc4',
                "content": 'Trong vật lý, mức cường độ âm L (đơn vị: dB) được tính bởi công thức \\( L = 10\\log\\left(\\dfrac{I}{I_0}\\right) \\), với I là cường độ âm và \\( I_0 \\) là cường độ âm chuẩn. Một người đứng cách một chiếc loa 10 m thì đo được mức cường độ âm là 80 dB. Giả sử sóng âm truyền đẳng hướng trong không gian và bỏ qua sự hấp thụ âm của môi trường (khi đó cường độ âm I tỉ lệ nghịch với bình phương khoảng cách từ nguồn tới điểm đo). Hỏi người đó phải di chuyển ra xa chiếc loa thêm bao nhiêu mét nữa để mức cường độ âm giảm xuống còn 60 dB?',
                "options": {
                    'A': '20 m',
                    'B': '90 m',
                    'C': '100 m',
                    'D': '50 m',
                },
                "correct": 'B',
                "points": 1,
                "explanation": """Hiệu hai mức cường độ âm:
\\( L_1 - L_2 = 10\\log\\left(\\dfrac{I_1}{I_0}\\right) - 10\\log\\left(\\dfrac{I_2}{I_0}\\right) = 10\\log\\left(\\dfrac{I_1}{I_2}\\right) \\)

Thay số: \\( 80-60=10\\log\\left(\\dfrac{I_1}{I_2}\\right) \\Leftrightarrow 20=10\\log\\left(\\dfrac{I_1}{I_2}\\right) \\Leftrightarrow \\log\\left(\\dfrac{I_1}{I_2}\\right)=2 \\Leftrightarrow \\dfrac{I_1}{I_2}=100 \\).

Do cường độ âm tỉ lệ nghịch với bình phương khoảng cách:
\\( \\dfrac{I_1}{I_2} = \\left(\\dfrac{d_2}{d_1}\\right)^2 \\Leftrightarrow 100=\\left(\\dfrac{d_2}{10}\\right)^2 \\Rightarrow \\dfrac{d_2}{10}=10 \\Rightarrow d_2=100 \\) (m)

Khoảng cách mới là 100 m. Vậy người đó cần di chuyển ra xa thêm: \\( 100-10=90 \\) m. Đáp án B.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_05',
                "type": 'short',
                "content": 'Trong hệ trục tọa độ Oxyz, cho mặt cầu \\( (S) \\) có tâm \\( I(1;-2;3) \\), bán kính \\( R=5 \\) và đường thẳng d có phương trình: \\( d: \\dfrac{x-1}{2} = \\dfrac{y+1}{1} = \\dfrac{z-2}{-2} \\). Biết đường thẳng d cắt mặt cầu (S) tại hai điểm phân biệt A và B. Tính diện tích tam giác IAB.',
                "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau05-de2.PNG",
                "blanks": [
                    {"label": 'S_IAB =', "answers": ['2√6', '2\\sqrt{6}']},
                ],
                "points": 1,
                "explanation": """Mặt cầu có tâm \\( I(1;-2;3) \\) và bán kính \\( R=5 \\). Đường thẳng d đi qua \\( M(1;-1;2) \\) và có VTCP \\( \\vec{u}=(2;1;-2) \\).

Tính vector \\( \\vec{IM} = (0;1;-1) \\).

Tích có hướng \\( [\\vec{IM},\\vec{u}] = (-1;-2;-2) \\).

Khoảng cách từ I đến d (đường cao IH của tam giác IAB):
\\( IH = \\dfrac{|[\\vec{IM},\\vec{u}]|}{|\\vec{u}|} = \\dfrac{\\sqrt{(-1)^2+(-2)^2+(-2)^2}}{\\sqrt{2^2+1^2+(-2)^2}} = \\dfrac{\\sqrt9}{\\sqrt9} = 1 \\)

Áp dụng định lý Pytago trong tam giác vuông IHA:
\\( HA = \\sqrt{IA^2-IH^2} = \\sqrt{R^2-IH^2} = \\sqrt{25-1} = \\sqrt{24} = 2\\sqrt6 \\)

Suy ra độ dài dây cung \\( AB = 2HA = 4\\sqrt6 \\).

Diện tích tam giác IAB:
\\( S_{IAB} = \\dfrac12\\cdot IH\\cdot AB = \\dfrac12\\cdot 1\\cdot 4\\sqrt6 = 2\\sqrt6 \\).""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_06',
                "type": 'mc4',
                "content": 'Trong không gian Oxyz, cho hai điểm \\( A(2;-4;4) \\), \\( B(5;-4;1) \\) và mặt phẳng \\( (P): x+2y-2z+5=0 \\). Gọi \\( M(a;b;c) \\) là điểm thuộc mặt phẳng (P) sao cho biểu thức \\( T = MA^2+2MB^2 \\) đạt giá trị nhỏ nhất. Tính tổng \\( S = a+b+c \\).',
                "options": {
                    'A': '\\( S = \\dfrac{7}{3} \\)',
                    'B': '\\( S = 7 \\)',
                    'C': '\\( S = \\dfrac{13}{3} \\)',
                    'D': '\\( S = -2 \\)',
                },
                "correct": 'A',
                "points": 1,
                "explanation": """Bước 1: Tìm điểm I thỏa mãn tâm tỉ cự \\( \\vec{IA}+2\\vec{IB}=\\vec{0} \\).

Tọa độ điểm I được tính bằng công thức trung bình có trọng số:
\\( x_I = \\dfrac{x_A+2x_B}{1+2} = \\dfrac{2+2\\cdot5}{3} = 4 \\)
\\( y_I = \\dfrac{y_A+2y_B}{1+2} = \\dfrac{-4+2\\cdot(-4)}{3} = -4 \\)
\\( z_I = \\dfrac{z_A+2z_B}{1+2} = \\dfrac{4+2\\cdot1}{3} = 2 \\)

Suy ra \\( I(4;-4;2) \\).

Bước 2: Phân tích biểu thức T theo I:
\\( T = (\\vec{MI}+\\vec{IA})^2 + 2(\\vec{MI}+\\vec{IB})^2 \\)
\\( = 3MI^2 + 2\\vec{MI}\\cdot(\\vec{IA}+2\\vec{IB}) + IA^2+2IB^2 \\)
\\( = 3MI^2 + IA^2+2IB^2 \\)

Vì A, B cố định nên I cố định \\( \\Rightarrow IA^2+2IB^2 \\) không đổi. Do đó, T nhỏ nhất khi và chỉ khi MI nhỏ nhất.

Mà \\( M\\in(P) \\), nên MI nhỏ nhất khi M là hình chiếu vuông góc của I lên (P).

Bước 3: Tìm tọa độ hình chiếu M.

Đường thẳng \\( \\Delta \\) đi qua I và vuông góc với (P) có VTCP \\( \\vec{n}_{(P)}=(1;2;-2) \\).

Phương trình tham số của \\( \\Delta \\):
\\( x=4+t,\\; y=-4+2t,\\; z=2-2t \\)

Thay tọa độ \\( \\Delta \\) vào phương trình mặt phẳng (P):
\\( (4+t)+2(-4+2t)-2(2-2t)+5=0 \\Leftrightarrow 9t-3=0 \\Leftrightarrow t=\\dfrac{1}{3} \\)

Thay \\( t=\\dfrac{1}{3} \\) vào \\( \\Delta \\), ta được tọa độ \\( M\\left(\\dfrac{13}{3};-\\dfrac{10}{3};\\dfrac{4}{3}\\right) \\).

Vậy \\( S=a+b+c=\\dfrac{13}{3}-\\dfrac{10}{3}+\\dfrac{4}{3}=\\dfrac{7}{3} \\). Đáp án A.""",
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de2_dd_07",
                "type": "dragdrop",
                "content": "Cho lăng trụ đứng ABC.A'B'C' có đáy ABC là tam giác vuông cân tại B, \\( AB=2a \\), chiều cao lăng trụ \\( AA'=3a \\). Kéo và thả các phương án lựa chọn thích hợp vào ô trống dưới đây để hoàn thiện các mệnh đề tính toán (lưu ý không phải phương án nào cũng được sử dụng hết):",
                "options_pool": [
                    "\\( 2a^2 \\)",
                    "\\( 4a^2 \\)",
                    "\\( 6a^3 \\)",
                    "\\( 12a^3 \\)",
                    "\\( \\dfrac{6a^3}{5} \\)"
                ],
                "blanks": [
                    {"label": "Diện tích của tam giác đáy ABC bằng:", "answer": "2a^2"},
                    {"label": "Thể tích của khối lăng trụ ABC.A'B'C' bằng:", "answer": "6a^3"},
                    {"label": "Thể tích của khối chóp A'.ABC bằng:", "answer": "2a^3"}
                ],
                "points": 1,
                "explanation": """Đáy ABC là tam giác vuông cân tại B với độ dài \\( AB=2a \\). Suy ra \\( BC=AB=2a \\).

Diện tích đáy: \\( S_{ABC}=\\dfrac12\\cdot AB\\cdot BC=\\dfrac12\\cdot2a\\cdot2a=2a^2 \\).

Lăng trụ đứng có chiều cao \\( h=AA'=3a \\).

Thể tích khối lăng trụ: \\( V_{ABC.A'B'C'}=S_{ABC}\\cdot h=2a^2\\cdot3a=6a^3 \\).

Thể tích khối chóp có cùng chung đáy và chiều cao với lăng trụ luôn bằng \\( \\dfrac13 \\) thể tích lăng trụ:
\\( V_{A'.ABC}=\\dfrac13\\cdot S_{ABC}\\cdot h=\\dfrac13\\cdot6a^3=2a^3 \\).

Lưu ý: giá trị \\( 2a^3 \\) không có sẵn trong ngân hàng đáp án gốc của đề — đây là điểm cần chọn đúng công thức tính toán (bằng \\( \\dfrac13 \\) lần lăng trụ) thay vì chọn nhầm theo các phương án nhiễu như \\( 4a^2, 12a^3, \\dfrac{6a^3}{5} \\).""",
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de2_tf_08",
                "type": "truefalse",
                "content": "Cho phương trình mũ: \\( 2^{x^2-1} = 3^{x+1} \\). Dựa vào kiến thức Logarit hóa, các mệnh đề sau đây là Đúng hay Sai?",
                "statements": [
                    {"text": "Phương trình đã cho tương đương với phương trình bậc hai: \\( x^2-(\\log_2 3)x-\\log_2 6=0 \\).", "correct": True},
                    {"text": "Phương trình có hai nghiệm phân biệt mang dấu trái ngược nhau.", "correct": True},
                    {"text": "Gọi S là tổng các nghiệm của phương trình đã cho, khi đó \\( 2^S=3 \\).", "correct": True},
                    {"text": "Phương trình có duy nhất một nghiệm nguyên và đó là một số nguyên âm.", "correct": True}
                ],
                "points": 1,
                "explanation": """Giải chi tiết phương trình (Logarit hóa hai vế cơ số 2):
\\( 2^{x^2-1}=3^{x+1} \\)
\\( \\Leftrightarrow \\log_2(2^{x^2-1}) = \\log_2(3^{x+1}) \\)
\\( \\Leftrightarrow x^2-1 = (x+1)\\log_2 3 \\)
\\( \\Leftrightarrow (x-1)(x+1) - (x+1)\\log_2 3 = 0 \\)
\\( \\Leftrightarrow (x+1)(x-1-\\log_2 3) = 0 \\)

Từ đó, ta có hai nghiệm: \\( x_1=-1 \\) và \\( x_2 = 1+\\log_2 3 = \\log_2 2+\\log_2 3 = \\log_2 6 \\).

a) Đa thức bậc hai nhận 2 nghiệm này là:
\\( (x+1)(x-\\log_2 6) = x^2-(\\log_2 6-1)x-\\log_2 6 = x^2-(\\log_2 3)x-\\log_2 6=0 \\) \\( \\Rightarrow \\) Đúng.

b) Hai nghiệm là \\( x_1=-1<0 \\) và \\( x_2=\\log_2 6>\\log_2 1=0 \\). Hai nghiệm trái dấu \\( \\Rightarrow \\) Đúng.

c) Tổng hai nghiệm \\( S=x_1+x_2=-1+\\log_2 6=\\log_2 3 \\).
Suy ra \\( 2^S = 2^{\\log_2 3}=3 \\) \\( \\Rightarrow \\) Đúng.

d) Tập nghiệm là \\( \\{-1;\\log_2 6\\} \\). Số \\( \\log_2 6 \\) là một số vô tỉ (khoảng 2.58). Nghiệm nguyên duy nhất là \\( -1 \\), và đây là số nguyên âm \\( \\Rightarrow \\) Đúng.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_09',
                "type": 'short',
                "content": 'Cho khối chóp tứ giác đều S.ABCD có tất cả các cạnh (cạnh đáy và cạnh bên) đều bằng a. Người ta tạo ra một hình nón (N) có đỉnh trùng với đỉnh S của khối chóp, và đường tròn đáy của hình nón chính là đường tròn ngoại tiếp hình vuông ABCD. Hãy tính số đo góc ở đỉnh của hình nón (N). (Đơn vị tính: độ, chỉ điền phần số).',
                
                "blanks": [
                    {"label": 'Góc ở đỉnh =', "answers": ['90']},
                ],
                "points": 1,
                "explanation": """Khối chóp S.ABCD có tất cả các cạnh bằng a.

Đáy ABCD là hình vuông cạnh a \\( \\Rightarrow \\) Đường chéo đáy là \\( BD=a\\sqrt2 \\).

Bán kính đường tròn ngoại tiếp đáy (cũng là bán kính đáy hình nón):
\\( R_{đáy} = OA = \\dfrac{BD}{2} = \\dfrac{a\\sqrt2}{2} \\)

Đường sinh của hình nón (N) chính là cạnh bên của khối chóp. Vậy \\( l=SA=a \\).

Gọi \\( \\alpha \\) là góc giữa đường cao SO và đường sinh SA (\\( \\alpha \\) là một nửa góc ở đỉnh của hình nón).

Trong tam giác vuông SOA vuông tại O:
\\( \\sin\\alpha = \\dfrac{OA}{SA} = \\dfrac{\\frac{a\\sqrt2}{2}}{a} = \\dfrac{\\sqrt2}{2} \\)

Suy ra \\( \\alpha = 45^\\circ \\).

Góc ở đỉnh của hình nón bằng \\( 2\\alpha = 2\\times45^\\circ = 90^\\circ \\).""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_10',
                "type": 'short',
                "content": 'Bạn Duy có hai đồng xu cân đối đồng chất, mỗi đồng xu có một mặt ghi số 2 và mặt còn lại ghi số 3. Bạn tung đồng thời hai đồng xu này, sau đó rút ngẫu nhiên một lá bài từ bộ bài 52 lá chuẩn. Biết xác suất để tổng các số trên hai mặt đồng xu lật ngửa bằng với con số ghi trên lá bài được rút (quy ước: các lá bài có số từ 2 đến 10 có giá trị tương ứng với con số trên lá; các lá J, Q, K, A coi như không có giá trị bằng số) được viết dưới dạng phân số tối giản \\( \\dfrac{a}{b} \\) (với \\( a, b \\in \\mathbb{N}^* \\)). Tính giá trị của biểu thức \\( T = a+b \\).',
                "blanks": [
                    {"label": 'T =', "answers": ['14']},
                ],
                "points": 1,
                "explanation": """Bước 1: Phân tích phép thử tung 2 đồng xu.

Mỗi đồng xu có 2 khả năng \\( \\{2,3\\} \\). Không gian mẫu khi tung 2 đồng xu có \\( 2\\times2=4 \\) phần tử.

Gọi X là tổng số ghi trên 2 đồng xu:
\\( X=4 \\) (2+2): 1 cách \\( \\Rightarrow P(X=4)=\\dfrac14 \\)
\\( X=5 \\) (2+3 hoặc 3+2): 2 cách \\( \\Rightarrow P(X=5)=\\dfrac24=\\dfrac12 \\)
\\( X=6 \\) (3+3): 1 cách \\( \\Rightarrow P(X=6)=\\dfrac14 \\)

Bước 2: Phân tích phép rút bài 52 lá.

Mỗi giá trị (ví dụ lá 4, 5, 6) đều xuất hiện đúng 4 lần trong bộ bài.

Gọi Y là con số ghi trên lá bài rút được:
\\( P(Y=k) = \\dfrac{4}{52} = \\dfrac{1}{13} \\) với \\( k\\in\\{2,3,...,10\\} \\)

Bước 3: Tính xác suất của biến cố mục tiêu.

Biến cố A: "Tổng số trên 2 đồng xu bằng số trên lá bài" \\( \\Leftrightarrow X=Y \\).

Vì 2 hành động độc lập, áp dụng công thức xác suất toàn phần:
\\( P(A) = P(X=4)P(Y=4)+P(X=5)P(Y=5)+P(X=6)P(Y=6) \\)
\\( = \\dfrac14\\cdot\\dfrac1{13}+\\dfrac24\\cdot\\dfrac1{13}+\\dfrac14\\cdot\\dfrac1{13} \\)
\\( = \\dfrac1{13}\\left(\\dfrac14+\\dfrac24+\\dfrac14\\right) = \\dfrac1{13}\\cdot1 = \\dfrac1{13} \\)

Phân số thu được là \\( \\dfrac1{13} \\), đã tối giản. Đồng nhất với \\( \\dfrac{a}{b} \\), ta được \\( a=1, b=13 \\).

Giá trị của \\( T=a+b=1+13=14 \\).""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_11',
                "type": 'mc4',
                "content": 'Cho hàm số: \\( y = \\dfrac{3\\tan x - 5}{1-\\sin^2 x} \\). Tập xác định của hàm số là:',
                "options": {
                    'A': '\\( D = \\mathbb{R}\\setminus\\left\\{\\dfrac{\\pi}{2}+k\\pi \\mid k\\in\\mathbb{Z}\\right\\} \\)',
                    'B': '\\( D = \\mathbb{R}\\setminus\\{k\\pi \\mid k\\in\\mathbb{Z}\\} \\)',
                    'C': '\\( D = \\mathbb{R}\\setminus\\left\\{\\dfrac{\\pi}{4}+k\\dfrac{\\pi}{2} \\mid k\\in\\mathbb{Z}\\right\\} \\)',
                    'D': '\\( D = \\mathbb{R}\\setminus\\left\\{\\dfrac{\\pi}{2}+k2\\pi \\mid k\\in\\mathbb{Z}\\right\\} \\)',
                },
                "correct": 'A',
                "points": 1,
                "explanation": """Hàm số xác định khi và chỉ khi thỏa mãn đồng thời hai điều kiện:
\\( \\cos x \\ne 0 \\) (điều kiện của \\( \\tan x \\))
\\( 1-\\sin^2 x \\ne 0 \\) (điều kiện mẫu số khác 0)

\\( \\Leftrightarrow \\begin{cases}\\cos x\\ne0\\\\ \\cos^2 x\\ne0\\end{cases} \\Leftrightarrow \\cos x\\ne0 \\)

\\( \\Leftrightarrow x \\ne \\dfrac{\\pi}{2}+k\\pi \\;(k\\in\\mathbb{Z}) \\)

Vậy tập xác định của hàm số là \\( D = \\mathbb{R}\\setminus\\left\\{\\dfrac{\\pi}{2}+k\\pi \\mid k\\in\\mathbb{Z}\\right\\} \\). Đáp án A.""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_12',
                "type": 'mc4',
                "content": 'Có 12 cây bút có chiều dài lập thành một cấp số cộng. Biết rằng cây bút thứ nhất dài 48 cm và cây thứ ba dài 42 cm. Cây bút cuối cùng trong bộ sưu tập này có chiều dài bằng bao nhiêu?',
                "options": {
                    'A': '12 cm',
                    'B': '15 cm',
                    'C': '16 cm',
                    'D': '18 cm',
                },
                "correct": 'B',
                "points": 1,
                "explanation": """Gọi chiều dài của 12 cây bút lần lượt là \\( u_1, u_2, \\ldots, u_{12} \\) lập thành cấp số cộng có công sai d.

Theo giả thiết, cây bút thứ nhất dài 48 cm và cây thứ ba dài 42 cm, suy ra:
\\( \\begin{cases} u_1 = 48 \\\\ u_3 = 42 \\end{cases} \\Leftrightarrow \\begin{cases} u_1=48 \\\\ u_1+2d=42 \\end{cases} \\)

\\( \\Rightarrow 48+2d=42 \\Leftrightarrow d=-3 \\)

Cây bút cuối cùng trong bộ sưu tập là \\( u_{12} \\). Áp dụng công thức số hạng tổng quát:
\\( u_{12} = u_1+11d = 48+11\\cdot(-3) = 15 \\) (cm)

Vậy cây bút cuối cùng dài 15 cm. Đáp án B.""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_13',
                "type": 'mc4',
                "content": 'Tính \\( L = \\lim\\limits_{x\\to0}\\dfrac{1-\\cos 2x}{x} \\).',
                "options": {
                    'A': '\\( L = 2 \\)',
                    'B': '\\( L = 1 \\)',
                    'C': '\\( L = 0 \\)',
                    'D': '\\( L = -2 \\)',
                },
                "correct": 'C',
                "points": 1,
                "explanation": """Sử dụng công thức nhân đôi \\( \\cos 2x = 1-2\\sin^2 x \\), ta biến đổi biểu thức giới hạn:

\\( L = \\lim\\limits_{x\\to0}\\dfrac{1-(1-2\\sin^2 x)}{x} = \\lim\\limits_{x\\to0}\\dfrac{2\\sin^2 x}{x} = \\lim\\limits_{x\\to0}\\left(2\\sin x\\cdot\\dfrac{\\sin x}{x}\\right) \\)

Áp dụng giới hạn cơ bản \\( \\lim\\limits_{x\\to0}\\dfrac{\\sin x}{x}=1 \\) và \\( \\lim\\limits_{x\\to0}\\sin x=0 \\), ta có:

\\( L = 2\\cdot0\\cdot1 = 0 \\). Đáp án C.""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_14',
                "type": 'mc4',
                "content": 'Cho cấp số nhân \\( (u_n) \\) thỏa mãn \\( u_2=6 \\) và \\( u_5=\\dfrac{3}{4} \\). Giá trị công bội q của cấp số nhân đã cho bằng:',
                "options": {
                    'A': '\\( q = 2 \\)',
                    'B': '\\( q = \\dfrac{1}{2} \\)',
                    'C': '\\( q = -\\dfrac{1}{2} \\)',
                    'D': '\\( q = 8 \\)',
                },
                "correct": 'B',
                "points": 1,
                "explanation": """Gọi \\( u_1 \\) là số hạng đầu và q là công bội của cấp số nhân. Theo định nghĩa:

\\( \\begin{cases} u_2 = u_1\\cdot q = 6 \\\\ u_5 = u_1\\cdot q^4 = \\dfrac34 \\end{cases} \\)

Lấy phương trình thứ hai chia cho phương trình thứ nhất vế theo vế (do \\( u_2\\ne0\\Rightarrow q\\ne0, u_1\\ne0 \\)):

\\( \\dfrac{u_1\\cdot q^4}{u_1\\cdot q} = \\dfrac{3/4}{6} \\Leftrightarrow q^3 = \\dfrac18 = \\left(\\dfrac12\\right)^3 \\)

Suy ra \\( q = \\dfrac12 \\). Đáp án B.""",
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_15',
                "type": 'mc4',
                "content": 'Cho hàm số: \\( y = 4\\sin^2 x + 3 \\). Giá trị nhỏ nhất của hàm số bằng:',
                "options": {
                    'A': '3',
                    'B': '4',
                    'C': '7',
                    'D': '-1',
                },
                "correct": 'A',
                "points": 1,
                "explanation": """Tập xác định: \\( D = \\mathbb{R} \\).

Ta biết rằng với mọi \\( x\\in\\mathbb{R} \\), ta luôn có:
\\( -1\\le\\sin x\\le1 \\Rightarrow 0\\le\\sin^2 x\\le1 \\)

Nhân các vế với 4 và cộng thêm 3, ta được:
\\( 0 \\le 4\\sin^2 x \\le 4 \\)
\\( \\Rightarrow 0+3 \\le 4\\sin^2 x+3 \\le 4+3 \\)
\\( \\Rightarrow 3 \\le y \\le 7 \\)

Do đó, giá trị nhỏ nhất của hàm số là 3. Dấu "=" xảy ra khi \\( \\sin^2 x=0 \\Leftrightarrow \\sin x=0 \\Leftrightarrow x=k\\pi \\;(k\\in\\mathbb{Z}) \\). Đáp án A.""",
            },

                      # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_16',
                "type": 'mc4',
                "content": 'Một bệnh nhân được tiêm một liều thuốc kháng sinh 500mg. Nghiên cứu y học động học cho thấy, sau mỗi giờ, lượng thuốc trong máu của bệnh nhân sẽ giảm đi 15% so với giờ trước đó do quá trình đào thải tự nhiên. Hỏi sau ít nhất bao nhiêu giờ thì lượng thuốc trong máu bệnh nhân giảm xuống dưới mức an toàn 100mg? (Giả sử bệnh nhân không được tiêm thêm thuốc trong suốt quá trình này).',
                "options": {
                    'A': '9 giờ',
                    'B': '10 giờ',
                    'C': '11 giờ',
                    'D': '12 giờ',
                },
                "correct": 'B',
                "points": 1,
                "explanation": """Đây là bài toán mô hình hóa thực tiễn dạng suy giảm mũ. Gọi \\( M(t) \\) là lượng thuốc trong máu sau t giờ kể từ lúc tiêm. Ban đầu lượng thuốc là \\( M(0)=500 \\)mg.

Vì mỗi giờ lượng thuốc giảm 15%, nghĩa là lượng thuốc còn lại sau mỗi giờ bằng 85% lượng thuốc của giờ ngay trước đó. Ta thiết lập được hàm số mô hình hóa lượng thuốc theo thời gian:
\\( M(t) = 500\\cdot(0.85)^t \\)

Để lượng thuốc trong máu giảm xuống dưới 100mg, ta cần giải bất phương trình:
\\( 500\\cdot(0.85)^t < 100 \\Leftrightarrow (0.85)^t < 0.2 \\)

Lấy logarit cơ số 0.85 hai vế. Lưu ý cơ số \\( 0.85<1 \\) nên bất đẳng thức đổi chiều:
\\( t > \\log_{0.85}(0.2) \\approx 9.903 \\)

Do yêu cầu tìm số giờ trọn vẹn (ít nhất) để lượng thuốc chắc chắn nằm dưới ngưỡng 100mg, ta chọn số nguyên nhỏ nhất thỏa mãn, tức là \\( t=10 \\).

Vậy sau ít nhất 10 giờ, lượng thuốc sẽ dưới mức 100mg. Đáp án B.""",
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de2_tf_17",
                "type": "truefalse",
                "content": "Cho hàm số phân thức \\( y = \\dfrac{2x-1}{x+1} \\). Xét tính đúng/sai của các mệnh đề sau đây:",
                "statements": [
                    {"text": "Đồ thị hàm số có tiệm cận đứng là đường thẳng \\( x=-1 \\) và tiệm cận ngang là đường thẳng \\( y=2 \\).", "correct": True},
                    {"text": "Hàm số đã cho đồng biến trên tập \\( \\mathbb{R}\\setminus\\{-1\\} \\).", "correct": False},
                    {"text": "Đồ thị hàm số cắt trục hoành tại điểm có hoành độ \\( x=\\dfrac12 \\).", "correct": True},
                    {"text": "Tâm đối xứng của đồ thị hàm số là điểm \\( I(1;2) \\).", "correct": False}
                ],
                "points": 1,
                "explanation": """a) Ta có \\( \\lim\\limits_{x\\to\\pm\\infty} y = \\lim\\limits_{x\\to\\pm\\infty}\\dfrac{2-1/x}{1+1/x}=2 \\), suy ra đường thẳng \\( y=2 \\) là tiệm cận ngang.

Lại có \\( \\lim\\limits_{x\\to-1^+}\\dfrac{2x-1}{x+1}=-\\infty \\), suy ra đường thẳng \\( x=-1 \\) là tiệm cận đứng \\( \\Rightarrow \\) Đúng.

b) Tập xác định \\( D=\\mathbb{R}\\setminus\\{-1\\} \\). Đạo hàm:
\\( y' = \\dfrac{2\\cdot1-(-1)\\cdot1}{(x+1)^2} = \\dfrac{3}{(x+1)^2} > 0,\\;\\forall x\\ne-1 \\)

Tuy nhiên, theo đúng chuẩn mực toán học, hàm số chỉ đồng biến trên từng khoảng xác định là \\( (-\\infty;-1) \\) và \\( (-1;+\\infty) \\). Không được dùng ký hiệu tập hợp \\( \\mathbb{R}\\setminus\\{-1\\} \\) để kết luận khoảng đơn điệu \\( \\Rightarrow \\) Sai.

c) Giao điểm với trục hoành thỏa mãn \\( y=0 \\Leftrightarrow \\dfrac{2x-1}{x+1}=0 \\Leftrightarrow 2x-1=0 \\Leftrightarrow x=\\dfrac12 \\) \\( \\Rightarrow \\) Đúng.

d) Tâm đối xứng của đồ thị hàm phân thức bậc nhất/bậc nhất chính là giao điểm của hai đường tiệm cận. Tiệm cận đứng \\( x=-1 \\), tiệm cận ngang \\( y=2 \\) nên tâm đối xứng phải là điểm \\( I(-1;2) \\), chứ không phải \\( I(1;2) \\) \\( \\Rightarrow \\) Sai.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_18',
                "type": 'short',
                "content": 'Trong mật mã học RSA, phép toán lũy thừa mô-đun (chia lấy dư) đóng vai trò cốt lõi trong việc tạo khóa bảo mật. Áp dụng tư duy thuật toán, hãy tìm số dư của phép chia \\( 2^{2026} \\) cho 7.',
                "blanks": [
                    {"label": 'Số dư =', "answers": ['2']},
                ],
                "points": 1,
                "explanation": """Để xử lý số mũ cực lớn, ta sử dụng tính chất của đồng dư thức (Modulo arithmetic). Ta tìm một lũy thừa cơ sở của 2 sao cho giá trị của nó gần với một bội số của 7. Nhận thấy \\( 2^3=8 \\) chia 7 dư 1. Do đó, ta có thể viết dưới dạng đồng dư:
\\( 2^3 \\equiv 1 \\pmod{7} \\)

Tiếp theo, ta phân tích số mũ 2026 theo cơ số 3 bằng phép chia có dư:
\\( 2026 = 3\\times675+1 \\)

Khi đó, ta tách biểu thức lũy thừa ban đầu thành:
\\( 2^{2026} = 2^{3\\times675+1} = (2^3)^{675}\\cdot2^1 = 8^{675}\\cdot2 \\)

Áp dụng tính chất nhân và lũy thừa của đồng dư thức:
\\( 8^{675}\\cdot2 \\equiv 1^{675}\\cdot2 \\pmod7 \\equiv 1\\cdot2 \\pmod7 \\equiv 2 \\pmod7 \\)

Vậy, số dư của phép chia \\( 2^{2026} \\) cho 7 là 2.""",
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de2_dd_19",
                "type": "dragdrop",
                "content": "Trong không gian với hệ tọa độ Oxyz, cho hai điểm \\( A(1;2;-1) \\) và \\( B(3;0;3) \\). Một thiết bị bay không người lái (Drone) được lập trình di chuyển trên một quỹ đạo là mặt cầu (S) nhận đoạn thẳng AB làm đường kính. Kéo và thả các phương án trong khung (một phương án có thể được dùng nhiều lần hoặc không dùng) để hoàn thành các thông số của quỹ đạo (S) dưới đây:",
                "options_pool": [
                    "\\( 1 \\)",
                    "\\( 2 \\)",
                    "\\( 3 \\)",
                    "\\( 6 \\)",
                    "\\( 24 \\)"
                ],
                "blanks": [
                    {"label": "Hoành độ tâm I của mặt cầu (S) là:", "answer": "2"},
                    {"label": "Tung độ tâm I của mặt cầu (S) là:", "answer": "1"},
                    {"label": "Bình phương bán kính R² của mặt cầu (S) là:", "answer": "6"}
                ],
                "points": 1,
                "explanation": """Mặt cầu (S) nhận đoạn thẳng AB làm đường kính nên tâm I của mặt cầu chính là trung điểm của đoạn thẳng AB. Tọa độ điểm I được xác định bởi công thức trung bình cộng:
\\( x_I = \\dfrac{x_A+x_B}{2} = \\dfrac{1+3}{2} = 2 \\)
\\( y_I = \\dfrac{y_A+y_B}{2} = \\dfrac{2+0}{2} = 1 \\)
\\( z_I = \\dfrac{z_A+z_B}{2} = \\dfrac{-1+3}{2} = 1 \\)

Vậy tọa độ tâm là \\( I(2;1;1) \\). Từ đây ta xác định được: Hoành độ là 2, tung độ là 1.

Bán kính R của mặt cầu bằng một nửa độ dài đường kính AB. Ta tính khoảng cách AB:
\\( AB = \\sqrt{(3-1)^2+(0-2)^2+(3-(-1))^2} = \\sqrt{2^2+(-2)^2+4^2} = \\sqrt{4+4+16} = \\sqrt{24} \\)

Suy ra \\( R = \\dfrac{AB}{2} = \\dfrac{\\sqrt{24}}{2} \\). Để tìm bình phương bán kính, ta tính:
\\( R^2 = \\left(\\dfrac{\\sqrt{24}}{2}\\right)^2 = \\dfrac{24}{4} = 6 \\)

Thứ tự kéo thả chính xác từ trên xuống dưới là: 2, 1, 6.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_20',
                "type": 'short',
                "content": 'Một lớp học có 15 học sinh, bao gồm 8 học sinh nam và 7 học sinh nữ. Giáo viên chủ nhiệm cần chọn ngẫu nhiên 4 học sinh để tham gia vào đội thanh niên xung kích của trường. Xác suất để trong 4 học sinh được chọn, số học sinh nữ chiếm ưu thế (nhiều hơn số học sinh nam) được viết dưới dạng phân số tối giản \\( \\dfrac{a}{b} \\) (với \\( a, b \\in \\mathbb{N}^* \\)). Tính giá trị của biểu thức \\( S = a+b \\).',
                "blanks": [
                    {"label": 'S =', "answers": ['16']},
                ],
                "points": 1,
                "explanation": """Phép thử: Chọn ngẫu nhiên 4 học sinh từ tổng số 15 học sinh. Số phần tử của không gian mẫu là số tổ hợp chập 4 của 15:
\\( |\\Omega| = C_{15}^4 = 1365 \\)

Gọi biến cố A: "Trong 4 học sinh được chọn, số học sinh nữ nhiều hơn số học sinh nam". Vì tổng số học sinh được chọn là 4, để số nữ lớn hơn số nam, ta chỉ có 2 trường hợp thỏa mãn:

Trường hợp 1: Chọn 3 học sinh nữ và 1 học sinh nam. Số cách chọn:
\\( C_7^3\\cdot C_8^1 = 35\\cdot8 = 280 \\) (cách)

Trường hợp 2: Chọn 4 học sinh nữ và 0 học sinh nam. Số cách chọn:
\\( C_7^4\\cdot C_8^0 = 35\\cdot1 = 35 \\) (cách)

Vì hai trường hợp này là độc lập và xung khắc, ta áp dụng quy tắc cộng để tìm số kết quả thuận lợi cho biến cố A:
\\( |A| = 280+35 = 315 \\)

Xác suất của biến cố A:
\\( P(A) = \\dfrac{|A|}{|\\Omega|} = \\dfrac{315}{1365} = \\dfrac{63}{273} = \\dfrac{9}{39} = \\dfrac{3}{13} \\)

Theo giả thiết, phân số này tối giản là \\( \\dfrac{a}{b} \\), suy ra \\( a=3, b=13 \\). Vậy \\( S=a+b=3+13=16 \\).""",
            },
            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_21',
                "type": 'mc4',
                "content": 'Một nhà máy cần sản xuất các thùng đựng sơn hình trụ có dung tích cố định bằng \\( 16\\pi \\) dm³. Để tiết kiệm nguyên liệu nhất (tức diện tích toàn phần của hình trụ đạt giá trị nhỏ nhất), bán kính đáy R của thùng sơn phải bằng bao nhiêu?',
                "options": {
                    'A': '\\( R = 1 \\) dm',
                    'B': '\\( R = 2 \\) dm',
                    'C': '\\( R = 4 \\) dm',
                    'D': '\\( R = \\sqrt{2} \\) dm',
                },
                "correct": 'B',
                "points": 1,
                "explanation": """Thể tích khối trụ được tính bởi công thức: \\( V=\\pi R^2 h = 16\\pi \\Rightarrow h=\\dfrac{16}{R^2} \\).

Diện tích toàn phần của hình trụ:
\\( S_{tp} = 2\\pi R^2+2\\pi Rh = 2\\pi R^2+2\\pi R\\left(\\dfrac{16}{R^2}\\right) = 2\\pi R^2+\\dfrac{32\\pi}{R} \\)

Khảo sát hàm số \\( S_{tp}(R) \\) với \\( R>0 \\):
\\( S_{tp}' = 4\\pi R-\\dfrac{32\\pi}{R^2} = 0 \\Rightarrow R^3=8 \\Rightarrow R=2 \\) (dm)

Kiểm tra đạo hàm hoặc bảng biến thiên thấy \\( S_{tp} \\) đạt giá trị nhỏ nhất tại \\( R=2 \\) dm. Đáp án B.""",
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de2_tf_22",
                "type": "truefalse",
                "content": "Trong không gian Oxyz, cho mặt phẳng \\( (P): 2x-2y+z-5=0 \\) và điểm \\( A(1;-2;3) \\). Xét tính đúng/sai của các mệnh đề sau:",
                "statements": [
                    {"text": "Khoảng cách từ điểm A đến mặt phẳng (P) bằng 2.", "correct": False},
                    {"text": "Đường thẳng \\( \\Delta \\) đi qua A và vuông góc với (P) có phương trình tham số là \\( x=1+2t,\\;y=-2-2t,\\;z=3+t \\).", "correct": True},
                    {"text": "Hình chiếu vuông góc của điểm A trên mặt phẳng (P) là điểm \\( H\\left(\\dfrac13;-\\dfrac23;\\dfrac{10}{3}\\right) \\).", "correct": True},
                    {"text": "Mặt cầu tâm A tiếp xúc với mặt phẳng (P) có phương trình là \\( (x-1)^2+(y+2)^2+(z-3)^2=\\dfrac{16}{9} \\).", "correct": True}
                ],
                "points": 1,
                "explanation": """a) Khoảng cách từ \\( A(1;-2;3) \\) đến (P) là:
\\( d(A,(P)) = \\dfrac{|2(1)-2(-2)+3-5|}{\\sqrt{2^2+(-2)^2+1^2}} = \\dfrac{|2+4+3-5|}{\\sqrt9} = \\dfrac43 \\ne 2 \\) \\( \\Rightarrow \\) Sai.

b) Vectơ pháp tuyến của (P) là \\( \\vec{n}=(2;-2;1) \\), đây cũng là vectơ chỉ phương của đường thẳng \\( \\Delta \\) vuông góc với (P). Phương trình tham số của \\( \\Delta \\) qua \\( A(1;-2;3) \\) là hoàn toàn chính xác \\( \\Rightarrow \\) Đúng.

c) Viết phương trình tham số của đường thẳng \\( \\Delta \\) qua A vuông góc với (P), sau đó tìm giao điểm H của \\( \\Delta \\) và (P) ta được \\( H\\left(\\dfrac13;-\\dfrac23;\\dfrac{10}{3}\\right) \\) \\( \\Rightarrow \\) Đúng.

d) Bán kính mặt cầu tiếp xúc với (P) chính là \\( R=d(A,(P))=\\dfrac43 \\), do đó phương trình mặt cầu là \\( (x-1)^2+(y+2)^2+(z-3)^2=\\left(\\dfrac43\\right)^2=\\dfrac{16}{9} \\) \\( \\Rightarrow \\) Đúng.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_23',
                "type": 'short',
                "content": 'Một chiếc ly thủy tinh có phần lòng bên trong được thiết kế bằng cách quay hình phẳng giới hạn bởi parabol \\( y=x^2 \\) và đường thẳng \\( y=4 \\) quanh trục tung Oy. Thể tích phần chứa nước tối đa của chiếc ly đó là \\( V=k\\pi \\). Giá trị của k bằng bao nhiêu?',
                "blanks": [
                    {"label": 'k =', "answers": ['8']},
                ],
                "points": 1,
                "explanation": """Miền giới hạn khi quay quanh trục Oy từ \\( y=0 \\) đến \\( y=4 \\), với phương trình đường sinh \\( x^2=y \\).

Công thức tính thể tích khối tròn xoay khi quay quanh trục Oy:
\\( V = \\pi\\displaystyle\\int_0^4 x^2\\,dy = \\pi\\displaystyle\\int_0^4 y\\,dy = \\pi\\cdot\\dfrac{y^2}{2}\\Big|_0^4 = \\dfrac{16\\pi}{2} = 8\\pi \\)

Suy ra \\( k=8 \\).""",
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de2_dd_24",
                "type": "dragdrop",
                "content": "Cho khai triển nhị thức Newton của \\( (x+2)^n \\;(n\\in\\mathbb{N}^*) \\), biết tổng các hệ số của khai triển bằng 243. Kéo và thả các phương án lựa chọn thích hợp vào ô trống:",
                "options_pool": [
                    "\\( 3 \\)",
                    "\\( 5 \\)",
                    "\\( 7 \\)",
                    "\\( 80 \\)",
                    "\\( 243 \\)",
                    "\\( 729 \\)"
                ],
                "blanks": [
                    {"label": "Giá trị của n bằng:", "answer": "5"},
                    {"label": "Hệ số của số hạng chứa x² trong khai triển bằng:", "answer": "80"}
                ],
                "points": 1,
                "explanation": """Tổng các hệ số của khai triển \\( (x+2)^n \\) được tính bằng cách thay \\( x=1 \\) vào biểu thức: \\( (1+2)^n = 3^n \\).

Theo đề bài: \\( 3^n = 243 = 3^5 \\Rightarrow n=5 \\).

Số hạng tổng quát trong khai triển \\( (x+2)^5 \\) là: \\( T_{k+1} = C_5^k x^{5-k}2^k \\).

Để tìm hệ số của số hạng chứa \\( x^2 \\), ta cho \\( 5-k=2 \\Rightarrow k=3 \\).

Hệ số tương ứng là: \\( C_5^3\\cdot2^3 = 10\\cdot8 = 80 \\).

Vậy \\( n=5 \\), hệ số của \\( x^2 \\) là 80.""",
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_25',
                "type": 'short',
                "content": 'Cho hàm số \\( f(x) = \\begin{cases} \\dfrac{x^2-3x+2}{x-1} & \\text{khi } x>1 \\\\ ax+2 & \\text{khi } x\\le1 \\end{cases} \\). Để hàm số có giới hạn hữu hạn tại điểm \\( x=1 \\), giá trị của tham số a bằng bao nhiêu?',
                "blanks": [
                    {"label": 'a =', "answers": ['-3']},
                ],
                "points": 1,
                "explanation": """Để hàm số có giới hạn tại \\( x=1 \\), giới hạn bên phải và giới hạn bên trái tại điểm \\( x=1 \\) phải tồn tại và bằng nhau, tức là:
\\( \\lim\\limits_{x\\to1^+} f(x) = \\lim\\limits_{x\\to1^-} f(x) \\)

Tính giới hạn bên phải:
\\( \\lim\\limits_{x\\to1^+} f(x) = \\lim\\limits_{x\\to1^+}\\dfrac{x^2-3x+2}{x-1} = \\lim\\limits_{x\\to1^+}\\dfrac{(x-1)(x-2)}{x-1} = \\lim\\limits_{x\\to1^+}(x-2) = 1-2 = -1 \\)

Tính giới hạn bên trái:
\\( \\lim\\limits_{x\\to1^-} f(x) = \\lim\\limits_{x\\to1^-}(ax+2) = a+2 \\)

Từ điều kiện tồn tại giới hạn: \\( a+2=-1 \\Rightarrow a=-3 \\).""",
            },

                      # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_26',
                "type": 'mc4',
                "content": '''Một nhà máy cần sản xuất các thùng đựng sơn hình trụ không có nắp đậy với thể tích thiết kế cố định bằng \\( 16\\pi \\, m^3 \\). Chi phí làm mặt đáy là 100.000 VNĐ/m² và chi phí làm mặt xung quanh là 50.000 VNĐ/m². Để chi phí sản xuất chiếc thùng đạt giá trị nhỏ nhất, bán kính đáy \\( r \\) của hình trụ phải bằng:''',
                "options": {
                    'A': '\\( r = 2 \\) m',
                    'B': '\\( r = 4 \\) m',
                    'C': '\\( r = 3 \\) m',
                    'D': '\\( r = 1 \\) m',
                },
                "correct": 'A',
                "points": 1,
                "explanation": '''Gọi \\( r, h \\) lần lượt là bán kính đáy và chiều cao thùng \\( (r>0, h>0) \\).

Thể tích: \\( V = \\pi r^2 h = 16\\pi \\Rightarrow h = \\dfrac{16}{r^2} \\).

Diện tích đáy: \\( S_{đáy} = \\pi r^2 \\) \\( \\Rightarrow \\) Chi phí đáy: \\( T_1 = 100000\\pi r^2 \\) (đồng).

Diện tích xung quanh: \\( S_{xq} = 2\\pi r h \\) \\( \\Rightarrow \\) Chi phí xung quanh: \\( T_2 = 50000 \\cdot 2\\pi r h = 100000\\pi r h \\) (đồng).

Tổng chi phí: \\( T(r) = 100000\\pi\\left(r^2 + rh\\right) = 100000\\pi\\left(r^2 + \\dfrac{16}{r}\\right) \\).

Xét \\( f(r) = r^2 + \\dfrac{16}{r} \\) với \\( r>0 \\):
\\( f'(r) = 2r - \\dfrac{16}{r^2} = \\dfrac{2r^3-16}{r^2} \\).

Cho \\( f'(r)=0 \\Rightarrow 2r^3=16 \\Rightarrow r^3=8 \\Rightarrow r=2 \\) (m).

Lập bảng biến thiên, hàm số đạt giá trị nhỏ nhất tại \\( r=2 \\). Chọn A.''',
            },

            {
                "id": 'de2_mc_30',
                "type": 'mc4',
                "content": 'Phương trình \\( 2\\sin^2 x - 5\\sin x\\cos x + 2\\cos^2 x = 0 \\) có tổng tất cả các nghiệm thuộc khoảng \\( (0; \\pi) \\) bằng:',
                "options": {
                    'A': '\\( \\dfrac{\\pi}{4} \\)',
                    'B': '\\( \\dfrac{\\pi}{2} \\)',
                    'C': '\\( \\dfrac{3\\pi}{4} \\)',
                    'D': '\\( \\pi \\)',
                },
                "correct": 'B',
                "points": 1,
                "explanation": '''Kiểm tra \\( \\cos x = 0 \\): khi đó \\( \\sin^2 x = 1 \\), thay vào phương trình được \\( 2(1) - 5(0) + 2(0) = 2 \\ne 0 \\), nên \\( \\cos x = 0 \\) không là nghiệm.

Chia cả hai vế cho \\( \\cos^2 x \\), đặt \\( t = \\tan x \\), phương trình trở thành:
\\( 2t^2 - 5t + 2 = 0 \\Leftrightarrow (2t-1)(t-2)=0 \\Leftrightarrow t=\\dfrac{1}{2} \\) hoặc \\( t=2 \\).

Với \\( t=\\dfrac{1}{2} \\Rightarrow x_1 = \\arctan\\dfrac{1}{2} \\) (thuộc \\( (0;\\pi) \\)).
Với \\( t=2 \\Rightarrow x_2 = \\arctan 2 \\) (thuộc \\( (0;\\pi) \\)).

Tổng hai nghiệm: \\( S = \\arctan\\dfrac{1}{2} + \\arctan 2 \\).

Áp dụng \\( \\arctan a + \\arctan\\dfrac{1}{a} = \\dfrac{\\pi}{2} \\) (với \\( a>0 \\)), ta có \\( S = \\dfrac{\\pi}{2} \\). Chọn B.''',
            },

            # ---------------- KÉO THẢ (dragdrop) ----------------
            {
                "id": "de2_dd_29",
                "type": "dragdrop",
                "content": "Cho hàm số \\( y = x^3 - 3x^2 + 2 \\). Kéo và thả các phương án lựa chọn thích hợp vào ô trống:",
                "options_pool": [
                    "\\( 2 \\)",
                    "\\( -2 \\)",
                    "\\( 4 \\)",
                    "\\( 0 \\)",
                    "\\( -4 \\)"
                ],
                "blanks": [
                    {"label": "Giá trị cực đại của hàm số bằng:", "answer": "2"},
                    {"label": "Giá trị cực tiểu của hàm số bằng:", "answer": "-2"},
                    {"label": "Tung độ giao điểm của đồ thị hàm số với trục tung bằng:", "answer": "2"}
                ],
                "points": 1,
                "explanation": '''Tập xác định: \\( D = \\mathbb{R} \\).

Đạo hàm: \\( y' = 3x^2 - 6x = 3x(x-2) \\).

Cho \\( y' = 0 \\Rightarrow x = 0 \\Rightarrow y = 2 \\), hoặc \\( x = 2 \\Rightarrow y = -2 \\).

Lập bảng biến thiên: hàm số đạt cực đại tại \\( x=0 \\) với \\( y_{CĐ} = 2 \\); đạt cực tiểu tại \\( x=2 \\) với \\( y_{CT} = -2 \\).

Giao điểm với trục tung có hoành độ \\( x=0 \\) \\( \\Rightarrow y(0) = 0^3 - 3(0)^2 + 2 = 2 \\).

Vậy: a) 2; b) −2; c) 2.''',
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_27',
                "type": 'short',
                "content": 'Có bao nhiêu số nguyên dương \\( n \\) nhỏ hơn hoặc bằng 100 sao cho biểu thức \\( P = n^2 + 3n + 5 \\) chia hết cho 5?',
                "blanks": [
                    {"label": 'Số giá trị n =', "answers": ['40']},
                ],
                "points": 1,
                "explanation": '''Ta có \\( P = n^2 + 3n + 5 \\). Vì 5 chia hết cho 5, để \\( P \\) chia hết cho 5 thì \\( n^2+3n \\) chia hết cho 5, tức \\( n(n+3) \\) chia hết cho 5.

Vì 5 là số nguyên tố, \\( n(n+3) \\vdots 5 \\Leftrightarrow n \\vdots 5 \\) hoặc \\( (n+3)\\vdots 5 \\).

Trường hợp 1: \\( n \\vdots 5 \\Rightarrow n=5k \\). Với \\( 1\\le n \\le 100 \\Rightarrow k \\in \\{1,...,20\\} \\): có 20 giá trị.

Trường hợp 2: \\( n+3 \\vdots 5 \\Rightarrow n = 5m-3 \\). Với \\( 1\\le n\\le 100 \\Rightarrow m \\in \\{1,...,20\\} \\): có 20 giá trị.

Hai trường hợp không trùng nhau (một bên n chia hết 5, bên kia n chia 5 dư 2).

Tổng số giá trị: \\( 20+20=40 \\).''',
            },

            {
                "id": 'de2_sh_28',
                "type": 'short',
                "content": 'Một hộp chứa 5 quả cầu trắng và 4 quả cầu đen. Lấy ngẫu nhiên đồng thời 3 quả cầu từ hộp. Tính xác suất để 3 quả cầu lấy ra có cả hai màu trắng và đen.',
                "blanks": [
                    {"label": 'Xác suất =', "answers": ['5/6', '\\dfrac{5}{6}']},
                ],
                "points": 1,
                "explanation": '''Số phần tử không gian mẫu: \\( n(\\Omega) = C_9^3 = 84 \\).

Gọi A là biến cố "3 quả cầu lấy ra có cả hai màu". Biến cố đối \\( \\overline{A} \\) là "3 quả chỉ có đúng một màu" (toàn trắng hoặc toàn đen).

Số cách chọn 3 quả toàn trắng: \\( C_5^3 = 10 \\).
Số cách chọn 3 quả toàn đen: \\( C_4^3 = 4 \\).

\\( n(\\overline{A}) = 10+4=14 \\).

Xác suất: \\( P(A) = 1 - P(\\overline{A}) = 1 - \\dfrac{14}{84} = 1-\\dfrac{1}{6} = \\dfrac{5}{6} \\).''',
            },

                      # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_31',
                "type": 'short',
                "content": 'Xét chuyển động của một vật theo quỹ đạo xác định bởi hàm số vận tốc \\( v(t) = 3t^2 - 12t + 9 \\) (m/s) trong khoảng thời gian từ \\( t = 0 \\) đến \\( t = 4 \\) (giây). Tính tổng quãng đường vật đi được trong khoảng thời gian đó.',
                "blanks": [
                    {"label": 'Quãng đường (m) =', "answers": ['12']},
                ],
                "points": 1,
                "explanation": '''Phương trình vận tốc: \\( v(t) = 3t^2 - 12t + 9 \\).

Ta có \\( v(t) = 0 \\Leftrightarrow 3t^2 - 12t + 9 = 0 \\Leftrightarrow t = 1 \\) hoặc \\( t = 3 \\) (cả hai đều thuộc \\( [0;4] \\)).

Quãng đường vật đi được là tổng độ dịch chuyển có trị tuyệt đối:
\\( S = \\displaystyle\\int_0^4 |3t^2-12t+9|\\,dt \\)
\\( = \\displaystyle\\int_0^1 (3t^2-12t+9)\\,dt + \\int_1^3 -(3t^2-12t+9)\\,dt + \\int_3^4 (3t^2-12t+9)\\,dt \\)

Tính từng tích phân:
\\( \\displaystyle\\int_0^1 (3t^2-12t+9)\\,dt = (t^3-6t^2+9t)\\Big|_0^1 = 4 \\).

\\( \\displaystyle\\int_1^3 -(3t^2-12t+9)\\,dt = -(t^3-6t^2+9t)\\Big|_1^3 = -(0-4) = 4 \\).

\\( \\displaystyle\\int_3^4 (3t^2-12t+9)\\,dt = (t^3-6t^2+9t)\\Big|_3^4 = 4-0 = 4 \\).

Tổng quãng đường: \\( S = 4+4+4 = 12 \\) (mét).''',
            },

            # ---------------- ĐÚNG / SAI (truefalse) ----------------
            {
                "id": "de2_tf_32",
                "type": "truefalse",
                "content": "Trong không gian \\( Oxyz \\), cho mặt phẳng \\( (P): 2x - 2y + z - 5 = 0 \\) và điểm \\( M(1; -2; 3) \\). Xét tính đúng/sai của các mệnh đề sau:",
                "statements": [
                    {"text": "Khoảng cách từ điểm M đến mặt phẳng (P) bằng \\( \\dfrac{2}{3} \\).", "correct": False},
                    {"text": "Hình chiếu vuông góc của M lên (P) có hoành độ âm.", "correct": False},
                    {"text": "Phương trình mặt cầu tâm M tiếp xúc với mặt phẳng (P) có bán kính bằng \\( \\dfrac{4}{3} \\).", "correct": True}
                ],
                "points": 1,
                "explanation": '''a) Khoảng cách từ \\( M(1;-2;3) \\) đến \\( (P): 2x-2y+z-5=0 \\) là:
\\( d(M,(P)) = \\dfrac{|2(1)-2(-2)+3-5|}{\\sqrt{2^2+(-2)^2+1^2}} = \\dfrac{|2+4+3-5|}{3} = \\dfrac{4}{3} \\ne \\dfrac{2}{3} \\) \\( \\Rightarrow \\) Sai.

b) Đường thẳng \\( \\Delta \\) qua M vuông góc với (P) có phương trình tham số:
\\( x = 1+2t,\\ y=-2-2t,\\ z=3+t \\).

Hình chiếu H là giao điểm của \\( \\Delta \\) và (P):
\\( 2(1+2t) - 2(-2-2t) + (3+t) - 5 = 0 \\Leftrightarrow 9t+4=0 \\Leftrightarrow t = -\\dfrac{4}{9} \\).

Hoành độ điểm H: \\( x_H = 1+2\\left(-\\dfrac{4}{9}\\right) = \\dfrac{1}{9} > 0 \\) \\( \\Rightarrow \\) Sai.

c) Mặt cầu tâm M tiếp xúc với (P) có bán kính \\( R = d(M,(P)) = \\dfrac{4}{3} \\) \\( \\Rightarrow \\) Đúng.''',
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_33',
                "type": 'short',
                "content": 'Một hộp đựng 6 thẻ được đánh số từ 1 đến 6. Rút ngẫu nhiên đồng thời 3 thẻ từ hộp đó. Tính xác suất để tổng các số trên 3 thẻ được rút ra là một số chia hết cho 3.',
                "blanks": [
                    {"label": 'Xác suất =', "answers": ['2/5', '\\dfrac{2}{5}', '0.4', '0,4']},
                ],
                "points": 1,
                "explanation": '''Số phần tử không gian mẫu: \\( n(\\Omega) = C_6^3 = 20 \\).

Chia tập \\( \\{1,2,3,4,5,6\\} \\) thành 3 nhóm theo số dư khi chia cho 3:
- Nhóm dư 0: \\( \\{3,6\\} \\) (2 phần tử).
- Nhóm dư 1: \\( \\{1,4\\} \\) (2 phần tử).
- Nhóm dư 2: \\( \\{2,5\\} \\) (2 phần tử).

Tổng 3 số chia hết cho 3 khi và chỉ khi 3 số được chọn thuộc 3 nhóm khác nhau (mỗi nhóm chọn 1 số):
\\( n(A) = C_2^1 \\cdot C_2^1 \\cdot C_2^1 = 2\\cdot2\\cdot2 = 8 \\).

Xác suất: \\( P = \\dfrac{8}{20} = \\dfrac{2}{5} = 0.4 \\).''',
            },

            # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_34',
                "type": 'mc4',
                "content": 'Cho hàm số \\( f(x) \\) có đạo hàm liên tục trên \\( \\mathbb{R} \\) và \\( f\'(x) = x(x-1)^2(x+2) \\). Số điểm cực trị của hàm số \\( g(x) = f(x^2 - 2x) \\) là:',
                "options": {
                    'A': '2',
                    'B': '3',
                    'C': '4',
                    'D': '5',
                },
                "correct": 'B',
                "points": 1,
                "explanation": '''Ta có \\( g\'(x) = (x^2-2x)\' \\cdot f\'(x^2-2x) = 2(x-1)f\'(x^2-2x) \\).

Cho \\( g\'(x) = 0 \\Leftrightarrow \\begin{cases} x-1=0 \\\\ f\'(x^2-2x)=0 \\end{cases} \\).

Từ \\( f\'(x) = x(x-1)^2(x+2) \\), phương trình \\( f\'(u)=0 \\) có nghiệm \\( u=0, u=-2 \\) (nghiệm đơn) và \\( u=1 \\) (nghiệm kép).

Do đó \\( f\'(x^2-2x)=0 \\) tương đương:
\\( x^2-2x=0 \\) hoặc \\( x^2-2x=-2 \\) (vô nghiệm) hoặc \\( x^2-2x=1 \\) (nghiệm kép, không đổi dấu).

\\( \\Leftrightarrow x=0 \\) hoặc \\( x=2 \\).

Kết hợp với nghiệm \\( x=1 \\), ta có các nghiệm đơn của \\( g\'(x)=0 \\) là \\( x=0, x=1, x=2 \\).

Vậy hàm số \\( g(x) \\) có đúng 3 điểm cực trị. Chọn B.''',
            },

            # ---------------- TRẢ LỜI NGẮN (short) ----------------
            {
                "id": 'de2_sh_35',
                "type": 'short',
                "content": 'Trong không gian với hệ tọa độ \\( Oxyz \\), cho mặt cầu \\( (S): x^2+y^2+z^2-2x+4z-4=0 \\) và điểm \\( M(1;0;-1) \\). Qua M vẽ dây cung AB của mặt cầu sao cho M là trung điểm của đoạn thẳng AB. Tính độ dài đoạn thẳng AB.',
                "blanks": [
                    {"label": 'AB =', "answers": ['4√2', '4\\sqrt{2}']},
                ],
                "points": 1,
                "explanation": '''Phương trình mặt cầu (S) viết lại dạng chính tắc:
\\( (x-1)^2 + y^2 + (z+2)^2 = 9 \\).

Mặt cầu có tâm \\( I(1;0;-2) \\), bán kính \\( R=3 \\).

Kiểm tra M(1;0;-1): \\( (1-1)^2+0^2+(-1+2)^2 = 1 < 9 \\Rightarrow M \\) nằm trong mặt cầu.

Vì M là trung điểm dây cung AB nên \\( IM \\perp AB \\).

Khoảng cách từ I đến M: \\( IM = \\sqrt{(1-1)^2+(0-0)^2+(-1-(-2))^2} = 1 \\).

Xét tam giác vuông IAM vuông tại M:
\\( AM = \\sqrt{R^2 - IM^2} = \\sqrt{9-1} = \\sqrt{8} = 2\\sqrt{2} \\).

Độ dài đoạn AB: \\( AB = 2AM = 4\\sqrt{2} \\).''',
            },
                      # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
            {
                "id": 'de2_mc_36',
                "type": 'mc4',
                "content": 'Trong không gian \\( Oxyz \\), cho mặt cầu \\( (S): (x-1)^2+(y-2)^2+(z-3)^2=25 \\) và điểm \\( A(7;2;3) \\). Gọi M là điểm di động trên mặt cầu (S). Giá trị nhỏ nhất của độ dài đoạn thẳng AM bằng:',
                "options": {
                    'A': '1',
                    'B': '2',
                    'C': '3',
                    'D': '5',
                },
                "correct": 'A',
                "points": 1,
                "explanation": '''Mặt cầu (S) có tâm \\( I(1;2;3) \\) và bán kính \\( R=5 \\).

Khoảng cách từ điểm \\( A(7;2;3) \\) đến tâm I:
\\( IA = \\sqrt{(7-1)^2+(2-2)^2+(3-3)^2} = \\sqrt{6^2} = 6 \\).

Vì \\( IA = 6 > R = 5 \\), điểm A nằm ngoài mặt cầu (S).

Do M di động trên mặt cầu (S), độ dài AM đạt giá trị nhỏ nhất khi M nằm trên đoạn thẳng IA và giao với mặt cầu (S):
\\( AM_{min} = IA - R = 6 - 5 = 1 \\). Chọn A.''',
            },

            {
                "id": 'de2_mc_37',
                "type": 'mc4',
                "content": 'Cho hàm số \\( f(x) \\) có đạo hàm \\( f\'(x) = x(x-2) \\) với mọi \\( x \\in \\mathbb{R} \\). Số điểm cực trị của hàm số \\( g(x) = f(x^3-3x) + \\dfrac{3}{4}x^4 - 3x^3 + 3x^2 \\) là:',
                "options": {
                    'A': '3',
                    'B': '5',
                    'C': '7',
                    'D': '9',
                },
                "correct": 'C',
                "points": 1,
                "explanation": '''Tính đạo hàm của \\( g(x) \\):
\\( g\'(x) = (3x^2-3)f\'(x^3-3x) + 3x^3 - 9x^2 + 6x = 3(x^2-1)f\'(x^3-3x) + 3x(x-1)(x-2) \\).

Theo giả thiết \\( f\'(t) = t(t-2) \\), suy ra:
\\( f\'(x^3-3x) = (x^3-3x)(x^3-3x-2) = x(x^2-3)(x-2)(x+1)^2 \\).

Do đó:
\\( g\'(x) = 3(x-1)(x+1)\\cdot x(x^2-3)(x-2)(x+1)^2 + 3x(x-1)(x-2) \\)
\\( = 3x(x-1)(x-2)\\left[(x+1)^3(x^2-3)+1\\right] \\).

Phương trình \\( g\'(x)=0 \\) có các nghiệm đơn phân biệt: \\( x=0, x=1, x=2 \\), và phương trình \\( (x+1)^3(x^2-3)+1=0 \\) có thêm 4 nghiệm phân biệt khác.

Tổng cộng phương trình \\( g\'(x)=0 \\) có 7 nghiệm đơn phân biệt, do đó hàm số \\( g(x) \\) có 7 điểm cực trị. Chọn C.''',
            },

            {
                "id": 'de2_mc_38',
                "type": 'mc4',
                "content": 'Gọi S là tập hợp tất cả các số tự nhiên gồm 3 chữ số đôi một khác nhau được chọn từ tập hợp \\( X = \\{0,1,2,3,4,5\\} \\). Chọn ngẫu nhiên một số từ tập S. Xác suất để số được chọn chia hết cho 15 bằng phân số tối giản \\( \\dfrac{a}{b} \\) \\( (a,b \\in \\mathbb{N}^*) \\). Giá trị của \\( a+b \\) bằng:',
                "options": {
                    'A': '41',
                    'B': '47',
                    'C': '51',
                    'D': '57',
                },
                "correct": 'D',
                "points": 1,
                "explanation": '''Số các số tự nhiên gồm 3 chữ số đôi một khác nhau từ X là: \\( n(\\Omega) = 5 \\times A_5^2 = 100 \\).

Một số chia hết cho 15 khi và chỉ khi vừa chia hết cho 3 vừa chia hết cho 5 (tận cùng là 0 hoặc 5).

Trường hợp 1: Chữ số tận cùng là 0.
Hai chữ số đầu chọn từ \\( \\{1,2,3,4,5\\} \\) sao cho tổng 3 chữ số chia hết cho 3. Các bộ thỏa mãn: \\( \\{1,2\\}, \\{1,5\\}, \\{2,4\\}, \\{3,4\\} \\). Mỗi bộ có 2! = 2 cách xếp \\( \\Rightarrow 4\\times2=8 \\) số.

Trường hợp 2: Chữ số tận cùng là 5.
Chữ số hàng trăm khác 0 và khác 5. Tổng 3 chữ số chia hết cho 3 \\( \\Leftrightarrow a+b+5 \\vdots 3 \\Leftrightarrow a+b+2 \\vdots 3 \\).
Các bộ 2 chữ số từ \\( \\{0,1,2,3,4\\} \\) cộng với 5 chia hết cho 3 gồm: \\( \\{0,1\\} \\) (hàng trăm chọn 1: 1 cách), \\( \\{0,4\\} \\) (hàng trăm chọn 4: 1 cách), \\( \\{1,3\\} \\) (hàng trăm có 2 cách chọn), \\( \\{2,4\\} \\) (hàng trăm có 2 cách chọn). Tổng: \\( 1+1+2+2=6 \\) số.

Tổng số số chia hết cho 15: \\( 8+6=14 \\).

Xác suất: \\( P = \\dfrac{14}{100} = \\dfrac{7}{50} \\).

Suy ra \\( a=7, b=50 \\Rightarrow a+b=57 \\). Chọn D.''',
            },

            {
                "id": 'de2_mc_39',
                "type": 'mc4',
                "content": 'Cho hình lăng trụ đứng \\( ABC.A\'B\'C\' \\) có đáy ABC là tam giác vuông cân tại B, \\( AB = a\\sqrt{2} \\), cạnh bên \\( AA\' = 2a \\). Gọi M là trung điểm của \\( A\'C\' \\). Thể tích của khối tứ diện M.ABC bằng:',
                "options": {
                    'A': '\\( \\dfrac{a^3}{3} \\)',
                    'B': '\\( \\dfrac{2a^3}{3} \\)',
                    'C': '\\( \\dfrac{a^3\\sqrt{2}}{3} \\)',
                    'D': '\\( \\dfrac{4a^3}{3} \\)',
                },
                "correct": 'B',
                "points": 1,
                "explanation": '''Tam giác ABC vuông cân tại B với \\( AB=BC=a\\sqrt{2} \\), diện tích đáy:
\\( S_{ABC} = \\dfrac{1}{2}AB\\cdot BC = \\dfrac{1}{2}(a\\sqrt{2})(a\\sqrt{2}) = a^2 \\).

Vì lăng trụ đứng nên chiều cao lăng trụ là \\( AA\' = 2a \\). Điểm M là trung điểm của \\( A\'C\' \\) nằm trên mặt phẳng \\( (A\'B\'C\') \\), khoảng cách từ M đến mặt phẳng đáy (ABC) bằng chiều cao lăng trụ: \\( d(M,(ABC)) = AA\' = 2a \\).

Thể tích khối tứ diện M.ABC:
\\( V_{M.ABC} = \\dfrac{1}{3}\\cdot d(M,(ABC))\\cdot S_{ABC} = \\dfrac{1}{3}\\cdot 2a\\cdot a^2 = \\dfrac{2a^3}{3} \\). Chọn B.''',
            },

            {
                "id": 'de2_mc_40',
                "type": 'mc4',
                "content": 'Cho các số thực dương \\( x, y, z \\) thỏa mãn \\( \\log_3(x+y+z) + \\log_3(xyz) = 3 \\). Giá trị nhỏ nhất của biểu thức \\( P = x^2+y^2+z^2 \\) bằng:',
                "options": {
                    'A': '6',
                    'B': '9',
                    'C': '12',
                    'D': '15',
                },
                "correct": 'B',
                "points": 1,
                "explanation": '''Phương trình giả thiết tương đương:
\\( \\log_3\\left((x+y+z)xyz\\right) = 3 \\Leftrightarrow (x+y+z)xyz = 3^3 = 27 \\).

Áp dụng bất đẳng thức Cauchy cho 3 số dương x, y, z:
\\( xyz \\le \\dfrac{(x+y+z)^3}{27} \\).

Thay vào phương trình trên:
\\( (x+y+z)\\cdot\\dfrac{(x+y+z)^3}{27} \\ge 27 \\Leftrightarrow (x+y+z)^4 \\ge 729 \\Rightarrow x+y+z \\ge 3\\sqrt{3} \\).

Sử dụng bất đẳng thức \\( x^2+y^2+z^2 \\ge \\dfrac{(x+y+z)^2}{3} \\), ta suy ra:
\\( P = x^2+y^2+z^2 \\ge \\dfrac{(3\\sqrt{3})^2}{3} = \\dfrac{27}{3} = 9 \\).

Dấu "=" xảy ra khi \\( x=y=z=\\sqrt{3} \\). Vậy giá trị nhỏ nhất của P bằng 9. Chọn B.''',
            },
        ], # kết thúc đề 2
    },  # kết thúc đề 2
    {
        "id": 'de3',
        "name": 'Đề số 3 - ĐỀ CHÍNH THỨC TSA ĐỢT 1 - 2026.',
        "description": '40 câu hỏi.',
        "questions": [

           # ---------------- ĐÚNG / SAI (truefalse) ----------------

    {
        "id": "de3_tf_01",
        "type": "truefalse",
        "content": "Cho hàm số \\( y = f(x) = \\sqrt{1+\\cos x} \\). Khi ta xét \\( x \\in (0,\\pi) \\), các nhận định dưới đây là đúng hay sai?",
        "statements": [
            {"text": "Phương trình \\( \\sqrt{1+\\cos x} = \\cos\\left(\\dfrac{x}{2}\\right) \\) có nghiệm.", "correct": false},
            {"text": "Phương trình \\( \\sqrt{1+\\cos x} = \\cos\\left(\\dfrac{x}{4}\\right) \\) có nghiệm.", "correct": true},
            {"text": "Phương trình \\( \\sqrt{1+\\cos x} = \\cos\\left(\\dfrac{\\pi}{8}\\right) \\) có đúng 01 nghiệm.", "correct": true}
        ],
        "points": 1,
        "explanation": "Ta có công thức hạ bậc: \\( 1+\\cos x = 2\\cos^2\\left(\\dfrac{x}{2}\\right) \\).\nSuy ra \\( \\sqrt{1+\\cos x} = \\sqrt{2} \\left| \\cos\\left(\\dfrac{x}{2}\\right) \\right| \\).\nVì \\( x \\in (0,\\pi) \\Rightarrow \\dfrac{x}{2} \\in \\left(0,\\dfrac{\\pi}{2}\\right) \\Rightarrow \\cos\\left(\\dfrac{x}{2}\\right) > 0 \\).\nDo đó: \\( \\sqrt{1+\\cos x} = \\sqrt{2}\\cos\\left(\\dfrac{x}{2}\\right) \\).\n\n1. Mệnh đề 1: Sai.\nPhương trình tương đương: \\( \\sqrt{2}\\cos\\left(\\dfrac{x}{2}\\right) = \\cos\\left(\\dfrac{x}{2}\\right) \\Leftrightarrow (\\sqrt{2}-1)\\cos\\left(\\dfrac{x}{2}\\right) = 0 \\Leftrightarrow \\cos\\left(\\dfrac{x}{2}\\right) = 0 \\).\nTuy nhiên với \\( x \\in (0,\\pi) \\) thì \\( \\cos\\left(\\dfrac{x}{2}\\right) > 0 \\).\nPhương trình vô nghiệm.\n\n2. Mệnh đề 2: Đúng.\nPhương trình tương đương: \\( \\sqrt{2}\\cos\\left(\\dfrac{x}{2}\\right) = \\cos\\left(\\dfrac{x}{4}\\right) \\Leftrightarrow \\sqrt{2}\\left[2\\cos^2\\left(\\dfrac{x}{4}\\right)-1\\right] = \\cos\\left(\\dfrac{x}{4}\\right) \\).\nĐặt \\( t = \\cos\\left(\\dfrac{x}{4}\\right) \\).\nVới \\( x \\in (0,\\pi) \\Rightarrow \\dfrac{x}{4} \\in \\left(0,\\dfrac{\\pi}{4}\\right) \\Rightarrow t \\in \\left(\\dfrac{\\sqrt{2}}{2}, 1\\right) \\).\nPhương trình trở thành \\( 2\\sqrt{2}t^2 - t - \\sqrt{2} = 0 \\).\nBấm máy ta được \\( t_1 = \\dfrac{1+\\sqrt{17}}{4\\sqrt{2}} \\approx 0.905 \\) (thỏa mãn) và \\( t_2 < 0 \\) (loại).\nVậy phương trình có nghiệm.\n\n3. Mệnh đề 3: Đúng.\nPhương trình tương đương: \\( \\sqrt{2}\\cos\\left(\\dfrac{x}{2}\\right) = \\cos\\left(\\dfrac{\\pi}{8}\\right) \\Leftrightarrow \\cos\\left(\\dfrac{x}{2}\\right) = \\dfrac{\\cos\\left(\\dfrac{\\pi}{8}\\right)}{\\sqrt{2}} \\approx 0.653 \\).\nHàm số \\( y = \\cos\\left(\\dfrac{x}{2}\\right) \\) nghịch biến trên \\( (0, \\pi) \\) và nhận giá trị từ 1 đến 0.\nVì \\( 0.653 \\in (0, 1) \\) nên phương trình có duy nhất 1 nghiệm."
    },
    {
        "id": "de3_sh_02",
        "type": "short",
        "content": "Bất phương trình \\( (\\log_2 x)^2 + \\log_3\\dfrac{36}{x} \\le \\left(1 + \\log_3\\dfrac{36}{x}\\right)\\log_2 x \\) có tập nghiệm là \\( x \\in [a, b] \\). Giá trị của \\( a + \\dfrac{b}{2} = \\) ?",
        "blanks": [
            {"label": "a + b/2 =", "answers": ["4"]}
        ],
        "points": 1,
        "explanation": "Điều kiện: \\( x > 0 \\).\nĐặt \\( u = \\log_2 x \\) và \\( v = \\log_3\\dfrac{36}{x} \\).\nBất phương trình trở thành: \\( u^2 + v \\le (1+v)u \\Leftrightarrow u^2 - u - uv + v \\le 0 \\Leftrightarrow u(u-1) - v(u-1) \\le 0 \\Leftrightarrow (u-1)(u-v) \\le 0 \\).\n\nTa xét 2 trường hợp:\n- TH1: \\( u \\ge 1 \\) và \\( u \\le v \\).\n\\( \\Leftrightarrow \\log_2 x \\ge 1 \\) và \\( \\log_2 x \\le \\log_3\\dfrac{36}{x} \\).\n\\( \\Leftrightarrow x \\ge 2 \\) và \\( \\log_2 x + \\log_3 x \\le \\log_3 36 \\).\nXét hàm số \\( f(x) = \\log_2 x + \\log_3 x \\) đồng biến trên \\( (0, +\\infty) \\).\nTa thấy \\( f(4) = \\log_2 4 + \\log_3 4 = 2 + \\log_3 4 = \\log_3 9 + \\log_3 4 = \\log_3 36 \\).\nDo đó \\( f(x) \\le f(4) \\Leftrightarrow x \\le 4 \\).\nKết hợp điều kiện ta được \\( x \\in [2, 4] \\).\n\n- TH2: \\( u \\le 1 \\) và \\( u \\ge v \\).\n\\( \\Leftrightarrow \\log_2 x \\le 1 \\) và \\( \\log_2 x \\ge \\log_3\\dfrac{36}{x} \\).\n\\( \\Leftrightarrow x \\le 2 \\) và \\( f(x) \\ge f(4) \\Rightarrow x \\ge 4 \\) (Hệ vô nghiệm).\n\nVậy tập nghiệm là \\( [2, 4] \\Rightarrow a=2, b=4 \\).\nSuy ra \\( a + \\dfrac{b}{2} = 2 + \\dfrac{4}{2} = 4 \\)."
    },
    {
        "id": "de3_sh_03",
        "type": "short",
        "content": "Can chi là hệ thống đánh số thứ tự năm theo chu kỳ, trong đó một năm được xác định bởi hai phần: Thiên Can (Giáp, Ất, Bính, Đinh, Mậu, Kỷ, Canh, Tân, Nhâm, Quý) và Địa Chi (Tý, Sửu, Dần, Mão, Thìn, Tỵ, Ngọ, Mùi, Thân, Dậu, Tuất, Hợi). Biết năm 1010 là năm Bính Tuất, vậy từ 1011 tính đến năm 2025 thì đã có bao nhiêu năm Bính Tuất?",
        "blanks": [
            {"label": "Số năm Bính Tuất đã có là:", "answers": ["16"]}
        ],
        "points": 1,
        "explanation": "Hệ thống Can Chi lặp lại theo chu kỳ là BCNN của 10 (Thiên Can) và 12 (Địa Chi) tức là 60 năm.\nSố năm từ 1011 đến 2025 là: \\( 2025 - 1010 = 1015 \\) năm.\nTa thực hiện phép chia: \\( \\dfrac{1015}{60} \\approx 16.91 \\).\nDo đó, trong khoảng thời gian này có trọn vẹn 16 chu kỳ 60 năm.\nCác năm Bính Tuất sẽ có dạng \\( 1010 + 60k \\) với \\( k \\in \\mathbb{N}^* \\).\nTa có: \\( 1011 \\le 1010 + 60k \\le 2025 \\Leftrightarrow 1 \\le 60k \\le 1015 \\Leftrightarrow \\dfrac{1}{60} \\le k \\le \\dfrac{1015}{60} \\approx 16.91 \\).\nVì \\( k \\in \\mathbb{N} \\) nên \\( k \\in \\{1; 2; ...; 16\\} \\).\nVậy có đúng 16 năm Bính Tuất."
    },
    {
        "id": "de3_sh_04",
        "type": "short",
        "content": "Hiếu và Nam đều có số báo danh có dạng là \\( \\overline{3a8b} \\). Biết số này đều chia hết cho 5 và 9 và số báo danh của Hiếu là số chẵn. Số báo danh của Hiếu và Nam lần lượt là:",
        "blanks": [
            {"label": "Số báo danh của Hiếu:", "answers": ["3780"]},
            {"label": "Số báo danh của Nam:", "answers": ["3285"]}
        ],
        "points": 1,
        "explanation": "Số \\( \\overline{3a8b} \\) chia hết cho 5 nên chữ số tận cùng \\( b \\in \\{0, 5\\} \\).\n\n- Trường hợp 1: Nếu \\( b=0 \\), số trở thành \\( \\overline{3a80} \\).\nĐể số này chia hết cho 9 thì tổng các chữ số \\( (3+a+8+0) = 11+a \\) phải chia hết cho 9.\nVì \\( a \\) là chữ số \\( (0 \\le a \\le 9) \\) nên \\( 11+a = 18 \\Rightarrow a=7 \\).\nTa được số 3780. Đây là số chẵn.\n\n- Trường hợp 2: Nếu \\( b=5 \\), số trở thành \\( \\overline{3a85} \\).\nĐể số này chia hết cho 9 thì tổng các chữ số \\( (3+a+8+5) = 16+a \\) phải chia hết cho 9.\nVì \\( 0 \\le a \\le 9 \\) nên \\( 16+a = 18 \\Rightarrow a=2 \\).\nTa được số 3285. Đây là số lẻ.\n\nTheo giả thiết, số báo danh của Hiếu là số chẵn nên của Hiếu là 3780.\nSuy ra số báo danh của Nam là 3285."
    },
    {
        "id": "de3_sh_05",
        "type": "short",
        "content": "Cho hàm số: \\( y = 4\\sin x\\sin\\left(x+\\dfrac{\\pi}{2}\\right) \\). Giá trị lớn nhất và giá trị nhỏ nhất của y lần lượt là:",
        "blanks": [
            {"label": "Giá trị lớn nhất của y là:", "answers": ["2"]},
            {"label": "Giá trị nhỏ nhất của y là:", "answers": ["-2"]}
        ],
        "points": 1,
        "explanation": "Sử dụng công thức lượng giác phụ chéo: \\( \\sin\\left(x+\\dfrac{\\pi}{2}\\right) = \\cos x \\).\nKhi đó hàm số được viết lại: \\( y = 4\\sin x\\cos x = 2(2\\sin x\\cos x) = 2\\sin(2x) \\).\nVì \\( -1 \\le \\sin(2x) \\le 1 \\) với mọi \\( x \\in \\mathbb{R} \\), ta suy ra \\( -2 \\le y \\le 2 \\).\nVậy Giá trị lớn nhất của y là 2, Giá trị nhỏ nhất của y là -2."
    },
    {
        "id": "de3_sh_06",
        "type": "short",
        "content": "Cho hàm số: \\( f(x)=(x+10)^6 \\). Tính \\( f''(2) \\).",
        "blanks": [
            {"label": "\\( f''(2) = \\)", "answers": ["622080"]}
        ],
        "points": 1,
        "explanation": "Ta tính đạo hàm cấp 1: \\( f'(x)=6(x+10)^5 \\).\n\nTiếp tục tính đạo hàm cấp 2: \\( f''(x)=6 \\cdot 5(x+10)^4=30(x+10)^4 \\).\n\nThay \\( x=2 \\) vào biểu thức đạo hàm cấp 2 ta được: \\( f''(2)=30(2+10)^4=30 \\cdot 12^4=30 \\cdot 20736=622080 \\)."
    },
    {
        "id": "de3_mc_07",
        "type": "mc4",
        "content": "Cho hàm số: \\( y=\\dfrac{1+x}{1-x} \\). Nhận xét nào sau đây đúng?",
        "options": {
            "A": "Đồ thị hàm có TCN \\( y=1 \\), TCĐ \\( x=1 \\)",
            "B": "Đồ thị hàm có TCN \\( y=-1 \\), TCĐ \\( x=1 \\)",
            "C": "Đồ thị hàm có TCN \\( y=1 \\), TCĐ \\( x=-1 \\)",
            "D": "Đồ thị hàm có TCN \\( y=-1 \\), TCĐ \\( x=-1 \\)"
        },
        "correct": "B",
        "points": 1,
        "explanation": "Hàm số đã cho là hàm phân thức bậc nhất trên bậc nhất: \\( y=\\dfrac{x+1}{-x+1} \\).\n\n- Tiệm cận ngang (TCN): \\( \\lim_{x\\to\\pm\\infty} y = \\lim_{x\\to\\pm\\infty} \\dfrac{x+1}{-x+1} = \\dfrac{1}{-1} = -1 \\). Suy ra TCN là đường thẳng \\( y=-1 \\).\n\n- Tiệm cận đứng (TCĐ): Nghiệm của mẫu thức là \\( -x+1=0 \\Leftrightarrow x=1 \\). Hơn nữa, tử số tại \\( x=1 \\) bằng \\( 2 \\neq 0 \\). Suy ra TCĐ là đường thẳng \\( x=1 \\).\n\nĐối chiếu với các đáp án, ta thấy Đáp án B là chính xác."
    },
    {
        "id": "de3_tf_08",
        "type": "truefalse",
        "content": "Cho hình lăng trụ đứng \\( ABC.A'B'C' \\) có tam giác \\( ABC \\) vuông cân tại \\( A \\). Biết \\( BC=3\\sqrt{2}a \\), \\( AA'=4a \\). Các nhận định sau đây đúng hay sai?",
        "image": "CHÈN_LINK_ẢNH_CÂU_8_VÀO_ĐÂY", 
        "statements": [
            {"text": "\\( AB'=3a \\).", "correct": false},
            {"text": "Thể tích hình lăng trụ: \\( V=6a^3 \\).", "correct": false}
        ],
        "points": 1,
        "explanation": "Vì tam giác \\( ABC \\) vuông cân tại \\( A \\), áp dụng định lý Pytago ta có:\n\n\\( AB^2+AC^2=BC^2 \\Leftrightarrow 2AB^2=(3\\sqrt{2}a)^2=18a^2 \\Rightarrow AB=AC=3a \\).\n\n1. Xét mệnh đề 1: Do hình lăng trụ đứng nên \\( BB' \\perp (ABC) \\Rightarrow BB' \\perp AB \\). Tam giác \\( ABB' \\) vuông tại \\( B \\), ta có:\n\n\\( AB'=\\sqrt{AB^2+BB'^2}=\\sqrt{(3a)^2+(4a)^2}=\\sqrt{9a^2+16a^2}=5a \\neq 3a \\). \\( \\Rightarrow \\) Sai.\n\n2. Xét mệnh đề 2: Thể tích lăng trụ được tính theo công thức \\( V=B\\cdot h \\):\n\n\\( V = S_{\\triangle ABC} \\cdot AA' = \\left( \\dfrac{1}{2}AB \\cdot AC \\right) \\cdot AA' = \\left( \\dfrac{1}{2} \\cdot 3a \\cdot 3a \\right) \\cdot 4a = 18a^3 \\neq 6a^3 \\). \\( \\Rightarrow \\) Sai."
    },
    {
        "id": "de3_sh_09",
        "type": "short",
        "content": "Tính \\( l=\\lim_{x\\to 0}\\dfrac{1-\\cos 2x}{x} \\).",
        "blanks": [
            {"label": "l =", "answers": ["0"]}
        ],
        "points": 1,
        "explanation": "Ta có công thức nhân đôi: \\( 1-\\cos 2x=2\\sin^2 x \\).\n\nKhi đó, giới hạn được viết lại thành: \\( l=\\lim_{x\\to 0}\\dfrac{2\\sin^2 x}{x} = \\lim_{x\\to 0}\\left( 2\\sin x \\cdot \\dfrac{\\sin x}{x} \\right) \\).\n\nVì \\( \\lim_{x\\to 0}\\sin x=0 \\) và \\( \\lim_{x\\to 0}\\dfrac{\\sin x}{x}=1 \\),\n\nnên \\( l=2 \\cdot 0 \\cdot 1 = 0 \\)."
    },
    {
        "id": "de3_sh_10",
        "type": "short",
        "content": "Một hàng học sinh gồm 3 nam và 7 nữ được xếp thành 1 hàng ngang. Xác suất để không có bất kì 2 bạn nam nào đứng cạnh nhau là bao nhiêu?",
        "blanks": [
            {"label": "Xác suất =", "answers": ["7/15"]}
        ],
        "points": 1,
        "explanation": "Số phần tử của không gian mẫu: Xếp 10 học sinh thành một hàng ngang có \\( n(\\Omega)=10! \\) cách.\n\nGọi biến cố \\( A \\): \"Không có bất kì 2 bạn nam nào đứng cạnh nhau\".\n\n- Bước 1: Xếp 7 bạn nữ thành một hàng ngang có \\( 7! \\) cách. Khi đó tạo ra 8 khoảng trống (gồm 6 khoảng giữa các bạn nữ và 2 khoảng ở hai đầu).\n\n- Bước 2: Xếp 3 bạn nam vào 8 khoảng trống đó có \\( A_8^3 \\) cách.\n\nSuy ra số kết quả thuận lợi cho biến cố \\( A \\) là \\( n(A)=7! \\cdot A_8^3 \\).\n\nXác suất cần tìm: \\( P(A) = \\dfrac{n(A)}{n(\\Omega)} = \\dfrac{7! \\cdot A_8^3}{10!} = \\dfrac{7! \\cdot 8 \\cdot 7 \\cdot 6}{10 \\cdot 9 \\cdot 8 \\cdot 7!} = \\dfrac{7 \\cdot 6}{10 \\cdot 9} = \\dfrac{42}{90} = \\dfrac{7}{15} \\)."
    }

        ]
    }
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
