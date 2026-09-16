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
        "name": "Đề thi tham khảo số 1 - Đánh giá năng lực học sinh THPT 2025",
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
