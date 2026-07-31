import streamlit as st
import math

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



# ==========================================
# CÂU 7 (Tương ứng Câu 11 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 7. </span> 
        <span style="color: #009900; font-weight: bold;">(Chuyên Trần Phú - Hải Phòng 2026) </span>
        Số điểm cực tiểu của đồ thị hàm số 
        <span style="white-space: nowrap;">$y = \dfrac{1}{5}x^5 - \dfrac{3}{4}x^4 + \dfrac{2}{3}x^3 + \dfrac{1}{2}$</span> là:
    </span>
    """, 
    unsafe_allow_html=True
)

options_q7 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $0$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $1$."
]

user_choice_q7 = st.radio(
    "Chọn đáp án của bạn cho Câu 7:", 
    options_q7, 
    index=None, 
    key="q7_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q7_check"):
    # Đáp án đúng là D -> tương ứng với options_q7[3]
    if user_choice_q7 == options_q7[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q7 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q7_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Tập xác định: $D = \mathbb{R}$")
        st.markdown(r"Đạo hàm:")
        st.latex(r"y' = x^4 - 3x^3 + 2x^2 = x^2(x^2 - 3x + 2)")
        st.latex(r"y' = 0 \Leftrightarrow x^2(x - 1)(x - 2) = 0 \Leftrightarrow \left[\begin{array}{l} x = 0 \text{ (nghiệm kép)} \\ x = 1 \text{ (nghiệm đơn)} \\ x = 2 \text{ (nghiệm đơn)} \end{array}\right.")
        
        st.markdown(r"Qua nghiệm kép $x = 0$, đạo hàm $y'$ không đổi dấu.")
        st.markdown(r"Qua nghiệm đơn $x = 1$, $y'$ đổi dấu từ $(+)$ sang $(-)$ nên $x = 1$ là điểm cực đại.")
        st.markdown(r"Qua nghiệm đơn $x = 2$, $y'$ đổi dấu từ $(-)$ sang $(+)$ nên $x = 2$ là điểm cực tiểu.")
        st.markdown(r"Vậy đồ thị hàm số có đúng $1$ điểm cực tiểu.")
        st.markdown("**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")



# ==========================================
# CÂU 8 (Tương ứng Câu 12 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 8. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Nguyễn Gia Thiều - Hà Nội 2026) </span>
        Cho hàm số $f(x)$ xác định trên $\mathbb{R}$ thỏa mãn đồng thời hai điều kiện: $f(x)$ là hàm số lẻ và 
        <span style="white-space: nowrap;">$f(x) = x^2$</span> với mọi <span style="white-space: nowrap;">$x \le 0$</span>. Giá trị của $f(2)$ bằng:
    </span>
    """, 
    unsafe_allow_html=True
)

options_q8 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $-4$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $-2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $0$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $4$."
]

user_choice_q8 = st.radio(
    "Chọn đáp án của bạn cho Câu 8:", 
    options_q8, 
    index=None, 
    key="q8_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q8_check"):
    # Đáp án đúng là A -> tương ứng với options_q8[0]
    if user_choice_q8 == options_q8[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q8 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q8_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Vì $f(x)$ là hàm số lẻ trên $\mathbb{R}$ nên ta có tính chất: $f(-x) = -f(x)$ với mọi $x \in \mathbb{R}$.")
        st.markdown(r"Thay $x = -2$, ta được:")
        st.latex(r"f(2) = -f(-2)")
        st.markdown(r"Theo giả thiết, $f(x) = x^2$ với mọi $x \le 0$. Vì $-2 \le 0$ nên:")
        st.latex(r"f(-2) = (-2)^2 = 4")
        st.markdown(r"Suy ra $f(2) = -4$.")
        st.markdown("**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")



# ==========================================
# CÂU 9 (Tương ứng Câu 13 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 9. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Nguyễn Gia Thiều - Hà Nội 2026) </span>
        Giá trị cực tiểu của hàm số <span style="white-space: nowrap;">$y = 4x^3 - 6x^2 + 11$</span> bằng:
    </span>
    """, 
    unsafe_allow_html=True
)

options_q9 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $0$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $9$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $11$."
]

user_choice_q9 = st.radio(
    "Chọn đáp án của bạn cho Câu 9:", 
    options_q9, 
    index=None, 
    key="q9_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q9_check"):
    # Đáp án đúng là C -> tương ứng với options_q9[2]
    if user_choice_q9 == options_q9[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q9 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q9_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Ta có đạo hàm:")
        st.latex(r"y' = 12x^2 - 12x = 12x(x - 1)")
        st.latex(r"y' = 0 \Leftrightarrow \left[\begin{array}{l} x = 0 \\ x = 1 \end{array}\right.")
        
        st.markdown(r"Tính đạo hàm cấp hai: $y'' = 24x - 12$")
        st.markdown(r"- Với $x = 0 \Rightarrow y''(0) = -12 < 0 \Rightarrow x = 0$ là điểm cực đại.")
        st.markdown(r"- Với $x = 1 \Rightarrow y''(1) = 12 > 0 \Rightarrow x = 1$ là điểm cực tiểu.")
        
        st.markdown(r"Vậy giá trị cực tiểu của hàm số là: $y_{CT} = y(1) = 4(1)^3 - 6(1)^2 + 11 = 9$.")
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")



# ==========================================
# CÂU 10 (Tương ứng Câu 14 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 10. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Nguyễn Gia Thiều - Hà Nội 2026) </span>
        Hàm số <span style="white-space: nowrap;">$y = -2x^3 + 9x^2 + 24x - 114$</span> đồng biến trên khoảng nào dưới đây?
    </span>
    """, 
    unsafe_allow_html=True
)

options_q10 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(-1; 4)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(-4; -1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(-\infty; -1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(4; +\infty)$."
]

user_choice_q10 = st.radio(
    "Chọn đáp án của bạn cho Câu 10:", 
    options_q10, 
    index=None, 
    key="q10_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q10_check"):
    # Đáp án đúng là A -> tương ứng với options_q10[0]
    if user_choice_q10 == options_q10[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q10 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q10_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Tập xác định: $D = \mathbb{R}$")
        st.markdown(r"Đạo hàm: $y' = -6x^2 + 18x + 24$")
        
        st.markdown(r"Hàm số đồng biến khi $y' > 0$:")
        st.latex(r"-6x^2 + 18x + 24 > 0 \Leftrightarrow x^2 - 3x - 4 < 0 \Leftrightarrow -1 < x < 4")
        
        st.markdown(r"Vậy hàm số đồng biến trên khoảng $(-1; 4)$.")
        st.markdown("**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# ==========================================
# CÂU 11 (Tương ứng Câu 16 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 11. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Nguyễn Gia Thiều - Hà Nội 2026) </span>
        Tiệm cận ngang của đồ thị hàm số 
        <span style="white-space: nowrap;">$y = \dfrac{2x - 4}{x + 2}$</span> là đường thẳng có phương trình
    </span>
    """, 
    unsafe_allow_html=True
)

options_q11 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = 2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $y = -2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $x = 2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $x = -2$."
]

user_choice_q11 = st.radio(
    "Chọn đáp án của bạn cho Câu 11:", 
    options_q11, 
    index=None, 
    key="q11_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q11_check"):
    # Đáp án đúng là A -> tương ứng với options_q11[0]
    if user_choice_q11 == options_q11[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q11 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q11_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Tập xác định: $D = \mathbb{R} \setminus \{-2\}$")
        st.markdown(r"Ta có:")
        st.latex(r"\lim_{x \to \pm\infty} y = \lim_{x \to \pm\infty} \dfrac{2x - 4}{x + 2} = \lim_{x \to \pm\infty} \dfrac{2 - \dfrac{4}{x}}{1 + \dfrac{2}{x}} = 2")
        
        st.markdown(r"Vậy tiệm cận ngang của đồ thị hàm số là đường thẳng **$y = 2$**.")
        st.markdown("**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# ==========================================
# CÂU 12 (Tương ứng Câu 17 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 12. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Bắc Ninh 2026) </span>
        Đường tiệm cận ngang của đồ thị hàm số 
        <span style="white-space: nowrap;">$y = \dfrac{3x - 1}{1 - x}$</span> có phương trình là
    </span>
    """, 
    unsafe_allow_html=True
)

options_q12 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $x = -3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $y = -3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $x = 3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $y = 3$."
]

user_choice_q12 = st.radio(
    "Chọn đáp án của bạn cho Câu 12:", 
    options_q12, 
    index=None, 
    key="q12_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q12_check"):
    # Đáp án đúng là B -> tương ứng với options_q12[1]
    if user_choice_q12 == options_q12[1]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q12 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q12_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Tập xác định: $D = \mathbb{R} \setminus \{1\}$")
        st.markdown(r"Ta có:")
        st.latex(r"\lim_{x \to \pm\infty} y = \lim_{x \to \pm\infty} \dfrac{3x - 1}{1 - x} = \lim_{x \to \pm\infty} \dfrac{3 - \dfrac{1}{x}}{\dfrac{1}{x} - 1} = -3")
        
        st.markdown(r"Vậy tiệm cận ngang của đồ thị hàm số là đường thẳng **$y = -3$**.")
        st.markdown("**Chọn đáp án B.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")




# ==========================================
# CÂU 13 (Tương ứng Câu 1 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 13. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Phú Thọ 2026) </span>
        Cho hàm số $y = f(x)$ có đạo hàm là $f'(x) = (x - 1)(x - 2)^2(x + 3), \forall x \in \mathbb{R}$. 
        Số điểm cực trị của hàm số đã cho là
    </span>
    """, 
    unsafe_allow_html=True
)

options_q13 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $0$."
]

user_choice_q13 = st.radio(
    "Chọn đáp án của bạn cho Câu 13:", 
    options_q13, 
    index=None, 
    key="q13_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q13_check"):
    # Đáp án đúng là A -> tương ứng với options_q13[0]
    if user_choice_q13 == options_q13[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q13 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q13_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Xét phương trình $f'(x) = 0$:")
        st.latex(r"f'(x) = (x - 1)(x - 2)^2(x + 3) = 0 \Leftrightarrow \left[\begin{array}{l} x = 1 \\ x = 2 \\ x = -3 \end{array}\right.")
        
        st.markdown(r"Ta thấy:")
        st.markdown(r"- $x = 1$ và $x = -3$ là các nghiệm bội lẻ (bậc 1), qua các điểm này $f'(x)$ đổi dấu.")
        st.markdown(r"- $x = 2$ là nghiệm bội chẵn (bậc 2), qua điểm này $f'(x)$ không đổi dấu.")
        
        st.markdown(r"Do hàm số chỉ đạt cực trị tại những điểm mà đạo hàm đổi dấu khi đi qua đó, nên đồ thị hàm số có đúng $2$ điểm cực trị.")
        st.markdown("**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# ==========================================
# CÂU 14 (Tương ứng Câu 2 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 14. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Phú Thọ 2026) </span>
        Giá trị lớn nhất của hàm số 
        <span style="white-space: nowrap;">$f(x) = \dfrac{2x + 3}{x - 1}$</span> trên đoạn 
        <span style="white-space: nowrap;">$[2; 5]$</span> bằng
    </span>
    """, 
    unsafe_allow_html=True
)

options_q14 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $\dfrac{13}{4}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $5$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $7$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $2$."
]

user_choice_q14 = st.radio(
    "Chọn đáp án của bạn cho Câu 14:", 
    options_q14, 
    index=None, 
    key="q14_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q14_check"):
    # Đáp án đúng là C -> tương ứng với options_q14[2]
    if user_choice_q14 == options_q14[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q14 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q14_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Xét hàm số $f(x) = \dfrac{2x + 3}{x - 1}$ trên đoạn $[2; 5]$.")
        st.markdown(r"Đạo hàm:")
        st.latex(r"f'(x) = \dfrac{2(-1) - 1(3)}{(x - 1)^2} = \dfrac{-5}{(x - 1)^2} < 0, \quad \forall x \in [2; 5]")
        
        st.markdown(r"Vì $f'(x) < 0$ trên đoạn $[2; 5]$, hàm số nghịch biến trên đoạn này.")
        st.markdown(r"Do đó, giá trị lớn nhất của hàm số đạt được tại đầu mút trái của đoạn:")
        st.latex(r"\max_{[2; 5]} f(x) = f(2) = \dfrac{2(2) + 3}{2 - 1} = 7")
        
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

import streamlit as st

# ==========================================
# CÂU 15 (Tương ứng Câu 42 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 15. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Cà Mau 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = x^3 - 3x^2 + 2$.</span> Gọi <span style="white-space: nowrap;">$M, m$</span> lần lượt là giá trị lớn nhất và giá trị nhỏ nhất của hàm số trên đoạn <span style="white-space: nowrap;">$[-2; 2]$</span>. Khi đó <span style="white-space: nowrap;">$M - m$</span> bằng
    </span>
    """, 
    unsafe_allow_html=True
)

options_q15 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $4$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $16$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $20$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $2$."
]

user_choice_q15 = st.radio(
    "Chọn đáp án của bạn cho Câu 15:", 
    options_q15, 
    index=None, 
    key="q15_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q15_check"):
    # Đáp án đúng là C -> tương ứng với options_q15[2] (20)
    if user_choice_q15 == options_q15[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q15 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q15_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Xét hàm số $y = x^3 - 3x^2 + 2$ trên đoạn $[-2; 2]$.")
        st.markdown(r"Đạo hàm: $y' = 3x^2 - 6x$")
        
        st.latex(r"y' = 0 \Leftrightarrow 3x^2 - 6x = 0 \Leftrightarrow \left[\begin{array}{l} x = 0 \in [-2; 2] \\ x = 2 \in [-2; 2] \end{array}\right.")
        
        st.markdown(r"Tính giá trị của hàm số tại các điểm tới hạn và các đầu mút:")
        st.markdown(r"- $y(-2) = (-2)^3 - 3(-2)^2 + 2 = -18$")
        st.markdown(r"- $y(0) = 0^3 - 3(0)^2 + 2 = 2$")
        st.markdown(r"- $y(2) = 2^3 - 3(2)^2 + 2 = -2$")
        
        st.markdown(r"Từ các giá trị trên, ta suy ra:")
        st.latex(r"M = \max_{[-2; 2]} y = 2")
        st.latex(r"m = \min_{[-2; 2]} y = -18")
        
        st.markdown(r"Khi đó: $M - m = 2 - (-18) = 20$.")
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# ==========================================
# CÂU 16 (Tương ứng Câu 43 trong ảnh)
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
        <span style="color: #008080; font-weight: bold;">Câu 16. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Đà Nẵng 2026) </span>
        Đồ thị hàm số <span style="white-space: nowrap;">$y = \dfrac{2x - 1}{x + 2}$</span> có tiệm cận ngang là:
    </span>
    """, 
    unsafe_allow_html=True
)

options_q16 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = -\dfrac{1}{2}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $y = \dfrac{1}{2}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $y = 2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $y = -2$."
]

user_choice_q16 = st.radio(
    "Chọn đáp án của bạn cho Câu 16:", 
    options_q16, 
    index=None, 
    key="q16_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q16_check"):
    # Đáp án đúng là C -> tương ứng với options_q16[2] (y = 2)
    if user_choice_q16 == options_q16[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_q16 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

if st.button("Xem lời giải chi tiết", key="q16_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Tập xác định: $D = \mathbb{R} \setminus \{-2\}$")
        st.markdown(r"Ta tính giới hạn của hàm số khi $x \to \pm\infty$:")
        st.latex(r"\lim_{x \to \pm\infty} y = \lim_{x \to \pm\infty} \dfrac{2x - 1}{x + 2} = \lim_{x \to \pm\infty} \dfrac{2 - \dfrac{1}{x}}{1 + \dfrac{2}{x}} = 2")
        
        st.markdown(r"Vậy tiệm cận ngang của đồ thị hàm số là đường thẳng **$y = 2$**.")
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU 17
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 17. </span> 
        Cho hàm số <span style="white-space: nowrap;">$f(x) = 2x^3 - 9x^2 - 24x + 1$</span>. Có bao nhiêu khẳng định đúng trong các khẳng định sau?<br>
        <span style="color: #cc0000; font-weight: bold;">(1)</span> Điểm cực đại của hàm số là <span style="white-space: nowrap;">$x = -1$</span>.<br>
        <span style="color: #cc0000; font-weight: bold;">(2)</span> Điểm cực tiểu của hàm số là <span style="white-space: nowrap;">$x = 4$</span>.<br>
        <span style="color: #cc0000; font-weight: bold;">(3)</span> Giá trị cực đại của hàm số là <span style="white-space: nowrap;">$y = 14$</span>.<br>
        <span style="color: #cc0000; font-weight: bold;">(4)</span> Giá trị cực tiểu của hàm số là <span style="white-space: nowrap;">$y = -111$</span>.
    </span>
    """, 
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án (Sử dụng LaTeX để tạo vòng tròn màu xanh ngọc)
options_17 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $4$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $2$."
]

# 3. Sử dụng st.radio với tham số horizontal=True để dàn hàng ngang
user_choice_17 = st.radio(
    "Chọn đáp án của bạn:", 
    options_17, 
    index=None, 
    key="q17_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q17_check"):
    if user_choice_17 == options_17[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_17 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

# 5. Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q17_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Tập xác định: $D = \mathbb{R}$.") 
        st.markdown(r"Đạo hàm: <span style='white-space: nowrap;'>$f'(x) = 6x^2 - 18x - 24$</span>.", unsafe_allow_html=True)
        st.markdown(r"Cho <span style='white-space: nowrap;'>$f'(x) = 0 \Leftrightarrow 6x^2 - 18x - 24 = 0 \Leftrightarrow \left[ \begin{array}{l} x = -1 \\ x = 4 \end{array} \right.$</span>.", unsafe_allow_html=True)
        st.markdown(r"Bảng xét dấu $f'(x)$: $f'(x) > 0$ khi $x \in (-\infty; -1) \cup (4; +\infty)$; $f'(x) < 0$ khi $x \in (-1; 4)$.", unsafe_allow_html=True)
        st.markdown(r"$\Rightarrow$ Hàm số đạt cực đại tại <span style='white-space: nowrap;'>$x = -1$</span> và đạt cực tiểu tại <span style='white-space: nowrap;'>$x = 4$</span>.", unsafe_allow_html=True)
        st.markdown(r"Giá trị cực đại: <span style='white-space: nowrap;'>$y_{CĐ} = f(-1) = 2(-1)^3 - 9(-1)^2 - 24(-1) + 1 = 14$</span>.", unsafe_allow_html=True)
        st.markdown(r"Giá trị cực tiểu: <span style='white-space: nowrap;'>$y_{CT} = f(4) = 2(4)^3 - 9(4)^2 - 24(4) + 1 = -111$</span>.", unsafe_allow_html=True)
        st.markdown(r"Vậy cả 4 khẳng định trên đều đúng.", unsafe_allow_html=True)
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")










# CÂU 18
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 18. </span> 
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> có đạo hàm <span style="white-space: nowrap;">$f'(x) = (x-2)^2(1-x)$</span> với mọi <span style="white-space: nowrap;">$x \in \mathbb{R}$</span>. Hàm số đã cho đồng biến trên khoảng nào dưới đây?
    </span>
    """, 
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án (Sử dụng LaTeX để tạo vòng tròn màu xanh ngọc)
options_18 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(1;2)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(1;+\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(2;+\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(-\infty;1)$."
]

# 3. Sử dụng st.radio với tham số horizontal=True để dàn hàng ngang
user_choice_18 = st.radio(
    "Chọn đáp án của bạn:", 
    options_18, 
    index=None, 
    key="q18_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q18_check"):
    if user_choice_18 == options_18[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_18 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

# 5. Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q18_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Ta có <span style='white-space: nowrap;'>$f'(x) = (x - 2)^2(1 - x)$</span>.", unsafe_allow_html=True) 
        st.markdown(r"Cho <span style='white-space: nowrap;'>$f'(x) = 0 \Leftrightarrow \left[ \begin{array}{l} x = 2 \\ x = 1 \end{array} \right.$</span>.", unsafe_allow_html=True)
        st.markdown(r"Do <span style='white-space: nowrap;'>$(x-2)^2 \ge 0$</span> với mọi <span style='white-space: nowrap;'>$x \in \mathbb{R}$</span> nên dấu của <span style='white-space: nowrap;'>$f'(x)$</span> phụ thuộc vào nhị thức <span style='white-space: nowrap;'>$1-x$</span>.", unsafe_allow_html=True)
        st.markdown(r"Hàm số đồng biến khi <span style='white-space: nowrap;'>$f'(x) > 0 \Leftrightarrow 1 - x > 0 \Leftrightarrow x < 1$</span>.", unsafe_allow_html=True)
        st.markdown(r"Vậy hàm số đồng biến trên khoảng <span style='white-space: nowrap;'>$(-\infty; 1)$</span>.", unsafe_allow_html=True)
        st.markdown("**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# CÂU 19
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 19. </span> 
        Hỏi hàm số <span style="white-space: nowrap;">$y = 2x^4 + 1$</span> đồng biến trên khoảng nào?
    </span>
    """, 
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án
options_19 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(-\infty;0)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(-\infty;-\frac{1}{2})$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(0;+\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(-\frac{1}{2};+\infty)$."
]

# 3. Sử dụng st.radio
user_choice_19 = st.radio(
    "Chọn đáp án của bạn:", 
    options_19, 
    index=None, 
    key="q19_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q19_check"):
    if user_choice_19 == options_19[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_19 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

# 5. Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q19_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Tập xác định: $D = \mathbb{R}$.") 
        st.markdown(r"Đạo hàm: <span style='white-space: nowrap;'>$y' = 8x^3$</span>.", unsafe_allow_html=True)
        st.markdown(r"Cho <span style='white-space: nowrap;'>$y' = 0 \Leftrightarrow 8x^3 = 0 \Leftrightarrow x = 0$</span>.", unsafe_allow_html=True)
        st.markdown(r"Hàm số đồng biến khi <span style='white-space: nowrap;'>$y' > 0 \Leftrightarrow 8x^3 > 0 \Leftrightarrow x > 0$</span>.", unsafe_allow_html=True)
        st.markdown(r"Vậy hàm số đồng biến trên khoảng <span style='white-space: nowrap;'>$(0; +\infty)$</span>.", unsafe_allow_html=True)
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# CÂU 20
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 20. </span> 
        Hàm số <span style="white-space: nowrap;">$y = \dfrac{2}{x^2+1}$</span> nghịch biến trên khoảng nào dưới đây?
    </span>
    """, 
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án
options_20 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(-\infty;+\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(0;+\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(-\infty;0)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(-1;1)$."
]

# 3. Sử dụng st.radio
user_choice_20 = st.radio(
    "Chọn đáp án của bạn:", 
    options_20, 
    index=None, 
    key="q20_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q20_check"):
    if user_choice_20 == options_20[1]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_20 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

# 5. Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q20_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Tập xác định: $D = \mathbb{R}$.") 
        st.latex(r"y' = \dfrac{-2 \cdot (x^2+1)'}{(x^2+1)^2} = \dfrac{-4x}{(x^2+1)^2}")
        st.markdown(r"Cho <span style='white-space: nowrap;'>$y' = 0 \Leftrightarrow -4x = 0 \Leftrightarrow x = 0$</span>.", unsafe_allow_html=True)
        st.markdown(r"Hàm số nghịch biến khi <span style='white-space: nowrap;'>$y' < 0 \Leftrightarrow \dfrac{-4x}{(x^2+1)^2} < 0 \Leftrightarrow x > 0$</span>.", unsafe_allow_html=True)
        st.markdown(r"Vậy hàm số nghịch biến trên khoảng <span style='white-space: nowrap;'>$(0; +\infty)$</span>.", unsafe_allow_html=True)
        st.markdown("**Chọn đáp án B.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU 21
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 21. </span> 
        Cho hàm số <span style="white-space: nowrap;">$y = \sqrt{2x^2+1}$</span>. Mệnh đề nào dưới đây <b>đúng</b>?
    </span>
    """, 
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án
options_21 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ Hàm số đồng biến trên khoảng $(0;+\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ Hàm số đồng biến trên khoảng $(-\infty;0)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ Hàm số nghịch biến trên khoảng $(0;+\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ Hàm số nghịch biến trên khoảng $(-1;1)$."
]

# 3. Sử dụng st.radio
user_choice_21 = st.radio(
    "Chọn đáp án của bạn:", 
    options_21, 
    index=None, 
    key="q21_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q21_check"):
    if user_choice_21 == options_21[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_21 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

# 5. Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q21_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Tập xác định: $D = \mathbb{R}$.") 
        st.latex(r"y' = \dfrac{(2x^2+1)'}{2\sqrt{2x^2+1}} = \dfrac{4x}{2\sqrt{2x^2+1}} = \dfrac{2x}{\sqrt{2x^2+1}}")
        st.markdown(r"Cho <span style='white-space: nowrap;'>$y' = 0 \Leftrightarrow 2x = 0 \Leftrightarrow x = 0$</span>.", unsafe_allow_html=True)
        st.markdown(r"Bảng xét dấu: với $x > 0$ thì $y' > 0$; với $x < 0$ thì $y' < 0$.", unsafe_allow_html=True)
        st.markdown(r"Vậy hàm số đồng biến trên khoảng <span style='white-space: nowrap;'>$(0; +\infty)$</span> và nghịch biến trên khoảng <span style='white-space: nowrap;'>$(-\infty; 0)$</span>.", unsafe_allow_html=True)
        st.markdown("**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


# CÂU 22
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 22. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Đồng Hỷ - Thái Nguyên 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> có bảng biến thiên như sau:
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh bảng biến thiên
st.image("images/image_85d958.PNG", use_container_width=True)

st.markdown(
    r"""
    <span style="
        display: block; 
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        margin-bottom: 10px;
    ">
        Điểm cực đại của hàm số <span style="white-space: nowrap;">$y = f(x)$</span> là:
    </span>
    """,
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án (Sử dụng horizontal=True vì đáp án ngắn)
options_22 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = 2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $x = 2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $x = 3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $y = -1$."
]

# 3. Nút chọn đáp án
user_choice_22 = st.radio(
    "Chọn đáp án của bạn (Câu 22):", 
    options_22, 
    index=None, 
    key="q22_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q22_check"):
    if user_choice_22 == options_22[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_22 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q22_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Dựa vào bảng biến thiên, ta thấy $f'(x)$ đổi dấu từ dương $(+)$ sang âm $(-)$ khi đi qua điểm $x = 3$.")
        
        st.markdown(r"Do đó, hàm số đạt cực đại tại $x = 3$.")
        
        st.markdown(r"> **Lưu ý:** Khái niệm **Điểm cực đại của hàm số** là chỉ giá trị của $x$. Nếu đề hỏi **Giá trị cực đại của hàm số** thì đáp án mới là $y = 2$.")
        
        st.markdown(r"**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

import streamlit as st

# CÂU 23
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 23. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Đồng Hỷ - Thái Nguyên 2026) </span>
        Hàm số nào sau đây có đồ thị là đường cong như hình vẽ?
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh đồ thị
st.image("images/image_85c6ee.PNG", use_container_width=True)

# 2. Danh sách 4 đáp án
options_23 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = x - \dfrac{1}{x - 1}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $y = -x + \dfrac{1}{x - 1}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $y = -x - \dfrac{1}{x - 1}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $y = x + \dfrac{1}{x - 1}$."
]

# 3. Nút chọn đáp án
user_choice_23 = st.radio(
    "Chọn đáp án của bạn (Câu 23):", 
    options_23, 
    index=None, 
    key="q23_radio", 
    horizontal=False 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q23_check"):
    if user_choice_23 == options_23[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_23 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q23_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Quan sát đồ thị, ta thấy:")
        st.markdown(r"- Đồ thị có tiệm cận đứng là $x = 1$.")
        st.markdown(r"- Điểm cực đại của đồ thị là điểm có tọa độ $(0; -1)$.")
        st.markdown(r"- Điểm cực tiểu của đồ thị là điểm có tọa độ $(2; 3)$.")
        
        st.markdown(r"Thay tọa độ điểm cực tiểu $(2; 3)$ vào các đáp án, ta được:")
        st.markdown(r"- **A:** $y(2) = 2 - \dfrac{1}{2 - 1} = 1 \neq 3$ (Loại).")
        st.markdown(r"- **B:** $y(2) = -2 + \dfrac{1}{2 - 1} = -1 \neq 3$ (Loại).")
        st.markdown(r"- **C:** $y(2) = -2 - \dfrac{1}{2 - 1} = -3 \neq 3$ (Loại).")
        st.markdown(r"- **D:** $y(2) = 2 + \dfrac{1}{2 - 1} = 3$ (Thỏa mãn).")
        
        st.markdown(r"Thử lại với đáp án D: Hàm số $y = x + \dfrac{1}{x - 1}$ có tập xác định $D = \mathbb{R} \setminus \{1\}$.")
        st.markdown(r"Đạo hàm: $y' = 1 - \dfrac{1}{(x - 1)^2}$. Cho $y' = 0 \Leftrightarrow (x - 1)^2 = 1 \Leftrightarrow \left[ \begin{array}{ll} x = 2 \Rightarrow y = 3 \\ x = 0 \Rightarrow y = -1 \end{array} \right.$. Kết quả này hoàn toàn phù hợp với tọa độ các điểm cực trị trên đồ thị.")
        
        st.markdown(r"**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


import streamlit as st

# CÂU 24
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 24. </span> 
        <span style="color: #009900; font-weight: bold;">(Chuyên Trần Phú - Hải Phòng 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> liên tục trên $\mathbb{R}$ và có đồ thị là đường cong trong hình dưới đây. Hàm số đã cho đồng biến trên khoảng nào dưới đây?
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh đồ thị
st.image("images/image_85701f.PNG", use_container_width=True)

# 2. Danh sách 4 đáp án (Sử dụng horizontal=True vì đáp án ngắn)
options_24 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(0;1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(-1;1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(-\infty;1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(0;+\infty)$."
]

# 3. Nút chọn đáp án
user_choice_24 = st.radio(
    "Chọn đáp án của bạn (Câu 24):", 
    options_24, 
    index=None, 
    key="q24_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q24_check"):
    if user_choice_24 == options_24[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_24 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q24_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Dựa vào đồ thị hàm số, ta thấy đồ thị có hướng đi lên (từ trái sang phải) trên các khoảng $(-\infty; -1)$ và $(0; 1)$.")
        
        st.markdown(r"Do đó, hàm số đồng biến trên các khoảng $(-\infty; -1)$ và $(0; 1)$.")
        
        st.markdown(r"Đối chiếu với các đáp án, khoảng $(0; 1)$ nằm trong đáp án A.")
        
        st.markdown(r"**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


import streamlit as st

# CÂU 25
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 25. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Nguyễn Gia Thiều - Hà Nội 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$f(x)$</span> liên tục trên đoạn $[-1; 5]$ và có đồ thị như hình vẽ bên (các điểm cực trị của đồ thị thể hiện rõ trên hình). Gọi $M$ và $m$ lần lượt là giá trị lớn nhất và nhỏ nhất của hàm số đã cho trên $[-1; 5]$.
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh đồ thị
st.image("images/image_8568dd2.PNG", use_container_width=True)

st.markdown(
    r"""
    <span style="
        display: block; 
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        margin-bottom: 10px;
    ">
        Giá trị của $M - m$ bằng:
    </span>
    """,
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án (Sử dụng horizontal=True vì đáp án ngắn)
options_25 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $4$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $5$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $6$."
]

# 3. Nút chọn đáp án
user_choice_25 = st.radio(
    "Chọn đáp án của bạn (Câu 25):", 
    options_25, 
    index=None, 
    key="q25_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q25_check"):
    if user_choice_25 == options_25[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_25 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q25_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Quan sát đồ thị hàm số trên đoạn $[-1; 5]$, ta thấy:")
        
        st.markdown(r"- Điểm cao nhất của đồ thị có tọa độ $(4; 3) \Rightarrow M = \max_{[-1; 5]} f(x) = 3$.")
        st.markdown(r"- Điểm thấp nhất của đồ thị có tọa độ $(2; -2)$ và $(-1; -2) \Rightarrow m = \min_{[-1; 5]} f(x) = -2$.")
        
        st.markdown(r"Do đó, $M - m = 3 - (-2) = 5$.")
        
        st.markdown(r"**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")




# CÂU 26
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 26. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Bắc Ninh 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> liên tục và có đồ thị trên đoạn $[-4; 3]$ như hình vẽ.
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh đồ thị
# Lưu ý: Sửa lại đường dẫn ảnh cho khớp với thực tế trên kho lưu trữ của bạn nếu cần
st.image("images/image_84ffdd.PNG", use_container_width=True)

st.markdown(
    r"""
    <span style="
        display: block; 
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        margin-bottom: 10px;
    ">
        Giá trị nhỏ nhất của hàm số <span style="white-space: nowrap;">$y = f(x)$</span> trên đoạn $[0; 3]$ là:
    </span>
    """,
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án (Sử dụng horizontal=True vì đáp án ngắn)
options_26 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $-4$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $-3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $-2$."
]

# 3. Nút chọn đáp án
user_choice_26 = st.radio(
    "Chọn đáp án của bạn (Câu 26):", 
    options_26, 
    index=None, 
    key="q26_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q26_check"):
    if user_choice_26 == options_26[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_26 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q26_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Quan sát đồ thị hàm số trên đoạn đang xét là $[0; 3]$, ta thấy:")
        
        st.markdown(r"- Tại $x = 0$, $y = -1$.")
        st.markdown(r"- Tại $x = 1$, $y = -2$ (đây là điểm thấp nhất trên đoạn này).")
        st.markdown(r"- Tại $x = 3$, $y = 2$.")
        
        st.markdown(r"Do đó, $\min_{[0; 3]} f(x) = -2$ tại $x = 1$.")
        
        st.markdown(r"> **Lưu ý:** Cần đọc kỹ đoạn đề bài yêu cầu là $[0; 3]$. Nếu nhìn nhầm sang đoạn $[-4; 3]$ thì sẽ dễ chọn sai đáp án B ($-3$).")
        
        st.markdown(r"**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


import streamlit as st

# CÂU 27
# ==========================================
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 27. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Bắc Ninh 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> liên tục trên $\mathbb{R}$ và có bảng xét dấu đạo hàm như hình vẽ sau:
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh bảng xét dấu đạo hàm
st.image("images/image_84f896.PNG", use_container_width=True)

st.markdown(
    r"""
    <span style="
        display: block; 
        font-family: 'Times New Roman', Times, serif; 
        font-size: 18px;
        margin-bottom: 10px;
    ">
        Số điểm cực tiểu của đồ thị hàm số <span style="white-space: nowrap;">$y = f(x)$</span> là:
    </span>
    """,
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án (Sử dụng horizontal=True vì đáp án ngắn)
options_27 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $0$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $3$."
]

# 3. Nút chọn đáp án
user_choice_27 = st.radio(
    "Chọn đáp án của bạn (Câu 27):", 
    options_27, 
    index=None, 
    key="q27_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q27_check"):
    if user_choice_27 == options_27[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_27 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q27_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Hàm số $y = f(x)$ được cho là **liên tục trên $\mathbb{R}$**.")
        
        st.markdown(r"Dựa vào bảng xét dấu đạo hàm, ta xét sự đổi dấu của $f'(x)$:")
        st.markdown(r"- Khi qua điểm $x = -1$, $f'(x)$ đổi dấu từ dương $(+)$ sang âm $(-)$ $\Rightarrow$ $x = -1$ là điểm cực đại.")
        st.markdown(r"- Khi qua điểm $x = 0$, $f'(x)$ đổi dấu từ âm $(-)$ sang dương $(+)$ $\Rightarrow$ $x = 0$ là điểm cực tiểu.")
        st.markdown(r"- Khi qua điểm $x = 1$, $f'(x)$ đổi dấu từ dương $(+)$ sang âm $(-)$ $\Rightarrow$ $x = 1$ là điểm cực đại.")
        
        st.markdown(r"> **Lưu ý:** Mặc dù tại $x = -1$ và $x = 1$, đạo hàm $f'(x)$ không xác định (ký hiệu `||`), nhưng do hàm số $f(x)$ liên tục trên $\mathbb{R}$ nên nó vẫn liên tục tại các điểm này. Vì vậy, sự đổi dấu của $f'(x)$ qua các điểm đó vẫn tạo ra điểm cực trị.")
        
        st.markdown(r"Vậy đồ thị hàm số có đúng $1$ điểm cực tiểu.")
        
        st.markdown(r"**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

import streamlit as st

# CÂU 28
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 28. </span> 
        <span style="color: #009900; font-weight: bold;">(Sở Phú Thọ 2026) </span>
        Cho hàm số bậc ba <span style="white-space: nowrap;">$y = ax^3 + bx^2 + cx + d \; (a \neq 0)$</span> có đồ thị như hình vẽ.<br>
        Hàm số nghịch biến trên khoảng nào trong các khoảng dưới đây?
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh đồ thị
st.image("images/image_84f419.PNG", use_container_width=True)

# 2. Danh sách 4 đáp án (Sử dụng horizontal=True vì đáp án ngắn)
options_28 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(-\infty; -1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(-1; 1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(1; +\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(-4; 0)$."
]

# 3. Nút chọn đáp án
user_choice_28 = st.radio(
    "Chọn đáp án của bạn (Câu 28):", 
    options_28, 
    index=None, 
    key="q28_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q28_check"):
    if user_choice_28 == options_28[1]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_28 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q28_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Quan sát đồ thị, ta thấy:")
        st.markdown(r"- Hướng của đồ thị đi xuống (từ trái sang phải) tương ứng với phần hoành độ $x$ nằm trong khoảng $(-1; 1)$.")
        
        st.markdown(r"Do đó, hàm số đã cho nghịch biến trên khoảng $(-1; 1)$.")
        
        st.markdown(r"**Chọn đáp án B.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

import streamlit as st

# CÂU 29
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 29. </span> 
        <span style="color: #009900; font-weight: bold;">(Mã 101 – 2020 Lần 1) </span>
        Cho hàm số <span style="white-space: nowrap;">$f(x)$</span> có bảng biến thiên như sau:<br>
        Hàm số đã cho đồng biến trên khoảng nào dưới đây?
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh đồ thị
st.image("images/image_775c3c.PNG", use_container_width=True)

# 2. Danh sách 4 đáp án (Sử dụng horizontal=True vì đáp án ngắn)
options_29 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(-\infty; -1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(0; 1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(-1; 1)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(-1; 0)$."
]

# 3. Nút chọn đáp án
user_choice_29 = st.radio(
    "Chọn đáp án của bạn (Câu 29):", 
    options_29, 
    index=None, 
    key="q29_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q29_check"):
    if user_choice_29 == options_29[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_29 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q29_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Quan sát bảng biến thiên, ta thấy đạo hàm $f'(x)$ mang dấu $(+)$ trên các khoảng $(-1; 0)$ và $(1; +\infty)$.")
        
        st.markdown(r"Do đó, hàm số đã cho đồng biến trên các khoảng $(-1; 0)$ và $(1; +\infty)$.")
        
        st.markdown(r"Đối chiếu với các đáp án, ta thấy khoảng $(-1; 0)$ nằm ở đáp án D.")
        
        st.markdown(r"**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

import streamlit as st

# CÂU 30
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 30. </span> 
        <span style="color: #009900; font-weight: bold;">(Mã 104 - 2017) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> có bảng xét dấu đạo hàm như sau:<br>
        Mệnh đề nào dưới đây <b>đúng</b>?
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh bảng xét dấu
st.image("images/image_774613.PNG", use_container_width=True)

# 2. Danh sách 4 đáp án (Để horizontal=False vì đáp án là dạng câu dài)
options_30 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ Hàm số nghịch biến trên khoảng $(-\infty; -2)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ Hàm số đồng biến trên khoảng $(-2; 0)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ Hàm số đồng biến trên khoảng $(-\infty; 0)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ Hàm số nghịch biến trên khoảng $(0; 2)$."
]

# 3. Nút chọn đáp án
user_choice_30 = st.radio(
    "Chọn đáp án của bạn (Câu 30):", 
    options_30, 
    index=None, 
    key="q30_radio", 
    horizontal=False 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q30_check"):
    if user_choice_30 == options_30[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_30 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q30_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Dựa vào bảng xét dấu đạo hàm, ta thấy:")
        st.markdown(r"- $y' > 0$ trên các khoảng $(-\infty; -2)$ và $(2; +\infty)$ nên hàm số đồng biến trên các khoảng này.")
        st.markdown(r"- $y' < 0$ trên các khoảng $(-2; 0)$ và $(0; 2)$ nên hàm số nghịch biến trên các khoảng này.")
        
        st.markdown(r"Đối chiếu với các phương án:")
        st.markdown(r"- **A sai** vì hàm số đồng biến trên $(-\infty; -2)$.")
        st.markdown(r"- **B sai** vì hàm số nghịch biến trên $(-2; 0)$.")
        st.markdown(r"- **C sai** vì hàm số không đồng biến trên toàn bộ $(-\infty; 0)$.")
        st.markdown(r"- **D đúng** vì hàm số nghịch biến trên $(0; 2)$.")
        
        st.markdown(r"**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


import streamlit as st

# CÂU 31
# 1. Hiển thị đề bài trong khung
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
        <span style="color: #008080; font-weight: bold;">Câu 31. </span> 
        <span style="color: #009900; font-weight: bold;">(Mã 101 - 2018) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> có bảng biến thiên như sau:<br>
        Hàm số đã cho nghịch biến trên khoảng nào dưới đây?
    </span>
    """, 
    unsafe_allow_html=True
)

# Chèn hình ảnh bảng biến thiên
st.image("images/image_76dd9111.PNG", use_container_width=True)

# 2. Danh sách 4 đáp án (Sử dụng horizontal=True vì đáp án ngắn)
options_31 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(-1; 0)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(-\infty; 0)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(1; +\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(0; 1)$."
]

# 3. Nút chọn đáp án
user_choice_31 = st.radio(
    "Chọn đáp án của bạn (Câu 31):", 
    options_31, 
    index=None, 
    key="q31_radio", 
    horizontal=True 
)

# 4. Nút kiểm tra
if st.button("Kiểm tra đáp án", key="q31_check"):
    if user_choice_31 == options_31[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_31 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

# 5. Nút lời giải
if st.button("Xem lời giải chi tiết", key="q31_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        
        st.markdown(r"Dựa vào bảng biến thiên, ta thấy đạo hàm $f'(x)$ mang dấu âm $(-)$ trên các khoảng $(-\infty; -1)$ và $(0; 1)$.")
        
        st.markdown(r"Do đó, hàm số nghịch biến trên các khoảng $(-\infty; -1)$ và $(0; 1)$.")
        
        st.markdown(r"Đối chiếu với các đáp án, khoảng $(0; 1)$ thuộc phương án D.")
        
        st.markdown(r"**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")




# CÂU 32
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
        <span style="color: #008080; font-weight: bold;">Câu 32. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Nguyễn Thị Minh Khai - Hà Nội 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$f(x)$</span> có bảng xét dấu của đạo hàm như sau:<br>
        Hàm số đã cho nghịch biến trên khoảng nào dưới đây?
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_767364.PNG", use_container_width=True)

options_32 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $(-3; 0)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $(0; +\infty)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $(0; 2)$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $(-\infty; -3)$."
]

user_choice_32 = st.radio(
    "Chọn đáp án của bạn (Câu 32):", 
    options_32, 
    index=None, 
    key="q32_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q32_check"):
    if user_choice_32 == options_32[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_32 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

if st.button("Xem lời giải chi tiết", key="q32_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Dựa vào bảng xét dấu đạo hàm, ta thấy $f'(x) < 0$ trên các khoảng $(-3; 0)$ và $(2; +\infty)$.")
        st.markdown(r"Do đó, hàm số nghịch biến trên khoảng $(-3; 0)$.")
        st.markdown(r"**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# CÂU 33
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
        <span style="color: #008080; font-weight: bold;">Câu 33. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Nguyễn Thị Minh Khai - Hà Nội 2026) </span>
        Bảng biến thiên sau đây là của hàm số nào?
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_7673641.PNG", use_container_width=True)

options_33 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = \dfrac{2x+3}{x+1}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $y = \dfrac{2x-1}{x-1}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $y = \dfrac{2x-1}{x+1}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $y = \dfrac{x+1}{2x-1}$."
]

user_choice_33 = st.radio(
    "Chọn đáp án của bạn (Câu 33):", 
    options_33, 
    index=None, 
    key="q33_radio", 
    horizontal=False 
)

if st.button("Kiểm tra đáp án", key="q33_check"):
    if user_choice_33 == options_33[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_33 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

if st.button("Xem lời giải chi tiết", key="q33_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Quan sát bảng biến thiên, ta thấy:")
        st.markdown(r"- Tiệm cận đứng của đồ thị là $x = -1$, loại các đáp án có mẫu chứa $x - 1$ (loại B, D).")
        st.markdown(r"- Tiệm cận ngang là $y = 2$.")
        st.markdown(r"- Chiều biến thiên: hàm số đồng biến trên các khoảng $(-\infty; -1)$ và $(-1; +\infty)$, do đó $y' > 0$.")
        st.markdown(r"Xét hàm số ở đáp án C: $y = \dfrac{2x-1}{x+1}$, ta có đạo hàm $y' = \dfrac{2(1) - (-1)\cdot 1}{(x+1)^2} = \dfrac{3}{(x+1)^2} > 0$ với mọi $x \neq -1$.")
        st.markdown(r"**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")




# CÂU 34
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
        <span style="color: #008080; font-weight: bold;">Câu 34. </span> 
        <span style="color: #009900; font-weight: bold;">(Cụm trường Hà Tĩnh 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$f(x) = ax^3 + bx^2 + cx + d$</span> có đồ thị như hình sau đây.<br>
        Số nghiệm dương của phương trình <span style="white-space: nowrap;">$2f(x) - 3 = 0$</span> là:
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_7664de.PNG", use_container_width=True)

options_34 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $0$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $2$."
]

user_choice_34 = st.radio(
    "Chọn đáp án của bạn (Câu 34):", 
    options_34, 
    index=None, 
    key="q34_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q34_check"):
    if user_choice_34 == options_34[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_34 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

if st.button("Xem lời giải chi tiết", key="q34_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Ta có phương trình: $2f(x) - 3 = 0 \iff f(x) = \dfrac{3}{2} = 1.5$.")
        st.markdown(r"Số nghiệm của phương trình chính là số giao điểm của đồ thị hàm số $y = f(x)$ và đường thẳng nằm ngang $y = 1.5$.")
        st.markdown(r"Quan sát đồ thị, đường thẳng $y = 1.5$ cắt đồ thị hàm số tại 3 điểm phân biệt, trong đó có 2 giao điểm có hoành độ dương và 1 giao điểm có hoành độ âm.")
        st.markdown(r"Do đó, phương trình đã cho có 2 nghiệm dương.")
        st.markdown(r"**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# CÂU 35
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
        <span style="color: #008080; font-weight: bold;">Câu 35. </span> 
        <span style="color: #009900; font-weight: bold;">(Cụm trường Hà Tĩnh 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> có bảng biến thiên như sau:<br>
        Giá trị cực đại của hàm số <span style="white-space: nowrap;">$y = f(x)$</span> là:
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_7664de1.PNG", use_container_width=True)

options_35 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = -3$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $y = -6$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $x = -7$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $x = -4$."
]

user_choice_35 = st.radio(
    "Chọn đáp án của bạn (Câu 35):", 
    options_35, 
    index=None, 
    key="q35_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q35_check"):
    if user_choice_35 == options_35[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_35 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

if st.button("Xem lời giải chi tiết", key="q35_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Dựa vào bảng biến thiên, ta thấy hàm số đạt cực đại tại điểm $x = -4$ và giá trị cực đại của hàm số là $y_{CĐ} = -3$.")
        st.markdown(r"**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")


import streamlit as st

# CÂU 36
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
        <span style="color: #008080; font-weight: bold;">Câu 36. </span> 
        <span style="color: #009900; font-weight: bold;">(Liên trường Nghệ An 2026) </span>
        Bạn Hải có một tấm bìa hình vuông cạnh <span style="white-space: nowrap;">$40\text{ cm}$</span>. Bạn muốn cắt bỏ ở bốn góc bốn hình vuông nhỏ bằng nhau để gấp và dán lại thành một hộp hình hộp chữ nhật không có nắp (tham khảo hình vẽ).<br>
        Để hộp có thể tích lớn nhất thì độ dài cạnh của hình vuông nhỏ bị cắt là:
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_7655f91.png", use_container_width=True)

options_36 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $6\text{ cm}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $5\text{ cm}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $\dfrac{20}{3}\text{ cm}$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $\dfrac{10}{3}\text{ cm}$."
]

user_choice_36 = st.radio(
    "Chọn đáp án của bạn (Câu 36):", 
    options_36, 
    index=None, 
    key="q36_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q36_check"):
    if user_choice_36 == options_36[2]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_36 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

if st.button("Xem lời giải chi tiết", key="q36_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Gọi $x$ (cm) là độ dài cạnh của hình vuông nhỏ bị cắt ở bốn góc với điều kiện $0 < x < 20$.")
        st.markdown(r"Khi đó, kích thước của hình hộp chữ nhật không có nắp được tạo thành là:")
        st.markdown(r"- Chiều cao: $x$")
        st.markdown(r"- Chiều dài đáy: $40 - 2x$")
        st.markdown(r"- Chiều rộng đáy: $40 - 2x$")
        st.markdown(r"Thể tích của hình hộp chữ nhật là: $V(x) = x(40 - 2x)^2 = 4x(20 - x)^2$.")
        st.markdown(r"Ta có đạo hàm: $V'(x) = 4(20 - x)^2 + 4x \cdot 2(20 - x)(-1) = 4(20 - x)(20 - x - 2x) = 4(20 - x)(20 - 3x)$.")
        st.markdown(r"Cho $V'(x) = 0 \implies \left[\begin{array}{l} x = 20 \text{ (loại)}\\ x = \dfrac{20}{3} \text{ (nhận)} \end{array}\right.$")
        st.markdown(r"Dựa vào bảng biến thiên hoặc chiều biến thiên của hàm số, thể tích $V(x)$ đạt giá trị lớn nhất khi $x = \dfrac{20}{3}$.")
        st.markdown(r"**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")




# CÂU 37
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
        <span style="color: #008080; font-weight: bold;">Câu 37. </span> 
        <span style="color: #009900; font-weight: bold;">(ĐGNL DHSPHN 2026) </span>
        Cho hàm số <span style="white-space: nowrap;">$y = f(x)$</span> có đạo hàm trên $\mathbb{R}$. Biết hàm số <span style="white-space: nowrap;">$y = f'(x)$</span> có đồ thị như hình vẽ. Phát biểu nào sau đây là đúng?
    </span>
    """, 
    unsafe_allow_html=True
)

st.image("images/image_75f0d5.png", use_container_width=True)

options_37 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ Hàm số $y = f(x)$ đạt cực đại tại $x_1 = -2$ và đạt cực tiểu tại $x_2 = 1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ Hàm số $y = f(x)$ đạt cực tiểu tại hai điểm $x_1 = -2$ và $x_2 = 1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ Hàm số $y = f(x)$ đạt cực đại tại hai điểm $x_1 = -2$ và $x_2 = 1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ Hàm số $y = f(x)$ đạt cực tiểu tại $x_1 = -2$ và đạt cực đại tại $x_2 = 1$."
]

user_choice_37 = st.radio(
    "Chọn đáp án của bạn (Câu 37):", 
    options_37, 
    index=None, 
    key="q37_radio", 
    horizontal=False 
)

if st.button("Kiểm tra đáp án", key="q37_check"):
    if user_choice_37 == options_37[3]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_37 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

if st.button("Xem lời giải chi tiết", key="q37_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Dựa vào đồ thị của hàm số $y = f'(x)$, ta thấy đồ thị cắt trục hoành tại hai điểm $x = -2$ và $x = 1$.")
        st.markdown(r"- Với $x < -2$, đồ thị nằm phía dưới trục hoành nên $f'(x) < 0$.")
        st.markdown(r"- Với $-2 < x < 1$, đồ thị nằm phía trên trục hoành nên $f'(x) > 0$.")
        st.markdown(r"- Với $x > 1$, đồ thị nằm phía dưới trục hoành nên $f'(x) < 0$.")
        st.markdown(r"Do đó, qua điểm $x = -2$, đạo hàm $f'(x)$ đổi dấu từ âm sang dương nên hàm số đạt cực tiểu tại $x = -2$.")
        st.markdown(r"Qua điểm $x = 1$, đạo hàm $f'(x)$ đổi dấu từ dương sang âm nên hàm số đạt cực đại tại $x = 1$.")
        st.markdown(r"**Chọn đáp án D.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")

# CÂU 38
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
        <span style="color: #008080; font-weight: bold;">Câu 38. </span> 
        <span style="color: #009900; font-weight: bold;">(ĐGNL DHSPHN 2026) </span>
        Tiệm cận xiên của đồ thị hàm số <span style="white-space: nowrap;">$y = \dfrac{x^2 + x + 2}{x + 2}$</span> là:
    </span>
    """, 
    unsafe_allow_html=True
)

options_38 = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ $y = x - 1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ $y = x + 1$.",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ $y = x - 2$.",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ $y = x + 2$."
]

user_choice_38 = st.radio(
    "Chọn đáp án của bạn (Câu 38):", 
    options_38, 
    index=None, 
    key="q38_radio", 
    horizontal=True 
)

if st.button("Kiểm tra đáp án", key="q38_check"):
    if user_choice_38 == options_38[0]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice_38 is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại nhé!")

if st.button("Xem lời giải chi tiết", key="q38_solution"):
    if st.session_state.get('logged_in', True): 
        st.info("Lời giải chi tiết:")
        st.markdown(r"Thực hiện phép chia đa thức tử cho mẫu, ta có:")
        st.markdown(r"$x^2 + x + 2 = (x + 2)(x - 1) + 4$")
        st.markdown(r"Do đó: $y = \dfrac{x^2 + x + 2}{x + 2} = x - 1 + \dfrac{4}{x + 2}$")
        st.markdown(r"Vì $\lim_{x \to \pm\infty} \left[ y - (x - 1) \right] = \lim_{x \to \pm\infty} \dfrac{4}{x + 2} = 0$, nên đường thẳng $y = x - 1$ là tiệm cận xiên của đồ thị hàm số.")
        st.markdown(r"**Chọn đáp án A.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")





