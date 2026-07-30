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
st.markdown("---")

# ==========================================
# CÂU 1
# ==========================================
# 1. Hiển thị đề bài trong khung, chữ "Câu 1." màu xanh ngọc (Đã sửa lại công thức toán)
st.markdown(
    """
    <div style="
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
        Cho hàm số y = x<sup>3</sup> - 3x + 2. Tọa độ điểm cực đại của đồ thị hàm số là:
    </div>
    """, 
    unsafe_allow_html=True
)

# 2. Danh sách 4 đáp án (Sử dụng LaTeX để tạo vòng tròn màu xanh ngọc)
# Ký hiệu r ở trước chuỗi giúp Python đọc đúng các mã lệnh của LaTeX
options = [
    r"$\color{#008080}{\textcircled{\small \textbf{A}}}\;$ (1; 0)",
    r"$\color{#008080}{\textcircled{\small \textbf{B}}}\;$ (-1; 4)",
    r"$\color{#008080}{\textcircled{\small \textbf{C}}}\;$ (-1; 0)",
    r"$\color{#008080}{\textcircled{\small \textbf{D}}}\;$ (1; 4)"
]

# 3. Sử dụng st.radio với tham số horizontal=True để dàn hàng ngang
user_choice = st.radio(
    "Chọn đáp án của bạn:", 
    options, 
    index=None, 
    key="q1_radio", 
    horizontal=True 
)

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q1_check"):
    # MẸO: Thay vì gõ lại chuỗi dài, ta so sánh với options[1] (Tức là đáp án B, vì đếm từ 0, 1, 2, 3)
    if user_choice == options[1]: 
        st.success("Chính xác! Chúc mừng bạn.")
    elif user_choice is None:
        st.warning("Bạn chưa chọn đáp án nào.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q1_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state['logged_in']:
        st.info("Lời giải chi tiết:")
        # Thêm chữ r vào trước chuỗi markdown để LaTeX \mathbb không bị lỗi
        st.markdown(r"Tập xác định: $D = \mathbb{R}$") 
        st.markdown("Đạo hàm:")
        
        # Streamlit hỗ trợ render trực tiếp LaTeX
        st.latex(r"y' = 3x^2 - 3")
        st.latex(r"y' = 0 \Leftrightarrow \left[\begin{array}{l} x = 1 \Rightarrow y = 0 \\ x = -1 \Rightarrow y = 4 \end{array}\right.")
        
        st.markdown("Lập bảng biến thiên, ta thấy hàm số đạt cực đại tại $x = -1$, giá trị cực đại $y_{CĐ} = 4$.")
        st.markdown("**Vậy tọa độ điểm cực đại là $(-1; 4)$. Chọn đáp án B.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")
        
st.markdown("---")
