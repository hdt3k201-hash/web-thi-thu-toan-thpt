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

import streamlit as st

# CÂU 1
import streamlit as st

# CÂU 1
# ==========================================
# 1. Hiển thị đề bài trong khung
# MẸO QUAN TRỌNG: Dùng thẻ <span style="display: block;"> thay vì <div>
# để Streamlit không bỏ qua việc render công thức Toán LaTeX bên trong HTML.
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
    ">
        <span style="color: #008080; font-weight: bold;">Câu 1. </span> 
        <span style="color: #009900; font-weight: bold;">(THPT Lê Thánh Tông HCM 2026) </span>
        Tiệm cận ngang của đồ thị hàm số :
        
        $y = \dfrac{2x - 3}{x + 1}$ là đường thẳng có phương trình:
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
        
        # Đã cập nhật \dfrac cho lời giải chi tiết đẹp hơn
        st.latex(r"\lim_{x \to +\infty} y = \lim_{x \to +\infty} \dfrac{2x - 3}{x + 1} = 2")
        st.latex(r"\lim_{x \to -\infty} y = \lim_{x \to -\infty} \dfrac{2x - 3}{x + 1} = 2")
        
        st.markdown(r"Do đó, đường thẳng **$y = 2$** là tiệm cận ngang của đồ thị hàm số.")
        st.markdown("**Chọn đáp án C.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")
