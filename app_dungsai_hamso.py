import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Ngân hàng câu hỏi", layout="centered")

# 1. Quản lý trạng thái đăng nhập bằng session_state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Giao diện đăng nhập ở thanh bên (Sidebar)
with st.sidebar:
    st.header("Tài khoản học sinh")
    if not st.session_state['logged_in']:
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập"):
            # Logic kiểm tra (đơn giản hóa cho ví dụ)
            if username == "hocsinh" and password == "123456":
                st.session_state['logged_in'] = True
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu.")
    else:
        st.success("Đã đăng nhập!")
        if st.button("Đăng xuất"):
            st.session_state['logged_in'] = False
            st.rerun()

# 2. Giao diện chính hiển thị câu hỏi
st.title("Chuyên đề: Hàm số")
st.markdown("---")

# CÂU HỎI 1 (ĐÚNG/SAI)
st.markdown(
    r"""
    <span style="
        display: block; 
        border: 1px solid #cccccc; 
        border-left: 4px solid #008080; 
        border-radius: 8px; 
        padding: 15px 20px; 
        background-color: #fcfcfc; 
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        line-height: 1.6;
    ">
        <span style="color: #008080; font-weight: bold;">Câu 1. </span> 
        Cho hàm số $f(x) = e^{7x+1} - 7x$.
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("image_58dcbe.png", use_container_width=True)

st.markdown("**Chọn Đúng (Đ) hoặc Sai (S) cho từng phát biểu:**")

# Hiển thị các phát biểu và tuỳ chọn Đúng/Sai
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(r"**a)** Tập xác định của hàm số là $\mathscr{D} = (0; +\infty)$")
with col2:
    ans_a = st.radio("q1a", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q1_a")

col3, col4 = st.columns([4, 1])
with col3:
    st.markdown(r"**b)** Đạo hàm của hàm số là $f'(x) = 7e^{7x+1} - 7x$")
with col4:
    ans_b = st.radio("q1b", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q1_b")

col5, col6 = st.columns([4, 1])
with col5:
    st.markdown(r"**c)** Tập nghiệm của bất phương trình $f'(x) < 0$ là $\left(-\infty; -\dfrac{1}{7}\right)$")
with col6:
    ans_c = st.radio("q1c", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q1_c")

col7, col8 = st.columns([4, 1])
with col7:
    st.markdown(r"**d)** Hàm số có giá trị cực tiểu là $2$")
with col8:
    ans_d = st.radio("q1d", ["Đ", "S"], index=None, horizontal=True, label_visibility="collapsed", key="q1_d")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q1_check"):
    if None in [ans_a, ans_b, ans_c, ans_d]:
        st.warning("Bạn chưa chọn đủ đáp án cho tất cả các phát biểu (a, b, c, d).")
    else:
        # Đáp án chuẩn: a-Sai, b-Sai, c-Đúng, d-Đúng
        correct_answers = {"a": "S", "b": "S", "c": "Đ", "d": "Đ"}
        user_answers = {"a": ans_a, "b": ans_b, "c": ans_c, "d": ans_d}
        
        # Đếm số câu đúng
        score = sum([1 for k in correct_answers if user_answers[k] == correct_answers[k]])
        
        if score == 4:
            st.success("Tuyệt vời! Bạn đã trả lời chính xác tất cả các phát biểu.")
        else:
            st.error(f"Bạn đã trả lời đúng {score}/4 phát biểu. Hãy xem lại kỹ hơn nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q1_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state['logged_in']:
        st.info("Lời giải chi tiết:")
        st.markdown(r"**a) Mệnh đề Sai:** Hàm số mũ $e^{7x+1}$ và đa thức $-7x$ xác định trên toàn bộ $\mathbb{R}$. Do đó, tập xác định của hàm số là $\mathscr{D} = \mathbb{R}$.")
        
        st.markdown(r"**b) Mệnh đề Sai:** Tính đạo hàm của hàm số:")
        st.latex(r"f'(x) = (7x+1)' \cdot e^{7x+1} - (7x)' = 7e^{7x+1} - 7")
        
        st.markdown(r"**c) Mệnh đề Đúng:** Xét bất phương trình $f'(x) < 0$:")
        st.latex(r"7e^{7x+1} - 7 < 0 \Leftrightarrow e^{7x+1} < 1 \Leftrightarrow 7x + 1 < 0 \Leftrightarrow x < -\frac{1}{7}")
        st.markdown(r"Tập nghiệm của bất phương trình là $\left(-\infty; -\dfrac{1}{7}\right)$.")
        
        st.markdown(r"**d) Mệnh đề Đúng:** Giải phương trình đạo hàm bằng 0:")
        st.latex(r"f'(x) = 0 \Leftrightarrow 7e^{7x+1} - 7 = 0 \Leftrightarrow 7x + 1 = 0 \Leftrightarrow x = -\frac{1}{7}")
        st.markdown(r"Khi $x$ đi qua giá trị $-\dfrac{1}{7}$, đạo hàm $f'(x)$ đổi dấu từ âm sang dương nên hàm số đạt cực tiểu tại $x = -\dfrac{1}{7}$. Giá trị cực tiểu bằng:")
        st.latex(r"f\left(-\frac{1}{7}\right) = e^{7\left(-\frac{1}{7}\right)+1} - 7\left(-\frac{1}{7}\right) = e^0 + 1 = 1 + 1 = 2")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")