import streamlit as st
import time
from datetime import datetime, timedelta

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Hệ Thống Thi Thử TSA Bách Khoa",
    page_icon="🦅",
    layout="wide"
)

# 2. GIAO DIỆN KHUNG VIỀN ĐỎ TRỰC QUAN (CUSTOM CSS)
st.markdown("""
<style>
    /* Header chính */
    .tsa-header {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(183, 28, 28, 0.3);
    }
    
    /* Áp dụng viền đỏ trực tiếp cho các Container của Streamlit */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #d32f2f !important;
        border-radius: 10px !important;
        background-color: #fffbfb !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05) !important;
    }
    
    /* Tiêu đề câu hỏi */
    .question-title {
        color: #b71c1c;
        font-weight: bold;
        font-size: 1.15em;
        margin-bottom: 12px;
        border-bottom: 1.5px dashed #ef9a9a;
        padding-bottom: 8px;
    }
    
    /* Nhãn loại câu hỏi */
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
    
    /* Khung đồng hồ đếm ngược */
    .timer-container {
        background-color: #b71c1c;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. KHỞI TẠO SESSION STATE
if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# 4. THANH BÊN (SIDEBAR): CHỌN ĐỀ THI & ĐỒNG HỒ ĐẾM NGƯỢC
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Logo_HUST.png/1200px-Logo_HUST.png", width=120)
st.sidebar.title("THI THỬ TSA ONLINE")

# Danh sách đề thi
selected_exam = st.sidebar.selectbox(
    "📋 Chọn Đề Thi TSA:",
    [
        "Đề TSA số 01: Chuyên đề Lượng giác & Dao động",
        "Đề TSA số 02: Hàm số & Mô hình Toán thực tế",
        "Đề TSA số 03: Xác suất & Phân tích số liệu"
    ]
)

st.sidebar.markdown("---")

# Đồng hồ bấm giờ lùi 60 phút
EXAM_DURATION_MINUTES = 60
elapsed_seconds = (datetime.now() - st.session_state.start_time).seconds
remaining_seconds = max(0, (EXAM_DURATION_MINUTES * 60) - elapsed_seconds)

mins, secs = divmod(remaining_seconds, 60)
timer_text = f"⏱️ Thời gian còn lại: {mins:02d}:{secs:02d}"

st.sidebar.markdown(f'<div class="timer-container">{timer_text}</div>', unsafe_allow_html=True)

if remaining_seconds == 0 and not st.session_state.exam_submitted:
    st.session_state.exam_submitted = True
    st.sidebar.warning("⚠️ Đã hết thời gian làm bài!")

if st.sidebar.button("🔄 Làm lại bài thi", type="secondary"):
    st.session_state.start_time = datetime.now()
    st.session_state.exam_submitted = False
    st.rerun()

# 5. TIÊU ĐỀ CHÍNH BÀI THI
st.markdown("""
<div class="tsa-header">
    <h1>KỲ THI ĐÁNH GIÁ TƯ DUY (TSA) - ĐẠI HỌC BÁCH KHOA HÀ NỘI</h1>
    <h3>CHUYÊN ĐỀ: LƯỢNG GIÁC & MÔ HÌNH TOÁN HỌC</h3>
</div>
""", unsafe_allow_html=True)

# 6. GIAO DIỆN LÀM BÀI / CHẤM ĐIỂM
if not st.session_state.exam_submitted:
    with st.form("tsa_exam_form"):
        
        # ---------------------------------------------------------------------
       # ---------------------------------------------------------------------
        # CÂU 1: CÂU HỎI KÉO THẢ / CHỌN PHƯƠNG ÁN ĐIỀN CHỖ TRỐNG
        # ---------------------------------------------------------------------
        with st.container(border=True):
            st.markdown("""
            <div class="question-title">
                <span class="tag-badge">DẠNG 1: CHỌN / KÉO THẢ PHƯƠNG ÁN</span> Câu 1: Mô hình Vòng quay Mặt Trời
            </div>
            """, unsafe_allow_html=True)
            
            # Lưu ý chữ 'r' ở đầu chuỗi (raw string) để hiển thị LaTeX an toàn
            st.markdown(r"""
            Một vòng quay Mặt Trời có bán kính $50\text{ m}$. Tâm của vòng quay nằm ở độ cao $60\text{ m}$ so với mặt đất. Vòng quay quay đều, mất $15$ phút để hoàn thành một vòng. Giả sử tại thời điểm $t=0$ (phút), một cabin bắt đầu chuyển động từ vị trí thấp nhất. Độ cao của cabin theo thời gian được mô hình hóa bởi:
            
            $$h(t) = A\cos(\omega t) + B \quad (A < 0)$$
            
            **Hãy lựa chọn các giá trị thích hợp tương ứng để hoàn thiện kết luận:**
            """)
            
            col1, col2, col3 = st.columns(3)
            q1_val_A = col1.selectbox("1) Giá trị A:", ["-- Chọn --", "50", "-50", "60", "-60"], key="q1_a")
            q1_val_w = col2.selectbox(r"2) Tần số góc $\omega$:", ["-- Chọn --", r"\dfrac{2\pi}{15}", r"\dfrac{15}{2\pi}", r"\dfrac{\pi}{15}"], key="q1_w")
            q1_val_B = col3.selectbox("3) Giá trị B:", ["-- Chọn --", "50", "60", "85", "10"], key="q1_b")
            q1_val_t = st.selectbox("4) Thời điểm đầu tiên cabin đạt độ cao 85m là vào phút thứ:", ["-- Chọn --", "2.5", "5", "7.5", "10"], key="q1_t")
        
        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # CÂU 2: CÂU HỎI TRẮC NGHIỆM 4 LỰA CHỌN
        # ---------------------------------------------------------------------
        with st.container(border=True):
            st.markdown("""
            <div class="question-title">
                <span class="tag-badge">DẠNG 2: TRẮC NGHIỆM 4 LỰA CHỌN</span> Câu 2: Đọc đồ thị hàm số lượng giác
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(r"""
            Cho hàm số lượng giác $y = a\sin(bx+c) + d$ có đồ thị đạt giá trị lớn nhất $y_{\max} = 4$, giá trị nhỏ nhất $y_{\min} = -2$, chu kỳ $T = \pi$. Biết $a > 0$, $b > 0$ và $c \in (-\pi; 0)$. Tính giá trị của biểu thức $P = a + b + c + d$.
            """)
            
            q2_ans = st.radio(
                "Chọn phương án đúng:",
                [
                    r"A. $P = 6 - \dfrac{\pi}{3}$",
                    r"B. $P = 4 + \dfrac{\pi}{3}$",
                    r"C. $P = 5 - \dfrac{\pi}{6}$",
                    r"D. $P = 3 + \dfrac{\pi}{2}$"
                ],
                key="q2",
                index=None
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # CÂU 3: CÂU HỎI TRẢ LỜI NGẮN (ĐIỀN ĐÁP ÁN)
        # ---------------------------------------------------------------------
        with st.container(border=True):
            st.markdown("""
            <div class="question-title">
                <span class="tag-badge">DẠNG 3: TRẢ LỜI NGẮN</span> Câu 3: Mực nước cảng biển
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(r"""
            Mực nước tại một cảng biển được mô hình hóa bởi hàm số $h(t) = 3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12$ (mét), trong đó $t$ là thời gian tính bằng giờ ($0 \le t \le 24$). Một tàu hàng yêu cầu mực nước tối thiểu là $13,5\text{ m}$ để cập cảng an toàn. Trong một ngày ($24$ giờ), tổng thời gian tàu có thể cập cảng an toàn là bao nhiêu giờ?
            """)
            
            q3_ans = st.text_input("Nhập kết quả dạng số (Ví dụ: 8):", key="q3")

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # CÂU 4: CÂU HỎI ĐÚNG / SAI (GỒM 4 PHÁT BIỂU)
        # ---------------------------------------------------------------------
        with st.container(border=True):
            st.markdown("""
            <div class="question-title">
                <span class="tag-badge">DẠNG 4: TRẮC NGHIỆM ĐÚNG / SAI</span> Câu 4: Phân tích nghiệm phương trình lượng giác
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(r"""
            Cho phương trình lượng giác: $2\cos^2 x - (2m+1)\cos x + m = 0 \quad (1)$. Xét tính đúng/sai của các phát biểu sau:
            """)
            
            q4_a = st.radio(r"a) Phương trình (1) có thể phân tích thành nhân tử dạng $(\cos x - m)(2\cos x - 1) = 0$.", ["Đúng", "Sai"], key="q4_1", horizontal=True)
            q4_b = st.radio(r"b) Khi $m = 1$, phương trình có đúng $2$ nghiệm phân biệt trên đoạn $[0; 2\pi]$.", ["Đúng", "Sai"], key="q4_2", horizontal=True)
            q4_c = st.radio(r"c) Để phương trình có đúng $3$ nghiệm phân biệt trên đoạn $[0; 2\pi]$ thì $m = -1$.", ["Đúng", "Sai"], key="q4_3", horizontal=True)
            q4_d = st.radio(r"d) Có tồn tại giá trị thực của $m$ để phương trình đã cho hoàn toàn vô nghiệm.", ["Đúng", "Sai"], key="q4_4", horizontal=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # NÚT NỘP BÀI THI
        submit_btn = st.form_submit_button("🚀 NỘP BÀI THI TSA", type="primary", use_container_width=True)
        
        if submit_btn:
            st.session_state.exam_submitted = True
            st.rerun()

# 7. MÀN HÌNH BÁO KẾT QUẢ VÀ LỜI GIẢI CHI TIẾT
else:
    st.balloons()
    st.success("🎉 BẠN ĐÃ HOÀN THÀNH BÀI THI TSA!")
    
    # Tính điểm
    total_score = 0.0
    
    # Kiểm tra Câu 1
    c1_correct = (st.session_state.get("q1_a") == "-50" and 
                  st.session_state.get("q1_w") == r"\dfrac{2\pi}{15}" and 
                  st.session_state.get("q1_b") == "60" and 
                  st.session_state.get("q1_t") == "5")
    if c1_correct: total_score += 2.5
    
    # Kiểm tra Câu 2
    c2_correct = st.session_state.get("q2") and st.session_state.get("q2").startswith("A.")
    if c2_correct: total_score += 2.5
    
    # Kiểm tra Câu 3
    c3_correct = st.session_state.get("q3", "").strip() == "8"
    if c3_correct: total_score += 2.5
    
    # Kiểm tra Câu 4
    c4_score = 0
    if st.session_state.get("q4_1") == "Đúng": c4_score += 1
    if st.session_state.get("q4_2") == "Sai": c4_score += 1
    if st.session_state.get("q4_3") == "Đúng": c4_score += 1
    if st.session_state.get("q4_4") == "Sai": c4_score += 1
    
    if c4_score == 4: total_score += 2.5
    elif c4_score == 3: total_score += 1.5
    elif c4_score == 2: total_score += 0.75
    elif c4_score == 1: total_score += 0.25

    # Hiển thị điểm số
    st.markdown(f"""
    <div style="background-color: #ffebee; border: 2px solid #b71c1c; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
        <h2 style="color: #b71c1c; margin: 0;">TỔNG ĐIỂM BÀI THI: {total_score:.2f} / 10.0</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📖 LỜI GIẢI CHI TIẾT CÁC CÂU HỎI")

    # Lời giải Câu 1
    with st.expander("🔍 Lời giải Câu 1: Mô hình Vòng quay Mặt Trời"):
        st.markdown(r"""
        - Độ cao tâm vòng quay là vị trí cân bằng $\Rightarrow B = 60$.
        - Bán kính vòng quay ứng với biên độ $|A| = 50$. Tại $t=0$ cabin ở vị trí thấp nhất $h(0) = 10\text{m} \Rightarrow A\cos(0) + 60 = 10 \Rightarrow A = -50$.
        - Chu kỳ $T = 15$ phút $\Rightarrow \omega = \dfrac{2\pi}{T} = \dfrac{2\pi}{15}$.
        - Phương trình độ cao: $h(t) = -50\cos\left(\dfrac{2\pi}{15}t\right) + 60$.
        - Để đạt độ cao $85\text{m}$: $-50\cos\left(\dfrac{2\pi}{15}t\right) + 60 = 85 \Leftrightarrow \cos\left(\dfrac{2\pi}{15}t\right) = -\dfrac{1}{2} \Rightarrow \dfrac{2\pi}{15}t = \dfrac{2\pi}{3} \Rightarrow t = 5$ (phút).
        """)

    # Lời giải Câu 2
    with st.expander("🔍 Lời giải Câu 2: Đọc đồ thị hàm số lượng giác"):
        st.markdown(r"""
        - Đường trung bình $d = \dfrac{y_{\max} + y_{\min}}{2} = \dfrac{4 + (-2)}{2} = 1$.
        - Biên độ $a = \dfrac{y_{\max} - y_{\min}}{2} = \dfrac{4 - (-2)}{2} = 3$.
        - Tần số góc $b = \dfrac{2\pi}{T} = \dfrac{2\pi}{\pi} = 2$.
        - Pha ban đầu $c = -\dfrac{\pi}{3}$ thỏa mãn $c \in (-\pi; 0)$.
        - Tổng $P = a + b + c + d = 3 + 2 - \dfrac{\pi}{3} + 1 = 6 - \dfrac{\pi}{3}$.
        - **Chọn đáp án A.**
        """)

    # Lời giải Câu 3
    with st.expander("🔍 Lời giải Câu 3: Mực nước cảng biển"):
        st.markdown(r"""
        - Điều kiện tàu cập cảng an toàn: $3\cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) + 12 \ge 13,5 \Leftrightarrow \cos\left(\dfrac{\pi t}{6} + \dfrac{\pi}{3}\right) \ge \dfrac{1}{2}$.
        - Giải bất phương trình lượng giác thu được: $-4 + 12k \le t \le 12k$.
        - Xét $t \in [0; 24]$:
          + Với $k = 1 \Rightarrow 8 \le t \le 12$ ($4$ tiếng).
          + Với $k = 2 \Rightarrow 20 \le t \le 24$ ($4$ tiếng).
        - Tổng thời gian tàu cập cảng an toàn là $4 + 4 = 8$ giờ.
        """)

    # Lời giải Câu 4
    with st.expander("🔍 Lời giải Câu 4: Phân tích nghiệm phương trình lượng giác"):
        st.markdown(r"""
        - **a) Đúng:** $2\cos^2 x - (2m+1)\cos x + m = 0 \Leftrightarrow (2\cos x - 1)(\cos x - m) = 0$.
        - **b) Sai:** Khi $m = 1$, phương trình cho $4$ nghiệm phân biệt trên $[0; 2\pi]$ bao gồm $x \in \left\{0; \dfrac{\pi}{3}; \dfrac{5\pi}{3}; 2\pi\right\}$.
        - **c) Đúng:** Để có $3$ nghiệm phân biệt trên $[0; 2\pi]$, nhánh $\cos x = m$ phải sinh ra đúng $1$ nghiệm phân biệt độc lập $\Rightarrow m = -1$ (cho nghiệm $x = \pi$).
        - **d) Sai:** Nhân tử $(2\cos x - 1) = 0$ luôn cho $2$ nghiệm cố định $\Rightarrow$ Phương trình luôn có nghiệm với mọi $m$.
        """)
