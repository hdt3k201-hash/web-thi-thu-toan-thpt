import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Trắc nghiệm Hàm số", layout="centered")

# ==========================================
# 1. QUẢN LÝ ĐĂNG NHẬP (Từ URL WordPress hoặc nhập thủ công)
# ==========================================
# Khởi tạo trạng thái đăng nhập mặc định nếu chưa có
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Đọc thông số từ URL
params = st.query_params

# Nếu trên URL có chứa tham số 'auth_status=success', tự động cho phép xem lời giải
if params.get("auth_status") == "success":
    st.session_state['logged_in'] = True
    st.sidebar.success("✅ Đã đồng bộ tài khoản từ Website!")
else:
    # Nếu không có tham số từ web, hiển thị form đăng nhập dự phòng ở Sidebar
    with st.sidebar:
        st.header("Tài khoản học sinh")
        if not st.session_state['logged_in']:
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            if st.button("Đăng nhập"):
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

# ==========================================
# 2. GIAO DIỆN CHÍNH: CÂU HỎI TRẮC NGHIỆM
# ==========================================
st.markdown(
    """
    <h1 style="text-align: center; color: #CC0000; font-family: 'Segoe UI', Roboto, sans-serif; font-weight: bold; font-size: 2.5em; margin-top: 20px; margin-bottom: 20px;">
        Chuyên đề: Hàm số (Trắc nghiệm)
    </h1>
    """, 
    unsafe_allow_html=True
)
# st.markdown("---")

# ==========================================

# CÂU 1

import streamlit as st

# CÂU 1
# ==========================================
# 1. Hiển thị đề bài trong khung
# MẸO: Thêm <span style="white-space: nowrap;"> bọc quanh công thức toán
# để tránh tình trạng công thức bị rớt dòng làm đôi.
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
        <span style="color: #009900; font-weight: bold;">(THPT Lê Thánh Tông HCM 2026) </span>
        Tiệm cận ngang của đồ thị hàm số 
        <span style="white-space: nowrap;">$y = \dfrac{2x - 3}{x + 1}$</span> 
        là đường thẳng có phương trình:
    </span>
    """, 
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án (Sử dụng LaTeX để tạo vòng tròn màu xanh ngọc)
options = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = -1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $x = -1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $y = 2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $x = 2$."
]

# 3. Sử dụng st.radio với tham số horizontal=True để dàn hàng ngang
user_choice = st.radio(
    "Chọn đáp án của bạn:", 
    options, 
    index=None, 
    key="q1_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q1_check"):
    if user_choice == options[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

# 5. Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q1_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Tập xác định: $D = \mathbb{R} \setminus \{-1\}$") 
        st.markdown(r"Ta có giới hạn của hàm số khi $x \to \pm\infty$:")
        
        st.latex(r"\lim_{x \to +\infty} y = \lim_{x \to +\infty} \dfrac{2x - 3}{x + 1} = 2")
        st.latex(r"\lim_{x \to -\infty} y = \lim_{x \to -\infty} \dfrac{2x - 3}{x + 1} = 2")
        
        st.markdown(r"Do đó, đường thẳng **$y = 2$** là tiệm cận ngang của đồ thị hàm số.")
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")




# ==========================================
# CÂU 2
# ==========================================
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
        <span style="color: #008080; font-weight: bold;">Câu 2. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT ĐH-KHTN HN 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$f(x) = x^3 - 3x + 2$.</span> Giá trị cực đại của hàm số đã cho bằng
    </span>
    """, 
    unsafe_allow_html=True
)

options_q2 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $-1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $0$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $4$."
]

user_choice_q2 = st.radio(
    "Chọn đáp án của bạn cho Câu 2:", 
    options_q2, 
    index=None, 
    key="q2_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q2_check"):
    # Đáp án đúng là D -> tương ứng với options_q2[3]
    if user_choice_q2 == options_q2[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q2 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q2_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Tập xác định: $D = \mathbb{R}$") 
        st.markdown(r"Đạo hàm: $f'(x) = 3x^2 - 3$")
        st.latex(r"f'(x) = 0 \Leftrightarrow \left[\begin{array}{l} x = 1 \\ x = -1 \end{array}\right.")
        
        st.markdown(r"Tính giá trị của hàm số tại các điểm tới hạn:")
        st.markdown(r"- Với $x = 1 \Rightarrow f(1) = 0$ (Giá trị cực tiểu)")
        st.markdown(r"- Với $x = -1 \Rightarrow f(-1) = 4$ (Giá trị cực đại)")
        
        st.markdown(r"Vậy giá trị cực đại của hàm số bằng **$4$**.")
        st.markdown("**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

st.write("---") # Đường gạch ngang phân cách giữa các câu

# ==========================================
# CÂU 3
# ==========================================
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
        <span style="color: #008080; font-weight: bold;">Câu 3. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT ĐH-KHTN HN 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$f(x)$</span> có 
        <span style="white-space: nowrap;">$f(1) = 3$</span> và 
        <span style="white-space: nowrap;">$f'(1) = 2$.</span> Giá trị của 
        <span style="white-space: nowrap;">$\lim_{x \to 1} \dfrac{f^2(x) - 9}{x - 1}$</span> bằng
    </span>
    """, 
    unsafe_allow_html=True
)

options_q3 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $12$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $6$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $18$."
]

user_choice_q3 = st.radio(
    "Chọn đáp án của bạn cho Câu 3:", 
    options_q3, 
    index=None, 
    key="q3_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q3_check"):
    # Đáp án đúng là A -> tương ứng với options_q3[0]
    if user_choice_q3 == options_q3[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q3 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q3_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Ta biến đổi biểu thức cần tính giới hạn:")
        st.latex(r"\lim_{x \to 1} \dfrac{f^2(x) - 9}{x - 1} = \lim_{x \to 1} \dfrac{(f(x) - 3)(f(x) + 3)}{x - 1}")
        
        st.markdown(r"Do $f(1) = 3$, nên ta có thể viết lại thành:")
        st.latex(r"= \lim_{x \to 1} \left[ \dfrac{f(x) - f(1)}{x - 1} \cdot (f(x) + 3) \right]")
        
        st.markdown(r"Theo định nghĩa đạo hàm tại một điểm, ta có $\lim_{x \to 1} \dfrac{f(x) - f(1)}{x - 1} = f'(1)$. Do đó:")
        st.latex(r"= f'(1) \cdot (f(1) + 3)")
        
        st.markdown(r"Thay các giá trị $f(1) = 3$ và $f'(1) = 2$ vào biểu thức, ta được:")
        st.latex(r"= 2 \cdot (3 + 3) = 12")
        
        st.markdown("**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")



# ==========================================
# CÂU 4
# ==========================================
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
        <span style="color: #008080; font-weight: bold;">Câu 4. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT ĐH-KHTN HN 2026) </span>
        Tiệm cận xiên của đồ thị hàm số 
        <span style="white-space: nowrap;">$y = \dfrac{2x^2 + x}{x + 1}$</span> là:
    </span>
    """, 
    unsafe_allow_html=True
)

options_q4 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = 2x + 1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $y = 2x - 3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $y = 2x$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $y = 2x - 1$."
]

user_choice_q4 = st.radio(
    "Chọn đáp án của bạn cho Câu 4:", 
    options_q4, 
    index=None, 
    key="q4_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q4_check"):
    # Đáp án đúng là D -> tương ứng với options_q4[3]
    if user_choice_q4 == options_q4[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q4 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q4_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Thực hiện phép chia đa thức tử số cho mẫu số, ta được:")
        st.latex(r"y = \dfrac{2x^2 + x}{x + 1} = \dfrac{2x(x + 1) - x}{x + 1} = \dfrac{2x(x + 1) - (x + 1) + 1}{x + 1}")
        st.latex(r"y = 2x - 1 + \dfrac{1}{x + 1}")
        
        st.markdown(r"Ta có $\lim_{x \to \pm\infty} \left[ y - (2x - 1) \right] = \lim_{x \to \pm\infty} \dfrac{1}{x + 1} = 0$")
        st.markdown(r"Vậy đường thẳng **$y = 2x - 1$** là tiệm cận xiên của đồ thị hàm số.")
        st.markdown("**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


st.write("---") # Đường gạch ngang phân cách giữa các câu


# ==========================================
# CÂU 5
# ==========================================
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
        <span style="color: #008080; font-weight: bold;">Câu 5. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Đồng Hỷ - Thái Nguyên 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = \dfrac{x + 2026}{x - 2025}$</span> có đồ thị $(C)$. Đồ thị $(C)$ có đường tiệm cận đứng là:
    </span>
    """, 
    unsafe_allow_html=True
)

options_q5 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $x = 2025$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $x = -2024$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $x = 1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $x = 6$."
]

user_choice_q5 = st.radio(
    "Chọn đáp án của bạn cho Câu 5:", 
    options_q5, 
    index=None, 
    key="q5_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q5_check"):
    # Đáp án đúng là A -> tương ứng với options_q5[0]
    if user_choice_q5 == options_q5[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q5 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q5_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Tập xác định: $D = \mathbb{R} \setminus \{2025\}$")
        st.markdown(r"Hàm số là phân thức bậc nhất trên bậc nhất. Đường tiệm cận đứng là nghiệm của mẫu số (và không trùng với nghiệm tử số).")
        st.latex(r"\lim_{x \to 2025^+} \dfrac{x + 2026}{x - 2025} = +\infty")
        st.markdown(r"Vậy tiệm cận đứng của đồ thị hàm số là đường thẳng **$x = 2025$**.")
        st.markdown("**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


st.write("---") # Đường gạch ngang phân cách giữa các câu


# ==========================================
# CÂU 6
# ==========================================
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
        <span style="color: #008080; font-weight: bold;">Câu 6. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Đồng Hỷ - Thái Nguyên 2026) </span>
        Giá trị lớn nhất của hàm số <span style="white-space: nowrap;">$y = x^3 - 3x + 1$</span> trên đoạn <span style="white-space: nowrap;">$[-2; 2]$</span> là:
    </span>
    """, 
    unsafe_allow_html=True
)

options_q6 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $-1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $-2$."
]

user_choice_q6 = st.radio(
    "Chọn đáp án của bạn cho Câu 6:", 
    options_q6, 
    index=None, 
    key="q6_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q6_check"):
    # Đáp án đúng là C -> tương ứng với options_q6[2]
    if user_choice_q6 == options_q6[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q6 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q6_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Xét hàm số $y = x^3 - 3x + 1$ trên đoạn $[-2; 2]$.")
        st.markdown(r"Đạo hàm: $y' = 3x^2 - 3$")
        
        st.latex(r"y' = 0 \Leftrightarrow 3x^2 - 3 = 0 \Leftrightarrow \left[\begin{array}{l} x = 1 \in [-2; 2] \\ x = -1 \in [-2; 2] \end{array}\right.")
        
        st.markdown(r"Ta tính các giá trị tại 2 đầu mút và các điểm làm cho đạo hàm bằng $0$:")
        st.markdown(r"- $y(-2) = (-2)^3 - 3(-2) + 1 = -1$")
        st.markdown(r"- $y(-1) = (-1)^3 - 3(-1) + 1 = 3$")
        st.markdown(r"- $y(1) = 1^3 - 3(1) + 1 = -1$")
        st.markdown(r"- $y(2) = 2^3 - 3(2) + 1 = 3$")
        
        st.markdown(r"So sánh các kết quả trên, ta thấy $\max_{[-2; 2]} y = 3$.")
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")
