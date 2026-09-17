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
# =======================================================================
# SSO VỚI WORDPRESS (giống hệt cơ chế bên app TSA)
# =======================================================================
import hmac
import hashlib
import base64
from functools import wraps

WP_SSO_SECRET = os.environ.get("WP_SSO_SECRET", "doi-secret-nay-khi-deploy-that")
WP_TOKEN_MAX_AGE = 900  # token chỉ có hiệu lực 15 phút kể từ lúc WordPress tạo ra


def verify_wp_token(token):
    """Giải mã & kiểm tra chữ ký token do WordPress tạo. Trả về tên học sinh
    nếu hợp lệ và chưa hết hạn, trả về None nếu token sai/giả/hết hạn."""
    if not token:
        return None
    try:
        padded_token = token + "=" * (-len(token) % 4)
        raw = base64.urlsafe_b64decode(padded_token.encode("utf-8")).decode("utf-8")
        name, ts_str, sig = raw.rsplit("|", 2)
    except Exception:
        return None

    expected_sig = hmac.new(
        WP_SSO_SECRET.encode("utf-8"), f"{name}|{ts_str}".encode("utf-8"), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(sig, expected_sig):
        return None

    try:
        if time.time() - int(ts_str) > WP_TOKEN_MAX_AGE:
            return None
    except Exception:
        return None

    return name


def student_required(view_func):
    """Decorator: chặn truy cập nếu học sinh chưa đăng nhập qua SSO."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("student"):
            return redirect(url_for("student_login"))
        return view_func(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET"])
def student_login():
    if session.get("student"):
        return redirect(url_for("exam_list"))
    wp_token = request.args.get("wp_token")
    name = verify_wp_token(wp_token)
    if name:
        session["student"] = {"full_name": name, "sbd": ""}
        return redirect(url_for("exam_list"))
    return """
    <div style="text-align:center; padding:60px 20px; font-family:sans-serif;">
        <p>Bạn cần đăng nhập trên trang chính để làm bài thi thử HSA.</p>
    </div>
    """


@app.route("/logout")
def student_logout():
    session.pop("student", None)
    return redirect(url_for("student_login"))
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
        "name": "Đề thi tham khảo số 1 - Đánh giá năng lực học sinh THPT 2026",
        "seed": 2025101,   # để trộn thứ tự xen kẽ trắc nghiệm/điền đáp án cố định
        "mc4": [
                {
        "content": "Cho hàm số \\(y=\\begin{cases}x, \\text{ khi } x\\ge 0\\\\-x, \\text{ khi } x<0\\end{cases}\\). Khẳng định nào dưới đây đúng?",
        "options": {
            "A": "Hàm số không có đạo hàm tại \\(x=0\\)",
            "B": "\\(y'_{(0)}=1\\)",
            "C": "\\(y'_{(0)}=0\\)",
            "D": "\\(y'_{(0)}=-1\\)",
        },
        "correct": "A",
        "explanation": "Đây chính là hàm số \\(y=|x|\\), viết dưới dạng từng khoảng. Ta xét đạo hàm bên trái và bên phải tại \\(x=0\\).\n\nĐạo hàm của hàm số trên từng khoảng là:\n\\[y'=\\begin{cases}1, & x\\ge 0\\\\-1, & x<0\\end{cases}\\]\n\nDo đó:\n\\[y'_{(0^+)}=1 \\quad \\text{và} \\quad y'_{(0^-)}=-1\\]\n\nHai đạo hàm một bên này khác nhau (\\(1\\ne -1\\)), nghĩa là đạo hàm tại \\(x=0\\) không tồn tại (không có một giá trị đạo hàm duy nhất tại đó).\n\nVậy hàm số không có đạo hàm tại \\(x=0\\). Chọn đáp án A.",
    },
    {
    "content": "Thời gian chạy 50m của 20 học sinh được ghi lại trong bảng dưới đây:",
    "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/hsa_de1_cau2_bang.PNG",
    "options": {"A": "8,54", "B": "4", "C": "8,50", "D": "8,53"},
    "correct": "D",
    "explanation": "Với mẫu số liệu không ghép nhóm, số trung bình cộng được tính bằng cách lấy tổng của (giá trị × tần số tương ứng) rồi chia cho tổng số học sinh (tổng tần số).\n\nTổng số học sinh: \\(2+3+9+5+1=20\\) (khớp với đề bài).\n\nÁp dụng công thức:\n\\[\\bar{x}=\\dfrac{8{,}3\\times 2+8{,}4\\times 3+8{,}5\\times 9+8{,}7\\times 5+8{,}8\\times 1}{20}\\]\n\nTính tử số:\n\\[8{,}3\\times2=16{,}6;\\quad 8{,}4\\times3=25{,}2;\\quad 8{,}5\\times9=76{,}5;\\quad 8{,}7\\times5=43{,}5;\\quad 8{,}8\\times1=8{,}8\\]\n\\[16{,}6+25{,}2+76{,}5+43{,}5+8{,}8=170{,}6\\]\n\nVậy:\n\\[\\bar{x}=\\dfrac{170{,}6}{20}=8{,}53\\]\n\nChọn đáp án D.",
},
    {
        "content": "Chu kì của hàm số \\(y=\\sin\\left(\\dfrac{2}{5}x\\right).\\cos\\left(\\dfrac{2}{5}x\\right)\\) là \\(k\\pi\\). Giá trị của \\(k\\) là",
        "options": {"A": "5/2", "B": "5", "C": "5/4", "D": "10"},
        "correct": "A",
        "explanation": "Trước tiên, ta rút gọn biểu thức bằng công thức nhân đôi \\(\\sin\\alpha\\cos\\alpha=\\dfrac{1}{2}\\sin(2\\alpha)\\):\n\\[y=\\sin\\left(\\dfrac{2}{5}x\\right).\\cos\\left(\\dfrac{2}{5}x\\right)=\\dfrac{1}{2}\\sin\\left(\\dfrac{4}{5}x\\right)\\]\n\nHàm số dạng \\(A\\sin(ax+b)\\) (với \\(A, a\\ne 0\\)) là hàm tuần hoàn với chu kì:\n\\[T=\\dfrac{2\\pi}{|a|}\\]\n\nỞ đây \\(a=\\dfrac{4}{5}\\), nên:\n\\[T=\\dfrac{2\\pi}{\\frac{4}{5}}=2\\pi\\times\\dfrac{5}{4}=\\dfrac{5\\pi}{2}\\]\n\nSo với dạng \\(T=k\\pi\\), ta có \\(k=\\dfrac{5}{2}\\).\n\nChọn đáp án A.",
    },
    {
        "content": "Cho hàm số \\(y=f(x)\\) có bảng biến thiên như hình dưới. Tổng số đường tiệm cận ngang và tiệm cận đứng của đồ thị hàm số đã cho là",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/hsa_de1_cau4_bbt.PNG",
        "options": {"A": "0", "B": "1", "C": "2", "D": "3"},
        "correct": "C",
        "explanation": "Dựa vào bảng biến thiên, ta quan sát hành vi của hàm số khi \\(x\\) tiến ra vô cực và tại các điểm gián đoạn.\n\nKhi \\(x\\to -\\infty\\), \\(y\\to -2\\); và khi \\(x\\to 0^-\\), \\(y\\to -\\infty\\). Khi \\(x\\to +\\infty\\), \\(y\\to +\\infty\\).\n\nTa thấy \\(y\\to -2\\) khi \\(x\\to-\\infty\\), là một giá trị hữu hạn, nên đồ thị hàm số có 1 đường tiệm cận ngang là \\(y=-2\\).\n\nMặt khác, tại \\(x=0\\), hàm số có giới hạn tiến ra vô cực (từ bên trái là \\(-\\infty\\), từ bên phải là 8 — nghĩa là hàm không xác định liên tục qua \\(x=0\\) và có một nhánh tiến ra vô cực), nên đồ thị có 1 đường tiệm cận đứng là \\(x=0\\).\n\nVậy:\n- Số đường tiệm cận ngang: 1\n- Số đường tiệm cận đứng: 1\n\nTổng số đường tiệm cận ngang và tiệm cận đứng là \\(1+1=2\\). Chọn đáp án C.",
    },
    {
        "content": "Tìm nguyên hàm \\(F(t)=\\displaystyle\\int tx\\,dt\\).",
        "options": {
            "A": "\\(F(t)=x+t+C\\)",
            "B": "\\(F(t)=\\dfrac{x^2t}{2}+C\\)",
            "C": "\\(F(t)=\\dfrac{xt^2}{2}+C\\)",
            "D": "\\(F(t)=\\dfrac{(tx)^2}{2}+C\\)",
        },
        "correct": "C",
        "explanation": "Chú ý biểu thức lấy nguyên hàm là theo biến \\(t\\) (ký hiệu \\(dt\\)), nên ta coi \\(x\\) là một hằng số (tham số), không phải biến số cần tích phân.\n\nVì \\(x\\) là hằng số, ta đưa nó ra ngoài dấu tích phân:\n\\[F(t)=\\int tx\\,dt=x\\int t\\,dt=x\\cdot\\dfrac{t^2}{2}+C=\\dfrac{xt^2}{2}+C\\]\n\nVậy \\(F(t)=\\dfrac{xt^2}{2}+C\\). Chọn đáp án C.\n\n(Lưu ý: nếu nhầm lẫn coi \\(t\\) là hằng số và lấy nguyên hàm theo \\(x\\) thì sẽ ra kết quả sai ở đáp án B — đây là bẫy phổ biến của bài toán này.)",
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
        "content": "Tích tất cả giá trị của \\(a\\) để góc tạo bởi đường thẳng \\(\\begin{cases}x=4+at\\\\y=7-2t\\end{cases}\\ (t\\in\\mathbb{R})\\) và đường thẳng \\(3x+4y-2=0\\) bằng \\(45^\\circ\\) là bao nhiêu?",
        "options": {"A": "-4", "B": "4", "C": "-14", "D": "2/7"},
        "correct": "A",
        "explanation": "Gọi \\(\\varphi\\) là góc giữa hai đường thẳng đã cho.\n\nĐường thẳng thứ nhất có vectơ chỉ phương \\(\\vec{u}=(a;-2)\\).\n\nĐường thẳng \\(3x+4y-2=0\\) có vectơ chỉ phương \\(\\vec{v}=(4;-3)\\).\n\nÁp dụng công thức góc giữa hai đường thẳng:\n\\[\\cos\\varphi=|\\cos(\\vec{u},\\vec{v})|=\\dfrac{|\\vec{u}.\\vec{v}|}{|\\vec{u}|.|\\vec{v}|}\\]\n\nThay số:\n\\[\\cos 45^\\circ=\\dfrac{|4a+6|}{\\sqrt{a^2+4}.\\sqrt{16+9}} \\Leftrightarrow \\dfrac{1}{\\sqrt2}=\\dfrac{|4a+6|}{5\\sqrt{a^2+4}}\\]\n\nKhử căn và giá trị tuyệt đối bằng cách bình phương hai vế:\n\\[5\\sqrt{a^2+4}=\\sqrt2\\,|4a+6| \\Rightarrow 25(a^2+4)=2(4a+6)^2\\]\n\\[\\Leftrightarrow 25a^2+100=32a^2+96a+72\\]\n\\[\\Leftrightarrow 7a^2+96a-28=0\\]\n\nGiải phương trình bậc hai, ta được hai nghiệm:\n\\[a=\\dfrac{2}{7} \\quad \\text{hoặc} \\quad a=-14\\]\n\nĐề bài hỏi tích tất cả các giá trị của a, nên:\n\\[\\dfrac{2}{7}\\times(-14)=-4\\]\n\nChọn đáp án A.",
    },
    {
        "content": "Một công ty xây dựng khảo sát khách hàng xem họ có nhu cầu mua nhà ở mức giá nào. Kết quả khảo sát được ghi lại ở bảng sau:",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/hsa_de1_cau7_bang.png",
        "options": {"A": "20,4", "B": "19,4", "C": "21,4", "D": "18,4"},
        "correct": "B",
        "explanation": "Đây là mẫu số liệu ghép nhóm nên ta cần tìm mốt bằng công thức riêng cho dữ liệu ghép nhóm, không phải chỉ tìm nhóm có tần số lớn nhất.\n\nQuan sát bảng, nhóm có số khách hàng lớn nhất (tần số lớn nhất) là nhóm \\([18;22)\\) với 120 khách hàng — đây là nhóm chứa mốt.\n\nĐặt các giá trị cần dùng:\n- \\(u_m=18\\) (đầu mút trái của nhóm chứa mốt)\n- \\(n_m=120\\) (tần số nhóm chứa mốt)\n- \\(n_{m-1}=78\\) (tần số nhóm liền trước)\n- \\(n_{m+1}=45\\) (tần số nhóm liền sau)\n- Độ dài mỗi nhóm là \\(22-18=4\\)\n\nÁp dụng công thức tính mốt của mẫu số liệu ghép nhóm:\n\\[M_0=u_m+\\dfrac{n_m-n_{m-1}}{(n_m-n_{m-1})+(n_m-n_{m+1})}\\times (22-18)\\]\n\nThay số:\n\\[M_0=18+\\dfrac{120-78}{(120-78)+(120-45)}\\times 4=18+\\dfrac{42}{42+75}\\times4\\]\n\\[=18+\\dfrac{42}{117}\\times4\\approx 18+1{,}4=19{,}4\\]\n\nVậy mốt của mẫu số liệu xấp xỉ 19,4. Chọn đáp án B.",
    },
    {
        "content": "Trong mặt phẳng Oxy, điểm \\(M\\) nằm trên đường tròn \\((x+3)^2+(y-4)^2=4\\) sao cho độ dài đoạn thẳng OM là ngắn nhất. Hoành độ điểm \\(M\\) là:",
        "options": {"A": "-9/5", "B": "12/5", "C": "-21/5", "D": "9/5"},
        "correct": "A",
        "explanation": "Trước tiên tìm tâm và bán kính của đường tròn.\n\nĐường tròn \\((x+3)^2+(y-4)^2=4\\) có tâm \\(I(-3;4)\\) và bán kính \\(R=2\\).\n\nVì O nằm ngoài đường tròn (do \\(OI=\\sqrt{9+16}=5>R=2\\)), điểm M trên đường tròn gần O nhất chính là giao điểm của đoạn thẳng OI với đường tròn, nằm giữa O và I.\n\nViết phương trình đường thẳng OI: đi qua \\(O(0;0)\\), nhận \\(\\overrightarrow{OI}=(-3;4)\\) làm vectơ chỉ phương:\n\\[\\begin{cases}x=-3t\\\\y=4t\\end{cases}\\ (t\\in\\mathbb{R})\\]\n\nTa có \\(OM\\le |OI-R|=5-2=3\\), và OM ngắn nhất khi \\(OM=3\\), tức M là điểm trên đoạn OI cách O một khoảng bằng 3 (nằm giữa O và I).\n\nVì \\(OI=5\\) và \\(OM=3\\), ta có tỉ lệ \\(\\overrightarrow{OM}=\\dfrac{3}{5}\\overrightarrow{OI}\\), suy ra:\n\\[M=\\left(\\dfrac{3}{5}\\times(-3);\\dfrac{3}{5}\\times4\\right)=\\left(-\\dfrac{9}{5};\\dfrac{12}{5}\\right)\\]\n\nVậy hoành độ điểm M là \\(-\\dfrac{9}{5}\\). Chọn đáp án A.",
    },
    {
        "content": "Một học sinh dùng giác kế, đứng cách chân cột cờ 10m rồi chỉnh mặt trước cao bằng mắt của mình để xác định góc nâng (góc tạo bởi tia sáng đi thẳng từ đỉnh cột cờ với mắt) so với phương nằm ngang. Khi đó góc nâng đo được \\(31^\\circ\\). Biết khoảng cách từ mặt sân đến mắt học sinh đó bằng 1,5m. Chiều cao cột cờ gần nhất với giá trị nào?",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/hsa_de1_cau9_giacke.png",
        "options": {"A": "6m", "B": "16,6m", "C": "7,5m", "D": "5,0m"},
        "correct": "C",
        "explanation": "Gọi AB là khoảng cách từ chân đến tầm mắt của học sinh, nên \\(AB=1{,}5\\)m.\n\nAC là khoảng cách từ chân học sinh đến chân cột cờ, nên \\(AC=10\\)m.\n\nCD là chiều cao cột cờ cần tìm, BE là đường ngang tầm mắt (song song với AC).\n\nGóc nâng chính là góc \\(\\widehat{DBE}=31^\\circ\\).\n\nVì tứ giác ABEC là hình chữ nhật (AB vuông góc AC, BE song song AC) nên:\n\\[BE=AC=10\\text{m}, \\qquad CE=AB=1{,}5\\text{m}\\]\n\nXét tam giác vuông BED (vuông tại E), ta có:\n\\[\\tan(\\widehat{DBE})=\\dfrac{DE}{BE} \\Rightarrow DE=BE\\times\\tan31^\\circ=10\\times\\tan31^\\circ\\approx 6\\text{m}\\]\n\nChiều cao cột cờ chính là tổng đoạn CE (đã tính ở dưới, tức phần từ chân cột đến ngang tầm mắt) và DE (phần từ tầm mắt lên đến đỉnh cột):\n\\[CD=CE+DE=1{,}5+6=7{,}5\\text{m}\\]\n\nVậy chiều cao cột cờ gần nhất với 7,5m. Chọn đáp án C.",
    },
    {
        "content": "Tập nghiệm của bất phương trình \\(x^2-x-12\\le 0\\) là?",
        "options": {
            "A": "[-3;4]",
            "B": "(-3;4)",
            "C": "\\((-\\infty;-3)\\cup(4;+\\infty)\\)",
            "D": "\\((-\\infty;-3]\\cup[4;+\\infty)\\)",
        },
        "correct": "A",
        "explanation": "Trước tiên giải phương trình \\(x^2-x-12=0\\) để tìm các nghiệm, làm mốc lập bảng xét dấu.\n\nÁp dụng công thức nghiệm hoặc phân tích nhân tử:\n\\[x^2-x-12=0 \\Leftrightarrow (x-4)(x+3)=0 \\Leftrightarrow \\begin{bmatrix}x=4\\\\x=-3\\end{bmatrix}\\]\n\nLập bảng xét dấu cho tam thức \\(f(x)=x^2-x-12\\) (có hệ số \\(a=1>0\\), nên f(x) dương ở ngoài khoảng hai nghiệm và âm ở trong khoảng hai nghiệm):\n\n\\(x\\): \\(-\\infty\\) ... \\(-3\\) ... \\(4\\) ... \\(+\\infty\\)\n\n\\(f(x)\\): \\(+\\) ... \\(0\\) ... \\(-\\) ... \\(0\\) ... \\(+\\)\n\nBất phương trình yêu cầu \\(f(x)\\le 0\\), tức là ta lấy khoảng mà f(x) âm hoặc bằng 0, đó là đoạn giữa hai nghiệm (bao gồm cả hai đầu mút vì có dấu bằng):\n\\[f(x)\\le 0 \\Leftrightarrow -3\\le x\\le 4\\]\n\nVậy tập nghiệm là \\([-3;4]\\). Chọn đáp án A.",
    },
    {
        "content": "Một tổ chăm sóc khách hàng của một trung tâm điện tử gồm 12 nhân viên. Số cách phân công 3 nhân viên đi đến ba địa điểm khác nhau để chăm sóc khách hàng là",
        "options": {"A": "1320", "B": "1230", "C": "220", "D": "1728"},
        "correct": "A",
        "explanation": "Vì 3 nhân viên được phân công đến 3 địa điểm khác nhau, nên đây là bài toán sắp xếp có phân biệt vị trí (mỗi địa điểm là một vai trò riêng biệt), không phải chỉ chọn ra một nhóm 3 người.\n\nDo có sự phân biệt thứ tự (ai đến địa điểm nào cũng quan trọng), ta sử dụng công thức chỉnh hợp chập 3 của 12 phần tử:\n\\[A_{12}^3=\\dfrac{12!}{(12-3)!}=12\\times11\\times10=1320\\]\n\nVậy có 1320 cách phân công. Chọn đáp án A.",
    },
    {
        "content": "Một hộp chứa 9 chiếc thẻ được đánh số từ 1 đến 9. Lấy ngẫu nhiên 3 chiếc thẻ từ hộp. Tính xác suất để tổng các số ghi trên 3 chiếc thẻ được lấy ra là một số lẻ.",
        "options": {"A": "10/21", "B": "11/21", "C": "5/21", "D": "4/21"},
        "correct": "A",
        "explanation": "Số phần tử của không gian mẫu (số cách chọn ngẫu nhiên 3 thẻ trong 9 thẻ, không phân biệt thứ tự):\n\\[n(\\Omega)=C_9^3=84\\]\n\nGọi A là biến cố \"tổng các số ghi trên 3 chiếc thẻ được lấy ra là một số lẻ\".\n\nĐể tổng 3 số là số lẻ, cần có một số lẻ chữ số lẻ trong 3 số được chọn (1 hoặc 3 số lẻ). Trong tập từ 1 đến 9 có 5 số lẻ (1,3,5,7,9) và 4 số chẵn (2,4,6,8).\n\nTa xét 2 trường hợp cho biến cố A:\n- Cả 3 số đều là số lẻ: có \\(C_5^3\\) cách chọn.\n- Có 2 số chẵn và 1 số lẻ: có \\(C_4^2\\times C_5^1\\) cách chọn.\n\nTính số cách thỏa mãn:\n\\[n(A)=C_5^3+C_4^2.C_5^1=10+6\\times5=10+30=40\\]\n\nXác suất cần tìm:\n\\[P(A)=\\dfrac{n(A)}{n(\\Omega)}=\\dfrac{40}{84}=\\dfrac{10}{21}\\]\n\nVậy xác suất là \\(\\dfrac{10}{21}\\). Chọn đáp án A.",
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
        "content": "Trong hệ trục tọa độ Oxy, cho đường thẳng \\(d:\\begin{cases}x=-4t+1\\\\y=-2+3t\\end{cases}\\). Một vectơ chỉ phương của \\(d\\) là:",
        "options": {"A": "(1;3)", "B": "(-4;2)", "C": "(4;-3)", "D": "(-1;3)"},
        "correct": "C",
        "explanation": "Với đường thẳng cho dưới dạng phương trình tham số \\(d:\\begin{cases}x=x_0+at\\\\y=y_0+bt\\end{cases}\\), vectơ \\(\\vec{u}=(a;b)\\) (hệ số đứng trước t ở mỗi phương trình) chính là một vectơ chỉ phương của đường thẳng.\n\nĐối chiếu với đề bài:\n\\[\\begin{cases}x=-4t+1\\\\y=-2+3t\\end{cases}\\]\n\nHệ số của \\(t\\) trong phương trình \\(x\\) là \\(-4\\), trong phương trình \\(y\\) là \\(3\\).\n\nVậy một vectơ chỉ phương của \\(d\\) là \\((-4;3)\\).\n\nLưu ý rằng một đường thẳng có vô số vectơ chỉ phương, chúng đều cùng phương (tỉ lệ) với nhau. Nhân vectơ \\((-4;3)\\) với \\(-1\\) ta được \\((4;-3)\\) — đây cũng là một vectơ chỉ phương hợp lệ của \\(d\\), và nó khớp với đáp án C.\n\nChọn đáp án C.",
    },
    {
        "content": "Tìm tất cả các giá trị của tham số \\(m\\) để bất phương trình \\(x^2-(m+2)x+8m+1\\le 0\\) vô nghiệm.",
        "options": {
            "A": "\\(m\\in[0;28]\\)",
            "B": "\\(m\\in(0;28)\\)",
            "C": "\\(m\\in(-\\infty;0)\\cup(28;+\\infty)\\)",
            "D": "\\(m\\in(-\\infty;0]\\cup[28;+\\infty)\\)",
        },
        "correct": "B",
        "explanation": "Đặt \\(f(x)=x^2-(m+2)x+8m+1\\). Bất phương trình \\(f(x)\\le 0\\) vô nghiệm nghĩa là không tồn tại giá trị \\(x\\) nào làm cho \\(f(x)\\le 0\\), tức là \\(f(x)>0\\) đúng với mọi \\(x\\in\\mathbb{R}\\).\n\nVới tam thức bậc hai có hệ số \\(a>0\\), điều kiện để \\(f(x)>0,\\,\\forall x\\) là \\(\\Delta<0\\) (parabol nằm hoàn toàn phía trên trục hoành, không cắt và không tiếp xúc với trục hoành).\n\nỞ đây \\(a=1>0\\) (thỏa mãn). Ta tính \\(\\Delta\\):\n\\[\\Delta=(m+2)^2-4(8m+1)\\]\n\nYêu cầu \\(\\Delta<0\\):\n\\[(m+2)^2-4(8m+1)<0\\]\n\\[\\Leftrightarrow m^2+4m+4-32m-4<0\\]\n\\[\\Leftrightarrow m^2-28m<0\\]\n\\[\\Leftrightarrow m(m-28)<0\\]\n\\[\\Leftrightarrow 0<m<28\\]\n\nVậy \\(m\\in(0;28)\\). Chọn đáp án B.",
    },
    {
        "content": "Số cách xếp 5 học sinh ngồi vào một dãy gồm 5 chiếc ghế sao cho mỗi ghế có đúng một học sinh ngồi là",
        "options": {"A": "600", "B": "120", "C": "3125", "D": "720"},
        "correct": "B",
        "explanation": "Đây là bài toán sắp xếp 5 học sinh vào 5 vị trí ghế khác nhau, mỗi ghế đúng một học sinh — tức là ta cần đếm số hoán vị của 5 phần tử.\n\nSố cách xếp 5 học sinh vào 5 chiếc ghế (mỗi cách xếp là một hoán vị của 5 phần tử) là:\n\\[5! = 5\\times4\\times3\\times2\\times1=120 \\text{ (cách)}\\]\n\nVậy có 120 cách xếp. Chọn đáp án B.",
    },
    {
        "content": "Cho dãy số \\((u_n)\\) xác định bởi \\(u_1=1\\) và \\(u_{n+1}=\\sqrt{3u_n^2+2}\\). Đặt \\(S=u_1^2+u_2^2+\\cdots+u_{2023}^2+2023\\). Hỏi \\(S\\) có bao nhiêu chữ số?",
        "options": {"A": "966", "B": "965", "C": "964", "D": "963"},
        "correct": "A",
        "explanation": "Từ công thức truy hồi \\(u_{n+1}=\\sqrt{3u_n^2+2}\\), bình phương hai vế ta được:\n\\[u_{n+1}^2=3u_n^2+2 \\Leftrightarrow u_{n+1}^2+1=3(u_n^2+1)\\]\n\nĐặt \\(v_n=u_n^2+1\\), ta có \\(v_{n+1}=3v_n\\), nghĩa là \\((v_n)\\) là một cấp số nhân với công bội \\(q=3\\).\n\nSố hạng đầu: \\(v_1=u_1^2+1=1+1=2\\).\n\nSuy ra công thức tổng quát: \\(v_n=2\\cdot3^{n-1}\\), tức là:\n\\[u_n^2=2\\cdot3^{n-1}-1\\]\n\nBây giờ ta tính tổng \\(S\\). Ta có:\n\\[\\sum_{n=1}^{2023}u_n^2=\\sum_{n=1}^{2023}\\left(2\\cdot3^{n-1}-1\\right)=2\\left(1+3+3^2+\\cdots+3^{2022}\\right)-2023\\]\n\nCộng thêm 2023 theo đề bài (\\(S\\) đã bao gồm \\(+2023\\)), phần \\(-2023\\) và \\(+2023\\) triệt tiêu nhau:\n\\[S=2\\left(1+3+3^2+\\cdots+3^{2022}\\right)=2\\cdot\\dfrac{3^{2023}-1}{3-1}=3^{2023}-1\\]\n\nBây giờ ta tìm số chữ số của \\(S=3^{2023}-1\\). Vì \\(S+1=3^{2023}\\), số chữ số của \\(3^{2023}\\) là:\n\\[\\lfloor 2023\\log 3\\rfloor+1=966 \\text{ (chữ số)}\\]\n\nVì \\(3^{2023}\\) là một số lẻ, việc trừ đi 1 (để ra \\(S\\)) không thể làm giảm số chữ số xuống 965 (điều đó chỉ xảy ra nếu \\(3^{2023}\\) có dạng \\(10^{965}\\), là một số chẵn — vô lý). Do đó \\(S\\) cũng có đúng 966 chữ số.\n\nVậy \\(S\\) có 966 chữ số. Chọn đáp án A.",
    },
    {
        "content": "Giới hạn \\(L=\\displaystyle\\lim \\dfrac{3n-1}{n+2}\\) bằng",
        "options": {"A": "\\(+\\infty\\)", "B": "0", "C": "1", "D": "3"},
        "correct": "D",
        "explanation": "Đây là giới hạn của một phân thức có bậc tử và bậc mẫu bằng nhau (đều là bậc 1 theo \\(n\\)), nên ta chia cả tử và mẫu cho \\(n\\) (lũy thừa bậc cao nhất) để tính giới hạn.\n\nChia cả tử và mẫu cho \\(n\\):\n\\[L=\\lim\\dfrac{3n-1}{n+2}=\\lim\\dfrac{3-\\dfrac{1}{n}}{1+\\dfrac{2}{n}}\\]\n\nKhi \\(n\\to+\\infty\\), các số hạng \\(\\dfrac{1}{n}\\) và \\(\\dfrac{2}{n}\\) đều tiến về 0, nên:\n\\[L=\\dfrac{3-0}{1+0}=3\\]\n\nVậy \\(L=3\\). Chọn đáp án D.",
    },
    {
        "content": "Biết bất phương trình \\(\\log_2(3^x-3)\\cdot\\log_8\\left(\\dfrac{3^x}{4}-\\dfrac{3}{4}\\right)\\le 1\\) có tập nghiệm là đoạn \\([a;b]\\). Giá trị biểu thức \\(a+b\\) bằng",
        "options": {
            "A": "\\(1+\\log_3 77\\)",
            "B": "\\(\\log_3\\dfrac{77}{2}\\)",
            "C": "\\(-2+\\log_2\\dfrac{77}{2}\\)",
            "D": "\\(-1+\\log_2 77\\)",
        },
        "correct": "B",
        "explanation": "Trước tiên tìm điều kiện xác định:\n\\[\\begin{cases}3^x-3>0\\\\\\dfrac{3^x}{4}-\\dfrac{3}{4}>0\\end{cases}\\Leftrightarrow x>1\\]\n\n(Hai điều kiện này thực chất tương đương nhau, vì \\(\\dfrac{3^x}{4}-\\dfrac{3}{4}=\\dfrac{3^x-3}{4}\\), cùng dấu với \\(3^x-3\\).)\n\nNhận xét rằng \\(\\dfrac{3^x}{4}-\\dfrac{3}{4}=\\dfrac{3^x-3}{4}\\), nên ta có thể viết lại log thứ hai theo cùng biểu thức với log thứ nhất:\n\\[\\log_8\\left(\\dfrac{3^x-3}{4}\\right)=\\log_8(3^x-3)-\\log_8 4=\\dfrac{1}{3}\\log_2(3^x-3)-\\dfrac{2}{3}\\]\n\n(vì \\(\\log_8 t=\\dfrac{1}{3}\\log_2 t\\) và \\(\\log_2 4=2\\))\n\nĐặt \\(t=\\log_2(3^x-3)\\). Bất phương trình trở thành:\n\\[t\\cdot\\dfrac{1}{3}(t-2)\\le 1\\]\n\\[\\Leftrightarrow t(t-2)\\le 3\\]\n\\[\\Leftrightarrow t^2-2t-3\\le 0\\]\n\\[\\Leftrightarrow (t-3)(t+1)\\le 0\\]\n\\[\\Leftrightarrow -1\\le t\\le 3\\]\n\nTrở lại biến \\(x\\):\n\\[-1\\le \\log_2(3^x-3)\\le 3\\]\n\\[\\Leftrightarrow 2^{-1}\\le 3^x-3\\le 2^3\\]\n\\[\\Leftrightarrow \\dfrac{1}{2}\\le 3^x-3\\le 8\\]\n\\[\\Leftrightarrow \\dfrac{7}{2}\\le 3^x\\le 11\\]\n\nLấy \\(\\log_3\\) hai vế:\n\\[\\log_3\\dfrac{7}{2}\\le x\\le \\log_3 11\\]\n\nVậy \\(a=\\log_3\\dfrac{7}{2}\\), \\(b=\\log_3 11\\). Tính tổng:\n\\[a+b=\\log_3\\dfrac{7}{2}+\\log_3 11=\\log_3\\left(\\dfrac{7}{2}\\times 11\\right)=\\log_3\\dfrac{77}{2}\\]\n\nChọn đáp án B.",
    },
              {
        "content": "Hai xạ thủ cùng bắn, mỗi người một viên đạn vào bia một cách độc lập với nhau. Xác suất bắn trúng bia của hai xạ thủ lần lượt là \\(\\dfrac{1}{3}\\) và \\(\\dfrac{1}{4}\\). Tính xác suất của biến cố có ít nhất một xạ thủ không bắn trúng bia.",
        "options": {"A": "1/3", "B": "1/6", "C": "11/12", "D": "2/3"},
        "correct": "C",
        "explanation": "Xác suất để xạ thủ thứ nhất bắn không trúng bia là:\n\\[1-\\dfrac{1}{3}=\\dfrac{2}{3}\\]\n\nXác suất để xạ thủ thứ hai bắn không trúng bia là:\n\\[1-\\dfrac{1}{4}=\\dfrac{3}{4}\\]\n\nGọi A là biến cố \"Có ít nhất một xạ thủ không bắn trúng bia\". Biến cố A xảy ra trong 3 trường hợp (loại trừ trường hợp cả hai đều bắn trúng):\n\n- Người thứ nhất trúng, người thứ hai không trúng: \\(\\dfrac{1}{3}\\times\\dfrac{3}{4}=\\dfrac{1}{4}\\)\n- Người thứ nhất không trúng, người thứ hai trúng: \\(\\dfrac{2}{3}\\times\\dfrac{1}{4}=\\dfrac{1}{6}\\)\n- Cả hai đều không trúng: \\(\\dfrac{2}{3}\\times\\dfrac{3}{4}=\\dfrac{1}{2}\\)\n\nCộng lại theo quy tắc cộng xác suất (các biến cố xung khắc nhau):\n\\[P(A)=\\dfrac{1}{4}+\\dfrac{1}{6}+\\dfrac{1}{2}=\\dfrac{3}{12}+\\dfrac{2}{12}+\\dfrac{6}{12}=\\dfrac{11}{12}\\]\n\n(Cách làm nhanh hơn: dùng biến cố đối — biến cố \"cả hai đều bắn trúng\" có xác suất \\(\\dfrac{1}{3}\\times\\dfrac{1}{4}=\\dfrac{1}{12}\\), nên \\(P(A)=1-\\dfrac{1}{12}=\\dfrac{11}{12}\\), cho cùng kết quả.)\n\nVậy xác suất cần tìm là \\(\\dfrac{11}{12}\\). Chọn đáp án C.",
    },
    {
        "content": "Trong không gian với hệ tọa độ Oxyz, cho hình vuông ABCD, \\(B(3;0;8)\\), \\(D(-5;-4;0)\\). Biết đỉnh A thuộc mặt phẳng (Oxy) và có tọa độ là những số nguyên, khi đó \\(|\\overrightarrow{CA}+\\overrightarrow{CB}|\\) bằng:",
        "options": {"A": "6√10", "B": "10√6", "C": "10√5", "D": "5√10"},
        "correct": "A",
        "explanation": "Ta có trung điểm của BD là \\(I(-1;-2;4)\\), và độ dài đường chéo \\(BD=\\sqrt{(3+5)^2+(0+4)^2+(8-0)^2}=\\sqrt{64+16+64}=12\\).\n\nVì A thuộc mặt phẳng (Oxy) nên A có dạng \\(A(a;b;0)\\).\n\nVì ABCD là hình vuông, ta có hai điều kiện: hai cạnh kề bằng nhau (\\(AB=AD\\)) và đường chéo AI bằng nửa đường chéo BD (do I là tâm hình vuông, cách đều 4 đỉnh một khoảng bằng nửa đường chéo):\n\\[\\begin{cases}AB^2=AD^2\\\\AI^2=\\left(\\dfrac{1}{2}BD\\right)^2\\end{cases}\\]\n\nThay tọa độ vào:\n\\[\\begin{cases}(a-3)^2+b^2+8^2=(a+5)^2+(b+4)^2\\\\(a+1)^2+(b+2)^2+4^2=36\\end{cases}\\]\n\nRút gọn phương trình thứ nhất, ta được \\(b=4-2a\\). Thay vào phương trình thứ hai:\n\\[(a+1)^2+(6-2a)^2=20\\]\n\nGiải ra ta được hai nghiệm:\n\\[\\begin{cases}a=1\\\\b=2\\end{cases} \\quad \\text{hoặc} \\quad \\begin{cases}a=\\dfrac{17}{5}\\\\b=-\\dfrac{14}{5}\\end{cases}\\]\n\nVì đề bài yêu cầu tọa độ A là số nguyên, ta loại nghiệm thứ hai (không nguyên), chỉ nhận:\n\\[A(1;2;0)\\]\n\nTừ tính chất hình vuông ABCD, điểm C đối xứng với A qua tâm I, nên \\(C=2I-A=(-2\\times1-1;\\,-2\\times2-2;\\,2\\times4-0)\\), tính lại chính xác: \\(C=2I-A=(-1\\times2-1;\\,-2\\times2-2;\\,4\\times2-0)=(-3;-6;8)\\).\n\nTừ đó:\n\\[\\overrightarrow{CA}=A-C=(4;8;-8), \\qquad \\overrightarrow{CB}=B-C=(6;6;0)\\]\n\nCộng hai vectơ:\n\\[\\overrightarrow{CA}+\\overrightarrow{CB}=(10;14;-8)\\]\n\nTính độ dài:\n\\[|\\overrightarrow{CA}+\\overrightarrow{CB}|=\\sqrt{10^2+14^2+(-8)^2}=\\sqrt{100+196+64}=\\sqrt{360}=6\\sqrt{10}\\]\n\nChọn đáp án A.",
    },
    {
        "content": "Hàm số \\(f(x)\\) có đạo hàm xác định trên \\(\\mathbb{R}\\) thỏa mãn \\(y=f(x)+f(-x)\\) đồng biến trên khoảng \\((1;5)\\). Khi đó hàm số \\(y=f(x)+f(-x)\\) nghịch biến trên khoảng nào?",
        "options": {"A": "(-1;1)", "B": "(1;2)", "C": "(-3;-1)", "D": "(-2;0)"},
        "correct": "C",
        "explanation": "Đặt \\(g(x)=f(x)+f(-x)\\). Ta có đạo hàm:\n\\[g'(x)=f'(x)-f'(-x)\\]\n\nTheo giả thiết, \\(g(x)\\) đồng biến trên \\((1;5)\\), nghĩa là:\n\\[g'(x)=f'(x)-f'(-x)>0,\\quad \\forall x\\in(1;5)\\]\n\nBây giờ ta đặt \\(x=-t\\), khi \\(x\\in(1;5)\\) thì \\(t\\in(-5;-1)\\). Thay vào bất đẳng thức trên:\n\\[f'(-t)-f'(t)>0,\\quad \\forall t\\in(-5;-1)\\]\n\\[\\Leftrightarrow f'(t)-f'(-t)<0,\\quad \\forall t\\in(-5;-1)\\]\n\nĐổi lại tên biến t thành x (chỉ là ký hiệu), ta có:\n\\[f'(x)-f'(-x)<0,\\quad \\forall x\\in(-5;-1)\\]\n\nTức là \\(g'(x)<0\\) trên khoảng \\((-5;-1)\\), nghĩa là hàm số \\(g(x)=f(x)+f(-x)\\) nghịch biến trên \\((-5;-1)\\).\n\nTrong các đáp án cho sẵn, khoảng \\((-3;-1)\\) nằm trọn trong \\((-5;-1)\\), nên hàm số chắc chắn nghịch biến trên \\((-3;-1)\\).\n\nChọn đáp án C.",
    },
    {
        "content": "Khoảng cách giữa hai điểm cực trị của đồ thị hàm số \\(y=(x-2)^2(x+1)\\) là",
        "options": {"A": "2√5", "B": "5√2", "C": "4", "D": "2"},
        "correct": "A",
        "explanation": "Trước tiên khai triển và tính đạo hàm để tìm các điểm cực trị.\n\nÁp dụng quy tắc đạo hàm của tích, với \\(u=(x-2)^2\\) và \\(v=(x+1)\\):\n\\[f'(x)=2(x-2)(x+1)+(x-2)^2\\]\n\nRút gọn:\n\\[f'(x)=(x-2)\\left[2(x+1)+(x-2)\\right]=(x-2)(3x)=3x^2-6x\\]\n\nGiải phương trình \\(f'(x)=0\\):\n\\[3x^2-6x=0 \\Leftrightarrow 3x(x-2)=0 \\Leftrightarrow \\begin{bmatrix}x=0\\\\x=2\\end{bmatrix}\\]\n\nTính giá trị hàm số tại hai điểm này:\n- Tại \\(x=0\\): \\(y=(0-2)^2(0+1)=4\\times1=4\\)\n- Tại \\(x=2\\): \\(y=(2-2)^2(2+1)=0\\)\n\nVậy hai điểm cực trị là \\((0;4)\\) và \\((2;0)\\).\n\nÁp dụng công thức tính khoảng cách giữa hai điểm:\n\\[d=\\sqrt{(0-2)^2+(4-0)^2}=\\sqrt{4+16}=\\sqrt{20}=2\\sqrt5\\]\n\nVậy khoảng cách giữa hai điểm cực trị là \\(2\\sqrt5\\). Chọn đáp án A.",
    },
    {
        "content": "Nhiệt độ ngoài trời ở một thành phố vào các thời điểm khác nhau trong ngày có thể được mô phỏng bởi công thức \\(h(t)=29+3\\sin\\dfrac{\\pi}{12}(t-9)\\), với \\(h\\) tính bằng \\(^\\circ C\\) và \\(t\\) là thời gian trong ngày tính bằng giờ. Thời gian nhiệt độ cao nhất trong ngày là:",
        "options": {"A": "13 giờ", "B": "15 giờ", "C": "12 giờ", "D": "14 giờ"},
        "correct": "B",
        "explanation": "Vì hàm số sin luôn nhận giá trị trong đoạn \\([-1;1]\\), ta có:\n\\[-1\\le\\sin\\dfrac{\\pi}{12}(t-9)\\le1,\\quad \\forall t\\]\n\nNhân cả ba vế với 3 rồi cộng thêm 29:\n\\[-3\\le 3\\sin\\dfrac{\\pi}{12}(t-9)\\le3 \\Leftrightarrow 26\\le h(t)\\le32\\]\n\nDo đó nhiệt độ cao nhất trong ngày là \\(32^\\circ C\\), đạt được khi:\n\\[\\sin\\dfrac{\\pi}{12}(t-9)=1\\]\n\nGiải phương trình lượng giác cơ bản này:\n\\[\\dfrac{\\pi}{12}(t-9)=\\dfrac{\\pi}{2}+k2\\pi \\Leftrightarrow t=15+24k,\\ (k\\in\\mathbb{Z})\\]\n\nVì thời gian trong ngày thỏa \\(0\\le t\\le24\\), thay vào điều kiện:\n\\[0\\le15+24k\\le24 \\Leftrightarrow -\\dfrac{15}{24}\\le k\\le\\dfrac{9}{24}\\]\n\nDo \\(k\\) nguyên, chỉ có \\(k=0\\) thỏa mãn, khi đó \\(t=15\\).\n\nVậy lúc 15 giờ là thời điểm nhiệt độ cao nhất trong ngày. Chọn đáp án B.",
    },
    {
        "content": "Cho hàm số \\(y=f(x)\\) có bảng biến thiên như hình dưới. Số nghiệm thực của phương trình \\(2f(x)-11=0\\) là",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/hsa1_cau22_bbt.PNG",
        "options": {"A": "2", "B": "3", "C": "4", "D": "0"},
        "correct": "A",
        "explanation": "Trước tiên biến đổi phương trình về dạng \\(f(x)=a\\) để so sánh với đồ thị hàm số đã cho.\n\nTa có:\n\\[2f(x)-11=0 \\Leftrightarrow f(x)=\\dfrac{11}{2}\\]\n\nSố nghiệm của phương trình \\(f(x)=\\dfrac{11}{2}\\) chính là số giao điểm của đồ thị hàm số \\(y=f(x)\\) với đường thẳng nằm ngang \\(y=\\dfrac{11}{2}=5{,}5\\).\n\nDựa vào bảng biến thiên, ta thấy hàm số có các khoảng biến thiên như sau: đi từ \\(+\\infty\\) giảm xuống 1 (tại \\(x=-1\\)), tăng lên 2 (tại \\(x=0\\)), giảm xuống 1 (tại \\(x=1\\)), rồi tăng ra \\(+\\infty\\).\n\nGiá trị \\(y=5{,}5\\) lớn hơn giá trị cực đại địa phương là 2 (đạt tại \\(x=0\\)), nên đường thẳng \\(y=5{,}5\\) chỉ có thể cắt đồ thị ở hai nhánh ngoài cùng — nhánh bên trái (đi từ \\(+\\infty\\) xuống 1, đoạn \\(x<-1\\)) và nhánh bên phải (đi từ 1 lên \\(+\\infty\\), đoạn \\(x>1\\)).\n\nMỗi nhánh này là một đường liên tục, đơn điệu trải dài từ một giá trị nhỏ hơn 5,5 đến \\(+\\infty\\) (hoặc ngược lại), nên mỗi nhánh cắt đường thẳng \\(y=5{,}5\\) đúng 1 lần. Hai nhánh ở giữa (từ 1 lên 2, và từ 2 xuống 1) không vượt quá giá trị 2, nên không cắt đường thẳng \\(y=5{,}5\\).\n\nVậy tổng cộng có 2 giao điểm, tức phương trình có 2 nghiệm phân biệt. Chọn đáp án A.",
    },
          {
  "content": "Cho hình chóp S.ABC có diện tích đáy bằng 9. Mặt phẳng \\( (P) \\) song song với \\( (ABC) \\) cắt đoạn SA tại \\( M \\) sao cho \\( SM = 2MA \\). Diện tích thiết diện của hình chóp S.ABC tạo bởi \\( (P) \\) bằng",
  "options": {"A": "1", "B": "16/9", "C": "4/81", "D": "4"},
  "correct": "D",
  "explanation": "Gọi N, P lần lượt là giao điểm của mặt phẳng \\( (P) \\) và các cạnh SB, SC.\n\nVì \\( (P) // (ABC) \\) nên theo định lí Talet, ta có:\n\\( \\dfrac{SM}{SA} = \\dfrac{SN}{SB} = \\dfrac{SP}{SC} = \\dfrac{2}{3} \\).\n\nKhi đó \\( (P) \\) cắt hình chóp S.ABC theo thiết diện là tam giác MNP đồng dạng với tam giác ABC theo tỉ số \\( k = \\dfrac{2}{3} \\).\n\nVậy \\( S_{\\triangle MNP} = k^2 . S_{\\triangle ABC} = \\left(\\dfrac{2}{3}\\right)^2 . 9 = 4 \\).\n\nĐáp án D.",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau24.PNG"
},
{
  "content": "Nguyên hàm của hàm số \\( f(x) = 2^x + x \\) là",
  "options": {
    "A": "\\( 2^x + x^2 + C \\)",
    "B": "\\( \\dfrac{2^x}{\\ln 2} + x^2 + C \\)",
    "C": "\\( 2^x + \\dfrac{x^2}{2} + C \\)",
    "D": "\\( \\dfrac{2^x}{\\ln 2} + \\dfrac{x^2}{2} + C \\)"
  },
  "correct": "D",
  "explanation": "Sử dụng các công thức nguyên hàm cơ bản:\n\\( \\int a^x dx = \\dfrac{a^x}{\\ln a} + C \\); \\( \\int x^n dx = \\dfrac{x^{n+1}}{n+1} + C \\).\n\nTa có:\n\\( \\int f(x)dx = \\int (2^x + x)dx = \\dfrac{2^x}{\\ln 2} + \\dfrac{x^2}{2} + C \\).\n\nĐáp án D."
},
{
  "content": "Tìm \\( m \\) để góc giữa hai vectơ \\( \\vec{u} = (1;\\log_3 5;\\log_m 2) \\), \\( \\vec{v} = (3;\\log_5 3;4) \\) là góc nhọn.",
  "options": {
    "A": "\\( m > \\dfrac{1}{2}, m \\ne 1 \\)",
    "B": "\\( m > 1 \\)",
    "C": "\\( 0 < m < \\dfrac{1}{2} \\)",
    "D": "\\( m > 1 \\) hoặc \\( 0 < m < \\dfrac{1}{2} \\)"
  },
  "correct": "D",
  "explanation": "Để \\( (\\vec{u},\\vec{v}) < 90^\\circ \\Rightarrow \\cos(\\vec{u},\\vec{v}) > 0 \\).\n\n\\( \\Rightarrow \\vec{u}.\\vec{v} > 0 \\)\n\\( \\Leftrightarrow 3 + \\log_3 5.\\log_5 3 + 4\\log_m 2 > 0 \\)\n\n\\( \\Leftrightarrow 4 + 4\\log_m 2 > 0 \\)\n\\( \\Leftrightarrow \\log_m 2 > -1 \\)\n\n\\( \\Leftrightarrow \\left[\\begin{array}{l} m > 1 \\\\ m < \\dfrac{1}{2} \\end{array}\\right. \\)\n\nKết hợp điều kiện \\( m > 0 \\Rightarrow \\left[\\begin{array}{l} m > 1 \\\\ 0 < m < \\dfrac{1}{2} \\end{array}\\right. \\)\n\nĐáp án D."
},
          {
  "content": "Cho tứ diện ABCD có độ dài các cạnh \\( AB = AC = AD = BC = BD = a \\) và \\( CD = a\\sqrt{2} \\). Tính góc giữa hai đường thẳng AD và BC.",
  "options": {"A": "90°", "B": "45°", "C": "30°", "D": "60°"},
  "correct": "D",
  "explanation": "Gọi I, K, H lần lượt là trung điểm các cạnh DC, DB, AB.\n\nKhi đó: \\( KH // AD, KI // BC \\Rightarrow (AD,BC) = (KH,KI) \\).\n\nXét \\( \\triangle BIC \\), \\( BI = \\sqrt{BC^2 - AC^2} = \\sqrt{a^2 - \\dfrac{a^2}{2}} = \\dfrac{a}{\\sqrt{2}} \\).\n\nTa có \\( \\begin{cases} AB \\perp DH \\\\ AB \\perp HC \\end{cases} \\Rightarrow AB \\perp (DHC) \\Rightarrow AB \\perp HI \\).\n\nXét \\( \\triangle BIH \\), \\( HI = \\sqrt{IB^2 - HB^2} = \\sqrt{\\dfrac{a^2}{2} - \\dfrac{a^2}{4}} = \\dfrac{a}{2} \\). (1)\n\nXét \\( \\triangle IHK \\), ta có:\n\\( IK = \\dfrac{BC}{2} = \\dfrac{a}{2} \\), \\( HK = \\dfrac{AD}{2} = \\dfrac{a}{2} \\)\n\n\\( \\Rightarrow IK = HK = \\dfrac{a}{2} \\). (2)\n\nTừ (1), (2) \\( \\Rightarrow HI = IK = HK \\Rightarrow \\triangle IHK \\) là tam giác đều\n\n\\( \\Rightarrow \\widehat{IKH} = 60^\\circ \\Rightarrow (KH,KI) = 60^\\circ \\).\n\nĐáp án D.",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau41.PNG"
},
{
  "content": "Cho hàm số \\( y = f(x) \\) là một hàm đa thức có bảng xét dấu \\( f'(x) \\) như sau:",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau44_de.PNG",
  "options": {"A": "5", "B": "3", "C": "1", "D": "7"},
  "correct": "A",
  "content_2": "Số điểm cực trị của hàm số \\( g(x) = f(-2x^2 + |x|) \\) là",
  "explanation": "Ta có \\( g(x) = f(-2x^2 + |x|) = f(-2|x|^2 + |x|) \\).\n\nSố điểm cực trị của hàm số \\( h(|x|) \\) bằng hai lần số điểm cực trị dương của hàm số \\( h(x) \\) cộng thêm 1.\n\nXét hàm số:\n\\( h(x) = f(-2x^2 + x) \\)\n\n\\( \\Rightarrow h'(x) = (-4x+1)f'(-2x^2+x) = 0 \\)\n\n\\( \\Leftrightarrow \\left[\\begin{array}{l} x = \\dfrac{1}{4} \\\\ -2x^2+x = -1 \\\\ -2x^2+x = 1 \\end{array}\\right. \\Leftrightarrow \\left[\\begin{array}{l} x = \\dfrac{1}{4} \\\\ x = 1 \\\\ x = \\dfrac{-1}{2} \\end{array}\\right. \\)\n\nBảng xét dấu hàm số \\( h(x) = f(-2x^2+x) \\):",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau44_loigiai.PNG",
  "explanation_2": "Hàm số \\( h(x) = f(-2x^2+x) \\) có 2 điểm cực trị dương.\n\nVậy hàm số \\( g(x) = f(-2x^2+|x|) = f(-2|x|^2+|x|) \\) có 5 điểm cực trị.\n\nĐáp án A."
},
{
  "content": "Một ô tô đang chạy với vận tốc 10 m/s thì người lái xe đạp phanh. Từ thời điểm đó, ô tô chuyển động chậm dần đều với vận tốc \\( v(t) = -2t + 10 \\; (m/s) \\), trong đó \\( t \\) là khoảng thời gian tính bằng giây, kể từ lúc bắt đầu đạp phanh. Tính quãng đường ô tô di chuyển được trong 8 giây cuối cùng.",
  "options": {"A": "55 m", "B": "50 m", "C": "25 m", "D": "16 m"},
  "correct": "A",
  "explanation": "Ta sử dụng quãng đường đi được trong khoảng thời gian từ \\( t_1 \\) đến \\( t_2 \\) là \\( S = \\displaystyle\\int_{t_1}^{t_2} v(t)dt \\).\n\nVới \\( v(t) \\) là hàm vận tốc.\n\nChú ý rằng khi xe dừng hẳn thì vận tốc bằng 0.\n\nNên thời gian kể từ lúc đạp phanh đến lúc ô tô dừng hẳn là:\n\\( -2t + 10 = 0 \\Leftrightarrow t = 5 \\) (s)\n\nQuãng đường ô tô đi được từ lúc đạp phanh đến lúc ô tô dừng hẳn là:\n\\( S_2 = \\displaystyle\\int_0^5 (-2t+10)dt = \\left(-t^2+10t\\right)\\Big|_0^5 = 25 \\; m \\)\n\nNhư vậy trong 8 giây cuối thì có 3 giây ô tô đi với vận tốc 10 m/s và 5 giây ô tô chuyển động chậm dần đều.\n\nQuãng đường ô tô đi được trong 3 giây trước khi đạp phanh là:\n\\( S_1 = 3.10 = 30 \\; m \\)\n\nVậy trong 8 giây cuối ô tô đi được quãng đường:\n\\( S = S_1 + S_2 = 30 + 25 = 55 \\; m \\)\n\nĐáp án A."
},
            {
                # CÂU VÍ DỤ minh họa cách chèn ẢNH và văn bản SAU ẢNH.
                # Hãy thay link "image" bằng ảnh thật của bạn (upload lên
                # GitHub/Imgur... rồi dán link raw vào đây) và sửa lại nội
                # dung/đáp án cho đúng với hình vẽ thật.
                "content": "Cho đồ thị hàm số \\( y = f(x) \\) như hình vẽ bên.",
                "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de1_cau4.PNG",
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
        "content": "Cho 51 đồng xu, trong đó có 1 đồng xu nặng hơn về khối lượng, các đồng còn lại có khối lượng bằng nhau. Có 1 cái cân 2 đĩa. Hỏi cần ít nhất bao nhiêu lần cân để chắc chắn xác định được đồng xu khác loại đó?",
        "answers": ["4"],
        "explanation": "Với bài toán cân để tìm 1 đồng xu khác biệt (nặng hơn) trong N đồng xu bằng cân 2 đĩa, mỗi lần cân cho ta 3 khả năng xảy ra (lệch trái, lệch phải, hoặc thăng bằng).\n\nDo đó với k lần cân, ta phân biệt được tối đa \\(3^k\\) trường hợp, nên điều kiện cần là \\(3^k \\ge N\\).\n\nVới \\(N = 51\\): ta thử \\(3^3 = 27 < 51\\) (chưa đủ), còn \\(3^4 = 81 \\ge 51\\) (đủ). Vậy \\(k = 4\\).\n\nCó thể hình dung cách cân cụ thể như sau:\n- Lần 1: Chia 51 xu thành 3 nhóm 17 - 17 - 17, cân 2 nhóm bất kỳ. Nếu cân bằng thì xu lạ nằm trong nhóm còn lại; nếu lệch thì nó nằm ở đĩa nặng hơn. Dù thế nào ta cũng khoanh vùng còn 17 xu.\n- Lần 2: Chia 17 xu thành 6 - 6 - 5, cân 2 nhóm 6. Trường hợp xấu nhất còn lại 6 xu nghi vấn.\n- Lần 3: Chia 6 xu thành 2 - 2 - 2, cân 2 nhóm 2. Còn lại 2 xu nghi vấn.\n- Lần 4: Cân 2 xu cuối cùng, bên nào nặng hơn chính là đồng xu cần tìm.\n\nVậy cần ít nhất 4 lần cân.",
    },
    {
        "content": "Cho các số lẻ từ 5 đến 21 xếp vào ô vuông \\(3 \\times 3\\) như hình vẽ. Biết tổng các đường ngang, đường dọc và đường chéo đều bằng nhau. Hãy tìm giá trị của x.",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/logic_cau2.png",
        "answers": ["11"],
        "explanation": "Trước tiên tìm hằng số ma thuật (tổng mỗi hàng/cột/đường chéo).\n\nDãy số lẻ từ 5 đến 21 gồm 9 số: 5, 7, 9, 11, 13, 15, 17, 19, 21, có tổng là \\(S = \\dfrac{9(5+21)}{2} = 117\\).\n\nVì bảng có 3 hàng, mỗi hàng có cùng một tổng và cộng lại đúng bằng tổng cả 9 số, nên hằng số ma thuật là \\(M = \\dfrac{117}{3} = 39\\).\n\nTrong ô vuông ma phương \\(3\\times 3\\) chuẩn, ô chính giữa luôn bằng \\(M/3\\), tức là ô trung tâm \\(= \\dfrac{39}{3} = 13\\).\n\nBây giờ ta điền dần các ô còn thiếu, dựa vào tổng mỗi hàng/cột/chéo đều bằng 39:\n- Hàng giữa có 9, tâm 13, và 17: kiểm tra \\(9+13+17=39\\) (đúng).\n- Cột giữa có 5 ở trên, tâm 13, nên ô dưới cùng cột giữa là \\(39-5-13=21\\).\n- Đường chéo phụ (từ x ở góc dưới trái, qua tâm 13, đến góc trên phải): góc trên phải \\(=39-13-x=26-x\\).\n- Hàng trên cùng có góc trên trái, số 5, và góc trên phải \\((26-x)\\): góc trên trái \\(=39-5-(26-x)=8+x\\).\n- Cột đầu tiên có góc trên trái \\((8+x)\\), số 9, và x ở dưới cùng, tổng bằng 39:\n\\[(8+x)+9+x=39 \\Leftrightarrow 2x+17=39 \\Leftrightarrow x=11\\]\n\nThử lại: điền đủ bảng ta được hàng dưới cùng là 11, 21, 7 và đường chéo chính \\(19+13+7=39\\) — hoàn toàn khớp.\n\nVậy \\(x = 11\\).",
    },
    {
        "content": "Hãy sắp xếp 5 chữ cái A, B, C, D, E vào bảng \\(5 \\times 5\\) sao cho mỗi hàng và mỗi cột đều đủ cả 5 chữ cái (không chữ nào lặp lại trên cùng hàng hoặc cột). Hãy tìm chữ cái ở ô có dấu ★ trong hình.",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/logic_cau3.png",
        "answers": ["A"],
        "explanation": "Yêu cầu bài toán — mỗi hàng, mỗi cột không được lặp chữ cái — chính là dạng bài toán về Hình vuông Latinh (Latin Square), giống hệt cách suy luận khi giải Sudoku.\n\nQuan sát các cột đã biết vài chữ cái:\n- Cột cuối cùng (cột 5) đã có E (hàng 1) và B (hàng 2), nên 3 ô còn lại của cột này (hàng 3, 4, 5) chỉ có thể là A, C, D theo một thứ tự nào đó.\n- Cột đầu tiên (cột 1) đã có A (hàng 1) và C (hàng 5), nên 3 ô còn lại (hàng 2, 3, 4) chỉ có thể là B, D, E.\n\nDựa vào các ràng buộc này và tiếp tục loại trừ tương tự cho từng hàng, từng cột, ta dò ra được duy nhất một cách điền thỏa mãn toàn bộ điều kiện đề bài:\n\nA C B D E\nD E A C B\nE B D A C\nB A C E D\nC D E B A\n\nSo với bảng trên, ô có dấu ★ (hàng 4, cột 2) chính là chữ A.\n\nVậy chữ cái cần tìm là A.",
    },
    {
        "content": "Cho dãy số: 1, 3, 3, 3, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, ... (số 1 xuất hiện 1 lần, số 3 xuất hiện 3 lần, số 5 xuất hiện 5 lần, số 7 xuất hiện 7 lần, cứ thế tiếp tục với các số lẻ). Hỏi số hạng thứ 2025 của dãy là số nào?",
        "answers": ["89"],
        "explanation": "Ta chia dãy số thành từng nhóm, mỗi nhóm gồm các số hạng bằng nhau:\n- Nhóm 1: số 1, xuất hiện 1 lần.\n- Nhóm 2: số 3, xuất hiện 3 lần.\n- Nhóm 3: số 5, xuất hiện 5 lần.\n- ...\n- Nhóm thứ n: số \\((2n-1)\\), xuất hiện \\((2n-1)\\) lần.\n\nTổng số phần tử tính đến hết nhóm thứ n là:\n\\[S_n = 1+3+5+\\cdots+(2n-1)=n^2\\]\n\nTa cần tìm xem vị trí 2025 rơi vào nhóm thứ mấy, tức tìm n sao cho \\((n-1)^2 < 2025 \\le n^2\\).\n\nVì \\(45^2 = 2025\\), nên \\(S_{45}=2025\\) — nghĩa là số hạng thứ 2025 chính là phần tử cuối cùng của nhóm thứ 45.\n\nGiá trị của các phần tử trong nhóm thứ 45 chính là số lẻ thứ 45:\n\\[2\\times 45 - 1 = 89\\]\n\nVậy số hạng thứ 2025 của dãy là 89.",
    },      
    {
        "content": "Tích tất cả các giá trị của \\(a\\) để góc tạo bởi đường thẳng \\(\\begin{cases}x=4+at\\\\y=7-2t\\end{cases}\\ (t\\in\\mathbb{R})\\) và đường thẳng \\(3x+4y-2=0\\) bằng \\(45^\\circ\\) là bao nhiêu?",
        "answers": ["-4"],
        "explanation": "Gọi \\(\\varphi\\) là góc giữa hai đường thẳng đã cho.\n\nĐường thẳng thứ nhất có vectơ chỉ phương \\(\\vec{u}=(a;-2)\\) (lấy từ hệ số của t).\n\nĐường thẳng thứ hai \\(3x+4y-2=0\\) có vectơ chỉ phương \\(\\vec{v}=(4;-3)\\) (đổi vai trò hệ số a, b của phương trình tổng quát, đảo dấu một hệ số).\n\nGóc giữa hai đường thẳng được tính qua công thức:\n\\[\\cos\\varphi=|\\cos(\\vec{u},\\vec{v})|=\\dfrac{|\\vec{u}.\\vec{v}|}{|\\vec{u}|.|\\vec{v}|}\\]\n\nThay số:\n\\[\\cos 45^\\circ=\\dfrac{|4a+6|}{\\sqrt{a^2+4}.\\sqrt{16+9}} \\Leftrightarrow \\dfrac{1}{\\sqrt2}=\\dfrac{|4a+6|}{5\\sqrt{a^2+4}}\\]\n\nNhân chéo rồi bình phương hai vế để khử căn và dấu giá trị tuyệt đối:\n\\[5\\sqrt{a^2+4}=\\sqrt2\\,|4a+6| \\Rightarrow 25(a^2+4)=2(4a+6)^2\\]\n\\[\\Leftrightarrow 25a^2+100=32a^2+96a+72\\]\n\\[\\Leftrightarrow 7a^2+96a-28=0\\]\n\nGiải phương trình bậc hai này ta được hai nghiệm:\n\\[a=\\dfrac{2}{7} \\quad \\text{hoặc} \\quad a=-14\\]\n\nĐề bài yêu cầu tích tất cả các giá trị của a thỏa mãn, nên:\n\\[\\dfrac{2}{7}\\times(-14)=-4\\]\n\nVậy tích các giá trị của a là \\(-4\\).",
    },
    {
        "content": "Một viên đạn được bắn lên với tốc độ ban đầu \\(v_0=196\\) m/s từ mặt đất theo phương thẳng đứng. Phương trình chuyển động của viên đạn là \\(y=v_0t-4{,}9t^2\\) (m), trong đó \\(t\\) là thời gian tính bằng giây kể từ lúc bắn, trục Oy hướng lên và gốc O là vị trí bắn. Bỏ qua sức cản không khí. Hỏi tại thời điểm tốc độ của viên đạn bằng 0, viên đạn cách mặt đất bao nhiêu mét?",
        "answers": ["1960"],
        "explanation": "Vận tốc chính là đạo hàm của quãng đường theo thời gian, tức \\(v(t) = y'(t)\\).\n\nLấy đạo hàm phương trình chuyển động:\n\\[v(t)=y'(t)=v_0-9{,}8t=196-9{,}8t\\]\n\nTốc độ của viên đạn bằng 0 khi:\n\\[196-9{,}8t=0 \\Leftrightarrow t=20 \\text{ (giây)}\\]\n\nĐây chính là thời điểm viên đạn ở vị trí cao nhất (vì trước đó nó đang bay lên, tốc độ giảm dần đến 0 rồi bắt đầu rơi xuống).\n\nThay \\(t=20\\) vào phương trình chuyển động để tìm độ cao lúc đó:\n\\[y(20)=196\\times 20-4{,}9\\times 20^2=3920-1960=1960 \\text{ (m)}\\]\n\nVậy tại thời điểm tốc độ bằng 0, viên đạn cách mặt đất 1960 mét.",
    },
    {
        "content": "Trong không gian với hệ tọa độ Oxyz, cho \\(\\vec{i}, \\vec{j}, \\vec{k}\\) lần lượt là các vectơ đơn vị nằm trên các trục tọa độ Ox, Oy, Oz và \\(\\vec{u}\\) là một vectơ tùy ý khác \\(\\vec{0}\\). Tính \\(T=\\cos^2(\\vec{u},\\vec{i})+\\cos^2(\\vec{u},\\vec{j})+\\cos^2(\\vec{u},\\vec{k})\\).",
        "answers": ["1"],
        "explanation": "Giả sử \\(\\vec{u}=(x;y;z)\\). Ta có \\(\\vec{i}=(1;0;0)\\), \\(\\vec{j}=(0;1;0)\\), \\(\\vec{k}=(0;0;1)\\).\n\nÁp dụng công thức tính góc giữa hai vectơ, ta được:\n\\[\\cos(\\vec{u},\\vec{i})=\\dfrac{x}{\\sqrt{x^2+y^2+z^2}},\\quad \\cos(\\vec{u},\\vec{j})=\\dfrac{y}{\\sqrt{x^2+y^2+z^2}},\\quad \\cos(\\vec{u},\\vec{k})=\\dfrac{z}{\\sqrt{x^2+y^2+z^2}}\\]\n\nBình phương từng cái rồi cộng lại:\n\\[T=\\left(\\dfrac{x}{\\sqrt{x^2+y^2+z^2}}\\right)^2+\\left(\\dfrac{y}{\\sqrt{x^2+y^2+z^2}}\\right)^2+\\left(\\dfrac{z}{\\sqrt{x^2+y^2+z^2}}\\right)^2\\]\n\\[=\\dfrac{x^2+y^2+z^2}{x^2+y^2+z^2}=1\\]\n\nVậy \\(T=1\\) với mọi vectơ \\(\\vec{u}\\) khác \\(\\vec{0}\\) — kết quả này không phụ thuộc vào tọa độ cụ thể của \\(\\vec{u}\\).",
    },
    {
        "content": "Có bao nhiêu giá trị nguyên của tham số \\(m\\in[-25;25]\\) để hàm số \\(y=x^3-3x^2+mx+2\\) có cực đại và cực tiểu?",
        "answers": ["28"],
        "explanation": "Hàm số bậc ba \\(y=ax^3+bx^2+cx+d\\) (với \\(a\\ne 0\\)) có cả cực đại và cực tiểu khi và chỉ khi phương trình \\(y'=0\\) có hai nghiệm phân biệt.\n\nTa có:\n\\[y'=3x^2-6x+m\\]\n\nXét phương trình \\(y'=0 \\Leftrightarrow 3x^2-6x+m=0\\;(*)\\).\n\nĐể hàm số có cực đại và cực tiểu thì (*) phải có hai nghiệm phân biệt, tức là:\n\\[\\Delta' > 0 \\Leftrightarrow 9-3m>0 \\Leftrightarrow m<3\\]\n\nKết hợp với điều kiện \\(m\\) nguyên và \\(m\\in[-25;25]\\), ta có:\n\\[m\\in\\{-25;-24;\\ldots;2\\}\\]\n\nĐếm số phần tử: từ \\(-25\\) đến \\(2\\) có \\(2-(-25)+1=28\\) giá trị.\n\nVậy có 28 giá trị nguyên của \\(m\\) thỏa mãn yêu cầu bài toán.",
    },
    {
        "content": "Một kiến trúc sư thiết kế một hội trường với 15 ghế ngồi ở hàng thứ nhất, 18 ghế ngồi ở hàng thứ hai, 21 ghế ngồi ở hàng thứ ba, và cứ như vậy (số ghế ở hàng sau nhiều hơn 3 ghế so với hàng liền trước). Nếu muốn hội trường có sức chứa ít nhất 870 ghế ngồi thì kiến trúc sư phải thiết kế tối thiểu bao nhiêu hàng ghế?",
        "answers": ["20"],
        "explanation": "Số ghế ở các hàng tạo thành một cấp số cộng với số hạng đầu \\(u_1=15\\) và công sai \\(d=3\\).\n\nGọi \\(n\\) là số hàng ghế của hội trường (\\(n\\in\\mathbb{N}^*\\)). Tổng số ghế trong hội trường là tổng \\(n\\) số hạng đầu của cấp số cộng:\n\\[S_n=\\dfrac{[2u_1+(n-1)d]\\cdot n}{2}=\\dfrac{[2\\cdot15+(n-1)\\cdot3]\\,n}{2}=\\dfrac{3n^2+27n}{2}\\]\n\nĐể hội trường có sức chứa ít nhất 870 ghế thì \\(S_n\\ge 870\\):\n\\[\\dfrac{3n^2+27n}{2}\\ge 870 \\Leftrightarrow n^2+9n-580\\ge 0\\]\n\nGiải bất phương trình bậc hai này, ta được:\n\\[n\\ge 20 \\quad \\text{hoặc} \\quad n\\le -29\\]\n\nVì \\(n\\) là số hàng ghế nên phải dương, do đó \\(n\\ge 20\\).\n\nVậy kiến trúc sư phải thiết kế tối thiểu 20 hàng ghế.",
    },
    {
        "content": "Cho phương trình \\(\\log_{\\frac{1}{2}}(2x-m)+\\log_2(3-x)=0\\), với \\(m\\) là tham số. Hỏi có bao nhiêu giá trị nguyên dương của \\(m\\) để phương trình có nghiệm?",
        "answers": ["5"],
        "explanation": "Trước tiên tìm điều kiện xác định:\n\\[\\begin{cases}2x-m>0\\\\3-x>0\\end{cases}\\Leftrightarrow \\begin{cases}2x-m>0\\\\x<3\\end{cases}\\]\n\nBiến đổi phương trình về cùng cơ số 2. Vì \\(\\log_{\\frac{1}{2}}t=-\\log_2 t\\), ta có:\n\\[\\log_{\\frac{1}{2}}(2x-m)+\\log_2(3-x)=0\\]\n\\[\\Leftrightarrow -\\log_2(2x-m)+\\log_2(3-x)=0\\]\n\\[\\Leftrightarrow \\log_2(2x-m)=\\log_2(3-x)\\]\n\nGiải phương trình logarit (hai vế cùng cơ số nên biểu thức trong log bằng nhau):\n\\[2x-m=3-x \\Leftrightarrow 3x=m+3\\]\n\nĐể phương trình có nghiệm \\(x\\) thỏa mãn điều kiện \\(x<3\\), ta cần:\n\\[\\dfrac{m+3}{3}<3 \\Leftrightarrow m+3<9 \\Leftrightarrow m<6\\]\n\n(Về mặt điều kiện \\(2x-m>0\\), khi thay \\(x=\\frac{m+3}{3}\\) vào ta được \\(2x-m=3-x>0\\) luôn đúng do \\(x<3\\), nên không cần xét thêm.)\n\nKết hợp với điều kiện \\(m\\) là số nguyên dương, ta có:\n\\[m\\in\\{1;2;3;4;5\\}\\]\n\nVậy có 5 giá trị nguyên dương của \\(m\\) thỏa mãn yêu cầu bài toán.",
    },
    {
        "content": "Cho hai mặt phẳng \\((P):2x-y+2z-3=0\\) và \\((Q):x+my+z-1=0\\). Tìm tham số \\(m\\) để hai mặt phẳng \\((P)\\) và \\((Q)\\) vuông góc với nhau.",
        "answers": ["4"],
        "explanation": "Xác định vectơ pháp tuyến của từng mặt phẳng, dựa vào hệ số của \\(x, y, z\\) trong phương trình:\n\\[\\vec{n_P}=(2;-1;2), \\qquad \\vec{n_Q}=(1;m;1)\\]\n\nHai mặt phẳng vuông góc với nhau khi và chỉ khi hai vectơ pháp tuyến của chúng vuông góc, tức là tích vô hướng của chúng bằng 0:\n\\[\\vec{n_P}\\cdot\\vec{n_Q}=0\\]\n\\[\\Leftrightarrow 2\\cdot1+(-1)\\cdot m+2\\cdot1=0\\]\n\\[\\Leftrightarrow 2-m+2=0 \\Leftrightarrow m=4\\]\n\nVậy \\(m=4\\) thì hai mặt phẳng \\((P)\\) và \\((Q)\\) vuông góc với nhau.",
    },
        {
        "content": "Một chiếc cổng parabol dạng \\(y=-\\dfrac{1}{2}x^2\\) có chiều rộng \\(d=8\\)m. Hỏi chiều cao của chiếc cổng là bao nhiêu mét?",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/hsa2_cau2_parabol.png",
        "answers": ["8"],
        "explanation": "Đỉnh của parabol nằm tại gốc tọa độ O (đây là điểm cao nhất của cổng), và cổng đối xứng qua trục Oy.\n\nVì chiều rộng của cổng là 8m và cổng đối xứng qua trục tung, nên khoảng cách từ chân cổng đến trục đối xứng Oy là:\n\\[\\dfrac{8}{2}=4\\]\n\nSuy ra hoành độ của hai chân cổng lần lượt là \\(x=-4\\) và \\(x=4\\).\n\nThay \\(x=4\\) vào phương trình parabol để tìm tung độ chân cổng:\n\\[y=-\\dfrac{1}{2}\\cdot4^2=-\\dfrac{1}{2}\\times16=-8\\]\n\nChiều cao của cổng chính là khoảng cách theo phương thẳng đứng từ đỉnh cổng (tại O) xuống đến chân cổng, tức là trị tuyệt đối của tung độ chân cổng:\n\\[h=|-8|=8 \\text{ (mét)}\\]\n\nVậy chiều cao của chiếc cổng là 8 mét.",
    },
    {
        "content": "Cho cấp số nhân \\((u_n)\\) thỏa mãn \\(2(u_3+u_4+u_5)=u_6+u_7+u_8\\). Tính \\(\\dfrac{u_8+u_9+u_{10}}{u_2+u_3+u_4}\\).",
        "answers": ["4"],
        "explanation": "Gọi \\(q\\) là công bội của cấp số nhân. Theo đề bài:\n\\[2(u_3+u_4+u_5)=u_6+u_7+u_8\\]\n\nBiểu diễn các số hạng theo \\(u_3\\) và công bội \\(q\\) (chú ý \\(u_6=u_3q^3\\), \\(u_7=u_3q^4\\), \\(u_8=u_3q^5\\)... nhưng để đơn giản ta biểu diễn cả hai vế qua cùng một mốc — cách làm gốc dùng \\(u_4=u_3q,\\,u_5=u_3q^2\\) và \\(u_6=u_6,\\,u_7=u_6q,\\,u_8=u_6q^2\\)):\n\\[2\\left(u_3+u_3q+u_3q^2\\right)=u_6+u_6q+u_6q^2\\]\n\\[\\Leftrightarrow 2u_3\\left(1+q+q^2\\right)=u_6\\left(1+q+q^2\\right)\\]\n\nVì \\(1+q+q^2>0\\) với mọi \\(q\\) (biểu thức này luôn dương do có thể viết thành \\(\\left(q+\\frac12\\right)^2+\\frac34>0\\)), ta được:\n\\[2u_3=u_6\\]\n\nMặt khác \\(u_6=u_3q^3\\) (vì cách nhau 3 số hạng trong cấp số nhân), nên:\n\\[2u_3=u_3q^3 \\Leftrightarrow u_3(2-q^3)=0\\]\n\nDo \\(u_3\\ne 0\\) (nếu \\(u_3=0\\) thì cả dãy đều bằng 0, không tạo thành cấp số nhân hợp lệ), ta suy ra:\n\\[q^3=2 \\Leftrightarrow q=\\sqrt[3]{2}\\]\n\nBây giờ tính tỉ số cần tìm. Biểu diễn tử số và mẫu số theo \\(u_2\\) và công bội \\(q\\):\n\\[\\dfrac{u_8+u_9+u_{10}}{u_2+u_3+u_4}=\\dfrac{u_8+u_8q+u_8q^2}{u_2+u_2q+u_2q^2}=\\dfrac{u_8\\left(1+q+q^2\\right)}{u_2\\left(1+q+q^2\\right)}=\\dfrac{u_8}{u_2}\\]\n\nVì \\(u_8=u_2\\cdot q^6\\) (cách nhau 6 số hạng), nên:\n\\[\\dfrac{u_8}{u_2}=q^6=\\left(\\sqrt[3]{2}\\right)^6=2^2=4\\]\n\nVậy giá trị cần tính là 4.",
    },
    {
        "content": "Cho các số nguyên \\(a, b, c\\) thỏa mãn \\(a+\\dfrac{b+\\log_2 5}{c+\\log_2 3}=\\log_6 45\\). Tổng \\(a+b+c\\) bằng bao nhiêu?",
        "answers": ["1"],
        "explanation": "Trước tiên, đổi \\(\\log_6 45\\) về cơ số 2 bằng công thức đổi cơ số \\(\\log_a b=\\dfrac{\\log_c b}{\\log_c a}\\):\n\\[a+\\dfrac{b+\\log_2 5}{c+\\log_2 3}=\\log_6 45=\\dfrac{\\log_2 45}{\\log_2 6}\\]\n\nPhân tích \\(45=3^2\\cdot5\\) và \\(6=2\\cdot3\\), sử dụng công thức \\(\\log_a(xy)=\\log_a x+\\log_a y\\):\n\\[\\dfrac{\\log_2 45}{\\log_2 6}=\\dfrac{\\log_2(3^2\\cdot5)}{\\log_2(2\\cdot3)}=\\dfrac{2\\log_2 3+\\log_2 5}{1+\\log_2 3}\\]\n\nVậy phương trình trở thành:\n\\[a+\\dfrac{b+\\log_2 5}{c+\\log_2 3}=\\dfrac{2\\log_2 3+\\log_2 5}{1+\\log_2 3}\\]\n\nBiến đổi vế phải để xuất hiện phần nguyên cộng phần dư (tách sao cho phần không chứa \\(\\log_2 5\\) tách riêng):\n\\[\\dfrac{2\\log_2 3+\\log_2 5}{1+\\log_2 3}=\\dfrac{2+2\\log_2 3-2+\\log_2 5}{1+\\log_2 3}=2+\\dfrac{-2+\\log_2 5}{1+\\log_2 3}\\]\n\n(Ở đây ta cộng trừ 2 vào tử số để tách ra phần nguyên khớp với mẫu số \\(1+\\log_2 3\\), vì \\(2\\times(1+\\log_2 3)=2+2\\log_2 3\\).)\n\nVậy:\n\\[a+\\dfrac{b+\\log_2 5}{c+\\log_2 3}=2+\\dfrac{-2+\\log_2 5}{1+\\log_2 3}\\]\n\nĐồng nhất hệ số hai vế (vì \\(a,b,c\\) là các số nguyên và \\(\\log_2 3,\\log_2 5\\) là các số vô tỉ độc lập tuyến tính với số hữu tỉ), ta có:\n\\[a=2,\\quad b=-2,\\quad c=1\\]\n\nVậy tổng \\(a+b+c=2+(-2)+1=1\\).",
    },
          {
        "content": "Cho hình chóp S.ABC có đáy ABC là tam giác vuông tại A, các cạnh \\(AB=AC=a\\), các góc \\(\\widehat{SBA}=\\widehat{SCA}=90^\\circ\\). Gọi H là hình chiếu vuông góc của S trên (ABC) và \\(SH=a\\sqrt{2}\\). Tính cosin góc giữa hai mặt phẳng (SAB) và (SAC).",
        "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/hsa2_cau13_hinhchop.PNG",
        "answers": ["1/3"],
        "explanation": "Trước tiên ta xác định vị trí điểm H bằng một phép dựng phụ.\n\nGọi \\((\\alpha)\\) là mặt phẳng đi qua B và vuông góc với AB, khi đó \\((\\alpha)\\cap(ABC)\\) là đường thẳng qua B song song với AC.\n\nGọi \\((\\beta)\\) là mặt phẳng đi qua C và vuông góc với AC, khi đó \\((\\beta)\\cap(ABC)\\) là đường thẳng qua C song song với AB.\n\nVì \\(\\widehat{SBA}=90^\\circ\\) nghĩa là \\(SB\\perp AB\\), và tương tự \\(SC\\perp AC\\), nên SH — với H là hình chiếu của S — chính là giao tuyến của hai mặt phẳng \\((\\alpha)\\) và \\((\\beta)\\), và H chính là đỉnh thứ tư của hình vuông ABHC (vì tam giác ABC vuông cân tại A với AB=AC=a).\n\nKhi đó, hai tam giác SAB và SAC là hai tam giác vuông bằng nhau (vuông tại B và C tương ứng), với:\n\\[SB=SC=\\sqrt{SH^2+HB^2}\\]\n\nVì H là đỉnh hình vuông ABHC cạnh a, nên \\(HB=HC=a\\sqrt{2}\\) (đường chéo của hình vuông cạnh a). Do đó:\n\\[SB=SC=\\sqrt{(a\\sqrt2)^2+(a\\sqrt2)^2}=\\sqrt{2a^2+2a^2}=a\\sqrt{4}=a\\sqrt3\\]\n\n\\[SA=\\sqrt{SH^2+HA^2}\\]\n\nVì HA là đường chéo của hình vuông ABHC, nên \\(HA=a\\sqrt2\\), suy ra:\n\\[SA=\\sqrt{(a\\sqrt2)^2+(a\\sqrt2)^2}=\\sqrt{4a^2}=2a\\]\n\nGọi I là chân đường cao hạ từ đỉnh B của tam giác SAB, ta có \\(BI\\perp SA\\). Vì tam giác SAC bằng tam giác SAB (cạnh — cạnh — cạnh: SB=SC, SA chung, AB=AC), chân đường cao từ C trong tam giác SAC (gọi là CI) cũng rơi vào đúng điểm I trên SA.\n\nDo đó, góc giữa hai mặt phẳng (SAB) và (SAC) chính là góc giữa hai đường thẳng IB và IC (vì cả hai đều vuông góc với giao tuyến chung SA tại cùng một điểm I).\n\nXét tam giác SAB vuông tại B với đường cao BI, ta tính được:\n\\[IB=\\dfrac{SB\\cdot AB}{SA}=\\dfrac{a\\sqrt3\\cdot a}{2a}=\\dfrac{a\\sqrt3}{2}\\]\n\nTương tự, \\(IC=\\dfrac{a\\sqrt3}{2}\\) (do tam giác SAC bằng tam giác SAB).\n\nMặt khác, \\(BC=a\\sqrt2\\) (đường chéo hình vuông cạnh a, hoặc cạnh huyền của tam giác vuông cân ABC tại A).\n\nXét tam giác IBC cân tại I (vì IB=IC), áp dụng định lý hàm số cos để tính góc \\(\\widehat{BIC}\\):\n\\[\\cos\\widehat{BIC}=\\dfrac{IB^2+IC^2-BC^2}{2\\cdot IB\\cdot IC}=\\dfrac{\\dfrac{3a^2}{4}+\\dfrac{3a^2}{4}-2a^2}{2\\cdot\\dfrac{3a^2}{4}}=\\dfrac{-\\dfrac{a^2}{2}}{\\dfrac{3a^2}{2}}=-\\dfrac{1}{3}\\]\n\nVì góc giữa hai mặt phẳng luôn được quy ước là góc không tù (nằm trong khoảng từ \\(0^\\circ\\) đến \\(90^\\circ\\)), nên cosin của góc giữa hai mặt phẳng (SAB) và (SAC) chính là giá trị tuyệt đối của kết quả trên:\n\\[\\cos\\left((SAB),(SAC)\\right)=\\left|-\\dfrac{1}{3}\\right|=\\dfrac{1}{3}\\]\n\nVậy cosin góc giữa hai mặt phẳng (SAB) và (SAC) bằng \\(\\dfrac{1}{3}\\).",
    },
        ],
    },

    # ------------------------------------------------------------------
    # ĐỀ 2
    # ------------------------------------------------------------------
    {
        "id": "de2",
        "name": "Đề thi tham khảo số 2 - Đánh giá năng lực học sinh THPT 2026",
        "seed": 2025202,
        "mc4": [
            {
  "content": "Tập giá trị của hàm số \\( y = \\dfrac{\\sin 3x - 2\\cos 3x + 10}{6\\cos x \\cos 2x - 4\\cos^3 x + 3} \\) có bao nhiêu số nguyên?",
  "options": {"A": "12", "B": "10", "C": "11", "D": "13"},
  "correct": "C",
  "explanation": "Ta có:\n\n\\( y = \\dfrac{\\sin 3x - 2\\cos 3x + 10}{6\\cos x \\cos 2x - 4\\cos^3 x + 3} \\)\n\n\\( = \\dfrac{\\sin 3x - 2\\cos 3x + 10}{3(\\cos 3x + \\cos x) - (\\cos 3x + 3\\cos x) + 3} \\)\n\n\\( = \\dfrac{\\sin 3x - 2\\cos 3x + 10}{2\\cos 3x + 3} \\)\n\n\\( \\Leftrightarrow (2\\cos 3x + 3)y = \\sin 3x - 2\\cos 3x + 10 \\)\n\n\\( \\Leftrightarrow (2y+2)\\cos 3x - \\sin 3x = 10 - 3y \\)\n\nĐiều kiện có nghiệm của phương trình là:\n\n\\( (2y+2)^2 + (-1)^2 \\ge (10-3y)^2 \\)\n\n\\( \\Leftrightarrow 4y^2 + 8y + 4 + 1 \\ge 100 - 60y + 9y^2 \\)\n\n\\( \\Leftrightarrow 5y^2 - 68y + 95 \\le 0 \\)\n\n\\( \\Leftrightarrow \\dfrac{34-\\sqrt{681}}{5} \\le y \\le \\dfrac{34+\\sqrt{681}}{5} \\)\n\nMà \\( y \\in \\mathbb{Z} \\) nên \\( y = \\{2;3;4;\\ldots;12\\} \\).\n\nVậy tập giá trị của \\( y \\) có 11 số nguyên.\n\nĐáp án C."
},
{
  "content": "Biểu đồ dưới đây thể hiện tỉ lệ lạm phát cơ bản bình quân năm trong giai đoạn 2018 – 2022:",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau15_de.PNG",
  "content_2": "Trong giai đoạn từ 2018 – 2021, năm có tỉ lệ lạm phát cơ bản bình quân năm cao nhất là?",
  "options": {"A": "Năm 2022", "B": "Năm 2019", "C": "Năm 2021", "D": "Năm 2020"},
  "correct": "D",
  "explanation": "Nhìn vào biểu đồ để xác định.\n\nTrong giai đoạn từ 2018 – 2021, năm 2020 có tỉ lệ lạm phát cơ bản bình quân năm cao nhất.\n\nĐáp án D."
},
{
  "content": "Nhiệt độ ngoài trời ở một thành phố vào các thời điểm khác nhau trong ngày có thể được mô phỏng bởi công thức \\( h(t) = 29 + 3\\sin \\dfrac{\\pi}{12}(t-9) \\) với \\( h \\) tính bằng \\( ^\\circ C \\) và \\( t \\) là thời gian trong ngày tính bằng giờ.\n\nThời gian nhiệt độ cao nhất trong ngày là:",
  "options": {"A": "13 giờ", "B": "15 giờ", "C": "12 giờ", "D": "14 giờ"},
  "correct": "B",
  "explanation": "Sử dụng tập giá trị của hàm số sin để tìm nhiệt độ cao nhất trong ngày, sau đó giải điều kiện để tìm thời gian nhiệt độ cao nhất.\n\nDo \\( -1 \\le \\sin \\dfrac{\\pi}{12}(t-9) \\le 1, \\forall t \\) nên\n\n\\( -3 \\le 3\\sin \\dfrac{\\pi}{12}(t-9) \\le 3 \\)\n\n\\( \\Leftrightarrow 26 \\le 29 + 3\\sin \\dfrac{\\pi}{12}(t-9) \\le 32 \\)\n\n\\( \\Leftrightarrow 26 \\le h(t) \\le 32 \\)\n\nDo đó nhiệt độ cao nhất trong ngày là \\( 32^\\circ C \\).\n\nDấu bằng xảy ra\n\n\\( \\Leftrightarrow \\sin \\dfrac{\\pi}{12}(t-9) = 1 \\Leftrightarrow \\dfrac{\\pi}{12}(t-9) = \\dfrac{\\pi}{2} + k2\\pi \\Leftrightarrow t = 15 + 24k \\; (k \\in \\mathbb{Z}) \\)\n\nDo \\( 0 \\le t \\le 24 \\Leftrightarrow 0 \\le 15+24k \\le 24 \\Leftrightarrow -\\dfrac{15}{24} \\le k \\le \\dfrac{9}{24} \\). Mà \\( k \\in \\mathbb{Z} \\) nên \\( k = 0 \\).\n\nKhi đó \\( t = 15 \\).\n\nVậy lúc 15h là thời gian nhiệt độ cao nhất trong ngày.\n\nĐáp án B."
},
{
  "content": "Hai cậu bé cùng bắn bi vào lỗ. Xác suất người thứ nhất bắn trúng vào lỗ là 85%, xác suất người thứ hai bắn trúng vào lỗ là 70%. Hỏi xác suất để cả hai người cùng bắn trúng vào lỗ:",
  "options": {"A": "59,5%", "B": "15%", "C": "30%", "D": "4,5%"},
  "correct": "A",
  "explanation": "Sử dụng quy tắc nhân và cộng trong xác suất.\n\nXác suất người thứ nhất bắn trúng lỗ: 0,85\n\nXác suất người thứ hai bắn trúng bia: 0,7\n\nXác suất để cả hai người cùng bắn trúng bia:\n\n\\( 0,85 . 0,7 = 0,595 = 59,5\\% \\)\n\nĐáp án A."
},
{
  "content": "Cho lăng trụ đứng \\( ABC.A'B'C' \\) có đáy ABC là tam giác đều cạnh \\( a \\). Gọi \\( D \\) là trung điểm cạnh BC. Biết \\( AA' = 2a \\), khoảng cách giữa hai đường thẳng \\( A'B \\) và \\( C'D \\) là:",
  "options": {
    "A": "\\( a\\sqrt{17} \\)",
    "B": "\\( \\dfrac{a}{\\sqrt{17}} \\)",
    "C": "\\( 2a\\sqrt{17} \\)",
    "D": "\\( \\dfrac{2a}{\\sqrt{17}} \\)"
  },
  "correct": "D",
  "explanation": "Gọi \\( D' \\) là trung điểm của \\( B'C' \\). Kẻ \\( B'H \\perp BD' \\). Chứng minh \\( d(A'B; C'D) = B'H \\).\n\nGọi \\( D' \\) là trung điểm của \\( B'C' \\), ta có \\( BDC'D' \\) là hình bình hành\n\n\\( \\Rightarrow C'D // BD' \\Rightarrow C'D // (A'BD') \\).\n\nKẻ \\( B'H \\perp BD' \\).\n\nTa có:\n\\( \\begin{cases} A'D' \\perp B'C' \\\\ A'D' \\perp BB' \\end{cases} \\Rightarrow A'D' \\perp (BCC'B') \\Rightarrow A'D' \\perp B'H \\).\n\n\\( \\begin{cases} B'H \\perp BD' \\\\ B'H \\perp A'D' \\end{cases} \\Rightarrow B'H \\perp (A'BD') \\).\n\nSuy ra,\n\\( d(A'B, C'D) = d(C'D; (A'BD')) = d(C'; (A'BD')) = d(B'; (A'BD')) = B'H \\).\n\nTa có: \\( B'D' = \\dfrac{a}{2}; BB' = 2a \\).\n\nXét \\( \\triangle BB'D' \\) vuông tại \\( B' \\) ta có:\n\n\\( \\dfrac{1}{B'H^2} = \\dfrac{1}{BB'^2} + \\dfrac{1}{B'D'^2} = \\dfrac{1}{4a^2} + \\dfrac{4}{a^2} \\Rightarrow BH = \\dfrac{2a}{\\sqrt{17}} \\).\n\nĐáp án D.",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau19_loigiai.PNG"
},
{
  "content": "Cho phương trình \\( (m-1)x^4 + 2(m-3)x^2 + m + 3 = 0 \\) (\\( m \\) là tham số). Tìm \\( m \\) để phương trình vô nghiệm.",
  "options": {
    "A": "\\( m \\in (-\\infty; -3) \\cup \\left(\\dfrac{3}{2}; +\\infty\\right) \\)",
    "B": "\\( m \\le -3 \\)",
    "C": "\\( m > \\dfrac{3}{2} \\)",
    "D": "\\( m < -3 \\)"
  },
  "correct": "A",
  "explanation": "Đặt \\( t = x^2, (t \\ge 0) \\).\n\nĐể phương trình ẩn \\( x \\) vô nghiệm thì phương trình ẩn \\( t \\) vô nghiệm hoặc có 2 nghiệm âm.\n\nĐặt \\( t = x^2, (t \\ge 0) \\). Khi đó ta có phương trình:\n\\( (m-1)t^2 + 2(m-3)t + m+3 = 0 \\). (1)\n\nVới \\( m = 1 \\) thì (1) \\( \\Leftrightarrow -4t+4=0 \\Leftrightarrow t=1 \\Leftrightarrow x = \\pm 1 \\) (Loại)\n\nVới \\( m \\ne 1 \\) để phương trình ban đầu vô nghiệm thì:\n\nTH1: (1) vô nghiệm \\( \\Leftrightarrow \\Delta' < 0 \\Leftrightarrow -8m+12 < 0 \\Leftrightarrow m > \\dfrac{3}{2} \\).\n\nTH2: (1) có 2 nghiệm âm\n\n\\( \\Leftrightarrow \\begin{cases} \\Delta' \\ge 0 \\\\ t_1.t_2 > 0 \\\\ t_1+t_2 < 0 \\end{cases} \\Leftrightarrow \\begin{cases} -8m+12 \\ge 0 \\\\ \\dfrac{m+3}{m-1} > 0 \\\\ -\\dfrac{2(m-3)}{m+1} < 0 \\end{cases} \\)\n\n\\( \\Leftrightarrow \\begin{cases} m \\le \\dfrac{3}{2} \\\\ m \\in (-\\infty;-3) \\cup (1;+\\infty) \\\\ m \\in (-\\infty;1) \\cup (3;+\\infty) \\end{cases} \\Leftrightarrow m \\in (-\\infty;-3) \\)\n\nKết hợp 2 trường hợp, ta được \\( m \\in (-\\infty;-3) \\cup \\left(\\dfrac{3}{2};+\\infty\\right) \\).\n\nĐáp án A."
},
          {
  "content": "Cho hàm số \\( f(x) = k\\sqrt[3]{x} + \\sqrt{x} \\). Với giá trị nào của \\( k \\) thì \\( f'(1) = \\dfrac{3}{2} \\)?",
  "options": {"A": "\\( k = 1 \\)", "B": "\\( k = \\dfrac{9}{2} \\)", "C": "\\( k = -3 \\)", "D": "\\( k = 3 \\)"},
  "correct": "D",
  "explanation": "Tính đạo hàm của hàm số. Từ đó tính \\( f'(1) \\Rightarrow k \\).\n\nTa có: \\( f(x) = k.\\sqrt[3]{x} + \\sqrt{x} = k.x^{\\frac{1}{3}} + \\sqrt{x} \\).\n\n\\( f'(x) = \\dfrac{k}{3}x^{-\\frac{2}{3}} + \\dfrac{1}{2\\sqrt{x}} = \\dfrac{k}{3\\sqrt[3]{x^2}} + \\dfrac{1}{2\\sqrt{x}} \\).\n\nĐể \\( f'(1) = \\dfrac{3}{2} \\Leftrightarrow \\dfrac{k}{3} + \\dfrac{1}{2} = \\dfrac{3}{2} \\Leftrightarrow k = 3 \\).\n\nĐáp án D."
},
{
  "content": "Cho hàm số \\( f(x) \\) có đạo hàm trên \\( \\mathbb{R} \\) và \\( f'(x) < 0, \\forall x \\in (0;+\\infty) \\) biết \\( f(0) = 3 \\). Khẳng định nào sau đây có thể xảy ra.",
  "options": {
    "A": "\\( f(2024) = 3,5 \\)",
    "B": "\\( f(2023) + f(2024) = 6 \\)",
    "C": "\\( f(2023) < f(2024) \\)",
    "D": "\\( f(-2024) = 3 \\)"
  },
  "correct": "D",
  "explanation": "Xét từng đáp án.\n\nDo \\( f'(x) < 0, \\forall x \\in (0;+\\infty) \\) nên hàm số \\( y = f(x) \\) nghịch biến trên \\( (0;+\\infty) \\).\n\nKhi đó ta có:\n\n\\( f(2024) < f(0) = 3 \\Rightarrow \\) A sai\n\n\\( f(2023) < f(0) = 3 \\Rightarrow f(2023) + f(2024) < 3+3 = 6 \\Rightarrow \\) B sai\n\n\\( f(2023) > f(2024) \\Rightarrow \\) C sai\n\nDo đó, D đúng.\n\nĐáp án D."
},
{
  "content": "Phương trình đường tròn có tâm thuộc đường thẳng \\( \\Delta: x - 2y = 0 \\), tiếp xúc với đường thẳng \\( \\Delta': 2x - y + 2 = 0 \\) đồng thời đường tròn đi qua điểm \\( M(1;3) \\) là:",
  "options": {
    "A": "\\( (x+2)^2+(y+1)^2=5 \\) và \\( \\left(x+\\dfrac{23}{4}\\right)^2+\\left(y+\\dfrac{23}{8}\\right)^2=\\dfrac{1445}{64} \\)",
    "B": "\\( (x-2)^2+(y-1)^2=5 \\) và \\( \\left(x-\\dfrac{23}{4}\\right)^2+\\left(y-\\dfrac{23}{8}\\right)^2=\\dfrac{1445}{64} \\)",
    "C": "\\( (x+1)^2+(y-1)^2=5 \\) và \\( \\left(x-\\dfrac{23}{4}\\right)^2+\\left(y-\\dfrac{23}{8}\\right)^2=\\dfrac{1445}{64} \\)",
    "D": "\\( (x-2)^2+(y-1)^2=5 \\) và \\( \\left(x-\\dfrac{23}{4}\\right)^2+\\left(y-\\dfrac{23}{8}\\right)^2=\\dfrac{1885}{16} \\)"
  },
  "correct": "B",
  "explanation": "Gọi tâm của đường tròn cần tìm là \\( I(2t;t) \\in \\Delta: x-2y=0 \\).\n\nTa có: \\( MI = d(I;\\Delta') \\) từ đó tìm được \\( t \\).\n\nTheo giả thiết, ta có:\n\n\\( MI = d(I;\\Delta') \\Leftrightarrow \\sqrt{(2t-1)^2+(t-3)^2} = \\dfrac{|2.2t-t+2|}{\\sqrt{5}} \\)\n\n\\( \\Leftrightarrow \\sqrt{5t^2-10t+10} = \\dfrac{|3t+2|}{\\sqrt{5}} \\Leftrightarrow 8t^2-31t+23=0 \\)\n\n\\( \\Leftrightarrow \\left[\\begin{array}{l} t=1 \\\\ t=\\dfrac{23}{8} \\end{array}\\right. \\)\n\nVới \\( t=1 \\) thì đường tròn cần tìm có tâm \\( I(2;1) \\), bán kính \\( R = IM = \\sqrt{5} \\), và có phương trình là:\n\n\\( (x-2)^2+(y-1)^2=5 \\)\n\nVới \\( t=\\dfrac{23}{8} \\) thì đường tròn cần tìm có tâm \\( I\\left(\\dfrac{23}{4};\\dfrac{23}{8}\\right) \\), bán kính \\( R=IM=\\dfrac{17\\sqrt{5}}{8} \\), và có phương trình là:\n\n\\( \\left(x-\\dfrac{23}{4}\\right)^2+\\left(y-\\dfrac{23}{8}\\right)^2=\\dfrac{1445}{64} \\)\n\nVậy có hai đường tròn thỏa mãn yêu cầu bài toán như trên.\n\nĐáp án B."
},
{
  "content": "Khoảng cách giữa hai điểm cực trị của đồ thị hàm số \\( y = (x-2)^2(x+1) \\) là",
  "options": {"A": "\\( 2\\sqrt{5} \\)", "B": "\\( 5\\sqrt{2} \\)", "C": "4", "D": "2"},
  "correct": "A",
  "explanation": "Tìm hai điểm cực trị. Áp dụng công thức khoảng cách giữa hai điểm.\n\n\\( f'(x) = 2(x-2)(x+1) + (x-2)^2 = 2x^2-2x-4+x^2-4x+4 = 3x^2-6x \\)\n\n\\( f'(x) = 0 \\Leftrightarrow \\left[\\begin{array}{l} x=0 \\Rightarrow y=4 \\\\ x=2 \\Rightarrow y=0 \\end{array}\\right. \\)\n\n\\( \\Rightarrow \\) Khoảng cách giữa hai điểm cực trị là \\( \\sqrt{(0-2)^2+(4-0)^2} = 2\\sqrt{5} \\).\n\n**Có thể sử dụng máy tính casio 580vnx để tìm cực đại và cực tiểu của hàm bậc 3.**\n\nĐáp án A."
},
{
  "content": "Với số nguyên dương \\( n \\), gọi \\( a_{3n-3} \\) là hệ số của \\( x^{3n-3} \\) trong khai triển thành đa thức của \\( (x^2+1)^n(x+2)^n \\). Tìm \\( n \\) để \\( a_{3n-3} = 26n \\).",
  "options": {"A": "\\( n = 6 \\)", "B": "\\( n = 7 \\)", "C": "\\( n = 5 \\)", "D": "\\( n = 4 \\)"},
  "correct": "C",
  "explanation": "Ta có:\n\n\\( (x^2+1)^n = C_n^0 x^{2n} + C_n^1 x^{2n-2} + C_n^2 x^{2n-4} + \\ldots + C_n^n \\)\n\n\\( (x+2)^n = C_n^0 x^n + 2C_n^1 x^{n-1} + 2^2C_n^2 x^{n-2} + \\ldots + 2^nC_n^n \\)\n\nTa thấy \\( n=1, n=2 \\) không thoả mãn điều kiện bài toán.\n\nVới \\( n \\ge 3 \\) ta có: \\( x^{3n-3} = x^{2n}.x^{n-3} = x^{2n-2}.x^{n-1} \\)\n\nDo đó hệ số của \\( x^{3n-3} \\) trong khai triển thành đa thức của \\( (x^2+1)^n(x+2)^n \\) là:\n\n\\( a_{3n-3} = 2^3.C_n^0.C_n^3 + 2.C_n^1.C_n^1 \\)\n\n\\( \\Rightarrow a_{3n-3} = 26n \\Leftrightarrow \\dfrac{2n(2n^2-3n+4)}{3} = 26n \\)\n\n\\( \\Leftrightarrow \\left[\\begin{array}{l} n=0 \\; (L) \\\\ n=-\\dfrac{7}{2} \\; (L) \\\\ n=5 \\; (t/m) \\end{array}\\right. \\)\n\nVậy \\( n=5 \\) là giá trị cần tìm.\n\nĐáp án C."
},
{
  "content": "Chọn ngẫu nhiên lần lượt các số a, b phân biệt thuộc tập hợp \\( \\{3^k \\mid k \\in \\mathbb{N}, 1 \\le k \\le 10\\} \\). Tính xác suất để \\( \\log_a b \\) là một số nguyên dương.",
  "options": {"A": "\\( \\dfrac{17}{90} \\)", "B": "\\( \\dfrac{17}{45} \\)", "C": "\\( \\dfrac{3}{10} \\)", "D": "\\( \\dfrac{22}{45} \\)"},
  "correct": "A",
  "explanation": "Sử dụng công thức tính xác suất xảy ra biến cố \\( A: P(A) = \\dfrac{n_A}{n_\\Omega} \\).\n\nPhép thử: \"Chọn ngẫu nhiên lần lượt các số a, b phân biệt thuộc tập hợp \\( \\{3^k \\mid k \\in \\mathbb{N}, 1 \\le k \\le 10\\} \\)\"\n\nBiến cố \\( A \\): \"\\( \\log_a b \\) là một số nguyên dương\".\n\n\\( \\Rightarrow n_\\Omega = 10.9 = 90 \\)\n\n+ Giả sử \\( a = 3^{k_1}, b = 3^{k_2} \\; (k_1 \\ne k_2) \\Rightarrow \\log_a b = \\log_{3^{k_1}}(3^{k_2}) = \\dfrac{k_2}{k_1} \\) là một số nguyên dương\n\nTa lập bảng các giá trị \\( k_2 \\) tương ứng với \\( k_1 \\) thỏa mãn \\( k_1 | k_2 \\) và \\( k_1 \\ne k_2 \\):",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau29_loigiai.PNG",
  "explanation_2": "Từ bảng trên, ta có:\n\n\\( n_A = 17 \\Rightarrow P(A) = \\dfrac{n_A}{n_\\Omega} = \\dfrac{17}{90} \\).\n\nĐáp án A."
},
          {
  "content": "Cho các số thực a, b, c thỏa mãn \\( c^2 + a = 18 \\) và \\( \\displaystyle\\lim_{x\\to+\\infty}\\left(\\sqrt{ax^2+bx}-cx\\right) = -2 \\). Tính giá trị biểu thức \\( P = a+b+5c \\).",
  "options": {"A": "\\( P = 18 \\)", "B": "\\( P = 12 \\)", "C": "\\( P = 9 \\)", "D": "\\( P = 5 \\)"},
  "correct": "B",
  "explanation": "Dạng vô định \\( \\infty - \\infty \\).\n\n\\( \\displaystyle\\lim_{x\\to+\\infty}\\left(\\sqrt{ax^2+bx}-cx\\right) = \\lim_{x\\to+\\infty}\\dfrac{(a-c^2)x^2+bx}{\\sqrt{ax^2+bx}+cx} = \\lim_{x\\to+\\infty}\\dfrac{(a-c^2)x+b}{\\sqrt{a+\\dfrac{b}{x}}+c} = -2 \\)\n\nKhi và chỉ khi:\n\n\\( \\begin{cases} a-c^2=0 \\\\ \\dfrac{b}{\\sqrt{a}+c}=-2 \\end{cases} \\Leftrightarrow \\begin{cases} a=c^2 \\\\ b=-2\\sqrt{a}-2c \\end{cases} \\)\n\nKết hợp với \\( c^2+a=18 \\)\n\nKhi đó \\( 2c^2=18 \\Leftrightarrow c^2=9 \\rightarrow a=9 \\) và \\( c=3 \\) (vì \\( c \\ne -\\sqrt{a} \\))\n\nVậy \\( b=-2\\sqrt{a}-2c=-2\\sqrt{9}-2.3=-12 \\) nên \\( a+b+5c=9-12+5.3=12 \\).\n\nĐáp án B."
},
{
  "content": "Gọi \\( S \\) là tập hợp các số tự nhiên có 6 chữ số. Chọn ngẫu nhiên một số từ \\( S \\), xác suất để các chữ số của số đó đôi một khác nhau và phải có mặt chữ số 0 và 1 bằng",
  "options": {"A": "\\( \\dfrac{7}{150} \\)", "B": "\\( \\dfrac{7}{375} \\)", "C": "\\( \\dfrac{7}{125} \\)", "D": "\\( \\dfrac{189}{1250} \\)"},
  "correct": "A",
  "explanation": "Sử dụng các quy tắc đếm xác định số kết quả thuận lợi xảy ra biến cố.\n\n+ Gọi số tự nhiên có 6 chữ số là \\( \\overline{a_1a_2a_3a_4a_5a_6} \\).\n\nChọn \\( a_1 \\): có 9 cách.\n\nChọn \\( a_2 \\): có 10 cách.\n\nChọn \\( a_3 \\): có 10 cách.\n\nChọn \\( a_4 \\): có 10 cách.\n\nChọn \\( a_5 \\): có 10 cách.\n\nChọn \\( a_6 \\): có 10 cách.\n\nSuy ra số các phần tử của \\( S \\) là: \\( 9.10^5 \\) cách.\n\nChọn ngẫu nhiên một số từ \\( S \\Rightarrow n(\\Omega) = 9.10^5 \\).\n\n+ Gọi \\( A \\) là biến cố: \"Số được chọn có 6 chữ số đôi một khác nhau và có mặt chữ số 0 và 1\".\n\nTH1: \\( a_1 = 1 \\).\n\nCó 5 vị trí để xếp số 0.\n\nVà có \\( A_8^4 \\) cách chọn 4 vị trí còn lại.\n\nSuy ra có: \\( 5.A_8^4 = 8400 \\) số.\n\nTH2: \\( a_1 = 2, \\ldots, 9 \\)\n\nChọn \\( a_1 \\): có 8 cách.\n\nXếp hai số 0 và 1 có: \\( A_5^2 = 20 \\) cách.\n\nXếp vào 3 vị trí còn lại có: \\( A_7^3 = 210 \\) cách.\n\nSuy ra có: \\( 8.20.210 = 33600 \\) số.\n\n\\( \\Rightarrow n(A) = 8400+33600 = 42000 \\)\n\n\\( \\Rightarrow P(A) = \\dfrac{n(A)}{n(\\Omega)} = \\dfrac{42000}{900000} = \\dfrac{7}{150} \\).\n\nĐáp án A."
},
{
  "content": "Cho a, b, c là ba số thực dương, \\( a>1 \\) thỏa mãn\n\n\\( \\log_a^2(bc) + \\log_a\\left(b^3c^3+\\dfrac{bc}{4}\\right)^2 + 4 + \\sqrt{9-c^2} = 0 \\)\n\nKhi đó, giá trị của biểu thức \\( T = a+3b+2c \\) gần với giá trị nào nhất sau đây?",
  "options": {"A": "8", "B": "9", "C": "7", "D": "10"},
  "correct": "A",
  "explanation": "Áp dụng bất đẳng thức \\( (x+y)^2 \\ge 4xy \\):\n\n\\( \\left(b^3c^3+\\dfrac{bc}{4}\\right)^2 \\ge b^4c^4 \\Rightarrow \\log_a\\left(b^3c^3+\\dfrac{bc}{4}\\right)^2 \\ge 4\\log_a(bc) \\)\n\nDo đó với \\( \\forall a>1, b,c>0 \\)\n\n\\( \\log_a^2(bc) + \\log_a\\left(b^3c^3+\\dfrac{bc}{4}\\right)^2 + 4 + \\sqrt{9-c^2} \\ge \\log_a^2(bc) + 4\\log_a(bc) + 4 + \\sqrt{9-c^2} \\)\n\n\\( \\Leftrightarrow \\log_a^2(bc) + \\log_a\\left(b^3c^3+\\dfrac{bc}{4}\\right)^2 + 4 + \\sqrt{9-c^2} \\ge \\left[\\log_a(bc)+2\\right]^2 + \\sqrt{9-c^2} \\ge 0 \\)\n\nDấu \"=\" xảy ra khi\n\n\\( \\begin{cases} b^3c^3=\\dfrac{bc}{4} \\\\ \\log_a(bc)=-2 \\\\ c^2=9 \\\\ a>1 \\\\ b>0 \\\\ c>0 \\end{cases} \\Rightarrow \\begin{cases} a=\\sqrt{2} \\\\ b=\\dfrac{1}{6} \\\\ c=3 \\end{cases} \\)\n\nKhi đó \\( T = a+3b+2c = \\sqrt{2}+\\dfrac{1}{2}+6 \\approx 7,91 \\).\n\nVậy giá trị của T gần 8 nhất.\n\nĐáp án A."
},
          {
  "content": "Cho hình chóp S.ABCD có đáy ABCD là hình bình hành. Mặt phẳng (α) qua BD và song song với SA, mặt phẳng \\( (\\alpha) \\) cắt SC tại \\( K \\). Tính tỉ số \\( \\dfrac{SK}{KC} \\).",
  "options": {"A": "\\( \\dfrac{SK}{KC}=2 \\)", "B": "\\( \\dfrac{SK}{KC}=3 \\)", "C": "\\( \\dfrac{SK}{KC}=1 \\)", "D": "\\( \\dfrac{SK}{KC}=\\dfrac{1}{2} \\)"},
  "correct": "C",
  "explanation": "Xác định thiết diện của \\( (\\alpha) \\) và hình chóp S.ABCD. Sử dụng định lý Talet để tính tỉ số \\( \\dfrac{SK}{KC} \\).\n\nGọi \\( O = AC \\cap BD \\).\n\nTrong \\( (SAC) \\), kẻ \\( OK // SA \\; (K \\in SC) \\).\n\nDo đó \\( (\\alpha) \\) là mặt phẳng \\( (KBD) \\).\n\nVì ABCD là hình bình hành nên \\( O \\) là trung điểm của \\( AC \\Rightarrow \\dfrac{OC}{OA}=1 \\).\n\nDo \\( OK // SA \\Rightarrow \\dfrac{OC}{OA} = \\dfrac{KC}{KS} = 1 \\Rightarrow \\dfrac{SK}{KC}=1 \\).\n\nĐáp án C.",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau33_loigiai.PNG"
},
{
  "content": "Cho tứ diện ABCD có BCD là tam giác vuông tại đỉnh \\( B \\), cạnh \\( CD = a, BD = \\dfrac{a\\sqrt{6}}{3} \\), \\( AB = AC = AD = \\dfrac{a\\sqrt{3}}{2} \\). Tính cosin của góc nhị diện [A, BC, D].",
  "options": {"A": "\\( \\dfrac{\\sqrt{2}}{2} \\)", "B": "\\( \\dfrac{1}{2} \\)", "C": "\\( \\dfrac{\\sqrt{3}}{2} \\)", "D": "\\( -\\dfrac{1}{2} \\)"},
  "correct": "B",
  "explanation": "Xác định góc nhị diện [A, BC, D].\n\nGọi M, H lần lượt là trung điểm của BC, CD.\n\nDo \\( \\triangle BCD \\) vuông tại \\( B \\) nên \\( BH = CH = DH \\) hay \\( H \\) là tâm đường tròn ngoại tiếp \\( \\triangle BCD \\).\n\nMà \\( AB = AC = AD \\) nên AH là đường cao kẻ từ \\( A \\) xuống \\( (BCD) \\) hay \\( AH \\perp (BCD) \\).\n\n\\( \\Rightarrow AH \\perp BC \\). (1)\n\nM, H là trung điểm của BC, CD nên MH là đường trung bình của \\( \\triangle BCD \\)\n\n\\( \\Rightarrow \\begin{cases} MH = \\dfrac{1}{2}BD = \\dfrac{a\\sqrt{6}}{6} \\\\ MH // BD \\end{cases} \\)\n\nMà \\( MD \\perp BC \\) nên \\( MH \\perp BC \\). (2)\n\nTừ (1), (2) suy ra: \\( BC \\perp (AMH) \\).\n\nSuy ra: \\( \\begin{cases} BC \\perp AM \\\\ BC \\perp MH \\end{cases} \\Rightarrow [A,BC,D] = \\widehat{AMH} \\).\n\nLại có: \\( AH = \\sqrt{AC^2-CH^2} = \\sqrt{\\left(\\dfrac{a\\sqrt{3}}{2}\\right)^2-\\left(\\dfrac{a}{2}\\right)^2} = \\dfrac{a\\sqrt{2}}{2} \\).\n\n\\( \\Rightarrow \\tan\\widehat{AMH} = \\dfrac{AH}{MH} = \\sqrt{3} \\Rightarrow \\widehat{AMH} = \\dfrac{\\pi}{3} \\Rightarrow \\cos\\widehat{AMH} = \\dfrac{1}{2} \\).\n\nĐáp án B.",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau35_loigiai.PNG"
},
            {
                "content": "Cho hàm số \\( f(x) = -2x + 7 \\). Giá trị \\( f(3) \\) bằng",
                "options": {"A": "1", "B": "-1", "C": "13", "D": "4"},
                "correct": "A",
                "explanation": "\\( f(3) = -2 \\times 3 + 7 = 1 \\). Đáp án A.",
            },
           
            {
                "content": "Cho dãy số liệu: 4, 6, 8, 10, 12. Số trung bình cộng của dãy số liệu trên bằng",
                "options": {"A": "9", "B": "7", "C": "8", "D": "10"},
                "correct": "C",
                "explanation": "Trung bình cộng \\( = (4+6+8+10+12):5 = 40:5 = 8 \\). Đáp án C.",
            },
          {
  "content": "Nghiệm của phương trình \\( 2^{2x-1} = 8 \\) là:",
  "options": {"A": "\\( x=2 \\)", "B": "\\( x=1 \\)", "C": "\\( x=4 \\)", "D": "\\( x=\\dfrac{5}{2} \\)"},
  "correct": "A",
  "explanation": "Dùng máy tính bỏ túi tìm nghiệm hoặc dùng tính chất cơ bản của số mũ, lũy thừa để giải nhanh.\n\nTa có: \\( 2^{2x-1}=8 \\Leftrightarrow 2x-1=3 \\Leftrightarrow x=2 \\).\n\nĐáp án A."
},
{
  "content": "Một vật chuyển động theo quy luật \\( s = -\\dfrac{1}{2}t^3+9t^2 \\) với \\( t \\) (giây) là khoảng thời gian tính từ lúc bắt đầu chuyển động và \\( s \\) (mét) là quãng đường vật đi được trong khoảng thời gian đó. Hỏi trong khoảng thời gian 10 giây, kể từ lúc bắt đầu chuyển động, vận tốc lớn nhất của vật đạt được bằng bao nhiêu?",
  "options": {"A": "216 (m/s)", "B": "30 (m/s)", "C": "400 (m/s)", "D": "54 (m/s)"},
  "correct": "D",
  "explanation": "Vận tốc của vật là \\( v(t)=s'(t) \\). Tìm giá trị lớn nhất của \\( v(t) \\).\n\nVận tốc tại thời điểm \\( t \\) là \\( v(t)=s'(t)=-\\dfrac{3}{2}t^2+18t \\) với \\( t\\in[0;10] \\).\n\nTa có: \\( v'(t)=-3t+18=0 \\Leftrightarrow t=6 \\).\n\nSuy ra: \\( v(0)=0; v(10)=30; v(6)=54 \\).\n\nVậy vận tốc lớn nhất của vật đạt được bằng 54 (m/s).\n\nĐáp án D."
},
{
  "content": "Trong mặt phẳng với hệ tọa độ Oxy, cho đường thẳng \\( d: \\begin{cases} x=2+t \\\\ y=1-3t \\end{cases} \\) và hai điểm \\( A(1;2), B(-2;m) \\). Tìm tất cả các giá trị của tham số \\( m \\) để \\( A \\) và \\( B \\) nằm cùng phía đối với \\( d \\).",
  "options": {"A": "\\( m>13 \\)", "B": "\\( m\\ge 13 \\)", "C": "\\( m<13 \\)", "D": "\\( m=13 \\)"},
  "correct": "C",
  "explanation": "Đưa phương trình đường thẳng \\( d \\) về dạng tổng quát \\( ax+by+c=0 \\).\n\nĐiều kiện để hai điểm \\( A(x_A;y_A), B(x_B;y_B) \\) nằm cùng phía đối với \\( d \\) là:\n\n\\( (a.x_A+b.y_A+c)(a.x_B+b.y_B+c)>0 \\).\n\nTa có: \\( d: \\begin{cases} x=2+t \\\\ y=1-3t \\end{cases} \\Rightarrow d: 3x+y-7=0 \\).\n\nĐể \\( A, B \\) nằm cùng phía đối với \\( d \\) thì:\n\n\\( (3x_A+y_A-7)(3x_B+y_B-7)>0 \\Leftrightarrow -2(m-13)>0 \\Leftrightarrow m-13<0 \\Leftrightarrow m<13 \\).\n\nĐáp án C."
},
{
  "content": "Cho cấp số cộng \\( (u_n) \\) có \\( u_1=4 \\). Giá trị nhỏ nhất của \\( u_1u_2+u_2u_3+u_3u_1 \\) bằng:",
  "options": {"A": "-8", "B": "-24", "C": "-20", "D": "-6"},
  "correct": "B",
  "explanation": "Sử dụng công thức số hạng tổng quát của CSC: \\( u_n=u_1+(n-1)d \\).\n\nTính biểu thức \\( u_1u_2+u_2u_3+u_3u_1 \\) theo \\( d \\) rồi tìm giá trị nhỏ nhất.\n\nTa gọi \\( d \\) là công sai của cấp số cộng.\n\nKhi đó:\n\n\\( u_1u_2+u_2u_3+u_3u_1 = 4(4+d)+(4+d)(4+2d)+4(4+2d) \\)\n\n\\( = 2d^2+24d+48 = 2(d+6)^2-24 \\ge -24 \\)\n\nVậy giá trị nhỏ nhất của \\( u_1u_2+u_2u_3+u_3u_1 \\) là -24 đạt được khi \\( d=-6 \\).\n\nĐáp án B."
},
{
  "content": "Cho cấp số nhân \\( (u_n) \\) có \\( u_2=-6, u_5=48 \\). Tính \\( S_5 \\).",
  "options": {"A": "33", "B": "-31", "C": "93", "D": "11"},
  "correct": "A",
  "explanation": "Tính tổng n số hạng đầu tiên của dãy.\n\nTa có \\( \\begin{cases} u_1.q=-6 \\\\ u_1.q^4=48 \\end{cases} \\Rightarrow \\begin{cases} u_1.q=-6 \\\\ q^3=-8 \\end{cases} \\Rightarrow \\begin{cases} u_1=3 \\\\ q=-2 \\end{cases} \\).\n\nVậy \\( S_5 = \\dfrac{3\\left(1-(-2)^5\\right)}{1-(-2)} = 33 \\).\n\nĐáp án A."
},
{
  "content": "Năng lượng giải tỏa \\( E \\) của một trận động đất tại tâm địa chấn \\( M \\) độ Richter được xác định bởi công thức \\( \\log E = 11,4+1,5M \\). Vào năm 1995, thành phố \\( X \\) xảy ra một trận động đất 8 độ Richter và năng lượng giải tỏa tại tâm địa chấn của nó gấp 14 lần trận động đất ra tại thành phố \\( Y \\) vào năm 1997. Hỏi khi đó độ lớn của trận động đất tại thành phố \\( Y \\) là bao nhiêu? (kết quả làm tròn đến hàng phần chục)",
  "options": {"A": "7,2 độ Richter", "B": "7,8 độ Richter", "C": "8,3 độ Richter", "D": "6,8 độ Richter"},
  "correct": "A",
  "explanation": "Từ tỉ lệ năng lượng tỏa ra của 2 trận động đất suy ra độ lớn của trận động đất tại thành phố \\( Y \\).\n\nTheo đề bài ta có: \\( \\dfrac{E_X}{E_Y}=14 \\).\n\n\\( \\Rightarrow \\log\\left(\\dfrac{E_X}{E_Y}\\right) = \\log E_X - \\log E_Y = 1,5(M_X-M_Y) = \\log 14 \\)\n\n\\( \\Leftrightarrow M_X-M_Y = \\dfrac{\\log 14}{1,5} \\Rightarrow M_Y = 8-\\dfrac{\\log 14}{1,5} \\approx 7,2 \\)\n\nVậy độ lớn của trận động đất tại thành phố \\( Y \\) là 7,2 độ Richter.\n\nĐáp án A."
},
{
  "content": "Tồn tại bao nhiêu giá trị nguyên của tham số \\( m\\in[-30;30] \\) sao cho đồ thị hàm số \\( y=\\dfrac{2x^2+5}{x^3+(m-4)x+2m} \\) có ít nhất một tiệm cận đứng nằm bên phải trục tung?",
  "options": {"A": "61", "B": "32", "C": "16", "D": "13"},
  "correct": "B",
  "explanation": "Để đồ thị hàm số có ít nhất một tiệm cận đứng nằm bên phải trục tung thì phương trình \\( x^3+(m-4)x+2m=0 \\) có ít nhất 1 nghiệm dương.\n\nTa có:\n\n\\( x^3+(m-4)x+2m=0 \\)\n\n\\( \\Leftrightarrow x^3-4x+mx+2m=0 \\)\n\n\\( \\Leftrightarrow x(x-2)(x+2)+m(x+2)=0 \\)\n\n\\( \\Leftrightarrow (x+2)(x^2-2x+m)=0 \\)\n\n\\( \\Leftrightarrow \\left[\\begin{array}{l} x=-2 \\\\ x^2-2x+m=0 \\; (*) \\end{array}\\right. \\)\n\nĐể (*) có ít nhất 1 nghiệm dương thì:\n\nTH1: (*) có 2 nghiệm trái dấu \\( \\Leftrightarrow m<0 \\)\n\nMà \\( m\\in[-30;30]; m\\in\\mathbb{Z} \\) nên \\( m\\in\\{-30;-29;\\ldots;-1\\} \\).\n\nTH2: (*) có 2 nghiệm phân biệt \\( 0\\le x_1<x_2 \\)\n\n\\( \\Leftrightarrow \\begin{cases} \\Delta'=1-m>0 \\\\ x_1x_2=m\\ge 0 \\\\ x_1+x_2=2>0 \\end{cases} \\Leftrightarrow 0\\le m<1 \\).\n\nMà \\( m\\in[-30;30]; m\\in\\mathbb{Z} \\) nên \\( m=0 \\).\n\nTH3: (*) có nghiệm kép lớn hơn 0.\n\n\\( \\Leftrightarrow \\begin{cases} \\Delta'=1-m=0 \\\\ x_1x_2=m>0 \\end{cases} \\Leftrightarrow 0<m\\le 1 \\).\n\nMà \\( m\\in[-30;30]; m\\in\\mathbb{Z} \\) nên \\( m=1 \\).\n\nVậy \\( m\\in\\{-30;-29;\\ldots;1\\} \\Rightarrow \\) có 32 giá trị nguyên của \\( m \\) thỏa mãn yêu cầu bài toán.\n\nĐáp án B."
},
          {
  "content": "Hàm số \\( y = 3\\cos\\left(\\dfrac{\\pi}{4}-mx\\right) \\) tuần hoàn có chu kì \\( T=3\\pi \\) khi",
  "options": {"A": "\\( m=\\pm\\dfrac{3}{2} \\)", "B": "\\( m=\\pm 1 \\)", "C": "\\( m=\\pm\\dfrac{2}{3} \\)", "D": "\\( m=\\pm 2 \\)"},
  "correct": "C",
  "explanation": "Tìm chu kì của hàm số lượng giác.\n\nHàm số \\( y=3\\cos\\left(\\dfrac{\\pi}{4}-mx\\right) \\) có nghĩa \\( \\forall x\\in\\mathbb{R} \\Leftrightarrow D=\\mathbb{R} \\).\n\nChu kì của hàm số \\( T=\\dfrac{2\\pi}{|-m|}=3\\pi \\Leftrightarrow m=\\pm\\dfrac{2}{3} \\).\n\nĐáp án C."
},
{
  "content": "Giả sử \\( x_1, x_2 \\) là nghiệm của phương trình \\( x^2-(m+2)x+m^2+1=0 \\). Khi đó giá trị lớn nhất của biểu thức \\( P=4(x_1+x_2)-x_1x_2 \\) bằng:",
  "options": {"A": "\\( \\dfrac{95}{9} \\)", "B": "11", "C": "7", "D": "\\( -\\dfrac{1}{9} \\)"},
  "correct": "A",
  "explanation": "Tìm điều kiện để phương trình bậc hai có hai nghiệm \\( \\Leftrightarrow \\Delta \\ge 0 \\).\n\nÁp dụng định lý Viet để tìm \\( x_1+x_2 \\) và \\( x_1x_2 \\) theo \\( m \\). Từ đó tính giá trị lớn nhất của \\( P \\).\n\nĐể phương trình có hai nghiệm \\( x_1; x_2 \\) thì\n\n\\( \\Delta = (m+2)^2-4(m^2+1) \\ge 0 \\Leftrightarrow -3m^2+4m \\ge 0 \\Leftrightarrow 0 \\le m \\le \\dfrac{4}{3} \\).\n\nÁp dụng hệ thức Viet ta có: \\( \\begin{cases} x_1+x_2=m+2 \\\\ x_1.x_2=m^2+1 \\end{cases} \\)\n\nKhi đó: \\( P = 4(m+2)-(m^2+1) = -m^2+4m+7 \\).\n\nXét hàm số \\( P(m)=-m^2+4m+7, \\forall m\\in\\left[0;\\dfrac{4}{3}\\right] \\) có hệ số \\( a<0 \\), hoành độ đỉnh \\( x=2 \\) nên \\( P(m) \\) đồng biến trên \\( \\left[0;\\dfrac{4}{3}\\right] \\Rightarrow \\displaystyle\\max_{\\left[0;\\frac{4}{3}\\right]} P = P\\left(\\dfrac{4}{3}\\right) = \\dfrac{95}{9} \\).\n\nĐáp án A."
},
          {
  "content": "Cho hàm số \\( y = \\dfrac{2x+1}{x-2} \\) có đồ thị \\( (C) \\). Hỏi có tất cả bao nhiêu điểm thuộc đồ thị \\( (C) \\) mà tiếp tuyến của \\( (C) \\) tại điểm đó tạo với hai trục tọa độ một tam giác có diện tích bằng \\( \\dfrac{2}{5} \\)?",
  "options": {"A": "4", "B": "5", "C": "2", "D": "3"},
  "correct": "C",
  "explanation": "Xác định phương trình tiếp tuyến tại 1 điểm.\n\nPhương trình tiếp tuyến của \\( (C) \\) tại điểm có hoành độ \\( x_0 \\) là:\n\n\\( y = \\dfrac{-5}{(x_0-2)^2}(x-x_0)+\\dfrac{2x_0+1}{x_0-2} \\)\n\nTọa độ giao điểm của tiếp tuyến với các trục tọa độ là\n\n\\( A\\left(\\dfrac{2x_0^2+2x_0-2}{5};0\\right), B\\left(0;\\dfrac{2x_0^2+2x_0-2}{(x_0-2)^2}\\right) \\)\n\nDo đó diện tích tam giác \\( S_{OAB} = \\dfrac{1}{2}.OA.OB = \\dfrac{\\left(2x_0^2+2x_0-2\\right)^2}{10(x_0-2)^2} = \\dfrac{2}{5} \\Leftrightarrow \\left[\\begin{array}{l} x_0=-3 \\\\ x_0=1 \\end{array}\\right. \\)\n\nVậy có 2 điểm thỏa mãn.\n\nĐáp án C."
},
{
  "content": "Có bao nhiêu cặp số nguyên \\( (x,y) \\) thỏa mãn điều kiện \\( 0\\le y\\le 100 \\) và \\( x^6+6x^4y+12x^2y^2-19y^3+3x^2-3y=0 \\)?",
  "options": {"A": "10", "B": "100", "C": "20", "D": "21"},
  "correct": "D",
  "explanation": "Sử dụng hàm đặc trưng.\n\n\\( x^6+6x^4y+12x^2y^2-19y^3+3x^2-3y=0 \\)\n\n\\( \\Leftrightarrow x^6+6x^4y+12x^2y^2+8y^3-27y^3+3x^2-3y=0 \\)\n\n\\( \\Leftrightarrow x^6+6x^4y+12x^2y^2+8y^3+3x^2+6y = 27y^3+9y \\)\n\n\\( \\Leftrightarrow \\left(x^2+2y\\right)^3+3\\left(x^2+2y\\right) = (3y)^3+3.3y \\) (*)\n\nXét hàm số: \\( f(t) = t^3+3t \\)\n\nTa có: \\( f'(t) = 3t^2+3>0 \\; \\forall t\\in\\mathbb{R} \\Rightarrow f(t) \\) là hàm đồng biến trên \\( \\mathbb{R} \\)\n\nVì vậy (*) \\( \\Leftrightarrow f(x^2+2y) = f(3y) \\Leftrightarrow x^2+2y=3y \\Leftrightarrow x^2=y \\)\n\nTheo giả thiết ta có: \\( 0\\le y\\le 100 \\Leftrightarrow 0\\le x^2\\le 100 \\Leftrightarrow -10\\le x\\le 10 \\)\n\nVì x nguyên nên \\( x\\in\\{-10;-9;-8;\\ldots;8;9;10\\} \\), với mỗi \\( x \\) xác định duy nhất giá trị \\( y=x^2 \\).\n\nVậy có 21 cặp \\( (x;y) \\) thỏa mãn bài toán.\n\nĐáp án D."
},
{
  "content": "Trong phòng giáo viên, giờ ra chơi có bốn cô giáo: An, Bình, Giang và Nhàn ngồi nói chuyện với nhau quanh 1 chiếc bàn hình tròn. Cô mặc áo dài xanh (không phải là cô An và cô Bình) thì ngồi giữa cô mặc áo dài tím và cô Nhàn. Cô mặc áo dài trắng thì ngồi giữa cô mặc áo dài hồng và cô Bình. Vậy cô An mặc áo màu gì?",
  "options": {"A": "Hồng", "B": "Tím", "C": "Trắng", "D": "Xanh"},
  "correct": "C",
  "explanation": "Cô mặc áo dài xanh không phải cô An và cô Bình lại ngồi giữa cô mặc áo dài tím và cô Nhàn ⇒ loại phương án D.\n\n⇒ Cô mặc áo dài xanh là cô Giang.\n\nCô mặc áo dài trắng thì ngồi giữa cô mặc áo dài hồng và cô Nhàn\n\n⇒ Cô mặc áo tím là cô Bình, áo hồng là cô Nhàn và cô An mặc áo trắng.\n\nĐáp án C."
},
{
  "content": "Cho hình chóp S.ABCD đáy là hình vuông cạnh \\( a \\). Mặt bên SAD là tam giác đều và nằm trong mặt phẳng vuông góc với đáy. Gọi M, N, P lần lượt là trung điểm của các cạnh SB, BC, CD. Tính thể tích khối tứ diện CMNP.",
  "options": {"A": "\\( 3a^3\\sqrt{3} \\)", "B": "\\( \\dfrac{a^3\\sqrt{3}}{96} \\)", "C": "\\( \\dfrac{a^3\\sqrt{2}}{96} \\)", "D": "\\( \\dfrac{a^3}{96} \\)"},
  "correct": "B",
  "explanation": "Sử dụng tỉ số thể tích.",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_cau7_loigiai.PNG",
  "explanation_2": "\\( \\dfrac{V_{CMNP}}{V_{CMBD}} = \\dfrac{CN}{CB}.\\dfrac{CP}{CD} = \\dfrac{1}{4} \\) (*),\n\n\\( \\dfrac{V_{CMBD}}{V_{S.CBD}} = \\dfrac{V_{M.CBD}}{V_{S.CBD}} = \\dfrac{BM}{BS} = \\dfrac{1}{2} \\) (**)\n\nLấy (*).(**) ta được: \\( \\dfrac{V_{CMNP}}{V_{S.BCD}} = \\dfrac{1}{8} \\Rightarrow V_{CMNP} = \\dfrac{1}{8}V_{S.BCD} \\)\n\nGọi H là trung điểm AD \\( \\Rightarrow SH \\perp AD \\) và \\( (SAD) \\perp (ABCD) \\) nên \\( SH \\perp (ABCD) \\)\n\n\\( V_{S.BCD} = \\dfrac{1}{3}SH.S_{BCD} = \\dfrac{a^3\\sqrt{3}}{12} \\Rightarrow V_{CMNP} = \\dfrac{a^3\\sqrt{3}}{96} \\)\n\nĐáp án B."
},
{
  "content": "Cho hình chóp S.ABCD có đáy ABCD là hình thoi và \\( AB=BD=a, SA=a\\sqrt{3}, SA\\perp(ABCD) \\). Gọi M là điểm trên cạnh SB sao cho \\( BM=\\dfrac{2}{3}SB \\). Giả sử N là điểm di động trên cạnh AD. Tìm vị trí điểm N để \\( BN\\perp DM \\)?",
  "options": {
    "A": "N nằm trên cạnh AD sao cho \\( AN=\\dfrac{3}{5}AD \\)",
    "B": "N nằm trên cạnh AD sao cho \\( AN=\\dfrac{2}{5}AD \\)",
    "C": "N nằm trên cạnh AD sao cho \\( AN=\\dfrac{4}{5}AD \\)",
    "D": "N nằm trên cạnh AD sao cho \\( AN=\\dfrac{3}{4}AD \\)"
  },
  "correct": "B",
  "explanation": "Phân tích vectơ.",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_cau8_loigiai.PNG",
  "explanation_2": "Vẽ \\( ME \\parallel SA \\Rightarrow ME \\perp (ABCD) \\), do đó \\( DM \\perp BN \\Leftrightarrow DE \\perp BN \\). Đặt \\( AN = x\\vec{AD} \\)\n\nTa có: \\( \\vec{DE} = \\vec{DA}+\\vec{AE} = -\\vec{AD}+\\dfrac{1}{3}\\vec{AB} \\)\n\n\\( \\vec{BN} = -\\vec{AB}+\\vec{AN} = -\\vec{AB}+x\\vec{AD} \\)\n\nVì \\( BN\\perp DE \\Leftrightarrow (3\\vec{AD}-\\vec{AB})(\\vec{AB}-x\\vec{AD}) = 0 \\)\n\n\\( \\Leftrightarrow -3x\\vec{AD}^2-\\vec{AB}^2+(3+x)\\vec{AB}.\\vec{AD} = 0 \\)\n\nVì tam giác ABD đều nên: \\( \\vec{AB}.\\vec{AD} = AB.AD.\\cos\\widehat{BAD} = a.a.\\cos 60^\\circ = \\dfrac{a^2}{2} \\)\n\n\\( \\Leftrightarrow -3ax^2-a^2+\\dfrac{a^2(3+x)}{2} = 0 \\Leftrightarrow x=\\dfrac{2}{5} \\Rightarrow AN = \\dfrac{2}{5}AD \\)\n\nĐáp án B."
},
{
  "content": "Có bao nhiêu giá trị nguyên của tham số \\( m \\) trong đoạn \\( [-10;10] \\) sao cho đồ thị hàm số \\( y=x^3 \\) cắt đường thẳng \\( y=3mx-m^2 \\) tại ba điểm phân biệt?",
  "options": {"A": "4", "B": "6", "C": "3", "D": "8"},
  "correct": "B",
  "explanation": "Xét phương trình hoành độ giao điểm, dựa vào hình dáng đồ thị nhận xét.\n\nXét phương trình hoành độ giao điểm:\n\n\\( x^3 = 3mx-m^2 \\Leftrightarrow x^3-3mx+m^2=0 \\) (1)\n\nYêu cầu bài toán tương đương với phương trình (1) có ba nghiệm phân biệt.\n\nXét hàm số: \\( f(x)=x^3-3mx+m^2 \\) có đồ thị \\( (C) \\). Để phương trình (1) có 3 nghiệm phân biệt thì đồ thị hàm số \\( (C) \\) phải có 2 cực trị nằm về hai phía của trục hoành.\n\nTa có: \\( f'(x)=3x^2-3m, f'(x)=0 \\Leftrightarrow x^2=m \\)\n\nĐể đồ thị hàm số có 2 cực trị nằm về 2 phía so với trục hoành thì \\( x^2=m \\Leftrightarrow x=\\pm\\sqrt{m} \\)\n\n\\( x=\\sqrt{m} \\Rightarrow y=-2m\\sqrt{m}+m^2 \\)\n\n\\( x=-\\sqrt{m} \\Rightarrow y=2m\\sqrt{m}+m^2 \\)\n\nKết hợp các điều kiện ta được: \\( m\\in(4;10] \\) mà \\( m\\in\\mathbb{Z} \\Rightarrow m\\in\\{5;6;7;8;9;10\\} \\)\n\nĐáp án B."
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
  "content": "Đường thẳng \\( y = \\dfrac{1}{2} \\) cắt đồ thị hàm số \\( y = 2\\sin^2 x \\) tại 4 điểm A, B, C, D như hình vẽ. Giá trị của \\( x_B + x_D \\) là \\( \\dfrac{a}{b}\\pi \\). Biết \\( \\dfrac{a}{b} \\) là phân số tối giản. Tính giá trị của \\( 2a+b \\) (điền số nguyên).",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau18_de.PNG",
  "answers": ["19"],
  "explanation": "Tương giao đồ thị, giải phương trình lượng giác tìm \\( x_B; x_D \\). Từ đó tính giá trị \\( x_B+x_D \\).\n\nPhương trình hoành độ giao điểm là:\n\n\\( 2\\sin^2 x = \\dfrac{1}{2} \\Leftrightarrow 1-\\cos 2x = \\dfrac{1}{2} \\Leftrightarrow \\cos 2x = \\dfrac{1}{2} \\)\n\n\\( \\Leftrightarrow 2x = \\pm\\dfrac{\\pi}{3}+k2\\pi \\Leftrightarrow x = \\pm\\dfrac{\\pi}{6}+k\\pi \\)\n\nTa thấy \\( x_A, x_B, x_C, x_D \\) là bốn nghiệm dương nhỏ nhất của phương trình trên.\n\nDo đó: \\( x_A=\\dfrac{\\pi}{6}; x_B=\\dfrac{5\\pi}{6}; x_C=\\dfrac{7\\pi}{6}; x_D=\\dfrac{11\\pi}{6} \\Rightarrow x_B+x_D=\\dfrac{8}{3}\\pi \\).\n\nVậy \\( 2a+b = 8.2+3 = 19 \\)."
},
{
  "content": "Cho hình hộp chữ nhật \\( ABCD.A'B'C'D' \\) có các kích thước \\( AB=4, AD=3, AA'=5 \\). Khoảng cách giữa hai đường thẳng \\( AC' \\) và \\( B'C \\) bằng bao nhiêu? (điền dạng phân số a/b, ví dụ 30/19).",
  "answers": ["30/19"],
  "explanation": "Trong \\( (BB'C'C) \\) kẻ \\( C'M // B'C \\; (M \\in BC) \\).\n\n\\( \\Rightarrow B'C // (AC'M) \\Rightarrow d(AC';B'C) = d(B'C;(AC'M)) = d(C;(AC'M)) \\).",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau20_loigiai.PNG",
  "explanation_2": "Kẻ \\( CH \\perp AM; CK \\perp C'H \\).\n\nDo \\( \\begin{cases} CH \\perp AM \\\\ CC' \\perp AM \\end{cases} \\Rightarrow AM \\perp (CC'H) \\Rightarrow AM \\perp CK \\)\n\nMà \\( CK \\perp C'H \\Rightarrow CK \\perp (AC'M) \\Rightarrow d(C;(AC'M)) = CK \\).\n\nTa có: \\( B'C'MC \\) là hình bình hành nên \\( CM = B'C' = 3 \\).\n\n\\( \\dfrac{1}{d^2(B;AM)} = \\dfrac{1}{AB^2}+\\dfrac{1}{BM^2} \\Rightarrow d(B;AM) = \\dfrac{12}{\\sqrt{13}} \\)\n\n\\( \\Rightarrow CH = \\dfrac{1}{2}d(B;AM) = \\dfrac{6}{\\sqrt{13}} \\).\n\nÁp dụng hệ thức lượng trong tam giác vuông \\( C'CH \\) ta có:\n\n\\( \\dfrac{1}{CK^2} = \\dfrac{1}{CH^2}+\\dfrac{1}{CC'^2} \\Rightarrow CK = \\dfrac{30}{19} \\)."
},
{
  "content": "Một vật chuyển động theo quy luật \\( s = -\\dfrac{2}{3}t^3+7t^2+3 \\) với \\( t \\) giây \\( (0 \\le t \\le 7) \\) là khoảng thời gian tính từ lúc vật bắt đầu chuyển động đến khi dừng lại và \\( s \\) (mét) là quãng đường vật đi được trong khoảng thời gian đó. Hỏi khi vật đạt vận tốc là 12 m/s lần thứ 2 thì vật đã chuyển động được bao nhiêu mét? (điền số nguyên).",
  "answers": ["111"],
  "explanation": "Vận tốc của vật: \\( v = s' \\). Giải phương trình \\( v=12 \\) tìm \\( t \\), từ đó tính quãng đường vật đã chuyển động.\n\nVận tốc của vật là: \\( v = s' = -2t^2+14t \\).\n\nVận tốc của vật đạt \\( 12 \\, m/s \\) thì \\( -2t^2+14t=12 \\Leftrightarrow 2t^2-14t+12=0 \\Leftrightarrow \\left[\\begin{array}{l} t=1 \\\\ t=6 \\end{array}\\right. \\)\n\n\\( \\Rightarrow \\) Vật đạt vận tốc là \\( 12 \\, m/s \\) lần thứ 2 khi \\( t=6 \\).\n\nLúc đó quãng đường vật đi được là:\n\n\\( s(6) = -\\dfrac{2}{3}.6^3+7.6^2+3 = 111 \\) (mét)."
},
{
  "content": "Cho hàm số \\( y = \\sqrt{2x-x^2} \\). Biết hàm số nghịch biến trên đoạn \\( (a;b) \\). Tính \\( a+2b \\) (điền số nguyên).",
  "answers": ["5"],
  "explanation": "Tìm tập xác định, khảo sát hàm số, kết luận khoảng nghịch biến.\n\nTập xác định: \\( D=[0;2] \\).\n\nTa có: \\( y' = \\dfrac{1-x}{\\sqrt{2x-x^2}} = 0 \\Leftrightarrow x=1 \\).\n\nBảng xét dấu:",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau27_loigiai.PNG",
  "explanation_2": "Từ bảng xét dấu, ta thấy hàm số nghịch biến trên \\( (1;2) \\).\n\nKhi đó: \\( a=1; b=2 \\Rightarrow a+2b = 1+2.2 = 5 \\)."
},
          {
  "content": "Cho phương trình \\( e^x = \\ln(x+a)+a \\), với \\( a \\) là tham số. Có bao nhiêu giá trị nguyên của \\( a \\) thuộc khoảng \\( (0;19) \\) để phương trình có nghiệm dương? (điền số nguyên).",
  "answers": ["17"],
  "explanation": "Biến đổi đưa phương trình về dạng hàm đặc trưng đưa phương trình về dạng \\( a = g(x) \\). Khảo sát hàm số \\( g(x) \\) để tìm điều kiện của \\( a \\).\n\nTa có:\n\n\\( e^x = \\ln(x+a)+a \\Leftrightarrow e^x+x = \\ln(x+a)+x+a \\Leftrightarrow e^x+x = e^{\\ln(x+a)}+\\ln(x+a) \\) (1)\n\nXét hàm số \\( f(t) = e^t+t \\) có \\( f'(t) = e^t+1>0, \\forall t \\). Suy ra hàm số \\( f(t) \\) đồng biến trên \\( \\mathbb{R} \\).\n\nDo đó: (1) \\( \\Leftrightarrow f(x) = f[\\ln(x+a)] \\Leftrightarrow x = \\ln(x+a) \\Leftrightarrow a = e^x-x \\).\n\nĐặt \\( g(x) = e^x-x \\Rightarrow g'(x) = e^x-1=0 \\Leftrightarrow x=0 \\).\n\nBảng biến thiên của hàm số \\( g(x) \\):",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau34_loigiai.PNG",
  "explanation_2": "Để phương trình có nghiệm dương thì \\( a>1 \\).\n\nDo \\( a\\in(0;19) \\) và \\( a\\in\\mathbb{Z} \\) nên \\( a\\in\\{2;3;\\ldots;18\\} \\)\n\nVậy có 17 giá trị nguyên của \\( a \\) để phương trình có nghiệm dương."
},
{
  "content": "Gọi S là tập hợp các ước nguyên dương của 1605632. Chọn ngẫu nhiên một số từ S. Tính xác suất để số được chọn chia hết cho 7 (điền dạng phân số a/b, ví dụ 2/3).",
  "answers": ["2/3"],
  "explanation": "Số ước nguyên dương của số A có phân tích thành thừa số nguyên tố \\( A = x_1^{n_1}.x_2^{n_2}\\ldots x_k^{n_k} \\) là \\( (n_1+1)(n_2+1)\\ldots(n_k+1) \\).\n\nTa có: \\( 1605632 = 2^{15}.7^2 \\)\n\nSuy ra số các ước nguyên dương của 1605632 là \\( (15+1)(2+1) = 48 \\).\n\nSố phần tử của không gian mẫu: \\( n(\\Omega) = 48 \\).\n\nTrong đó, số các số chia hết cho 7 là: \\( (15+1).2 = 32 \\).\n\nXác suất cần tìm là: \\( P = \\dfrac{32}{48} = \\dfrac{2}{3} \\)."
},
{
  "content": "Hai cạnh của hình chữ nhật nằm trên hai đường thẳng \\( d_1: 4x-3y+5=0 \\) và \\( d_2: 3x+4y-5=0 \\). Hình chữ nhật có đỉnh \\( A(2;1) \\). Tính diện tích của hình chữ nhật (điền số nguyên).",
  "answers": ["2"],
  "explanation": "Tính độ dài hai cạnh kề của hình chữ nhật.\n\nTa có: \\( \\vec{n_{d_1}} = (4;-3); \\vec{n_{d_2}} = (3;4) \\).\n\nDo \\( A \\) không thuộc hai đường thẳng \\( d_1; d_2 \\) và \\( d_1 \\perp d_2 \\) nên độ dài hai cạnh kề nhau của hình chữ nhật bằng khoảng cách từ \\( A \\) đến hai đường thẳng \\( d_1; d_2 \\).\n\nTa có:\n\n\\( d(A;d_1) = \\dfrac{|4.2-3.1+5|}{\\sqrt{4^2+3^2}} = 2 \\).\n\n\\( d(A;d_2) = \\dfrac{|3.2+4.1-5|}{\\sqrt{3^2+4^2}} = 1 \\).\n\n\\( \\Rightarrow S = d(A;d_1).d(A;d_2) = 2.1 = 2 \\)."
},
{
  "content": "Cho phương trình \\( x^2 - 2m|x| + 9 - m = 0 \\). Tìm \\( m \\) để phương trình có 3 nghiệm phân biệt (điền số nguyên).",
  "answers": ["9"],
  "explanation": "Đặt \\( |x| = t \\; (t \\ge 0) \\). Biện luận số nghiệm của \\( t \\).\n\nĐặt \\( |x| = t \\; (t \\ge 0) \\) thì phương trình (*) trở thành: \\( t^2-2mt+9-m=0 \\) (1)\n\nĐể phương trình (*) có 3 nghiệm phân biệt thì phương trình (1) phải có nghiệm \\( t=0 \\) và một nghiệm \\( t>0 \\).\n\nKhi \\( t=0 \\Rightarrow m=9 \\) thì (1) \\( \\Leftrightarrow t^2-18t=0 \\Rightarrow \\left[\\begin{array}{l} t=18>0 \\; (TM) \\\\ t=0 \\end{array}\\right. \\)\n\nVậy \\( m=9 \\)."
},
            {
  "content": "Cho hàm số \\( f(x) \\) có bảng biến thiên của hàm số \\( y=f'(x) \\) như hình vẽ bên. Có bao nhiêu giá trị nguyên của tham số \\( m\\in(-10;10) \\) để hàm số \\( y=f(3x-1)+x^3-3mx \\) đồng biến trên khoảng \\( (-2;1) \\)? (điền số nguyên).",
  "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de2_cau42_de.PNG",
  "answers": ["6"],
  "explanation": "Để hàm số \\( y=f(3x-1)+x^3-3mx \\) đồng biến trên khoảng \\( (-2;1) \\)\n\n\\( \\Leftrightarrow y' \\ge 0, \\forall x\\in(-2;1) \\)\n\n\\( \\Leftrightarrow 3f'(3x-1)+3x^2-3m \\ge 0, \\forall x\\in(-2;1) \\)\n\n\\( \\Leftrightarrow m \\le f'(3x-1)+x^2, \\forall x\\in(-2;1) \\) (*)\n\nĐặt \\( k(x)=f'(3x-1), h(x)=x^2 \\) và \\( g(x)=f'(3x-1)+x^2=k(x)+h(x) \\).\n\nTa có: \\( \\displaystyle\\min_{(-2;1)}k(x) = k(0)=-4 \\).\n\nDo đó, ta có: \\( \\displaystyle\\min_{(-2;1)}f'(3x-1) = f'(-1)=-4 \\) khi \\( 3x-1=-1 \\Leftrightarrow x=0 \\).\n\n\\( \\Rightarrow \\displaystyle\\min_{(-2;1)}k(x)=k(0)=-4 \\).\n\nDo đó, \\( \\displaystyle\\min_{(-2;1)}g(x)=g(0)=k(0)+h(0)=0-4=-4 \\).\n\nTừ (*) ta có \\( m \\le f'(3x-1)+x^2, \\forall x\\in(-2;1) \\Leftrightarrow m \\le \\displaystyle\\min_{(-2;1)}g(x) \\Leftrightarrow m \\le -4 \\).\n\nMà \\( m\\in(-10;10) \\Rightarrow m\\in\\{-9;\\ldots;-4\\} \\).\n\nVậy có tất cả 6 số nguyên thỏa mãn."
},
{
  "content": "Biết \\( \\displaystyle\\lim_{x\\to 3}\\dfrac{x^2+bx+c}{x-3}=8 \\; (b,c\\in\\mathbb{R}) \\). Giá trị \\( P=b+c \\) bằng bao nhiêu? (điền số nguyên).",
  "answers": ["-13"],
  "explanation": "Nhận dạng giới hạn vô định \\( \\dfrac{0}{0} \\).\n\nVì \\( \\displaystyle\\lim_{x\\to 3}\\dfrac{x^2+bx+c}{x-3}=8 \\) là hữu hạn nên phương trình \\( x^2+bx+c=0 \\) có nghiệm \\( x=3 \\)\n\n\\( \\Leftrightarrow 3b+c+9=0 \\Leftrightarrow c=-9-3b \\)\n\nKhi đó\n\n\\( \\displaystyle\\lim_{x\\to 3}\\dfrac{x^2+bx+c}{x-3} = \\lim_{x\\to 3}\\dfrac{x^2+bx-9-3b}{x-3} = \\lim_{x\\to 3}\\dfrac{(x-3)(x+3+b)}{x-3} \\)\n\n\\( = \\lim_{x\\to 3}(x+3+b) = 8 \\Leftrightarrow 6+b=8 \\Leftrightarrow b=2 \\Rightarrow c=-15 \\)\n\nVậy \\( P=b+c=-13 \\)."
},
          {
  "content": "Một đề kiểm tra trắc nghiệm 45 phút môn Tiếng Anh của lớp 10 là một đề gồm 25 câu hỏi độc lập, mỗi câu hỏi có 4 đáp án trả lời trong đó chỉ có một đáp án đúng. Mỗi câu trả lời đúng được 0,4 điểm, câu trả lời sai không được điểm. Bạn Bình vì học rất kém môn Tiếng Anh nên làm bài bằng cách chọn ngẫu nhiên câu trả lời cho tất cả 25 câu. Gọi A là biến cố \"Bình làm đúng k câu\", biết xác suất của biến cố A đạt giá trị lớn nhất. Tính k (điền số nguyên).",
  "answers": ["6"],
  "explanation": "Vì đề thi có 25 câu và mỗi câu có 4 phương án trả lời nên xác suất để Bình làm đúng \\( k \\) câu là\n\n\\( P = C_{25}^k.\\left(\\dfrac{1}{4}\\right)^k.\\left(\\dfrac{3}{4}\\right)^{25-k} = \\dfrac{C_{25}^k.3^{25-k}}{4^{25}} \\)\n\nvới \\( 0 \\le k \\le 25 \\).\n\nXét hàm \\( f(k) = C_{25}^k.3^{25-k} \\) với \\( k\\in\\mathbb{N} \\) và \\( k\\le 25 \\).\n\nTa có \\( f(k) \\) lớn nhất \\( \\Leftrightarrow \\begin{cases} f(k)\\ge f(k-1) \\\\ f(k)\\ge f(k+1) \\end{cases} \\Leftrightarrow 6,5\\ge k\\ge 5,5 \\Rightarrow k=6 \\).\n\nSuy ra \\( \\displaystyle\\max_{0\\le k\\le 25} f(k) = f(6) \\).\n\nVậy \\( k=6 \\)."
},
          {
  "content": "Giả sử chiều cao (tính bằng cm) của một giống cây trồng (trong vòng một số tháng nhất định) tuân theo quy luật logistic được mô hình hóa bằng hàm số: \\( f(t) = \\dfrac{200}{1+4e^{-t}}, t\\ge 0 \\). Trong đó, thời gian \\( t \\) được tính bằng tháng kể từ khi hạt bắt đầu nảy mầm. Khi đó đạo hàm \\( f'(t) \\) sẽ biểu thị tốc độ tăng chiều cao của giống cây đó. Hỏi sau khi hạt giống bắt đầu nảy mầm thì sau bao nhiêu tháng tốc độ tăng chiều cao của cây là lớn nhất? Kết quả lấy phần nguyên (điền số nguyên).",
  "answers": ["1"],
  "explanation": "Khảo sát hàm số đạo hàm.\n\nTa có:\n\n\\( f(t) = \\dfrac{200}{1+4e^{-t}} \\Rightarrow f'(t) = 200.\\dfrac{4e^{-t}}{(1+4e^{-t})^2} \\)\n\n\\( f''(t) = 200.\\dfrac{-4e^{-t}(1+4e^{-t})^2-2(1+4e^{-t})(-4e^{-t}).4e^{-t}}{(1+4e^{-t})^4} \\)\n\n\\( = 200.\\dfrac{-4e^{-t}(1+4e^{-t})(1+4e^{-t}-8e^{-t})}{(1+4e^{-t})^4} \\)\n\n\\( = 200.\\dfrac{-4e^{-t}(1+4e^{-t})(1-4e^{-t})}{(1+4e^{-t})^4} \\)\n\n\\( f''(t) = 0 \\Leftrightarrow e^{-t}=\\dfrac{1}{4} \\Leftrightarrow t=-\\ln\\dfrac{1}{4}=\\ln 4 \\)\n\nBảng biến thiên:",
  "image_explanation": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_cau22_loigiai.PNG",
  "explanation_2": "Vậy sau khi hạt nảy mầm khoảng \\( \\ln 4 \\approx 1,38 \\) tháng thì cây có tốc độ tăng chiều cao lớn nhất.\n\nLấy phần nguyên ta được đáp số là 1."
},
{
  "content": "Vào năm 2020, dân số của một quốc gia là khoảng 97 triệu người và tốc độ tăng trưởng dân số là 0,91%. Nếu tốc độ tăng trưởng dân số này được giữ nguyên hàng năm, hãy ước tính dân số quốc gia đó vào năm 2030 (lấy phần nguyên, điền số nguyên, đơn vị triệu người).",
  "answers": ["106"],
  "explanation": "Sử dụng số hạng tổng quát cấp số nhân.\n\nDân số hằng năm lập thành cấp số nhân với số hạng đầu là 97 và công bội \\( q=1,0091 \\).\n\nDân số của quốc gia đó năm 2030 tức \\( n=11 \\) là:\n\n\\( u_{11} = 97.1,0091^{10} \\approx 106,197 \\) triệu người.\n\nLấy phần nguyên ta được đáp số là 106."
},
{
  "content": "Cho hai số thực \\( x\\ge 0; 1\\le y\\le 3 \\) thỏa mãn \\( 2^{x-2y}.(2^x+1) = 4^y+2^x+4 \\). Tìm giá trị nhỏ nhất của biểu thức \\( P = 2^{x-y-2}-x-y^2+2037 \\) (nhập đáp án vào ô trống).",
  "answers": ["2025"],
  "explanation": "Giải bất phương trình hàm mũ.\n\nGiả thiết cho \\( 2^{x-2y}.(2^x+1) = 4^y+2^x+4 \\)\n\n\\( \\Leftrightarrow 2^x.(2^x+1) = 2(2^y+x+2).2^{2y} \\Leftrightarrow 2^x.(2^x+1) = 2^{2y+1}(2^y+x+2) \\)\n\n\\( \\Leftrightarrow 2^{2x}.(2^x+1) \\cdot 2^{-x} = 2^{2y+x+1}(2^y+x+1+1) \\)\n\nXét hàm số \\( f(t) = 2^t.(t+1) \\) trên \\( (0;+\\infty) \\); suy ra\n\n\\( f'(t) = 2^t.(t+1)\\ln 2+2^t > 0, \\forall t\\in(0;+\\infty) \\)\n\nVậy hàm số \\( f(t) \\) luôn đồng biến trên \\( (0;+\\infty) \\) nên ta có:\n\n\\( 2^{2x}.(2x+1) = 2^{2y+x+1}(2y+x+1+1) \\Leftrightarrow 2x = 2y+x+1 \\Leftrightarrow x = 2y+1 \\)\n\nSuy ra:\n\n\\( P = 2^{x-y-2}-x-y^2+2037 = 2^{y-1}-\\left(y^2+2y+1\\right)+2037 = \\dfrac{1}{4}.2^{y+1}-(y+1)^2+2037 \\)\n\nXét hàm số \\( g(a) = \\dfrac{1}{4}.2^a-a^2; a\\in[2;4] \\)\n\n\\( g'(a) = \\dfrac{2^a.\\ln 2}{4}-2a \\Rightarrow g''(a) = \\dfrac{2^a.\\ln^2 2}{4}-2 < 0, a\\in[2;4] \\)\n\n\\( \\Rightarrow g'(a) \\) luôn nghịch biến trên \\( [2;4] \\)\n\n\\( \\Rightarrow \\displaystyle\\max_{[2;4]} g'(a) = g'(2) = \\ln 2-4 < 0 \\)\n\n\\( \\Rightarrow g(a) \\) luôn nghịch biến trên \\( [2;4] \\)\n\n\\( \\Rightarrow \\displaystyle\\min_{[2;4]} g(a) = g(4) = -12 \\)\n\nVậy \\( \\min P = -12+2037 = 2025 \\) khi \\( y+1=4 \\Leftrightarrow y=3; x=7 \\).\n\nĐáp án: 2025."
},
{
  "content": "Một đề kiểm tra trắc nghiệm 45 phút môn Tiếng Anh của lớp 10 là một đề gồm 25 câu hỏi độc lập, mỗi câu hỏi có 4 đáp án trả lời trong đó chỉ có một đáp án đúng. Mỗi câu trả lời đúng được 0,4 điểm, câu trả lời sai không được điểm. Bạn Bình vì học rất kém môn Tiếng Anh nên làm bài bằng cách chọn ngẫu nhiên câu trả lời cho tất cả 25 câu. Gọi A là biến cố \"Bình làm đúng k câu\", biết xác suất của biến cố A đạt giá trị lớn nhất. Tính k (điền số nguyên).",
  "answers": ["6"],
  "explanation": "Vì đề thi có 25 câu và mỗi câu có 4 phương án trả lời nên xác suất để Bình làm đúng \\( k \\) câu là\n\n\\( P = C_{25}^k.\\left(\\dfrac{1}{4}\\right)^k.\\left(\\dfrac{3}{4}\\right)^{25-k} = \\dfrac{C_{25}^k.3^{25-k}}{4^{25}} \\)\n\nVới \\( 0 \\le k \\le 25 \\).\n\nXét hàm \\( f(k) = C_{25}^k.3^{25-k} \\) với \\( k\\in\\mathbb{N} \\) và \\( k\\le 25 \\).\n\nTa có \\( f(k) \\) lớn nhất \\( \\Leftrightarrow \\begin{cases} f(k) \\ge f(k-1) \\\\ f(k) \\ge f(k+1) \\end{cases} \\Leftrightarrow 6,5 \\ge k \\ge 5,5 \\Rightarrow k=6 \\).\n\nSuy ra \\( \\displaystyle\\max_{0\\le k\\le 25} f(k) = f(6) \\).\n\nVậy \\( k=6 \\)."
},
        ],
    },

    # ------------------------------------------------------------------
    # ĐỀ 3
    # ------------------------------------------------------------------
    {
        "id": "de3",
        "name": "Đề thi tham khảo số 3 - Đánh giá năng lực học sinh THPT 2026",
        "seed": 2025303,
"mc4": [
  # ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
{
    "content": """Cho hàm số \\( y=f(x) \\) có đạo hàm trên \\( \\mathbb{R} \\) là \\( f'(x)=(x+3)(x-4) \\). Tính tổng các giá trị nguyên của tham số \\( m\\in[-10;5] \\) để hàm số \\( y=f(x^2-3x+m) \\) có nhiều điểm cực trị nhất.""",
    "options": {"A": "13", "B": "15", "C": "17", "D": "19"},
    "correct": "B",
    "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_cau9_loigiai.PNG",
    "points": 1,
    "explanation": """Sử dụng tương giao đồ thị.

Xét hàm số \\( y=f(x^2-3x+m) \\) có

\\( y' = (2x-3).f'(x^2-3x+m) \\)

\\( y'=0 \\Leftrightarrow \\left[\\begin{array}{l} 2x-3=0 \\\\ f'(x^2-3x+m)=0 \\end{array}\\right. \\)

Để hàm số \\( y=f(x^2-3x+m) \\) có nhiều cực trị nhất thì phương trình \\( f'(x^2-3x+m)=0 \\) có nhiều nghiệm bội lẻ khác \\( \\dfrac{3}{2} \\) nhất.

Xét phương trình: \\( f'(x^2-3x+m)=0 \\Leftrightarrow (x^2-3x+m+3)(x^2-3x+m-4)=0 \\)

\\( \\Leftrightarrow \\left[\\begin{array}{l} x^2-3x=-m-3 \\\\ x^2-3x=4-m \\end{array}\\right. \\)

Xét hàm số: \\( h(x)=x^2-3x \\)

\\( h'(x)=2x-3, h'=0 \\Leftrightarrow x=\\dfrac{3}{2} \\)

Bảng biến thiên hàm số \\( h(x)=x^2-3x \\) như trên.

Để \\( f'(x^2-3x+m)=0 \\) có nhiều nghiệm bội lẻ nhất thì hệ phương trình trên có nhiều nghiệm bội lẻ nhất.

Số nghiệm của hai phương trình này là số giao điểm của đồ thị hàm số \\( h(x)=x^2-3x \\) và các đường thẳng \\( y=-m-3 \\) và \\( y=4-m \\).

Dựa vào bảng biến thiên của hàm số \\( h(x)=x^2-3x \\):

\\( \\left\\{\\begin{array}{l} -m-3>-\\dfrac{9}{4} \\\\ 4-m>-\\dfrac{9}{4} \\end{array}\\right. \\Leftrightarrow \\left\\{\\begin{array}{l} m<-\\dfrac{3}{4} \\\\ m<\\dfrac{25}{4} \\end{array}\\right. \\)

Mà \\( m\\in[-10;5] \\), kết hợp các điều kiện \\( m\\in\\left(-\\dfrac{3}{4};5\\right], m\\in\\mathbb{Z} \\Rightarrow m\\in\\{0;1;2;3;4;5\\} \\)

Vậy tổng các giá trị nguyên của m thỏa mãn yêu cầu bài toán là: 15.

Đáp án B.""",
},

# ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
{
    "content": """Có bao nhiêu giá trị nguyên dương của tham số \\( m \\) để phương trình \\( m^2 \\ln\\left(\\dfrac{x}{e}\\right) = (2-m)\\ln x - 4 \\) có nghiệm thuộc vào đoạn \\( \\left[\\dfrac{1}{e};1\\right] \\)?""",
    "options": {"A": "0", "B": "1", "C": "2", "D": "3"},
    "correct": "B",
    "points": 1,
    "explanation": """Ta có: \\( m^2 \\ln\\left(\\dfrac{x}{e}\\right) = (2-m)\\ln x - 4 \\)

\\( \\Leftrightarrow m^2(\\ln x - 1) = (2-m)\\ln x - 4 \\)

\\( \\Leftrightarrow (m^2+m-2)\\ln x = m^2 - 4 \\)  (1)

Với \\( m^2+m-2=0 \\Rightarrow m=1 \\) (do \\( m>0 \\)):

(1) trở thành \\( 0.\\ln x = -3 \\) (Vô lý) nên loại \\( m=1 \\).

Với \\( m \\neq 1 \\), (1) \\( \\Leftrightarrow \\ln x = \\dfrac{m-2}{m-1} \\)  (2)

Hàm số \\( y=\\ln x \\) đồng biến trên \\( \\left[\\dfrac{1}{e};1\\right] \\), suy ra \\( \\ln x \\in [-1;0] \\).

Phương trình (2) có nghiệm thuộc đoạn \\( \\left[\\dfrac{1}{e};1\\right] \\) khi \\( -1 \\le \\dfrac{m-2}{m-1} \\le 0 \\), tức là:

\\( \\dfrac{m-2}{m-1} \\ge -1 \\) và \\( \\dfrac{m-2}{m-1} \\le 0 \\)

Giải điều kiện thứ nhất: \\( \\dfrac{m-2}{m-1} \\ge -1 \\Leftrightarrow m \\ge \\dfrac{3}{2} \\) hoặc \\( m<1 \\)

Giải điều kiện thứ hai: \\( \\dfrac{m-2}{m-1} \\le 0 \\Leftrightarrow 1<m\\le 2 \\)

Kết hợp cả hai điều kiện, ta được \\( \\dfrac{3}{2} \\le m \\le 2 \\).

Suy ra \\( m=2 \\) là giá trị nguyên dương duy nhất thỏa mãn.

Vậy có 1 giá trị nguyên dương của tham số \\( m \\) thỏa mãn yêu cầu bài toán. Đáp án B.""",
},

# ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
{
    "content": """Tìm giá trị của tham số \\( m \\) để hàm số sau liên tục tại \\( x=0 \\):

\\( f(x) = \\left\\{\\begin{array}{ll} \\dfrac{\\sqrt{1-x}-\\sqrt{1+x}}{x}, & x<0 \\\\ m+\\dfrac{1-x}{1+x}, & x\\ge 0 \\end{array}\\right. \\)""",
    "options": {"A": "\\( m=1 \\)", "B": "\\( m=-2 \\)", "C": "\\( m=3 \\)", "D": "\\( m=-4 \\)"},
    "correct": "B",
    "points": 1,
    "explanation": """Ta có:

\\( \\lim_{x\\to 0^+} f(x) = \\lim_{x\\to 0^+}\\left(m+\\dfrac{1-x}{1+x}\\right) = m+1 \\)

\\( \\lim_{x\\to 0^-} f(x) = \\lim_{x\\to 0^-}\\left(\\dfrac{\\sqrt{1-x}-\\sqrt{1+x}}{x}\\right) = \\lim_{x\\to 0^-}\\left(\\dfrac{-2x}{x(\\sqrt{1-x}+\\sqrt{1+x})}\\right) = \\lim_{x\\to 0^-}\\left(\\dfrac{-2}{\\sqrt{1-x}+\\sqrt{1+x}}\\right) = -1 \\)

\\( f(0) = m+1 \\)

\\( f(x) \\) liên tục tại \\( x=0 \\) khi và chỉ khi:

\\( \\lim_{x\\to 0^+} f(x) = \\lim_{x\\to 0^-} f(x) = f(0) \\Leftrightarrow m+1 = -1 \\Leftrightarrow m=-2 \\)

Vậy \\( m=-2 \\). Đáp án B.""",
},

# ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
{
    "content": """Cho dãy số \\( (u_n) \\) biết \\( \\left\\{\\begin{array}{l} u_1 = 1 \\\\ u_n = \\dfrac{1}{3}u_{n-1} + 2 \\end{array}\\right. \\). Mệnh đề nào sau đây đúng?""",
    "options": {
        "A": "\\( (u_n) \\) là dãy số tăng.",
        "B": "\\( (u_n) \\) là dãy số giảm.",
        "C": "\\( (u_n) \\) không là dãy tăng, không là dãy giảm.",
        "D": "\\( u_5 = 2 \\)"
    },
    "correct": "A",
    "points": 1,
    "explanation": """Ta có \\( u_1 < u_2 < u_3 \\), ta dự đoán dãy số đã cho là dãy số tăng.

Ta chứng minh quy nạp:

Theo giả thiết ta thấy \\( u_n > 0, \\forall n \\in \\mathbb{N}^* \\).

Giả sử \\( u_k > u_{k-1} \\ge 2 \\). Ta chứng minh \\( u_{k+1} > u_k \\).

Thật vậy:

\\( u_{k+1} - u_k = \\dfrac{1}{3}(u_k - u_{k-1}) > 0 \\Leftrightarrow u_{k+1} > u_k \\)

Vậy dãy đã cho là dãy tăng. Đáp án A.""",
},

# ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
{
    "content": """Cho tứ diện ABCD. Trên các cạnh AD và BC lần lượt lấy các điểm M, N sao cho \\( \\overrightarrow{AM} = 3\\overrightarrow{MD}, \\overrightarrow{NB} = -3\\overrightarrow{NC} \\). Gọi P, Q lần lượt là trung điểm của AD, BC. Khẳng định nào sau đây sai?""",
    "options": {
        "A": "Các vectơ \\( \\overrightarrow{AB}, \\overrightarrow{DC}, \\overrightarrow{MN} \\) đồng phẳng.",
        "B": "Các vectơ \\( \\overrightarrow{AB}, \\overrightarrow{PQ}, \\overrightarrow{MN} \\) đồng phẳng.",
        "C": "Các vectơ \\( \\overrightarrow{PQ}, \\overrightarrow{DC}, \\overrightarrow{MN} \\) đồng phẳng.",
        "D": "Các vectơ \\( \\overrightarrow{BD}, \\overrightarrow{AC}, \\overrightarrow{MN} \\) đồng phẳng."
    },
    "correct": "D",
    "points": 1,
    "explanation": """Gọi \\( I \\) là trung điểm của BD, K là trọng tâm của tam giác ABD.

Ta có AB, DC, MN song song với mặt phẳng (PIQ) nên vectơ \\( \\overrightarrow{AB}, \\overrightarrow{DC}, \\overrightarrow{MN} \\) đồng phẳng.

AB, MN song song với mặt phẳng (PIQ) nên vectơ \\( \\overrightarrow{AB}, \\overrightarrow{PQ}, \\overrightarrow{MN} \\) đồng phẳng.

DC, MN song song với mặt phẳng (PIQ) nên vectơ \\( \\overrightarrow{PQ}, \\overrightarrow{DC}, \\overrightarrow{MN} \\) đồng phẳng.

Các vectơ \\( \\overrightarrow{BD}, \\overrightarrow{AC}, \\overrightarrow{MN} \\) không đồng phẳng.

Đáp án D.""",
},

# ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
{
    "content": """Một vườn thú ghi lại tuổi thọ (đơn vị: năm) của 20 con khỉ và ghi lại kết quả như sau:

Nhóm chứa tứ phân vị thứ ba là:""",
    "options": {"A": "[10;11)", "B": "[11;12)", "C": "[12;13)", "D": "[14;15)"},
    "correct": "C",
    "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_cau38.PNG",
    "points": 1,
    "explanation": """Ta có \\( n=20 \\).

Khi đó \\( \\dfrac{3}{4}.20 = 15 \\) và \\( 1+3+8 < 15 < 1+3+8+6 \\).

Vậy tứ phân vị thứ ba thuộc nhóm [12;13). Đáp án C.""",
},

# ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
{
    "content": """Cho tứ diện ABCD có \\( AC=AD=BC=BD=a \\) và hai mặt phẳng \\( (ACD), (BCD) \\) vuông góc với nhau. Tính độ dài cạnh CD sao cho hai mặt phẳng \\( (ABC), (ABD) \\) vuông góc với nhau.""",
    "options": {
        "A": "\\( \\dfrac{2}{\\sqrt{3}}a \\)",
        "B": "\\( \\dfrac{1}{\\sqrt{3}}a \\)",
        "C": "\\( \\dfrac{1}{2}a \\)",
        "D": "\\( \\sqrt{3}a \\)"
    },
    "correct": "A",
    "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_cau39.PNG",
    "points": 1,
    "explanation": """Gọi \\( H \\) là trung điểm của CD, suy ra \\( AH \\perp CD \\).

Mà \\( \\left\\{\\begin{array}{l} (ACD) \\perp (BCD) \\\\ (ACD) \\cap (BCD) = CD \\end{array}\\right. \\)

Suy ra \\( AH \\perp (BCD) \\).

Gọi \\( M \\) là trung điểm AB nên \\( CM \\perp AB \\).

Và \\( \\left\\{\\begin{array}{l} (ABC) \\perp (ABD) \\\\ (ABC) \\cap (ABD) = AB \\end{array}\\right. \\Rightarrow CM \\perp DM \\).

\\( \\Delta ABC = \\Delta ABD \\Rightarrow MC = DM \\Rightarrow \\Delta MCD \\) vuông cân tại \\( M \\).

Đặt \\( CD = x \\Rightarrow AH^2 = BH^2 = a^2 - \\dfrac{x^2}{4} \\Leftrightarrow AB^2 = AH^2+BH^2 = 2a^2 - \\dfrac{x^2}{2} \\).

Ta có:

\\( MH = \\dfrac{1}{2}AB = \\dfrac{1}{2}\\sqrt{2a^2-\\dfrac{x^2}{2}} \\)

Mà \\( MH = \\dfrac{\\sqrt{2}}{2}CD \\Leftrightarrow \\sqrt{2a^2-\\dfrac{x^2}{2}}.\\dfrac{1}{2} = \\dfrac{\\sqrt{2}}{2}x \\Leftrightarrow 4a^2=3x^2 \\Leftrightarrow x=\\dfrac{2}{\\sqrt{3}}a \\).

Đáp án A.""",
},



# ---------------- TRẮC NGHIỆM 4 LỰA CHỌN (mc4) ----------------
{
    "content": "Tìm tất cả các giá trị của tham số \\( m \\) để hàm số \\( y=\\dfrac{x^2+m}{x^2-3x+2} \\) có đúng 1 tiệm cận đứng?",
    "options": {
        "A": "\\( m\\in\\{-1;-4\\} \\)",
        "B": "\\( m=-1 \\)",
        "C": "\\( m=-4 \\)",
        "D": "\\( m\\in\\{1;4\\} \\)"
    },
    "correct": "A",
    "points": 1,
    "explanation": "Ta có: \\( y=\\dfrac{x^2+m}{x^2-3x+2}=\\dfrac{x^2+m}{(x-1)(x-2)} \\).\n\nĐồ thị hàm số có đúng một tiệm cận đứng khi tử số triệt tiêu tại đúng một trong hai nghiệm của mẫu, tức là:\n\n\\( \\left[\\begin{array}{l} 1^2+m=0 \\\\ 2^2+m=0 \\end{array}\\right. \\Leftrightarrow \\left[\\begin{array}{l} m=-1 \\\\ m=-4 \\end{array}\\right. \\)\n\nVậy \\( m\\in\\{-1;-4\\} \\).\n\nĐáp án A.",
},

{
    "content": "Một tòa nhà cao 50 m, vào những ngày trời nắng, độ dài bóng của tòa nhà được tính theo công thức \\( S(t) = 50\\cot\\left(\\dfrac{\\pi}{12}t\\right) \\). Trong đó S được tính bằng mét, t là số giờ tính từ 6 giờ sáng. Trong một ngày có bao nhiêu thời điểm bóng có độ dài bằng chiều cao của tòa nhà?",
    "options": {
        "A": "0",
        "B": "1",
        "C": "2",
        "D": "3"
    },
    "correct": "C",
    "points": 1,
    "explanation": "Độ dài bóng của tòa nhà bằng chiều cao của tòa nhà khi:\n\n\\( S(t)=50 \\Leftrightarrow 50\\cot\\left(\\dfrac{\\pi}{12}t\\right)=50 \\Leftrightarrow \\cot\\left(\\dfrac{\\pi}{12}t\\right)=1 \\)\n\n\\( \\Leftrightarrow \\dfrac{\\pi}{12}t=\\dfrac{\\pi}{4}+k\\pi \\Leftrightarrow t=3+12k \\; (k\\in\\mathbb{Z}) \\)\n\nVì \\( 0\\le t\\le 12 \\) nên \\( t=3 \\) hoặc \\( t=9 \\), tức là vào lúc 9 giờ sáng hoặc 3 giờ chiều.\n\nVậy trong ngày có 2 thời điểm bóng của tòa nhà dài bằng chiều cao của nó.\n\nĐáp án C.",
},

{
    "content": "Cho hai biến cố A và B, với \\( P(A)=\\dfrac{3}{8}, P(B)=\\dfrac{1}{2}, P(\\overline{A}\\overline{B})=\\dfrac{1}{5} \\). Giá trị của \\( P(A\\cup B) \\) là?",
    "options": {
        "A": "\\( \\dfrac{3}{40} \\)",
        "B": "\\( \\dfrac{4}{5} \\)",
        "C": "\\( \\dfrac{5}{40} \\)",
        "D": "\\( \\dfrac{3}{5} \\)"
    },
    "correct": "A",
    "points": 1,
    "explanation": "Ta có \\( P(A\\cup B) = 1-P(\\overline{A}\\overline{B}) = 1-\\dfrac{1}{5} = \\dfrac{4}{5} \\).\n\nKhi đó: \\( P(AB) = P(A)+P(B)-P(A\\cup B) = \\dfrac{3}{8}+\\dfrac{1}{2}-\\dfrac{4}{5} = \\dfrac{3}{40} \\).\n\nĐáp án A.",
},

{
    "content": "Trên sườn đồi, với độ dốc 16% (Độ dốc của sườn đồi được tính bằng tan của góc nhọn tạo bởi sườn đồi với phương nằm ngang) có một cây cao thẳng đứng. Ở phía chân đồi, cách gốc cây 30m, người ta nhìn ngọn cây dưới một góc 45° so với phương nằm ngang. Tính chiều cao của cây đó (làm tròn đến hàng đơn vị, theo đơn vị mét).",
    "options": {
        "A": "25m",
        "B": "26m",
        "C": "27m",
        "D": "28m"
    },
    "correct": "B",
    "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/de3_cau29_loigiai.PNG",
    "points": 1,
    "explanation": "Do sườn đồi dốc 16% nên sườn đồi tạo với phương nằm ngang một góc \\( \\widehat{BAD} \\approx 9^\\circ \\).\n\nTừ đó ta có: \\( \\widehat{BAC} = \\widehat{DAC}-\\widehat{DAB} \\approx 36^\\circ \\) và \\( \\widehat{BCA}=45^\\circ \\).\n\nÁp dụng định lí sin trong tam giác ABC, ta được:\n\n\\( BC = \\dfrac{AB}{\\sin\\widehat{BCA}}.\\sin\\widehat{BAC} \\approx 26 \\; (m) \\).\n\nĐáp án B.",
},

{
    "content": "Cho cấp số cộng \\( (u_n) \\) có số hạng đầu \\( u_1 = 10 \\) và công sai \\( d = -3 \\). Giá trị của \\( u_8 \\) bằng",
    "options": {
        "A": "-11",
        "B": "31",
        "C": "11",
        "D": "-8"
    },
    "correct": "A",
    "points": 1,
    "explanation": "Ta có: \\( u_8 = u_1 + 7d = 10 + 7 \\times (-3) = -11 \\).\n\nĐáp án A.",
},

{
    "content": "Cho dãy số liệu: 10, 12, 14, 16, 18. Số trung bình cộng của dãy số liệu trên bằng",
    "options": {
        "A": "13",
        "B": "15",
        "C": "16",
        "D": "14"
    },
    "correct": "D",
    "points": 1,
    "explanation": "Số trung bình cộng là:\n\n\\( \\overline{x} = (10+12+14+16+18):5 = 70:5 = 14 \\).\n\nĐáp án D.",
},

{
    "content": "Một nhóm có 10 học sinh. Hỏi có bao nhiêu cách chọn ra 3 học sinh từ nhóm đó (không phân biệt thứ tự)?",
    "options": {
        "A": "720",
        "B": "30",
        "C": "120",
        "D": "45"
    },
    "correct": "C",
    "points": 1,
    "explanation": "Vì chọn 3 học sinh mà không phân biệt thứ tự nên số cách chọn là một tổ hợp chập 3 của 10:\n\n\\( C_{10}^3 = 120 \\) (cách).\n\nĐáp án C.",
},

{
    "content": "Có bao nhiêu giá trị nguyên dương của tham số \\( m \\) để phương trình \\( m^2\\ln\\left(\\dfrac{x}{e}\\right) = (2-m)\\ln x - 4 \\) có nghiệm thuộc vào đoạn \\( \\left[\\dfrac{1}{e};1\\right] \\)?",
    "options": {
        "A": "0",
        "B": "1",
        "C": "2",
        "D": "3"
    },
    "correct": "B",
    "points": 1,
    "explanation": "Ta có:\n\n\\( m^2\\ln\\left(\\dfrac{x}{e}\\right) = (2-m)\\ln x - 4 \\Leftrightarrow m^2(\\ln x - 1) = (2-m)\\ln x - 4 \\)\n\n\\( \\Leftrightarrow (m^2+m-2)\\ln x = m^2 - 4 \\quad (1) \\)\n\nVới \\( m^2+m-2=0 \\Rightarrow m=1 \\) (do \\( m>0 \\)): khi đó (1) trở thành \\( 0.\\ln x = -3 \\) (vô lí) nên loại \\( m=1 \\).\n\nVới \\( m\\ne 1 \\), (1) \\( \\Leftrightarrow \\ln x = \\dfrac{m-2}{m-1} \\quad (2) \\)\n\nHàm số \\( y=\\ln x \\) đồng biến trên \\( \\left[\\dfrac{1}{e};1\\right] \\), suy ra \\( \\ln x \\in [-1;0] \\).\n\nPhương trình (2) có nghiệm thuộc đoạn \\( \\left[\\dfrac{1}{e};1\\right] \\) khi \\( -1 \\le \\dfrac{m-2}{m-1} \\le 0 \\).\n\nGiải điều kiện thứ nhất: \\( \\dfrac{m-2}{m-1} \\ge -1 \\Leftrightarrow m\\ge \\dfrac{3}{2} \\) hoặc \\( m<1 \\).\n\nGiải điều kiện thứ hai: \\( \\dfrac{m-2}{m-1} \\le 0 \\Leftrightarrow 1<m\\le 2 \\).\n\nKết hợp hai điều kiện, ta được \\( \\dfrac{3}{2}\\le m\\le 2 \\).\n\nVì \\( m \\) nguyên dương nên \\( m=2 \\). Vậy có 1 giá trị nguyên dương của \\( m \\) thỏa mãn.\n\nĐáp án B.",
},

{
    "content": "Cho hình chóp \\( S.ABCD \\) trong đó \\( ABCD \\) là hình chữ nhật, \\( SA \\perp (ABCD) \\). Trong các tam giác sau tam giác nào không phải là tam giác vuông?",
    "options": {
        "A": "\\( \\triangle SBC \\)",
        "B": "\\( \\triangle SCD \\)",
        "C": "\\( \\triangle SAB \\)",
        "D": "\\( \\triangle SBD \\)"
    },
    "correct": "D",
    "points": 1,
    "explanation": "<img src=\"https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau2-de4.PNG\" alt=\"Hình chóp S.ABCD\" style=\"max-width:100%;\"/>\n\n\\( \\triangle SBC \\) vuông tại \\( B \\) do \\( BC \\perp (SAB) \\Rightarrow BC \\perp SB \\).\n\n\\( \\triangle SCD \\) vuông tại \\( C \\) do \\( CD \\perp (SAD) \\Rightarrow CD \\perp SD \\).\n\n\\( \\triangle SAB \\) vuông tại A do \\( SA \\perp AB \\).\n\nVậy tam giác không phải là tam giác vuông là \\( \\triangle SBD \\).",
},
{
    "content": "Cho hình chóp \\( S.ABCD \\) có \\( SA \\perp (ABCD) \\) và đáy là hình vuông. Từ \\( A \\) kẻ \\( AH \\perp SB \\). Khẳng định nào sau đây đúng?",
    "options": {
        "A": "\\( SB \\perp (HAC) \\)",
        "B": "\\( AH \\perp (SAD) \\)",
        "C": "\\( AH \\perp (SBD) \\)",
        "D": "\\( AH \\perp (SBC) \\)"
    },
    "correct": "D",
    "points": 1,
    "explanation": "<img src=\"https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau4-de4.PNG\" alt=\"Hình chóp S.ABCD với H\" style=\"max-width:100%;\"/>\n\nCó \\( \\begin{cases} BC \\perp SA \\\\ BC \\perp AB \\end{cases} \\Rightarrow BC \\perp (SAB) \\), mà \\( AH \\subset (SAB) \\) nên \\( BC \\perp AH \\).\n\nCó \\( \\begin{cases} AH \\perp SB \\\\ AH \\perp BC \\end{cases} \\Rightarrow AH \\perp (SBC) \\).",
},

  {
    "content": "Cho hàm số \\( y = f(x) \\) có bảng biến thiên như sau:Hỏi hàm số đã cho đồng biến trên khoảng nào dưới đây?",
    "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau6-de3.PNG",
    "options": {
        "A": "\\( (-\\infty;1) \\)",
        "B": "\\( (-3;-2) \\)",
        "C": "\\( (-1;1) \\)",
        "D": "\\( (-2;0) \\)"
    },
    "correct": "B",
    "points": 1,
    "explanation": "Từ bảng biến thiên ta có hàm số đồng biến trên \\( (-\\infty;-1) \\) và \\( (1;3) \\).\n\nVì \\( (-3;-2) \\subset (-\\infty;-1) \\) nên hàm số đồng biến trên khoảng \\( (-3;-2) \\).",
},
{
    "content": "Cho 2 số thực dương \\( a, b \\) thỏa mãn \\( a+b = 5ab \\). Khẳng định nào sau đây là khẳng định đúng?",
    "options": {
        "A": "\\( \\log\\dfrac{a+b}{5} = (\\log a + \\log b) \\)",
        "B": "\\( \\log(a+b) = (\\log a + \\log b) \\)",
        "C": "\\( \\log(a+b) = 5(\\log a + \\log b) \\)",
        "D": "\\( \\log\\dfrac{a+b}{5} = (\\log a - \\log b) \\)"
    },
    "correct": "A",
    "points": 1,
    "explanation": "Từ \\( a+b = 5ab \\Rightarrow \\log(a+b) = \\log 5 + \\log a + \\log b \\Rightarrow \\log\\dfrac{a+b}{5} = \\log a + \\log b \\).\n\nSuy ra phương án đúng là \\( \\log\\dfrac{a+b}{5} = (\\log a + \\log b) \\).",
},
{
    "content": "Tìm số hạng chứa \\( x^{31} \\) trong khai triển \\( \\left(x + \\dfrac{1}{x^2}\\right)^{40} \\).",
    "options": {
        "A": "\\( -C_{40}^{37}x^{31} \\)",
        "B": "\\( C_{40}^{37}x^{31} \\)",
        "C": "\\( C_{40}^{2}x^{31} \\)",
        "D": "\\( C_{40}^{4}x^{31} \\)"
    },
    "correct": "B",
    "points": 1,
    "explanation": "Theo khai triển nhị thức Newton, ta có:\n\n\\( \\left(x + \\dfrac{1}{x^2}\\right)^{40} = \\sum_{k=0}^{40} C_{40}^{k}.x^{40-k}.\\left(\\dfrac{1}{x^2}\\right)^{k} = \\sum_{k=0}^{40} C_{40}^{k}.x^{40-3k} \\).\n\nHệ số của \\( x^{31} \\) ứng với \\( 40 - 3k = 31 \\Leftrightarrow k = 3 \\) → số hạng cần tìm là \\( C_{40}^{37}x^{31} \\).",
},

{
    "content": "Rút ngẫu nhiên một lá bài từ bộ bài tú lơ khơ 52 lá. Tính xác suất để rút được lá bài có chất rô hoặc lá bài 10.",
    "options": {
        "A": "\\( \\dfrac{1}{4} \\)",
        "B": "\\( \\dfrac{4}{13} \\)",
        "C": "\\( \\dfrac{9}{26} \\)",
        "D": "\\( \\dfrac{17}{52} \\)"
    },
    "correct": "B",
    "points": 1,
    "explanation": "Số phần tử không gian mẫu \\( n(\\Omega) = 52 \\).\n\nGọi \\( A \\) là biến cố \"rút được lá bài có chất rô\", \\( n(A) = \\dfrac{52}{4} = 13 \\).\n\nGọi \\( B \\) là biến cố \"rút được lá bài 10\", \\( n(B) = 4 \\).\n\nCó duy nhất một lá bài vừa có chất rô và là lá bài 10, do đó \\( n(A \\cap B) = 1 \\).\n\n\\( P(A \\cup B) = P(A) + P(B) - P(A \\cap B) = \\dfrac{13}{52} + \\dfrac{4}{52} - \\dfrac{1}{52} = \\dfrac{4}{13} \\).",
},
{
    "content": "Trong các hệ thức sau, hệ thức nào không đúng?",
    "options": {
        "A": "\\( \\cos^4\\alpha - \\sin^4\\alpha = \\cos^2\\alpha - \\sin^2\\alpha \\)",
        "B": "\\( \\cos^4\\alpha + \\sin^4\\alpha = 1 \\)",
        "C": "\\( (\\sin\\alpha + \\cos\\alpha)^2 = 1 + 2\\sin\\alpha\\cos\\alpha \\)",
        "D": "\\( (\\sin\\alpha - \\cos\\alpha)^2 = 1 - 2\\sin\\alpha\\cos\\alpha \\)"
    },
    "correct": "B",
    "points": 1,
    "explanation": "Sử dụng máy tính bỏ túi thử với \\( \\alpha = \\dfrac{\\pi}{6} \\) ta có \\( \\cos^4\\dfrac{\\pi}{6} + \\sin^4\\dfrac{\\pi}{6} = \\dfrac{5}{8} \\neq 1 \\).\n\nVậy hệ thức không đúng là \\( \\cos^4\\alpha + \\sin^4\\alpha = 1 \\).",
},
{
    "content": "Có bao nhiêu giá trị nguyên dương của tham số \\( m \\) để hàm số \\( y = \\dfrac{8}{3}x^3 + 2\\ln x - mx \\) đồng biến trên \\( (0;1) \\)?",
    "options": {
        "A": "5",
        "B": "6",
        "C": "10",
        "D": "Vô số"
    },
    "correct": "B",
    "points": 1,
    "explanation": "<img src=\"https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau14-de4.PNG\" alt=\"TXĐ \\( D = \\mathbb{R}^{+} \\)>.\n\nTa có \\( y' = 8x^2 + \\dfrac{2}{x} - m \\). Yêu cầu bài toán \\( \\Leftrightarrow y' \\geq 0 \\ \\forall x \\in (0;1) \\)\n\n\\( \\Leftrightarrow 8x^2 + \\dfrac{2}{x} - m \\geq 0 \\ \\forall x \\in (0;1) \\Leftrightarrow h(x) = 8x^2 + \\dfrac{2}{x} \\geq m \\ \\forall x \\in (0;1) \\Leftrightarrow m \\leq \\min_{(0;1)} h(x) \\).\n\nXét hàm \\( h(x) = 8x^2 + \\dfrac{2}{x} \\ \\forall x \\in (0;1) \\). Ta có \\( h'(x) = 16x - \\dfrac{2}{x^2} \\Rightarrow h'(x) = 0 \\Rightarrow x = \\dfrac{1}{2} \\).\n\nLập bảng biến thiên ta được \\( h\\left(\\dfrac{1}{2}\\right) = 6 \\) là giá trị nhỏ nhất trên \\( (0;1) \\).\n\nTừ đó suy ra \\( m \\leq 6 \\), kết hợp với \\( m \\) nguyên dương ta được \\( m \\in \\{1;2;3;4;5;6\\} \\).",
},
{
    "content": "Tìm hệ số của \\( x^9 \\) trong khai triển \\( P(x) = x(1-2x^4)^5 + x^3(1+x^2)^5 \\).",
    "options": {
        "A": "5",
        "B": "10",
        "C": "50",
        "D": "45"
    },
    "correct": "C",
    "points": 1,
    "explanation": "Để tìm hệ số của \\( x^9 \\) trong khai triển \\( P(x) \\), ta cần tìm hệ số của \\( x^8 \\) trong khai triển \\( (1-2x^4)^5 \\) và hệ số của \\( x^6 \\) trong khai triển \\( (1+x^2)^5 \\).\n\nTa có:\n\n\\( (1-2x^4)^5 = 1 - 10x^4 + 40x^8 - 80x^{12} + 80x^{16} - 32x^{20} \\).\n\n\\( (1+x^2)^5 = 1 + 5x^2 + 10x^4 + 10x^6 + 5x^8 + x^{10} \\).\n\nSuy ra \\( P(x) = \\ldots + x.40x^8 + \\ldots + x^3.10x^6 = \\ldots + 50x^9 + \\ldots \\).\n\nVậy hệ số của \\( x^9 \\) trong khai triển \\( P(x) \\) là 50.",
},  

  
],

# ---------------- TRẢ LỜI NGẮN (short) ----------------
"short": [
   

    {
        "content": "Một cửa hàng có 400 sản phẩm, trong đó 10% là hàng lỗi. Hỏi có bao nhiêu sản phẩm lỗi? (chỉ điền số)",
        "answers": ["40"],
        "points": 1,
        "explanation": "Số sản phẩm lỗi là:\n\n\\( 400 \\times 10\\% = 40 \\) (sản phẩm).",
    },


  {
    "content": "Cho hai số thực \\( x \\geq 0 \\); \\( 1 \\leq y \\leq 3 \\) thỏa mãn \\( 2^{x-2y}(2x+1) = 4y + 2x + 4 \\). Tìm giá trị nhỏ nhất của biểu thức \\( P = 2^{x-y-2} - x - y^2 + 2037 \\) (điền đáp án vào ô trống).",
    "answers": ["2025"],
    "points": 1,
    "explanation": "Từ giả thiết ta có:\n\n\\( 2^x(2x+1) = 2(2y+x+2)2^{2y} \\Leftrightarrow 2^{2x}(2x+1) = 2^{2y+x+1}(2y+x+1+1) \\).\n\nXét hàm số \\( f(t) = 2^t(t+1) \\) trên \\( (0;+\\infty) \\), có \\( f'(t) = 2^t(t+1)\\ln 2 + 2^t > 0 \\) nên \\( f(t) \\) đồng biến.\n\nSuy ra \\( 2x = 2y + x + 1 \\Leftrightarrow x = 2y + 1 \\).\n\nThay vào P:\n\n\\( P = 2^{x-y-2} - x - y^2 + 2037 = 2^{y-1} - (y^2+2y+1) + 2037 = \\dfrac{1}{4}.2^{y+1} - (y+1)^2 + 2037 \\).\n\nXét \\( g(a) = \\dfrac{1}{4}.2^a - a^2 \\) với \\( a = y+1 \\in [2;4] \\).\n\nTa có \\( g'(a) = \\dfrac{2^a\\ln 2}{4} - 2a \\), và \\( g''(a) = \\dfrac{2^a\\ln^2 2}{4} - 2 < 0 \\) trên \\([2;4]\\) nên \\( g'(a) \\) nghịch biến, mà \\( \\max g'(a) = g'(2) = \\ln 2 - 4 < 0 \\Rightarrow g'(a) < 0 \\) trên \\([2;4]\\).\n\nVậy \\( g(a) \\) nghịch biến trên \\([2;4] \\Rightarrow \\min g(a) = g(4) = -12 \\).\n\nVậy \\( \\min P = -12 + 2037 = 2025 \\), đạt được khi \\( y+1 = 4 \\Rightarrow y = 3; x = 7 \\).",
},
{
    "content": "Tìm số nguyên dương \\( n \\) bé nhất sao cho trong khai triển \\( (x+1)^n \\) có hai hệ số liên tiếp nhau có tỷ số là \\( \\dfrac{7}{15} \\) (điền đáp án vào ô trống).",
    "answers": ["21"],
    "points": 1,
    "explanation": "Ta có \\( (1+x)^n = C_n^0 + C_n^1x + C_n^2x^2 + \\ldots + C_n^{n-1}x^{n-1} + C_n^nx^n \\).\n\nSố hạng thứ \\( k \\) và \\( k+1 \\) theo khai triển trên có hệ số là \\( C_n^{k-1}, C_n^k \\) với \\( 1 \\leq k \\leq n \\).\n\nTheo giả thiết:\n\n\\( \\dfrac{C_n^{k-1}}{C_n^k} = \\dfrac{7}{15} \\Leftrightarrow \\dfrac{k}{n-k+1} = \\dfrac{7}{15} \\Leftrightarrow 15k = 7(n-k+1) \\Leftrightarrow 22k = 7(n+1) \\).\n\nDo \\( \\gcd(22,7) = 1 \\) nên \\( n+1 \\) chia hết cho 22. Vậy \\( n = 22m - 1, m \\in \\mathbb{N} \\).\n\nVậy số nguyên dương \\( n \\) bé nhất thỏa mãn đề bài là \\( n = 21 \\).",
},
{
    "content": "Cho 8 bạn học sinh A, B, C, D, E, F, G, H. Hỏi có bao nhiêu cách xếp 8 bạn đó ngồi quanh một bàn tròn có 8 chiếc ghế?",
    "answers": ["5040"],
    "points": 1,
    "explanation": "Ta chọn cố định vị trí của bạn A (để loại bỏ các cách xếp trùng nhau do xoay vòng), sau đó xếp 7 bạn còn lại vào 7 vị trí còn lại, ta có \\( 7! \\) cách.\n\nVậy số cách xếp là \\( 7! = 5040 \\).",
},

  {
    "content": "Có bao nhiêu số nguyên \\( x \\) sao cho tồn tại số thực \\( y \\) thỏa mãn \\( \\log_3(x+y) = \\log_4(x^2+y^2) \\) (điền đáp án vào ô trống).",
    "answers": ["2"],
    "points": 1,
    "explanation": "Đặt \\( t = \\log_3(x+y) = \\log_4(x^2+y^2) \\Rightarrow \\begin{cases} x+y = 3^t \\\\ x^2+y^2 = 4^t \\end{cases} \\).\n\nÁp dụng bất đẳng thức Cauchy: \\( 9^t = (x+y)^2 \\leq 2(x^2+y^2) = 2.4^t \\Rightarrow \\left(\\dfrac{9}{4}\\right)^t \\leq 2 \\Rightarrow t \\leq \\log_{9/4}2 \\).\n\nKhi đó \\( x^2+y^2 = 4^t \\leq 4^{\\log_{9/4}2} \\approx 1{,}89 \\Rightarrow x \\in \\{-1;0;1\\} \\).\n\n• Trường hợp \\( x=0 \\): \\( \\begin{cases} y=3^t \\\\ y^2=4^t \\end{cases} \\Rightarrow \\begin{cases} t=0 \\\\ y=1 \\end{cases} \\) (thỏa mãn).\n\n• Trường hợp \\( x=1 \\): \\( \\begin{cases} y=3^t-1 \\\\ y^2=4^t-1 \\end{cases} \\Rightarrow \\begin{cases} t=0 \\\\ y=0 \\end{cases} \\) (thỏa mãn).\n\n• Trường hợp \\( x=-1 \\): \\( \\begin{cases} y=3^t+1 \\\\ y^2+1=4^t \\geq 1 \\end{cases} \\Rightarrow t \\geq 0 \\Rightarrow x^2+y^2 \\geq 5 \\), mâu thuẫn với \\( x^2+y^2 \\leq 4^{\\log_{9/4}2} \\approx 1{,}89 \\) (loại).\n\nVậy có hai giá trị \\( x \\in \\{0;1\\} \\).",
},
{
    "content": "Anh An mua ô tô trả góp trị giá 400 triệu với lãi suất 1,2% một tháng. Hỏi hàng tháng anh An phải trả bao nhiêu triệu để sau 4 năm thì hết nợ (làm tròn đến hàng đơn vị)?",
    "answers": ["11"],
    "points": 1,
    "explanation": "Dùng công thức vay trả góp \\( T = \\dfrac{M.a.(1+a)^n}{(1+a)^n - 1} \\), trong đó \\( T \\) là số tiền trả hàng tháng, \\( M \\) là số tiền vay ban đầu, \\( a \\) là lãi suất mỗi tháng, \\( n \\) là số tháng vay.\n\nTa có \\( n = 4 \\times 12 = 48 \\) tháng, \\( a = 0{,}012 \\), \\( M = 400 \\).\n\n\\( T = \\dfrac{400.0{,}012.1{,}012^{48}}{1{,}012^{48} - 1} \\approx 11 \\).\n\nVậy mỗi tháng anh An phải trả khoảng 11 triệu.",
},
{
    "content": "Trên bàn cờ 6x7 như hình vẽ, người chơi chỉ được di chuyển quân cờ theo các cạnh của hình vuông, mỗi bước đi được một cạnh. Có bao nhiêu cách di chuyển quân cờ từ điểm A đến điểm B bằng 13 bước? (điền đáp án vào ô trống).",
    "image": "https://raw.githubusercontent.com/hdt3k201-hash/web-thi-thu-toan-thpt/main/images/cau40-de3.PNG",
    "answers": ["1716"],
    "points": 1,
    "explanation": "Để di chuyển từ điểm A đến điểm B cần phải đi ít nhất 13 bước. Vì vậy, để đi từ A đến B bằng 13 bước, ta phải đi 7 bước trên các cạnh nằm ngang và 6 bước trên các cạnh đứng, tức là chỉ được di chuyển lên trên hoặc sang phải.\n\nKí hiệu các bước đi lên là L, mỗi bước sang phải là P. Khi đó, mỗi đường đi từ A đến B là một chuỗi 13 kí tự gồm 6 chữ L và 7 chữ P.\n\nVậy số cách di chuyển là \\( C_{13}^6 = C_{13}^7 = 1716 \\).",
},
  
    ],
    },
  ]


def build_exam(exam_def):
    """Ghép câu trắc nghiệm + điền đáp án của 1 đề (viết tay ở EXAM_DEFS),
    gán id/số thứ tự theo ĐÚNG thứ tự khai báo trong EXAM_DEFS.
    KHÔNG xáo trộn ở đây nữa — việc xáo trộn được làm riêng cho mỗi lượt
    làm bài (xem get_shuffled_exam) để mỗi lần vào lại có thứ tự khác."""
    exam_id = exam_def["id"]

    questions = []
    for q in exam_def["mc4"]:
        q2 = dict(q)
        q2["type"] = "mc4"
        questions.append(q2)
    for q in exam_def["short"]:
        q2 = dict(q)
        q2["type"] = "short"
        questions.append(q2)

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


def get_shuffled_exam(exam_id, order):
    """Trả về đề thi với các câu hỏi được sắp lại đúng theo `order`
    (danh sách chỉ số câu hỏi gốc, đã xáo ngẫu nhiên lúc bắt đầu làm bài),
    gán lại id/number theo vị trí hiển thị thực tế."""
    base = get_exam_by_id(exam_id)
    if not base:
        return None
    base_questions = base["questions"]
    questions = []
    for pos, orig_idx in enumerate(order, start=1):
        q = dict(base_questions[orig_idx])
        q["id"] = f"{exam_id}_q{pos:02d}"
        q["number"] = pos
        questions.append(q)
    return {
        "id": base["id"], "name": base["name"],
        "description": base["description"], "questions": questions,
    }




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
.loi-giai-box{
  white-space:pre-line;      /* tôn trọng \n trong text -> xuống dòng đúng chỗ */
  line-height:1.6;
}
.loi-giai-box p{margin:0 0 8px;}
.q-content{white-space:pre-line;}   /* để content_2 / content nhiều dòng cũng đẹp */
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
          {% if q.content_2 %}<div style="margin-top:6px;">{{ q.content_2|safe }}</div>{% endif %}
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
        {% if q.content_2 %}<div style="margin-top:6px;">{{ q.content_2|safe }}</div>{% endif %}
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

       <div class="loi-giai-box" style="background:#fff8e6;border-left:4px solid #f0ad4e;padding:10px 14px;border-radius:8px;font-size:.9rem;margin-top:10px;">
       <strong>Lời giải:</strong><br>{{ q.explanation|safe }}
       {% if q.image_explanation %}
       <div style="text-align:center;margin:10px 0;">
       <img src="{{ q.image_explanation }}" alt="Hình minh họa lời giải câu {{ q.number }}" style="max-width:100%;border-radius:8px;">
       </div>
       {% endif %}
       {% if q.explanation_2 %}<div style="margin-top:8px;">{{ q.explanation_2|safe }}</div>{% endif %}
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

    order = list(range(len(exam["questions"])))
    random.shuffle(order)   # xáo NGẪU NHIÊN THẬT, mỗi lần bắt đầu đều khác

    session["attempt"] = {
        "attempt_id": uuid.uuid4().hex[:10],
        "exam_id": exam_id,
        "question_order": order,
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
    exam = get_shuffled_exam(attempt["exam_id"], attempt["question_order"])
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
    exam = get_shuffled_exam(attempt["exam_id"], attempt["question_order"])
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
    exam = get_shuffled_exam(attempt["exam_id"], attempt["question_order"])
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
    exam = get_shuffled_exam(attempt["exam_id"], attempt["question_order"])
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
