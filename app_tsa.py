from datetime import datetime, timedelta
import time
import streamlit as st
import streamlit.components.v1 as components  # Sử dụng module chuẩn để chạy JS

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Hệ Thống Thi Thử TSA Bách Khoa", page_icon="🦅", layout="wide"
)

# 2. GIAO DIỆN KHUNG VIỀN ĐỎ TRỰC QUAN (CUSTOM CSS)
st.markdown(
    """
<style>
    /* Header chính - Đã thu nhỏ khung và cỡ chữ */
    .tsa-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
        color: white;
        padding: 12px 15px !important;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 3px 6px rgba(183, 28, 28, 0.25);
    }
    .tsa-header h1 {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding-bottom: 4px !important;
        color: white !important;
        line-height: 1.3 !important;
    }
    .tsa-header h3 {
        font-size: 1.0rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
        color: #ffcdd2 !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #d32f2f !important;
        border-radius: 10px !important;
        background-color: #fffbfb !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05) !important;
    }
    .question-title {
        color: #b71c1c;
        font-weight: bold;
        font-size: 1.15em;
        margin-bottom: 12px;
        border-bottom: 1.5px dashed #ef9a9a;
        padding-bottom: 8px;
    }
    .tag-badge {
        background-color: #ffebee;
        color: #c62828;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85em;
        font-weight: bold;
        border: 1px solid #ef9a9a;
        margin-right: 8px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 3. KHỞI TẠO SESSION STATE
if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# 4. THANH BÊN (SIDEBAR): CHỌN ĐỀ THI & ĐỒNG HỒ ĐẾM NGƯỢC
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Logo_HUST.png/1200px-Logo_HUST.png",
    width=120,
)
st.sidebar.title("THI THỬ TSA ONLINE")

# Danh sách đề thi
selected_exam = st.sidebar.selectbox(
    "📋 Chọn Đề Thi TSA:",
    [
        "Đề TSA số 01: Chuyên đề Lượng giác ",
        "Đề TSA số 02: Hàm số & Mô hình Toán thực tế",
        "Đề TSA số 03: Xác suất & Phân tích số liệu",
    ],
)

# --- XỬ LÝ RESET KHI NGƯỜI DÙNG ĐỔI ĐỀ THI ---
if "current_exam" not in st.session_state:
    st.session_state.current_exam = selected_exam

EXAM_DURATION_MINUTES = 60

# Nếu chọn đề khác với đề hiện tại -> Reset bài làm và đồng hồ
if selected_exam != st.session_state.current_exam:
    st.session_state.current_exam = selected_exam
    st.session_state.exam_submitted = False
    st.session_state.end_time_tsa = time.time() + (EXAM_DURATION_MINUTES * 60)
    st.rerun()

st.sidebar.markdown("---")

# --- ĐỒNG HỒ ĐẾM NGƯỢC DÙNG COMPONENTS ---
if "end_time_tsa" not in st.session_state:
    st.session_state.end_time_tsa = time.time() + (EXAM_DURATION_MINUTES * 60)

remaining_sec = max(0, int(st.session_state.end_time_tsa - time.time()))
init_mins, init_secs = divmod(remaining_sec, 60)
init_time_str = f"{init_mins:02d}:{init_secs:02d}"
end_timestamp_ms = int(st.session_state.end_time_tsa * 1000)

with st.sidebar:
    components.html(
        f"""
    <div style="background-color: #b71c1c; color: white; padding: 12px; border-radius: 10px; text-align: center; font-family: 'Source Sans Pro', sans-serif; box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin: 2px;">
        <div style="font-size: 15px; font-weight: bold; margin-bottom: 4px;">⏱️ Thời gian còn lại:</div>
        <div id="tsa-countdown" style="font-size: 26px; font-weight: bold; letter-spacing: 2px;">{init_time_str}</div>
    </div>

    <script>
    (function() {{
        const targetTime = {end_timestamp_ms};
        const timerElement = document.getElementById("tsa-countdown");

        function updateClock() {{
            if (!timerElement) return;
            const now = new Date().getTime();
            const remainingMs = targetTime - now;

            if (remainingMs <= 0) {{
                timerElement.innerHTML = "00:00";
                timerElement.style.color = "#ffcdd2";
                return;
            }}

            const totalSeconds = Math.floor(remainingMs / 1000);
            const m = Math.floor(totalSeconds / 60);
            const s = totalSeconds % 60;

            const formattedM = m < 10 ? "0" + m : m;
            const formattedS = s < 10 ? "0" + s : s;

            timerElement.innerHTML = formattedM + ":" + formattedS;
        }}
        setInterval(updateClock, 1000);
    }})();
    </script>
    """,
        height=100,
    )

# Nút Làm lại bài thi
if st.sidebar.button("🔄 Làm lại bài thi", type="secondary"):
    st.session_state.end_time_tsa = time.time() + (EXAM_DURATION_MINUTES * 60)
    st.session_state.exam_submitted = False
    st.rerun()


# 5. TIÊU ĐỀ CHÍNH BÀI THI (TỰ ĐỘNG CẬP NHẬT THEO SIDEBAR)
exam_parts = selected_exam.split(": ")
exam_name = exam_parts[0].upper()  # VD: ĐỀ TSA SỐ 01
exam_topic = (
    f"CHUYÊN ĐỀ: {exam_parts[1].upper()}"
    if len(exam_parts) > 1
    else "ĐÁNH GIÁ TƯ DUY TOÁN HỌC"
)

st.markdown(
    f"""
<div class="tsa-header">
    <h1>KỲ THI ĐÁNH GIÁ TƯ DUY (TSA) - {exam_name}</h1>
    <h3>{exam_topic}</h3>
</div>
""",
    unsafe_allow_html=True,
)


# =====================================================================
# 6. GIAO DIỆN LÀM BÀI VÀ CHẤM ĐIỂM (PHÂN THEO ĐỀ)
# =====================================================================

# ------------------------- ĐỀ TSA SỐ 01 -------------------------
if "Đề TSA số 01" in selected_exam:
    if not st.session_state.exam_submitted:
        with st.form("tsa_exam_form_1"):
            
            # ================= CÂU 1 =================
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="question-title">
                        <b>Câu 1:</b> <span class="tag-badge">[Kéo thả / Chọn phương án]</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Một vòng quay Mặt Trời (Ferris wheel) có bán kính **50 m**. Tâm của vòng quay nằm ở độ cao **60 m** so với mặt đất. Vòng quay quay đều, mất **15** phút để hoàn thành một vòng. Giả sử tại thời điểm **t = 0** (phút), một cabin bắt đầu chuyển động từ vị trí thấp nhất của vòng quay. Độ cao của cabin so với mặt đất (tính bằng mét) theo thời gian t được mô hình hóa bởi hàm số:[cite: 2]

$$h(t) = A\cos(\omega t) + B \quad (A < 0)$$
"""
                )
                st.markdown(
                    """
                    <div style="background-color: #f8f9fa; border: 1.5px solid #dcdfe6; border-radius: 8px; padding: 12px 16px; margin: 12px 0;">
                        <div style="font-weight: bold; color: #1e88e5; margin-bottom: 8px; font-size: 14px;">🎯 KHUNG PHƯƠNG ÁN LỰA CHỌN:</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">-50</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">50</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">60</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">85</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">2π/15</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""**Hãy điền vào các vị trí còn thiếu:**
* Giá trị $A =$ **`[ (1) ]`** &nbsp;&nbsp;|&nbsp;&nbsp; Tần số góc $\omega =$ **`[ (2) ]`** &nbsp;&nbsp;|&nbsp;&nbsp; Giá trị $B =$ **`[ (3) ]`**
"""
                )
                col1, col2, col3 = st.columns(3)
                with col1:
                    q1_val_A = st.selectbox(
                        "📌 (1) Chọn giá trị A:",
                        ["-- Chọn --", "-50", "50", "60", "85"],
                        key="q1_a",
                    )
                with col2:
                    q1_val_w = st.selectbox(
                        "📌 (2) Chọn ω:",
                        ["-- Chọn --", "2π/15", "π/15", "15/2π"],
                        key="q1_w",
                    )
                with col3:
                    q1_val_B = st.selectbox(
                        "📌 (3) Chọn giá trị B:",
                        ["-- Chọn --", "50", "60", "85"],
                        key="q1_b",
                    )

            # ================= CÂU 2 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 2:</b> <span class="tag-badge">[Trắc nghiệm 4 lựa chọn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Cho hàm số lượng giác $y = a\sin(bx+c) + d$ có đồ thị như hình vẽ bên dưới. Biết $a > 0$, $b > 0$ và $c \in (-\pi; 0)$. Tính giá trị của biểu thức $P = a + b + c + d$."""
                )
                
                # CHÈN LỆNH HÌNH VẼ THEO YÊU CẦU
                try:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image("images/de1_tsa_cau2.PNG", width=400)
                except: 
                    st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau1_p1.png")
                
                q2_ans = st.radio(
                    "Chọn phương án đúng:",
                    [
                        r"A. $P = 6 - \dfrac{\pi}{3}$",
                        r"B. $P = 4 + \dfrac{\pi}{3}$",
                        r"C. $P = 5 - \dfrac{\pi}{6}$",
                        r"D. $P = 3 + \dfrac{\pi}{2}$",
                    ],
                    key="q2",
                    index=None,
                )

            # ================= CÂU 3 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 3:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Mực nước tại một cảng biển được mô hình hóa bởi hàm số $h(t) = 3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12$ (mét), trong đó t là thời gian tính bằng giờ ($0 \le t \le 24$). Một tàu hàng yêu cầu mực nước tối thiểu là **13,5 m** để có thể cập cảng an toàn. Trong một ngày (24 giờ), tổng thời gian tàu có thể cập cảng an toàn là bao nhiêu giờ?"""
                )
                q3_ans = st.text_input("Nhập kết quả dạng số (Ví dụ: 8):", key="q3")

            # ================= CÂU 4 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 4:</b> <span class="tag-badge">[Đúng/Sai]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(r"""Cho phương trình lượng giác: $2\cos^2 x - (2m+1)\cos x + m = 0 \quad (1)$. Xét tính đúng/sai của các mệnh đề sau:""")
                q4_a = st.radio(
                    r"a) Phương trình (1) có thể phân tích thành nhân tử dạng $(\cos x - m)(2\cos x - 1) = 0$.",
                    ["Đúng", "Sai"],
                    key="q4_1",
                    horizontal=True,
                    index=None
                )
                q4_b = st.radio(
                    r"b) Khi $m = 1$, phương trình có đúng **2** nghiệm phân biệt trên đoạn $[0; 2\pi]$.",
                    ["Đúng", "Sai"],
                    key="q4_2",
                    horizontal=True,
                    index=None
                )
                q4_c = st.radio(
                    r"c) Để phương trình có đúng **3** nghiệm phân biệt trên đoạn $[0; 2\pi]$ thì $m = -1$.",
                    ["Đúng", "Sai"],
                    key="q4_3",
                    horizontal=True,
                    index=None
                )
                q4_d = st.radio(
                    r"d) Có tồn tại giá trị thực của m để phương trình đã cho hoàn toàn vô nghiệm.",
                    ["Đúng", "Sai"],
                    key="q4_4",
                    horizontal=True,
                    index=None
                )

            # ================= CÂU 5 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 5:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Mực nước tại một cảng biển được mô hình hóa bởi hàm số $h(t) = 3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12$ (mét), trong đó t là thời gian tính bằng giờ $(0 \le t \le 24)$.
                    Một tàu hàng yêu cầu mực nước tối thiểu là 13.5m để có thể cập cảng an toàn.
                    Trong một ngày (24 giờ), tổng thời gian tàu có thể cập cảng an toàn là bao nhiêu giờ?"""
                )
                q5_ans = st.text_input("Nhập kết quả dạng số (Ví dụ: 8):", key="q5")

            # ================= CÂU 6 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 6:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Tìm giá trị nhỏ nhất của hàm số $y = 3\sin x + 4\cos x + 5$."""
                )
                q6_ans = st.text_input("Nhập kết quả dạng số:", key="q6")

            # ================= CÂU 7 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 7:</b> <span class="tag-badge">[Đúng/Sai]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Một con lắc lò xo dao động điều hòa với phương trình li độ $x(t) = 5\cos\left(4\pi t - \dfrac{\pi}{2}\right)$ (cm), trong đó t tính bằng giây.
                    Vận tốc của vật là đạo hàm của li độ theo thời gian $v(t) = x^{\prime}(t)$.
                    Xét tính đúng/sai của các mệnh đề sau:"""
                )
                q7_a = st.radio(
                    r"A. Chu kì dao động toàn phần của con lắc lò xo là $T = 0,5$ giây.",
                    ["Đúng", "Sai"],
                    key="q7_1",
                    horizontal=True,
                    index=None
                )
                q7_b = st.radio(
                    r"B. Tại thời điểm ban đầu $t = 0$, vật chuyển động đi qua vị trí cân bằng theo chiều âm.",
                    ["Đúng", "Sai"],
                    key="q7_2",
                    horizontal=True,
                    index=None
                )
                q7_c = st.radio(
                    r"C. Vận tốc đạt giá trị lớn nhất của vật trong suốt quá trình dao động là $20\pi$ (cm/s).",
                    ["Đúng", "Sai"],
                    key="q7_3",
                    horizontal=True,
                    index=None
                )
                q7_d = st.radio(
                    r"D. Thời gian ngắn nhất để vật di chuyển từ vị trí cân bằng ra đến biên dương cực đại là 0,25 giây.",
                    ["Đúng", "Sai"],
                    key="q7_4",
                    horizontal=True,
                    index=None
                )

            # ================= CÂU 8 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 8:</b> <span class="tag-badge">[Trắc nghiệm 4 lựa chọn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Có bao nhiêu giá trị nguyên của tham số $m \in [-10; 10]$ để phương trình $\tan x + \cot x = m$ có nghiệm thực?"""
                )
                q8_ans = st.radio(
                    "Chọn phương án đúng:",
                    [
                        r"A. 18",
                        r"B. 21",
                        r"C. 17",
                        r"D. 19",
                    ],
                    key="q8",
                    index=None,
                )

            # ================= CÂU 9 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 9:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Nồng độ bụi mịn PM2.5 ngoài trời tại một thành phố trong ngày được mô hình hóa bởi hàm số $C(t) = 20\sin\left(\dfrac{\pi}{12}(t-6)\right) + 40$, trong đó C là nồng độ $(\mu g/m^{3})$ và t là thời gian trong ngày $(0 \le t \le 24)$. Khuyến cáo sức khỏe quy định không nên ra ngoài khi nồng độ vượt mức $50\mu g/m^{3}$.[cite: 1] Trong một ngày, khoảng thời gian không an toàn kéo dài liên tục bao nhiêu tiếng?"""
                )
                q9_ans = st.text_input("Nhập kết quả dạng số (Ví dụ: 8):", key="q9")


            # ================= CÂU 10 =================
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="question-title">
                        <b>Câu 10:</b> <span class="tag-badge">[Kéo thả / Chọn phương án]</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Cho biểu thức lượng giác $P = \sin\left(x + \frac{\pi}{6}\right)\cos\left(x - \frac{\pi}{6}\right)$. Kéo và thả các kết quả đúng vào các vị trí 1 và 2 để hoàn thiện quá trình biến đổi đại số:"""
                )
                st.markdown(
                    """
                    <div style="background-color: #f8f9fa; border: 1.5px solid #dcdfe6; border-radius: 8px; padding: 12px 16px; margin: 12px 0;">
                        <div style="font-weight: bold; color: #1e88e5; margin-bottom: 8px; font-size: 14px;">🎯 KHUNG PHƯƠNG ÁN LỰA CHỌN:</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">1/2 sin(2x) + √3/4</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">1/2 sin(2x) + √3/2</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">1/2 cos(2x) + √3/4</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">(2+√3)/4</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">(1+√3)/2</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    q10_1 = st.selectbox(
                        "📌 1) Rút gọn hoàn toàn biểu thức P, ta thu được kết quả: P =",
                        ["-- Chọn --", "1/2 sin(2x) + √3/4", "1/2 sin(2x) + √3/2", "1/2 cos(2x) + √3/4", "(2+√3)/4", "(1+√3)/2"],
                        key="q10_1",
                    )
                with col2:
                    q10_2 = st.selectbox(
                        "📌 2) Giá trị lớn nhất có thể đạt được của biểu thức P là: P_max =",
                        ["-- Chọn --", "1/2 sin(2x) + √3/4", "1/2 sin(2x) + √3/2", "1/2 cos(2x) + √3/4", "(2+√3)/4", "(1+√3)/2"],
                        key="q10_2",
                    )

            # ================= CÂU 11 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 11:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Đếm số lượng các nghiệm nguyên x thuộc đoạn $[1; 2026]$ thỏa mãn phương trình lượng giác: $\cos\left(\dfrac{\pi x}{3}\right) = \dfrac{1}{2}$."""
                )
                q11_ans = st.text_input("Nhập số lượng nghiệm (Ví dụ: 100):", key="q11")

            # ================= CÂU 12 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 12:</b> <span class="tag-badge">[Đúng/Sai]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(r"""Cho phương trình lượng giác: $(2\cos x + 1)(\cos x - m) = 0$. Xét tính đúng/sai của các mệnh đề sau:""")
                q12_a = st.radio(
                    r"A. Phương trình luôn có ít nhất **2** nghiệm phân biệt thuộc khoảng $(0; 2\pi)$ với mọi giá trị của tham số $m \in \mathbb{R}$.",
                    ["Đúng", "Sai"],
                    key="q12_1",
                    horizontal=True,
                    index=None
                )
                q12_b = st.radio(
                    r"B. Khi $m = 1$, phương trình có đúng **3** nghiệm phân biệt trên đoạn $[0; 2\pi]$.",
                    ["Đúng", "Sai"],
                    key="q12_2",
                    horizontal=True,
                    index=None
                )
                q12_c = st.radio(
                    r"C. Điều kiện cần và đủ để phương trình có đúng **4** nghiệm phân biệt trên đoạn $[-\pi; \pi]$ là $m \in (-1; 1) \setminus \{-\dfrac{1}{2}\}$.",
                    ["Đúng", "Sai"],
                    key="q12_3",
                    horizontal=True,
                    index=None
                )
                q12_d = st.radio(
                    r"D. Giả sử $m = -\dfrac{1}{2}$, tổng tất cả các nghiệm của phương trình trên đoạn $[0; 10\pi]$ là $25\pi$.",
                    ["Đúng", "Sai"],
                    key="q12_4",
                    horizontal=True,
                    index=None
                )

            # ================= CÂU 13 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 13:</b> <span class="tag-badge">[Trắc nghiệm 4 lựa chọn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Có bao nhiêu giá trị nguyên của tham số $m \in [-10; 10]$ để phương trình $m\sin x + (m+1)\cos x = m+2$ có nghiệm thực?"""
                )
                q13_ans = st.radio(
                    "Chọn phương án đúng:",
                    [
                        r"A. 17",
                        r"B. 18",
                        r"C. 19",
                        r"D. 20",
                    ],
                    key="q13",
                    index=None,
                )

            # ================= CÂU 14 =================
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="question-title">
                        <b>Câu 14:</b> <span class="tag-badge">[Kéo thả / Chọn phương án]</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Xét phương trình lượng giác $\sin 2x = 0$ trên đoạn $[0; 10\pi]$.Kéo và thả các giá trị số thích hợp để hoàn thiện các kết luận dưới đây liên quan đến tính chất của tập nghiệm."""
                )
                st.markdown(
                    """
                    <div style="background-color: #f8f9fa; border: 1.5px solid #dcdfe6; border-radius: 8px; padding: 12px 16px; margin: 12px 0;">
                        <div style="font-weight: bold; color: #1e88e5; margin-bottom: 8px; font-size: 14px;">🎯 KHUNG PHƯƠNG ÁN LỰA CHỌN:</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">20</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">21</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">100π</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">105π</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">210π</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    q14_1 = st.selectbox(
                        "📌 1) Số lượng các nghiệm phân biệt của phương trình là:",
                        ["-- Chọn --", "20", "21", "100π", "105π", "210π"],
                        key="q14_1",
                    )
                with col2:
                    q14_2 = st.selectbox(
                        "📌 2) Tổng của tất cả các nghiệm đó có giá trị bằng:",
                        ["-- Chọn --", "20", "21", "100π", "105π", "210π"],
                        key="q14_2",
                    )

            # ================= CÂU 15 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 15:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Số giờ ánh sáng mặt trời trong ngày tại một thành phố được mô hình hóa xấp xỉ bởi hàm số $H(t) = 12 + 3\sin\left[\dfrac{2\pi}{365}(t - 80)\right]$, trong đó H là số giờ chiếu sáng và t là số thứ tự của ngày trong năm $(1 \le t \le 365)$.[cite: 2] Một loại cây công nghiệp đặc biệt chỉ có thể sinh trưởng tốt nếu thời gian chiếu sáng trong ngày lớn hơn **13,5 giờ**. Hỏi trong một năm không nhuận, có bao nhiêu ngày cây có thể sinh trưởng tốt?"""
                )
                q15_ans = st.text_input("Nhập kết quả (Ví dụ: 50):", key="q15")

            # ================= CÂU 16 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 16:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Tìm giá trị của tham số thực m để hàm số $y = \dfrac{\sin x + m\cos x + 1}{\cos x - \sin x + 2}$ có giá trị lớn nhất đúng bằng 2.[cite: 2]"""
                )
                q16_ans = st.text_input("Nhập kết quả (Ví dụ: -2):", key="q16")

            # ================= CÂU 17 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 17:</b> <span class="tag-badge">[Trắc nghiệm 4 lựa chọn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Giải phương trình lượng giác $\sin x + \sin 2x + \sin 3x = 0$.[cite: 2] Hỏi các nghiệm của phương trình này được biểu diễn bởi bao nhiêu điểm phân biệt trên đường tròn lượng giác?[cite: 2]"""
                )
                q17_ans = st.radio(
                    "Chọn phương án đúng:",
                    [
                        r"A. 4",
                        r"B. 5",
                        r"C. 6",
                        r"D. 8",
                    ],
                    key="q17",
                    index=None,
                )

            # ================= CÂU 18 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 18:</b> <span class="tag-badge">[Đúng/Sai]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(r"""Cho phương trình chứa tham số m: $\sin^4 x + \cos^4 x = m$.[cite: 2] Xét tính đúng/sai của các mệnh đề sau đây:[cite: 2]""")
                q18_a = st.radio(
                    r"A. Khi $m = 1$, phương trình đã cho có đúng **4** nghiệm phân biệt trên đoạn $[0; \pi]$.",
                    ["Đúng", "Sai"],
                    key="q18_1",
                    horizontal=True,
                    index=None
                )
                q18_b = st.radio(
                    r"B. Điều kiện cần và đủ để phương trình có nghiệm là $m \in \left[\dfrac{1}{2}; 1\right]$.",
                    ["Đúng", "Sai"],
                    key="q18_2",
                    horizontal=True,
                    index=None
                )
                q18_c = st.radio(
                    r"C. Khi $m = \dfrac{3}{4}$, các điểm biểu diễn tập nghiệm của phương trình trên đường tròn lượng giác tạo thành đỉnh của một hình bát giác đều.",
                    ["Đúng", "Sai"],
                    key="q18_3",
                    horizontal=True,
                    index=None
                )
                q18_d = st.radio(
                    r"D. Nếu $m = \dfrac{1}{2}$, phương trình đã cho tương đương với phương trình $\cos 4x = -1$.",
                    ["Đúng", "Sai"],
                    key="q18_4",
                    horizontal=True,
                    index=None
                )

            # ================= CÂU 19 =================
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 19:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Tính chính xác giá trị của tổng hữu hạn sau: 
$$S = \sin^2 10^\circ + \sin^2 20^\circ + \sin^2 30^\circ + \dots + \sin^2 170^\circ + \sin^2 180^\circ$$[cite: 2]"""
                )
                q19_ans = st.text_input("Nhập giá trị của S (Ví dụ: 9):", key="q19")

            # ================= CÂU 20 =================
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="question-title">
                        <b>Câu 20:</b> <span class="tag-badge">[Kéo thả / Chọn phương án]</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Kéo và thả các tập hợp tương ứng vào ô trống bên dưới để biểu diễn điều kiện cần và đủ của tham số m sao cho các phương trình lượng giác tương ứng có nghiệm.[cite: 2]"""
                )
                st.markdown(
                    """
                    <div style="background-color: #f8f9fa; border: 1.5px solid #dcdfe6; border-radius: 8px; padding: 12px 16px; margin: 12px 0;">
                        <div style="font-weight: bold; color: #1e88e5; margin-bottom: 8px; font-size: 14px;">🎯 KHUNG PHƯƠNG ÁN LỰA CHỌN:</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">[-5; 5]</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">[-3; 1]</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">[-5; 3]</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">[1; 3]</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">(-∞; 1]</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    q20_1 = st.selectbox(
                        "📌 1) $3\sin x + 4\cos x = m$",
                        ["-- Chọn --", "[-5; 5]", "[-3; 1]", "[-5; 3]", "[1; 3]", "(-∞; 1]"],
                        key="q20_1",
                    )
                with col2:
                    q20_2 = st.selectbox(
                        "📌 2) $\sin^2 x - 2\sin x + m = 0$",
                        ["-- Chọn --", "[-5; 5]", "[-3; 1]", "[-5; 3]", "[1; 3]", "(-∞; 1]"],
                        key="q20_2",
                    )
                with col3:
                    q20_3 = st.selectbox(
                        "📌 3) $\cos 2x - 4\cos x + m = 0$",
                        ["-- Chọn --", "[-5; 5]", "[-3; 1]", "[-5; 3]", "[1; 3]", "(-∞; 1]"],
                        key="q20_3",
                    )

            # ================= SUBMIT BUTTON =================
            submit_btn = st.form_submit_button(
                f"🚀 NỘP BÀI {exam_name}", type="primary", use_container_width=True
            )
            if submit_btn:
                st.session_state.exam_submitted = True
                st.rerun()

    else:
        # ---- CHẤM ĐIỂM & LỜI GIẢI ĐỀ 1 ----
        st.balloons()
        st.success(f"🎉 BẠN ĐÃ HOÀN THÀNH {exam_name}!")
        total_score = 0.0

        # Chấm Câu 1
        if (
            st.session_state.get("q1_a") == "-50"
            and st.session_state.get("q1_w") == "2π/15"
            and st.session_state.get("q1_b") == "60"
        ):
            total_score += 2.5
            
        # Chấm Câu 2
        if st.session_state.get("q2") and st.session_state.get("q2").startswith("A."):
            total_score += 2.5
            
        # Chấm Câu 3
        if st.session_state.get("q3", "").strip() == "8":
            total_score += 2.5

        # Chấm Câu 4
        c4_score = 0
        if st.session_state.get("q4_1") == "Đúng": c4_score += 1
        if st.session_state.get("q4_2") == "Sai": c4_score += 1
        if st.session_state.get("q4_3") == "Đúng": c4_score += 1
        if st.session_state.get("q4_4") == "Sai": c4_score += 1

        if c4_score == 4: total_score += 2.5
        elif c4_score == 3: total_score += 1.5
        elif c4_score == 2: total_score += 0.75
        elif c4_score == 1: total_score += 0.25

        # Chấm Câu 5
        if st.session_state.get("q5", "").strip() == "8":
            total_score += 1.0
            
        # Chấm Câu 6
        if st.session_state.get("q6", "").strip() == "0":
            total_score += 1.0

        # Chấm Câu 7
        c7_score = 0
        if st.session_state.get("q7_1") == "Đúng": c7_score += 1
        if st.session_state.get("q7_2") == "Sai": c7_score += 1
        if st.session_state.get("q7_3") == "Đúng": c7_score += 1
        if st.session_state.get("q7_4") == "Sai": c7_score += 1

        if c7_score == 4: total_score += 1.0
        elif c7_score == 3: total_score += 0.5
        elif c7_score == 2: total_score += 0.25
        
        # Chấm Câu 8
        if st.session_state.get("q8") and st.session_state.get("q8").startswith("A."):
            total_score += 1.0
            
        # Chấm Câu 9
        if st.session_state.get("q9", "").strip() == "8":
            total_score += 1.0

        # Hiển thị điểm số
        st.markdown(
            f"""
            <div style="background-color: #ffebee; border: 2px solid #b71c1c; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
                <h2 style="color: #b71c1c; margin: 0;">TỔNG ĐIỂM {exam_name}: {total_score:.2f} / 10.0</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Chấm Câu 10
        if (
            st.session_state.get("q10_1") == "1/2 sin(2x) + √3/4"
            and st.session_state.get("q10_2") == "(2+√3)/4"
        ):
            total_score += 1.0
            
        # Chấm Câu 11
        if st.session_state.get("q11", "").strip() == "675":
            total_score += 1.0

        # Chấm Câu 12
        c12_score = 0
        if st.session_state.get("q12_1") == "Đúng": c12_score += 1
        if st.session_state.get("q12_2") == "Sai": c12_score += 1
        if st.session_state.get("q12_3") == "Đúng": c12_score += 1
        if st.session_state.get("q12_4") == "Sai": c12_score += 1

        if c12_score == 4: total_score += 1.0
        elif c12_score == 3: total_score += 0.5
        elif c12_score == 2: total_score += 0.25
        
        # Chấm Câu 13
        if st.session_state.get("q13") and st.session_state.get("q13").startswith("B."):
            total_score += 1.0

        # Chấm Câu 14
        if (
            st.session_state.get("q14_1") == "21"
            and st.session_state.get("q14_2") == "105π"
        ):
            total_score += 1.0
            
        # Chấm Câu 15
        if st.session_state.get("q15", "").strip() == "122":
            total_score += 1.0

        # Hiển thị điểm số (Cho phần này)
        st.markdown(
            f"""
            <div style="background-color: #ffebee; border: 2px solid #b71c1c; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
                <h2 style="color: #b71c1c; margin: 0;">TỔNG ĐIỂM {exam_name}: {total_score:.2f} / 6.0</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Chấm Câu 16
        if st.session_state.get("q16", "").strip() == "-2":
            total_score += 1.0
            
        # Chấm Câu 17
        if st.session_state.get("q17") and st.session_state.get("q17").startswith("C."):
            total_score += 1.0

        # Chấm Câu 18
        c18_score = 0
        if st.session_state.get("q18_1") == "Sai": c18_score += 1
        if st.session_state.get("q18_2") == "Đúng": c18_score += 1
        if st.session_state.get("q18_3") == "Đúng": c18_score += 1
        if st.session_state.get("q18_4") == "Đúng": c18_score += 1

        if c18_score == 4: total_score += 1.0
        elif c18_score == 3: total_score += 0.5
        elif c18_score == 2: total_score += 0.25
        
        # Chấm Câu 19
        if st.session_state.get("q19", "").strip() == "9":
            total_score += 1.0

        # Chấm Câu 20
        if (
            st.session_state.get("q20_1") == "[-5; 5]"
            and st.session_state.get("q20_2") == "[-3; 1]"
            and st.session_state.get("q20_3") == "[-5; 3]"
        ):
            total_score += 1.0

        # Hiển thị điểm số 
        st.markdown(
            f"""
            <div style="background-color: #ffebee; border: 2px solid #b71c1c; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
                <h2 style="color: #b71c1c; margin: 0;">TỔNG ĐIỂM {exam_name}: {total_score:.2f} / 5.0</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.subheader(f"📖 LỜI GIẢI CHI TIẾT - {exam_name}")

        with st.expander("🔍 Lời giải Câu 1: Mô hình Vòng quay Mặt Trời"):
            st.markdown(r"""
* Từ giả thiết bài toán, độ cao của tâm vòng quay đóng vai trò là hằng số dịch chuyển trên trục tung, do đó ta có ngay $B = 60$.
* Bán kính vòng quay sẽ tương ứng với biên độ của dao động, tức là $|A| = 50$.
* Tại thời điểm ban đầu $t = 0$, cabin xuất phát từ điểm thấp nhất của quỹ đạo, nên độ cao lúc này là: $h(0) = B - |A| = 60 - 50 = 10 \text{ m}$.
* Thay $t = 0$ vào hàm số, ta được $A\cos(0) + 60 = 10 \Rightarrow A = -50$. Giá trị này hoàn toàn phù hợp với điều kiện $A < 0$ mà đề bài đã cho.
* Mặt khác, chu kỳ hoàn thành một vòng quay là $T = 15$ phút, từ đó ta tính được tần số góc: $\omega = \dfrac{2\pi}{T} = \dfrac{2\pi}{15}$.
* Lắp ghép các thông số trên, ta được kết quả: $A = -50$; $\omega = 2\pi/15$; $B = 60$.
""")
            
        with st.expander("🔍 Lời giải Câu 2: Đọc đồ thị hàm số lượng giác"):
            st.markdown(r"""
* Quan sát đồ thị, ta thấy hàm số đạt giá trị lớn nhất $y_{\max} = 4$ và giá trị nhỏ nhất $y_{\min} = -2$.
* Từ đó, đường trung bình $d$ và biên độ $a$ được xác định dễ dàng:
  * $d = \dfrac{y_{\max} + y_{\min}}{2} = \dfrac{4 + (-2)}{2} = 1$.
  * $a = \dfrac{y_{\max} - y_{\min}}{2} = \dfrac{4 - (-2)}{2} = 3$.
* Nhìn trên trục hoành, khoảng cách từ điểm cực tiểu tại $x = \dfrac{2\pi}{3}$ đến điểm cực đại ngay sau đó tại $x = \dfrac{7\pi}{6}$ tương ứng với nửa chu kỳ: $\dfrac{T}{2} = \dfrac{7\pi}{6} - \dfrac{2\pi}{3} = \dfrac{\pi}{2} \Rightarrow T = \pi$.
* Suy ra hệ số góc $b$ của hàm số là: $b = \dfrac{2\pi}{T} = \dfrac{2\pi}{\pi} = 2$.
* Lúc này, hàm số đã có dạng: $y = 3\sin(2x+c) + 1$. Đồ thị đi qua điểm uốn $(\dfrac{\pi}{6}; 1)$ theo hướng đi xuống, thay vào phương trình: $3\sin\left(2 \cdot \dfrac{\pi}{6} + c\right) + 1 = 1 \Leftrightarrow \sin\left(\dfrac{\pi}{3} + c\right) = 0$.
* Vì đồ thị đi xuống, đạo hàm phải mang dấu âm, do đó pha tương ứng là: $\dfrac{\pi}{3} + c = \pi \Rightarrow c = -\dfrac{\pi}{3}$ (Thỏa mãn $c \in (-\pi; 0)$).
* Cuối cùng tính $P = a + b + c + d = 3 + 2 + \left(-\dfrac{\pi}{3}\right) + 1 = 6 - \dfrac{\pi}{3}$.

$\Rightarrow$ **Chọn đáp án A.**
""")
            
        with st.expander("🔍 Lời giải Câu 3: Mực nước cảng biển"):
            st.markdown(r"""
* Để tàu có thể neo đậu an toàn, mực nước lúc đó phải thỏa mãn bất phương trình: $3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12 \ge 13,5$.
* Rút gọn, ta thu được: $\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) \ge \dfrac{1}{2}$.
* Giải bất phương trình này trên vòng tròn lượng giác: $-\dfrac{\pi}{3} + k2\pi \le \dfrac{\pi t}{6} + \dfrac{\pi}{3} \le \dfrac{\pi}{3} + k2\pi$.
* Trừ đi $\dfrac{\pi}{3}$ và nhân với $\dfrac{6}{\pi}$ để cô lập $t$, ta được: $-4 + 12k \le t \le 12k$.
* Tìm các khoảng thời gian hợp lệ trong phạm vi một ngày ($t \in [0; 24]$):
  * Thay $k = 1$, ta có $8 \le t \le 12$ (Kéo dài **4** tiếng).
  * Thay $k = 2$, ta có $20 \le t \le 24$ (Kéo dài **4** tiếng).
* Tổng thời gian khả thi để tàu cập bến an toàn trong ngày là: $4 + 4 = 8$ giờ.

$\Rightarrow$ **Đáp số cần điền: 8.**[cite: 2]
""")
            
        with st.expander("🔍 Lời giải Câu 4: Phân tích nghiệm phương trình lượng giác"):
            st.markdown(r"""
Phương trình có thể phân tích thành tích như sau: $(2\cos x - 1)(\cos x - m) = 0 \Leftrightarrow \cos x = \dfrac{1}{2} \quad (*)$ hoặc $\cos x = m \quad (**)$.

* **a) Đúng.** Phép tách nhân tử hoàn toàn chính xác.
* **b) Sai.** Khi thay $m = 1$ vào pt (**), ta được $\cos x = 1 \Rightarrow x = 0$ hoặc $x = 2\pi$. Phương trình (*) luôn cố định 2 nghiệm là $x = \dfrac{\pi}{3}$ và $x = \dfrac{5\pi}{3}$. Tổng cộng phương trình có **4** nghiệm phân biệt chứ không phải 2.
* **c) Đúng.** Pt (*) luôn có cố định 2 nghiệm trên $[0; 2\pi]$. Để pt tổng có đúng 3 nghiệm, nhánh (**) phải sinh ra duy nhất 1 nghiệm (xảy ra tại $m = 1$ hoặc $m = -1$). Do $m = 1$ cho 2 nghiệm (vừa xét), nên chỉ có $m = -1$ (cho nghiệm duy nhất $x = \pi$) là thỏa mãn.
* **d) Sai.** Vì phương trình luôn chứa nhân tử $\left(\cos x - \dfrac{1}{2}\right) = 0$, nên nó luôn có ít nhất 2 nghiệm thực bất chấp giá trị của tham số $m$.
""")
        with st.expander("🔍 Lời giải Câu 5: Thời gian tàu cập cảng"):
            st.markdown(r"""
* Để tàu có thể neo đậu an toàn, mực nước lúc đó phải thỏa mãn bất phương trình: $3\cos\left(\frac{\pi t}{6} + \frac{\pi}{3}\right) + 12 \ge 13,5$.
* Chuyển vế và rút gọn, ta thu được bất phương trình lượng giác cơ bản: $3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) \ge 1,5 \Leftrightarrow \cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) \ge \dfrac{1}{2}$.
* Giải bất phương trình này trên vòng tròn lượng giác, ta có: $-\dfrac{\pi}{3} + k2\pi \le \dfrac{\pi t}{6} + \dfrac{\pi}{3} \le \dfrac{\pi}{3} + k2\pi$.
* Trừ $\frac{\pi}{3}$ cho toàn bộ các vế và nhân với $\frac{6}{\pi}$ để cô lập t, ta được: $-\dfrac{2\pi}{3} + k2\pi \le \dfrac{\pi t}{6} \le k2\pi \Leftrightarrow -4 + 12k \le t \le 12k$.
* Tìm các khoảng thời gian hợp lệ trong phạm vi một ngày ($t \in [0; 24]$):
  * Thay $k = 1$, ta có $8 \le t \le 12$ Nghĩa là tàu có thể cập cảng từ 8 giờ đến 12 giờ (kéo dài **4** tiếng).
  * Thay $k = 2$, ta có $20 \le t \le 24$ Nghĩa là tàu có thể cập cảng từ 20 giờ đến 24 giờ (kéo dài thêm **4** tiếng nữa).
* Tổng thời gian khả thi để tàu cập bến an toàn trong ngày là: $4 + 4 = 8$ giờ.

$\Rightarrow$ **Đáp số cần điền: 8.**[cite: 1]
""")

        with st.expander("🔍 Lời giải Câu 6: Giá trị nhỏ nhất của hàm số"):
            st.markdown(r"""
* Sử dụng bất đẳng thức Bunhiacôvski (hoặc từ điều kiện có nghiệm của phương trình $a\sin x + b\cos x = c$), ta đánh giá được cụm biểu thức lượng giác: $|3\sin x + 4\cos x| \le \sqrt{3^2 + 4^2} = 5$.
* Do đó, biểu thức $3\sin x + 4\cos x$ bị chặn khép kín trong khoảng $[-5; 5]$: $-5 \le 3\sin x + 4\cos x \le 5$.
* Cộng hằng số tự do 5 vào tất cả các vế để khôi phục lại hàm số $y$ ban đầu: $-5 + 5 \le 3\sin x + 4\cos x + 5 \le 5 + 5 \Leftrightarrow 0 \le y \le 10$.
* Từ bất đẳng thức kép trên, ta kết luận được ngay giá trị nhỏ nhất của hàm số là 0.

$\Rightarrow$ **Đáp số cần điền: 0.**[cite: 1]
""")

        with st.expander("🔍 Lời giải Câu 7: Phân tích dao động con lắc lò xo"):
            st.markdown(r"""
Dựa vào phương trình li độ $x(t) = 5\cos\left(4\pi t - \frac{\pi}{2}\right)$, ta lần lượt phân tích các tính chất động học của vật:

* **A. Đúng.** Tần số góc của dao động là $\omega = 4\pi$, từ đó ta tính được chu kỳ toàn phần $T = \frac{2\pi}{\omega} = \frac{2\pi}{4\pi} = 0,5$ (giây).
* **B. Sai.** Thay $t=0$ vào phương trình li độ, ta có $x(0) = 5\cos\left(-\frac{\pi}{2}\right) = 0$ nghĩa là vật đang ở vị trí cân bằng.[cite: 1] Xét phương trình vận tốc $v(t) = x^{\prime}(t) = -20\pi\sin\left(4\pi t - \frac{\pi}{2}\right)$, tại $t=0$ thì $v(0) = -20\pi\sin\left(-\frac{\pi}{2}\right) = 20\pi$.[cite: 1] Vì vận tốc mang giá trị dương nên vật phải đang di chuyển theo chiều dương.
* **C. Đúng.** Giá trị cực đại của vận tốc chính là tốc độ khi vật quét qua vị trí cân bằng, được tính bằng $v_{\max} = \omega A = 4\pi \cdot 5 = 20\pi$ (cm/s).
* **D. Sai.** Thời gian ngắn nhất để vật đi từ vị trí cân bằng ra đến vị trí biên tương đương với một phần tư chu kỳ dao động, tức là $\Delta t = \frac{T}{4} = \frac{0,5}{4} = 0,125$ (giây).
""")

        with st.expander("🔍 Lời giải Câu 8: Phương trình lượng giác chứa tham số"):
            st.markdown(r"""
* Trước hết, ta đặt điều kiện xác định cho phương trình là $\sin x \ne 0$ và $\cos x \ne 0$, gộp chung lại thành $\sin 2x \ne 0$.
* Biến đổi vế trái của phương trình bằng cách đưa về các hàm cơ bản: $\tan x + \cot x = \frac{\sin x}{\cos x} + \frac{\cos x}{\sin x} = \frac{\sin^2 x + \cos^2 x}{\sin x \cdot \cos x} = \frac{1}{\frac{1}{2}\sin 2x} = \frac{2}{\sin 2x}$.
* Lúc này, phương trình đã cho trở thành: $\frac{2}{\sin 2x} = m \Leftrightarrow \sin 2x = \frac{2}{m}$ (điều kiện $m \ne 0$).
* Để phương trình có nghiệm, giá trị lượng giác $\sin 2x$ phải nằm trong giới hạn tự nhiên của nó là đoạn $[-1; 1]$.[cite: 1] Đồng thời, do điều kiện xác định $\sin 2x \ne 0$, ta thiết lập được hệ bất phương trình cho tham số m: $-1 \le \frac{2}{m} \le 1$ và $\frac{2}{m} \ne 0 \Leftrightarrow |m| \ge 2$.[cite: 1]
* Kết hợp với điều kiện bài toán yêu cầu m là số nguyên thuộc đoạn $[-10; 10]$, ta liệt kê được các giá trị hợp lệ: $m \in \{-10, -9, ..., -2\} \cup \{2, 3, ..., 10\}$.[cite: 1]
* Đếm số lượng phần tử, ta có $9 + 9 = 18$ giá trị thỏa mãn.[cite: 1]

$\Rightarrow$ **Chọn đáp án A.**[cite: 1]
""")

        with st.expander("🔍 Lời giải Câu 9: Mô hình nồng độ bụi mịn PM2.5"):
            st.markdown(r"""
* Khoảng thời gian không an toàn tương ứng với lúc nồng độ bụi mịn vượt ngưỡng cho phép.[cite: 1] Do đó, ta thiết lập bất phương trình: $20\sin\left(\frac{\pi}{12}(t-6)\right) + 40 \ge 50 \Leftrightarrow 20\sin\left(\frac{\pi}{12}(t-6)\right) \ge 10$.[cite: 1]
* Rút gọn, ta thu được: $\sin\left(\frac{\pi}{12}(t-6)\right) \ge \frac{1}{2}$.[cite: 1]
* Giải bất phương trình này trên vòng tròn lượng giác, ta định vị được khoảng nghiệm như sau: $\frac{\pi}{6} + k2\pi \le \frac{\pi}{12}(t-6) \le \frac{5\pi}{6} + k2\pi$.[cite: 1]
* Nhân cả ba vế với $\frac{12}{\pi}$ để khử các hệ số: $2 + 24k \le t - 6 \le 10 + 24k \Leftrightarrow 8 + 24k \le t \le 16 + 24k$.[cite: 1]
* Bởi vì thời gian được khảo sát gói gọn trong một chu kỳ ngày $(t \in [0; 24])$, ta chỉ có thể chọn giá trị $k = 0$, tương ứng với khoảng: $8 \le t \le 16$.[cite: 1]
* Điều này có nghĩa là mức độ ô nhiễm sẽ duy trì ở trạng thái không an toàn từ 8 giờ sáng đến 16 giờ chiều.[cite: 1] Tính thời lượng kéo dài liên tục, ta lấy $16 - 8 = 8$ tiếng.[cite: 1]

$\Rightarrow$ **Đáp số cần điền: 8.**[cite: 1]
""")
            with st.expander("🔍 Lời giải Câu 10: Rút gọn biểu thức lượng giác"):
                st.markdown(r"""
* Sử dụng công thức biến đổi tích thành tổng $\sin a \cos b = \frac{1}{2}[\sin(a+b) + \sin(a-b)]$.
* Với $a = x + \frac{\pi}{6}$ và $b = x - \frac{\pi}{6}$, ta khai triển $P$ như sau: $P = \frac{1}{2}\left[\sin\left(x + \frac{\pi}{6} + x - \frac{\pi}{6}\right) + \sin\left(x + \frac{\pi}{6} - \left(x - \frac{\pi}{6}\right)\right)\right]$.
* Rút gọn các số hạng đồng dạng ở góc bên trong: $P = \frac{1}{2}\left[\sin 2x + \sin\left(\frac{\pi}{3}\right)\right] = \frac{1}{2}\sin 2x + \frac{\sqrt{3}}{4}$.
* Giá trị lớn nhất của biểu thức này dựa trên tính chất $\sin 2x \le 1$ với mọi số thực x.[cite: 2] Suy ra: $P \le \frac{1}{2} \cdot 1 + \frac{\sqrt{3}}{4} = \frac{2+\sqrt{3}}{4}$.
* Dấu bằng xảy ra khi $\sin 2x = 1 \Leftrightarrow 2x = \frac{\pi}{2} + k2\pi$, tức là $x = \frac{\pi}{4} + k\pi$.

$\Rightarrow$ **Kết quả:** 1) $\frac{1}{2}\sin 2x + \frac{\sqrt{3}}{4}$; 2) $\frac{2+\sqrt{3}}{4}$.
""")

        with st.expander("🔍 Lời giải Câu 11: Đếm số nghiệm nguyên"):
            st.markdown(r"""
* Phương trình $\cos\left(\frac{\pi x}{3}\right) = \frac{1}{2}$ sẽ cho ta hai họ nghiệm lượng giác: $\frac{\pi x}{3} = \frac{\pi}{3} + k2\pi$ hoặc $\frac{\pi x}{3} = -\frac{\pi}{3} + k2\pi \quad (k \in \mathbb{Z})$.
* Rút gọn $\pi$ và nhân chéo 3 lên, ta cô lập được x: $x = 1 + 6k$ hoặc $x = -1 + 6k$.
* Ép điều kiện $x \in [1; 2026]$ cho từng họ nghiệm:
  * **Với họ $x = 6k + 1$:** $1 \le 6k + 1 \le 2026 \Leftrightarrow 0 \le 6k \le 2025 \Leftrightarrow 0 \le k \le 337,5$.[cite: 2] Do k nguyên, k nhận các giá trị từ 0 đến 337, tương ứng tạo ra **338** nghiệm.
  * **Với họ $x = 6k - 1$:** $1 \le 6k - 1 \le 2026 \Leftrightarrow 2 \le 6k \le 2027 \Leftrightarrow 0,33 \le k \le 337,8$.[cite: 2] Lúc này k nhận các giá trị nguyên từ 1 đến 337, sinh ra thêm **337** nghiệm nữa.
* Vì hai họ nghiệm này rời nhau hoàn toàn, tổng số nghiệm nguyên hợp lệ là $338 + 337 = 675$.

$\Rightarrow$ **Đáp số cần điền: 675.**[cite: 2]
""")

        with st.expander("🔍 Lời giải Câu 12: Phương trình tích chứa tham số"):
            st.markdown(r"""
Cấu trúc của phương trình tích đã cho: $(2\cos x + 1)(\cos x - m) = 0 \Leftrightarrow \cos x = -\frac{1}{2} \quad (1)$ hoặc $\cos x = m \quad (2)$.[cite: 2]

* **A. Đúng.** Phương trình (1) là phương trình hằng số, luôn cho ra đúng 2 nghiệm $x = \frac{2\pi}{3}$ và $x = \frac{4\pi}{3}$ trên khoảng $(0; 2\pi)$.[cite: 2] Hệ phương trình luôn có tối thiểu 2 nghiệm này bất chấp m.
* **B. Sai.** Khi $m = 1$, pt (2) trở thành $\cos x = 1$.[cite: 2] Trên đoạn $[0; 2\pi]$, nó sinh ra 2 nghiệm là $x = 0$ và $x = 2\pi$.[cite: 2] Kết hợp với 2 nghiệm của pt (1), tổng cộng ta có 4 nghiệm phân biệt, không phải 3.
* **C. Đúng.** Trên đoạn $[-\pi; \pi]$, pt (1) đóng góp 2 nghiệm là $\pm \frac{2\pi}{3}$.[cite: 2] Để có đúng 4 nghiệm, pt (2) phải sinh ra thêm đúng 2 nghiệm mới.[cite: 2] Điều này xảy ra khi $-1 < m < 1$ và $m \ne -\frac{1}{2}$ để tránh trùng nghiệm.
* **D. Sai.** Khi $m = -\frac{1}{2}$, phương trình trở thành nghiệm kép $\cos x = -\frac{1}{2}$.[cite: 2] Trên đoạn $[0; 2\pi]$, tổng 2 nghiệm là $\frac{2\pi}{3} + \frac{4\pi}{3} = 2\pi$.[cite: 2] Trên đoạn $[0; 10\pi]$ tương ứng với 5 vòng tròn tuần hoàn, tổng các nghiệm sẽ là: $(2\pi) + (2\pi + 4\pi) + (2\pi + 8\pi) + (2\pi + 12\pi) + (2\pi + 16\pi) = 50\pi$, chứ không phải $25\pi$.
""")

        with st.expander("🔍 Lời giải Câu 13: Phương trình lượng giác bậc nhất"):
            st.markdown(r"""
* Đây là phương trình dạng $a\sin x + b\cos x = c$.Điều kiện có nghiệm là $a^2 + b^2 \ge c^2$.
* Áp dụng vào bài toán: $m^2 + (m+1)^2 \ge (m+2)^2$.
* Khai triển và rút gọn: $m^2 + m^2 + 2m + 1 \ge m^2 + 4m + 4 \Leftrightarrow m^2 - 2m - 3 \ge 0$.
* Giải bất phương trình: $m \le -1$ hoặc $m \ge 3$.
* Với giới hạn $m \in [-10; 10]$ và $m \in \mathbb{Z}$, ta liệt kê được: $m \in \{-10; -9; ...; -1\} \cup \{3; 4; ...; 10\}$.
* Số lượng phần tử âm là 10, dương là 8. Tổng cộng có $10 + 8 = 18$ giá trị thỏa mãn.

$\Rightarrow$ **Chọn đáp án B.**
""")

        with st.expander("🔍 Lời giải Câu 14: Phân tích tập nghiệm phương trình cơ bản"):
            st.markdown(r"""
* Giải phương trình: $\sin 2x = 0 \Leftrightarrow 2x = k\pi \Leftrightarrow x = k\dfrac{\pi}{2} \quad (k \in \mathbb{Z})$.
* Để nghiệm nằm trong đoạn $[0; 10\pi]$: $0 \le k\dfrac{\pi}{2} \le 10\pi \Leftrightarrow 0 \le \frac{k}{2} \le 10 \Leftrightarrow 0 \le k \le 20$.
* Với $k$ từ 0 đến 20, ta đếm được $20 - 0 + 1 = 21$ nghiệm hợp lệ.[cite: 2]
* Tổng các nghiệm này là: $S = 0 + \dfrac{\pi}{2} + \dfrac{2\pi}{2} + ... + \dfrac{20\pi}{2} = \dfrac{\pi}{2}(0 + 1 + 2 + ... + 20)$.
* Sử dụng công thức cấp số cộng (Gauss): $S = \dfrac{\pi}{2} \cdot \dfrac{20 \cdot 21}{2} = \dfrac{\pi}{2} \cdot 210 = 105\pi$.

$\Rightarrow$ **Kết quả:** 1) 21; 2) $105\pi$.
""")

        with st.expander("🔍 Lời giải Câu 15: Mô hình ánh sáng mặt trời"):
            st.markdown(r"""
* Yêu cầu bài toán được dịch sang bất phương trình: $H(t) > 13,5 \Leftrightarrow 12 + 3\sin\left[\dfrac{2\pi}{365}(t - 80)\right] > 13,5$.
* Rút gọn hàm lượng giác: $\sin\left[\dfrac{2\pi}{365}(t - 80)\right] > 0,5$.
* Trên cung tròn lượng giác, hàm sin nhận giá trị lớn hơn $1/2$ trong giới hạn góc từ $\dfrac{\pi}{6}$ đến $\dfrac{5\pi}{6}$.
* Ta thiết lập: $\frac{\pi}{6} < \frac{2\pi}{365}(t - 80) < \dfrac{5\pi}{6}$.
* Triệt tiêu $\pi$ và nhân chéo đại lượng $\dfrac{365}{2}$ lên: $\dfrac{365}{12} < t - 80 < \dfrac{5 \cdot 365}{12} \Leftrightarrow 30,41 < t - 80 < 152,08$.
* Cộng thêm 80 vào ba vế: $110,41 < t < 232,08$.
* Vì t là số nguyên, các ngày thỏa mãn là: $111 \le t \le 232$.
* Tổng số ngày là $232 - 111 + 1 = 122$ ngày.

$\Rightarrow$ **Đáp số cần điền: 122.**
""")

        with st.expander("🔍 Lời giải Câu 16: Tìm tham số m để hàm số đạt Max"):
            st.markdown(r"""
* Biến đổi hàm số phân thức lượng giác thành phương trình bậc nhất theo $\sin x$ và $\cos x$.[cite: 2] Nhân chéo mẫu số (vì $\cos x - \sin x + 2 > 0 \, \forall x$): $y(\cos x - \sin x + 2) = \sin x + m\cos x + 1$.[cite: 2]
* Nhóm các hệ số: $(y+1)\sin x + (m-y)\cos x = 2y-1$.[cite: 2]
* Phương trình có nghiệm $x$ khi thỏa mãn điều kiện biên độ: $(y+1)^2 + (m-y)^2 \ge (2y-1)^2$.[cite: 2]
* Khai triển và rút gọn: $y^2 + 2y + 1 + m^2 - 2my + y^2 \ge 4y^2 - 4y + 1 \Leftrightarrow 2y^2 - (2m+6)y - m^2 \le 0 \quad (*)$.[cite: 2]
* Tập nghiệm của (*) chính là tập giá trị của hàm số đoạn $[y_{\min}; y_{\max}]$.[cite: 2] Để giá trị lớn nhất $y_{\max} = 2$, thì $y=2$ phải là nghiệm làm cho vế trái bằng 0: $2(2)^2 - (2m+6)(2) - m^2 = 0 \Leftrightarrow 8 - 4m - 12 - m^2 = 0 \Leftrightarrow m^2 + 4m + 4 = 0$.[cite: 2]
* Hằng đẳng thức xuất hiện: $(m+2)^2 = 0 \Rightarrow m = -2$.[cite: 2]

$\Rightarrow$ **Đáp số cần điền: -2.**[cite: 2]
""")

        with st.expander("🔍 Lời giải Câu 17: Biểu diễn nghiệm trên đường tròn lượng giác"):
            st.markdown(r"""
* Ghép cặp số hạng đầu và số hạng cuối, tận dụng công thức tổng thành tích: $(\sin 3x + \sin x) + \sin 2x = 0 \Leftrightarrow 2\sin 2x\cos x + \sin 2x = 0$.[cite: 2]
* Rút nhân tử chung: $\sin 2x(2\cos x + 1) = 0$.[cite: 2]
* Điều này dẫn đến 2 trường hợp:
  * $\sin 2x = 0 \Rightarrow 2x = k\pi \Rightarrow x = k\dfrac{\pi}{2}$.[cite: 2] Họ nghiệm này tạo ra **4 điểm** phân biệt ứng với các góc $0, \dfrac{\pi}{2}, \pi, \dfrac{3\pi}{2}$.[cite: 2]
  * $\cos x = -\dfrac{1}{2} \Rightarrow x = \pm\dfrac{2\pi}{3} + k2\pi$.[cite: 2] Họ này bổ sung thêm đúng **2 điểm** hoàn toàn mới là $\dfrac{2\pi}{3} (120^\circ)$ và $\dfrac{4\pi}{3} (240^\circ)$.[cite: 2]
* Hai tập hợp điểm này không trùng lặp, nên tổng số điểm biểu diễn phân biệt là $4 + 2 = 6$ điểm.[cite: 2]

$\Rightarrow$ **Chọn đáp án C.**[cite: 2]
""")

        with st.expander("🔍 Lời giải Câu 18: Biện luận số nghiệm phương trình lượng giác"):
            st.markdown(r"""
Hạ bậc nhanh phương trình bằng hằng đẳng thức mở rộng: $(\sin^2 x + \cos^2 x)^2 - 2\sin^2 x\cos^2 x = m \Leftrightarrow 1 - \dfrac{1}{2}\sin^2 2x = m \Leftrightarrow \sin^2 2x = 2(1-m)$.[cite: 2]

* **A. Sai.** Khi $m = 1 \Rightarrow \sin^2 2x = 0 \Leftrightarrow \sin 2x = 0 \Rightarrow x = k\dfrac{\pi}{2}$.[cite: 2] Trên đoạn $[0; \pi]$, ta tìm được **3** nghiệm phân biệt $\left\{0; \dfrac{\pi}{2}; \pi\right\}$, không phải 4.[cite: 2]
* **B. Đúng.** Vì hàm bình phương $\sin^2 2x$ luôn bị khống chế trong đoạn $[0; 1]$, nên phương trình có nghiệm khi: $0 \le 2(1-m) \le 1 \Leftrightarrow 0 \le 1-m \le \dfrac{1}{2} \Leftrightarrow \dfrac{1}{2} \le m \le 1$.[cite: 2]
* **C. Đúng.** Thử trực tiếp $m = \dfrac{3}{4}$, ta được $\sin^2 2x = \dfrac{1}{2} \Rightarrow \cos^2 2x = \dfrac{1}{2} \Rightarrow \cos 4x = 0$.[cite: 2] Nghiệm thu được là $4x = \dfrac{\pi}{2} + k\pi \Rightarrow x = \dfrac{\pi}{8} + k\dfrac{\pi}{4}$.[cite: 2] Khoảng cách giữa các nghiệm là $\dfrac{\pi}{4} (45^\circ)$, chia đường tròn thành 8 phần bằng nhau tạo thành bát giác đều.[cite: 2]
* **D. Đúng.** Thay $m = \dfrac{1}{2}$ vào, ta nhận được $\sin^2 2x = 1$.[cite: 2] Dùng công thức hạ bậc: $\dfrac{1-\cos 4x}{2} = 1 \Leftrightarrow \cos 4x = -1$.[cite: 2]
""")

        with st.expander("🔍 Lời giải Câu 19: Tính tổng chuỗi lượng giác"):
            st.markdown(r"""
* Dãy tổng S bao gồm các số hạng là bình phương hàm sin của các góc tăng dần với bước nhảy $10^\circ$, kéo dài từ $10^\circ$ đến $180^\circ$.[cite: 2] Có tổng cộng 18 số hạng.[cite: 2]
* Tách hai góc đặc biệt: $\sin^2 90^\circ = 1$ và $\sin^2 180^\circ = 0$.[cite: 2]
* Với các góc từ $10^\circ$ đến $80^\circ$, ta gom được thành 4 cặp phụ nhau có tổng bằng 1 (VD: $\sin^2 10^\circ + \sin^2 80^\circ = \sin^2 10^\circ + \cos^2 10^\circ = 1$).[cite: 2] Vậy 4 cặp này cho giá trị bằng **4**.[cite: 2]
* Đối với các góc tù từ $100^\circ$ đến $170^\circ$, tính chất góc bù cho phép đưa về góc nhọn (VD: $\sin 170^\circ = \sin 10^\circ$).[cite: 2] Như vậy, chuỗi này phản chiếu hoàn toàn chuỗi từ $10^\circ$ đến $80^\circ$, cũng cho kết quả bằng **4**.[cite: 2]
* Tổng kết toàn bộ chuỗi: $S = 4 + 1 + 4 + 0 = 9$.[cite: 2]

$\Rightarrow$ **Đáp số cần điền: 9.**[cite: 2]
""")

        with st.expander("🔍 Lời giải Câu 20: Tập giá trị hàm số lượng giác"):
            st.markdown(r"""
* **1)** Phương trình $3\sin x + 4\cos x = m$ có nghiệm khi: $3^2 + 4^2 \ge m^2 \Leftrightarrow m^2 \le 25 \Leftrightarrow m \in [-5; 5]$.[cite: 2]
* **2)** Phương trình sinh ra $m = -\sin^2 x + 2\sin x$.[cite: 2] Đặt $t = \sin x \in [-1; 1]$.[cite: 2] Hàm số $f(t) = -t^2 + 2t$ trên đoạn $[-1; 1]$.[cite: 2] Đỉnh parabol tại $t = 1 \Rightarrow f(1) = 1$.[cite: 2] Giá trị tại biên còn lại $f(-1) = -3$.[cite: 2] Tập giá trị quét từ $-3$ đến $1$, buộc $m \in [-3; 1]$.[cite: 2]
* **3)** Dùng công thức nhân đôi: $m = -(2\cos^2 x - 1) + 4\cos x = -2\cos^2 x + 4\cos x + 1$.[cite: 2] Đặt $u = \cos x \in [-1; 1]$.[cite: 2] Hàm $g(u) = -2u^2 + 4u + 1$.[cite: 2] Đỉnh đồ thị nằm ở $u = 1 \Rightarrow g(1) = 3$.[cite: 2] Giá trị tại đầu mút kia $g(-1) = -5$.[cite: 2] Hàm trải dài trên đoạn $[-5; 3]$.[cite: 2] Đồng nghĩa với $m \in [-5; 3]$.[cite: 2]

$\Rightarrow$ **Kết quả:** 1) `[-5; 5]`, 2) `[-3; 1]`, 3) `[-5; 3]`.[cite: 2]
""")



        

# ------------------------- ĐỀ TSA SỐ 02 -------------------------
elif "Đề TSA số 02" in selected_exam:
    if not st.session_state.exam_submitted:
        with st.form("tsa_exam_form_2"):
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 1 (Đề 2):</b> <span class="tag-badge">[Trắc nghiệm]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(r"""Một sự kiện dịch bệnh truyền nhiễm được mô hình hóa bởi hàm số logarit. Đây là câu hỏi ví dụ cho Đề số 2...""")
                st.radio(
                    "Chọn đáp án:",
                    ["A. Hàm đồng biến", "B. Hàm nghịch biến"],
                    key="q_de2_1",
                    index=None,
                )

            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 2 (Đề 2):</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(r"""Tính giá trị lớn nhất của hàm số chi phí sản xuất $C(x) = x^3 - 3x^2 + 5$ trên đoạn $[0; 3]$.""")
                st.text_input("Nhập kết quả:", key="q_de2_2")

            submit_btn = st.form_submit_button(
                f"🚀 NỘP BÀI {exam_name}", type="primary", use_container_width=True
            )
            if submit_btn:
                st.session_state.exam_submitted = True
                st.rerun()
                
    else:
        # ---- CHẤM ĐIỂM & LỜI GIẢI ĐỀ 2 ----
        st.balloons()
        st.success(f"🎉 BẠN ĐÃ HOÀN THÀNH {exam_name}!")
        total_score = 0.0

        if st.session_state.get("q_de2_1") == "A. Hàm đồng biến":
            total_score += 5.0
        if st.session_state.get("q_de2_2", "").strip() == "5":
            total_score += 5.0

        st.markdown(
            f"""
            <div style="background-color: #ffebee; border: 2px solid #b71c1c; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
                <h2 style="color: #b71c1c; margin: 0;">TỔNG ĐIỂM {exam_name}: {total_score:.2f} / 10.0</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.subheader(f"📖 LỜI GIẢI CHI TIẾT - {exam_name}")

        with st.expander("🔍 Lời giải Câu 1 & 2 (Đề 2)"):
            st.markdown("Lời giải chi tiết cho đề hàm số sẽ hiển thị ở đây...")


# ------------------------- ĐỀ TSA SỐ 03 -------------------------
elif "Đề TSA số 03" in selected_exam:
    if not st.session_state.exam_submitted:
        with st.form("tsa_exam_form_3"):
            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 1 (Đề 3):</b> <span class="tag-badge">[Trắc nghiệm]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(r"""Cho bảng số liệu về độ tuổi của sinh viên Bách Khoa. Hãy tính số trung vị...""")
                st.radio(
                    "Chọn đáp án:",
                    ["A. 19", "B. 20", "C. 21", "D. 22"],
                    key="q_de3_1",
                    index=None,
                )

            submit_btn = st.form_submit_button(
                f"🚀 NỘP BÀI {exam_name}", type="primary", use_container_width=True
            )
            if submit_btn:
                st.session_state.exam_submitted = True
                st.rerun()
                
    else:
        # ---- CHẤM ĐIỂM & LỜI GIẢI ĐỀ 3 ----
        st.balloons()
        st.success(f"🎉 BẠN ĐÃ HOÀN THÀNH {exam_name}!")
        total_score = 0.0

        if st.session_state.get("q_de3_1") == "C. 21":
            total_score += 10.0

        st.markdown(
            f"""
            <div style="background-color: #ffebee; border: 2px solid #b71c1c; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
                <h2 style="color: #b71c1c; margin: 0;">TỔNG ĐIỂM {exam_name}: {total_score:.2f} / 10.0</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.subheader(f"📖 LỜI GIẢI CHI TIẾT - {exam_name}")

        with st.expander("🔍 Lời giải Câu 1 (Đề 3)"):
            st.markdown("Lời giải chi tiết cho đề xác suất thống kê sẽ hiển thị ở đây...")
