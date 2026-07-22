import streamlit as st
import time

# ==================== CẤU HÌNH TRANG & FONT CHỮ ====================
st.set_page_config(page_title="Hệ thống thi thử Toán THPT", layout="wide")

st.markdown("""
    <style>
    /* Ép toàn bộ chữ và công thức Toán học dùng font Times New Roman */
    html, body, [class*="css"] {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 18px !important; 
    }
    .katex {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 1.1em !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== MENU & ĐỒNG HỒ 90 PHÚT (SIDEBAR) ====================
with st.sidebar:
    st.header("📂 DANH SÁCH ĐỀ THI")
    danh_sach_de = [
        "Đề 1: Sự biến thiên và cực trị của hàm số",
        "Đề 2: Sự biến thiên và cực trị của hàm số",
        "Đề 3: Hàm số mũ và Lôgarit (Ví dụ)"  # <--- Thêm Đề 3 vào đây
    ]
    de_thi_chon = st.selectbox("Chọn đề thi:", danh_sach_de)
        
    st.markdown("---")
    st.header("⏱️ THỜI GIAN LÀM BÀI")
    
    from streamlit.components.v1 import html
    dong_ho_html = """
    <div style="font-family: 'Times New Roman', serif; font-size: 28px; font-weight: bold; color: #d9534f; background-color: #f8f9fa; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #ddd;">
        <span id="timer">90:00</span>
    </div>
    <script>
        var totalSeconds = 90 * 60;
        var timerElement = document.getElementById('timer');
        var timer = setInterval(function() {
            var minutes = Math.floor(totalSeconds / 60);
            var seconds = totalSeconds % 60;
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            timerElement.textContent = minutes + ":" + seconds;
            if (totalSeconds <= 0) {
                clearInterval(timer);
                timerElement.textContent = "HẾT GIỜ!";
            } else {
                totalSeconds--;
            }
        }, 1000);
    </script>
    """
    html(dong_ho_html, height=70)

# ==================== XỬ LÝ NỘI DUNG ĐỀ 1 ====================
if de_thi_chon == "Đề 1: Sự biến thiên và cực trị của hàm số":
    key_nop_bai = "submitted_de1"
    if key_nop_bai not in st.session_state:
        st.session_state[key_nop_bai] = False
        
    st.markdown(
    """
    <h1 style="text-align: center; color: #00a88f;">ĐỀ 1. SỰ BIẾN THIÊN VÀ CỰC TRỊ CỦA HÀM SỐ</h1>
    """, 
    unsafe_allow_html=True
    )
    st.markdown("---")

    if not st.session_state[key_nop_bai]:
        with st.form("form_de_1"):
            
            # =====================================================================
            # PHẦN 1: TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN (12 CÂU)
            # =====================================================================
            st.markdown( """
            <h2 style="color: #0000FF;">Phần 1. Câu hỏi trắc nghiệm nhiều phương án lựa chọn</h2>
            """, 
            unsafe_allow_html=True
            )
            st.markdown(
                '<em style="color: #0000FF;"><b>Thí sinh trả lời từ câu 1 đến câu 12. Mỗi câu hỏi chỉ chọn 1 phương án. (Mỗi câu đúng 0.25 điểm)</b></em>', 
                unsafe_allow_html=True
            )
            
            st.markdown("**Câu 1:** Hàm số $y=f(x)$ liên tục trên $\\mathbb{R}$ có bảng biến thiên hàm số $y=f'(x)$ như hình dưới:")
            try:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/Cau1_p1.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau1_p1.png")
            
            st.markdown("Số điểm cực trị của hàm số $y=f(x)$ là")
            p1_q1 = st.radio("C1:", [r"A. $4$", r"B. $1$", r"C. $2$", r"D. $3$"], key="p1_q1", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 2:** Cho hàm số bậc bốn $y=f(x)$ có đồ thị là đường cong trong hình dưới đây:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau2_p1.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau2_p1.png")
            st.markdown("Hàm số đã cho đồng biến trên khoảng nào dưới đây?")
            p1_q2 = st.radio("C2:", [r"A. $(7; +\infty)$", r"B. $(-2; 3)$", r"C. $(-\infty; -2)$", r"D. $(-2; 0)$"], key="p1_q2", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 3:** Cho hàm số $y=f(x)$ có bảng biến thiên như sau:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau3_p1.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau3_p1.png")
            st.markdown("Hàm số đã cho nghịch biến trên khoảng nào dưới đây?")
            p1_q3 = st.radio("C3:", [r"A. $(-2; 0)$", r"B. $(-\infty; 0)$", r"C. $(1; 3)$", r"D. $(3; +\infty)$"], key="p1_q3", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 4:** Cho hàm số $y=f'(x)$ có đồ thị là đường cong trong hình vẽ dưới đây:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau4_p1.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau4_p1.png")
            st.markdown("Hàm số $y=f(x)$ đồng biến trên khoảng nào sau đây?")
            p1_q4 = st.radio("C4:", [r"A. $(-\infty; -1)$", r"B. $(-1; 1)$", r"C. $(1; 4)$", r"D. $(1; +\infty)$"], key="p1_q4", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 5:** Hàm số nào sau đây nghịch biến trên $\\mathbb{R}$?")
            p1_q5 = st.radio("C5:", [r"A. $y = -x^3 + 3x^2 - 9x$", r"B. $y = -x^3 + x + 1$", r"C. $y = \dfrac{x-1}{x-2}$", r"D. $y = 2x^2 + 3x + 2$"], key="p1_q5", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 6:** Cho hàm số $y=f(x)$ có đồ thị là đường cong như hình vẽ bên dưới:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau6_p1.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau6_p1.png")
            st.markdown("Hàm số $f(x)$ đạt cực đại tại điểm nào sau đây?")
            p1_q6 = st.radio("C6:", [r"A. $x = 1$", r"B. $x = -1$", r"C. $y = 3$", r"D. $M(-1; 3)$"], key="p1_q6", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 7:** Cho hàm số $y=f(x)$ xác định trên $\\mathbb{R}$ và có bảng biến thiên như hình vẽ sau:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau7_p1.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau7_p1.png")
            st.markdown("Giá trị cực tiểu của hàm số $y=f(x)$ là")
            p1_q7 = st.radio("C7:", [r"A. $-10$", r"B. $11$", r"C. $6$", r"D. $-20$"], key="p1_q7", label_visibility="collapsed")
            st.divider()

            st.markdown(r"**Câu 8:** Cho hàm số $y=\frac{x-2}{x+1}$, khẳng định nào sau đây là đúng?")
            p1_q8 = st.radio("C8:", [
                r"A. Hàm số đồng biến trên $(-\infty; -1) \cup (-1; +\infty)$", 
                r"B. Hàm số đồng biến trên $(-\infty; -1)$ và $(-1; +\infty)$", 
                r"C. Hàm số đồng biến trên $\mathbb{R} \setminus \{-1\}$", 
                r"D. Hàm số đồng biến trên $(-\infty; 1)$"
            ], key="p1_q8", label_visibility="collapsed")
            st.divider()

            st.markdown(r"**Câu 9:** Hàm số $y=\dfrac{x^2-3x+5}{x+1}$ nghịch biến trên các khoảng nào?")
            p1_q9 = st.radio("C9:", [
                r"A. $(-4; 2)$", 
                r"B. $(-\infty; -2)$", 
                r"C. $(-\infty; -1)$ và $(-1; +\infty)$", 
                r"D. $(-4; -1)$ và $(-1; 2)$"
            ], key="p1_q9", label_visibility="collapsed")
            st.divider()

            st.markdown(r"**Câu 10:** Cho hàm số $y=f(x)$ xác định trên $\mathbb{R}$ và có đạo hàm $f'(x) = 12x^{2025}(x+1)(3-x), \forall x \in \mathbb{R}$. Hàm số đã cho đồng biến trên khoảng nào sau đây?")
            p1_q10 = st.radio("C10:", [r"A. $(-\infty; -1)$", r"B. $(-1; 3)$", r"C. $(3; +\infty)$", r"D. $(-\infty; 0)$"], key="p1_q10", label_visibility="collapsed")
            st.divider()

            st.markdown(r"**Câu 11:** Cho hàm số $y=\dfrac{x^2-2x-7}{x-4}$. Phát biểu nào sau đây là đúng?")
            p1_q11 = st.radio("C11:", [
                r"A. $x_{CT} = 3, x_{CĐ} = 5$", 
                r"B. $x_{CT} = -3, x_{CĐ} = 5$", 
                r"C. $x_{CT} = 5, x_{CĐ} = 3$", 
                r"D. $x_{CT} = 5, x_{CĐ} = -3$"
            ], key="p1_q11", label_visibility="collapsed")
            st.divider()

            st.markdown(r"**Câu 12:** Điểm cực tiểu của hàm số $y=\dfrac{-x^2+2x-1}{x+2}$ là")
            p1_q12 = st.radio("C12:", [r"A. $x = 1$", r"B. $x = -5$", r"C. $x = 2$", r"D. $x = 5$"], key="p1_q12", label_visibility="collapsed")
            st.divider()

            # =====================================================================
            # PHẦN 2: TRẮC NGHIỆM ĐÚNG/SAI (4 CÂU)
            # =====================================================================
            st.markdown(
                """
                <h2 style="color: #0000FF;">Phần 2. Trắc nghiệm lựa chọn đúng/sai</h2>
                """, 
                unsafe_allow_html=True
            )
            st.markdown(
                '<em style="color: #0000FF;"><b>Thí sinh trả lời từ câu 1 đến câu 4. Trong mỗi ý a), b), c), d) chọn đúng hoặc sai.</b></em>', 
                unsafe_allow_html=True
            )
            
            # --- Câu 1 ---
            st.markdown("**Câu 1:** Cho hàm số bậc bốn $y=f(x)$. Hàm số $y=f'(x)$ có đồ thị như hình dưới đây")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau1_p2.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau1_p2.png")
            
            p2_q1 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số $y=f(x)$ đồng biến trên khoảng $(-\infty; 0)$"); p2_q1["a"] = c2.radio("p2c1a", ["Đúng", "Sai"], key="p2_q1_a", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Hàm số đồng biến trên khoảng $(-1; 1)$"); p2_q1["b"] = c2.radio("p2c1b", ["Đúng", "Sai"], key="p2_q1_b", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số $y=f(x)$ nghịch biến trên khoảng $(-\infty; 0)$"); p2_q1["c"] = c2.radio("p2c1c", ["Đúng", "Sai"], key="p2_q1_c", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("d) Hàm số $y=f(x)$ nghịch biến trên khoảng $(1; 2)$"); p2_q1["d"] = c2.radio("p2c1d", ["Đúng", "Sai"], key="p2_q1_d", horizontal=True, label_visibility="collapsed")
            st.divider()

            # --- Câu 2 ---
            st.markdown(r"**Câu 2:** Cho hàm số $y=f(x)=\dfrac{x^2+3x}{x-1}$.")
            p2_q2 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số $f(x)$ đồng biến trên khoảng $(-\infty; 1)$"); p2_q2["a"] = c2.radio("p2c2a", ["Đúng", "Sai"], key="p2_q2_a", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Cực đại của hàm số $f(x)$ là $1$"); p2_q2["b"] = c2.radio("p2c2b", ["Đúng", "Sai"], key="p2_q2_b", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số $f(x)$ có ba điểm cực trị"); p2_q2["c"] = c2.radio("p2c2c", ["Đúng", "Sai"], key="p2_q2_c", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("d) Hàm số $f(x)$ nghịch biến trên khoảng $(-1; 3)$"); p2_q2["d"] = c2.radio("p2c2d", ["Đúng", "Sai"], key="p2_q2_d", horizontal=True, label_visibility="collapsed")
            st.divider()

            # --- Câu 3 ---
            st.markdown(r"**Câu 3:** Cho hàm số $y=2^{x^2 - 3x + \dfrac{13}{4}}$.")
            p2_q3 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số nghịch biến trên khoảng $(-1; 0)$"); p2_q3["a"] = c2.radio("p2c3a", ["Đúng", "Sai"], key="p2_q3_a", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Hàm số đồng biến trên khoảng $(0; 1)$"); p2_q3["b"] = c2.radio("p2c3b", ["Đúng", "Sai"], key="p2_q3_b", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số có giá trị cực tiểu $y_{CT} = 2$"); p2_q3["c"] = c2.radio("p2c3c", ["Đúng", "Sai"], key="p2_q3_c", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("d) Hàm số có 2 điểm cực trị"); p2_q3["d"] = c2.radio("p2c3d", ["Đúng", "Sai"], key="p2_q3_d", horizontal=True, label_visibility="collapsed")
            st.divider()

            # --- Câu 4 ---
            st.markdown(r"**Câu 4:** Cho hàm số $y=\log_2(x^2 - 4x + 5)$ có đồ thị là $(C)$.")
            p2_q4 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số có tập xác định là $D=\mathbb{R}$"); p2_q4["a"] = c2.radio("p2c4a", ["Đúng", "Sai"], key="p2_q4_a", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Hàm số đồng biến trên $\mathbb{R}$"); p2_q4["b"] = c2.radio("p2c4b", ["Đúng", "Sai"], key="p2_q4_b", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số đạt cực tiểu tại $x=2$"); p2_q4["c"] = c2.radio("p2c4c", ["Đúng", "Sai"], key="p2_q4_c", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown(r"d) Giả sử đồ thị $(C)$ cắt đường thẳng $y=1$ tại $A, B$ và điểm cực trị $M$. Bán kính đường tròn ngoại tiếp $\Delta MAB$ bằng $2$."); p2_q4["d"] = c2.radio("p2c4d", ["Đúng", "Sai"], key="p2_q4_d", horizontal=True, label_visibility="collapsed")
            st.divider()
            
            # =====================================================================
            # PHẦN 3: TRẢ LỜI NGẮN (6 CÂU)
            # =====================================================================
            st.markdown(
                """
                <h2 style="color: #0000FF;">Phần 3. Câu hỏi trắc nghiệm trả lời ngắn</h2>
                """, 
                unsafe_allow_html=True
            )
            st.markdown(
                '<em style="color: #0000FF;"><b>Thí sinh trả lời từ câu 1 đến câu 6. Điền kết quả dạng số vào ô trống. (Mỗi câu đúng 0.5 điểm)</b></em>', 
                unsafe_allow_html=True
            )

            
            st.markdown("**Câu 1:** Biết đường thẳng đi qua hai điểm cực trị của đồ thị của hàm số $y = -x^3 + 3x^2 + 9x + 1$ là $ax+by+4=0$. Tính $a+2b$.")
            p3_q1 = st.text_input("Nhập đáp án Câu 1:", key="p3_q1")
            st.divider()

            st.markdown("**Câu 2:** Biết đồ thị hàm số $y=ax^3+bx^2+cx+d$ có hai điểm cực trị $A(1; -7), B(2; -8)$. Tính $y(-1)$")
            p3_q2 = st.text_input("Nhập đáp án Câu 2:", key="p3_q2")
            st.divider()
            
            st.markdown("**Câu 3:** Cho hàm số $y=ax^3+bx^2+cx+d$ ($a,b,c \in \mathbb{R}$) có bảng xét dấu đạo hàm. Biết phương trình $y'=0$ có 2 nghiệm dương phân biệt. Có bao nhiêu số dương trong các số $a, b, c$?")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau3_p3.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau3_p3.png")
            p3_q3 = st.text_input("Nhập đáp án Câu 3:", key="p3_q3")
            st.divider()

            st.markdown("**Câu 4:** Xét một chất điểm chuyển động trên một trục số nằm ngang, vị trí $s(t) = t^3 - 9t^2 + 15t, t \ge 0$. Hỏi có bao nhiêu giá trị $t$ nguyên để chất điểm chuyển động sang trái?")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau4_p3.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau4_p3.PNG")
            p3_q4 = st.text_input("Nhập đáp án Câu 4:", key="p3_q4")
            st.divider()

            st.markdown("**Câu 5:** Máng trượt của một cầu trượt cho trẻ em được uốn từ một tấm kim loại bề rộng 80 cm. Gọi $S$ là diện tích mặt cắt ngang. Với $x$ đạt giá trị bằng bao nhiêu thì cầu trượt đảm bảo an toàn nhất cho trẻ em?")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau5_p3.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau5_p3.png")
            p3_q5 = st.text_input("Nhập đáp án Câu 5:", key="p3_q5")
            st.divider()

            st.markdown(r"**Câu 6:** Giả sử doanh số của một sản phẩm mới tuân theo quy luật logistic $f(t) = \dfrac{5000}{1+5e^{-t}}, t \ge 0$. Hỏi sau khi phát hành bao nhiêu năm thì tốc độ bán hàng là lớn nhất? (quy tròn đến hàng phần trăm).")
            p3_q6 = st.text_input("Nhập đáp án Câu 6:", key="p3_q6")
            st.divider()

            # NÚT NỘP BÀI
            submitted = st.form_submit_button("Nộp Bài Thi", type="primary")
            
            if submitted:
                st.session_state[key_nop_bai] = True
                st.session_state.p1 = [p1_q1, p1_q2, p1_q3, p1_q4, p1_q5, p1_q6, p1_q7, p1_q8, p1_q9, p1_q10, p1_q11, p1_q12]
                st.session_state.p2 = [p2_q1, p2_q2, p2_q3, p2_q4]
                st.session_state.p3 = [p3_q1, p3_q2, p3_q3, p3_q4, p3_q5, p3_q6]
                st.rerun()

    # ==================== XỬ LÝ CHẤM ĐIỂM & ĐÁP ÁN ĐỀ 1 ====================
    else:
        tong_diem = 0.0
        
        p1_ans_key = ["C", "C", "C", "B", "A", "B", "D", "B", "D", "A", "C", "B"]
        for i in range(12):
            if st.session_state.p1[i].startswith(f"{p1_ans_key[i]}."):
                tong_diem += 0.25
                
        p2_ans_key = [
            {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Sai"},
            {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"},
            {"a": "Đúng", "b": "Sai", "c": "Đúng", "d": "Sai"}
        ]
        for i in range(4):
            dung_so_y = 0
            for k in ["a", "b", "c", "d"]:
                if st.session_state.p2[i][k] == p2_ans_key[i][k]:
                    dung_so_y += 1
            if dung_so_y == 1: tong_diem += 0.1
            elif dung_so_y == 2: tong_diem += 0.25
            elif dung_so_y == 3: tong_diem += 0.5
            elif dung_so_y == 4: tong_diem += 1.0

        p3_ans_key = ["6", "-35", "3", "3", "20", "1.61"]
        for i in range(6):
            if st.session_state.p3[i].strip() == p3_ans_key[i]:
                tong_diem += 0.5
                
        st.balloons()
        st.success(f"🎉 BẠN ĐÃ HOÀN THÀNH BÀI THI! Tổng điểm: **{tong_diem:.2f} / 10.0**")
        
        if st.button("🔄 Làm lại đề này"):
            st.session_state[key_nop_bai] = False
            st.rerun()
            
        st.markdown("---")
        st.header("📖 ĐÁP ÁN & LỜI GIẢI CHI TIẾT")
        
        st.subheader("Phần 1: Trắc nghiệm 4 lựa chọn")
        with st.expander("🔍 Câu 1 - Câu 6"):
            st.markdown(r"""
            **Câu 1 (C):** Phương trình $f'(x)=0$ có hai nghiệm đơn nên hàm số có 2 điểm cực trị.
            
            **Câu 2 (C):** Hàm số đồng biến trên khoảng $(-\infty; -2)$.
            
            **Câu 3 (C):** Từ BBT, hàm số nghịch biến trên $(1; 3)$.
            
            **Câu 4 (B):** Dựa vào đồ thị, $f'(x) > 0, \forall x \in (-1; 1)$ và $(4; +\infty)$.
            
            **Câu 5 (A):** $y = -x^3 + 3x^2 - 9x \Rightarrow y' = -3x^2 + 6x - 9 < 0, \forall x \in \mathbb{R}$.
            
            **Câu 6 (B):** Từ đồ thị, hàm số đạt cực đại tại $x = -1$.
            """)
            
        with st.expander("🔍 Câu 7 - Câu 12"):
            st.markdown(r"""
            **Câu 7 (D):** Dựa vào BBT, giá trị cực tiểu là $y_{CT} = -20$.
            
            **Câu 8 (B):** TXĐ: $\mathbb{R} \setminus \{-1\}$. $y' = \dfrac{3}{(x+1)^2} > 0$. Hàm số đồng biến trên $(-\infty; -1)$ và $(-1; +\infty)$.
            
            **Câu 9 (D):** $y' = \dfrac{x^2+2x-8}{(x+1)^2}$. Cho $y' = 0 \Leftrightarrow x = -4 \lor x = 2$. Lập BBT ta thấy hàm số nghịch biến trên $(-4; -1)$ và $(-1; 2)$.
           
            **Câu 10 (A):** $f'(x) = 0 \Leftrightarrow x=0, x=-1, x=3$. Qua $x=-1$, $f'(x)$ đổi dấu từ $-$ sang $+$. Đồng biến trên $(-\infty; -1)$.
            
            **Câu 11 (C):** $y' = \dfrac{x^2-8x+15}{(x-4)^2} = 0 \Leftrightarrow x=3, x=5$. BBT cho thấy $x_{CĐ}=3, x_{CT}=5$.
           
            **Câu 12 (B):** $y' = \dfrac{-x^2-4x+5}{(x+2)^2} = 0 \Leftrightarrow x=1, x=-5$. BBT cho thấy cực tiểu tại $x = -5$.
            """)

        st.subheader("Phần 2: Trắc nghiệm lựa chọn đúng sai")
        with st.expander("🔍 Câu 1 & Câu 2"):
            st.markdown(r"""
            **Câu 1:** (a-Sai, b-Đúng, c-Sai, d-Đúng). 
            
            *Giải thích:* Đồ thị $f'(x)$ nằm trên trục $Ox$ (dương) ở $(-1; 1)$ và $(2; +\infty)$ nên đồng biến. Đồ thị $f'(x)$ âm ở $(-\infty; -1)$ và $(1; 2)$ nên nghịch biến.
            
            **Câu 2:** (a-Sai, b-Đúng, c-Sai, d-Sai).
            
            *Giải thích:* $y' = \dfrac{x^2-2x-3}{(x-1)^2} = 0 \Leftrightarrow x=-1 \lor x=3$. Có 2 điểm cực trị, cực đại tại $x=-1 \Rightarrow y=1$. Không xác định tại $x=1$ nên không nghịch biến trên $(-1; 3)$.
            """)
            
        with st.expander("🔍 Câu 3 & Câu 4"):
            st.markdown(r"""
            **Câu 3:** (a-Đúng, b-Sai, c-Đúng, d-Sai).
            *Giải thích:* $y' = (2x-3) \cdot 2^{x^2-3x+\frac{13}{4}} \ln 2$. $y'=0 \Leftrightarrow x=\frac{3}{2}$. Hàm số chỉ có 1 điểm cực trị là cực tiểu tại $x=\frac{3}{2}$ với $y_{CT} = 2$.
            
            **Câu 4:** (a-Đúng, b-Sai, c-Đúng, d-Sai).
            *Giải thích:* TXĐ $\mathbb{R}$. $y' = \frac{2x-4}{(x^2-4x+5)\ln 2} = 0 \Leftrightarrow x=2$. Cực tiểu $M(2; 0)$. Giao với $y=1$ cho $A(1; 1), B(3; 1)$. Tam giác $MAB$ vuông tại $M$, bán kính $R = \frac{AB}{2} = 1 \neq 2$.
            """)

        st.subheader("Phần 3: Câu hỏi trả lời ngắn")
        with st.expander("🔍 Lời giải Câu 1 - Câu 6"):
            st.markdown(r"""
            **Câu 1 (Ans: 6):** $y' = -3x^2+6x+9=0 \Leftrightarrow x=-1 \lor x=3$. Điểm CT: $A(-1; -4), B(3; 28)$. Đường thẳng $AB$: $8x-y+4=0 \Rightarrow a=8, b=-1 \Rightarrow a+2b=6$.
            
            **Câu 2 (Ans: -35):** Thế tọa độ cực trị vào hệ phương trình giải ra $a,b,c,d \Rightarrow y = 2x^3 - 9x^2 + 12x - 12$. Tính $y(-1) = -35$.
            
            **Câu 3 (Ans: 3):** Phương trình $y'=0$ có nghiệm $x_1, x_2 > 0 \Rightarrow -\frac{2b}{3a}>0, \dfrac{c}{3a}>0$. Do nhánh phải đi lên $\Rightarrow a>0$. Do đó $b<0, c>0$. Cắt $Oy$ tại $d>0 \Rightarrow a,c,d > 0$ (Có 3 số dương).
            
            **Câu 4 (Ans: 3):** Vận tốc $v(t) = s'(t) = 3t^2 - 18t + 15 < 0 \Leftrightarrow 1 < t < 5$. Do $t \in \mathbb{Z} \Rightarrow t \in \{2, 3, 4\}$.
            
            **Câu 5 (Ans: 20):** Bề rộng $2x+y = 80 \Rightarrow y = 80-2x$. Diện tích $S(x) = x(80-2x) = -2x^2 + 80x$. $S'(x) = -4x + 80 = 0 \Leftrightarrow x=20$ cm.
            
            **Câu 6 (Ans: 1.61):** Tốc độ bán hàng $h(t) = f'(t) = \dfrac{25000e^{-t}}{(1+5e^{-t})^2}$. Khảo sát $h'(t)=0 \Leftrightarrow 1-5e^{-t}=0 \Leftrightarrow t = \ln 5 \approx 1.61$ năm.
            """)

# ==================== XỬ LÝ NỘI DUNG ĐỀ 2 ====================
# ==================== XỬ LÝ NỘI DUNG ĐỀ 2 (TỪ FILE PDF) ====================
elif de_thi_chon == "Đề 2: Sự biến thiên và cực trị của hàm số":
    key_nop_bai = "submitted_de2"
    if key_nop_bai not in st.session_state:
        st.session_state[key_nop_bai] = False
        
    st.markdown(
        '<h1 style="text-align: center; color: #0000FF;">ĐỀ 2: ÔN TẬP SỰ BIẾN THIÊN VÀ CỰC TRỊ</h1>', 
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    if not st.session_state[key_nop_bai]:
        with st.form("form_de_2"):
            
            # =====================================================================
            # PHẦN 1: TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN (12 CÂU)
            # =====================================================================
            st.markdown('<h2 style="color: #0000FF;">Phần 1. Câu hỏi trắc nghiệm nhiều phương án lựa chọn</h2>', unsafe_allow_html=True)
            st.markdown('<em style="color: #0000FF;"><b>Thí sinh trả lời từ câu 1 đến câu 12. Mỗi câu hỏi chỉ chọn 1 phương án. (Mỗi câu đúng 0.25 điểm)</b></em>', unsafe_allow_html=True)
            
            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 1:</span> Cho hàm số $f(x)$ có đạo hàm liên tục trên $\\mathbb{R}$. Mệnh đề nào sau đây đúng?', unsafe_allow_html=True)
            p1_q1_d2 = st.radio("C1_d2", [
                r"A. Nếu $f'(x) \neq 0, \forall x \in \mathbb{R}$ thì hàm số $f(x)$ đồng biến trên $\mathbb{R}$", 
                r"B. Nếu $f'(x) > 0, \forall x \in \mathbb{R}$ thì hàm số $f(x)$ đồng biến trên $\mathbb{R}$", 
                r"C. Nếu $f'(x) = 0, \forall x \in \mathbb{R}$ thì hàm số $f(x)$ đồng biến trên $\mathbb{R}$", 
                r"D. Nếu $f'(x) < 0, \forall x \in \mathbb{R}$ thì hàm số $f(x)$ đồng biến trên $\mathbb{R}$"
            ], key="p1_q1_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 2:</span> Cho hàm số bậc bốn có đồ thị như hình vẽ dưới đây:', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau2_p1_d2.PNG", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau2_p1.png")
            st.markdown('Điểm cực tiểu của đồ thị hàm số đã cho là')
            p1_q2_d2 = st.radio("C2_d2", [r"A. $x=-1$", r"B. $x=0$", r"C. $x=2$", r"D. $A(0;-1)$"], key="p1_q2_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 3:</span> Hàm số nào sau đây nghịch biến trên tập xác định của nó?', unsafe_allow_html=True)
            p1_q3_d2 = st.radio("C3_d2", [
                r"A. $y=\dfrac{2x+1}{x-3}$", 
                r"B. $y=-x^3+2x^2-15x-1$", 
                r"C. $y=-2x^2+1$", 
                r"D. $y=x^3-2x^2+2024x+5$"
            ], key="p1_q3_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 4:</span> Cho hàm số $y=f(x)$ có bảng biến thiên sau:', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau4_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau4_p1.png")
            st.markdown('Hàm số đã cho nghịch biến trên khoảng nào dưới đây?')
            p1_q4_d2 = st.radio("C4_d2", [r"A. $(-1;1)$", r"B. $(4;+\infty)$", r"C. $(-\infty;2)$", r"D. $(0;1)$"], key="p1_q4_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 5:</span> Cho hàm số $y=f(x)$ có bảng biến thiên như sau:', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau5_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau5_p1.png")
            st.markdown('Hàm số đồng biến trên khoảng nào dưới đây?')
            p1_q5_d2 = st.radio("C5_d2", [r"A. $(2;+\infty)$", r"B. $(-2;+\infty)$", r"C. $(-\infty;0)$", r"D. $(-\infty;2)$"], key="p1_q5_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 6:</span> Hàm số $y=(x^2-1)(3x-2)^3$ có bao nhiêu điểm cực đại?', unsafe_allow_html=True)
            p1_q6_d2 = st.radio("C6_d2", [r"A. $0$", r"B. $2$", r"C. $3$", r"D. $1$"], key="p1_q6_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 7:</span> Cho hàm số $y=f(x)$ có $f^{\prime}(x)=(x+2)(x+1)(x^2-1), \forall x \in \mathbb{R}$. Hàm số $y=f(x)$ đồng biến trên khoảng nào sau đây?', unsafe_allow_html=True)
            p1_q7_d2 = st.radio("C7_d2", [r"A. $(-1;1)$", r"B. $(0;+\infty)$", r"C. $(-\infty;-2)$", r"D. $(-2;-1)$"], key="p1_q7_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 8:</span> Cho hàm số $y=f(x)$ có bảng biến thiên như sau:', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau8_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau8_p1.png")
            st.markdown('Giá trị cực đại của $f(x)$ là')
            p1_q8_d2 = st.radio("C8_d2", [r"A. $4$", r"B. $8$", r"C. $10$", r"D. $-2$"], key="p1_q8_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 9:</span> Tính giá trị cực đại của hàm số $y=\dfrac{\ln x}{x}$.', unsafe_allow_html=True)
            p1_q9_d2 = st.radio("C9_d2", [r"A. $\dfrac{1}{e}$", r"B. $1$", r"C. $e$", r"D. $0$"], key="p1_q9_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 10:</span> Cho hàm số $y=f(x)$ có bảng biến thiên như sau:', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau10_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau10_p1.png")
            st.markdown('Hàm số đã cho nghịch biến trên khoảng nào dưới đây?')
            p1_q10_d2 = st.radio("C10_d2", [r"A. $(0;4)$", r"B. $(0;2)$", r"C. $(-1;1)$", r"D. $(-\infty;-1)$"], key="p1_q10_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 11:</span> Cho hàm số $y=f(x)$ liên tục trên $\mathbb{R}$ và có bảng xét dấu $f^{\prime}(x)$ như sau:', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau11_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau11_p1.png")
            st.markdown('Hàm số $y=f(x)$ có bao nhiêu điểm cực trị?')
            p1_q11_d2 = st.radio("C11_d2", [r"A. $3$", r"B. $2$", r"C. $1$", r"D. $4$"], key="p1_q11_d2", label_visibility="collapsed")
            st.divider()

            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 12:</span> Biết $M(1;-5)$ là một điểm cực trị của đồ thị hàm số $y=f(x)=x^3+ax^2+bx+1$. Giá trị $f(2)$ bằng', unsafe_allow_html=True)
            p1_q12_d2 = st.radio("C12_d2", [r"A. $-3$", r"B. $-21$", r"C. $3$", r"D. $15$"], key="p1_q12_d2", label_visibility="collapsed")
            st.divider()

            # =====================================================================
            # PHẦN 2: TRẮC NGHIỆM ĐÚNG/SAI (4 CÂU)
            # =====================================================================
            st.markdown('<h2 style="color: #0000FF;">Phần 2. Trắc nghiệm lựa chọn đúng sai</h2>', unsafe_allow_html=True)
            st.markdown('<em style="color: #0000FF;"><b>Thí sinh trả lời từ câu 1 đến câu 4. Trong mỗi ý a), b), c), d) chọn đúng hoặc sai.</b></em>', unsafe_allow_html=True)
            
            # --- Câu 1 ---
            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 1:</span> Cho hàm số $y=f(x)$ có bảng biến thiên như sau:', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau1_p2.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau1_p2.png")
            
            p2_q1_d2 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số $y=f(x)$ đồng biến trên khoảng $(-\infty; 2)$."); p2_q1_d2["a"] = c2.radio("p2c1a_d2", ["Đúng", "Sai"], key="p2_q1_a_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Hàm số $y=f(x)$ nghịch biến trên khoảng $(0;3)$."); p2_q1_d2["b"] = c2.radio("p2c1b_d2", ["Đúng", "Sai"], key="p2_q1_b_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số $y=f(x)$ đạt cực đại tại $x=2$."); p2_q1_d2["c"] = c2.radio("p2c1c_d2", ["Đúng", "Sai"], key="p2_q1_c_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("d) Giá trị cực tiểu của hàm số $y=f(x)$ là $y=-4$."); p2_q1_d2["d"] = c2.radio("p2c1d_d2", ["Đúng", "Sai"], key="p2_q1_d_d2", horizontal=True, label_visibility="collapsed")
            st.divider()

            # --- Câu 2 ---
            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 2:</span> Cho hàm số bậc ba $y=f(x)$ có đồ thị là đường cong như hình vẽ sau', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau2_p2.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau2_p2.png")
            st.markdown('Mỗi khẳng định sau đây đúng hay sai?')
            p2_q2_d2 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số $y=f(x)$ đồng biến trên khoảng $(-\infty;3)$."); p2_q2_d2["a"] = c2.radio("p2c2a_d2", ["Đúng", "Sai"], key="p2_q2_a_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Tổng giá trị cực đại và giá trị cực tiểu của hàm số $y=f(x)$ là $2$."); p2_q2_d2["b"] = c2.radio("p2c2b_d2", ["Đúng", "Sai"], key="p2_q2_b_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số $y=f(x)$ có hai cực trị trái dấu."); p2_q2_d2["c"] = c2.radio("p2c2c_d2", ["Đúng", "Sai"], key="p2_q2_c_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("d) Phương trình đường thẳng qua 2 điểm cực trị của đồ thị hàm số $y=f(x)$ là $d:y=-3x$."); p2_q2_d2["d"] = c2.radio("p2c2d_d2", ["Đúng", "Sai"], key="p2_q2_d_d2", horizontal=True, label_visibility="collapsed")
            st.divider()

            # --- Câu 3 ---
            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 3:</span> Cho hàm số bậc bốn trùng phương $f(x)$ có bảng biến thiên như sau:', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau3_p2.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau3_p2.png")
            p2_q3_d2 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số đồng biến trên $(-1;1)$."); p2_q3_d2["a"] = c2.radio("p2c3a_d2", ["Đúng", "Sai"], key="p2_q3_a_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Độ dài đoạn thẳng nối hai điểm cực tiểu là $2$."); p2_q3_d2["b"] = c2.radio("p2c3b_d2", ["Đúng", "Sai"], key="p2_q3_b_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số $f(2x)$ nghịch biến trên $(0;1)$."); p2_q3_d2["c"] = c2.radio("p2c3c_d2", ["Đúng", "Sai"], key="p2_q3_c_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown(r"d) Số điểm cực trị của hàm số $y=\frac{1}{x^4}[f(x)-1]^4$ là $5$."); p2_q3_d2["d"] = c2.radio("p2c3d_d2", ["Đúng", "Sai"], key="p2_q3_d_d2", horizontal=True, label_visibility="collapsed")
            st.divider()

            # --- Câu 4 ---
            st.markdown('<span style="color: #0000FF; font-weight: bold;">Câu 4:</span> Cho hàm số $y=f(x)$ có đạo hàm $f^{\prime}(x)=(x+1)e^x$.', unsafe_allow_html=True)
            p2_q4_d2 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số nghịch biến trên $(-\infty;-1)$."); p2_q4_d2["a"] = c2.radio("p2c4a_d2", ["Đúng", "Sai"], key="p2_q4_a_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Giá trị cực tiểu của hàm số là $0$."); p2_q4_d2["b"] = c2.radio("p2c4b_d2", ["Đúng", "Sai"], key="p2_q4_b_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số $f(x^2)$ đồng biến trên $(-1;+\infty)$."); p2_q4_d2["c"] = c2.radio("p2c4c_d2", ["Đúng", "Sai"], key="p2_q4_c_d2", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown(r"d) Có $2025$ giá trị nguyên của tham số $m$ trong $[-2024;2025]$ để hàm số $g(x)=f(\ln x)-mx^2+4mx-2$ nghịch biến trên $(e;e^{2024})$."); p2_q4_d2["d"] = c2.radio("p2c4d_d2", ["Đúng", "Sai"], key="p2_q4_d_d2", horizontal=True, label_visibility="collapsed")
            st.divider()
            
            # =====================================================================
            # PHẦN 3: TRẢ LỜI NGẮN (6 CÂU)
            # =====================================================================
            st.markdown('<h2 style="color: #0000FF;">Phần 3. Câu hỏi trắc nghiệm trả lời ngắn</h2>', unsafe_allow_html=True)
            st.markdown('<em style="color: #0000FF;"><b>Thí sinh trả lời từ câu 1 đến câu 6. Điền kết quả dạng số vào ô trống. (Mỗi câu đúng 0.5 điểm)</b></em>', unsafe_allow_html=True)
            
            st.markdown(r'<span style="color: #0000FF; font-weight: bold;">Câu 1:</span> Biết rằng tất cả các khoảng nghịch biến của hàm số $y=\frac{x^2+2x+2}{x+1}$ là hai khoảng $(a;b), (b;c)$ với $a<b<c$. Tính $T=a+b+c$', unsafe_allow_html=True)
            p3_q1_d2 = st.text_input("Nhập đáp án Câu 1:", key="p3_q1_d2")
            st.divider()

            st.markdown(r'<span style="color: #0000FF; font-weight: bold;">Câu 2:</span> Biết rằng đồ thị hàm số $y=x^4-2ax^2+b$ có một điểm cực trị là $(1;2)$. Tính khoảng cách giữa điểm cực đại và điểm cực tiểu của đồ thị hàm số đã cho (quy tròn đến hàng phần trăm).', unsafe_allow_html=True)
            p3_q2_d2 = st.text_input("Nhập đáp án Câu 2:", key="p3_q2_d2")
            st.divider()
            
            st.markdown(r'<span style="color: #0000FF; font-weight: bold;">Câu 3:</span> Biết rằng hai điểm cực trị của đồ thị hàm số $y=\frac{x^2+2x-3}{x^2+1}$ cùng với điểm $I(-\sqrt{5};-\sqrt{5})$ tạo thành một tam giác. Diện tích tam giác đó bằng (kết quả làm tròn đến hàng phần trăm).', unsafe_allow_html=True)
            p3_q3_d2 = st.text_input("Nhập đáp án Câu 3:", key="p3_q3_d2")
            st.divider()

            st.markdown(r'<span style="color: #0000FF; font-weight: bold;">Câu 4:</span> Xí nghiệp A sản xuất độc quyền một loại sản phẩm. Biết rằng hàm tổng chi phí sản xuất là $TC=x^3-77x^2+1000x+40000$ và hàm doanh thu là $TR=-2x^2+1312x$, với $x$ là số sản phẩm. Lợi nhuận của xí nghiệp A được xác định bằng hàm số $f(x)=TR-TC$, cực đại lợi nhuận của xí nghiệp A khi đó đạt bao nhiêu sản phẩm?', unsafe_allow_html=True)
            p3_q4_d2 = st.text_input("Nhập đáp án Câu 4:", key="p3_q4_d2")
            st.divider()

            st.markdown(r'<span style="color: #0000FF; font-weight: bold;">Câu 5:</span> Hàm số $y=\log_3(x^2-2x)$ nghịch biến trên khoảng $(-\infty;a)$ có độ dài lớn nhất. Khi đó $a$ bằng?', unsafe_allow_html=True)
            p3_q5_d2 = st.text_input("Nhập đáp án Câu 5:", key="p3_q5_d2")
            st.divider()

            st.markdown(r'<span style="color: #0000FF; font-weight: bold;">Câu 6:</span> Lát cắt ngang của một vùng đất ven biển được mô hình hoá thành một hàm số bậc ba $y=f(x)$ có đồ thị như hình vẽ (đơn vị độ dài trên các trục là km).', unsafe_allow_html=True)
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/d2_cau6_p3.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/d2_cau6_p3.png")
            st.markdown(r'Biết khoảng cách hai bên chân đồi $OA=2$ km, độ rộng của hồ $AB=1$ km và ngọn đồi cao $528$ m. Tìm độ sâu của hồ (tính bằng mét) tại điểm sâu nhất? (làm tròn đến hàng đơn vị).', unsafe_allow_html=True)
            p3_q6_d2 = st.text_input("Nhập đáp án Câu 6:", key="p3_q6_d2")
            st.divider()

            # NÚT NỘP BÀI
            submitted_2 = st.form_submit_button("Nộp Bài Thi Đề 2", type="primary")
            
            if submitted_2:
                st.session_state[key_nop_bai] = True
                st.session_state.p1_d2 = [p1_q1_d2, p1_q2_d2, p1_q3_d2, p1_q4_d2, p1_q5_d2, p1_q6_d2, p1_q7_d2, p1_q8_d2, p1_q9_d2, p1_q10_d2, p1_q11_d2, p1_q12_d2]
                st.session_state.p2_d2 = [p2_q1_d2, p2_q2_d2, p2_q3_d2, p2_q4_d2]
                st.session_state.p3_d2 = [p3_q1_d2, p3_q2_d2, p3_q3_d2, p3_q4_d2, p3_q5_d2, p3_q6_d2]
                st.rerun()

    # ==================== XỬ LÝ CHẤM ĐIỂM & ĐÁP ÁN ĐỀ 2 ====================
    else:
        tong_diem_d2 = 0.0
        
        # Chấm điểm Phần 1
        p1_ans_key_d2 = ["B", "B", "B", "D", "A", "D", "C", "B", "A", "C", "A", "C"]
        for i in range(12):
            if st.session_state.p1_d2[i].startswith(f"{p1_ans_key_d2[i]}."):
                tong_diem_d2 += 0.25
                
        # Chấm điểm Phần 2
        p2_ans_key_d2 = [
            {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            {"a": "Sai", "b": "Đúng", "c": "Đúng", "d": "Sai"},
            {"a": "Sai", "b": "Đúng", "c": "Sai", "d": "Đúng"},
            {"a": "Đúng", "b": "Sai", "c": "Sai", "d": "Sai"}
        ]
        for i in range(4):
            dung_so_y = 0
            for k in ["a", "b", "c", "d"]:
                if st.session_state.p2_d2[i][k] == p2_ans_key_d2[i][k]:
                    dung_so_y += 1
            if dung_so_y == 1: tong_diem_d2 += 0.1
            elif dung_so_y == 2: tong_diem_d2 += 0.25
            elif dung_so_y == 3: tong_diem_d2 += 0.5
            elif dung_so_y == 4: tong_diem_d2 += 1.0

        # Chấm điểm Phần 3
        p3_ans_key_d2 = ["-3", "1.41", "6.71", "52", "0", "158"]
        for i in range(6):
            ans_hs = st.session_state.p3_d2[i].strip().replace(",", ".")
            if ans_hs == p3_ans_key_d2[i]:
                tong_diem_d2 += 0.5
                
        st.balloons()
        st.success(f"🎉 BẠN ĐÃ HOÀN THÀNH BÀI THI! Tổng điểm: **{tong_diem_d2:.2f} / 10.0**")
        
        if st.button("🔄 Làm lại Đề 2"):
            st.session_state[key_nop_bai] = False
            st.rerun()
            
        st.markdown("---")
        st.markdown('<h2 style="color: #0000FF;">📖 ĐÁP ÁN & LỜI GIẢI CHI TIẾT ĐỀ 2</h2>', unsafe_allow_html=True)
        
        st.subheader("Phần 1: Trắc nghiệm nhiều phương án lựa chọn")
        with st.expander("🔍 Lời giải Câu 1 - Câu 6"):
            st.markdown(r"""
            **Câu 1 (B):** Hàm số $f(x)$ có đạo hàm liên tục trên $\mathbb{R}$ thì hàm số $f(x)$ đồng biến trên $\mathbb{R}$ khi $f'(x)>0, \forall x \in \mathbb{R}$[cite: 1].
            
            **Câu 2 (B):** Dựa vào đồ thị, điểm cực tiểu của đồ thị hàm số đã cho là $x=0$[cite: 1].
            
            **Câu 3 (B):** Hàm số $y=-x^3+2x^2-15x-1$ có TXĐ $D=\mathbb{R}$[cite: 1]. Ta có $y' = -3x^2+4x-15 < 0, \forall x \in \mathbb{R}$ (vì $a=-3<0$ và $\Delta' = 4 - (-3)(-15) = -41 < 0$)[cite: 1]. Vậy hàm số nghịch biến trên $\mathbb{R}$[cite: 1].
            
            **Câu 4 (D):** Dựa vào bảng biến thiên ta thấy hàm số nghịch biến trên khoảng $(-1;0)$ và $(0;1)$[cite: 1].
            
            **Câu 5 (A):** Từ bảng biến thiên của hàm số ta có hàm số đồng biến trên hai khoảng $(-\infty;-1)$ và $(-1;+\infty)$ do vậy hàm số đồng biến trên khoảng $(2;+\infty)$[cite: 1].
            
            **Câu 6 (D):** $y' = (3x-2)^2(15x^2-4x-9)$[cite: 1]. Vì $(3x-2)^2 \ge 0, \forall x \in \mathbb{R}$ nên dấu của $y'$ là dấu của biểu thức $15x^2-4x-9$[cite: 1]. Phương trình $15x^2-4x-9=0$ có hai nghiệm phân biệt là $x=\frac{2\pm\sqrt{139}}{15}$[cite: 1]. Lập bảng biến thiên ta suy ra hàm số có 1 điểm cực đại[cite: 1].
            """)
            
        with st.expander("🔍 Lời giải Câu 7 - Câu 12"):
            st.markdown(r"""
            **Câu 7 (C):** Ta có $f'(x)=0 \Leftrightarrow (x+2)(x+1)(x^2-1)=0 \Leftrightarrow x=-2, x=-1, x=1$[cite: 1]. Qua bảng xét dấu đạo hàm, hàm số đồng biến trên khoảng $(-\infty;-2)$ và $(1;+\infty)$[cite: 1].
            
            **Câu 8 (B):** Dựa vào bảng biến thiên, ta suy ra giá trị cực đại của hàm số $f(x)$ bằng $8$[cite: 1].
            
            **Câu 9 (A):** Tập xác định: $D=(0;+\infty)$[cite: 1]. Có $y' = \frac{1-\ln x}{x^2}$[cite: 1]. Phương trình $y'=0 \Leftrightarrow \ln x = 1 \Leftrightarrow x=e$[cite: 1]. Dựa vào bảng biến thiên, hàm số có giá trị cực đại $y = \frac{1}{e}$[cite: 1].
            
            **Câu 10 (C):** Từ bảng biến thiên suy ra hàm số nghịch biến trên khoảng $(-1;1)$[cite: 1].
            
            **Câu 11 (A):** Vì hàm số $y=f(x)$ liên tục trên $\mathbb{R}$ và $f'(x)$ đổi dấu 3 lần nên hàm số $y=f(x)$ có 3 điểm cực trị[cite: 1].
            
            **Câu 12 (C):** Ta có: $y' = f'(x) = 3x^2+2ax+b$[cite: 1]. Vì $M(1;-5)$ là một điểm cực trị của đồ thị hàm số $y=f(x)$, ta có hệ $\begin{cases} f'(1)=0 \\ f(1)=5 \end{cases} \Leftrightarrow \begin{cases} 2a+b=-3 \\ a+b=3 \end{cases} \Leftrightarrow \begin{cases} a=-6 \\ b=9 \end{cases}$[cite: 1]. Vậy $f(x)=x^3-6x^2+9x+1 \Rightarrow f(2)=3$[cite: 1].
            """)

        st.subheader("Phần 2: Trắc nghiệm lựa chọn đúng sai")
        with st.expander("🔍 Lời giải Câu 1 & Câu 2"):
            st.markdown(r"""
            **Câu 1:** (a-Sai, b-Đúng, c-Sai, d-Đúng)[cite: 1]. 
            *Giải thích:*
            - Hàm số $y=f(x)$ đồng biến trên các khoảng $(-\infty;0)$ và $(3;+\infty)$[cite: 1].
            - Hàm số $y=f(x)$ nghịch biến trên khoảng $(0;3)$[cite: 1].
            - Hàm số $y=f(x)$ đạt cực đại tại $x=0$[cite: 1].
            - Giá trị cực tiểu của hàm số $y=f(x)$ là $y=-4$[cite: 1].
            
            **Câu 2:** (a-Sai, b-Đúng, c-Đúng, d-Sai)[cite: 1].
            *Giải thích:*
            - Hàm số $y=f(x)$ đồng biến trên các khoảng $(-\infty;-1)$ và $(1;+\infty)$[cite: 1].
            - Giá trị cực đại là $y=3$, giá trị cực tiểu là $y=-1$. Tổng là $3 + (-1) = 2$[cite: 1].
            - Hàm số $y=f(x)$ có hai cực trị là $x=\pm 1$ (trái dấu)[cite: 1].
            - Đường thẳng qua hai điểm cực trị $A(-1;3), B(1;-1)$ có phương trình $d: y = -2x+1$[cite: 1].
            """)
            
        with st.expander("🔍 Lời giải Câu 3 & Câu 4"):
            st.markdown(r"""
            **Câu 3:** (a-Sai, b-Đúng, c-Sai, d-Đúng)[cite: 1].
            *Giải thích:*
            - Sai vì hàm số nghịch biến trên $(0;1)$[cite: 1].
            - Hai điểm cực tiểu có tọa độ $(-1;-1)$ và $(1;-1)$. Độ dài đoạn nối là $\sqrt{(1+1)^2+(-1+1)^2} = 2$[cite: 1].
            - Ta có $[f(2x)]' = 2f'(2x) = 0 \Leftrightarrow x=-\frac{1}{2}, x=0, x=\frac{1}{2}$[cite: 1]. Khảo sát thấy hàm số đồng biến trên khoảng $(\frac{1}{2};1)$[cite: 1].
            - Giả sử $f(x)=ax^4+bx^2+c \Rightarrow f(x)=2x^4-4x^2+1$[cite: 1]. Khi đó $y = \frac{1}{x^4}[2x^4-4x^2]^4 = 2^4 x^4(x^2-2)^4$[cite: 1]. Có $y' = 2^4 \cdot 4 \cdot x^3(x^2-2)^3(3x^2-2)$[cite: 1]. Xét $y'=0$ có $5$ nghiệm bội lẻ nên hàm số có $5$ điểm cực trị[cite: 1].
            
            **Câu 4:** (a-Đúng, b-Sai, c-Sai, d-Sai)[cite: 1].
            *Giải thích:*
            - $f'(x) = (x+1)e^x$ đổi dấu tại $x=-1$, đúng[cite: 1].
            - Không đủ cơ sở để xác định hàm số $f(x)$ nên không xác định được giá trị cực tiểu[cite: 1].
            - Ta có $[f(x^2)]' = 2xf'(x^2) = 2x(x^2+1)e^{x^2} = 0 \Leftrightarrow x=0$. Hàm số nghịch biến trên $(-1;0)$[cite: 1].
            - Ta có $g'(x) = \ln x + 1 - 2mx + 4m \le 0, \forall x \in (e; e^{2024}) \Leftrightarrow 2m \ge \frac{\ln x + 1}{x-2}$[cite: 1]. Khảo sát hàm số suy ra $m \ge \frac{1}{e-2} \Rightarrow m \ge 2$[cite: 1]. Do $m \in [-2024; 2025]$ nên $m \in \{2; 3; \dots; 2025\}$ (có $2024$ giá trị)[cite: 1].
            """)

        st.subheader("Phần 3: Câu hỏi trả lời ngắn")
        with st.expander("🔍 Lời giải Câu 1 - Câu 6"):
            st.markdown(r"""
            **Câu 1 (Đáp án: -3):** Tập xác định: $\mathbb{R} \setminus \{-1\}$. Ta có $y' = \frac{x^2+2x}{(x+1)^2} = 0 \Leftrightarrow x=0, x=-2$[cite: 1]. Hàm số nghịch biến trên $(-2;-1)$ và $(-1;0)$ $\Rightarrow a=-2, b=-1, c=0 \Rightarrow T = -3$[cite: 1].
            
            **Câu 2 (Đáp án: 1.41):** Đồ thị có điểm cực trị $(1;2) \Rightarrow a=1, b=3$[cite: 1]. Hàm số $y'=4x^3-4x = 0 \Leftrightarrow x=0, x=1, x=-1$[cite: 1]. Đồ thị có 2 điểm cực tiểu $A(-1;2), B(1;2)$ và 1 điểm cực đại $C(0;3)$[cite: 1]. Khoảng cách $AC = \sqrt{(0-1)^2+(3-2)^2} = \sqrt{2} \approx 1.41$[cite: 1].
            
            **Câu 3 (Đáp án: 6.71):** Tập xác định $\mathbb{R}$[cite: 1]. $y' = \frac{-2x^2+8x+2}{(x^2+1)^2} = 0 \Leftrightarrow x=2-\sqrt{5}, x=2+\sqrt{5}$[cite: 1]. Hai điểm cực trị là $A(2-\sqrt{5}; -1-\sqrt{5})$ và $B(2+\sqrt{5}; -1+\sqrt{5})$[cite: 1]. Ta tính được $\vec{AB} = (2\sqrt{5}; 2\sqrt{5})$, $\vec{AI} = (2; -1)$[cite: 1]. Diện tích tam giác $S_{ABI} = \frac{1}{2}|ad-bc| = \frac{1}{2}|-2\sqrt{5}-4\sqrt{5}| = 3\sqrt{5} \approx 6.71$[cite: 1].
            
            **Câu 4 (Đáp án: 52):** Hàm lợi nhuận $f(x) = TR - TC = -x^3+75x^2+312x-40000$[cite: 1]. TXĐ $D=(0;+\infty)$[cite: 1]. Có $f'(x) = -3x^2+150x+312 = 0 \Leftrightarrow x=52$ hoặc $x=-2$ (loại)[cite: 1]. Khảo sát BBT ta thấy hàm số đạt giá trị cực đại tại $x=52$[cite: 1].
            
            **Câu 5 (Đáp án: 0):** Tập xác định $D=(-\infty;0) \cup (2;+\infty)$[cite: 1]. Ta có $y' = \frac{2x-2}{(x^2-2x)\ln 3} = 0 \Leftrightarrow x=1$[cite: 1]. Dựa vào BBT, hàm số nghịch biến trên $(-\infty;0)$[cite: 1]. Vậy $a=0$[cite: 1].
            
            **Câu 6 (Đáp án: 158):** Đồ thị $y=f(x)$ đi qua $O(0;0), A(2;0), C(3;0)$ suy ra $y = a(x^3-5x^2+6x)$ với $a>0$[cite: 1]. $y'=a(3x^2-10x+6)=0 \Leftrightarrow x = \frac{5\pm\sqrt{7}}{3}$[cite: 1]. Điểm cực đại $x_{CĐ} = \frac{5-\sqrt{7}}{3}$ với $y_{CĐ} = 0.528$ suy ra $a \approx 0.25$[cite: 1]. Điểm cực tiểu sâu nhất là $x_{CT} = \frac{5+\sqrt{7}}{3}$, tính được $y_{CT} \approx -0.1578$ (km)[cite: 1]. Vậy độ sâu là xấp xỉ $158$ mét[cite: 1].
            """)

# ==================== XỬ LÝ NỘI DUNG ĐỀ 3 ====================
# ==================== XỬ LÝ NỘI DUNG ĐỀ 3 ====================
elif de_thi_chon == "Đề 3: Hàm số mũ và Lôgarit (Ví dụ)":
    key_nop_bai = "submitted_de3"  # Dùng khóa riêng biệt cho Đề 3
    if key_nop_bai not in st.session_state:
        st.session_state[key_nop_bai] = False
        
    st.title("ĐỀ 3: HÀM SỐ MŨ VÀ LÔGARIT")
    st.markdown("---")
    
    if not st.session_state[key_nop_bai]:
        with st.form("form_de_3"):
            st.markdown("**Câu 1 (Đề 3):** Nội dung câu hỏi mũ và lôgarit...")
            q1_d3 = st.radio("C1_d3", [r"A. Đáp án A", r"B. Đáp án B", r"C. Đáp án C", r"D. Đáp án D"], label_visibility="collapsed")
            st.divider()
            
            # Thêm tiếp các câu hỏi 2, 3, 4... của Đề 3 tại đây nếu cần
            
            submitted_3 = st.form_submit_button("Nộp Bài Thi Đề 3", type="primary")
            if submitted_3:
                st.session_state[key_nop_bai] = True
                st.session_state.q1_d3_ans = q1_d3
                st.rerun()
    else:
        # Chấm điểm và hiển thị kết quả Đề 3
        score_d3 = 0
        if "q1_d3_ans" in st.session_state and st.session_state.q1_d3_ans.startswith("A."):
            score_d3 += 0.25
            
        st.success(f"🎉 Bạn đã hoàn thành Đề 3! Tổng điểm: **{score_d3}**")
        
        if st.button("🔄 Làm lại Đề 3"):
            st.session_state[key_nop_bai] = False
            st.rerun()
            
        st.markdown("---")
        st.header("📖 LỜI GIẢI CHI TIẾT ĐỀ 3")
        with st.expander("🔍 Câu 1: Xem lời giải chi tiết"):
            st.markdown("**Đáp án đúng:** A")
            st.markdown("**Hướng dẫn giải:** Lời giải chi tiết cho câu hỏi mũ và lôgarit...")
