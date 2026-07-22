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
        "Đề 2: Khối đa diện và Thể tích (Ví dụ)",
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
    <h1 style="text-align: center; color: #00a88f;">BÀI 1. SỰ BIẾN THIÊN VÀ CỰC TRỊ CỦA HÀM SỐ</h1>
    """, 
    unsafe_allow_html=True
    )
    st.markdown("---")

    if not st.session_state[key_nop_bai]:
        with st.form("form_de_1"):
            
            # =====================================================================
            # PHẦN 1: TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN (12 CÂU)
            # =====================================================================
            st.header("Phần 1. Câu hỏi trắc nghiệm nhiều phương án lựa chọn")
            st.caption("Thí sinh trả lời từ câu 1 đến câu 12. Mỗi câu hỏi chỉ chọn 1 phương án. (Mỗi câu đúng 0.25 điểm)")
            
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
                    st.image("images/cau2_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau2_p1.png")
            st.markdown("Hàm số đã cho đồng biến trên khoảng nào dưới đây?")
            p1_q2 = st.radio("C2:", [r"A. $(7; +\infty)$", r"B. $(-2; 3)$", r"C. $(-\infty; -2)$", r"D. $(-2; 0)$"], key="p1_q2", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 3:** Cho hàm số $y=f(x)$ có bảng biến thiên như sau:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau3_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau3_p1.png")
            st.markdown("Hàm số đã cho nghịch biến trên khoảng nào dưới đây?")
            p1_q3 = st.radio("C3:", [r"A. $(-2; 0)$", r"B. $(-\infty; 0)$", r"C. $(1; 3)$", r"D. $(3; +\infty)$"], key="p1_q3", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 4:** Cho hàm số $y=f'(x)$ có đồ thị là đường cong trong hình vẽ dưới đây:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau4_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau4_p1.png")
            st.markdown("Hàm số $y=f(x)$ đồng biến trên khoảng nào sau đây?")
            p1_q4 = st.radio("C4:", [r"A. $(-\infty; -1)$", r"B. $(-1; 1)$", r"C. $(1; 4)$", r"D. $(1; +\infty)$"], key="p1_q4", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 5:** Hàm số nào sau đây nghịch biến trên $\\mathbb{R}$?")
            p1_q5 = st.radio("C5:", [r"A. $y = -x^3 + 3x^2 - 9x$", r"B. $y = -x^3 + x + 1$", r"C. $y = \frac{x-1}{x-2}$", r"D. $y = 2x^2 + 3x + 2$"], key="p1_q5", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 6:** Cho hàm số $y=f(x)$ có đồ thị là đường cong như hình vẽ bên dưới:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau6_p1.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau6_p1.png")
            st.markdown("Hàm số $f(x)$ đạt cực đại tại điểm nào sau đây?")
            p1_q6 = st.radio("C6:", [r"A. $x = 1$", r"B. $x = -1$", r"C. $y = 3$", r"D. $M(-1; 3)$"], key="p1_q6", label_visibility="collapsed")
            st.divider()

            st.markdown("**Câu 7:** Cho hàm số $y=f(x)$ xác định trên $\\mathbb{R}$ và có bảng biến thiên như hình vẽ sau:")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau7_p1.png", width=400)
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

            st.markdown(r"**Câu 9:** Hàm số $y=\frac{x^2-3x+5}{x+1}$ nghịch biến trên các khoảng nào?")
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
            st.header("Phần 2. Trắc nghiệm lựa chọn đúng sai")
            st.caption("Thí sinh trả lời từ câu 1 đến câu 4. Trong mỗi ý a), b), c), d) chọn đúng hoặc sai.")
            
            # --- Câu 1 ---
            st.markdown("**Câu 1:** Cho hàm số bậc bốn $y=f(x)$. Hàm số $y=f'(x)$ có đồ thị như hình dưới đây")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau1_p2.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau1_p2.png")
            
            p2_q1 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số $y=f(x)$ đồng biến trên khoảng $(-\infty; 0)$"); p2_q1["a"] = c2.radio("p2c1a", ["Đúng", "Sai"], key="p2_q1_a", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Hàm số đồng biến trên khoảng $(-1; 1)$"); p2_q1["b"] = c2.radio("p2c1b", ["Đúng", "Sai"], key="p2_q1_b", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số $y=f(x)$ nghịch biến trên khoảng $(-\infty; 0)$"); p2_q1["c"] = c2.radio("p2c1c", ["Đúng", "Sai"], key="p2_q1_c", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("d) Hàm số $y=f(x)$ nghịch biến trên khoảng $(1; 2)$"); p2_q1["d"] = c2.radio("p2c1d", ["Đúng", "Sai"], key="p2_q1_d", horizontal=True, label_visibility="collapsed")
            st.divider()

            # --- Câu 2 ---
            st.markdown(r"**Câu 2:** Cho hàm số $y=f(x)=\frac{x^2+3x}{x-1}$.")
            p2_q2 = {}
            c1, c2 = st.columns([4, 1]); c1.markdown("a) Hàm số $f(x)$ đồng biến trên khoảng $(-\infty; 1)$"); p2_q2["a"] = c2.radio("p2c2a", ["Đúng", "Sai"], key="p2_q2_a", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("b) Cực đại của hàm số $f(x)$ là $1$"); p2_q2["b"] = c2.radio("p2c2b", ["Đúng", "Sai"], key="p2_q2_b", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("c) Hàm số $f(x)$ có ba điểm cực trị"); p2_q2["c"] = c2.radio("p2c2c", ["Đúng", "Sai"], key="p2_q2_c", horizontal=True, label_visibility="collapsed")
            c1, c2 = st.columns([4, 1]); c1.markdown("d) Hàm số $f(x)$ nghịch biến trên khoảng $(-1; 3)$"); p2_q2["d"] = c2.radio("p2c2d", ["Đúng", "Sai"], key="p2_q2_d", horizontal=True, label_visibility="collapsed")
            st.divider()

            # --- Câu 3 ---
            st.markdown(r"**Câu 3:** Cho hàm số $y=2^{x^2 - 3x + \frac{13}{4}}$.")
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
            st.header("Phần 3. Câu hỏi trắc nghiệm trả lời ngắn")
            st.caption("Thí sinh trả lời từ câu 1 đến câu 6. Điền kết quả dạng số vào ô trống. (Mỗi câu đúng 0.5 điểm)")
            
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
                    st.image("images/cau3_p3.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau3_p3.png")
            p3_q3 = st.text_input("Nhập đáp án Câu 3:", key="p3_q3")
            st.divider()

            st.markdown("**Câu 4:** Xét một chất điểm chuyển động trên một trục số nằm ngang, vị trí $s(t) = t^3 - 9t^2 + 15t, t \ge 0$. Hỏi có bao nhiêu giá trị $t$ nguyên để chất điểm chuyển động sang trái?")
            p3_q4 = st.text_input("Nhập đáp án Câu 4:", key="p3_q4")
            st.divider()

            st.markdown("**Câu 5:** Máng trượt của một cầu trượt cho trẻ em được uốn từ một tấm kim loại bề rộng 80 cm. Gọi $S$ là diện tích mặt cắt ngang. Với $x$ đạt giá trị bằng bao nhiêu thì cầu trượt đảm bảo an toàn nhất cho trẻ em?")
            try: 
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("images/cau5_p3.png", width=400)
            except: 
                st.warning("⚠️ Lỗi: Thiếu file ảnh images/cau5_p3.png")
            p3_q5 = st.text_input("Nhập đáp án Câu 5:", key="p3_q5")
            st.divider()

            st.markdown(r"**Câu 6:** Giả sử doanh số của một sản phẩm mới tuân theo quy luật logistic $f(t) = \frac{5000}{1+5e^{-t}}, t \ge 0$. Hỏi sau khi phát hành bao nhiêu năm thì tốc độ bán hàng là lớn nhất? (quy tròn đến hàng phần trăm).")
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
            **Câu 8 (B):** TXĐ: $\mathbb{R} \setminus \{-1\}$. $y' = \frac{3}{(x+1)^2} > 0$. Hàm số đồng biến trên $(-\infty; -1)$ và $(-1; +\infty)$.
            **Câu 9 (D):** $y' = \frac{x^2+2x-8}{(x+1)^2}$. Cho $y' = 0 \Leftrightarrow x = -4 \lor x = 2$. Lập BBT ta thấy hàm số nghịch biến trên $(-4; -1)$ và $(-1; 2)$.
            **Câu 10 (A):** $f'(x) = 0 \Leftrightarrow x=0, x=-1, x=3$. Qua $x=-1$, $f'(x)$ đổi dấu từ $-$ sang $+$. Đồng biến trên $(-\infty; -1)$.
            **Câu 11 (C):** $y' = \frac{x^2-8x+15}{(x-4)^2} = 0 \Leftrightarrow x=3, x=5$. BBT cho thấy $x_{CĐ}=3, x_{CT}=5$.
            **Câu 12 (B):** $y' = \frac{-x^2-4x+5}{(x+2)^2} = 0 \Leftrightarrow x=1, x=-5$. BBT cho thấy cực tiểu tại $x = -5$.
            """)

        st.subheader("Phần 2: Trắc nghiệm lựa chọn đúng sai")
        with st.expander("🔍 Câu 1 & Câu 2"):
            st.markdown(r"""
            **Câu 1:** (a-Sai, b-Đúng, c-Sai, d-Đúng). 
            *Giải thích:* Đồ thị $f'(x)$ nằm trên trục $Ox$ (dương) ở $(-1; 1)$ và $(2; +\infty)$ nên đồng biến. Đồ thị $f'(x)$ âm ở $(-\infty; -1)$ và $(1; 2)$ nên nghịch biến.
            
            **Câu 2:** (a-Sai, b-Đúng, c-Sai, d-Sai).
            *Giải thích:* $y' = \frac{x^2-2x-3}{(x-1)^2} = 0 \Leftrightarrow x=-1 \lor x=3$. Có 2 điểm cực trị, cực đại tại $x=-1 \Rightarrow y=1$. Không xác định tại $x=1$ nên không nghịch biến trên $(-1; 3)$.
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
            
            **Câu 3 (Ans: 3):** Phương trình $y'=0$ có nghiệm $x_1, x_2 > 0 \Rightarrow -\frac{2b}{3a}>0, \frac{c}{3a}>0$. Do nhánh phải đi lên $\Rightarrow a>0$. Do đó $b<0, c>0$. Cắt $Oy$ tại $d>0 \Rightarrow a,c,d > 0$ (Có 3 số dương).
            
            **Câu 4 (Ans: 3):** Vận tốc $v(t) = s'(t) = 3t^2 - 18t + 15 < 0 \Leftrightarrow 1 < t < 5$. Do $t \in \mathbb{Z} \Rightarrow t \in \{2, 3, 4\}$.
            
            **Câu 5 (Ans: 20):** Bề rộng $2x+y = 80 \Rightarrow y = 80-2x$. Diện tích $S(x) = x(80-2x) = -2x^2 + 80x$. $S'(x) = -4x + 80 = 0 \Leftrightarrow x=20$ cm.
            
            **Câu 6 (Ans: 1.61):** Tốc độ bán hàng $h(t) = f'(t) = \frac{25000e^{-t}}{(1+5e^{-t})^2}$. Khảo sát $h'(t)=0 \Leftrightarrow 1-5e^{-t}=0 \Leftrightarrow t = \ln 5 \approx 1.61$ năm.
            """)

# ==================== XỬ LÝ NỘI DUNG ĐỀ 2 ====================
elif de_thi_chon == "Đề 2: Khối đa diện và Thể tích (Ví dụ)":
    key_nop_bai = "submitted_de2"
    if key_nop_bai not in st.session_state:
        st.session_state[key_nop_bai] = False
        
    st.title("ĐỀ 2: KHỐI ĐA DIỆN VÀ THỂ TÍCH")
    st.markdown("---")
    
    if not st.session_state[key_nop_bai]:
        with st.form("form_de_2"):
            st.markdown("**Câu 1 (Đề 2):** Nội dung câu hỏi khối đa diện...")
            q1_d2 = st.radio("C1_d2", [r"A. Đáp án A", r"B. Đáp án B", r"C. Đáp án C", r"D. Đáp án D"], label_visibility="collapsed")
            st.divider()
            
            submitted_2 = st.form_submit_button("Nộp Bài Thi Đề 2", type="primary")
            if submitted_2:
                st.session_state[key_nop_bai] = True
                st.session_state.q1_d2_ans = q1_d2
                st.rerun()
    else:
        score_d2 = 0
        if "q1_d2_ans" in st.session_state and st.session_state.q1_d2_ans.startswith("A."):
            score_d2 += 0.25
            
        st.success(f"🎉 Bạn đã hoàn thành Đề 2! Tổng điểm: **{score_d2}**")
        
        if st.button("🔄 Làm lại Đề 2"):
            st.session_state[key_nop_bai] = False
            st.rerun()
            
        st.markdown("---")
        st.header("📖 LỜI GIẢI CHI TIẾT ĐỀ 2")
        with st.expander("🔍 Câu 1: Xem lời giải chi tiết"):
            st.markdown("**Đáp án đúng:** A")
            st.markdown("**Hướng dẫn giải:** Lời giải chi tiết cho câu hỏi khối đa diện...")

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
