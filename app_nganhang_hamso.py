import streamlit as st

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
st.title("Chuyên đề: Hàm số")
st.markdown("---")

# CÂU HỎI 1
st.markdown("**Câu 1:** Tìm giá trị lớn nhất của hàm số $y = -x^2 + 4x - 3$.")

# Học sinh nhập đáp án ngắn
user_answer_1 = st.text_input("Nhập đáp án của bạn (chỉ điền số):", key="q1_ans")

# Nút kiểm tra Đúng/Sai
if st.button("Kiểm tra đáp án", key="q1_check"):
    if user_answer_1.strip() == "1":
        st.success("Chính xác! Cảm ơn bạn.")
    elif user_answer_1 == "":
        st.warning("Bạn chưa nhập đáp án.")
    else:
        st.error("Sai rồi. Hãy kiểm tra lại tính toán nhé!")

# Nút xem lời giải chi tiết
if st.button("Xem lời giải chi tiết", key="q1_solution"):
    # Kiểm tra điều kiện đăng nhập
    if st.session_state['logged_in']:
        st.info("Lời giải chi tiết:")
        # Streamlit hỗ trợ render trực tiếp LaTeX
        st.latex(r"y = -x^2 + 4x - 3 = -(x^2 - 4x + 4) + 1 = -(x - 2)^2 + 1")
        st.markdown("Vì $-(x - 2)^2 \le 0$ với mọi $x$, nên $y \le 1$.")
        st.markdown("Dấu bằng xảy ra khi $x = 2$. Vậy $\max y = 1$.")
    else:
        st.warning("🔒 Vui lòng Đăng nhập để xem lời giải chi tiết.")
        
st.markdown("---")
