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
        "Đề TSA số 01: Chuyên đề Lượng giác & Dao động",
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
            with st.container(border=True):
                # Tách phần HTML và Markdown riêng biệt để tối ưu hiển thị
                st.markdown(
                    """
                    <div class="question-title">
                        <b>Câu 1:</b> <span class="tag-badge">[Kéo thả / Chọn phương án]</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""
Một vòng quay Mặt Trời có bán kính **50 m**. Tâm của vòng quay nằm ở độ cao **60 m** so với mặt đất. Vòng quay quay đều, mất **15** phút để hoàn thành một vòng. Giả sử tại thời điểm **t = 0** (phút), một cabin bắt đầu chuyển động từ vị trí thấp nhất. Độ cao của cabin theo thời gian được mô hình hóa bởi:

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
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">80</span>
                            <span style="background-color: #e3f2fd; color: #0d47a1; padding: 4px 12px; border-radius: 15px; font-weight: 600;">2π/15</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""
**Hãy điền vào các vị trí còn thiếu:**
* Giá trị $A =$ **`[ (1) ]`** &nbsp;&nbsp;|&nbsp;&nbsp; Tần số góc $\omega =$ **`[ (2) ]`** &nbsp;&nbsp;|&nbsp;&nbsp; Giá trị $B =$ **`[ (3) ]`**
"""
                )
                col1, col2, col3 = st.columns(3)
                with col1:
                    q1_val_A = st.selectbox(
                        "📌 (1) Chọn giá trị A:",
                        ["-- Chọn --", "-50", "50", "60", "80"],
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

            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 2:</b> <span class="tag-badge">[Trắc nghiệm 4 lựa chọn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Cho hàm số $y = a\sin(bx+c) + d$ có $y_{\max} = 4$, $y_{\min} = -2$, chu kỳ $T = \pi$. Biết $a, b > 0$ và $c \in (-\pi; 0)$. Tính $P = a + b + c + d$."""
                )
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

            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 3:</b> <span class="tag-badge">[Trả lời ngắn]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    r"""Mực nước cảng biển là $h(t) = 3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12$ (mét). Tàu cần mực nước $\ge 13,5\text{ m}$. Trong 24h, tổng thời gian tàu cập cảng an toàn là bao nhiêu giờ?"""
                )
                q3_ans = st.text_input("Nhập kết quả dạng số (Ví dụ: 8):", key="q3")

            with st.container(border=True):
                st.markdown(
                    r"""<div class="question-title"><b>Câu 4:</b> <span class="tag-badge">[Đúng/Sai]</span></div>""",
                    unsafe_allow_html=True,
                )
                st.markdown(r"""Cho phương trình: $2\cos^2 x - (2m+1)\cos x + m = 0 \quad (1)$.""")
                q4_a = st.radio(
                    r"a) (1) tương đương $(\cos x - m)(2\cos x - 1) = 0$.",
                    ["Đúng", "Sai"],
                    key="q4_1",
                    horizontal=True,
                )
                q4_b = st.radio(
                    r"b) Khi $m = 1$, phương trình có đúng $2$ nghiệm trên $[0; 2\pi]$.",
                    ["Đúng", "Sai"],
                    key="q4_2",
                    horizontal=True,
                )
                q4_c = st.radio(
                    r"c) Để có đúng $3$ nghiệm trên $[0; 2\pi]$ thì $m = -1$.",
                    ["Đúng", "Sai"],
                    key="q4_3",
                    horizontal=True,
                )
                q4_d = st.radio(
                    r"d) Tồn tại $m$ để phương trình vô nghiệm.",
                    ["Đúng", "Sai"],
                    key="q4_4",
                    horizontal=True,
                )

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

        if (
            st.session_state.get("q1_a") == "-50"
            and st.session_state.get("q1_w") == "2π/15"
            and st.session_state.get("q1_b") == "60"
        ):
            total_score += 2.5
            
        if st.session_state.get("q2") and st.session_state.get("q2").startswith("A."):
            total_score += 2.5
            
        if st.session_state.get("q3", "").strip() == "8":
            total_score += 2.5

        c4_score = 0
        if st.session_state.get("q4_1") == "Đúng": c4_score += 1
        if st.session_state.get("q4_2") == "Sai": c4_score += 1
        if st.session_state.get("q4_3") == "Đúng": c4_score += 1
        if st.session_state.get("q4_4") == "Sai": c4_score += 1

        if c4_score == 4: total_score += 2.5
        elif c4_score == 3: total_score += 1.5
        elif c4_score == 2: total_score += 0.75
        elif c4_score == 1: total_score += 0.25

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

        with st.expander("🔍 Lời giải Câu 1: Mô hình Vòng quay Mặt Trời"):
            st.markdown(r"""- Độ cao tâm vòng quay là vị trí cân bằng $\Rightarrow B = 60$...""")
        with st.expander("🔍 Lời giải Câu 2: Đọc đồ thị hàm số lượng giác"):
            st.markdown(r"""- **Chọn đáp án A.** ($P = 6 - \dfrac{\pi}{3}$)""")
        with st.expander("🔍 Lời giải Câu 3: Mực nước cảng biển"):
            st.markdown(r"""- Tổng thời gian tàu cập cảng an toàn là 8 giờ.""")
        with st.expander("🔍 Lời giải Câu 4: Phân tích nghiệm phương trình lượng giác"):
            st.markdown(r"""- **a) Đúng | b) Sai | c) Đúng | d) Sai**""")


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
