import streamlit as st
import numpy as np
import math

st.set_page_config(page_title="Ngân hàng câu hỏi", layout="centered")

# 1. Đọc thông số từ URL (do WordPress truyền sang)
params = st.query_params

# Nếu trên URL có chứa tham số 'auth_status=success', tự động cho phép xem lời giải
if params.get("auth_status") == "success":
    st.session_state['logged_in'] = True
    st.sidebar.success("✅ Đã đồng bộ tài khoản từ Website!")
else:
    # Nếu không có tham số từ web, hiển thị form đăng nhập dự phòng như cũ
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

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



# 2. Giao diện chính hiển thị câu hỏi
# Tiêu đề chuyên đề căn giữa màn hình, màu xanh đậm (Dark Blue)
st.markdown(
    '<h2 style="text-align: center; color: red;">CHUYÊN ĐỀ: SỐ HỌC TSA</h2>',
    unsafe_allow_html=True
)
st.markdown("---")


import streamlit as st

# Tiêu đề câu hỏi
st.markdown(
    '<b style="color: blue;">Câu 1. [Trả lời ngắn ]</b>',
    unsafe_allow_html=True
)

# Nội dung câu hỏi 
st.markdown(r"""
Cho số tự nhiên $N = 202600$. Có bao nhiêu ước số nguyên dương của $N$ chia hết cho $10$?
""")

# --- Ô NHẬP ĐÁP ÁN VÀ KIỂM TRA ---
user_answer = st.text_input("Nhập số lượng ước số:", key="q1_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q1_check"):
    # Chuẩn hóa đầu vào (loại bỏ khoảng trắng thừa)
    normalized_user_answer = user_answer.strip()
    
    # Đáp án chính xác là 12
    if normalized_user_answer == "12":
        st.success("Chính xác! Cảm ơn bạn. Lời giải chi tiết đã được mở khóa.")
    elif user_answer == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy cẩn thận phân tích số $N$ ra thừa số nguyên tố và nhớ áp dụng quy tắc nhân nhé!")

# --- XEM LỜI GIẢI CHI TIẾT (ĐIỀU KIỆN ĐĂNG NHẬP) ---
st.markdown("---")

# Khởi tạo trạng thái hiển thị lời giải nếu chưa có
if 'q1_solution_shown' not in st.session_state:
    st.session_state['q1_solution_shown'] = False

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Xem lời giải chi tiết", key="q1_solution"):
        # Kiểm tra điều kiện đăng nhập
        if st.session_state.get('logged_in'):
            st.session_state['q1_solution_shown'] = True
        else:
            st.warning("🔒 Vui lòng Đăng nhập trên website để xem lời giải chi tiết.")
            st.session_state['q1_solution_shown'] = False 

# Hiển thị lời giải nếu được yêu cầu và thỏa mãn điều kiện
if st.session_state.get('q1_solution_shown') and st.session_state.get('logged_in'):
    st.info("### Hướng dẫn chi tiết:")
    
    st.markdown(r"""
    **Bước 1: Phân tích số $N$ ra thừa số nguyên tố:**
    
    Ta có:
    $$N = 202600 = 2026 \times 100$$
    $$N = (2 \times 1013) \times (2^2 \times 5^2)$$
    $$N = 2^3 \times 5^2 \times 1013^1$$
    
    **Bước 2: Tìm điều kiện của các ước số chia hết cho $10$:**
    
    Để một ước số $d$ của $N$ chia hết cho $10$ (tức là chia hết cho $2 \times 5$), thì $d$ phải có dạng $d = 2^x \times 5^y \times 1013^z$ trong đó:
    
    *   Số mũ $x \in \{1, 2, 3\}$ (có $3$ cách chọn, do $d$ phải chứa ít nhất thừa số $2^1$).
    *   Số mũ $y \in \{1, 2\}$ (có $2$ cách chọn, do $d$ phải chứa ít nhất thừa số $5^1$).
    *   Số mũ $z \in \{0, 1\}$ (có $2$ cách chọn).
    
    **Bước 3: Tính toán kết quả**
    
    Áp dụng quy tắc nhân, số lượng ước số thỏa mãn yêu cầu bài toán là:
    $$3 \times 2 \times 2 = 12 \text{ (ước số)}$$
    
    **Đáp số:** $12$
    """)
    
st.markdown("---")
