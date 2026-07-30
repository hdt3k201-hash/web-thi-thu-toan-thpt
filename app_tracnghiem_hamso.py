import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Trắc nghiệm Hàm số", layout="centered")

# ==========================================
# 1. QUẢN LÝ TRẠNG THÁI ĐĂNG NHẬP
# ==========================================
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

# ==========================================
# 2. GIAO DIỆN CHÍNH: CÂU HỎI TRẮC NGHIỆM
# ==========================================
st.title("Chuyên đề: Hàm số (Trắc nghiệm)")
st.markdown("---")

# Đề bài
st.markdown("**Câu 1:** Cho hàm số $y = x^3 - 3x + 2$. Tọa độ điểm cực đại của đồ thị hàm số là:")

# Danh sách 4 đáp án
options = [
    "A. (1; 0)",
    "B. (-1; 4)",
    "C. (-1; 0)",
    "D. (1; 4)"
]

# Sử dụng st.radio để tạo trắc nghiệm 4 đáp án
# index=None giúp mặc định không có đáp án nào được chọn sẵn
user_choice = st.radio("Chọn đáp án của bạn:", options, index=None, key="q1_radio")

# Nút kiểm tra đáp án
if st.button("Kiểm tra đáp án", key="q1_check"):
    if user_choice == "B. (-1; 4)":
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
        st.markdown("Tập xác định: $D = \mathbb{R}$")
        st.markdown("Đạo hàm:")
        
        # Streamlit hỗ trợ render trực tiếp LaTeX
        st.latex(r"y' = 3x^2 - 3")
        st.latex(r"y' = 0 \Leftrightarrow \left[\begin{array}{l} x = 1 \Rightarrow y = 0 \\ x = -1 \Rightarrow y = 4 \end{array}\right.")
        
        st.markdown("Lập bảng biến thiên, ta thấy hàm số đạt cực đại tại $x = -1$, giá trị cực đại $y_{CĐ} = 4$.")
        st.markdown("**Vậy tọa độ điểm cực đại là $(-1; 4)$. Chọn đáp án B.**")
    else:
        st.warning("🔒 Vui lòng Đăng nhập ở thanh menu bên trái để xem lời giải chi tiết.")
        
st.markdown("---")